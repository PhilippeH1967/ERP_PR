# Story 3.5: Project Wizard Step 4 — Subcontractors & Confirmation

Status: done

## Story
As a project manager, I want to finalize the project setup with status confirmation and reference ST budget layers, So that the project transitions from draft to active with all financial structure in place.

## Acceptance Criteria
- ProjectStatus enum defines ACTIVE, ON_HOLD, COMPLETED, CANCELLED
- Project.status field defaults to ACTIVE
- FinancialPhase model groups realization phases for billing with fixed_amount or hourly_budget_max
- FinancialPhase supports FORFAIT and HORAIRE billing modes
- Amendment model tracks contract changes with budget_impact, status workflow (DRAFT/SUBMITTED/APPROVED/REJECTED)
- AmendmentViewSet provides CRUD nested under project with auto-numbered amendments

## Tasks / Subtasks
- [x] Define ProjectStatus TextChoices enum
- [x] Add status field on Project model with ACTIVE default
- [x] Define FinancialPhase model with billing_mode, fixed_amount, hourly_budget_max
- [x] Define Amendment model with status workflow and budget_impact
- [x] Add amendment_number auto-increment in AmendmentViewSet.perform_create
- [x] Add UniqueConstraint on (project, amendment_number)
- [x] Create FinancialPhaseSerializer
- [x] Create AmendmentSerializer with OptimisticLockMixin
- [x] Create AmendmentViewSet nested under project
- [x] Write test for amendment creation

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- ProjectStatus enum with four states, default ACTIVE on Project
- FinancialPhase model for billing layer grouping (fixed price or hourly cap)
- Amendment model with full status workflow, budget_impact tracking, HistoricalRecords audit
- AmendmentViewSet auto-numbers amendments per project and sets requested_by from request.user
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (ProjectStatus, FinancialPhase, Amendment)
- backend/apps/projects/serializers.py (FinancialPhaseSerializer, AmendmentSerializer)
- backend/apps/projects/views.py (AmendmentViewSet)
- backend/apps/projects/urls.py (nested amendments route)
- backend/apps/projects/migrations/0001_initial.py
- backend/apps/projects/tests/test_models.py (TestAmendment)
