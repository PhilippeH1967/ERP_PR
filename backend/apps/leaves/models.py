"""
Leave/Absence models — Module J (Bloc 2).

Workflow: Employee requests → PM/Director approves → PAIE validates
         → TimeEntry auto-created for approved leaves.

Integration:
  - Payroll controls check sick+overtime conflicts
  - Leave bank tracks accrued/used balance per employee per year
  - Approved leaves inject TimeEntry on internal absence project
"""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel


class LeaveType(TenantScopedModel):
    """Configurable leave types (vacation, sick, personal, etc.)."""

    code = models.CharField(max_length=30, db_index=True)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100, blank=True, default="")
    is_paid = models.BooleanField(default=True)
    requires_medical_cert = models.BooleanField(
        default=False,
        help_text="Requires medical certificate if absence > threshold days",
    )
    medical_cert_threshold_days = models.PositiveIntegerField(
        default=3,
        help_text="Number of consecutive days before medical cert required",
    )
    max_days_per_year = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        help_text="Maximum days per year (null = unlimited)",
    )
    accrual_rate_monthly = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Days accrued per month (0 = no accrual, allocated upfront)",
    )
    can_carry_over = models.BooleanField(
        default=False,
        help_text="Can unused days carry over to next year",
    )
    carry_over_max_days = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        help_text="Maximum days that can carry over",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "leaves_type"
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["code", "tenant"],
                name="uq_leave_type_code_tenant",
            ),
        ]

    def __str__(self):
        return f"{self.code} — {self.name}"


class LeaveBank(TenantScopedModel):
    """Yearly leave balance per employee per leave type."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leave_banks",
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name="banks",
    )
    year = models.PositiveIntegerField()
    accrued = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        help_text="Total days accrued for the year",
    )
    used = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        help_text="Total days used (approved leaves)",
    )
    carried_over = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        help_text="Days carried over from previous year",
    )
    manual_adjustment = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        help_text="Manual adjustment by HR (positive or negative)",
    )

    class Meta:
        db_table = "leaves_bank"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "leave_type", "year", "tenant"],
                name="uq_leave_bank_employee_type_year",
            ),
        ]
        ordering = ["-year", "leave_type__order"]

    def __str__(self):
        return f"{self.employee.username} — {self.leave_type.code} {self.year}"

    @property
    def balance(self):
        """Available days = accrued + carried_over + adjustment - used."""
        return float(self.accrued) + float(self.carried_over) + float(self.manual_adjustment) - float(self.used)


class RequestStatus(models.TextChoices):
    PENDING = "PENDING", "En attente"
    APPROVED = "APPROVED", "Approuvé"
    REJECTED = "REJECTED", "Rejeté"
    CANCELLED = "CANCELLED", "Annulé"


class LeaveRequest(TenantScopedModel):
    """Employee leave request with approval workflow."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leave_requests",
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.PROTECT,
        related_name="requests",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    hours_per_day = models.DecimalField(
        max_digits=4, decimal_places=2, default=8,
        help_text="Hours per day (7.5 or 8 typically)",
    )
    total_days = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Total leave days requested (can be 0.5 for half-day)",
    )
    reason = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING,
    )
    # Approval
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="approved_leaves",
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, default="")
    # Medical certificate
    medical_cert_uploaded = models.BooleanField(default=False)
    # Link to auto-created time entries
    time_entries_created = models.BooleanField(
        default=False,
        help_text="True if TimeEntry records were auto-created on approval",
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "leaves_request"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.employee.username} — {self.leave_type.code} {self.start_date} → {self.end_date}"

    @property
    def total_hours(self):
        return float(self.total_days) * float(self.hours_per_day)


class PublicHoliday(TenantScopedModel):
    """Statutory holidays by jurisdiction (linked to LaborRule)."""

    name = models.CharField(max_length=100)
    date = models.DateField(db_index=True)
    is_paid = models.BooleanField(default=True)
    labor_rule = models.ForeignKey(
        "core.LaborRule",
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="holidays",
        help_text="Jurisdiction this holiday applies to",
    )

    class Meta:
        db_table = "leaves_public_holiday"
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["date", "tenant"],
                name="uq_public_holiday_date_tenant",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.date})"
