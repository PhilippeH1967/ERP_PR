# API Reference

Base URL : `http://localhost:8000/api/v1/`

## Authentification

```
POST /auth/token/           → { access, refresh }
POST /auth/token/refresh/   → { access }
GET  /auth/me/              → { user, roles, tenant }
GET  /auth/config/          → { sso_available }
```

## Projets

```
GET/POST       /projects/
GET/PATCH/DEL  /projects/{id}/
POST           /projects/create_from_template/
GET            /projects/{id}/dashboard/
GET/POST       /projects/{id}/phases/
GET/POST       /projects/{id}/tasks/
GET/POST       /projects/{id}/wbs/
GET/POST       /projects/{id}/amendments/
GET/POST       /projects/{id}/assignments/
GET            /project_templates/
```

## Feuilles de temps

```
GET/POST       /time_entries/
PATCH          /time_entries/{id}/
POST           /time_entries/submit_week/
GET            /time_entries/weekly_stats/
POST           /time_entries/copy_previous_week/
POST           /time_entries/approve_entries/
POST           /time_entries/reject_entries/
POST           /time_entries/bulk_correct/
POST           /time_entries/transfer_hours/
GET            /time_entries/is_period_locked/
POST           /time_entries/lock_period/
POST           /time_entries/lock_before/
GET            /time_entries/period_summary/

GET/POST       /weekly_approvals/
POST           /weekly_approvals/{id}/approve_pm/
POST           /weekly_approvals/{id}/approve_finance/
POST           /weekly_approvals/{id}/validate_paie/
POST           /weekly_approvals/bulk_validate_paie/
GET            /weekly_approvals/pm_dashboard/
GET            /weekly_approvals/finance_dashboard/
GET            /weekly_approvals/paie_dashboard/
```

## Facturation

```
GET/POST       /invoices/
GET/PATCH      /invoices/{id}/
POST           /invoices/create_from_project/
POST           /invoices/{id}/submit/
POST           /invoices/{id}/approve/
POST           /invoices/{id}/mark_hours_invoiced/
GET            /invoices/{id}/aging_analysis/
GET/POST       /invoices/{id}/lines/
GET/POST       /credit_notes/
GET/POST       /payments/
GET/POST       /holdbacks/
GET/POST       /write_offs/
```

## Congés

```
GET/POST       /leave_types/
POST           /leave_types/seed/
GET            /leave_banks/my_balances/
GET/POST       /leave_requests/
POST           /leave_requests/{id}/approve/
POST           /leave_requests/{id}/reject/
POST           /leave_requests/{id}/cancel/
GET/POST       /public_holidays/
```

## Fournisseurs / ST

```
GET/POST       /external_organizations/
POST           /external_organizations/check_duplicate/
GET/POST       /st_invoices/
POST           /st_invoices/{id}/authorize/
POST           /st_invoices/{id}/mark_paid/
POST           /st_invoices/{id}/dispute/
POST           /st_invoices/batch_authorize/
GET            /st_invoices/summary_by_supplier/
GET/POST       /st_payments/
GET/POST       /st_credit_notes/
GET/POST       /st_disputes/
POST           /st_disputes/{id}/resolve/
GET/POST       /st_holdbacks/
POST           /st_holdbacks/{id}/release/
```

## Consortium

```
GET/POST       /consortiums/
GET/PATCH      /consortiums/{id}/
GET            /consortiums/{id}/validate_coefficients/
GET/POST       /consortiums/{id}/members/
```

## Planification

```
GET/POST       /allocations/
GET            /allocations/global_planning/
GET            /allocations/load_alerts/
GET/POST       /milestones/
POST           /milestones/auto_update_status/
GET/POST       /availability/
POST           /availability/generate/
GET/POST       /phase_dependencies/
GET            /gantt/project_gantt/?project_id={id}
```

## Dashboard & Rapports

```
GET            /dashboard/
GET            /dashboard/pm-kpis/
GET            /dashboard/bu-kpis/
GET            /dashboard/system-health/
GET            /dashboard/hours-report/?group_by=project&start_date=&end_date=
```

## Exports / Imports

```
GET            /exports/invoices/
GET            /exports/payments/
GET            /exports/expenses/
GET            /exports/time_entries/?month=4&year=2026
GET            /imports/
GET            /imports/{key}/template/
POST           /imports/{key}/upload/
```

## Configuration

```
GET/POST       /tax_schemes/
GET/POST       /tax_schemes/{id}/rates/
GET/POST       /business_units/
GET/POST       /labor_rules/
GET/POST       /expense_categories/
GET            /users/search/
```
