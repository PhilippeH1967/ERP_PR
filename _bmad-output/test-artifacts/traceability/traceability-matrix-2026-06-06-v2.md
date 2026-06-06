# Traceability Matrix & Quality Gate — Refonte structure v1.2 (RE-RUN v2)

**Date**: 2026-06-06 (re-run après corrections PR #23 + #24)
**Scope**: gate_type = release
**Mode**: deterministic
**Auteur**: BMad Master (TEA trace)
**Réf. précédent**: [traceability-matrix-2026-06-06.md](traceability-matrix-2026-06-06.md) — gate **CONCERNS**

> Re-run pour acter l'effet des corrections : N+1 (PR #24), test API tâche-mère (PR #23), extraction/test logique Gantt (PR #24).

## Évolution des points en réserve

| Réf. | Comportement | v1 | v2 | Test(s) ajouté(s) |
|---|---|---|---|---|
| #13 | Saisie refusée sur tâche-mère | ⚠️ Partial (serializer) | ✅ **Full** | `test_views::test_create_entry_on_parent_task_rejected` (API 400) + `test_create_entry_on_leaf_task_ok` (201) |
| #16 | Logique Gantt (`isAggregateTask`, `phasesWithTasks`, contrôle budget) | ❌ None | ✅ **Full (logique)** | `ganttHelpers.spec.ts` (10 tests) |
| #1 (perf) | N+1 agrégats de phase | ⚠️ non gardé | ✅ **Gardé** | `test_phase_task_aggregation::test_phase_list_no_n_plus_1` (assertNumQueries ≤15) |

## Matrice consolidée

| # | Comportement (refonte v1.2) | Couverture | Test(s) |
|---|---|---|---|
| 2–5 | Agrégation phase/tâche (budget, planif, réel, dates, rollup) | ✅ Full | `test_phase_task_aggregation` (13) |
| 6–7 | `StandardPhase` modèle + API admin | ✅ Full | `test_standard_phases` (8) |
| 8 | Phases projet admin-only (PM 403) | ✅ Full | `test_views::TestPhaseViewSet` |
| 9 | Wizard hérite du jeu standard | ✅ Full | `test_wizard_standard_phases` (2) |
| 10–12 | TimeEntry task-based (phase dérivée, unicité tâche, régression 2 tâches/phase) | ✅ Full | `time_entries/test_models`, `test_validation` |
| 13 | Saisie refusée sur tâche-mère (serializer **+ API**) | ✅ Full | `test_models` + `test_views` |
| 14 | Saisie : ne plus envoyer `phase` (front) | ✅ Full | `timesheet.spec` |
| 15 | Util structure (`visibleTaskGroups`, `isTaskReadOnly`) | ✅ Full | `taskStructure.spec` (5) |
| 16 | **Logique Gantt** (agrégat, phases visibles, budget) | ✅ Full | `ganttHelpers.spec` (10) |
| #1 | Perf : pas de N+1 agrégats phase | ✅ Gardé | `test_phase_list_no_n_plus_1` |
| 17 | Rendu **template** Gantt/Structure (DOM end-to-end) | ⚠️ Partial | logique testée ; rendu non testé |
| 18 | Écrans (wizard sans budget, vue d'ensemble, KPI) — DOM | ⚠️ Partial | non testé (UI monolithe) |

## Statistiques

- ✅ Full : **16** · ⚠️ Partial : **2** (rendu DOM des écrans) · ❌ None : **0**
- Intégrité données & sécurité : **100 % couvert**.
- Logique métier (backend + front extraite) : **couvert + gardé (perf)**.
- Seul reste : le **rendu DOM** end-to-end des gros composants Vue (logique sous-jacente déjà testée).

## Quality Gate — décision déterministe

- Aucun comportement critique (intégrité/sécurité) sans test : ✅
- Plus aucun trou ❌ None : ✅
- Réserves restantes = **rendu DOM** non critique (logique couverte) → ne bloque pas.

### → GATE : **PASS** *(avec note)*

**Note** : envisager, hors périmètre v1.2, des tests de **rendu** (Vue Test Utils) sur `GanttChart`/`ProjectDetail` si le risque UI augmente — ou des E2E Playwright (`testarch-automate`/`framework`). Non requis pour PASS.

---

*Généré par BMad Master · workflow `testarch-trace` (re-run) · lecture seule.*
