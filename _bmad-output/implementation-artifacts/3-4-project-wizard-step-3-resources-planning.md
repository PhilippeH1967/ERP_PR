# Story 3.4: Project Wizard Step 3 — Resources & Planning

Status: done

## Story
As a project manager, I want to assign employees to project phases and define support services, So that resource planning is captured during project setup.

## Acceptance Criteria
- EmployeeAssignment model links employee (User FK) to project and optionally to phase
- Assignment tracks percentage (default 100%), start_date, end_date
- SupportService model stores name, client_facing_label, budgeted hours/cost, billing_mode
- SupportService linked to Project via FK with CASCADE
- EmployeeAssignmentViewSet provides CRUD nested under project
- SupportService data included in ProjectSerializer as nested read-only

## Tasks / Subtasks
- [x] Define EmployeeAssignment model with employee FK, project FK, phase FK (nullable)
- [x] Add percentage DecimalField (max_digits=5, decimal_places=2, default=100)
- [x] Add start_date and end_date on EmployeeAssignment
- [x] Define SupportService model with budget and billing fields
- [x] Add client_facing_label on SupportService
- [x] Create EmployeeAssignmentSerializer
- [x] Create EmployeeAssignmentViewSet nested under project
- [x] Create SupportServiceSerializer included in ProjectSerializer
- [x] Register assignment routes in urls.py
- [x] Support services auto-created from template via create_from_template service

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- EmployeeAssignment model with employee/project/phase FKs and percentage allocation
- SupportService model with budget tracking and client-facing labels
- EmployeeAssignmentViewSet at /api/v1/projects/{pk}/assignments/
- SupportServiceSerializer nested read-only in ProjectSerializer
- Template service creates support services from support_services_config
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/models.py (EmployeeAssignment, SupportService)
- backend/apps/projects/serializers.py (EmployeeAssignmentSerializer, SupportServiceSerializer)
- backend/apps/projects/views.py (EmployeeAssignmentViewSet)
- backend/apps/projects/urls.py (nested assignments route)
- backend/apps/projects/services.py (support service creation from template)
- backend/apps/projects/migrations/0001_initial.py
