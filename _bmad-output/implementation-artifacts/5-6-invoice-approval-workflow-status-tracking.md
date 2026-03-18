# Story 5.6: Invoice Approval Workflow and Status Tracking

Status: done

## Story
As a finance manager, I want a formal approval workflow for invoices (Draft, Submitted, Approved, Sent, Paid), so that invoices follow proper authorization before being sent to clients.

## Acceptance Criteria
- InvoiceStatus enum: DRAFT, SUBMITTED, APPROVED, SENT, PAID
- submit action sets status to SUBMITTED and records submitted_by
- approve action sets status to APPROVED and records approved_by
- HistoricalRecords tracks all status changes
- CreditNote model supports partial/full adjustments with same status workflow

## Tasks / Subtasks
- [x] Create InvoiceStatus TextChoices enum
- [x] Add submitted_by and approved_by FKs to Invoice
- [x] Add date_sent and date_paid fields
- [x] Implement submit action on InvoiceViewSet
- [x] Implement approve action on InvoiceViewSet
- [x] Create CreditNote model with invoice FK, amount, reason, status
- [x] Create CreditNoteSerializer and CreditNoteViewSet
- [x] Write tests for workflow transitions

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- 5-step invoice workflow: DRAFT -> SUBMITTED -> APPROVED -> SENT -> PAID
- submit action records submitted_by from request.user
- approve action records approved_by from request.user
- CreditNote model for partial/full invoice adjustments (avoir)
- HistoricalRecords on both Invoice and CreditNote for audit trail
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py
- backend/apps/billing/views.py
- backend/apps/billing/serializers.py
- backend/apps/billing/urls.py
- backend/apps/billing/tests/test_views.py
