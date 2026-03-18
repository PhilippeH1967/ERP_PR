"""Dashboard KPI aggregation services."""

from decimal import Decimal

from django.db.models import Sum


def get_role_dashboard_kpis(user, tenant_id: int) -> dict:
    """Aggregate KPIs for the authenticated user's dashboard."""
    from apps.billing.models import Invoice
    from apps.expenses.models import ExpenseReport
    from apps.projects.models import Project
    from apps.time_entries.models import WeeklyApproval

    projects_active = Project.objects.filter(
        tenant_id=tenant_id, status="ACTIVE"
    ).count()

    timesheets_pending = WeeklyApproval.objects.filter(
        tenant_id=tenant_id, pm_status="PENDING"
    ).count()

    invoices_outstanding = Invoice.objects.filter(
        tenant_id=tenant_id, status="SENT"
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    expenses_pending = ExpenseReport.objects.filter(
        tenant_id=tenant_id, status="SUBMITTED"
    ).count()

    return {
        "projects_active": projects_active,
        "timesheets_pending": timesheets_pending,
        "invoices_outstanding": str(invoices_outstanding),
        "expenses_pending": expenses_pending,
    }


def get_pm_financial_kpis(user, tenant_id: int) -> dict:
    """PM-specific financial KPIs across managed projects."""
    from apps.billing.models import Invoice
    from apps.projects.models import Project
    from apps.time_entries.models import TimeEntry

    managed = Project.objects.filter(tenant_id=tenant_id, pm=user, status="ACTIVE")
    project_ids = list(managed.values_list("id", flat=True))

    total_invoiced = Invoice.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    total_hours = TimeEntry.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

    return {
        "projects_managed": len(project_ids),
        "total_invoiced": str(total_invoiced),
        "total_hours": str(total_hours),
    }
