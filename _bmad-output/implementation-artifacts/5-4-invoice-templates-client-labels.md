# Story 5.4: Invoice Templates and Client Labels

Status: done

## Story
As a billing coordinator, I want configurable invoice templates and client-specific labels for WBS items, so that each client receives invoices in their preferred format with their own terminology.

## Acceptance Criteria
- InvoiceTemplate model with name, description, template_config (JSONField), is_active
- ClientLabel model maps WBS codes to client-specific labels per project
- UniqueConstraint on (project, wbs_code) for client labels
- Invoice FK to InvoiceTemplate (optional)
- Full CRUD for templates and labels

## Tasks / Subtasks
- [x] Create InvoiceTemplate model with JSONField for layout config
- [x] Create ClientLabel model with project FK, wbs_code, client_label
- [x] Add UniqueConstraint on project+wbs_code
- [x] Add template FK to Invoice model
- [x] Create InvoiceTemplateSerializer
- [x] Create InvoiceTemplateViewSet (active templates only)
- [x] Register URL routes
- [x] Write tests for template and label CRUD

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- InvoiceTemplate stores layout config as JSON (sections, columns, footer, logo)
- ClientLabel maps internal WBS codes to client-facing labels per project
- InvoiceTemplateViewSet filters to is_active=True by default
- Invoice.template optional FK allows per-invoice template selection
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py
- backend/apps/billing/serializers.py
- backend/apps/billing/views.py
- backend/apps/billing/urls.py
- backend/apps/billing/tests/test_models.py
