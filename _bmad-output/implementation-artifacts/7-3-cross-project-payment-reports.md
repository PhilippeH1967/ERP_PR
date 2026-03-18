# Story 7.3: Cross-Project Payment Reports

Status: done

## Story
As a finance manager, I want holdback tracking for subcontractors and an extended supplier registry, so that retention amounts are monitored across projects and supplier data is comprehensive.

## Acceptance Criteria
- STHoldback model tracks accumulated, released, remaining holdback per supplier per project
- percentage_rate for contractual retention percentage
- ExternalOrganization extended with banking_info (JSONField), type_tags, NEQ, full address
- All models tenant-scoped with HistoricalRecords

## Tasks / Subtasks
- [x] Create STHoldback model with project FK, supplier FK
- [x] Add percentage_rate, accumulated, released, remaining fields
- [x] Add HistoricalRecords to STHoldback
- [x] Extend ExternalOrganization with banking_info JSONField
- [x] Add type_tags JSONField for role classification (st, partner, competitor)
- [x] Add NEQ, address, city, province, postal_code, country fields
- [x] Add contact fields (name, email, phone)
- [x] Create serializers for STHoldback and ExternalOrganization
- [x] Register URL routes
- [x] Write tests for holdback tracking and organization registry

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- STHoldback mirrors billing Holdback pattern but for supplier-side retention
- Tracks accumulated vs released vs remaining per supplier per project
- ExternalOrganization is a comprehensive supplier registry with NEQ, full address, banking_info, type_tags
- type_tags allow same organization to have different roles across projects
- banking_info stored as JSON for flexible banking detail storage
- is_active flag for soft-delete capability
### Change Log
- 2026-03-18: Implemented as part of Epic 7 batch
### File List
- backend/apps/suppliers/models.py
- backend/apps/suppliers/serializers.py
- backend/apps/suppliers/views.py
- backend/apps/suppliers/urls.py
- backend/apps/suppliers/tests/test_models.py
- backend/apps/suppliers/tests/test_views.py
- backend/apps/suppliers/migrations/0002_historicalstholdback_historicalstinvoice_stholdback_and_more.py
