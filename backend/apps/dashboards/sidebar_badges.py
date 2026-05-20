"""Sidebar badges and health indicators (Sprint 2 - B4 + B5)."""

from datetime import timedelta

from django.db.models import Exists, OuterRef
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sidebar_badges(request):
    """Return badge counts, health, and freshness for sidebar items."""
    tenant_id = getattr(request, "tenant_id", None)
    tf = {"tenant_id": tenant_id} if tenant_id else {}
    now = timezone.now()
    yesterday = now - timedelta(hours=24)

    from apps.billing.models import Invoice
    from apps.core.models import ProjectRole, Role
    from apps.expenses.models import ExpenseReport
    from apps.projects.models import Project
    from apps.suppliers.models import STInvoice
    from apps.time_entries.models import TimeEntry, WeeklyApproval

    # S-080/S-081: the `approvals` badge must reflect what the connected
    # user can act on. For ADMIN/PAIE/FINANCE → tenant-wide; for a PM →
    # only WeeklyApprovals whose employee has timesheet entries on the
    # PM's projects in the same week (matches pm_dashboard's filter).
    user_roles = set(
        ProjectRole.objects.filter(user=request.user, **tf).values_list("role", flat=True)
    )
    cross_tenant_roles = {Role.ADMIN, Role.PAIE, Role.FINANCE}
    approvals_qs = WeeklyApproval.objects.filter(**tf, pm_status="PENDING")
    if user_roles.isdisjoint(cross_tenant_roles):
        my_project_ids = Project.objects.filter(**tf, pm=request.user).values_list("id", flat=True)
        if my_project_ids:
            entry_on_my_project = TimeEntry.objects.filter(
                employee_id=OuterRef("employee_id"),
                project_id__in=list(my_project_ids),
                date__gte=OuterRef("week_start"),
                date__lte=OuterRef("week_end"),
            )
            approvals_qs = approvals_qs.annotate(_rel=Exists(entry_on_my_project)).filter(_rel=True)
        else:
            approvals_qs = approvals_qs.none()

    badges = {
        "approvals": approvals_qs.count(),
        "timesheets": WeeklyApproval.objects.filter(
            **tf, employee=request.user, pm_status="PENDING"
        ).count(),
        "expenses": ExpenseReport.objects.filter(
            **tf, status__in=["SUBMITTED", "PM_APPROVED"]
        ).count(),
        "billing": Invoice.objects.filter(**tf, status__in=["DRAFT", "SUBMITTED"]).count(),
        "suppliers": STInvoice.objects.filter(**tf, status="received").count(),
        "period-locks": 0,
    }

    # Health indicators
    total_projects = Project.objects.filter(**tf, status="ACTIVE").count() or 1
    at_risk = Project.objects.filter(**tf, status="ON_HOLD").count()
    risk_pct = at_risk / total_projects * 100
    project_health = "green" if risk_pct < 10 else ("amber" if risk_pct < 25 else "red")

    aging_90 = Invoice.objects.filter(
        **tf, status="SENT", updated_at__lte=now - timedelta(days=90)
    ).count()
    billing_health = "green" if aging_90 == 0 else ("amber" if aging_90 <= 3 else "red")

    health = {"projects": project_health, "billing": billing_health}

    has_new = {
        "projects": Project.objects.filter(**tf, created_at__gte=yesterday).exists(),
        "billing": Invoice.objects.filter(**tf, created_at__gte=yesterday).exists(),
    }

    return Response({"data": {"badges": badges, "health": health, "has_new": has_new}})
