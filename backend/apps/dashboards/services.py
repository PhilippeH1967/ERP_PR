"""Dashboard KPI aggregation services."""

from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.utils import timezone


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
    """FR73 — PM financial KPIs across managed projects."""
    from apps.billing.models import Invoice
    from apps.projects.models import Phase, Project
    from apps.time_entries.models import TimeEntry

    today = timezone.now().date()
    month_start = today.replace(day=1)

    managed = Project.objects.filter(tenant_id=tenant_id, pm=user, status="ACTIVE")
    project_ids = list(managed.values_list("id", flat=True))

    total_invoiced = Invoice.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    total_hours = TimeEntry.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

    # Hours this month
    hours_this_month = TimeEntry.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id,
        date__gte=month_start, date__lte=today,
    ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

    # Billable hours (non-internal projects)
    billable_hours = TimeEntry.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id,
        project__is_internal=False,
    ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

    billing_rate = round(float(billable_hours) / float(total_hours) * 100, 1) if total_hours else 0

    # CA/Salary ratio — simplified: total_invoiced / (total_hours * avg_hourly_cost)
    avg_hourly_cost = 45  # Placeholder — should come from HR config
    salary_cost = float(total_hours) * avg_hourly_cost
    ca_salary_ratio = round(float(total_invoiced) / salary_cost, 2) if salary_cost > 0 else 0

    # Actions required = pending approvals on PM's projects
    from apps.time_entries.models import WeeklyApproval
    actions_required = WeeklyApproval.objects.filter(
        tenant_id=tenant_id, pm_status="PENDING",
    ).count()

    # Budget total (phases of managed projects)
    budget_total = Phase.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id,
    ).aggregate(total=Sum("budgeted_cost"))["total"] or Decimal("0")

    # Carnet de commandes = budget_total - total_invoiced
    carnet_commandes = float(budget_total) - float(total_invoiced)

    return {
        "projects_managed": len(project_ids),
        "total_invoiced": str(total_invoiced),
        "total_hours": str(total_hours),
        "hours_this_month": str(hours_this_month),
        "billing_rate": billing_rate,
        "ca_salary_ratio": ca_salary_ratio,
        "actions_required": actions_required,
        "carnet_commandes": str(round(carnet_commandes, 2)),
        "budget_total": str(budget_total),
    }


def get_bu_director_kpis(user, tenant_id: int) -> dict:
    """BU Director KPIs — projects, hours, utilization, budget for the unit."""
    from apps.billing.models import Invoice
    from apps.projects.models import Phase, Project
    from apps.time_entries.models import TimeEntry

    bu_filter = {"tenant_id": tenant_id, "status": "ACTIVE"}
    user_bu = getattr(user, "business_unit", None) or ""
    if user_bu:
        bu_filter["business_unit"] = user_bu

    projects = Project.objects.filter(**bu_filter)
    project_ids = list(projects.values_list("id", flat=True))
    projects_in_bu = len(project_ids)

    total_hours_bu = TimeEntry.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

    budgeted_hours = Phase.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("budgeted_hours"))["total"] or Decimal("0")

    utilization_percent = (
        float(total_hours_bu / budgeted_hours * 100) if budgeted_hours else 0.0
    )

    budgeted_cost = Phase.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("budgeted_cost"))["total"] or Decimal("0")

    total_invoiced = Invoice.objects.filter(
        project_id__in=project_ids, tenant_id=tenant_id
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    budget_consumed_percent = (
        float(total_invoiced / budgeted_cost * 100) if budgeted_cost else 0.0
    )

    return {
        "projects_in_bu": projects_in_bu,
        "total_hours_bu": str(total_hours_bu),
        "utilization_percent": round(utilization_percent, 1),
        "budget_consumed_percent": round(budget_consumed_percent, 1),
    }


def get_hours_report(tenant_id: int, group_by="project", period_start=None, period_end=None) -> list:
    """FR74 — Hours report by project, person, or BU with billable breakdown."""
    from apps.time_entries.models import TimeEntry

    today = timezone.now().date()
    if not period_start:
        period_start = today.replace(day=1)
    if not period_end:
        period_end = today

    qs = TimeEntry.objects.filter(
        tenant_id=tenant_id,
        date__gte=period_start,
        date__lte=period_end,
    )

    if group_by == "project":
        data = qs.values(
            "project__code", "project__name", "project__is_internal"
        ).annotate(
            total_hours=Sum("hours"),
            entry_count=Count("id"),
        ).order_by("project__code")
        return [
            {
                "group": r["project__code"],
                "label": r["project__name"],
                "total_hours": float(r["total_hours"]),
                "billable": not r["project__is_internal"],
                "entries": r["entry_count"],
            }
            for r in data
        ]

    elif group_by == "employee":
        data = qs.values(
            "employee__username", "employee__first_name", "employee__last_name"
        ).annotate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(project__is_internal=False)),
        ).order_by("employee__username")
        return [
            {
                "group": r["employee__username"],
                "label": f"{r['employee__first_name'] or ''} {r['employee__last_name'] or ''}".strip() or r["employee__username"],
                "total_hours": float(r["total_hours"]),
                "billable_hours": float(r["billable_hours"] or 0),
                "billing_rate": round(float(r["billable_hours"] or 0) / float(r["total_hours"]) * 100, 1) if r["total_hours"] else 0,
            }
            for r in data
        ]

    elif group_by == "bu":
        data = qs.values(
            "project__business_unit"
        ).annotate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(project__is_internal=False)),
            project_count=Count("project", distinct=True),
            employee_count=Count("employee", distinct=True),
        ).order_by("project__business_unit")
        return [
            {
                "group": r["project__business_unit"] or "Non assigné",
                "total_hours": float(r["total_hours"]),
                "billable_hours": float(r["billable_hours"] or 0),
                "projects": r["project_count"],
                "employees": r["employee_count"],
            }
            for r in data
        ]

    return []


def get_system_health(tenant_id: int) -> dict:
    """FR75 — System health metrics for admin."""
    from django.contrib.auth import get_user_model

    from apps.billing.models import Invoice
    from apps.core.models import UserTenantAssociation
    from apps.time_entries.models import WeeklyApproval

    User = get_user_model()
    today = timezone.now().date()

    active_users = UserTenantAssociation.objects.filter(
        tenant_id=tenant_id, user__is_active=True,
    ).count()

    pending_approvals = WeeklyApproval.objects.filter(
        tenant_id=tenant_id, pm_status="PENDING",
    ).count()

    overdue_invoices = Invoice.objects.filter(
        tenant_id=tenant_id, status="SENT",
        date_sent__lt=today - timedelta(days=30),
    ).count()

    # Recent activity (last 7 days)
    from apps.time_entries.models import TimeEntry
    recent_entries = TimeEntry.objects.filter(
        tenant_id=tenant_id,
        created_at__gte=timezone.now() - timedelta(days=7),
    ).count()

    active_this_week = TimeEntry.objects.filter(
        tenant_id=tenant_id,
        date__gte=today - timedelta(days=7),
    ).values("employee").distinct().count()

    return {
        "active_users": active_users,
        "active_this_week": active_this_week,
        "pending_approvals": pending_approvals,
        "overdue_invoices": overdue_invoices,
        "recent_entries_7d": recent_entries,
    }
