# Story 5.1: Financial Phases and Dual Rate Configuration

Status: done

## Story
As a project controller, I want financial phases with dual billing rates (forfait and hourly), so that each phase of a project can be invoiced according to its contractual structure.

## Acceptance Criteria
- FinancialPhase model exists in projects app with billing configuration
- Referenced by InvoiceLine via foreign key
- Supports both forfait (fixed-fee) and hourly billing modes
- Linked to project phases for WBS alignment

## Tasks / Subtasks
- [x] Verify FinancialPhase model in projects app
- [x] Ensure FK reference from InvoiceLine to FinancialPhase
- [x] Confirm LineType choices include FORFAIT, HORAIRE, ST, DEPENSE
- [x] Write tests for financial phase linkage

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- FinancialPhase model resides in backend/apps/projects/ (pre-existing)
- InvoiceLine.financial_phase FK links billing lines to financial phases
- LineType enum supports FORFAIT, HORAIRE, ST, DEPENSE billing modes
- Dual rate configuration available through financial phase fields
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py (InvoiceLine FK reference)
- backend/apps/projects/models.py (FinancialPhase model)
- backend/apps/billing/tests/test_models.py
