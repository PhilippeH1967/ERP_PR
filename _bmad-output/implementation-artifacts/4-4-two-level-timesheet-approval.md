# Story 4.4: Two-Level Timesheet Approval

Status: done

## Story
As a project manager, I want to approve my team's submitted timesheets as first-level validation, so that hours are verified before finance review.

## Acceptance Criteria
- WeeklyApproval model tracks pm_status, pm_approved_by, pm_approved_at
- approve_pm action endpoint performs first-level approval
- Anti-self-approval: cannot approve own timesheet (uses cannot_approve_own utility)
- Unique constraint on (employee, week_start, tenant)
- ApprovalStatus enum (PENDING, APPROVED, REJECTED)

## Tasks / Subtasks
- [x] Create WeeklyApproval model with employee, week_start, week_end
- [x] Add pm_status, pm_approved_by, pm_approved_at fields
- [x] Add ApprovalStatus TextChoices enum
- [x] Add UniqueConstraint on employee+week_start+tenant
- [x] Create WeeklyApprovalSerializer
- [x] Create WeeklyApprovalViewSet with filterset_fields
- [x] Implement approve_pm action with anti-self-approval check
- [x] Return SELF_APPROVAL error (403) when employee tries to approve own sheet
- [x] Write tests for approval workflow and self-approval blocking

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- WeeklyApproval model with two-level approval fields (PM + Finance)
- approve_pm action uses cannot_approve_own from apps.core.permissions
- Returns 403 with SELF_APPROVAL error code on self-approval attempt
- Filterable by employee, week_start, pm_status, finance_status
### Change Log
- 2026-03-18: Implemented as part of Epic 4 batch
### File List
- backend/apps/time_entries/models.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/urls.py
- backend/apps/time_entries/tests/test_views.py
