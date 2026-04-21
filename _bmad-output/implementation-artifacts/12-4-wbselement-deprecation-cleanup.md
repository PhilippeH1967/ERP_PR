# Story 12.4: WBSElement Deprecation Cleanup (Dette Technique B2)

Status: draft

## Story
As a **developer maintaining the project module**, I want to remove the deprecated `WBSElement` model and all its associated code paths (ViewSet, serializer, admin, API, frontend types and calls), So that the codebase has a single canonical WBS representation via `Phase` → `Task` and new contributors are not confused by parallel implementations.

## Context
- `WBSElement` was the original WBS model. It has been **replaced by `Task`** (story 3.7 + migration `0003_create_task_model.py`).
- The deprecation was documented in `backend/apps/projects/models.py:274-306` with the comment : *"DEPRECATED — Use Task model instead. Kept for migration compatibility."*
- The model still coexists, creating :
  - Duplicate data paths (WBSElement vs Task)
  - Confusion for new contributors
  - Unnecessary endpoint `/api/projects/{id}/wbs/` still exposed
  - ChangePoint import still writes to `WBSElement` instead of `Task`
- **Décision B2 actée** (Philippe, 2026-04-21) : retirer complètement `WBSElement`.
- Reference : `_bmad-output/planning-artifacts/module-projets.md` §9.4, §10.1.

## Inventory of references to remove

### Backend (10 files, 38 occurrences)
| Fichier | Rôle |
|---|---|
| `apps/projects/models.py` L274-306 | Définition modèle `WBSElement` |
| `apps/projects/urls.py` L12, L24 | Import + route `r"wbs"` |
| `apps/projects/views.py` (5 ref.) | `WBSElementViewSet` + actions |
| `apps/projects/serializers.py` (4 ref.) | `WBSElementSerializer` |
| `apps/projects/admin.py` (3 ref.) | Inscription admin |
| `apps/projects/migrations/0001_initial.py` | Création table `projects_wbs_element` |
| `apps/projects/migrations/0003_create_task_model.py` L1 | Docstring (mention, garder) |
| `apps/projects/tests/test_models.py` (4 ref.) | Tests legacy à retirer |
| `apps/data_ops/management/commands/import_changepoint.py` L375, L387 | Import ChangePoint → migrer vers `Task` |
| `apps/core/tests/test_sprint_v4.py` (6 ref.) | Tests legacy à retirer |

### Frontend (3 files)
| Fichier | Rôle |
|---|---|
| `features/projects/types/project.types.ts` L56, L67 | Interface `WBSElement` + `children` |
| `features/projects/api/projectApi.ts` L2, L36-42 | Méthodes `listWBS`, `create/update/deleteWBSElement` |
| `features/projects/views/ProjectDetail.vue` L292, L295, L322, L791 | 4 appels frontend |

## Acceptance Criteria

### AC1 — ChangePoint import migré vers Task
- **Given** the ChangePoint import script currently writes to `WBSElement`
- **When** the import is migrated
- **Then** the script creates `Phase` + `Task` rows instead (using the existing Task model)
- **And** a re-run of the import on a staging snapshot produces the same logical data
- **And** existing tests for the ChangePoint import still pass

### AC2 — Backward-compatible data migration
- **Given** a database with existing `projects_wbs_element` rows
- **When** the cleanup migration runs
- **Then** any orphan WBSElement row without a corresponding `Task` is migrated via `RunPython` (copy `standard_label`, `client_facing_label`, `budgeted_hours`, `budgeted_cost`, `contract_value`, `is_billable`, parent linkage)
- **And** the `RunPython` function has a symmetric `reverse` (per database.md rule on backfills)
- **And** on Hostinger staging, row count pre/post matches expected (zero data loss)

