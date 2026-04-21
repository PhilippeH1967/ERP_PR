"""Project API views."""

from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Amendment,
    Phase,
    Project,
    ProjectTemplate,
    Task,
    WBSElement,
)
from .serializers import (
    AmendmentSerializer,
    PhaseSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    ProjectTemplateSerializer,
    TaskSerializer,
    WBSElementSerializer,
)
from .services import (
    AmendmentTransitionError,
    approve_amendment,
    create_project_from_template,
    reject_amendment,
    submit_amendment,
)


class ProjectTemplateViewSet(viewsets.ModelViewSet):
    """CRUD for project templates."""

    serializer_class = ProjectTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ProjectTemplate.objects.filter(is_active=True)
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.annotate(projects_count=Count("projects"))

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            # Fallback: use first tenant
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.first())

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Project.objects.filter(template=instance).exists():
            return Response(
                {
                    "error": {
                        "code": "TEMPLATE_IN_USE",
                        "message": "Ce template est utilisé par des projets et ne peut pas être supprimé.",
                        "details": [],
                    }
                },
                status=409,
            )
        return super().destroy(request, *args, **kwargs)


VALID_TRANSITIONS = {
    "ACTIVE": ["ON_HOLD", "COMPLETED", "CANCELLED"],
    "ON_HOLD": ["ACTIVE", "CANCELLED"],
    "COMPLETED": [],  # Cannot transition from COMPLETED
    "CANCELLED": [],  # Cannot transition from CANCELLED
}


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD for projects with search, filter, wizard support."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["code", "name"]
    filterset_fields = ["status", "contract_type", "is_internal", "client"]
    ordering_fields = ["code", "name", "created_at", "start_date"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Project.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)

        # BUG-008: EMPLOYEE role should only see projects they are assigned to
        from apps.core.models import ProjectRole, Role

        user_roles = set(
            ProjectRole.objects.filter(user=self.request.user).values_list("role", flat=True)
        )
        privileged = {
            Role.ADMIN,
            Role.FINANCE,
            Role.PM,
            Role.PROJECT_DIRECTOR,
            Role.BU_DIRECTOR,
            Role.DEPT_ASSISTANT,
            Role.PAIE,
        }
        if not user_roles & privileged:
            from apps.planning.models import ResourceAllocation

            assigned_project_ids = ResourceAllocation.objects.filter(
                employee=self.request.user
            ).values_list("project_id", flat=True)
            qs = qs.filter(id__in=assigned_project_ids)

        return qs.select_related("client", "pm", "consortium").prefetch_related(
            "phases", "tasks", "support_services"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["if_match_version"] = self.request.headers.get("If-Match")
        return ctx

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.first())

    def partial_update(self, request, *args, **kwargs):
        """Validate status transitions before updating."""
        new_status = request.data.get("status")
        if new_status:
            instance = self.get_object()
            current_status = instance.status
            if current_status != new_status:
                allowed = VALID_TRANSITIONS.get(current_status, [])
                if new_status not in allowed:
                    return Response(
                        {
                            "error": {
                                "code": "INVALID_STATUS_TRANSITION",
                                "message": (
                                    f"Transition de '{current_status}' vers '{new_status}' "
                                    f"non autorisée. Transitions valides: {', '.join(allowed) if allowed else 'aucune'}."
                                ),
                                "details": [],
                            }
                        },
                        status=400,
                    )
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def create_from_template(self, request):
        """Create project from template (Wizard Step 1)."""
        template_id = request.data.get("template_id")
        project_data = request.data.get("project", {})
        tenant_id = getattr(request, "tenant_id", None)

        if not template_id:
            err = {"code": "MISSING_TEMPLATE", "message": "template_id required", "details": []}
            return Response({"error": err}, status=400)

        try:
            project = create_project_from_template(template_id, project_data, tenant_id)
            return Response(ProjectSerializer(project).data, status=201)
        except ProjectTemplate.DoesNotExist:
            err = {"code": "TEMPLATE_NOT_FOUND", "message": "Template not found", "details": []}
            return Response({"error": err}, status=404)

    @action(detail=True, methods=["get"], url_path="budget-summary")
    def budget_summary(self, request, pk=None):
        """Original + current contract value with approved amendments breakdown.

        Returns the original contract value (``total_fees``), the current
        contract value (original + Σ approved amendment deltas) and the list
        of approved amendments contributing to the delta. Amendments in
        DRAFT/SUBMITTED/REJECTED are excluded from both the sum and breakdown.
        """
        from decimal import Decimal

        project = (
            self.get_queryset().with_current_contract_value().filter(pk=self.kwargs["pk"]).first()
        )
        if project is None:
            return Response(status=404)

        approved = (
            project.amendments.filter(status=Amendment.AmendmentStatus.APPROVED)
            .select_related("approved_by")
            .order_by("amendment_number")
        )

        original = project.total_fees or Decimal("0")
        current = project.current_contract_value or Decimal("0")
        total_impact = current - original

        return Response(
            {
                "project_id": project.pk,
                "original_contract_value": str(original),
                "current_contract_value": str(current),
                "total_approved_impact": str(total_impact),
                "amendments": [
                    {
                        "id": amd.pk,
                        "amendment_number": amd.amendment_number,
                        "description": amd.description,
                        "budget_impact": str(amd.budget_impact),
                        "status": amd.status,
                        "approval_date": (
                            amd.approval_date.isoformat() if amd.approval_date else None
                        ),
                        "approved_by_id": amd.approved_by_id,
                    }
                    for amd in approved
                ],
            }
        )

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        """Project health dashboard with real KPIs."""
        from decimal import Decimal

        from django.db.models import Sum

        project = self.get_object()

        # Hours consumed vs budgeted
        from apps.time_entries.models import TimeEntry

        hours_consumed = TimeEntry.objects.filter(project=project).aggregate(total=Sum("hours"))[
            "total"
        ] or Decimal("0")

        budget_hours = project.phases.aggregate(total=Sum("budgeted_hours"))["total"] or Decimal(
            "0"
        )

        utilization = float(hours_consumed / budget_hours * 100) if budget_hours > 0 else 0

        # Health indicator
        if utilization < 75:
            health = "green"
        elif utilization < 90:
            health = "yellow"
        else:
            health = "red"

        return Response(
            {
                "project_id": project.pk,
                "code": project.code,
                "name": project.name,
                "status": project.status,
                "hours_consumed": str(hours_consumed),
                "budget_hours": str(budget_hours),
                "budget_utilization_percent": round(utilization, 1),
                "health": health,
            }
        )

    @action(detail=True, methods=["get"], url_path="team_stats")
    def team_stats(self, request, pk=None):
        """Team statistics: monthly hours per employee + budget health per phase."""
        from datetime import timedelta
        from decimal import Decimal

        from django.db.models import Sum
        from django.db.models.functions import TruncMonth

        project = self.get_object()

        from apps.time_entries.models import TimeEntry
        from apps.planning.models import ResourceAllocation

        # Budget health per phase: which phases are over budget?
        phases_health = []
        for phase in project.phases.all():
            budget_h = float(
                phase.tasks.aggregate(s=Sum("budgeted_hours"))["s"] or phase.budgeted_hours or 0
            )
            actual_h = float(
                TimeEntry.objects.filter(phase=phase).aggregate(s=Sum("hours"))["s"] or 0
            )
            planned_h = sum(
                a.total_planned_hours for a in phase.resource_allocations.filter(status="ACTIVE")
            )
            over = actual_h > budget_h > 0
            phases_health.append(
                {
                    "phase_id": phase.id,
                    "phase_name": phase.name,
                    "budget_hours": budget_h,
                    "planned_hours": planned_h,
                    "actual_hours": actual_h,
                    "over_budget": over,
                }
            )

        over_count = sum(1 for p in phases_health if p["over_budget"])
        total_phases = len(phases_health)
        budget_status = "green"
        if over_count >= 3 or (total_phases > 0 and over_count / total_phases > 0.3):
            budget_status = "red"
        elif over_count > 0:
            budget_status = "orange"

        # Monthly hours per employee (last 6 months)
        from django.utils import timezone

        six_months_ago = (timezone.now() - timedelta(days=180)).date().replace(day=1)
        monthly = (
            TimeEntry.objects.filter(project=project, date__gte=six_months_ago)
            .annotate(month=TruncMonth("date"))
            .values(
                "employee__id",
                "employee__first_name",
                "employee__last_name",
                "employee__username",
                "month",
            )
            .annotate(total_hours=Sum("hours"))
            .order_by("employee__username", "month")
        )

        # Group by employee
        emp_monthly = {}
        for row in monthly:
            eid = row["employee__id"]
            if eid not in emp_monthly:
                name = f"{row['employee__first_name']} {row['employee__last_name']}".strip()
                emp_monthly[eid] = {
                    "employee_id": eid,
                    "employee_name": name or row["employee__username"],
                    "months": [],
                }
            emp_monthly[eid]["months"].append(
                {
                    "month": row["month"].strftime("%Y-%m"),
                    "hours": float(row["total_hours"]),
                }
            )

        # Planning status per employee
        emp_planning = {}
        for alloc in ResourceAllocation.objects.filter(project=project, status="ACTIVE"):
            eid = alloc.employee_id
            emp_planning[eid] = emp_planning.get(eid, 0) + alloc.total_planned_hours

        return Response(
            {
                "data": {
                    "budget_status": budget_status,
                    "over_budget_phases": over_count,
                    "total_phases": total_phases,
                    "phases_health": phases_health,
                    "employees_monthly": list(emp_monthly.values()),
                    "employees_planning": {str(k): v for k, v in emp_planning.items()},
                }
            }
        )


