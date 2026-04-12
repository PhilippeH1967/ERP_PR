"""Sidebar badges and health indicators (Sprint 2 - B4 + B5)."""

from datetime import timedelta

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

    from apps.time_entries.models import WeeklyApproval
    from apps.expenses.models import ExpenseReport
    from apps.billing.models import Invoice
    from apps.suppliers.models import STInvoice
    from apps.projects.models import Project

    badges = {
        "approvals": WeeklyApproval.objects.filter(**tf, pm_status="PENDING").count(),
        "timesheets": WeeklyApproval.objects.filter(**tf, employee=request.user, pm_status="PENDING").count(),
        "expenses": ExpenseReport.objects.filter(**tf, status__in=["SUBMITTED", "PM_APPROVED"]).count(),
        "billing": Invoice.objects.filter(**tf, status__in=["DRAFT", "SUBMITTED"]).count(),
        "suppliers": STInvoice.objects.filter(**tf, status="received").count(),
        "period-locks": 0,
    }

    # Health indicators
    total_projects = Project.objects.filter(**tf, status="ACTIVE").count() or 1
    at_risk = Project.objects.filter(**tf, status="ON_HOLD").count()
    risk_pct = at_risk / total_projects * 100
    project_health = "green" if risk_pct < 10 else ("amber" if risk_pct < 25 else "red")

    aging_90 = Invoice.objects.filter(**tf, status="SENT", updated_at__lte=now - timedelta(days=90)).count()
    billing_health = "green" if aging_90 == 0 else ("amber" if aging_90 <= 3 else "red")

    health = {"projects": project_health, "billing": billing_health}

    has_new = {
        "projects": Project.objects.filter(**tf, created_at__gte=yesterday).exists(),
        "billing": Invoice.objects.filter(**tf, created_at__gte=yesterday).exists(),
    }

    return Response({"data": {"badges": badges, "health": health, "has_new": has_new}})
