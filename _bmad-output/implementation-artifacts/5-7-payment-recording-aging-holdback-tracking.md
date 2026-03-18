# Story 5.7: Payment Recording, Aging, and Holdback Tracking

Status: done

## Story
As a finance analyst, I want to record payments, track aging of outstanding invoices, and manage contractual holdbacks, so that cash flow and receivables are accurately monitored.

## Acceptance Criteria
- Payment model with invoice FK, amount, payment_date, reference, method
- PaymentAllocation model for splitting payments across invoices
- Holdback model tracks accumulated, released, remaining amounts with percentage_rate
- WriteOff model for invoice write-offs (radiation)
- get_aging_analysis service function returns 0-30, 31-60, 61-90, 90+ day buckets
- get_client_financial_summary aggregates total invoiced, paid, outstanding

## Tasks / Subtasks
- [x] Create Payment model with HistoricalRecords
- [x] Create PaymentAllocation model
- [x] Create Holdback model with percentage_rate, accumulated, released, remaining
- [x] Create WriteOff model with HistoricalRecords
- [x] Implement get_aging_analysis service
- [x] Implement get_client_financial_summary service
- [x] Add aging_analysis action to InvoiceViewSet
- [x] Create ViewSets for Payment, Holdback, WriteOff
- [x] Write tests for aging calculation and payment allocation

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Payment, PaymentAllocation, Holdback, WriteOff models all implemented
- get_aging_analysis computes 4 aging buckets from sent invoices minus payments
- get_client_financial_summary aggregates total CA, paid, outstanding, project count
- aging_analysis exposed as action on InvoiceViewSet
- All financial models have HistoricalRecords for audit
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py
- backend/apps/billing/services.py
- backend/apps/billing/serializers.py
- backend/apps/billing/views.py
- backend/apps/billing/urls.py
- backend/apps/billing/tests/test_models.py
- backend/apps/billing/tests/test_services.py
- backend/apps/billing/tests/test_views.py
