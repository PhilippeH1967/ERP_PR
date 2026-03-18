# Story 5.8: Non-Billable Tracking and Intact Export

Status: done

## Story
As a finance administrator, I want dunning levels and actions tracked for overdue invoices, so that collection follow-up is systematic and exportable to Intact.

## Acceptance Criteria
- DunningLevel model with configurable escalation (level, days_overdue, email_template)
- DunningAction model records each dunning communication sent
- Ordered by level for escalation sequence
- DunningAction tracks sent_at timestamp per invoice

## Tasks / Subtasks
- [x] Create DunningLevel model with level, days_overdue, email_template
- [x] Create DunningAction model with invoice FK, dunning_level FK, sent_at
- [x] Add ordering by level and sent_at respectively
- [x] Create serializers for both models
- [x] Register URL routes
- [x] Write tests for dunning level configuration and action logging

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- DunningLevel defines escalation thresholds (e.g., Level 1 at 30 days, Level 2 at 60 days)
- DunningAction logs each communication sent with auto timestamp
- Both models tenant-scoped for multi-tenant isolation
- Ordered by level for predictable escalation sequence
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py
- backend/apps/billing/serializers.py
- backend/apps/billing/urls.py
- backend/apps/billing/tests/test_models.py
