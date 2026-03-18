# Story 7.2: Payment Execution and Validation

Status: done

## Story
As a finance analyst, I want to record partial payments to subcontractors, manage credit notes and disputes, so that ST payment obligations are accurately tracked.

## Acceptance Criteria
- STPayment model supports partial payments linked to STInvoice
- STCreditNote model for supplier credit notes
- STDispute model tracks open/resolved/escalated disputes with expected resolution date
- All models have HistoricalRecords for audit

## Tasks / Subtasks
- [x] Create STPayment model with amount, payment_date, status
- [x] Create STCreditNote model with supplier FK, amount, status
- [x] Create STDispute model with description, status choices, expected_resolution
- [x] Add HistoricalRecords to all three models
- [x] Create serializers for STPayment, STCreditNote, STDispute
- [x] Create ViewSets for all three models
- [x] Register URL routes
- [x] Write tests for payment recording and dispute tracking

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- STPayment supports partial payments with pending status tracking
- STCreditNote can be linked to specific STInvoice or standalone per supplier
- STDispute tracks disputes with 3 statuses: open, resolved, escalated
- expected_resolution date field for dispute timeline management
- All 3 models have HistoricalRecords for full audit trail
### Change Log
- 2026-03-18: Implemented as part of Epic 7 batch
### File List
- backend/apps/suppliers/models.py
- backend/apps/suppliers/serializers.py
- backend/apps/suppliers/views.py
- backend/apps/suppliers/urls.py
- backend/apps/suppliers/tests/test_models.py
- backend/apps/suppliers/tests/test_views.py
