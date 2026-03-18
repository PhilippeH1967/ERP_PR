# Story 4.3: Phase and Person Blocking

Status: done

## Story
As a project manager, I want to lock time entry at the phase level or for specific people, so that completed phases or departed team members cannot have new hours recorded.

## Acceptance Criteria
- TimesheetLock model with lock_type enum (PHASE, PERSON)
- Supports phase-level locks (all employees blocked for a phase) and person-level locks (specific employee blocked)
- Tracks who locked and when (locked_by, locked_at)
- Full CRUD API for managing locks
- Tenant-scoped

## Tasks / Subtasks
- [x] Create TimesheetLock model with LockType choices (PHASE, PERSON)
- [x] Add project FK, phase FK (nullable), person FK (nullable)
- [x] Add locked_by FK and locked_at auto timestamp
- [x] Create TimesheetLockSerializer
- [x] Create TimesheetLockViewSet with perform_create setting locked_by
- [x] Register URL routes
- [x] Write tests for lock creation and retrieval

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- TimesheetLock model with PHASE and PERSON lock types
- Phase locks block all employees; person locks block a specific employee
- locked_by auto-set from request.user in perform_create
- Tenant-aware ViewSet with full CRUD
### Change Log
- 2026-03-18: Implemented as part of Epic 4 batch
### File List
- backend/apps/time_entries/models.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/urls.py
- backend/apps/time_entries/tests/test_models.py
