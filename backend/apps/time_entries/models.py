"""Time entry, approval, and locking models."""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class TimeEntryStatus(models.TextChoices):
    DRAFT = "DRAFT", "Brouillon"
    SUBMITTED = "SUBMITTED", "Soumis"
    PM_APPROVED = "PM_APPROVED", "Approuvé PM"
    FINANCE_APPROVED = "FINANCE_APPROVED", "Approuvé Finance"
    PAIE_VALIDATED = "PAIE_VALIDATED", "Validé Paie"
    LOCKED = "LOCKED", "Verrouillé"


class TimeEntry(TenantScopedModel, VersionedModel):
    """Individual time entry — one cell in the weekly grid."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="time_entries"
    )
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="time_entries"
    )
    phase = models.ForeignKey(
        "projects.Phase", on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateField(db_index=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")
    rejection_reason = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=TimeEntryStatus.choices, default=TimeEntryStatus.DRAFT
    )
    is_favorite = models.BooleanField(default=False)
    is_invoiced = models.BooleanField(default=False)
    invoiced_on = models.ForeignKey(
        "billing.Invoice", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="invoiced_entries",
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "time_entries_entry"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "project", "phase", "date"],
                name="uq_time_entry_employee_project_phase_date",
            ),
        ]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee} — {self.project} — {self.date} ({self.hours}h)"


class ApprovalStatus(models.TextChoices):
    PENDING = "PENDING", "En attente"
    APPROVED = "APPROVED", "Approuvé"
    REJECTED = "REJECTED", "Rejeté"


class WeeklyApproval(TenantScopedModel):
    """Two-level approval tracking for a week of timesheets."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="weekly_approvals",
    )
    week_start = models.DateField(db_index=True)
    week_end = models.DateField()
    # Level 1: PM
    pm_status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    pm_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="pm_approvals",
    )
    pm_approved_at = models.DateTimeField(null=True, blank=True)
    # Level 2: Finance
    finance_status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    finance_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="finance_approvals",
    )
    finance_approved_at = models.DateTimeField(null=True, blank=True)
    # Level 3: Paie
    paie_status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    paie_validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="paie_validations",
    )
    paie_validated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "time_entries_weekly_approval"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "week_start", "tenant"],
                name="uq_weekly_approval_employee_week",
            ),
        ]
        ordering = ["-week_start"]

    def __str__(self):
        return f"{self.employee} — week {self.week_start}"


class TimesheetLock(TenantScopedModel):
    """Phase or person-level time entry blocking."""

    class LockType(models.TextChoices):
        PHASE = "PHASE", "Phase (all employees)"
        PERSON = "PERSON", "Person (specific employee)"

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="timesheet_locks"
    )
    phase = models.ForeignKey(
        "projects.Phase", on_delete=models.CASCADE, null=True, blank=True
    )
    person = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name="timesheet_locks",
    )
    lock_type = models.CharField(max_length=10, choices=LockType.choices)
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="locks_created",
    )
    locked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "time_entries_lock"

    def __str__(self):
        target = self.phase or self.person or "unknown"
        return f"Lock ({self.lock_type}) — {target}"


class PeriodUnlock(TenantScopedModel):
    """Temporary unlock of a locked period for corrections."""

    class UnlockReason(models.TextChoices):
        CORRECTION = "CORRECTION", "Correction"
        AMENDMENT = "AMENDMENT", "Avenant"
        AUDIT = "AUDIT", "Audit"

    period_start = models.DateField()
    period_end = models.DateField()
    reason = models.CharField(max_length=20, choices=UnlockReason.choices)
    justification = models.TextField(blank=True, default="")
    unlocked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="period_unlocks",
    )
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "time_entries_period_unlock"
        ordering = ["-unlocked_at"]

    def __str__(self):
        return f"Unlock {self.period_start}–{self.period_end} ({self.reason})"


class PeriodFreeze(TenantScopedModel):
    """Global freeze date — no entries allowed before this date."""

    freeze_before = models.DateField(
        help_text="No time entries can be created or modified before this date.",
    )
    frozen_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="period_freezes",
    )
    frozen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "time_entries_period_freeze"
        ordering = ["-frozen_at"]

    def __str__(self):
        return f"Freeze before {self.freeze_before}"
