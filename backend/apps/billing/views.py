"""Billing API views."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from apps.core.models import ProjectRole, Role

# Billing roles
BILLING_VIEW_ROLES = {Role.ADMIN, Role.FINANCE, Role.PM, Role.PROJECT_DIRECTOR}
BILLING_WRITE_ROLES = {Role.ADMIN, Role.FINANCE}
BILLING_APPROVE_ROLES = {Role.ADMIN, Role.FINANCE, Role.PROJECT_DIRECTOR}
BILLING_SUBMIT_ROLES = {Role.ADMIN, Role.FINANCE, Role.PM}


def _user_roles(user):
    return set(ProjectRole.objects.filter(user=user).values_list("role", flat=True))


class CanViewBilling(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return bool(_user_roles(request.user) & BILLING_VIEW_ROLES)
        return bool(_user_roles(request.user) & BILLING_WRITE_ROLES)


class CanWriteBilling(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return bool(_user_roles(request.user) & BILLING_VIEW_ROLES)
        return bool(_user_roles(request.user) & BILLING_WRITE_ROLES)

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

    permission_classes = [CanViewBilling]
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

    @action(detail=False, methods=["post"], url_path="create_from_project")
    def create_from_project(self, request):
        """Create invoice with all billable phases pre-populated as lines."""
        from decimal import Decimal

        from django.db.models import Sum

        from apps.projects.models import Phase, Project

        project_id = request.data.get("project_id")
        if not project_id:
            return Response(
                {"error": {"code": "MISSING_FIELD", "message": "project_id est requis."}},
                status=400,
            )

        try:
            project = Project.objects.select_related("client").get(pk=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": {"code": "NOT_FOUND", "message": "Projet introuvable."}},
                status=404,
            )

        if not project.client:
            return Response(
                {"error": {"code": "NO_CLIENT", "message": "Ce projet n'a pas de client associé."}},
                status=400,
            )

        # Generate provisional invoice number
        import time

        invoice_number = f"PROV-{str(int(time.time()))[-6:]}"

        # Determine tenant
        tenant = None
        tenant_id = getattr(request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            tenant = Tenant.objects.get(pk=tenant_id)
        elif hasattr(project, "tenant"):
            tenant = project.tenant

        # Create draft invoice
        invoice = Invoice.objects.create(
            project=project,
            client=project.client,
            invoice_number=invoice_number,
            status="DRAFT",
            tenant=tenant,
        )

        # Create lines for each billable phase
        phases = Phase.objects.filter(
            project=project, budgeted_cost__gt=0
        ).order_by("order")

        for phase in phases:
            # Calculate invoiced_to_date: sum of amount_to_bill from previous
            # invoice lines linked to the same phase (via financial_phase or
            # matching deliverable_name on the same project)
            # Only count lines from SUBMITTED+ invoices (not DRAFT brouillons)
            invoiced_to_date = (
                InvoiceLine.objects.filter(
                    invoice__project=project,
                    invoice__status__in=["SUBMITTED", "APPROVED", "SENT", "PAID"],
                    deliverable_name=phase.client_facing_label or phase.name,
                )
                .aggregate(total=Sum("amount_to_bill"))["total"]
                or Decimal("0")
            )

            amount_to_bill = Decimal("0")

            # For HORAIRE phases, calculate from uninvoiced approved time entries
            if phase.billing_mode == "HORAIRE":
                from apps.time_entries.models import TimeEntry

                uninvoiced_entries = TimeEntry.objects.filter(
                    project=project,
                    phase=phase,
                    status="PM_APPROVED",
                    is_invoiced=False,
                )
                total_hours = uninvoiced_entries.aggregate(
                    h=Sum("hours")
                )["h"] or Decimal("0")
                hourly_rate = Decimal("85")  # default rate
                amount_to_bill = total_hours * hourly_rate

            InvoiceLine.objects.create(
                invoice=invoice,
                deliverable_name=phase.client_facing_label or phase.name,
                line_type=phase.billing_mode,  # FORFAIT or HORAIRE
                total_contract_amount=phase.budgeted_cost,
                invoiced_to_date=invoiced_to_date,
                amount_to_bill=amount_to_bill,
                order=phase.order,
                tenant=tenant,
            )

        # Create lines for refacturable ST invoices
        from apps.suppliers.models import STInvoice

        st_invoices = STInvoice.objects.filter(
            project=project,
            budget_refacturable__gt=0,
        ).select_related("supplier")

        max_order = phases.count()
        for idx, st_inv in enumerate(st_invoices, start=1):
            InvoiceLine.objects.create(
                invoice=invoice,
                deliverable_name=f"ST — {st_inv.supplier.name}",
                line_type="ST",
                total_contract_amount=st_inv.budget_refacturable,
                invoiced_to_date=Decimal("0"),
                amount_to_bill=st_inv.budget_refacturable,
                order=max_order + idx,
                tenant=tenant,
            )

        # Recalculate totals
        total = invoice.lines.aggregate(t=Sum("amount_to_bill"))["t"] or Decimal("0")
        Invoice.objects.filter(pk=invoice.pk).update(
            total_amount=total,
            tax_tps=round(total * Decimal("0.05"), 2),
            tax_tvq=round(total * Decimal("0.09975"), 2),
        )
        invoice.refresh_from_db()

        return Response(InvoiceSerializer(invoice).data, status=201)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Submit invoice for approval. Requires ADMIN/FINANCE/PM."""
        roles = _user_roles(request.user)
        if not roles & BILLING_SUBMIT_ROLES:
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Vous n'avez pas le droit de soumettre une facture."}},
                status=403,
            )
        invoice = self.get_object()
        if invoice.status != "DRAFT":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seule une facture brouillon peut être soumise."}},
                status=400,
            )
        # Assign definitive sequential invoice number on submission
        if invoice.invoice_number.startswith("PROV-"):
            from django.utils import timezone
            year = timezone.now().year
            # Global sequential number — ensures chronological audit trail
            last = Invoice.objects.filter(
                invoice_number__regex=r"^FAC-\d{4}-\d+$",
            ).exclude(status="DRAFT").order_by("-id").first()
            if last:
                try:
                    seq = int(last.invoice_number.split("-")[-1]) + 1
                except ValueError:
                    seq = 1
            else:
                seq = 1
            invoice.invoice_number = f"FAC-{year}-{seq:05d}"

        invoice.status = "SUBMITTED"
        invoice.submitted_by = request.user
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """Approve invoice. Requires ADMIN/FINANCE/PROJECT_DIRECTOR. Anti-self-approval."""
        roles = _user_roles(request.user)
        if not roles & BILLING_APPROVE_ROLES:
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Vous n'avez pas le droit d'approuver une facture."}},
                status=403,
            )
        invoice = self.get_object()
        if invoice.status != "SUBMITTED":
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "Seule une facture soumise peut être approuvée."}},
                status=400,
            )
        # Anti-self-approval
        if invoice.submitted_by_id == request.user.id:
            return Response(
                {"error": {"code": "SELF_APPROVAL", "message": "Vous ne pouvez pas approuver votre propre facture."}},
                status=403,
            )
        invoice.status = "APPROVED"
        invoice.approved_by = request.user
        invoice.save()
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        """Mark invoice as sent to client. Requires ADMIN/FINANCE."""
        roles = _user_roles(request.user)
        if not roles & BILLING_WRITE_ROLES:
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Vous n'avez pas le droit d'envoyer une facture."}},
                status=403,
            )
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
        """Mark invoice as paid. Requires ADMIN/FINANCE."""
        from django.utils import timezone

        roles = _user_roles(request.user)
        if not roles & BILLING_WRITE_ROLES:
            return Response(
                {"error": {"code": "FORBIDDEN", "message": "Vous n'avez pas le droit d'enregistrer un paiement."}},
                status=403,
            )
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

    @action(detail=True, methods=["post"])
    def mark_hours_invoiced(self, request, pk=None):
        """Mark time entries as invoiced for HORAIRE lines on SENT/PAID invoices."""
        invoice = self.get_object()
        if invoice.status not in ("SENT", "PAID"):
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "La facture doit être envoyée ou payée."}},
                status=400,
            )

        from apps.time_entries.models import TimeEntry

        total_marked = 0
        for line in invoice.lines.filter(line_type="HORAIRE"):
            entries = TimeEntry.objects.filter(
                project=invoice.project,
                phase__name=line.deliverable_name,
                status="PM_APPROVED",
                is_invoiced=False,
            ) | TimeEntry.objects.filter(
                project=invoice.project,
                phase__client_facing_label=line.deliverable_name,
                status="PM_APPROVED",
                is_invoiced=False,
            )
            count = entries.distinct().update(is_invoiced=True, invoiced_on=invoice)
            total_marked += count

        return Response({"marked_count": total_marked})

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
    permission_classes = [CanWriteBilling]

    def get_queryset(self):
        return InvoiceLine.objects.filter(invoice_id=self.kwargs["invoice_pk"]).select_related("invoice", "financial_phase")

    def _recalculate_invoice_totals(self, invoice):
        """Recalculate invoice totals from lines."""
        from decimal import Decimal
        from django.db.models import Sum
        total = invoice.lines.aggregate(t=Sum("amount_to_bill"))["t"] or Decimal("0")
        # Use update() to avoid VersionedModel/HistoricalRecords F() conflict
        Invoice.objects.filter(pk=invoice.pk).update(
            total_amount=total,
            tax_tps=round(total * Decimal("0.05"), 2),
            tax_tvq=round(total * Decimal("0.09975"), 2),
        )

    def perform_create(self, serializer):
        invoice = Invoice.objects.get(pk=self.kwargs["invoice_pk"])
        serializer.save(invoice=invoice, tenant=invoice.tenant)
        self._recalculate_invoice_totals(invoice)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._recalculate_invoice_totals(instance.invoice)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        invoice = instance.invoice
        instance.delete()
        self._recalculate_invoice_totals(invoice)
        return Response({"deleted": True}, status=200)


class CreditNoteViewSet(viewsets.ModelViewSet):
    serializer_class = CreditNoteSerializer
    permission_classes = [CanWriteBilling]
    filterset_fields = ["status", "project"]

    def get_queryset(self):
        qs = CreditNote.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [CanWriteBilling]

    def get_queryset(self):
        qs = Payment.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class HoldbackViewSet(viewsets.ModelViewSet):
    serializer_class = HoldbackSerializer
    permission_classes = [CanWriteBilling]

    def get_queryset(self):
        qs = Holdback.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class WriteOffViewSet(viewsets.ModelViewSet):
    serializer_class = WriteOffSerializer
    permission_classes = [CanWriteBilling]

    def get_queryset(self):
        qs = WriteOff.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class InvoiceTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceTemplateSerializer
    permission_classes = [CanWriteBilling]

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
    permission_classes = [CanWriteBilling]

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
