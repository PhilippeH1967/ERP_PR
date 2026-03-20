"""External organizations, ST invoices, payments, disputes, holdbacks."""

from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class ExternalOrganization(TenantScopedModel):
    """
    Shared registry of external organizations.

    The same organization can have different roles across projects
    (subcontractor on one, consortium partner on another, competitor on a third).
    """

    name = models.CharField(max_length=255)
    neq = models.CharField(
        max_length=20,
        blank=True,
        default="",
        db_index=True,
        help_text="Numéro d'entreprise du Québec",
    )
    address = models.TextField(blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    province = models.CharField(max_length=100, default="Québec")
    postal_code = models.CharField(max_length=10, blank=True, default="")
    country = models.CharField(max_length=100, default="Canada")
    contact_name = models.CharField(max_length=255, blank=True, default="")
    contact_email = models.EmailField(blank=True, default="")
    contact_phone = models.CharField(max_length=30, blank=True, default="")
    banking_info = models.JSONField(default=dict, blank=True)
    type_tags = models.JSONField(
        default=list,
        blank=True,
        help_text='Role tags: ["st", "partner", "competitor"]',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "suppliers_external_org"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["neq", "tenant"],
                name="uq_supplier_neq_tenant",
                condition=models.Q(neq__gt=""),
            ),
        ]

    def __str__(self):
        return self.name


class STInvoice(TenantScopedModel, VersionedModel):
    """Subcontractor invoice."""

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="st_invoices"
    )
    supplier = models.ForeignKey(
        ExternalOrganization, on_delete=models.CASCADE, related_name="st_invoices"
    )
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(
        max_length=10,
        choices=[("manual", "Manual"), ("api", "API")],
        default="manual",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("received", "Reçu"), ("authorized", "Autorisé"),
            ("paid", "Payé"), ("disputed", "En litige"), ("credited", "Crédité"),
        ],
        default="received",
    )
    budget_internal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    budget_refacturable = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    budget_absorbed = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    history = HistoricalRecords()

    class Meta:
        db_table = "suppliers_st_invoice"
        ordering = ["-invoice_date"]

    def __str__(self):
        return f"ST {self.invoice_number} — {self.supplier.name}"


class STPayment(TenantScopedModel, VersionedModel):
    """Payment to subcontractor — can be partial."""

    st_invoice = models.ForeignKey(STInvoice, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, default="pending")

    history = HistoricalRecords()

    class Meta:
        db_table = "suppliers_st_payment"

    def __str__(self):
        return f"STPayment {self.amount} — {self.st_invoice}"


class STCreditNote(TenantScopedModel, VersionedModel):
    """Credit note from subcontractor."""

    st_invoice = models.ForeignKey(STInvoice, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(ExternalOrganization, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="draft")

    history = HistoricalRecords()

    class Meta:
        db_table = "suppliers_st_credit_note"

    def __str__(self):
        return f"STCredit {self.amount}"


class STDispute(TenantScopedModel, VersionedModel):
    """Dispute on a subcontractor invoice."""

    st_invoice = models.ForeignKey(STInvoice, on_delete=models.CASCADE, related_name="disputes")
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("open", "Ouvert"), ("resolved", "Résolu"), ("escalated", "Escaladé")],
        default="open",
    )
    expected_resolution = models.DateField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "suppliers_st_dispute"

    def __str__(self):
        return f"Dispute {self.st_invoice} — {self.status}"


class STHoldback(TenantScopedModel, VersionedModel):
    """Holdback tracking for subcontractor."""

    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    supplier = models.ForeignKey(ExternalOrganization, on_delete=models.CASCADE)
    percentage_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    accumulated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    released = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="active")

    history = HistoricalRecords()

    class Meta:
        db_table = "suppliers_st_holdback"

    def __str__(self):
        return f"STHoldback {self.supplier.name} — {self.remaining}"
