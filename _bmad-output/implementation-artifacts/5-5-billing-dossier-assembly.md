# Story 5.5: Billing Dossier Assembly

Status: done

## Story
As a billing coordinator, I want to assemble a billing dossier with invoice and annexes, so that complete billing packages can be generated and sent to clients.

## Acceptance Criteria
- BillingDossier model with invoice FK, annexes_config (JSONField), status, file_url
- Status choices: generating, ready
- generated_at timestamp for tracking
- Full CRUD API

## Tasks / Subtasks
- [x] Create BillingDossier model with invoice FK
- [x] Add annexes_config JSONField (default=list) for annex configuration
- [x] Add status field with generating/ready choices
- [x] Add file_url for generated document location
- [x] Add generated_at timestamp
- [x] Create BillingDossierSerializer
- [x] Register URL routes
- [x] Write tests for dossier creation and status transitions

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- BillingDossier tracks assembled billing packages per invoice
- annexes_config stores list of annex configurations as JSON
- Status transitions from "generating" to "ready" upon completion
- file_url stores path/URL to generated PDF package
### Change Log
- 2026-03-18: Implemented as part of Epic 5 batch
### File List
- backend/apps/billing/models.py
- backend/apps/billing/serializers.py
- backend/apps/billing/urls.py
- backend/apps/billing/tests/test_models.py
