# Story 4.2: Timesheet Draft, Submit, and Favorites

Status: done

## Story
As an employee, I want to save my timesheet as a draft and submit it when ready, and mark favorite project/phase combinations, so that I can work incrementally and quickly re-enter recurring assignments.

## Acceptance Criteria
- TimeEntry defaults to DRAFT status
- submit_week action endpoint transitions all DRAFT entries for a given week to SUBMITTED
- is_favorite boolean field on TimeEntry for quick re-selection
- Returns count of submitted entries

## Tasks / Subtasks
- [x] Add is_favorite BooleanField to TimeEntry model (default=False)
- [x] Implement submit_week custom action on TimeEntryViewSet
- [x] Validate week_start parameter is provided
- [x] Bulk update DRAFT entries to SUBMITTED for the employee's week
- [x] Return submitted_count in response
- [x] Write tests for submit_week action

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Added is_favorite field to TimeEntry for recurring project/phase combos
- submit_week action filters by employee + week_start + DRAFT status, bulk updates to SUBMITTED
- Returns JSON with submitted_count
- Error response with MISSING_WEEK code if week_start not provided
### Change Log
- 2026-03-18: Implemented as part of Epic 4 batch
### File List
- backend/apps/time_entries/models.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/tests/test_views.py
