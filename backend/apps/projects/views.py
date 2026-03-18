"""Project API views."""

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
    WBSElement,
)
from .serializers import (
    AmendmentSerializer,
    EmployeeAssignmentSerializer,
    PhaseSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    ProjectTemplateSerializer,
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
        return qs


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD for projects with search, filter, wizard support."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["code", "name"]
    filterset_fields = ["status", "contract_type", "is_internal"]
    ordering_fields = ["code", "name", "created_at", "start_date"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Project.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
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
            serializer.save()

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
        """Project health dashboard (Story 3.8)."""
        project = self.get_object()
        return Response({
            "project_id": project.pk,
            "code": project.code,
            "name": project.name,
            "status": project.status,
            "budget_utilization_percent": 0,
            "hours_vs_planned_percent": 0,
            "health": "green",
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
        return EmployeeAssignment.objects.filter(project_id=self.kwargs["project_pk"])

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        serializer.save(project=project, tenant=project.tenant)
