# Audit — Surface hors-requête & chiffrage activation DB_APP_USER

> Pré-requis à l'activation de `DB_APP_USER` (rôle non-superuser) avec
> RLS `FORCE` déjà en place en prod. Objet : recenser TOUT code qui
> touche une table tenant-scoped sans passer par `TenantMiddleware`,
> donc sans `app.current_tenant` posé → casserait sous rôle non-superuser.

## Méthode

Recherche exhaustive : `@shared_task` / `.delay(` / `.apply_async`,
`CELERY_BEAT_SCHEDULE`, `apps/*/management/commands/*`, appels de
`services.py` hors vues, signals. Surface **bornée et petite**.

## Résultat — 3 catégories

### A. Tâches Celery — CHANGEMENT DE CODE REQUIS (3 points)

Exécutées par celery-beat, aucun flag manuel possible → doivent poser
`app.current_tenant` dans le code.

| Tâche | Fichier | Tables tenant-scoped touchées | État |
|---|---|---|---|
| `expire_delegations` | core/tasks.py:11 | `core_delegation` (`.update()` **global cross-tenant**) | ⚠️ à **restructurer** en boucle par tenant |
| `send_timesheet_reminders` | time_entries/tasks.py:39 | `time_entries_weekly_approval`, `notifications_notification` | ✅ déjà `for tenant in Tenant…` → wrapper le corps |
| `escalate_missing_timesheets` | time_entries/tasks.py:90 | `time_entries_weekly_approval`, `core_project_role`, `planning_allocation`, `notifications_notification` | ✅ déjà boucle par tenant → wrapper le corps |

Note : `Tenant.objects.filter(is_active=True)` (driver de boucle) n'est
PAS tenant-scoped → l'itération elle-même reste valide sous non-superuser ;
seul le **corps** par tenant doit être sous contexte.
`UserTenantAssociation` n'est pas tenant-scoped non plus (OK).

### B. Commandes management — AUCUN CODE, flag opérationnel (11 cmd)

Lancées manuellement par un admin → `DJANGO_DB_PRIVILEGED=1` (rôle
propriétaire/superuser bypasse RLS). Déjà le pattern documenté pour
`migrate`/`setup_rls`.

- DDL/rôles : `setup_rls`, `setup_db_roles` (déjà privilégié par nature)
- Seed/import (INSERT tenant-scoped) : `import_changepoint`,
  `import_changepoint_data`, `import_reference_data`,
  `seed_reference_data`, `seed_test_users`, `create_admin_account`,
  `seed_templates`, `seed_leave_types`, `seed_expense_categories`

→ **0 ligne de code**, juste discipline runbook (1 ligne de doc à
généraliser dans deployment.md).

### C. Aucune autre surface

- `services.py` (dashboards, etc.) : appelés **uniquement** depuis des
  vues (dans le cycle requête → middleware pose le tenant). Aucun appel
  depuis tâche/commande.
- Aucun `.delay()` / `.apply_async()` ailleurs → pas de notification
  asynchrone hors des 3 tâches ci-dessus.
- Signals SSO (`signals.py`) : ne touchent que `Tenant` /
  `UserTenantAssociation` (non tenant-scoped). RAS.
- Web/API : déjà couvert par `TenantMiddleware`.

## Chiffrage du chantier

| Lot | Détail | Effort |
|---|---|---|
| 1. Helper `tenant_context(tenant_id)` | context manager : `SET app.current_tenant` à l'entrée, `RESET` en `finally` (anti-fuite entre itérations, connexions Celery persistantes). + tests unitaires. | **S** (~20 lignes + 3 tests) |
| 2. `escalate_missing_timesheets` + `send_timesheet_reminders` | envelopper le corps de boucle `for tenant` par `with tenant_context(tenant.id):`. + tests | **S** (2 edits, déjà la bonne forme) |
| 3. `expire_delegations` | transformer le `.update()` global en boucle `for tenant in Tenant.active` + `with tenant_context`. + test | **S** (1 petite restructuration) |
| 4. Doc runbook | généraliser « commandes seed/import → `DJANGO_DB_PRIVILEGED=1` » dans deployment.md | **XS** (doc) |
| 5. (option) Filet de sécurité | commande `check_rls` qui vérifie qu'une requête tenant-scoped sans contexte échoue bien sous le rôle app (smoke post-déploiement) | **S** (optionnel) |

**Total : 3 points de code** (tous dans 2 fichiers `tasks.py`),
**1 helper partagé**, **0 changement dans les 11 commandes** (flag
opérationnel), **0 dans les services/web**.

## Conclusion

> **STATUT : IMPLÉMENTÉ** (TDD). Helper `apps/core/tenant_context.py`,
> 3 tâches Celery enveloppées, doc runbook ajoutée, tests verts
> (test_tenant_context, test_tasks core + time_entries). `DB_APP_USER`
> peut désormais être activé sans casser Celery.

Chantier **petit et cerné** : ~½ journée dev (lots 1–4, TDD inclus).
Le risque «Celery casse» se réduit à **3 tâches** grâce à un helper
unique. Pré-requis avant de positionner `DB_APP_USER` en prod ;
indépendant du nombre de compagnies (1 aujourd'hui) — à faire avant
l'onboarding d'une 2ᵉ société.