class PhaseViewSet(viewsets.ModelViewSet):
    """CRUD for project phases."""

    serializer_class = PhaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Phase.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(project=project, tenant=project.tenant)

    def perform_destroy(self, instance):
        if instance.is_mandatory:
            from rest_framework.exceptions import ValidationError

            raise ValidationError(
                {
                    "error": {
                        "code": "MANDATORY_PHASE",
                        "message": "Cette phase est obligatoire et ne peut pas être supprimée.",
                        "details": [],
                    }
                }
            )
        instance.delete()


class WBSElementViewSet(viewsets.ModelViewSet):
    """CRUD for WBS elements with hierarchy."""

    serializer_class = WBSElementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WBSElement.objects.filter(project_id=self.kwargs["project_pk"], parent__isnull=True)

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(project=project, tenant=project.tenant)


class AmendmentViewSet(viewsets.ModelViewSet):
    """CRUD for project amendments."""

    serializer_class = AmendmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Amendment.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        next_num = (project.amendments.count() or 0) + 1
        serializer.save(
            project=project,
            tenant=project.tenant,
            amendment_number=next_num,
            requested_by=self.request.user,
        )

    @action(detail=True, methods=["post"])
    def submit(self, request, project_pk=None, pk=None):
        """DRAFT → SUBMITTED. Any authenticated user."""
        amendment = self.get_object()
        try:
            submit_amendment(amendment, actor=request.user)
        except AmendmentTransitionError as exc:
            return Response(
                {
                    "error": {
                        "code": "INVALID_AMENDMENT_TRANSITION",
                        "message": str(exc),
                        "details": [],
                    }
                },
                status=400,
            )
        return Response(AmendmentSerializer(amendment).data, status=200)

    @action(detail=True, methods=["post"])
    def approve(self, request, project_pk=None, pk=None):
        """SUBMITTED → APPROVED. Only Associé en charge."""
        amendment = self.get_object()
        try:
            approve_amendment(amendment, actor=request.user)
        except PermissionError as exc:
            return Response(
                {
                    "error": {
                        "code": "FORBIDDEN_AMENDMENT_APPROVAL",
                        "message": str(exc),
                        "details": [],
                    }
                },
                status=403,
            )
        except AmendmentTransitionError as exc:
            return Response(
                {
                    "error": {
                        "code": "INVALID_AMENDMENT_TRANSITION",
                        "message": str(exc),
                        "details": [],
                    }
                },
                status=400,
            )
        return Response(AmendmentSerializer(amendment).data, status=200)

    @action(detail=True, methods=["get"])
    def scope(self, request, project_pk=None, pk=None):
        """Return phases and tasks attached to this amendment.

        Used by the UI to show the scope (periemetre) of an avenant so the PM
        can add phases/tasks directly from the amendment panel.
        """
        amendment = self.get_object()
        phases = amendment.phases.all().order_by("order", "name")
        tasks = amendment.tasks.select_related("phase").order_by("phase__order", "wbs_code")
        return Response(
            {
                "phases": PhaseSerializer(phases, many=True).data,
                "tasks": TaskSerializer(tasks, many=True).data,
            },
            status=200,
        )

    @action(detail=True, methods=["post"])
    def reject(self, request, project_pk=None, pk=None):
        """SUBMITTED → REJECTED. Only Associé en charge."""
        amendment = self.get_object()
        reason = request.data.get("reason", "") if hasattr(request, "data") else ""
        try:
            reject_amendment(amendment, actor=request.user, reason=reason)
        except PermissionError as exc:
            return Response(
                {
                    "error": {
                        "code": "FORBIDDEN_AMENDMENT_REJECTION",
                        "message": str(exc),
                        "details": [],
                    }
                },
                status=403,
            )
        except AmendmentTransitionError as exc:
            return Response(
                {
                    "error": {
                        "code": "INVALID_AMENDMENT_TRANSITION",
                        "message": str(exc),
                        "details": [],
                    }
                },
                status=400,
            )
        return Response(AmendmentSerializer(amendment).data, status=200)


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD for project tasks (WBS operational units)."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs["project_pk"]).select_related(
            "phase", "parent"
        )

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        # Auto-generate wbs_code if not provided
        wbs_code = serializer.validated_data.get("wbs_code")
        if not wbs_code:
            phase = serializer.validated_data.get("phase")
            phase_code = phase.code if phase and phase.code else str(phase.pk if phase else "0")
            existing_count = Task.objects.filter(project=project, phase=phase).count()
            wbs_code = f"{phase_code}.{existing_count + 1}"
            # Ensure uniqueness by incrementing if collision
            while Task.objects.filter(project=project, wbs_code=wbs_code).exists():
                existing_count += 1
                wbs_code = f"{phase_code}.{existing_count + 1}"
            serializer.validated_data["wbs_code"] = wbs_code
        serializer.save(project=project, tenant=project.tenant)
