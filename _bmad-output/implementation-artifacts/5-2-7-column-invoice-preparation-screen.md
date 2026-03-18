# Story 5.2: 7-Column Invoice Preparation Screen

Status: done

## Story
As a billing coordinator, I want an invoice preparation screen with 7 columns (deliverable, contract amount, invoiced to date, billing %, hours %, amount to bill, % after), so that I can accurately prepare invoices aligned with project progress.

## Acceptance Criteria
- Invoice model with full lifecycle fields (number, status, amounts, taxes, dates)
- InvoiceLine model with 7-column structure matching FR29 billing screen
- amount_to_bill is editable (the key billing input)
- Nested line items via InvoiceViewSet with prefetch_related
- InvoiceListSerializer for list view, InvoiceSerializer for detail

## Tasks / Subtasks
- [x] Create Invoice model (project, client, invoice_number, status, total_amount, tax_tps, tax_tvq, dates)
- [x] Create InvoiceLine model with 7-column fields
- [x] Add HistoricalRecords to Invoice
- [x] Create InvoiceSerializer and InvoiceListSerializer
- [x] Create InvoiceLineSerializer
- [x] Create InvoiceViewSet with search, filter, ordering
- [x] Create nested InvoiceLineViewSet
- [x] Register URL routes
- [x] Write tests for invoice and line CRUD

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Invoice model with provisional numbering (PROV-xxxx), TPS/TVQ tax fields
- InvoiceLine 7-column structure: total_contract_amount, invoiced_to_date, pct_billing_advancement, pct_hours_advancement, amount_to_bill (editable), pct_after_billing, order
- InvoiceViewSet with SearchFilter on invoice_number and project code
- Nested InvoiceLineViewSet filtered by invoice_pk from URL
- List vs detail serializer split for performance
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py
- backend/apps/billing/serializers.py
- backend/apps/billing/views.py
- backend/apps/billing/urls.py
- backend/apps/billing/tests/test_models.py
- backend/apps/billing/tests/test_views.py
- backend/apps/billing/migrations/0001_initial.py
