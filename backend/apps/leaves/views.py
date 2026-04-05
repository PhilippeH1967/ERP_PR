"""Leave API views."""

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LeaveBank, LeaveRequest, LeaveType, PublicHoliday, RequestStatus
from .serializers import (
    LeaveBankSerializer,
    LeaveRequestSerializer,
    LeaveTypeSerializer,
    PublicHolidaySerializer,
)
from .services import create_time_entries_for_leave


def _get_tenant(request):
    from apps.core.models import Tenant
    tenant_id = getattr(request, "tenant_id", None)
    if tenant_id:
        return Tenant.objects.get(pk=tenant_id)
    return Tenant.objects.first()


class LeaveTypeViewSet(viewsets.ModelViewSet):
    """CRUD for leave types (admin-managed)."""

    serializer_class = LeaveTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = LeaveType.objects.filter(is_active=True)
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant(self.request))

    @action(detail=False, methods=["post"])
    def seed(self, request):
        """Seed standard Québec leave types."""
        from .services import seed_leave_types
        tenant = _get_tenant(request)
        count = seed_leave_types(tenant)
        return Response({"created": count})


class LeaveBankViewSet(viewsets.ModelViewSet):
    """Leave bank balances per employee."""

    serializer_class = LeaveBankSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["employee", "leave_type", "year"]

    def get_queryset(self):
        qs = LeaveBank.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        # Employees see only their own, PM/Finance/Admin see all
        from apps.core.models import ProjectRole, Role
        user_roles = set(
            ProjectRole.objects.filter(user=self.request.user).values_list("role", flat=True)
        )
        privileged = {Role.ADMIN, Role.FINANCE, Role.PAIE, Role.PM, Role.PROJECT_DIRECTOR}
        if not user_roles & privileged:
            qs = qs.filter(employee=self.request.user)
        return qs.select_related("leave_type")

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant(self.request))

    @action(detail=False, methods=["get"])
    def my_balances(self, request):
        """Get current user's leave balances for current year."""
        year = timezone.now().year
        banks = LeaveBank.objects.filter(
            employee=request.user, year=year,
        ).select_related("leave_type")
        if hasattr(request, "tenant_id") and request.tenant_id:
            banks = banks.filter(tenant_id=request.tenant_id)
        serializer = LeaveBankSerializer(banks, many=True)
        return Response(serializer.data)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """Leave request CRUD with approval workflow."""

    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["employee", "leave_type", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = LeaveRequest.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        # Employees see only their own, PM/Admin see all
        from apps.core.models import ProjectRole, Role
        user_roles = set(
            ProjectRole.objects.filter(user=self.request.user).values_list("role", flat=True)
        )
        privileged = {Role.ADMIN, Role.PM, Role.PROJECT_DIRECTOR, Role.PAIE}
        if not user_roles & privileged:
            qs = qs.filter(employee=self.request.user)
        return qs.select_related("leave_type", "employee", "approved_by")

    def perform_create(self, serializer):
        serializer.save(
            tenant=_get_tenant(self.request),
            employee=self.request.user,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """PM/Director approves a leave request."""
        leave = self.get_object()
        if leave.status != RequestStatus.PENDING:
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seules les demandes en attente peuvent être approuvées"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if leave.employee == request.user:
            return Response(
                {"error": {"code": "SELF_APPROVAL", "message": "Impossible d'approuver sa propre demande"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check balance
        year = leave.start_date.year
        bank = LeaveBank.objects.filter(
            tenant=leave.tenant, employee=leave.employee,
            leave_type=leave.leave_type, year=year,
        ).first()
        if bank and leave.leave_type.max_days_per_year:
            if bank.balance < float(leave.total_days):
                return Response(
                    {"error": {
                        "code": "INSUFFICIENT_BALANCE",
                        "message": f"Solde insuffisant: {bank.balance}j disponibles, {leave.total_days}j demandés",
                    }},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        leave.status = RequestStatus.APPROVED
        leave.approved_by = request.user
        leave.approved_at = timezone.now()
        leave.save()

        # Auto-create time entries
        entries_created = create_time_entries_for_leave(leave)

        serializer = self.get_serializer(leave)
        data = serializer.data
        data["time_entries_created_count"] = entries_created
        return Response(data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """PM/Director rejects a leave request."""
        leave = self.get_object()
        if leave.status != RequestStatus.PENDING:
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seules les demandes en attente peuvent être rejetées"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason = request.data.get("reason", "")
        leave.status = RequestStatus.REJECTED
        leave.rejection_reason = reason
        leave.save()

        return Response(self.get_serializer(leave).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Employee cancels their own pending request."""
        leave = self.get_object()
        if leave.employee != request.user:
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Seul le demandeur peut annuler"}},
                status=status.HTTP_403_FORBIDDEN,
            )
        if leave.status not in (RequestStatus.PENDING, RequestStatus.APPROVED):
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Impossible d'annuler cette demande"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave.status = RequestStatus.CANCELLED
        leave.save()
        return Response(self.get_serializer(leave).data)


class PublicHolidayViewSet(viewsets.ModelViewSet):
    """Public holidays management."""

    serializer_class = PublicHolidaySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PublicHoliday.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant(self.request))
