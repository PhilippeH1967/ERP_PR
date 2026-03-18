# Story 4.6: Automated Timesheet Reminders

Status: done

## Story
As a finance administrator, I want automated reminders sent to employees with incomplete timesheets, so that submissions happen on time without manual follow-up.

## Acceptance Criteria
- Celery shared_task send_timesheet_reminders (stub implementation)
- Designed for Celery Beat scheduling (e.g., Thursday 5pm)
- PeriodUnlock model allows temporary unlocking of locked periods for corrections
- PeriodUnlock tracks reason (CORRECTION, AMENDMENT, AUDIT), justification, unlocked_by

## Tasks / Subtasks
- [x] Create send_timesheet_reminders Celery shared_task (stub)
- [x] Add structlog logging for reminder count
- [x] Create PeriodUnlock model with UnlockReason choices
- [x] Add period_start, period_end, reason, justification, unlocked_by fields
- [x] Create PeriodUnlockSerializer
- [x] Create PeriodUnlockViewSet with tenant-aware perform_create
- [x] Register URL routes
- [x] Write tests for period unlock CRUD

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- send_timesheet_reminders Celery task created as stub with structlog output
- PeriodUnlock model with 3 unlock reasons (CORRECTION, AMENDMENT, AUDIT)
- unlocked_by auto-set from request.user
- Full ViewSet CRUD for managing period unlocks
- Task returns dict with reminders_sent count (0 in stub)
### Change Log
- 2026-03-18: Implemented as part of Epic 4 batch
### File List
- backend/apps/time_entries/tasks.py
- backend/apps/time_entries/models.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/urls.py
- backend/apps/time_entries/tests/test_models.py
