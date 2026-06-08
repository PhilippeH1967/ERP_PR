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
| core (auth, tenant, RLS, permissions, sprints) | 282 | ✅ |
| projects (WBS, phases/tâches standard, services transversaux, équipes, avenants, agrégats) | 272 | ✅ |
| planning | 46 | ✅ |
| time_entries | 41 | ✅ |
| billing | 34 | ✅ |
| suppliers | 11 | ✅ |
| leaves | 8 | ✅ |
| dashboards | 8 | ✅ |
| consortiums | 6 | ✅ |
| expenses | 6 | ✅ |
| data_ops | 6 | ✅ |
| **Total** | **744** | **✅** |

> Les features récentes (catalogue `StandardTask` + `task_suggestions`, équipes `Team`
> + `assign_team`, visibilité projet interne `is_internal`, `construction_cost`,
> tâches internes obligatoires) sont couvertes — voir
> `apps/projects/tests/test_standard_tasks.py`, `apps/core/tests/test_teams.py`,
> `apps/projects/tests/test_internal_mandatory_tasks.py`.

## Tests frontend automatisés (Vitest)

```bash
cd frontend && npm run test:unit          # vitest run
cd frontend && npm run test:unit -- --watch
```

**130 tests** sur **24 fichiers** (`frontend/src/__tests__/*.spec.ts`). Couvrent
notamment : grille de saisie (timesheet, favoris, tâches obligatoires), Gantt
(chart, helpers, jalons slide-over), avancement par phase, picker de tâches
standard, panneau membres d'équipe, schémas fiscaux, et les écrans de
paramétrage admin **Équipes** (`teamSettings.spec.ts`) et **Tâches standard**
(`standardTaskSettings.spec.ts`).

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
