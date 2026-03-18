# Story 3.9: Internal Projects & Personnel Lending

Status: done

## Story
As an operations manager, I want to flag projects as internal and filter them separately, So that internal overhead projects (admin, training, R&D) are distinguished from billable client work.

## Acceptance Criteria
- Project.is_internal BooleanField defaults to False
- Internal projects filterable via /api/v1/projects/?is_internal=true
- is_internal included in ProjectListSerializer for list views
- create_from_template service accepts is_internal in project_data whitelist
- Internal projects can use the same template/phase/WBS structure as client projects

## Tasks / Subtasks
- [x] Add is_internal BooleanField on Project model (default=False)
- [x] Include is_internal in filterset_fields on ProjectViewSet
- [x] Include is_internal in ProjectListSerializer fields
- [x] Include is_internal in ProjectSerializer fields
- [x] Whitelist is_internal in create_project_from_template service

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- is_internal flag on Project model for distinguishing internal vs client projects
- Filterable via DjangoFilterBackend on the project list endpoint
- Included in both list and detail serializers
- Template-based creation supports is_internal flag
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (Project.is_internal)
- backend/apps/projects/serializers.py (ProjectSerializer, ProjectListSerializer)
- backend/apps/projects/views.py (ProjectViewSet filterset_fields)
- backend/apps/projects/services.py (is_internal in whitelist)
- backend/apps/projects/migrations/0001_initial.py
