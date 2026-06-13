# Tests

## Tests backend automatisés

```bash
# Tous les tests
docker compose exec django python -m pytest

# Par module
docker compose exec django python -m pytest apps/projects/
docker compose exec django python -m pytest apps/time_entries/
docker compose exec django python -m pytest apps/billing/
docker compose exec django python -m pytest apps/leaves/
docker compose exec django python -m pytest apps/planning/
docker compose exec django python -m pytest apps/suppliers/
docker compose exec django python -m pytest apps/consortiums/

# Avec verbose
docker compose exec django python -m pytest -v --tb=short
```

### Couverture par module (pytest)

| Module | Tests | Statut |
|--------|-------|--------|
| core (auth, tenant, RLS, permissions, sprints) | 290 | ✅ |
| projects (WBS, standards, services transversaux, équipes, avenants, billing_address, agrégats) | 291 | ✅ |
| planning | 46 | ✅ |
| time_entries (blocages, discipline, immuabilité heures facturées) | 100 | ✅ |
| billing | 34 | ✅ |
| clients (dont anti-doublon adresses) | 27 | ✅ |
| suppliers | 11 | ✅ |
| leaves | 8 | ✅ |
| dashboards | 8 | ✅ |
| consortiums | 6 | ✅ |
| expenses | 6 | ✅ |
| data_ops | 6 | ✅ |
| **Total** | **833** | **✅** |

> Les features récentes (catalogue `StandardTask` + `task_suggestions`, équipes `Team`
> + `assign_team`, visibilité projet interne `is_internal`, `construction_cost`,
> tâches internes obligatoires) sont couvertes — voir
> `apps/projects/tests/test_standard_tasks.py`, `apps/core/tests/test_teams.py`,
> `apps/projects/tests/test_internal_mandatory_tasks.py`.
>
> **PR #74 — invariants feuilles de temps (41 nouveaux tests) :**
> - `test_invoiced_immutability.py` : 15 tests — verrou modèle (`save()` + signal
>   `pre_delete`), API `bulk_correct`, `transfer_hours`, `reject_entries`, `reject_pm`,
>   suppression de tâche avec entrées facturées.
> - `test_submission_discipline.py` : 26 tests — discipline LATE_TIMESHEETS sur tous
>   les chemins d'écriture (`create`, `update`, `copy_previous_week`,
>   `prefill_holidays`) ; régularisation des semaines en retard toujours permise.

## Tests frontend automatisés (Vitest)

```bash
cd frontend && npm run test:unit          # vitest run
cd frontend && npm run test:unit -- --watch
```

**204 tests** sur **33 fichiers** (`frontend/src/__tests__/*.spec.ts`). Couvrent
notamment : grille de saisie (timesheet, favoris, tâches obligatoires), Gantt,
fiche tâche unique (`taskSlideOver`), dialogue d'affectation unifié
(`assignResourceDialog`), onglet ⚙️ Paramètres du projet (`projectSettingsTab` —
client, adresses, adresse de facturation par projet), aide contextuelle
(`helpContent`/`helpPanel`), échéancier (`scheduleHelpers`), arbre Équipe & charge
(`phasePeopleTree`), écrans admin (Équipes, Tâches standard), schémas fiscaux,
discipline de soumission et immuabilité des heures facturées (`timesheetDiscipline`).

**PR #74 — 14 nouveaux tests Vitest (`timesheetDiscipline.spec.ts`) :**
- helpers de dates : `getMondayOfWeek` sans dérive UTC le soir (fuseaux ouest),
  `getDatesForWeek` avec dates locales
- store : `lateBlocked` actif sur semaine courante seulement, `fetchWeek` ne
  pré-remplit pas les fériés si saisie bloquée, `saveCell` expose le message
  backend, `goToWeek` vide les entrées immédiatement
- `TimesheetCell` : message d'erreur backend affiché, flash succès uniquement
  en cas de réponse 2xx

E2E Playwright : `cd frontend && npm run test:e2e`.

## Intégration continue (GitHub Actions)

`.github/workflows/ci.yml` — sur chaque push / PR : service PostgreSQL,
`config.settings.test` (cache LocMem), gate **ruff** bloquant
(`--select F,B,S,UP,I`) + ruff complet non bloquant, puis frontend
(`type-check`, `lint`, `test:unit`). Pas de merge si la CI échoue.

## Tests visuels (humains)

Fichier : `tests_visuels/plan_tests_complet_v3.xlsx`

### 13 onglets — 357 tests

| Onglet | Tests |
|--------|-------|
| 01 — Auth & Navigation | 22 |
| 02 — Clients | 10 |
| 03 — Projets | 76 |
| 04 — Feuilles de temps | 96 |
| 05 — Congés | 10 |
| 06 — Fournisseurs ST | 18 |
| 07 — Planification | 9 |
| 08 — Facturation | 30 |
| 09 — Dépenses | 14 |
| 10 — Exports Intacct | 6 |
| 11 — Consortium | 14 |
| 12 — Dashboard & Admin | 41 |
| 13 — Gantt | 11 |

### Dernier rapport QA

Fichier : `tests_visuels/rapport_tests_ERP_v1.2.000_workflows.xlsx`

Résultat : 107 PASS, 4 FAIL (corrigés), 7 PARTIAL, 33 SKIP (imports exclus)
