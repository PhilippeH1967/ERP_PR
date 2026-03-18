"""Time entry API views."""

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import cannot_approve_own

from .models import PeriodUnlock, TimeEntry, TimesheetLock, WeeklyApproval
from .serializers import (
    PeriodUnlockSerializer,
    TimeEntrySerializer,
    TimesheetLockSerializer,
    WeeklyApprovalSerializer,
)


class TimeEntryViewSet(viewsets.ModelViewSet):
    """CRUD for time entries with auto-save support."""

    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["employee", "project", "phase", "date", "status"]
    ordering = ["-date"]

    def get_queryset(self):
        qs = TimeEntry.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("project", "phase")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["if_match_version"] = self.request.headers.get("If-Match")
        return ctx

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(
                tenant=Tenant.objects.get(pk=tenant_id),
                employee=self.request.user,
            )
        else:
            serializer.save(employee=self.request.user)

    @action(detail=False, methods=["post"])
    def submit_week(self, request):
        """Submit all draft entries for a week."""
        week_start = request.data.get("week_start")
        if not week_start:
            err = {"code": "MISSING_WEEK", "message": "week_start required", "details": []}
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)
        entries = TimeEntry.objects.filter(
            employee=request.user, date__gte=week_start, status="DRAFT",
        )
        count = entries.update(status="SUBMITTED")
        return Response({"submitted_count": count})


class WeeklyApprovalViewSet(viewsets.ModelViewSet):
    """Weekly approval tracking with two-level workflow."""

    serializer_class = WeeklyApprovalSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["employee", "week_start", "pm_status", "finance_status"]

    def get_queryset(self):
        qs = WeeklyApproval.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    @action(detail=True, methods=["post"])
    def approve_pm(self, request, pk=None):
        """PM first-level approval with anti-self-approval."""
        approval = self.get_object()
        if not cannot_approve_own(request.user, approval.employee_id):
            err = {
                "code": "SELF_APPROVAL",
                "message": "Cannot approve own timesheet",
                "details": [],
            }
            return Response({"error": err}, status=status.HTTP_403_FORBIDDEN)
        approval.pm_status = "APPROVED"
        approval.pm_approved_by = request.user
        approval.pm_approved_at = timezone.now()
        approval.save()
        return Response(WeeklyApprovalSerializer(approval).data)

    @action(detail=True, methods=["post"])
    def approve_finance(self, request, pk=None):
        """Finance second-level approval."""
        approval = self.get_object()
        if not cannot_approve_own(request.user, approval.employee_id):
            err = {
                "code": "SELF_APPROVAL",
                "message": "Cannot approve own timesheet",
                "details": [],
            }
            return Response({"error": err}, status=status.HTTP_403_FORBIDDEN)
        approval.finance_status = "APPROVED"
        approval.finance_approved_by = request.user
        approval.finance_approved_at = timezone.now()
        approval.save()
        return Response(WeeklyApprovalSerializer(approval).data)


class TimesheetLockViewSet(viewsets.ModelViewSet):
    """Phase and person-level locking."""

    serializer_class = TimesheetLockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TimesheetLock.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(
                tenant=Tenant.objects.get(pk=tenant_id),
                locked_by=self.request.user,
            )
        else:
            serializer.save(locked_by=self.request.user)


class PeriodUnlockViewSet(viewsets.ModelViewSet):
    """Temporary period unlocks for corrections."""

    serializer_class = PeriodUnlockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PeriodUnlock.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(
                tenant=Tenant.objects.get(pk=tenant_id),
                unlocked_by=self.request.user,
            )
        else:
            serializer.save(unlocked_by=self.request.user)
