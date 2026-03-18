# Story 3.10: Project Lifecycle & Leadership Management

Status: done

## Story
As an administrator, I want project status transitions and leadership changes to be tracked with full audit history, So that we have a complete record of who managed the project and when status changes occurred.

## Acceptance Criteria
- Project.status field uses ProjectStatus enum (ACTIVE, ON_HOLD, COMPLETED, CANCELLED)
- Leadership FKs (pm, associate_in_charge, invoice_approver, bu_director) all SET_NULL on delete
- HistoricalRecords (django-simple-history) tracks all changes to Project model
- Amendment model also uses HistoricalRecords for audit trail
- Project uses VersionedModel for optimistic locking via version field
- Project history accessible and verified in tests (history.count() tracks updates)
- Ordering by -created_at on Project for most-recent-first listing

## Tasks / Subtasks
- [x] Add history = HistoricalRecords() on Project model
- [x] Add history = HistoricalRecords() on Amendment model
- [x] Extend VersionedModel on Project for optimistic lock version field
- [x] Define four leadership FK fields with SET_NULL and distinct related_names
- [x] Add ProjectStatus TextChoices enum with four states
- [x] Set default ordering to ["-created_at"] on Project Meta
- [x] Use OptimisticLockMixin on ProjectSerializer for concurrency control
- [x] Write test verifying history tracking on Project name change (history.count() == 2)
- [x] Write test verifying project code uniqueness per tenant

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- HistoricalRecords on both Project and Amendment for full audit trail
- VersionedModel + OptimisticLockMixin for optimistic concurrency control
- Four leadership FKs with SET_NULL to preserve project data when users are removed
- ProjectStatus enum enforces valid state transitions at the field level
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (Project with HistoricalRecords, VersionedModel, leadership FKs, ProjectStatus)
- backend/apps/projects/models.py (Amendment with HistoricalRecords)
- backend/apps/projects/serializers.py (ProjectSerializer with OptimisticLockMixin)
- backend/apps/projects/migrations/0001_initial.py
- backend/apps/projects/tests/test_models.py (test_project_history_tracked, test_project_code_unique_per_tenant)