### AC3 — Backend code removal
- **Given** the cleanup migration has run
- **When** the developer removes `WBSElement` code
- **Then** :
  - Model removed from `models.py`
  - `WBSElementViewSet` + serializer + admin unregistered
  - Route `/wbs/` removed from `urls.py`
  - Tests targeting `WBSElement` removed (pas remplacés — les équivalents `Task` existent déjà)
- **And** `python manage.py makemigrations --check` passe
- **And** `pytest apps/projects/` et `pytest apps/core/` passent (tests régression OK)
- **And** `ruff check .` propre

### AC4 — Frontend code removal
- **Given** the backend no longer exposes `/wbs/`
- **When** the developer removes frontend references
- **Then** :
  - Interface `WBSElement` supprimée de `project.types.ts`
  - Méthodes `listWBS`, `create/update/deleteWBSElement` supprimées de `projectApi.ts`
  - Fonctions `createWBSElement`, `updateWBSElement`, `deleteWBSElement` retirées de `ProjectDetail.vue`
  - L'UI qui les appelait est **déjà remplacée** par les composants Phase/Task (vérifier — sinon la story devient bloquante)
- **And** `npm run type-check` propre
- **And** `npm run lint` propre
- **And** `npm run test:unit` + `npm run test:e2e` passent

### AC5 — Migration de suppression finale
- **Given** all code references are removed
- **When** the final migration runs
- **Then** `DeleteModel("WBSElement")` supprime la table `projects_wbs_element`
- **And** la migration est **séparée** de AC2 (ordre : backfill → dépréciation code → drop table)
- **And** validation utilisateur requise avant merge (confirmation explicite Philippe, per database.md §Destructivité)

### AC6 — Documentation
- **Given** WBSElement est retiré
- **When** un contributeur consulte `module-projets.md`
- **Then** §10.1 marque le point comme **✅ résolu** avec la date
- **And** toute référence résiduelle à `WBSElement` dans la doc est supprimée

## Tasks / Subtasks

### Backend — Phase 1 : Audit & Migration ChangePoint
- [ ] **TDD first** — écrire tests confirmant que l'import ChangePoint crée bien des `Task` (et pas des `WBSElement`)
- [ ] Modifier `apps/data_ops/management/commands/import_changepoint.py` L375, L387 pour utiliser `Phase` + `Task` au lieu de `WBSElement`
- [ ] Re-tester l'import ChangePoint sur un dump staging

### Backend — Phase 2 : Backfill data
- [ ] Créer migration `apps/projects/migrations/00XX_backfill_wbselement_to_task.py`
- [ ] `RunPython` : pour chaque `WBSElement` sans `Task` équivalent, créer un `Task` (avec mapping approprié)
- [ ] Fonction `reverse` symétrique obligatoire
- [ ] Tester sur une copie DB prod (instruction database.md)

### Backend — Phase 3 : Code removal
- [ ] Retirer `WBSElement` de `models.py`
- [ ] Retirer `WBSElementViewSet` de `views.py`
- [ ] Retirer `WBSElementSerializer` de `serializers.py`
- [ ] Retirer inscription admin dans `admin.py`
- [ ] Retirer route `r"wbs"` de `urls.py`
- [ ] Retirer tests legacy (`test_models.py` + `test_sprint_v4.py`)

### Backend — Phase 4 : Migration de suppression
- [ ] Créer migration `apps/projects/migrations/00YY_delete_wbselement.py` avec `DeleteModel("WBSElement")`
- [ ] **Confirmer avec Philippe avant merge** (per database.md §Destructivité)
- [ ] Vérifier `makemigrations --check`

### Frontend
- [ ] Retirer interface `WBSElement` de `types/project.types.ts`
- [ ] Retirer méthodes WBS de `api/projectApi.ts`
- [ ] Retirer fonctions `createWBSElement`, `updateWBSElement`, `deleteWBSElement` dans `ProjectDetail.vue`
- [ ] **Vérifier** que l'UI ne dépend plus de ces méthodes — sinon stop et rééval
- [ ] `npm run type-check` + `npm run lint` + `npm run test:unit` + `npm run test:e2e` passent

