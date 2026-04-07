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

### Couverture par module

| Module | Tests | Statut |
|--------|-------|--------|
| projects | 17 | ✅ |
| time_entries | 17 | ✅ |
| billing | 18 | ✅ |
| leaves | 8 | ✅ |
| planning | 5 | ✅ |
| suppliers | 11 | ✅ |
| consortiums | 6 | ✅ |
| expenses | 6 | ✅ |
| core (tenant isolation) | 9 | ✅ |
| **Total** | **~100** | **✅** |

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
