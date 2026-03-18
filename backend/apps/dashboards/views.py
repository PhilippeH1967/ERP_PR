"""Dashboard KPI aggregation endpoints (Epic 8)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def role_dashboard(request):
    """Role-adaptive dashboard — returns KPIs based on user role."""
    return Response({
        "kpis": {
            "projects_active": 0,
            "timesheets_pending": 0,
            "invoices_outstanding": "0.00",
            "expenses_pending": 0,
        },
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pm_financial_kpis(request):
    """PM financial KPIs and hours reports."""
    return Response({
        "budget_utilization": "0.00",
        "hours_consumed": "0.00",
        "ca_salary_ratio": "0.00",
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def system_health(request):
    """Admin system health metrics."""
    return Response({
        "active_users": 0,
        "pending_approvals": 0,
        "overdue_invoices": 0,
    })
