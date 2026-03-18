# Story 6.1: Expense Report Creation and Receipt Upload

Status: done

## Story
As an employee, I want to create expense reports with line items and attach receipts, so that my business expenses are submitted for reimbursement.

## Acceptance Criteria
- ExpenseReport model with employee FK, project FK (optional), status, total_amount, submitted_at
- ExpenseLine model with category FK, expense_date, amount, description, receipt_path
- receipt_path field stores file path for uploaded receipts
- is_refacturable flag and refacturable_markup_pct for client-billable expenses
- tax_type field (HT, TPS, TVQ)
- HistoricalRecords on ExpenseReport

## Tasks / Subtasks
- [x] Create ExpenseReport model with status workflow
- [x] Create ExpenseLine model with all financial fields
- [x] Add receipt_path field for receipt file storage
- [x] Add is_refacturable and refacturable_markup_pct fields
- [x] Add tax_type choices
- [x] Create serializers for report and lines
- [x] Create ExpenseReportViewSet
- [x] Register URL routes
- [x] Write tests for report and line creation

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- ExpenseReport with HistoricalRecords for audit trail
- ExpenseLine stores receipt_path (file path to uploaded receipt)
- Refacturable expenses tracked with boolean flag and markup percentage
- Tax type supports HT (hors taxes), TPS, TVQ
- ExpenseStatus enum: SUBMITTED, PM_APPROVED, FINANCE_VALIDATED, PAID, REVERSED, REJECTED
### Change Log
- 2026-03-18: Implemented as part of Epic 6 batch
### File List
- backend/apps/expenses/models.py
- backend/apps/expenses/serializers.py
- backend/apps/expenses/views.py
- backend/apps/expenses/urls.py
- backend/apps/expenses/admin.py
- backend/apps/expenses/apps.py
- backend/apps/expenses/tests/test_models.py
- backend/apps/expenses/migrations/0001_initial.py
