"""Billing API views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    CreditNote,
    Holdback,
    Invoice,
    InvoiceLine,
    InvoiceTemplate,
    Payment,
    WriteOff,
)
from .serializers import (
    CreditNoteSerializer,
    HoldbackSerializer,
    InvoiceLineSerializer,
    InvoiceListSerializer,
    InvoiceSerializer,
    InvoiceTemplateSerializer,
    PaymentSerializer,
    WriteOffSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    """Full invoice CRUD with workflow actions."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["invoice_number", "project__code"]
    filterset_fields = ["status", "project", "client"]
    ordering = ["-date_created"]

    def get_queryset(self):
        qs = Invoice.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("project", "client").prefetch_related("lines")

    def get_serializer_class(self):
        if self.action == "list":
            return InvoiceListSerializer
        return InvoiceSerializer

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

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Submit invoice for approval."""
        invoice = self.get_object()
        invoice.status = "SUBMITTED"
        invoice.submitted_by = request.user
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Approve invoice."""
        invoice = self.get_object()
        invoice.status = "APPROVED"
        invoice.approved_by = request.user
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["get"])
    def aging_analysis(self, request, pk=None):
        """Invoice aging analysis for this invoice's client."""
        from apps.billing.services import get_aging_analysis

        invoice = self.get_object()
        tenant_id = getattr(request, "tenant_id", invoice.tenant_id)
        aging = get_aging_analysis(invoice.client_id, tenant_id)
        return Response(aging)


class InvoiceLineViewSet(viewsets.ModelViewSet):
    """CRUD for invoice line items (7-column)."""

    serializer_class = InvoiceLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvoiceLine.objects.filter(invoice_id=self.kwargs["invoice_pk"])

    def perform_create(self, serializer):
        invoice = Invoice.objects.get(pk=self.kwargs["invoice_pk"])
        serializer.save(invoice=invoice, tenant=invoice.tenant)


class CreditNoteViewSet(viewsets.ModelViewSet):
    serializer_class = CreditNoteSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "project"]

    def get_queryset(self):
        qs = CreditNote.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Payment.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class HoldbackViewSet(viewsets.ModelViewSet):
    serializer_class = HoldbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Holdback.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class WriteOffViewSet(viewsets.ModelViewSet):
    serializer_class = WriteOffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = WriteOff.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class InvoiceTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = InvoiceTemplate.objects.filter(is_active=True)
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs
