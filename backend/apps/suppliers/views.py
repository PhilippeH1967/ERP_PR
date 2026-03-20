"""External organization and ST invoice API views."""

from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ExternalOrganization, STInvoice
from .serializers import ExternalOrganizationSerializer, STInvoiceSerializer


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
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.first())

    @action(detail=False, methods=["post"])
    def check_duplicate(self, request):
        """Check for duplicate organizations by name or NEQ."""
        name = request.data.get("name", "").strip()
        neq = request.data.get("neq", "").strip()
        tenant_id = getattr(request, "tenant_id", None)

        duplicates = []
        qs = ExternalOrganization.objects.all()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)

        if neq:
            for org in qs.filter(neq__iexact=neq):
                duplicates.append({
                    "id": org.id, "name": org.name, "neq": org.neq,
                    "match_type": "neq_exact",
                })

        if name and len(name) >= 3:
            for org in qs.filter(name__icontains=name).exclude(
                id__in=[d["id"] for d in duplicates]
            )[:5]:
                duplicates.append({
                    "id": org.id, "name": org.name, "neq": org.neq,
                    "match_type": "name_similar",
                })

        return Response({"duplicates": duplicates})


class STInvoiceViewSet(viewsets.ModelViewSet):
    """CRUD for subcontractor invoices with workflow actions."""

    serializer_class = STInvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["invoice_number", "supplier__name", "project__code"]
    ordering = ["-invoice_date"]

    def get_queryset(self):
        qs = STInvoice.objects.select_related("supplier", "project").all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.first())

    @action(detail=True, methods=["post"])
    def authorize(self, request, pk=None):
        """PM authorizes ST invoice for payment."""
        invoice = self.get_object()
        if invoice.status != "received":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "La facture doit être au statut Reçu."}},
                status=400,
            )
        invoice.status = "authorized"
        invoice.save(skip_version_increment=False)
        return Response(STInvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        """Finance marks ST invoice as paid."""
        invoice = self.get_object()
        if invoice.status != "authorized":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "La facture doit être autorisée."}},
                status=400,
            )
        invoice.status = "paid"
        invoice.save(skip_version_increment=False)
        return Response(STInvoiceSerializer(invoice).data)
