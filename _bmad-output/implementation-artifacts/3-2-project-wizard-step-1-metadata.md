# Story 3.2: Project Wizard Step 1 — Metadata

Status: done

## Story
As a project manager, I want to enter project metadata (code, name, client, leadership, dates) and create a project from a template, So that the project is initialized with the correct structure and team leads.

## Acceptance Criteria
- Project model stores code (unique per tenant), name, client FK, contract_type, start_date, end_date
- Leadership FKs: pm, associate_in_charge, invoice_approver, bu_director (all nullable)
- business_unit and legal_entity text fields available
- create_from_template service accepts template_id + project_data dict, creates project with pre-populated phases and support services
- API endpoint POST /api/v1/projects/create_from_template/ triggers the service
- Returns 400 if template_id missing, 404 if template not found

## Tasks / Subtasks
- [x] Define Project model extending TenantScopedModel + VersionedModel
- [x] Add code field with UniqueConstraint on (code, tenant)
- [x] Add client FK to clients.Client with PROTECT
- [x] Add four leadership FK fields to AUTH_USER_MODEL
- [x] Add business_unit, legal_entity, start_date, end_date, construction_cost fields
- [x] Create ProjectSerializer with OptimisticLockMixin and nested phases/support_services
- [x] Create ProjectListSerializer with client_name for list view
- [x] Implement create_project_from_template in services.py
- [x] Add create_from_template action on ProjectViewSet
- [x] Write test for create_from_template verifying phases and support services count
- [x] Write test for project creation via API

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Project model with all metadata fields, unique code per tenant, client FK with PROTECT
- Four leadership FKs (pm, associate_in_charge, invoice_approver, bu_director)
- create_project_from_template service creates project + phases + support services from template config
- Wizard Step 1 endpoint at /api/v1/projects/create_from_template/ with error handling
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (Project model)
- backend/apps/projects/serializers.py (ProjectSerializer, ProjectListSerializer)
- backend/apps/projects/views.py (ProjectViewSet, create_from_template action)
- backend/apps/projects/services.py (create_project_from_template)
- backend/apps/projects/urls.py (projects route)
- backend/apps/projects/migrations/0001_initial.py
- backend/apps/projects/tests/test_views.py (TestCreateFromTemplate)
- backend/apps/projects/tests/test_models.py (TestProjectModel)
