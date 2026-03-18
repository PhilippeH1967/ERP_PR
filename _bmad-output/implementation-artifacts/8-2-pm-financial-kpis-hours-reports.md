# Story 8.2: PM Financial KPIs & Hours Reports

Status: done

## Story

As a **project manager**,
I want to see financial KPIs and hours summaries for my managed projects,
So that I can monitor budget consumption and resource utilization across my portfolio.

## Acceptance Criteria

- GET `/api/v1/dashboard/pm-kpis/` returns PM-specific financial KPIs
- Response includes `projects_managed`, `total_invoiced`, `total_hours`
- Only projects where the authenticated user is PM are included
- Endpoint is tenant-scoped and requires authentication

## Tasks / Subtasks

- [x] Task 1: Implement pm_financial_kpis endpoint
  - [x] 1.1 Created `pm_financial_kpis` FBV in dashboards/views.py
  - [x] 1.2 Implemented `get_pm_financial_kpis` service — filters Project by pm=user, aggregates Invoice totals and TimeEntry hours
  - [x] 1.3 Registered URL route `dashboard/pm-kpis/` in dashboards/urls.py

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- `get_pm_financial_kpis` filters active projects where `pm=user`, collects project IDs
- Aggregates `Invoice.total_amount` sum across managed projects
- Aggregates `TimeEntry.hours` sum across managed projects
- Returns `projects_managed` (count), `total_invoiced` (Decimal as string), `total_hours` (Decimal as string)

### Change Log
- 2026-03-18: Implemented as part of Epic 8 batch

### File List
- backend/apps/dashboards/views.py
- backend/apps/dashboards/services.py
- backend/apps/dashboards/urls.py
