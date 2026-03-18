# Story 4.1: Weekly Timesheet Entry Grid

Status: done

## Story
As an employee, I want to enter my time on a weekly grid by project and phase, so that my hours are accurately recorded for billing and project tracking.

## Acceptance Criteria
- TimeEntry model stores employee, project, phase, date, hours, status, notes
- CRUD REST API with full ModelViewSet
- Filter by employee, project, phase, date, and status via django-filters
- Unique constraint on (employee, project, phase, date) prevents duplicate entries
- Tenant-scoped with optimistic concurrency (VersionedModel)
- HistoricalRecords tracks all changes

## Tasks / Subtasks
- [x] Create TimeEntry model with all fields (employee FK, project FK, phase FK, date, hours, notes, status)
- [x] Add TimeEntryStatus choices (DRAFT, SUBMITTED, PM_APPROVED, FINANCE_APPROVED, LOCKED)
- [x] Add UniqueConstraint on employee+project+phase+date
- [x] Add HistoricalRecords for audit trail
- [x] Create TimeEntrySerializer
- [x] Create TimeEntryViewSet with CRUD, tenant filtering, and select_related
- [x] Register URL routes
- [x] Add filterset_fields for employee, project, phase, date, status
- [x] Write model and view tests

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Implemented TimeEntry model inheriting TenantScopedModel + VersionedModel
- TimeEntryStatus enum with 5 statuses (DRAFT through LOCKED)
- Full ModelViewSet with DjangoFilterBackend and OrderingFilter
- Tenant-aware queryset with select_related on project and phase
- perform_create auto-assigns employee from request.user
- 10 tests across test_models.py and test_views.py
### Change Log
- 2026-03-18: Implemented as part of Epic 4 batch
### File List
- backend/apps/time_entries/models.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/urls.py
- backend/apps/time_entries/admin.py
- backend/apps/time_entries/apps.py
- backend/apps/time_entries/tests/test_models.py
- backend/apps/time_entries/tests/test_views.py
- backend/apps/time_entries/migrations/0001_initial.py
