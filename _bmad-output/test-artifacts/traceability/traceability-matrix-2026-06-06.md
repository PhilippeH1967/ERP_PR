# Traceability Matrix & Quality Gate — Refonte structure v1.2

**Date**: 2026-06-06
**Scope**: gate_type = release (changements depuis 2026-06-05)
**Mode**: deterministic
**Auteur**: BMad Master (TEA trace)

> Mappe chaque **comportement modifié** à ses tests. Niveaux : unit / intégration (pytest), unit (Vitest). Pas de E2E sur ce périmètre.

## Matrice

| # | Comportement (modif v1.2) | Test(s) | Niveau | Couverture |
|---|---|---|---|---|
| 1 | Suppression `WBSElement` | retrait tests legacy ; migration `0012` | — | ✅ (code/test retirés) |
| 2 | Phase agrège budget/$ des tâches **saisissables** (no double-count) | `test_phase_task_aggregation::TestPhaseAggregation` | intégration | ✅ Full |
| 3 | Phase : `planned_hours`/`actual_hours` via `task__phase` | idem (`test_planned_hours_*`, `test_actual_hours_*`) | intégration | ✅ Full |
| 4 | Phase : dates `min/max` des tâches | `test_dates_aggregate_min_max_from_tasks`, `test_dates_null_when_no_task_dates` | intégration | ✅ Full |
| 5 | Tâche : `is_chargeable`, `effective_budgeted_*`, rollup mère | `TestTaskChargeable`, `TestParentTaskRollup` | intégration | ✅ Full |
| 6 | `StandardPhase` : modèle, unicité, seed idempotent | `test_standard_phases::TestStandardPhaseModel`, `TestSeedStandardPhases` | unit | ✅ Full |
| 7 | `StandardPhase` API : lecture auth, écriture **admin** | `TestStandardPhasePermissions` (401/403/200/204) | intégration | ✅ Full |
| 8 | Phases projet : écriture **admin-only** (PM 403) | `test_views::TestPhaseViewSet::test_pm_cannot_*` | intégration | ✅ Full |
| 9 | Wizard hérite du jeu standard (+ fallback template) | `test_wizard_standard_phases` (2 cas) | intégration | ✅ Full |
| 10 | TimeEntry : phase **dérivée** de la tâche | `test_models::test_phase_derived_from_task` | unit | ✅ Full |
| 11 | TimeEntry : unicité **sur la tâche** | `test_unique_constraint_on_task`, `test_validation::test_duplicate_entry_rejected` | unit/intégration | ✅ Full |
| 12 | **Régression** : 2 tâches même phase / même jour OK | `test_two_tasks_same_phase_same_date_ok` | unit | ✅ Full |
| 13 | Saisie refusée sur tâche-mère (serializer) | `test_serializer_rejects_parent_task`, `test_serializer_accepts_leaf_task` | unit | ⚠️ Partial (serializer, pas API) |
| 14 | Saisie de temps : ne plus envoyer `phase` (front) | `timesheet.spec::saveCell par tâche` | unit | ✅ Full |
| 15 | Util structure : `visibleTaskGroups`, `isTaskReadOnly` | `taskStructure.spec` (5 cas) | unit | ✅ Full |
| 16 | **Gantt** : `isAggregateTask`, `visiblePhases`, barre si dates, contrôle budget rouge | — | — | ❌ **None** |
| 17 | Écrans Structure (Phases lecture seule, Tâches Déplacer/agrégat, masquage vides) | partiel via #15 | — | ⚠️ Partial |
| 18 | Wizard sans budget phase ; vue d'ensemble agrégats ; KPI heures planifiées | — | — | ❌ None (UI) |

## Statistiques

- Comportements tracés : **18**
- ✅ Full : **12** · ⚠️ Partial : **3** · ❌ None : **3**
- Backend : **couverture quasi complète** (intégrité + permissions + régressions).
- Frontend : **trous** sur la logique Gantt (#16) et les écrans Structure/vue d'ensemble (#17, #18) — composant monolithique non testé.

## Quality Gate — décision déterministe

Règle : *FAIL* si un comportement critique (intégrité/sécurité) sans couverture ; *CONCERNS* si trous sur logique non critique ; *PASS* sinon.

- Intégrité (unicité tâche, double-comptage, phase dérivée, dates) : ✅ couvert.
- Sécurité (admin-only phases/standard) : ✅ couvert.
- Trous : **logique UI Gantt/Structure** (non critique sur le plan données/sécurité, mais sensible métier).

### → GATE : **CONCERNS**

Rien de bloquant côté données/sécurité (tout est couvert). Les réserves sont les **3 trous frontend** (#16–#18). Recommandation : lever #16 (Gantt) en priorité car il porte des règles métier (agrégat non cliquable, contrôle budget).

## Actions pour passer à PASS
1. Tester la logique **Gantt** (#16) — nécessite d'**extraire** `isAggregateTask` / filtrage `visiblePhases` / contrôle budget en utils purs (⚠️ **modifie du code applicatif**).
2. Test **API** de la règle « tâche-mère → 400 » (#13) — *test-only*.
3. (Option) `assertNumQueries` sur l'agrégation des phases — *test-only*.

---

*Généré par BMad Master · workflow `testarch-trace` · lecture seule.*
