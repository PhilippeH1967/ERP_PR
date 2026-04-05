"""Project API views."""

from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Amendment,
    EmployeeAssignment,
    Phase,
    Project,
    ProjectTemplate,
    Task,
    WBSElement,
)
from .serializers import (
    AmendmentSerializer,
    EmployeeAssignmentSerializer,
    PhaseSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    ProjectTemplateSerializer,
    TaskSerializer,
    WBSElementSerializer,
)
from .services import create_project_from_template


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
            Role.ADMIN, Role.FINANCE, Role.PM, Role.PROJECT_DIRECTOR,
            Role.BU_DIRECTOR, Role.DEPT_ASSISTANT, Role.PAIE,
        }
        if not user_roles & privileged:
            assigned_project_ids = EmployeeAssignment.objects.filter(
                employee=self.request.user
            ).values_list("project_id", flat=True)
            qs = qs.filter(id__in=assigned_project_ids)

        return qs.select_related("client").prefetch_related("phases", "support_services")

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

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        """Project health dashboard with real KPIs."""
        from decimal import Decimal

        from django.db.models import Sum

        project = self.get_object()

        # Hours consumed vs budgeted
        from apps.time_entries.models import TimeEntry

        hours_consumed = TimeEntry.objects.filter(
            project=project
        ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

        budget_hours = project.phases.aggregate(
            total=Sum("budgeted_hours")
        )["total"] or Decimal("0")

        utilization = (
            float(hours_consumed / budget_hours * 100) if budget_hours > 0 else 0
        )

        # Health indicator
        if utilization < 75:
            health = "green"
        elif utilization < 90:
            health = "yellow"
        else:
            health = "red"

        return Response({
            "project_id": project.pk,
            "code": project.code,
            "name": project.name,
            "status": project.status,
            "hours_consumed": str(hours_consumed),
            "budget_hours": str(budget_hours),
            "budget_utilization_percent": round(utilization, 1),
            "health": health,
        })


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
                {"error": {"code": "MANDATORY_PHASE", "message": "Cette phase est obligatoire et ne peut pas être supprimée.", "details": []}}
            )
        instance.delete()


class WBSElementViewSet(viewsets.ModelViewSet):
    """CRUD for WBS elements with hierarchy."""

    serializer_class = WBSElementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WBSElement.objects.filter(
            project_id=self.kwargs["project_pk"], parent__isnull=True
        )

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
            project=project, tenant=project.tenant,
            amendment_number=next_num, requested_by=self.request.user,
        )


class EmployeeAssignmentViewSet(viewsets.ModelViewSet):
    """CRUD for employee assignments to projects."""

    serializer_class = EmployeeAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmployeeAssignment.objects.filter(
            project_id=self.kwargs["project_pk"]
        ).select_related("employee", "phase")

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(project=project, tenant=project.tenant)


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD for project tasks (WBS operational units)."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            project_id=self.kwargs["project_pk"]
        ).select_related("phase", "parent")

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