### Documentation
- [ ] Update `module-projets.md` §10.1 → ✅ résolu avec date
- [ ] Update `epics.md` si Epic 3 Story 3.7 (WBS dual labels) doit être annotée

### Déploiement (Hostinger)
- [ ] Appliquer la migration de backfill (Phase 2) sur staging, valider la cohérence des données
- [ ] Valider fonctionnellement (feuilles de temps, planning, Gantt fonctionnent)
- [ ] Appliquer la migration de suppression (Phase 4) après confirmation Philippe
- [ ] Vérifier qu'aucun appel à `/api/projects/*/wbs/` ne reste dans les logs

## Tests

### Backend (pytest + factory_boy)
- [ ] `test_changepoint_import_creates_tasks_not_wbselement` — validation Phase 1
- [ ] `test_backfill_migration_creates_equivalent_task_rows` — validation Phase 2
- [ ] `test_backfill_migration_reverse_restores_wbselement` — symétrie reverse
- [ ] `test_no_wbselement_imports_remain` — grep dans tests CI (`assert no 'WBSElement' in apps.projects`)
- [ ] `test_no_wbs_route_exposed` — `GET /api/projects/{id}/wbs/` → 404 après cleanup
- [ ] Vérifier que les tests Task existants couvrent les cas qui étaient dans `test_sprint_v4.py` — sinon compléter

### Frontend (Vitest + Playwright)
- [ ] Vitest : aucun import de `WBSElement` dans le build
- [ ] Playwright E2E : feuilles de temps, planning, Gantt, création projet — tous fonctionnels sans WBSElement

## Risks & Open Questions

### Risques
- **Risque critique** : si l'UI actuelle de ProjectDetail.vue utilise encore `createWBSElement/updateWBSElement` pour l'édition (L292, L322), il faut d'abord vérifier que la colonne Task/Phase existe côté UI. Si non, cette story devient bloquante sur une story préalable "Migrer l'UI WBS vers Task".
- **Risque** : la commande `import_changepoint` est utilisée en prod pour les imports initiaux. Un bug dans la migration vers Task peut bloquer l'onboarding de nouveaux clients.
- **Risque** : ordre des migrations — si `DeleteModel` est appliqué avant backfill, perte de données.

### Questions ouvertes
- **Q1** : Le champ `contract_value` sur WBSElement a-t-il un équivalent sur Task ? Si non, vérifier si l'info est utile ou si on peut la perdre.
- **Q2** : Les données existantes sur Hostinger staging ont-elles été migrées de WBSElement vers Task, ou les deux cohabitent-elles encore ? **Vérifier avant de lancer la migration.**
- **Q3** : Les rapports ChangePoint utilisent-ils encore WBSElement via l'API ? Si oui, prévoir communication.

## Dev Agent Record
### Agent Model Used
_To be filled by dev agent_
### Completion Notes List
_To be filled during implementation_
### Change Log
- 2026-04-21: Story drafted from module-projets.md §9.4 + §10.1 (décision B2 actée)
### File List
_To be filled during implementation_

## References
- [_bmad-output/planning-artifacts/module-projets.md](../planning-artifacts/module-projets.md) §9.4, §10.1
- [_bmad-output/planning-artifacts/epics.md](../planning-artifacts/epics.md) Epic 3 Story 3.7
- [.claude/rules/database.md](../../.claude/rules/database.md) — Destructivité, Backfill, DROP
- [.claude/rules/deployment.md](../../.claude/rules/deployment.md) — Hostinger migration steps
- [backend/apps/projects/models.py:274-306](../../backend/apps/projects/models.py#L274-L306) — définition deprecated
- Story 3.7 (WBS Management Dual Labels) — historique Task
- Migration `0003_create_task_model.py` — bascule historique
