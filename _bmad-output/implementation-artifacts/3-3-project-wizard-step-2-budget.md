# Story 3.3: Project Wizard Step 2 — Budget

Status: done

## Story
As a project manager, I want to define budgeted hours and costs per phase and WBS element, So that the project has a clear financial baseline for tracking and billing.

## Acceptance Criteria
- Phase model stores budgeted_hours and budgeted_cost (DecimalField, default 0)
- WBSElement model stores budgeted_hours, budgeted_cost, and contract_value
- Phase linked to Project via FK with CASCADE delete
- WBSElement linked to Project and optionally to Phase via FK
- Phase supports billing_mode (FORFAIT or HORAIRE)
- Budget fields editable through PhaseViewSet and WBSElementViewSet

## Tasks / Subtasks
- [x] Define Phase model with budgeted_hours (max_digits=10) and budgeted_cost (max_digits=12)
- [x] Add BillingMode TextChoices enum (FORFAIT, HORAIRE)
- [x] Add billing_mode field to Phase with FORFAIT default
- [x] Add is_mandatory and is_locked flags on Phase
- [x] Define WBSElement model with budgeted_hours, budgeted_cost, contract_value fields
- [x] Add is_billable flag on WBSElement
- [x] Create PhaseSerializer exposing budget fields
- [x] Create PhaseViewSet as nested route under project
- [x] Write test for phase creation verifying default billing_mode
- [x] Write test for phase API CRUD

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Phase model with budget tracking (budgeted_hours, budgeted_cost), billing mode, ordering, mandatory/locked flags
- WBSElement model with budget fields and contract_value for billing baseline
- BillingMode enum with FORFAIT and HORAIRE options
- Full CRUD via PhaseViewSet nested under /api/v1/projects/{pk}/phases/
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (Phase, BillingMode)
- backend/apps/projects/serializers.py (PhaseSerializer)
- backend/apps/projects/views.py (PhaseViewSet)
- backend/apps/projects/urls.py (nested phases route)
- backend/apps/projects/migrations/0001_initial.py
- backend/apps/projects/tests/test_models.py (TestPhaseModel)
- backend/apps/projects/tests/test_views.py (TestPhaseAPI)
