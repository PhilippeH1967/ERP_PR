# Story 3.7: WBS Management & Dual Labels

Status: done

## Story
As a project manager, I want to manage a hierarchical WBS with both standard and client-facing labels, So that internal tracking uses standard nomenclature while client deliverables show customized names.

## Acceptance Criteria
- WBSElement has parent self-FK for hierarchy (parent nullable, CASCADE)
- standard_label and client_facing_label fields (client_facing_label defaults to empty string)
- ElementType enum: PHASE, TASK, SUBTASK
- WBS elements linked to project (CASCADE) and optionally to phase (CASCADE, nullable)
- WBSElementSerializer includes recursive children via SerializerMethodField
- WBSElementViewSet returns root-level elements (parent__isnull=True) with nested children
- __str__ returns client_facing_label if set, else standard_label

## Tasks / Subtasks
- [x] Define WBSElement model with parent self-FK (null=True, blank=True, related_name="children")
- [x] Add standard_label and client_facing_label CharField fields
- [x] Define ElementType TextChoices (PHASE, TASK, SUBTASK)
- [x] Add project FK and phase FK (nullable)
- [x] Add order, budgeted_hours, budgeted_cost, contract_value, is_billable fields
- [x] Implement __str__ returning client_facing_label or standard_label fallback
- [x] Create WBSElementSerializer with recursive get_children method
- [x] Create WBSElementViewSet filtering root elements per project
- [x] Write test for WBS hierarchy creation (parent-child relationship)

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- WBSElement with self-referential parent FK for unlimited nesting depth
- Dual-label system: standard_label for internal use, client_facing_label for external/client reports
- Recursive serializer renders full hierarchy tree in a single API call
- ViewSet only returns root nodes; children are nested via serializer
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (WBSElement, ElementType)
- backend/apps/projects/serializers.py (WBSElementSerializer with recursive children)
- backend/apps/projects/views.py (WBSElementViewSet)
- backend/apps/projects/urls.py (nested wbs route)
- backend/apps/projects/migrations/0001_initial.py
- backend/apps/projects/tests/test_models.py (TestWBSElement)
