# Story 3.6: Virtual-to-Real Resource Assignment

Status: done

## Story
As a project manager, I want to assign real employees to project phases with percentage allocation, So that resource planning reflects actual team commitments and availability.

## Acceptance Criteria
- EmployeeAssignment links employee (User FK) to project and phase (nullable FK)
- percentage field (DecimalField, max_digits=5, decimal_places=2) defaults to 100%
- Assignment supports date range (start_date, end_date) for time-bounded allocation
- Assignments are tenant-scoped
- CRUD available at /api/v1/projects/{pk}/assignments/

## Tasks / Subtasks
- [x] Define EmployeeAssignment with employee FK (CASCADE), project FK (CASCADE), phase FK (CASCADE, nullable)
- [x] Add percentage field with 100% default
- [x] Add start_date and end_date fields
- [x] Extend TenantScopedModel for multi-tenant support
- [x] Create EmployeeAssignmentSerializer with all fields
- [x] Create EmployeeAssignmentViewSet filtering by project_pk
- [x] Wire perform_create to set project and tenant from URL

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- EmployeeAssignment model with percentage-based allocation per phase
- Phase FK nullable to support project-level assignments without specific phase
- ViewSet auto-sets project and tenant from URL kwargs in perform_create
- Supports time-bounded assignments via start_date/end_date
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (EmployeeAssignment)
- backend/apps/projects/serializers.py (EmployeeAssignmentSerializer)
- backend/apps/projects/views.py (EmployeeAssignmentViewSet)
- backend/apps/projects/urls.py (nested assignments route)
- backend/apps/projects/migrations/0001_initial.py
