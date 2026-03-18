"""Client API views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client, ClientAddress, Contact
from .serializers import (
    ClientAddressSerializer,
    ClientListSerializer,
    ClientSerializer,
    ContactSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):
    """CRUD for clients with tenant isolation."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "alias", "sector"]
    filterset_fields = ["status", "sector"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_queryset(self):
        qs = Client.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.prefetch_related("contacts", "addresses")

    def get_serializer_class(self):
        if self.action == "list":
            return ClientListSerializer
        return ClientSerializer

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

    @action(detail=True, methods=["get"])
    def financial_summary(self, request, pk=None):
        """Aggregated financial data for a client (Story 2.3)."""
        return Response(
            {
                "total_ca": "0.00",
                "invoices_outstanding": "0.00",
                "projects_count": 0,
            }
        )


class ContactViewSet(viewsets.ModelViewSet):
    """CRUD for client contacts."""

    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(client_id=self.kwargs["client_pk"])

    def perform_create(self, serializer):
        client = Client.objects.get(pk=self.kwargs["client_pk"])
        serializer.save(client=client, tenant=client.tenant)


class ClientAddressViewSet(viewsets.ModelViewSet):
    """CRUD for client addresses."""

    serializer_class = ClientAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ClientAddress.objects.filter(client_id=self.kwargs["client_pk"])

    def perform_create(self, serializer):
        client = Client.objects.get(pk=self.kwargs["client_pk"])
        serializer.save(client=client, tenant=client.tenant)
