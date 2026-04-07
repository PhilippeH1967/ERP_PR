"""Dashboard KPI aggregation endpoints (Epic 8)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import (
    get_bu_director_kpis,
    get_hours_report,
    get_pm_financial_kpis,
    get_role_dashboard_kpis,
    get_system_health,
)


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
    """FR73 — PM financial KPIs: CA/salary ratio, billing rate, carnet de commandes."""
    tenant_id = getattr(request, "tenant_id", None)
    if not tenant_id:
        return Response({})
    kpis = get_pm_financial_kpis(request.user, tenant_id)
    return Response({"data": kpis})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def bu_director_kpis(request):
    """BU Director KPIs — projects, hours, utilization, budget."""
    tenant_id = getattr(request, "tenant_id", None)
    if not tenant_id:
        return Response({})
    kpis = get_bu_director_kpis(request.user, tenant_id)
    return Response({"data": kpis})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def system_health(request):
    """FR75 — Admin system health metrics."""
    tenant_id = getattr(request, "tenant_id", None)
    if not tenant_id:
        return Response({"data": {}})
    data = get_system_health(tenant_id)
    return Response({"data": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hours_report(request):
    """FR74 — Hours report by project, employee, or BU with billable breakdown.

    Query params:
      group_by: project | employee | bu (default: project)
      start_date: YYYY-MM-DD (default: first of current month)
      end_date: YYYY-MM-DD (default: today)
    """
    from datetime import date as dt_date

    tenant_id = getattr(request, "tenant_id", None)
    if not tenant_id:
        return Response({"data": []})

    group_by = request.query_params.get("group_by", "project")
    start = request.query_params.get("start_date")
    end = request.query_params.get("end_date")

    period_start = dt_date.fromisoformat(start) if start else None
    period_end = dt_date.fromisoformat(end) if end else None

    data = get_hours_report(tenant_id, group_by, period_start, period_end)
    return Response({"data": data, "group_by": group_by})
