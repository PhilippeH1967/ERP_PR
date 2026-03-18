# Story 8.1: Role-Based Dashboards

Status: done

## Story

As a **logged-in user**,
I want a role-adaptive dashboard that shows KPIs relevant to my role,
So that I can see the most important metrics at a glance without navigating through multiple screens.

## Acceptance Criteria

- GET `/api/v1/dashboard/` returns role-based KPIs for the authenticated user
- Response includes `projects_active`, `timesheets_pending`, `invoices_outstanding`, `expenses_pending`
- Endpoint is tenant-scoped and requires authentication
- Returns empty KPIs gracefully when no tenant is set
- Frontend DashboardView renders 4 KPI cards with bilingual labels

## Tasks / Subtasks

- [x] Task 1: Create `dashboards` Django app with views, services, urls
  - [x] 1.1 Created `backend/apps/dashboards/` app scaffold (apps.py, __init__.py)
  - [x] 1.2 Implemented `role_dashboard` view — GET endpoint with IsAuthenticated permission
  - [x] 1.3 Implemented `get_role_dashboard_kpis` service — aggregates Project, WeeklyApproval, Invoice, ExpenseReport counts
  - [x] 1.4 Registered URL route `dashboard/` in dashboards/urls.py
- [x] Task 2: Frontend DashboardView.vue
  - [x] 2.1 Created DashboardView.vue with 4 KPI cards (grid layout)
  - [x] 2.2 Integrated useLocale composable for currency formatting
  - [x] 2.3 API call to `dashboard/` on mount with graceful fallback

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Completion Notes List
- Created `role_dashboard` FBV endpoint returning 4 KPIs scoped to tenant
- `get_role_dashboard_kpis` service queries Project (ACTIVE), WeeklyApproval (PENDING), Invoice (SENT sum), ExpenseReport (SUBMITTED)
- DashboardView.vue renders 4 cards with French labels (Projets actifs, Feuilles en attente, Factures impayees, Depenses en attente)
- Currency formatting via `useLocale().fmt.currency()`

### Change Log
- 2026-03-18: Implemented as part of Epic 8 batch

### File List
- backend/apps/dashboards/__init__.py
- backend/apps/dashboards/apps.py
- backend/apps/dashboards/views.py
- backend/apps/dashboards/services.py
- backend/apps/dashboards/urls.py
- backend/apps/dashboards/tests/__init__.py
- frontend/src/features/dashboard/views/DashboardView.vue
