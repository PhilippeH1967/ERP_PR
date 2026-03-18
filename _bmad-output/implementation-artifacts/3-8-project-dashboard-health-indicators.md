# Story 3.8: Project Dashboard & Health Indicators

Status: done

## Story
As a project director, I want to see a project health dashboard with hours consumed vs budget and color-coded indicators, So that I can quickly identify projects that need attention.

## Acceptance Criteria
- Dashboard endpoint at GET /api/v1/projects/{pk}/dashboard/
- Returns hours_consumed (sum of TimeEntry hours), budget_hours (sum of Phase budgeted_hours)
- Calculates budget_utilization_percent as (hours_consumed / budget_hours * 100)
- Health indicator: green (< 75%), yellow (75-89%), red (>= 90%)
- Returns project_id, code, name, status alongside KPIs
- Handles zero-budget projects gracefully (0% utilization, green health)

## Tasks / Subtasks
- [x] Add dashboard action on ProjectViewSet (detail=True, methods=["get"])
- [x] Query TimeEntry hours consumed for the project using Sum aggregate
- [x] Query Phase budgeted_hours total using Sum aggregate
- [x] Calculate utilization percentage with zero-division guard
- [x] Implement green/yellow/red health thresholds
- [x] Return structured JSON response with all KPI fields
- [x] Write test for dashboard endpoint verifying green health on empty project

## Dev Agent Record
### Agent Model Used
Claude Opus 4.6 (1M context)
### Completion Notes List
- Dashboard action on ProjectViewSet queries TimeEntry and Phase aggregates
- Utilization percentage calculated with safe zero-budget handling
- Three-tier health system: green (< 75%), yellow (75-90%), red (>= 90%)
- Returns comprehensive payload with project metadata and financial KPIs
### Change Log
- 2026-03-18: Implemented as part of Epic 3 batch
### File List
- backend/apps/projects/views.py (ProjectViewSet.dashboard action)
- backend/apps/projects/tests/test_views.py (test_project_dashboard)
