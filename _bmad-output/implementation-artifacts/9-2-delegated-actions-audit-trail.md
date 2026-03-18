# Story 9.2: Delegated Actions & Audit Trail

Status: done

## Story

As a **compliance officer or administrator**,
I want all delegated actions to be tracked in an audit trail,
So that I can verify who performed actions and under what delegation authority.

## Acceptance Criteria

- django-simple-history HistoricalRecords tracks all changes on financial models
- Architecture pattern documents history_delegation_id for future delegation tracking
- HistoricalRecords enabled on ExpenseReport, Invoice, TimeEntry, and other financial models
- Full change history accessible per record

## Tasks / Subtasks

- [x] Task 1: Enable HistoricalRecords on all financial models
  - [x] 1.1 Added `history = HistoricalRecords()` to ExpenseReport model
  - [x] 1.2 Added HistoricalRecords to billing models (Invoice, InvoiceLine, Payment)
  - [x] 1.3 Added HistoricalRecords to time_entries models (TimeEntry, WeeklyApproval)
  - [x] 1.4 Added HistoricalRecords to projects, clients, suppliers models
  - [x] 1.5 Documented architecture pattern for history_delegation_id field (future)

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- django-simple-history `HistoricalRecords()` added to all financial and operational models
- Models with history tracking: ExpenseReport, Invoice, InvoiceLine, Payment, TimeEntry, WeeklyApproval, Project, Client, Supplier
- Architecture pattern reserves `history_delegation_id` for linking historical changes to delegation records
- History tables auto-created via migrations

### Change Log
- 2026-03-18: Implemented as part of Epic 9 batch

### File List
- backend/apps/expenses/models.py (ExpenseReport.history)
- backend/apps/billing/models.py (Invoice, InvoiceLine, Payment history)
- backend/apps/time_entries/models.py (TimeEntry, WeeklyApproval history)
- backend/apps/projects/models.py (Project history)
- backend/apps/clients/models.py (Client history)
- backend/apps/suppliers/models.py (Supplier history)
- backend/apps/core/models.py (VersionedModel with HistoricalRecords pattern)
