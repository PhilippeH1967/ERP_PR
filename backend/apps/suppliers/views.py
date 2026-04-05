"""External organization and ST invoice API views."""

from django.db import models
from django.db.models import Sum
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    ExternalOrganization,
    STCreditNote,
    STDispute,
    STHoldback,
    STInvoice,
    STPayment,
)
from .serializers import (
    ExternalOrganizationSerializer,
    STCreditNoteSerializer,
    STDisputeSerializer,
    STHoldbackSerializer,
    STInvoiceSerializer,
    STPaymentSerializer,
)


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
        project = self.request.query_params.get("project")
        if project:
            qs = qs.filter(project_id=project)
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

    @action(detail=True, methods=["post"])
    def dispute(self, request, pk=None):
        """Flag ST invoice as disputed."""
        invoice = self.get_object()
        reason = request.data.get("reason", "")
        if not reason:
            return Response(
                {"error": {"code": "REASON_REQUIRED", "message": "Le motif est obligatoire."}},
                status=400,
            )
        invoice.status = "disputed"
        invoice.save(skip_version_increment=False)
        # Create dispute record
        tenant = _get_tenant_for_create(request)
        STDispute.objects.create(
            tenant=tenant,
            st_invoice=invoice,
            description=reason,
            status="open",
        )
        return Response(STInvoiceSerializer(invoice).data)

    @action(detail=False, methods=["post"])
    def batch_authorize(self, request):
        """FR47c — Batch authorize multiple ST invoices."""
        ids = request.data.get("invoice_ids", [])
        if not ids:
            return Response(
                {"error": {"code": "MISSING_IDS", "message": "invoice_ids required"}},
                status=400,
            )
        count = STInvoice.objects.filter(id__in=ids, status="received").update(status="authorized")
        return Response({"authorized_count": count})

    @action(detail=False, methods=["post"])
    def batch_pay(self, request):
        """Batch mark multiple ST invoices as paid."""
        ids = request.data.get("invoice_ids", [])
        if not ids:
            return Response({"error": {"code": "MISSING_IDS", "message": "invoice_ids required"}}, status=400)
        count = STInvoice.objects.filter(id__in=ids, status="authorized").update(status="paid")
        return Response({"paid_count": count})

    @action(detail=False, methods=["get"])
    def summary_by_supplier(self, request):
        """FR51 — Per-subcontractor cumulative view."""
        qs = self.get_queryset()
        data = qs.values("supplier__id", "supplier__name").annotate(
            total_amount=Sum("amount"),
            total_refacturable=Sum("budget_refacturable"),
            invoice_count=models.Count("id"),
        ).order_by("supplier__name")
        return Response(list(data))


def _get_tenant_for_create(request):
    from apps.core.models import Tenant
    tenant_id = getattr(request, "tenant_id", None)
    if tenant_id:
        return Tenant.objects.get(pk=tenant_id)
    return Tenant.objects.first()


class STPaymentViewSet(viewsets.ModelViewSet):
    """CRUD for ST partial payments."""

    serializer_class = STPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = STPayment.objects.select_related("invoice", "invoice__supplier").all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        invoice = self.request.query_params.get("invoice")
        if invoice:
            qs = qs.filter(invoice_id=invoice)
        return qs

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant_for_create(self.request))


class STCreditNoteViewSet(viewsets.ModelViewSet):
    """CRUD for ST credit notes."""

    serializer_class = STCreditNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = STCreditNote.objects.select_related("supplier", "invoice").all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant_for_create(self.request))


class STDisputeViewSet(viewsets.ModelViewSet):
    """CRUD for ST invoice disputes."""

    serializer_class = STDisputeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = STDispute.objects.select_related("st_invoice", "st_invoice__supplier").all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant_for_create(self.request))

    @action(detail=True, methods=["post"])
    def resolve(self, request, pk=None):
        """Resolve a dispute."""
        dispute = self.get_object()
        dispute.status = "resolved"
        dispute.save()
        return Response(STDisputeSerializer(dispute).data)


class STHoldbackViewSet(viewsets.ModelViewSet):
    """CRUD for ST holdback tracking."""

    serializer_class = STHoldbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = STHoldback.objects.select_related("project", "supplier").all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(tenant=_get_tenant_for_create(self.request))

    @action(detail=True, methods=["post"])
    def release(self, request, pk=None):
        """Release holdback (partially or fully)."""
        holdback = self.get_object()
        amount = request.data.get("amount")
        if not amount:
            return Response(
                {"error": {"code": "AMOUNT_REQUIRED", "message": "Montant à libérer requis"}},
                status=400,
            )
        amount = float(amount)
        if amount > float(holdback.remaining):
            return Response(
                {"error": {"code": "EXCEEDS_REMAINING", "message": f"Montant dépasse le solde ({holdback.remaining})"}},
                status=400,
            )
        holdback.released = float(holdback.released) + amount
        holdback.remaining = float(holdback.accumulated) - float(holdback.released)
        holdback.save()
        return Response(STHoldbackSerializer(holdback).data)
