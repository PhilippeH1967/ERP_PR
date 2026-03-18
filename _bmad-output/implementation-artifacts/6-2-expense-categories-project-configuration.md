# Story 6.2: Expense Categories and Project Configuration

Status: done

## Story
As a finance administrator, I want configurable expense categories with GL accounts and refacturable defaults, so that expense classification is standardized and accounting-ready.

## Acceptance Criteria
- ExpenseCategory model with name, gl_account, is_refacturable_default, requires_receipt
- Categories are tenant-scoped and ordered by name
- ExpenseLine references category via FK (PROTECT)
- GL account field for Intact integration

## Tasks / Subtasks
- [x] Create ExpenseCategory model with all fields
- [x] Add is_refacturable_default boolean for default refacturable setting
- [x] Add requires_receipt boolean for receipt policy
- [x] Add gl_account field for accounting integration
- [x] Create ExpenseCategorySerializer
- [x] Register URL routes
- [x] Write tests for category CRUD

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- ExpenseCategory defines classification with GL account mapping
- is_refacturable_default pre-populates refacturable flag on new expense lines
- requires_receipt enforces receipt upload policy per category
- PROTECT delete prevents removing categories with existing expense lines
### Change Log
- 2026-03-18: Implemented as part of Epic 6 batch
### File List
- backend/apps/expenses/models.py
- backend/apps/expenses/serializers.py
- backend/apps/expenses/urls.py
- backend/apps/expenses/tests/test_models.py
