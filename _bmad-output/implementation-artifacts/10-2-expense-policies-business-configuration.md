# Story 10.2: Expense Policies & Business Configuration

Status: done

## Story

As a **finance administrator**,
I want to configure expense categories with refacturability defaults and receipt requirements,
So that expense submissions follow company policies automatically.

## Acceptance Criteria

- ExpenseCategory model has `is_refacturable_default` boolean field
- ExpenseCategory model has `requires_receipt` boolean field
- Categories are tenant-scoped and configurable per organization
- GL account mapping available per category
- ExpenseLine inherits `is_refacturable` default from category

## Tasks / Subtasks

- [x] Task 1: Implement ExpenseCategory configuration model
  - [x] 1.1 Created ExpenseCategory model with name, is_refacturable_default, requires_receipt, gl_account
  - [x] 1.2 Model extends TenantScopedModel for per-tenant isolation
  - [x] 1.3 ExpenseLine references ExpenseCategory via FK (PROTECT)
  - [x] 1.4 ExpenseLine has `is_refacturable` field that can be set per line (overriding category default)

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- ExpenseCategory: name (CharField), is_refacturable_default (BooleanField, default False), requires_receipt (BooleanField, default True), gl_account (CharField, optional)
- Tenant-scoped with db_table `expenses_category`, ordered by name
- ExpenseLine links to ExpenseCategory via FK with PROTECT delete behavior
- ExpenseLine.is_refacturable (BooleanField) allows per-line override of category default
- ExpenseLine also supports refacturable_markup_pct and tax_type configuration

### Change Log
- 2026-03-18: Implemented as part of Epic 10 batch

### File List
- backend/apps/expenses/models.py (ExpenseCategory, ExpenseLine)
- backend/apps/core/models.py (Tenant, TenantScopedModel)
