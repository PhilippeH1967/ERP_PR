# Story 3.6: Virtual-to-Real Resource Assignment

Status: done

## Story

As a **PM**,
I want to assign real employees to project phases via a selection modal,
So that my team is assigned and can start entering time.

## Acceptance Criteria

1. **Given** a project with phases **When** I click "Affecter" on a phase **Then** a modal opens for employee selection
2. **And** I can assign with a percentage (0-100%) and date range
3. **And** Assignment calls POST /api/v1/projects/{id}/assignments/
4. **And** Assigned employees appear in the Team tab of ProjectDetail

## Tasks / Subtasks

### Backend (DONE)
- [x] EmployeeAssignment model (employee, project, phase, percentage, start/end dates)
- [x] EmployeeAssignmentViewSet nested under /projects/{id}/assignments/

### Frontend
- [ ] F1: Create AssignmentModal.vue — employee search + percentage + dates
- [ ] F2: Add "Affecter" button on phase rows in ProjectDetail
- [ ] F3: Team tab shows assigned employees fetched from API
- [ ] F4: ESLint 0 errors

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Change Log
- 2026-03-18: Backend implemented as part of Epic 3 batch
- 2026-03-18: Frontend tasks added after audit
### File List
- backend/apps/projects/models.py (EmployeeAssignment)
- backend/apps/projects/serializers.py
- backend/apps/projects/views.py
