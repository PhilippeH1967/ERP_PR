# Story 2.4: External Organizations Registry

Status: done

## Story

As a **Finance user**,
I want a shared registry of external organizations with create/edit forms,
So that the same firm doesn't get entered multiple times across modules.

## Acceptance Criteria

1. **Given** I need to add a subcontractor **When** I click "Nouvelle organisation" **Then** a creation form opens
2. **And** Form fields: name*, NEQ, address, city, province, postal_code, contact info, type_tags
3. **And** Deduplication check on name + NEQ before creation

## Tasks / Subtasks

### Backend (DONE)
- [x] ExternalOrganization model with type_tags JSON, NEQ, contact fields
- [x] CRUD API at /api/v1/external_organizations/ with search

### Frontend
- [ ] F1: Create OrgCreateModal.vue (SlideOver form)
- [ ] F2: Integrate in SupplierList.vue

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### File List
