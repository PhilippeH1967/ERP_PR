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


def _has_lock_role(user, tenant_id=None):
    """Check if user has ADMIN, FINANCE, or PAIE role."""
    from apps.core.models import ProjectRole, Role

    qs = ProjectRole.objects.filter(
        user=user, role__in=[Role.ADMIN, Role.FINANCE, Role.PAIE],
    )
    if tenant_id:
        qs = qs.filter(tenant_id=tenant_id)
    return qs.exists()


def _get_tenant(request):
    """Get tenant from request or user association. Never returns None."""
    from apps.core.models import Tenant, UserTenantAssociation

    tenant_id = getattr(request, "tenant_id", None)
    if tenant_id:
        return Tenant.objects.get(pk=tenant_id)
    # Fallback: user's tenant association
    assoc = UserTenantAssociation.objects.filter(user=request.user).first()
    if assoc:
        return assoc.tenant
    # Last resort
    return Tenant.objects.first()


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
        # When filtering by project, privileged roles see all entries (for project detail tabs)
        project_filter = self.request.query_params.get("project")
        if project_filter:
            from apps.core.models import ProjectRole, Role
            user_roles = set(
                ProjectRole.objects.filter(user=self.request.user).values_list("role", flat=True)
            )
            privileged = {Role.ADMIN, Role.FINANCE, Role.PM, Role.PROJECT_DIRECTOR, Role.BU_DIRECTOR, Role.PAIE}
            if user_roles & privileged:
                qs = TimeEntry.objects.all()
            else:
                qs = TimeEntry.objects.filter(employee=self.request.user)
        else:
            qs = TimeEntry.objects.filter(employee=self.request.user)
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("project", "phase", "task")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["if_match_version"] = self.request.headers.get("If-Match")
        return ctx

    class PeriodLockError(Exception):
        """Raised when an operation is blocked by period lock/freeze."""
        def __init__(self, code, message):
            self.code = code
            self.message = message

    def _check_period_locked(self, date_val):
        """Check if a period is locked globally on this date."""
        from .models import PeriodFreeze, PeriodUnlock

        tenant_id = getattr(self.request, "tenant_id", None)

        # Check 1: global freeze date (with unlock exceptions)
        freeze_qs = PeriodFreeze.objects.all()
        if tenant_id:
            freeze_qs = freeze_qs.filter(tenant_id=tenant_id)
        latest_freeze = freeze_qs.order_by("-freeze_before").first()
        if latest_freeze and date_val < latest_freeze.freeze_before:
            unlock_exception = PeriodUnlock.objects.filter(
                period_start__lte=date_val, period_end__gte=date_val,
            )
            if tenant_id:
                unlock_exception = unlock_exception.filter(tenant_id=tenant_id)
            if not unlock_exception.exists():
                raise self.PeriodLockError("PERIOD_FROZEN", f"Les périodes avant le {latest_freeze.freeze_before} sont gelées.")

        # Check 2: exact date has LOCKED entries (unless unlocked)
        qs = TimeEntry.objects.filter(date=date_val, status="LOCKED")
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        if qs.exists():
            unlock_exception = PeriodUnlock.objects.filter(
                period_start__lte=date_val, period_end__gte=date_val,
            )
            if tenant_id:
                unlock_exception = unlock_exception.filter(tenant_id=tenant_id)
            if not unlock_exception.exists():
                raise self.PeriodLockError("PERIOD_LOCKED", f"La période du {date_val} est verrouillée.")

    def _check_phase_locked(self, project_id, phase_id):
        """Check if a phase is locked via TimesheetLock."""
        from .models import TimesheetLock
        tenant_id = getattr(self.request, "tenant_id", None)
        lock_qs = TimesheetLock.objects.filter(project_id=project_id, lock_type="PHASE")
        if tenant_id:
            lock_qs = lock_qs.filter(tenant_id=tenant_id)
        # Check specific phase lock or project-wide lock (phase=None)
        if lock_qs.filter(phase_id=phase_id).exists() or lock_qs.filter(phase__isnull=True).exists():
            raise self.PeriodLockError("PHASE_LOCKED", "Cette phase/tâche est verrouillée.")

    def _require_lock_role(self):
        """Raise 403 if user lacks ADMIN/FINANCE/PAIE role."""
        tenant_id = getattr(self.request, "tenant_id", None)
        if not _has_lock_role(self.request.user, tenant_id):
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Seuls les rôles ADMIN, FINANCE ou PAIE peuvent verrouiller/déverrouiller."}},
                status=status.HTTP_403_FORBIDDEN,
            )
        return None

    def _handle_lock_check(self, date_val, project_id=None, phase_id=None):
        """Run all lock checks and return Response if blocked, None if ok."""
        try:
            self._check_period_locked(date_val)
            if project_id is not None:
                self._check_phase_locked(project_id, phase_id)
        except self.PeriodLockError as e:
            return Response(
                {"error": {"code": e.code, "message": e.message}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date_val = serializer.validated_data.get("date")
        project_id = serializer.validated_data.get("project")
        phase_id = serializer.validated_data.get("phase")
        proj_id = project_id.id if hasattr(project_id, "id") else project_id
        ph_id = phase_id.id if hasattr(phase_id, "id") else phase_id
        blocked = self._handle_lock_check(date_val, proj_id, ph_id)
        if blocked:
            return blocked
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

            serializer.save(employee=self.request.user, tenant=_get_tenant(self.request))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "LOCKED":
            return Response(
                {"error": {"code": "ENTRY_LOCKED", "message": "Cette entrée est verrouillée."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        blocked = self._handle_lock_check(instance.date, instance.project_id, instance.phase_id)
        if blocked:
            return blocked
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == "LOCKED":
            return Response(
                {"error": {"code": "ENTRY_LOCKED", "message": "Cette entrée est verrouillée."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        blocked = self._handle_lock_check(instance.date, instance.project_id, instance.phase_id)
        if blocked:
            return blocked
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

        # Check period lock for all days in the week
        for day_offset in range(7):
            try:
                self._check_period_locked(week_start_date + timedelta(days=day_offset))
            except Exception:
                return Response(
                    {"error": {"code": "PERIOD_LOCKED", "message": f"La période est verrouillée. Impossible de soumettre."}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        entries = TimeEntry.objects.filter(
            employee=request.user, date__gte=week_start_date, date__lte=week_end, status="DRAFT",
        )
        count = entries.update(status="SUBMITTED", rejection_reason="")

        # Auto-create WeeklyApproval record for PM review
        if count > 0:
            tenant_id = getattr(request, "tenant_id", None)
            if not tenant_id:
                from apps.core.models import Tenant
                tenant = _get_tenant(self.request)
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

        # Get contract hours from employee profile
        try:
            uta = request.user.tenant_association
            ch = uta.effective_contract_hours
        except Exception:
            ch = 40

        return Response({
            "contract_hours": ch,
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

        # Check if target week is locked
        for day_offset in range(7):
            try:
                self._check_period_locked(current_start + timedelta(days=day_offset))
            except Exception:
                return Response(
                    {"error": {"code": "PERIOD_LOCKED", "message": "La semaine cible est verrouillée. Impossible de copier."}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        created = 0
        for entry in prev_entries:
            # Skip locked entries — don't copy from a locked period
            if entry.status == "LOCKED":
                continue
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

    @action(detail=False, methods=["get"])
    def is_period_locked(self, request):
        """Check if a period is locked — via freeze date or direct lock, with unlock exceptions."""
        from datetime import date as date_type, timedelta

        from .models import PeriodFreeze, PeriodUnlock

        week_start = request.query_params.get("week_start")
        if not week_start:
            return Response({"locked": False})
        ws = date_type.fromisoformat(week_start)
        we = ws + timedelta(days=6)
        tenant_id = getattr(request, "tenant_id", None)

        # Check for unlock exception on this week
        unlock_qs = PeriodUnlock.objects.filter(
            period_start__lte=ws, period_end__gte=we,
        )
        if tenant_id:
            unlock_qs = unlock_qs.filter(tenant_id=tenant_id)
        has_unlock = unlock_qs.exists()

        if has_unlock:
            return Response({"locked": False, "reason": "Déverrouillée temporairement"})

        # Check 1: global freeze date
        freeze_qs = PeriodFreeze.objects.all()
        if tenant_id:
            freeze_qs = freeze_qs.filter(tenant_id=tenant_id)
        latest_freeze = freeze_qs.order_by("-freeze_before").first()
        if latest_freeze and we < latest_freeze.freeze_before:
            return Response({"locked": True, "reason": f"Gelé avant le {latest_freeze.freeze_before}"})

        # Check 2: direct locked entries in this week
        locked_qs = TimeEntry.objects.filter(status="LOCKED")
        if tenant_id:
            locked_qs = locked_qs.filter(tenant_id=tenant_id)
        if locked_qs.filter(date__gte=ws, date__lte=we).exists():
            return Response({"locked": True})

        return Response({"locked": False})

    @action(detail=False, methods=["post"])
    def unlock_period(self, request):
        """Unlock a period — reverts LOCKED entries to DRAFT for corrections."""
        from datetime import date as date_type, timedelta

        denied = self._require_lock_role()
        if denied:
            return denied

        period_start = request.data.get("period_start")
        period_end = request.data.get("period_end")
        if not period_start or not period_end:
            return Response(
                {"error": {"code": "MISSING_DATES", "message": "period_start and period_end required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ps = date_type.fromisoformat(period_start) if isinstance(period_start, str) else period_start
        pe = date_type.fromisoformat(period_end) if isinstance(period_end, str) else period_end

        qs = TimeEntry.objects.filter(
            date__gte=ps, date__lte=pe, status="LOCKED",
        )
        tenant_id = getattr(request, "tenant_id", None)
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        # Revert to SUBMITTED (not DRAFT) — preserves the workflow
        # Employee must re-submit, PM must re-approve if changes needed
        count = qs.update(status="SUBMITTED")

        return Response({"unlocked_count": count, "period_start": ps.isoformat(), "period_end": pe.isoformat()})

    @action(detail=False, methods=["get"])
    def period_summary(self, request):
        """Return all weeks that have entries, with lock status."""
        from collections import defaultdict
        from datetime import timedelta
        from decimal import Decimal

        from django.db.models import Count, Min, Max, Sum

        denied = self._require_lock_role()
        if denied:
            return denied

        tenant_id = getattr(request, "tenant_id", None)
        base_qs = TimeEntry.objects.all()
        if tenant_id:
            base_qs = base_qs.filter(tenant_id=tenant_id)

        # Find date range
        bounds = base_qs.aggregate(min=Min("date"), max=Max("date"))
        if not bounds["min"]:
            return Response({"weeks": []})

        # Walk from first Sunday to last Saturday
        first = bounds["min"]
        # Go back to Sunday
        first_sunday = first - timedelta(days=(first.weekday() + 1) % 7)
        last = bounds["max"]
        last_saturday = last + timedelta(days=(5 - last.weekday()) % 7)

        weeks = []
        current = first_sunday
        while current <= last_saturday:
            week_end = current + timedelta(days=6)
            entries = base_qs.filter(date__gte=current, date__lte=week_end)
            count = entries.count()
            if count > 0:
                total_hours = float(entries.aggregate(t=Sum("hours"))["t"] or Decimal("0"))
                statuses = list(entries.values_list("status", flat=True).distinct())
                employee_count = entries.values("employee").distinct().count()
                all_locked = all(s == "LOCKED" for s in statuses)
                has_locked = "LOCKED" in statuses

                weeks.append({
                    "week_start": current.isoformat(),
                    "week_end": week_end.isoformat(),
                    "entry_count": count,
                    "total_hours": round(total_hours, 1),
                    "employee_count": employee_count,
                    "statuses": statuses,
                    "status": "locked" if all_locked else "partial" if has_locked else "open",
                })
            current += timedelta(days=7)

        weeks.reverse()  # Most recent first
        return Response({"weeks": weeks})

    @action(detail=False, methods=["post"])
    def lock_before(self, request):
        """Lock all entries before a given date."""
        from datetime import date as date_type

        denied = self._require_lock_role()
        if denied:
            return denied

        before_date = request.data.get("before_date")
        if not before_date:
            return Response(
                {"error": {"code": "MISSING_DATE", "message": "before_date required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        bd = date_type.fromisoformat(before_date) if isinstance(before_date, str) else before_date

        from django.db import transaction

        from apps.core.models import Tenant
        from .models import PeriodFreeze

        tenant_id = getattr(request, "tenant_id", None)

        with transaction.atomic():
            # Lock existing entries
            qs = TimeEntry.objects.filter(date__lt=bd).exclude(status="LOCKED")
            if tenant_id:
                qs = qs.filter(tenant_id=tenant_id)
            count = qs.update(status="LOCKED")

            # Create or update freeze date (prevents new entries on empty dates)
            tenant = Tenant.objects.get(pk=tenant_id) if tenant_id else _get_tenant(self.request)
            existing_freeze = PeriodFreeze.objects.filter(tenant=tenant).order_by("-freeze_before").first()
            if not existing_freeze or bd > existing_freeze.freeze_before:
                PeriodFreeze.objects.create(
                    tenant=tenant,
                    freeze_before=bd,
                    frozen_by=request.user,
            )

        return Response({"locked_count": count, "before_date": bd.isoformat()})

    @action(detail=False, methods=["post"])
    def lock_period(self, request):
        """Lock all entries in a period — sets status to LOCKED."""
        from datetime import date as date_type

        denied = self._require_lock_role()
        if denied:
            return denied

        period_start = request.data.get("period_start")
        period_end = request.data.get("period_end")
        if not period_start or not period_end:
            return Response(
                {"error": {"code": "MISSING_DATES", "message": "period_start and period_end required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ps = date_type.fromisoformat(period_start) if isinstance(period_start, str) else period_start
        pe = date_type.fromisoformat(period_end) if isinstance(period_end, str) else period_end

        # Validate: must be Sunday to Saturday (full week)
        if ps.weekday() != 6:  # 6 = Sunday
            return Response(
                {"error": {"code": "INVALID_PERIOD", "message": "La date de debut doit etre un dimanche"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        from datetime import timedelta
        expected_end = ps + timedelta(days=6)
        if pe != expected_end:
            return Response(
                {"error": {"code": "INVALID_PERIOD", "message": f"La date de fin doit etre le samedi ({expected_end.isoformat()})"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = TimeEntry.objects.filter(
            date__gte=ps, date__lte=pe,
        ).exclude(status="LOCKED")
        tenant_id = getattr(request, "tenant_id", None)
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        count = qs.update(status="LOCKED")

        return Response({"locked_count": count, "period_start": ps.isoformat(), "period_end": pe.isoformat()})

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

        # Auto-update WeeklyApproval if ALL entries for each affected employee are now PM_APPROVED
        if count > 0:
            from datetime import timedelta
            affected_employees = set(
                TimeEntry.objects.filter(id__in=entry_ids).values_list("employee_id", flat=True)
            )
            for emp_id in affected_employees:
                emp_entries = TimeEntry.objects.filter(employee_id=emp_id)
                # Find week range from the approved entries
                dates = list(emp_entries.filter(id__in=entry_ids).values_list("date", flat=True))
                if dates:
                    ws = min(dates) - timedelta(days=min(dates).weekday())
                    we = ws + timedelta(days=6)
                    all_week = TimeEntry.objects.filter(employee_id=emp_id, date__gte=ws, date__lte=we)
                    still_pending = all_week.exclude(
                        status__in=["PM_APPROVED", "PAIE_VALIDATED", "FINANCE_APPROVED", "LOCKED"]
                    ).exists()
                    if not still_pending:
                        approval = WeeklyApproval.objects.filter(employee_id=emp_id, week_start=ws).first()
                        if approval and approval.pm_status != "APPROVED":
                            approval.pm_status = "APPROVED"
                            approval.pm_approved_by = request.user
                            approval.pm_approved_at = timezone.now()
                            approval.save()

        return Response({"approved_count": count})

    @action(detail=False, methods=["post"])
    def approve_all_my_entries(self, request):
        """PM approves ALL submitted entries on their projects for a given employee/week."""
        from apps.projects.models import Project

        employee_id = request.data.get("employee_id")
        week_start = request.data.get("week_start")
        if not employee_id or not week_start:
            return Response(
                {"error": {"code": "MISSING_PARAMS", "message": "employee_id and week_start required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from datetime import date as date_type, timedelta
        ws = date_type.fromisoformat(week_start) if isinstance(week_start, str) else week_start
        we = ws + timedelta(days=6)

        my_project_ids = set(
            Project.objects.filter(pm=request.user).values_list("id", flat=True)
        )

        entries = TimeEntry.objects.filter(
            employee_id=employee_id,
            date__gte=ws, date__lte=we,
            status="SUBMITTED",
            project_id__in=my_project_ids,
        )

        # Anti-self-approval
        if int(employee_id) == request.user.id:
            return Response(
                {"error": {"code": "SELF_APPROVAL", "message": "Cannot approve own entries"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        count = entries.update(status="PM_APPROVED")

        # Auto-update WeeklyApproval if ALL entries for this employee/week are now PM_APPROVED
        all_entries = TimeEntry.objects.filter(
            employee_id=employee_id, date__gte=ws, date__lte=we,
        )
        still_pending = all_entries.exclude(
            status__in=["PM_APPROVED", "PAIE_VALIDATED", "FINANCE_APPROVED", "LOCKED"]
        ).exists()
        if not still_pending:
            approval = WeeklyApproval.objects.filter(
                employee_id=employee_id, week_start=ws,
            ).first()
            if approval and approval.pm_status != "APPROVED":
                approval.pm_status = "APPROVED"
                approval.pm_approved_by = request.user
                approval.pm_approved_at = timezone.now()
                approval.save()

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

    @action(detail=False, methods=["post"])
    def bulk_correct(self, request):
        """FR25 — Finance corrects validated timesheets with audit trail.

        Allows Finance/Admin to modify hours on entries that are already
        PM_APPROVED, FINANCE_APPROVED, or PAIE_VALIDATED. Creates an audit
        record via HistoricalRecords (simple-history).
        """
        if not _has_lock_role(request.user):
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Finance/Admin role required"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        corrections = request.data.get("corrections", [])
        if not corrections:
            return Response(
                {"error": {"code": "NO_CORRECTIONS", "message": "corrections array required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        corrected = 0
        errors = []
        for corr in corrections:
            entry_id = corr.get("entry_id")
            new_hours = corr.get("hours")
            reason = corr.get("reason", "Correction Finance")
            if not entry_id or new_hours is None:
                errors.append({"entry_id": entry_id, "message": "entry_id and hours required"})
                continue
            try:
                entry = TimeEntry.objects.get(pk=entry_id)
                if entry.status == "DRAFT":
                    errors.append({"entry_id": entry_id, "message": "Cannot correct DRAFT entries"})
                    continue
                entry.hours = new_hours
                entry.notes = f"{entry.notes}\n[Correction: {reason}]".strip()
                entry.save()  # Triggers HistoricalRecords
                corrected += 1
            except TimeEntry.DoesNotExist:
                errors.append({"entry_id": entry_id, "message": "Entry not found"})

        return Response({
            "corrected_count": corrected,
            "errors": errors,
        })

    @action(detail=False, methods=["post"])
    def transfer_hours(self, request):
        """FR27d — Bulk transfer hours between projects/tasks.

        Finance can move hours from one project/task to another.
        Original entries are updated, audit trail via HistoricalRecords.
        """
        if not _has_lock_role(request.user):
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Finance/Admin role required"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        entry_ids = request.data.get("entry_ids", [])
        target_project = request.data.get("target_project")
        target_task = request.data.get("target_task")
        reason = request.data.get("reason", "Transfert d'heures")

        if not entry_ids or not target_project:
            return Response(
                {"error": {"code": "MISSING_FIELDS", "message": "entry_ids and target_project required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from apps.projects.models import Project, Task

        try:
            project = Project.objects.get(pk=target_project)
        except Project.DoesNotExist:
            return Response(
                {"error": {"code": "PROJECT_NOT_FOUND", "message": "Target project not found"}},
                status=status.HTTP_404_NOT_FOUND,
            )

        task = None
        if target_task:
            try:
                task = Task.objects.get(pk=target_task, project=project)
            except Task.DoesNotExist:
                return Response(
                    {"error": {"code": "TASK_NOT_FOUND", "message": "Target task not found"}},
                    status=status.HTTP_404_NOT_FOUND,
                )

        entries = TimeEntry.objects.filter(id__in=entry_ids)
        transferred = 0
        for entry in entries:
            old_info = f"{entry.project.code}/{entry.task.wbs_code if entry.task else 'N/A'}"
            entry.project = project
            entry.task = task
            if task:
                entry.phase = task.phase
            entry.notes = f"{entry.notes}\n[Transféré de {old_info}: {reason}]".strip()
            entry.save()  # HistoricalRecords audit
            transferred += 1

        return Response({
            "transferred_count": transferred,
            "target_project": project.code,
            "target_task": task.wbs_code if task else None,
        })


class WeeklyApprovalViewSet(viewsets.ModelViewSet):
    """Weekly approval tracking with two-level workflow."""

    serializer_class = WeeklyApprovalSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["employee", "week_start", "pm_status", "finance_status"]

    def get_queryset(self):
        qs = WeeklyApproval.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        # Restrict visibility: employees see only their own, PM/Finance/Paie/Admin see all
        from apps.core.models import ProjectRole, Role
        user_roles = set(
            ProjectRole.objects.filter(user=self.request.user).values_list("role", flat=True)
        )
        privileged_roles = {Role.ADMIN, Role.FINANCE, Role.PAIE, Role.PM, Role.PROJECT_DIRECTOR}
        if not user_roles & privileged_roles:
            qs = qs.filter(employee=self.request.user)
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
        """Finance second-level approval — requires PM approval first."""
        approval = self.get_object()
        if approval.pm_status != "APPROVED":
            return Response(
                {"error": {"code": "PM_NOT_APPROVED", "message": "L'approbation PM est requise avant l'approbation Finance", "details": []}},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        from datetime import timedelta

        reason = request.data.get("reason", "")
        approval.pm_status = "REJECTED"
        approval.save()

        # Revert associated time entries back to DRAFT for modification
        from .models import TimeEntry

        TimeEntry.objects.filter(
            employee=approval.employee,
            date__gte=approval.week_start,
            date__lt=approval.week_start + timedelta(days=7),
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

        # Find projects — PM sees their own, ADMIN/PAIE see all
        from apps.core.models import ProjectRole, Role
        user_roles = set(
            ProjectRole.objects.filter(user=request.user).values_list("role", flat=True)
        )
        if Role.ADMIN in user_roles or Role.PAIE in user_roles:
            my_projects = Project.objects.all()
        else:
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


    @action(detail=False, methods=["get"])
    def finance_dashboard(self, request):
        """Finance dashboard: all approvals where pm_status=APPROVED, finance_status=PENDING."""
        from datetime import timedelta
        from decimal import Decimal

        from django.contrib.auth import get_user_model
        from django.db.models import Sum

        User = get_user_model()

        # Determine week
        week_start_str = request.query_params.get("week_start")
        if week_start_str:
            from datetime import date as date_type
            week_start = date_type.fromisoformat(week_start_str)
        else:
            today = timezone.now().date()
            week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # All approvals for this week
        approvals = WeeklyApproval.objects.filter(week_start=week_start)
        employees_data = []

        for approval in approvals:
            emp = approval.employee
            emp_name = f"{emp.first_name} {emp.last_name}".strip() or emp.email

            # Total hours this week
            all_entries = TimeEntry.objects.filter(
                employee=emp, date__gte=week_start, date__lte=week_end,
            )
            total_week = float(all_entries.aggregate(t=Sum("hours"))["t"] or Decimal("0"))

            # PM approved hours
            pm_approved = float(all_entries.filter(status="PM_APPROVED").aggregate(
                t=Sum("hours"))["t"] or Decimal("0"))

            employees_data.append({
                "employee_id": emp.id,
                "employee_name": emp_name,
                "employee_initials": (emp.first_name[:1] + emp.last_name[:1]).upper() if emp.first_name and emp.last_name else emp_name[:2].upper(),
                "total_week_hours": round(total_week, 1),
                "pm_approved_hours": round(pm_approved, 1),
                "approval_id": approval.id,
                "pm_status": approval.pm_status,
                "finance_status": approval.finance_status,
            })

        pending_count = sum(1 for e in employees_data if e["pm_status"] == "APPROVED" and e["finance_status"] == "PENDING")

        return Response({
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "kpis": {
                "total_approvals": len(employees_data),
                "pending_finance": pending_count,
                "approved_finance": sum(1 for e in employees_data if e["finance_status"] == "APPROVED"),
                "rejected_finance": sum(1 for e in employees_data if e["finance_status"] == "REJECTED"),
            },
            "employees": employees_data,
        })


    @action(detail=False, methods=["get"])
    def paie_dashboard(self, request):
        """Paie dashboard: completeness check + validation status for all employees."""
        from datetime import timedelta
        from decimal import Decimal

        from django.contrib.auth import get_user_model
        from django.db.models import Sum

        User = get_user_model()

        week_start_str = request.query_params.get("week_start")
        if week_start_str:
            from datetime import date as date_type
            week_start = date_type.fromisoformat(week_start_str)
        else:
            today = timezone.now().date()
            week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # All active employees in the tenant
        from apps.core.models import UserTenantAssociation
        tenant_id = getattr(request, "tenant_id", None)
        if tenant_id:
            active_employee_ids = set(
                UserTenantAssociation.objects.filter(tenant_id=tenant_id)
                .values_list("user_id", flat=True)
            )
        else:
            # Fallback: all users who have entries in the past 4 weeks + all with tenant association
            four_weeks_ago = week_start - timedelta(weeks=4)
            active_employee_ids = set(
                TimeEntry.objects.filter(date__gte=four_weeks_ago)
                .values_list("employee_id", flat=True).distinct()
            )
            # Also include all users with any tenant association
            active_employee_ids |= set(
                UserTenantAssociation.objects.all().values_list("user_id", flat=True)
            )
        # Exclude the paie user themselves from the list
        active_employee_ids.discard(request.user.id)

        from .payroll_controls import run_controls

        employees_data = []
        total_alerts = {"error": 0, "warning": 0, "info": 0}

        for emp_id in active_employee_ids:
            emp = User.objects.get(pk=emp_id)
            emp_name = f"{emp.first_name} {emp.last_name}".strip() or emp.email

            week_entries_qs = TimeEntry.objects.filter(
                employee_id=emp_id, date__gte=week_start, date__lte=week_end,
            ).select_related("project")
            week_entries = list(week_entries_qs)
            total_hours = sum(float(e.hours) for e in week_entries)
            entry_count = len(week_entries)

            # Status breakdown
            statuses = [e.status for e in week_entries]
            all_pm_approved = entry_count > 0 and all(s in ("PM_APPROVED", "PAIE_VALIDATED", "LOCKED") for s in statuses)
            has_submitted = any(s != "DRAFT" for s in statuses)

            # WeeklyApproval
            approval = WeeklyApproval.objects.filter(
                employee_id=emp_id, week_start=week_start,
            ).first()

            # Run payroll controls
            all_entries_qs = TimeEntry.objects.filter(employee_id=emp_id)
            if entry_count == 0:
                # No entries at all — missing timesheet
                alerts = [{
                    "code": "MISSING_TIMESHEET",
                    "severity": "error",
                    "message": "Aucune feuille de temps soumise pour cette semaine",
                }]
            else:
                alerts = run_controls(emp, week_start, week_end, week_entries, all_entries_qs)

            # Severity: error > warning > info
            has_errors = any(a["severity"] == "error" for a in alerts)
            has_warnings = any(a["severity"] == "warning" for a in alerts)
            if has_errors:
                severity = "error"
            elif has_warnings:
                severity = "warning"
            elif alerts:
                severity = "info"
            else:
                severity = "ok"

            for a in alerts:
                total_alerts[a["severity"]] = total_alerts.get(a["severity"], 0) + 1

            employees_data.append({
                "employee_id": emp_id,
                "employee_name": emp_name,
                "employee_initials": (emp.first_name[:1] + emp.last_name[:1]).upper() if emp.first_name and emp.last_name else emp_name[:2].upper(),
                "total_week_hours": round(total_hours, 1),
                "entry_count": entry_count,
                "has_submitted": has_submitted,
                "all_pm_approved": all_pm_approved,
                "approval_id": approval.id if approval else None,
                "pm_status": approval.pm_status if approval else None,
                "paie_status": approval.paie_status if approval else "PENDING",
                "alerts": alerts,
                "severity": severity,
            })

        # Sort: errors first, then warnings, then ok
        severity_order = {"error": 0, "warning": 1, "info": 2, "ok": 3}
        employees_data.sort(key=lambda e: severity_order.get(e["severity"], 3))

        # KPIs
        submitted = sum(1 for e in employees_data if e["has_submitted"])
        pm_approved = sum(1 for e in employees_data if e["all_pm_approved"])
        validated = sum(1 for e in employees_data if e["paie_status"] == "APPROVED")
        missing = sum(1 for e in employees_data if not e["has_submitted"])
        clean = sum(1 for e in employees_data if e["severity"] == "ok")

        return Response({
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "kpis": {
                "total_employees": len(employees_data),
                "submitted": submitted,
                "pm_approved": pm_approved,
                "validated": validated,
                "missing": missing,
                "alerts_error": sum(1 for e in employees_data if e["severity"] == "error"),
                "alerts_warning": sum(1 for e in employees_data if e["severity"] == "warning"),
                "clean": clean,
            },
            "employees": employees_data,
        })

    @action(detail=True, methods=["post"])
    def validate_paie(self, request, pk=None):
        """Paie validates — all entries must be PM_APPROVED."""
        from datetime import timedelta

        approval = self.get_object()

        # Anti-self-approval
        if not cannot_approve_own(request.user, approval.employee_id):
            return Response(
                {"error": {"code": "SELF_APPROVAL", "message": "Cannot validate own timesheet"}},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Check all entries are PM_APPROVED
        week_end = approval.week_start + timedelta(days=6)
        entries = TimeEntry.objects.filter(
            employee=approval.employee,
            date__gte=approval.week_start,
            date__lte=week_end,
        )
        non_approved = entries.exclude(status__in=["PM_APPROVED", "PAIE_VALIDATED", "LOCKED"])
        if non_approved.exists():
            return Response(
                {"error": {"code": "NOT_ALL_PM_APPROVED", "message": "Toutes les heures doivent etre approuvees par les CP avant la validation paie."}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate (atomic)
        from django.db import transaction
        with transaction.atomic():
            entries.filter(status="PM_APPROVED").update(status="PAIE_VALIDATED")
            approval.paie_status = "APPROVED"
            approval.paie_validated_by = request.user
            approval.paie_validated_at = timezone.now()
            approval.save()
        return Response(WeeklyApprovalSerializer(approval).data)

    @action(detail=False, methods=["post"])
    def bulk_validate_paie(self, request):
        """Bulk paie validation for multiple approvals."""
        from datetime import timedelta

        approval_ids = request.data.get("approval_ids", [])
        if not approval_ids:
            return Response(
                {"error": {"code": "MISSING_IDS", "message": "approval_ids required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from django.db import transaction

        validated = 0
        skipped = []
        for aid in approval_ids:
            approval = WeeklyApproval.objects.filter(id=aid).first()
            if not approval:
                skipped.append({"id": aid, "reason": "Not found"})
                continue
            if approval.employee_id == request.user.id:
                skipped.append({"id": aid, "reason": "Self-approval"})
                continue

            week_end = approval.week_start + timedelta(days=6)
            entries = TimeEntry.objects.filter(
                employee=approval.employee,
                date__gte=approval.week_start,
                date__lte=week_end,
            )
            non_approved = entries.exclude(status__in=["PM_APPROVED", "PAIE_VALIDATED", "LOCKED"])
            if non_approved.exists():
                skipped.append({"id": aid, "reason": "Not all PM approved"})
                continue

            with transaction.atomic():
                entries.filter(status="PM_APPROVED").update(status="PAIE_VALIDATED")
                approval.paie_status = "APPROVED"
                approval.paie_validated_by = request.user
                approval.paie_validated_at = timezone.now()
                approval.save()
            validated += 1

        return Response({
            "validated_count": validated,
            "skipped_count": len(skipped),
            "skipped": skipped,
        })

    @action(detail=True, methods=["post"])
    def reject_paie(self, request, pk=None):
        """Paie rejects — reverts entries to PM_APPROVED."""
        from datetime import timedelta

        approval = self.get_object()
        if approval.paie_status != "APPROVED":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seules les feuilles validees paie peuvent etre rejetees."}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        week_end = approval.week_start + timedelta(days=6)
        TimeEntry.objects.filter(
            employee=approval.employee,
            date__gte=approval.week_start,
            date__lte=week_end,
            status="PAIE_VALIDATED",
        ).update(status="PM_APPROVED")

        approval.paie_status = "REJECTED"
        approval.paie_validated_by = None
        approval.paie_validated_at = None
        approval.save()
        return Response(WeeklyApprovalSerializer(approval).data)


class TimesheetLockViewSet(viewsets.ModelViewSet):
    """Phase and person-level locking. Write operations require ADMIN/FINANCE/PAIE."""

    serializer_class = TimesheetLockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TimesheetLock.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("project", "phase", "locked_by")

    def _require_lock_permission(self):
        tenant_id = getattr(self.request, "tenant_id", None)
        if not _has_lock_role(self.request.user, tenant_id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les rôles ADMIN, FINANCE ou PAIE peuvent gérer les verrouillages.")

    def perform_create(self, serializer):
        self._require_lock_permission()
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(
                tenant=Tenant.objects.get(pk=tenant_id),
                locked_by=self.request.user,
            )
        else:
            from apps.core.models import Tenant
            serializer.save(locked_by=self.request.user, tenant=_get_tenant(self.request))

    def destroy(self, request, *args, **kwargs):
        self._require_lock_permission()
        instance = self.get_object()
        instance.delete()
        return Response({"deleted": True}, status=status.HTTP_200_OK)


class PeriodUnlockViewSet(viewsets.ModelViewSet):
    """Temporary period unlocks for corrections. Write operations require ADMIN/FINANCE/PAIE."""

    serializer_class = PeriodUnlockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PeriodUnlock.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def _require_lock_permission(self):
        tenant_id = getattr(self.request, "tenant_id", None)
        if not _has_lock_role(self.request.user, tenant_id):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les rôles ADMIN, FINANCE ou PAIE peuvent gérer les déverrouillages.")

    def perform_create(self, serializer):
        self._require_lock_permission()
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(
                tenant=Tenant.objects.get(pk=tenant_id),
                unlocked_by=self.request.user,
            )
        else:
            from apps.core.models import Tenant

            serializer.save(unlocked_by=self.request.user, tenant=_get_tenant(self.request))

    def destroy(self, request, *args, **kwargs):
        """When revoking an unlock, re-lock entries in that period."""
        self._require_lock_permission()
        instance = self.get_object()
        # Re-lock entries that were unlocked (revert SUBMITTED/DRAFT back to LOCKED)
        entries = TimeEntry.objects.filter(
            date__gte=instance.period_start,
            date__lte=instance.period_end,
        ).exclude(status="LOCKED")
        tenant_id = getattr(request, "tenant_id", None)
        if tenant_id:
            entries = entries.filter(tenant_id=tenant_id)
        count = entries.update(status="LOCKED")
        instance.delete()
        return Response({"deleted": True, "relocked_count": count}, status=status.HTTP_200_OK)
