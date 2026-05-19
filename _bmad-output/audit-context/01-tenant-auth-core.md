# Contexte d'audit — Cœur isolation tenant + auth (pure-contexte)

> Skill : `audit-context-building` (Trail of Bits). Mode pure-contexte :
> AUCUN finding / fix / exploit / sévérité. Construction de compréhension uniquement.
> Date : 2026-05-19. Scope : isolation multi-tenant + authentification.

## Phase 1 — Orientation (anchors)

| Module | Rôle sécurité | Entrypoints |
|---|---|---|
| `apps/core/middleware.py:TenantMiddleware` | Résout + injecte tenant, pose `app.current_tenant` PG (RLS) | `__call__`, `_extract_tenant_from_jwt` |
| `apps/core/auth.py` | JWT login/refresh, `/auth/me`, `/auth/config`, `user_search` | endpoints DRF |
| `apps/core/permissions.py` | `IsAdmin`, `IsFinance`, `HasProjectRole` + règles `rules` | `has_permission` |
| `apps/core/models.py` | `Tenant`, `ProjectRole`, `UserTenantAssociation` | ORM |

Acteurs : user authentifié (JWT), anonyme, admin tenant, superuser Django, autre-tenant (adverse).
État critique : `request.tenant_id`, var PG `app.current_tenant`, claim JWT `tenant_id`, header `X-Tenant-Id`.

## Phase 2 — Micro-analyse `TenantMiddleware.__call__` (L36-95)

Purpose : point unique d'application de l'isolation multi-tenant infra DB.
Propage le tenant à 2 niveaux : `request.tenant_id` (Python) + `SET app.current_tenant` (PG/RLS).

Hypothèses clés :
- a1 : `TENANT_EXEMPT_PATHS` couvre exactement les routes légitimement sans tenant.
- a2 : claim `tenant_id` du JWT fiable une fois signé.
- a3 (CRITIQUE) : le `SET` session cible la connexion qui sert la requête — dépend du mode pgbouncer + ATOMIC_REQUESTS. NON PROUVÉ.
- a4 : `Tenant.objects.get` (L73) n'est pas soumise à RLS (sinon récursion).
- a5 : un seul tenant par requête.

Blocs :
- L38-41 exempt paths : rupture délibérée de l'invariant "toute requête a un tenant". Incohérence enregistrée : middleware exempte `/admin/` mais Django admin déplacé sur `/django-admin/` (commit e9432a5) ; `/admin/*` sert le SPA Vue (pas de requête DB → sans impact mais anchor).
- L47-48 fallback `X-Tenant-Id` : a-hdr — rien dans CE code n'empêche un header forgé ; sûreté déléguée à la config d'auth DRF globale. Le `SET` RLS a déjà eu lieu avant le rejet 401 éventuel → couplage a3.
- L55-67 cast int : normalise type avant ORM. Invariant : tenant_id est int après L67.
- L69-84 validation : `Tenant.objects.get(pk=, is_active=True)` re-validé à CHAQUE requête → révocation tenant immédiate (bon couplage I4).
- L86-88 `SET app.current_tenant` (session, pas LOCAL) : I1 candidat non prouvé (a3). pgbouncer transaction-pooling pourrait faire fuiter le SET entre requêtes/tenants — unclear, à inspecter setup_rls + pool mode.

## Micro-analyse `_extract_tenant_from_jwt` (L97-110)

`AccessToken(token, verify=False)` : décode SANS vérifier la signature.
a-jwt1 : DRF re-vérifie plus tard. a-jwt2 : lire un claim non vérifié pour le SET RLS
serait sûr SI le SET est annulé quand l'auth échoue → dépend de a3.
`except Exception: return None` = fail vers fallback header (L47).
Règle skill : JWT non vérifié = donnée client = adverse jusqu'à preuve.

## Phase 3 — Invariants candidats

- I1 : requête servie sous `app.current_tenant == request.tenant_id` pour ses requêtes DB. NON PROUVÉ (a3).
- I2 : `request.tenant_id ∈ {None, int Tenant actif}`. Tenu (L55-84).
- I3 : routes exemptes n'accèdent à aucune donnée tenant-scoped. À vérifier route par route.
- I4 : désactivation Tenant effective à la requête suivante. Tenu (L73).

Clusters de fragilité (orientation future, PAS findings) :
1. `SET` session ↔ pgbouncer ↔ ATOMIC_REQUESTS (a3, 3 hypothèses convergent).
2. Claim JWT non vérifié pour décision sécurité (a-jwt2) ↔ a3.
3. Exemption `startswith` large + incohérence `/admin/` vs `/django-admin/`.
4. Fallback `X-Tenant-Id` sans garde explicite dans ce code (a-hdr).

Correction de modèle : `/admin/*` = SPA Vue (e9432a5) ; Django admin = `/django-admin/`.
Middleware exempte encore `/admin/` et PAS `/django-admin/`.

## Suite (fichiers non encore micro-analysés)
1. `auth.py:TokenObtainPairSerializer` — injection claim tenant_id (maillon confiance).
2. Pattern `get_queryset` tenant-filtré dans les ViewSets — uniformité.
3. `setup_rls.py` — politiques RLS réelles (résout a3/a4/I1).
4. `config/settings/*` — MIDDLEWARE order, ATOMIC_REQUESTS, DATABASES pgbouncer.
