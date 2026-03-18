# Story 7.1: ST Invoice Entry and PM Authorization

Status: done

## Story
As a project manager, I want to enter and authorize subcontractor invoices with 3-layer budget allocation (internal, refacturable, absorbed), so that ST costs are properly tracked and authorized.

## Acceptance Criteria
- STInvoice model with supplier FK (ExternalOrganization), project FK
- 3 budget layers: budget_internal, budget_refacturable, budget_absorbed
- Status workflow: received -> authorized -> paid -> disputed -> credited
- Source field distinguishes manual vs API entry
- HistoricalRecords for audit trail

## Tasks / Subtasks
- [x] Create STInvoice model with all fields
- [x] Add 3 budget layer fields (internal, refacturable, absorbed)
- [x] Add status choices and source choices
- [x] Add HistoricalRecords
- [x] Create STInvoiceSerializer
- [x] Create STInvoiceViewSet
- [x] Register URL routes
- [x] Write tests for ST invoice CRUD and budget allocation

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- STInvoice references ExternalOrganization as supplier
- 3-layer budget: budget_internal (firm cost), budget_refacturable (client-billable), budget_absorbed (non-recoverable)
- 5-status workflow: received, authorized, paid, disputed, credited
- source field tracks manual entry vs API import
- HistoricalRecords tracks all changes for audit
### Change Log
- 2026-03-18: Implemented as part of Epic 7 batch
### File List
- backend/apps/suppliers/models.py
- backend/apps/suppliers/serializers.py
- backend/apps/suppliers/views.py
- backend/apps/suppliers/urls.py
- backend/apps/suppliers/admin.py
- backend/apps/suppliers/apps.py
- backend/apps/suppliers/tests/test_models.py
- backend/apps/suppliers/tests/test_views.py
- backend/apps/suppliers/migrations/0001_initial.py
- backend/apps/suppliers/migrations/0002_historicalstholdback_historicalstinvoice_stholdback_and_more.py
