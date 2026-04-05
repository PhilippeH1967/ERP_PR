"""Planning API views."""

from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Availability, Milestone, ResourceAllocation
from .serializers import AvailabilitySerializer, MilestoneSerializer, ResourceAllocationSerializer


def _get_tenant(request):
    from apps.core.models import Tenant
    tid = getattr(request, "tenant_id", None)
    return Tenant.objects.get(pk=tid) if tid else Tenant.objects.first()


class ResourceAllocationViewSet(viewsets.ModelViewSet):
    """CRUD for resource allocations + planning dashboard."""

    serializer_class = ResourceAllocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["employee", "project", "status"]
    ordering = ["start_date"]

    def get_queryset(self):
        qs = ResourceAllocation.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("employee", "project", "phase", "task")

    def perform_create(self, serializer):
        serializer.save(
            tenant=_get_tenant(self.request),
            created_by=self.request.user,
        )

    @action(detail=False, methods=["get"])
    def global_planning(self, request):
        """US-PL01 — Global resource planning view.

        Returns employees with their allocations and load status.
        Query params: start_date, end_date (default: current month).
        """
        start = request.query_params.get("start_date")
        end = request.query_params.get("end_date")
        if not start:
            today = timezone.now().date()
            start = today.replace(day=1).isoformat()
            end = (today.replace(day=28) + timedelta(days=4)).replace(day=1).isoformat()

        qs = self.get_queryset().filter(
            status="ACTIVE",
            start_date__lte=end,
            end_date__gte=start,
        )

        # Group by employee
        employees = {}
        for alloc in qs:
            eid = alloc.employee_id
            if eid not in employees:
                name = alloc.employee.get_full_name() or alloc.employee.username
                # Get contract hours
                try:
                    ch = alloc.employee.tenant_association.effective_contract_hours
                except Exception:
                    ch = 40
                employees[eid] = {
                    "employee_id": eid,
                    "employee_name": name,
                    "contract_hours": ch,
                    "total_planned_hours_week": 0,
                    "allocations": [],
                    "load_status": "normal",
                }
            emp = employees[eid]
            emp["total_planned_hours_week"] += float(alloc.hours_per_week)
            emp["allocations"].append({
                "project_code": alloc.project.code,
                "project_name": alloc.project.name,
                "phase_name": alloc.phase.name if alloc.phase else "",
                "hours_per_week": float(alloc.hours_per_week),
                "start_date": alloc.start_date.isoformat(),
                "end_date": alloc.end_date.isoformat(),
            })

        # Compute load status
        for emp in employees.values():
            ratio = emp["total_planned_hours_week"] / emp["contract_hours"] if emp["contract_hours"] else 0
            if ratio > 1.2:
                emp["load_status"] = "critical"
            elif ratio > 1.0:
                emp["load_status"] = "overload"
            elif ratio < 0.5:
                emp["load_status"] = "underload"
            else:
                emp["load_status"] = "normal"
            emp["load_percent"] = round(ratio * 100, 1)

        return Response({
            "period": {"start": start, "end": end},
            "employees": list(employees.values()),
        })

    @action(detail=False, methods=["get"])
    def load_alerts(self, request):
        """US-PL11 — Overload/underload detection for next 4 weeks."""
        today = timezone.now().date()
        end = today + timedelta(weeks=4)

        qs = self.get_queryset().filter(
            status="ACTIVE",
            start_date__lte=end,
            end_date__gte=today,
        )

        # Aggregate hours per employee
        by_employee = {}
        for alloc in qs:
            eid = alloc.employee_id
            if eid not in by_employee:
                try:
                    ch = alloc.employee.tenant_association.effective_contract_hours
                except Exception:
                    ch = 40
                by_employee[eid] = {
                    "employee_id": eid,
                    "employee_name": alloc.employee.get_full_name() or alloc.employee.username,
                    "contract_hours": ch,
                    "planned_hours_week": 0,
                }
            by_employee[eid]["planned_hours_week"] += float(alloc.hours_per_week)

        alerts = []
        for emp in by_employee.values():
            ratio = emp["planned_hours_week"] / emp["contract_hours"] if emp["contract_hours"] else 0
            if ratio > 1.0:
                alerts.append({
                    **emp,
                    "alert_type": "critical" if ratio > 1.2 else "overload",
                    "load_percent": round(ratio * 100, 1),
                })
            elif ratio < 0.5 and emp["planned_hours_week"] > 0:
                alerts.append({
                    **emp,
                    "alert_type": "underload",
                    "load_percent": round(ratio * 100, 1),
                })

        return Response({"alerts": alerts, "period": {"start": today.isoformat(), "end": end.isoformat()}})


class MilestoneViewSet(viewsets.ModelViewSet):
    """CRUD for project milestones."""

    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project", "status"]

    def get_queryset(self):
        qs = Milestone.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("project")

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant(self.request))

    @action(detail=False, methods=["post"])
    def auto_update_status(self, request):
        """Auto-detect overdue milestones."""
        today = timezone.now().date()
        updated = Milestone.objects.filter(
            status="UPCOMING", date__lt=today,
        ).update(status="OVERDUE")
        return Response({"updated_to_overdue": updated})


class AvailabilityViewSet(viewsets.ModelViewSet):
    """Employee availability records."""

    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["employee", "date", "is_working_day"]

    def get_queryset(self):
        qs = Availability.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("employee")

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant(self.request))

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """Generate availability records for a period.

        Computes: working_days - leaves = capacity per day.
        """
        employee_id = request.data.get("employee_id")
        start = request.data.get("start_date")
        end = request.data.get("end_date")

        if not all([employee_id, start, end]):
            return Response(
                {"error": {"code": "MISSING_FIELDS", "message": "employee_id, start_date, end_date required"}},
                status=400,
            )

        from datetime import date as dt_date
        from django.contrib.auth import get_user_model
        from apps.leaves.models import LeaveRequest, RequestStatus

        User = get_user_model()
        employee = User.objects.get(pk=employee_id)
        tenant = _get_tenant(request)

        try:
            contract_hours = employee.tenant_association.effective_contract_hours / 5  # per day
        except Exception:
            contract_hours = 8

        # Get approved leaves in period
        leaves = LeaveRequest.objects.filter(
            employee=employee,
            status=RequestStatus.APPROVED,
            start_date__lte=end,
            end_date__gte=start,
        )
        leave_dates = {}
        for leave in leaves:
            d = leave.start_date
            while d <= leave.end_date:
                if d.weekday() < 5:
                    leave_dates[d] = leave.leave_type.code
                d += timedelta(days=1)

        # Generate records
        from datetime import datetime
        current = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        created = 0

        while current <= end_date:
            is_working = current.weekday() < 5
            leave_code = leave_dates.get(current, "")
            capacity = 0 if leave_code else (contract_hours if is_working else 0)

            Availability.objects.update_or_create(
                tenant=tenant, employee=employee, date=current,
                defaults={
                    "contractual_hours": contract_hours if is_working else 0,
                    "capacity_hours": capacity,
                    "is_working_day": is_working,
                    "leave_type": leave_code,
                },
            )
            created += 1
            current += timedelta(days=1)

        return Response({"generated": created})
