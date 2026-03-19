"""Billing API views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    CreditNote,
    DunningLevel,
    Holdback,
    Invoice,
    InvoiceLine,
    InvoiceTemplate,
    Payment,
    WriteOff,
)
from .serializers import (
    CreditNoteSerializer,
    DunningLevelSerializer,
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

    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        """Mark invoice as sent to client."""
        from django.utils import timezone

        invoice = self.get_object()
        if invoice.status != "APPROVED":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "La facture doit être approuvée."}},
                status=400,
            )
        invoice.status = "SENT"
        invoice.date_sent = timezone.now().date()
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        """Mark invoice as paid."""
        from django.utils import timezone

        invoice = self.get_object()
        if invoice.status != "SENT":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "La facture doit être envoyée."}},
                status=400,
            )
        invoice.status = "PAID"
        invoice.date_paid = timezone.now().date()
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["get"], url_path="print")
    def print_view(self, request, pk=None):
        """Print-ready HTML view for invoice brouillon / dossier."""
        from django.http import HttpResponse

        invoice = self.get_object()
        lines = invoice.lines.all()

        rows_html = ""
        for line in lines:
            rows_html += f"""
            <tr>
                <td>{line.deliverable_name}</td>
                <td class="right mono">{line.total_contract_amount:,.2f} $</td>
                <td class="right mono">{line.invoiced_to_date:,.2f} $</td>
                <td class="right mono">{line.pct_billing_advancement}%</td>
                <td class="right mono">{line.amount_to_bill:,.2f} $</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Facture {invoice.invoice_number}</title>
<style>
  body {{ font-family: -apple-system, sans-serif; font-size: 12px; color: #1F2937; margin: 40px; }}
  h1 {{ font-size: 20px; color: #2563EB; margin-bottom: 4px; }}
  .meta {{ color: #6B7280; font-size: 11px; margin-bottom: 20px; }}
  .amounts {{ display: flex; gap: 30px; margin-bottom: 20px; padding: 12px; background: #F9FAFB; border-radius: 6px; }}
  .amounts div {{ text-align: center; }}
  .amounts .val {{ font-size: 18px; font-weight: 700; font-family: monospace; }}
  .amounts .lbl {{ font-size: 10px; color: #6B7280; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
  th {{ background: #F3F4F6; padding: 8px; text-align: left; font-size: 10px; text-transform: uppercase; color: #6B7280; border-bottom: 2px solid #E5E7EB; }}
  td {{ padding: 8px; border-bottom: 1px solid #E5E7EB; }}
  .right {{ text-align: right; }}
  .mono {{ font-family: monospace; }}
  .footer {{ margin-top: 30px; padding-top: 12px; border-top: 1px solid #E5E7EB; font-size: 10px; color: #9CA3AF; }}
  @media print {{ body {{ margin: 20px; }} }}
</style>
</head>
<body>
  <h1>PR | ERP — Facture {invoice.invoice_number}</h1>
  <div class="meta">
    Projet: {invoice.project.code if invoice.project else '—'} — {invoice.project.name if invoice.project else '—'}<br>
    Client: {invoice.client.name if invoice.client else '—'}<br>
    Date: {invoice.date_created}<br>
    Statut: {invoice.status}
  </div>

  <div class="amounts">
    <div><div class="val">{invoice.total_amount:,.2f} $</div><div class="lbl">Montant HT</div></div>
    <div><div class="val">{invoice.tax_tps:,.2f} $</div><div class="lbl">TPS (5%)</div></div>
    <div><div class="val">{invoice.tax_tvq:,.2f} $</div><div class="lbl">TVQ (9.975%)</div></div>
  </div>

  <table>
    <thead><tr><th>Livrable</th><th class="right">Contrat</th><th class="right">Facturé</th><th class="right">% Fact.</th><th class="right">À facturer</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table>

  <div class="footer">
    Provencher Roy — Document généré le {timezone.now().strftime('%Y-%m-%d %H:%M')}<br>
    Coordonnées bancaires : Institution 815 — Transit 30000 — Compte 1234567
  </div>
</body>
</html>"""
        return HttpResponse(html, content_type="text/html")

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

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.first())


class DunningLevelViewSet(viewsets.ModelViewSet):
    """CRUD for dunning escalation levels."""

    serializer_class = DunningLevelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = DunningLevel.objects.all()
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
