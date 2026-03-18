"""Dashboard KPI aggregation endpoints (Epic 8)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import get_pm_financial_kpis, get_role_dashboard_kpis


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def role_dashboard(request):
    """Role-adaptive dashboard — returns KPIs based on user role."""
    tenant_id = getattr(request, "tenant_id", None)
    if not tenant_id:
        return Response({"kpis": {}})
    kpis = get_role_dashboard_kpis(request.user, tenant_id)
    return Response({"kpis": kpis})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pm_financial_kpis(request):
    """PM financial KPIs and hours reports."""
    tenant_id = getattr(request, "tenant_id", None)
    if not tenant_id:
        return Response({})
    kpis = get_pm_financial_kpis(request.user, tenant_id)
    return Response(kpis)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def system_health(request):
    """Admin system health metrics."""
    from apps.billing.models import Invoice
    from apps.time_entries.models import WeeklyApproval

    tenant_id = getattr(request, "tenant_id", None)
    pending = WeeklyApproval.objects.filter(
        tenant_id=tenant_id, pm_status="PENDING"
    ).count() if tenant_id else 0
    overdue = Invoice.objects.filter(
        tenant_id=tenant_id, status="SENT"
    ).count() if tenant_id else 0

    return Response({
        "active_users": 0,
        "pending_approvals": pending,
        "overdue_invoices": overdue,
    })
