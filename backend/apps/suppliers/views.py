"""External organization API views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ExternalOrganization
from .serializers import ExternalOrganizationSerializer


class ExternalOrganizationViewSet(viewsets.ModelViewSet):
    """CRUD for external organizations (shared registry)."""

    serializer_class = ExternalOrganizationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["name", "neq", "contact_name"]
    ordering = ["name"]

    def get_queryset(self):
        qs = ExternalOrganization.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            serializer.save()
