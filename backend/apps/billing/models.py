"""Invoicing, payment, holdback, and billing dossier models."""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class InvoiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "Brouillon"
    SUBMITTED = "SUBMITTED", "Soumis"
    APPROVED = "APPROVED", "Approuvé"
    SENT = "SENT", "Envoyé"
    PAID = "PAID", "Payé"


class Invoice(TenantScopedModel, VersionedModel):
    """Client invoice with 7-column line items."""

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="invoices",
        null=True, blank=True,
    )
    client = models.ForeignKey(
        "clients.Client", on_delete=models.PROTECT, related_name="invoices"
    )
    invoice_number = models.CharField(
        max_length=50, db_index=True,
        help_text="PROV-xxxx provisional, definitive at send",
    )
    status = models.CharField(
        max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_tps = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_tvq = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="submitted_invoices",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="approved_invoices",
    )
    date_created = models.DateField(auto_now_add=True)
    date_sent = models.DateField(null=True, blank=True)
    date_paid = models.DateField(null=True, blank=True)
    template = models.ForeignKey(
        "InvoiceTemplate", on_delete=models.SET_NULL, null=True, blank=True
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "billing_invoice"
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.invoice_number} — {self.project.code if self.project else 'Libre'}"


class LineType(models.TextChoices):
    FORFAIT = "FORFAIT", "Forfait"
    HORAIRE = "HORAIRE", "Horaire"
    ST = "ST", "Sous-traitant"
    DEPENSE = "DEPENSE", "Dépense"
    AUTRE = "AUTRE", "Autre (libre)"


class InvoiceLine(TenantScopedModel):
    """7-column invoice line item."""

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    financial_phase = models.ForeignKey(
        "projects.FinancialPhase", on_delete=models.SET_NULL, null=True, blank=True
    )
    deliverable_name = models.CharField(max_length=255)
    line_type = models.CharField(
        max_length=10, choices=LineType.choices, default=LineType.FORFAIT
    )
    # 7-column structure
    total_contract_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoiced_to_date = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pct_billing_advancement = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pct_hours_advancement = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    amount_to_bill = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Editable — amount to bill this period (FR29)",
    )
    pct_after_billing = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "billing_invoice_line"
        ordering = ["order"]

    def __str__(self):
        return f"{self.deliverable_name} ({self.line_type})"


class CreditNote(TenantScopedModel, VersionedModel):
    """Credit note (avoir) — partial or full adjustment to invoice."""

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, null=True, blank=True,
        related_name="credit_notes",
    )
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    credit_note_number = models.CharField(max_length=50, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "billing_credit_note"

    def __str__(self):
        return f"{self.credit_note_number} — {self.amount}"


class Payment(TenantScopedModel, VersionedModel):
    """Payment received — can be partial, allocated across invoices."""

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    reference = models.CharField(max_length=100, blank=True, default="")
    method = models.CharField(max_length=50, blank=True, default="")

    history = HistoricalRecords()

    class Meta:
        db_table = "billing_payment"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Payment {self.amount} on {self.payment_date}"


class PaymentAllocation(TenantScopedModel):
    """Allocates a single payment across multiple invoices."""

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="allocations"
    )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payment_allocations"
    )
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "billing_payment_allocation"

    def __str__(self):
        return f"{self.allocated_amount} → {self.invoice.invoice_number}"


class Holdback(TenantScopedModel, VersionedModel):
    """Contractual retention (retenue) tracking."""

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="holdbacks"
    )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, null=True, blank=True,
        related_name="holdbacks",
    )
    percentage_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    accumulated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    released = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="accumulated - released",
    )
    release_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="active")

    history = HistoricalRecords()

    class Meta:
        db_table = "billing_holdback"

    def __str__(self):
        return f"Holdback {self.project.code} — {self.remaining}"


class WriteOff(TenantScopedModel, VersionedModel):
    """Invoice write-off (radiation)."""

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="write_offs"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, default="pending")

    history = HistoricalRecords()

    class Meta:
        db_table = "billing_write_off"

    def __str__(self):
        return f"WriteOff {self.amount} — {self.invoice.invoice_number}"


class InvoiceTemplate(TenantScopedModel):
    """Configurable invoice format template (10+ per client)."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    template_config = models.JSONField(
        default=dict,
        help_text="Template layout: sections, columns, footer, logo",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "billing_invoice_template"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ClientLabel(TenantScopedModel):
    """Maps WBS internal labels to client-specific labels for invoicing."""

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="client_labels"
    )
    wbs_code = models.CharField(max_length=50)
    client_label = models.CharField(max_length=255)

    class Meta:
        db_table = "billing_client_label"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "wbs_code"],
                name="uq_client_label_project_wbs",
            ),
        ]

    def __str__(self):
        return f"{self.wbs_code} → {self.client_label}"


class DunningLevel(TenantScopedModel):
    """Configurable dunning escalation levels."""

    level = models.PositiveIntegerField()
    days_overdue = models.PositiveIntegerField()
    email_template = models.TextField()

    class Meta:
        db_table = "billing_dunning_level"
        ordering = ["level"]

    def __str__(self):
        return f"Level {self.level} ({self.days_overdue}+ days)"


class DunningAction(TenantScopedModel):
    """Record of dunning communication sent."""

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="dunning_actions"
    )
    dunning_level = models.ForeignKey(DunningLevel, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "billing_dunning_action"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"Dunning L{self.dunning_level.level} — {self.invoice.invoice_number}"


class BillingDossier(TenantScopedModel):
    """Assembled billing package with annexes."""

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="dossiers"
    )
    annexes_config = models.JSONField(default=list)
    status = models.CharField(
        max_length=20,
        choices=[("generating", "En cours"), ("ready", "Prêt")],
        default="generating",
    )
    file_url = models.CharField(max_length=500, blank=True, default="")
    generated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "billing_dossier"

    def __str__(self):
        return f"Dossier {self.invoice.invoice_number} ({self.status})"
