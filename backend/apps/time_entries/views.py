"""Time entry API views."""

import django_filters
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


class TimeEntryFilter(django_filters.FilterSet):
    date__gte = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = TimeEntry
        fields = ["employee", "project", "phase", "date", "status"]


class TimeEntryViewSet(viewsets.ModelViewSet):
    """CRUD for time entries with auto-save support."""

    serializer_class = TimeEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TimeEntryFilter
    ordering = ["-date"]

    def get_queryset(self):
        qs = TimeEntry.objects.filter(employee=self.request.user)
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
            from apps.core.models import Tenant

            serializer.save(employee=self.request.user, tenant=Tenant.objects.first())

    @action(detail=False, methods=["post"])
    def submit_week(self, request):
        """Submit all draft entries for a week."""
        week_start = request.data.get("week_start")
        if not week_start:
            err = {"code": "MISSING_WEEK", "message": "week_start required", "details": []}
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)
        from datetime import timedelta, date as date_type

        if isinstance(week_start, str):
            week_start_date = date_type.fromisoformat(week_start)
        else:
            week_start_date = week_start
        week_end = week_start_date + timedelta(days=6)
        entries = TimeEntry.objects.filter(
            employee=request.user, date__gte=week_start_date, date__lte=week_end, status="DRAFT",
        )
        count = entries.update(status="SUBMITTED", rejection_reason="")

        # Auto-create WeeklyApproval record for PM review
        if count > 0:
            tenant_id = getattr(request, "tenant_id", None)
            if not tenant_id:
                from apps.core.models import Tenant
                tenant = Tenant.objects.first()
                tenant_id = tenant.id if tenant else None
            if tenant_id:
                from apps.core.models import Tenant
                WeeklyApproval.objects.get_or_create(
                    employee=request.user,
                    week_start=week_start_date,
                    defaults={
                        "week_end": week_end,
                        "tenant_id": tenant_id,
                        "pm_status": "PENDING",
                        "finance_status": "PENDING",
                    },
                )

        return Response({"submitted_count": count})

    @action(detail=False, methods=["get"])
    def weekly_stats(self, request):
        """Employee timesheet stats relative to displayed week."""
        from datetime import date as date_type, timedelta
        from decimal import Decimal

        from django.db.models import Sum

        user = request.user

        # Use week_start param or default to current week
        week_start_str = request.query_params.get("week_start")
        if week_start_str:
            week_start = date_type.fromisoformat(week_start_str)
        else:
            today = timezone.now().date()
            week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # Per-week totals for sparkline (4 weeks: 3 previous + current)
        week_totals = []
        for w in range(3, 0, -1):
            ws = week_start - timedelta(weeks=w)
            we = ws + timedelta(days=6)
            wt = TimeEntry.objects.filter(
                employee=user, date__gte=ws, date__lte=we,
            ).aggregate(t=Sum("hours"))["t"] or Decimal("0")
            week_totals.append(round(float(wt), 1))

        # Current week total
        current_total = TimeEntry.objects.filter(
            employee=user, date__gte=week_start, date__lte=week_end,
        ).aggregate(t=Sum("hours"))["t"] or Decimal("0")
        week_totals.append(round(float(current_total), 1))

        # Average over the 4 weeks
        avg_4_weeks = round(sum(week_totals) / 4, 1)

        # Billable rate for displayed week
        billable = TimeEntry.objects.filter(
            employee=user, date__gte=week_start, date__lte=week_end,
            project__is_internal=False,
        ).aggregate(t=Sum("hours"))["t"] or Decimal("0")
        total_hours = float(current_total)
        billable_rate = (
            round(float(billable) / total_hours * 100)
            if total_hours > 0
            else 0
        )

        return Response({
            "contract_hours": 40,
            "average_4_weeks": avg_4_weeks,
            "billable_rate_percent": billable_rate,
            "week_totals": week_totals,
        })

    @action(detail=False, methods=["post"])
    def copy_previous_week(self, request):
        """Copy previous week's entries as drafts for current week."""
        from datetime import timedelta

        week_start = request.data.get("week_start")
        if not week_start:
            err = {
                "code": "MISSING_WEEK",
                "message": "week_start required",
                "details": [],
            }
            return Response({"error": err}, status=status.HTTP_400_BAD_REQUEST)

        from datetime import date as date_type

        current_start = date_type.fromisoformat(week_start)
        prev_start = current_start - timedelta(weeks=1)
        prev_end = prev_start + timedelta(days=6)

        prev_entries = TimeEntry.objects.filter(
            employee=request.user,
            date__gte=prev_start,
            date__lte=prev_end,
        )

        created = 0
        for entry in prev_entries:
            new_date = entry.date + timedelta(weeks=1)
            if not TimeEntry.objects.filter(
                employee=request.user,
                project=entry.project,
                phase=entry.phase,
                date=new_date,
            ).exists():
                TimeEntry.objects.create(
                    tenant_id=entry.tenant_id,
                    employee=request.user,
                    project=entry.project,
                    phase=entry.phase,
                    date=new_date,
                    hours=entry.hours,
                    status="DRAFT",
                    is_favorite=entry.is_favorite,
                )
                created += 1

        return Response({"copied_count": created})

    @action(detail=False, methods=["post"])
    def approve_entries(self, request):
        """PM approves specific time entries on their projects."""
        from apps.projects.models import Project

        entry_ids = request.data.get("entry_ids", [])
        if not entry_ids:
            return Response(
                {"error": {"code": "MISSING_IDS", "message": "entry_ids required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        my_project_ids = set(
            Project.objects.filter(pm=request.user).values_list("id", flat=True)
        )
        entries = TimeEntry.objects.filter(
            id__in=entry_ids, status="SUBMITTED", project_id__in=my_project_ids,
        )
        # Anti-self-approval
        own = entries.filter(employee=request.user)
        if own.exists():
            return Response(
                {"error": {"code": "SELF_APPROVAL", "message": "Cannot approve own entries"}},
                status=status.HTTP_403_FORBIDDEN,
            )
        count = entries.update(status="PM_APPROVED")
        return Response({"approved_count": count})

    @action(detail=False, methods=["post"])
    def reject_entries(self, request):
        """PM rejects specific time entries — sends back to DRAFT."""
        from apps.projects.models import Project

        entry_ids = request.data.get("entry_ids", [])
        reason = request.data.get("reason", "")
        if not entry_ids:
            return Response(
                {"error": {"code": "MISSING_IDS", "message": "entry_ids required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        my_project_ids = set(
            Project.objects.filter(pm=request.user).values_list("id", flat=True)
        )
        entries = TimeEntry.objects.filter(
            id__in=entry_ids, status="SUBMITTED", project_id__in=my_project_ids,
        )
        count = entries.update(status="DRAFT", rejection_reason=reason)
        return Response({"rejected_count": count, "reason": reason})


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

    @action(detail=True, methods=["post"])
    def reject_pm(self, request, pk=None):
        """PM rejects timesheet with reason — sends back for modifications."""
        approval = self.get_object()
        if approval.pm_status != "PENDING":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seules les feuilles en attente peuvent être rejetées."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reason = request.data.get("reason", "")
        approval.pm_status = "REJECTED"
        approval.save()

        # Revert associated time entries back to DRAFT for modification
        from .models import TimeEntry

        TimeEntry.objects.filter(
            employee=approval.employee,
            date__gte=approval.week_start,
            date__lt=approval.week_start + timezone.timedelta(days=7),
            status="SUBMITTED",
        ).update(status="DRAFT", rejection_reason=reason)

        return Response(WeeklyApprovalSerializer(approval).data)

    @action(detail=True, methods=["post"])
    def reject_finance(self, request, pk=None):
        """Finance rejects timesheet."""
        approval = self.get_object()
        if approval.finance_status != "PENDING":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seules les feuilles en attente Finance peuvent être rejetées."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        approval.finance_status = "REJECTED"
        approval.save()
        return Response(WeeklyApprovalSerializer(approval).data)

    @action(detail=True, methods=["get"])
    def entries(self, request, pk=None):
        """Return time entries for this approval's employee/week with PM context."""
        from datetime import timedelta

        approval = self.get_object()
        week_end = approval.week_start + timedelta(days=6)
        entries = TimeEntry.objects.filter(
            employee=approval.employee,
            date__gte=approval.week_start,
            date__lte=week_end,
        ).select_related("project", "phase", "project__pm").order_by("project__code", "phase__name", "date")

        # Build per-project PM info
        project_pm_map = {}
        for e in entries:
            if e.project_id not in project_pm_map:
                pm = e.project.pm
                pm_name = ""
                if pm:
                    pm_name = f"{pm.first_name} {pm.last_name}".strip() or pm.email
                is_mine = pm and pm.id == request.user.id
                project_pm_map[e.project_id] = {
                    "pm_name": pm_name,
                    "is_my_project": is_mine,
                    "pm_approved": False,  # will set below
                }

        # Enrich with serialized data + pm context
        data = TimeEntrySerializer(entries, many=True).data
        for item in data:
            pid = item["project"]
            pm_info = project_pm_map.get(pid, {})
            item["pm_name"] = pm_info.get("pm_name", "")
            item["is_my_project"] = pm_info.get("is_my_project", False)

        # Color based on per-entry status + ownership
        for item in data:
            entry_status = item.get("status", "")
            if item.get("is_my_project"):
                if entry_status == "PM_APPROVED":
                    item["approval_color"] = "approved"
                else:
                    item["approval_color"] = "mine"
            else:
                if entry_status == "PM_APPROVED":
                    item["approval_color"] = "approved"
                else:
                    item["approval_color"] = "other"

        return Response(data)

    @action(detail=False, methods=["get"])
    def pm_dashboard(self, request):
        """CP dashboard: employees with hours on PM's projects, enriched data."""
        from collections import defaultdict
        from datetime import timedelta
        from decimal import Decimal

        from django.contrib.auth import get_user_model
        from django.db.models import Sum

        from apps.projects.models import Project

        User = get_user_model()

        # Find projects managed by current user
        my_projects = Project.objects.filter(pm=request.user)
        if not my_projects.exists():
            return Response({"projects": [], "employees": [], "kpis": {}})

        # Determine week — use ?week_start param or current week Monday
        week_start_str = request.query_params.get("week_start")
        if week_start_str:
            from datetime import date as date_type
            week_start = date_type.fromisoformat(week_start_str)
        else:
            today = timezone.now().date()
            week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # Get all submitted/approved entries on my projects for this week
        project_entries = TimeEntry.objects.filter(
            project__in=my_projects,
            date__gte=week_start,
            date__lte=week_end,
            status__in=["SUBMITTED", "PM_APPROVED"],
        ).select_related("project", "phase", "employee")

        # Build employee data
        employee_ids = set(e.employee_id for e in project_entries)
        employees_data = []

        for emp_id in employee_ids:
            emp = User.objects.get(pk=emp_id)
            emp_name = f"{emp.first_name} {emp.last_name}".strip() or emp.email

            # Hours on PM's projects this week
            emp_project_entries = [e for e in project_entries if e.employee_id == emp_id]
            project_hours = sum(float(e.hours) for e in emp_project_entries)

            # Total hours this week (all projects)
            all_week_entries = TimeEntry.objects.filter(
                employee_id=emp_id,
                date__gte=week_start,
                date__lte=week_end,
            )
            total_week = float(all_week_entries.aggregate(t=Sum("hours"))["t"] or Decimal("0"))

            # 4-week trend (3 previous weeks + current week)
            trend = []
            for w in range(3, 0, -1):
                ws = week_start - timedelta(weeks=w)
                we = ws + timedelta(days=6)
                wt = TimeEntry.objects.filter(
                    employee_id=emp_id, date__gte=ws, date__lte=we,
                ).aggregate(t=Sum("hours"))["t"] or Decimal("0")
                trend.append(float(wt))
            trend.append(total_week)  # current week as last bar

            # Billable rate (on PM's projects)
            billable_entries = [e for e in emp_project_entries if not getattr(e.project, "is_internal", False)]
            billable_hours = sum(float(e.hours) for e in billable_entries)
            billable_rate = round(billable_hours / project_hours * 100) if project_hours > 0 else 0

            # Per-project breakdown
            projects_breakdown = defaultdict(lambda: {"hours": 0, "project_code": "", "project_name": ""})
            for e in emp_project_entries:
                pb = projects_breakdown[e.project_id]
                pb["hours"] += float(e.hours)
                pb["project_code"] = e.project.code
                pb["project_name"] = e.project.name

            # Find WeeklyApproval for this employee
            approval = WeeklyApproval.objects.filter(
                employee_id=emp_id, week_start=week_start,
            ).first()

            # Per-PM status: if approved by another PM, still PENDING for me
            if approval:
                if approval.pm_status == "APPROVED" and approval.pm_approved_by_id != request.user.id:
                    effective_pm_status = "PENDING"
                    approved_by_other = f"{approval.pm_approved_by.first_name} {approval.pm_approved_by.last_name}".strip() if approval.pm_approved_by else ""
                else:
                    effective_pm_status = approval.pm_status
                    approved_by_other = ""
            else:
                effective_pm_status = None
                approved_by_other = ""

            employees_data.append({
                "employee_id": emp_id,
                "employee_name": emp_name,
                "employee_initials": (emp.first_name[:1] + emp.last_name[:1]).upper() if emp.first_name and emp.last_name else emp_name[:2].upper(),
                "project_hours": round(project_hours, 1),
                "total_week_hours": round(total_week, 1),
                "trend_4w": trend,
                "billable_rate": billable_rate,
                "projects": [
                    {"project_id": pid, **pdata}
                    for pid, pdata in projects_breakdown.items()
                ],
                "approval_id": approval.id if approval else None,
                "pm_status": effective_pm_status,
                "finance_status": approval.finance_status if approval else None,
                "approved_by_other": approved_by_other,
            })

        # KPIs
        total_project_hours = sum(e["project_hours"] for e in employees_data)
        total_billable = sum(
            float(e.hours) for e in project_entries
            if not getattr(e.project, "is_internal", False)
        )
        pending_count = sum(1 for e in employees_data if e["pm_status"] == "PENDING")

        # Project info for KPI cards
        projects_info = []
        for p in my_projects:
            week_hours = sum(
                float(e.hours) for e in project_entries if e.project_id == p.id
            )
            emp_count = len(set(e.employee_id for e in project_entries if e.project_id == p.id))
            projects_info.append({
                "id": p.id,
                "code": p.code,
                "name": p.name,
                "week_hours": round(week_hours, 1),
                "employee_count": emp_count,
            })

        return Response({
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "kpis": {
                "total_hours": round(total_project_hours, 1),
                "billable_rate": round(total_billable / total_project_hours * 100) if total_project_hours > 0 else 0,
                "billable_hours": round(total_billable, 1),
                "pending_count": pending_count,
                "employee_count": len(employees_data),
            },
            "projects": projects_info,
            "employees": employees_data,
        })


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
            from apps.core.models import Tenant

            serializer.save(unlocked_by=self.request.user, tenant=Tenant.objects.first())
