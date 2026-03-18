# Story 3.1: Project Model & Template System

Status: done

## Story
As a project director, I want to create projects from pre-configured templates by contract type, So that project setup follows our standard methodology and phases are pre-populated automatically.

## Acceptance Criteria
- ProjectTemplate model stores name, code, contract_type, phases_config (JSON), support_services_config (JSON), is_active flag
- ContractType enum defines FORFAITAIRE, CONSORTIUM, CO_DEV, CONCEPTION_CONSTRUCTION
- Template CRUD API available at /api/v1/project_templates/ with full ModelViewSet
- Templates are tenant-scoped and filtered by is_active=True
- phases_config stores an array of phase definitions (name, client_label, type, billing_mode, is_mandatory)
- support_services_config stores an array of support service definitions (name, client_label)

## Tasks / Subtasks
- [x] Define ContractType TextChoices enum with four contract types
- [x] Create ProjectTemplate model extending TenantScopedModel
- [x] Add phases_config and support_services_config JSONFields with list defaults
- [x] Create ProjectTemplateSerializer with all fields
- [x] Create ProjectTemplateViewSet with tenant-scoped queryset filtering
- [x] Register route in urls.py under project_templates
- [x] Write model test for template creation and phases_config validation
- [x] Write migration 0001_initial covering ProjectTemplate

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Implemented ProjectTemplate model with JSONField configs for phases and support services
- ContractType enum with four Quebec engineering contract types
- Full CRUD via ProjectTemplateViewSet filtered by is_active and tenant
- Registered at /api/v1/project_templates/
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (ProjectTemplate, ContractType)
- backend/apps/projects/serializers.py (ProjectTemplateSerializer)
- backend/apps/projects/views.py (ProjectTemplateViewSet)
- backend/apps/projects/urls.py (project_templates route)
- backend/apps/projects/migrations/0001_initial.py
- backend/apps/projects/tests/test_models.py (TestProjectTemplate)
