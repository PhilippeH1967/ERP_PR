"""Expense report, line, category, and approval models."""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class ExpenseCategory(TenantScopedModel):
    """Configurable expense categories."""

    name = models.CharField(max_length=255)
    is_refacturable_default = models.BooleanField(default=False)
    requires_receipt = models.BooleanField(default=True)
    gl_account = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        db_table = "expenses_category"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ExpenseStatus(models.TextChoices):
    SUBMITTED = "SUBMITTED", "Soumis"
    PM_APPROVED = "PM_APPROVED", "Approuvé PM"
    FINANCE_VALIDATED = "FINANCE_VALIDATED", "Validé Finance"
    PAID = "PAID", "Payé"
    REVERSED = "REVERSED", "Annulé"
    REJECTED = "REJECTED", "Rejeté"


class ExpenseReport(TenantScopedModel, VersionedModel):
    """Expense report with 4-role approval workflow."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_reports"
    )
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(
        max_length=20, choices=ExpenseStatus.choices, default=ExpenseStatus.SUBMITTED
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "expenses_report"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Expense {self.employee} — {self.total_amount}"


class ExpenseLine(TenantScopedModel):
    """Individual expense line item."""

    report = models.ForeignKey(ExpenseReport, on_delete=models.CASCADE, related_name="lines")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT)
    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, default="")
    receipt_path = models.CharField(max_length=500, blank=True, default="")
    is_refacturable = models.BooleanField(default=False)
    refacturable_markup_pct = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    tax_type = models.CharField(
        max_length=5,
        choices=[("HT", "Hors taxes"), ("TPS", "TPS"), ("TVQ", "TVQ")],
        default="HT",
    )

    class Meta:
        db_table = "expenses_line"
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.category} — {self.amount}"


class ExpenseApproval(TenantScopedModel):
    """4-role approval chain record."""

    report = models.ForeignKey(ExpenseReport, on_delete=models.CASCADE, related_name="approvals")
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    role_level = models.CharField(
        max_length=20,
        choices=[
            ("submitter", "Soumetteur"),
            ("manager", "Gestionnaire"),
            ("finance_analyst", "Analyste Finance"),
            ("finance", "Finance"),
        ],
    )
    status = models.CharField(
        max_length=10, choices=[("approved", "Approuvé"), ("rejected", "Rejeté")]
    )
    rejection_reason = models.TextField(blank=True, default="")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "expenses_approval"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.role_level} — {self.status}"
