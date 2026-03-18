# Story 6.3: 4-Role Expense Approval Workflow

Status: done

## Story
As a finance manager, I want a 4-role approval chain for expense reports (submitter, manager, finance analyst, finance), so that expenses are properly authorized at each level before payment.

## Acceptance Criteria
- ExpenseApproval model with role_level choices: submitter, manager, finance_analyst, finance
- Each approval records approved_by, status (approved/rejected), rejection_reason, date
- ExpenseReport status follows: SUBMITTED -> PM_APPROVED -> FINANCE_VALIDATED -> PAID
- REVERSED and REJECTED statuses for cancellations

## Tasks / Subtasks
- [x] Create ExpenseApproval model with 4 role levels
- [x] Add approved_by FK, status choices, rejection_reason
- [x] Add auto timestamp on approval date
- [x] Create ExpenseApprovalSerializer
- [x] Register URL routes
- [x] Write tests for multi-level approval chain

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- ExpenseApproval records each approval step in the 4-role chain
- role_level choices: submitter, manager (gestionnaire), finance_analyst (analyste finance), finance
- Each approval is an independent record linked to the report
- rejection_reason captures rationale when status is "rejected"
- Ordered by date descending for latest-first display
### Change Log
- 2026-03-18: Implemented as part of Epic 6 batch
### File List
- backend/apps/expenses/models.py
- backend/apps/expenses/serializers.py
- backend/apps/expenses/urls.py
- backend/apps/expenses/tests/test_models.py
