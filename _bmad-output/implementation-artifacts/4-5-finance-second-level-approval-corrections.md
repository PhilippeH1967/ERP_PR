# Story 4.5: Finance Second-Level Approval and Corrections

Status: done

## Story
As a finance analyst, I want to perform second-level approval of timesheets and access historical corrections, so that hours are validated for billing accuracy.

## Acceptance Criteria
- WeeklyApproval extended with finance_status, finance_approved_by, finance_approved_at
- approve_finance action endpoint performs second-level approval
- Anti-self-approval enforced at finance level too
- HistoricalRecords on TimeEntry provides full audit trail of corrections
- Finance can review change history before approving

## Tasks / Subtasks
- [x] Add finance_status, finance_approved_by, finance_approved_at to WeeklyApproval
- [x] Implement approve_finance action on WeeklyApprovalViewSet
- [x] Add anti-self-approval check to approve_finance
- [x] Confirm HistoricalRecords on TimeEntry tracks all edits
- [x] Write tests for finance approval and correction tracking

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Finance approval fields added to WeeklyApproval model alongside PM fields
- approve_finance action mirrors approve_pm with same anti-self-approval guard
- TimeEntry.history (HistoricalRecords) tracks all field changes for audit
- Both approval actions return serialized WeeklyApproval response
### Change Log
- 2026-03-18: Implemented as part of Epic 4 batch
### File List
- backend/apps/time_entries/models.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/tests/test_views.py
