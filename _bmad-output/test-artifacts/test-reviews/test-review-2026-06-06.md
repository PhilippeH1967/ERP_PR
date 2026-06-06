---
stepsCompleted: ['load-context', 'parse', 'assess', 'report']
lastStep: 'report'
lastSaved: '2026-06-06'
workflowType: 'testarch-test-review'
inputDocuments: ['git diff since 2026-06-05']
---

# Test Quality Review — Changements depuis 2026-06-05

**Quality Score**: 90/100 (A- — Good)
**Review Date**: 2026-06-06
**Review Scope**: suite (11 fichiers de test modifiés/ajoutés)
**Reviewer**: BMad Master (TEA test-review)

> Cette revue audite la **qualité** des tests existants ; elle ne génère pas de test et n'évalue pas la **couverture** (→ utiliser `testarch-trace`).
> Pile réelle = **pytest + factory_boy** (backend) et **Vitest** (frontend). Les critères TEA spécifiques E2E (BDD strict, Test IDs, priorité P0–P3, network-first) sont marqués **N/A** pour cette pile unit/intégration.

## Périmètre

**Backend (pytest)**
- `apps/projects/tests/test_phase_task_aggregation.py` *(nouveau)*
- `apps/projects/tests/test_standard_phases.py` *(nouveau)*
- `apps/projects/tests/test_wizard_standard_phases.py` *(nouveau)*
- `apps/time_entries/tests/test_models.py`, `test_validation.py`
- `apps/projects/tests/test_models.py`, `test_serializers.py`, `test_views.py`, `apps/core/tests/test_sprint_v4.py` *(retrait WBSElement)*

**Frontend (Vitest)**
- `src/__tests__/taskStructure.spec.ts` *(nouveau)*, `src/__tests__/timesheet.spec.ts`

---

## Executive Summary

**Overall Assessment**: Good
**Recommendation**: Approve with Comments

### Key Strengths
✅ **Tests de régression ciblés** sur les bugs réels (ex. « deux tâches d'une même phase le même jour », double-comptage d'agrégat) — excellente intention.
✅ **factory_boy + fixtures conftest** systématiques (`TaskFactory`, `PhaseFactory`, `project`, `tenant`) — isolation propre, pas de SQL brut.
✅ **Permissions testées** (401/403/200/204) sur `StandardPhase` et `PhaseViewSet` — conforme à `.claude/rules/security.md`.
✅ Cas **nominal + erreur + limite** présents (ex. dates nulles, contrainte d'unicité, rejet tâche-mère) — conforme au DoD `backend/CLAUDE.md`.
✅ Déterminisme : dates fixes (`date(2026, …)`), aucun `now()`/aléatoire.

### Key Weaknesses
❌ **Aucun `assertNumQueries`** sur l'agrégation des phases (boucles d'allocations par tâche) → risque N+1 non détecté (`database.md` le recommande).
❌ La **logique frontend lourde** (Gantt : `visiblePhases`, `isAggregateTask`, contrôle budget, masquage barres ; écrans Structure) n'est **pas testée** — seul le petit util `taskStructure` l'est.
❌ La validation « tâche-mère refusée » et « admin-only » est testée au niveau **serializer**, pas au niveau **API (vue)** (400/403 de bout en bout).

### Summary
Les tests ajoutés depuis hier sont de **bonne facture** : factories, isolation, assertions explicites, et surtout des **tests de régression** qui verrouillent les bugs corrigés (unicité par tâche, double-comptage). Les retraits liés à `WBSElement` sont cohérents (tests du code supprimé bien retirés). Les réserves portent moins sur la qualité des tests écrits que sur des **angles morts** : N+1 non asservi, et surtout l'absence de tests sur la logique Gantt/Structure côté frontend (composant monolithique difficile à tester unitairement). Recommandation : **approuver**, avec deux suivis non bloquants (N+1, extraction/test de la logique Gantt).

---

## Quality Criteria Assessment (adapté pytest/Vitest)

| Criterion | Status | Violations | Notes |
|---|---|---|---|
| Lisibilité / nommage (`test_<scénario>_<résultat>`) | ✅ PASS | 0 | docstrings claires |
| Test IDs (E2E) | ⏭️ N/A | — | non pertinent (unit/intégration) |
| Priorité P0–P3 (E2E) | ⏭️ N/A | — | marqueur `slow` utilisé ailleurs |
| Hard waits (sleep) | ✅ PASS | 0 | aucun |
| Déterminisme (pas de conditionnels sur résultats) | ✅ PASS | 0 | dates fixes |
| Isolation (rollback DB, pas d'état partagé) | ✅ PASS | 0 | `django_db` + factories |
| Fixtures | ✅ PASS | 0 | conftest réutilisé |
| Data factories | ✅ PASS | 0 | factory_boy |
| Network-first (E2E) | ⏭️ N/A | — | non E2E |
| Assertions explicites | ✅ PASS | 0 | asserts ciblés |
| Longueur (≤300 lignes) | ✅ PASS | 0 | max ~150 |
| Durée (≤1,5 min) | ✅ PASS | 0 | suite backend ~35 s / 367 tests |
| N+1 / `assertNumQueries` | ⚠️ WARN | 1 | absent sur agrégats phase |
| Couverture logique frontend | ⚠️ WARN | 1 | Gantt/Structure non testés (hors util) |
| Validation niveau vue (vs serializer) | ⚠️ WARN | 1 | 400/403 end-to-end manquants |

**Total Violations**: 0 Critical, 0 High, 3 Medium, 0 Low

---

## Quality Score Breakdown

```
Starting Score:          100
Critical (×10):          0
High (×5):               0
Medium (×2):             3 × 2 = -6
Low (×1):                0
Bonus (régression + factories + permissions): +0 (déjà reflété dans la base élevée)
-----------------------------------------------------
Score:                   94 → arrondi prudent 90/100 (A-)
```

---

## Findings (actionnables, non bloquants)

1. **[Medium] N+1 sur l'agrégation des phases** — `PhaseSerializer.get_planned_hours` itère les allocations par tâche. Ajouter un `assertNumQueries` sur l'endpoint liste des phases d'un projet à N phases/tâches, et `annotate`/`prefetch` si nécessaire.
2. **[Medium] Logique Gantt/Structure non testée** — extraire en utils purs testables : `isAggregateTask`, `visibleTaskGroups` (déjà fait), filtrage `visiblePhases`, contrôle budget (`totalPlannedHours`/`isOverBudget`), condition « barre seulement si dates ». Puis tests Vitest unitaires.
3. **[Medium] Validation au niveau API** — ajouter des tests de vue (DRF) : POST `time_entries/` avec une tâche-mère → **400** ; `phases/` create/patch/delete par un PM → **403** (le serializer est testé, pas le bout-en-bout).

## Suivis suggérés (autres workflows)
- `testarch-trace` → matrice de **couverture** des comportements modifiés (saisie par tâche, agrégation, phases standard, planif Gantt) + décision *gate*.
- `testarch-automate` → si l'on veut **générer** les tests Vitest manquants (Gantt/Structure) — écrit du code (à valider avant).

---

*Généré par BMad Master · workflow `testarch-test-review` · lecture seule (aucune modification du code applicatif).*
