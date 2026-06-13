"""Time entry, approval, and locking models."""

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
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
        "projects.Phase", on_delete=models.CASCADE, null=True, blank=True,
        help_text="DEPRECATED — use task instead",
    )
    task = models.ForeignKey(
        "projects.Task", on_delete=models.CASCADE, null=True, blank=True,
        related_name="time_entries",
        help_text="Task (WBS) for this time entry — replaces phase",
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
            # Unicité au niveau TÂCHE (l'unité de saisie). Contrainte partielle :
            # ne s'applique qu'aux entrées rattachées à une tâche.
            models.UniqueConstraint(
                fields=["employee", "project", "task", "date"],
                condition=models.Q(task__isnull=False),
                name="uq_time_entry_employee_project_task_date",
            ),
        ]
        ordering = ["-date"]

    # Champs qui portent la valeur facturée : figés dès que is_invoiced=True.
    # Les transitions de statut (workflow paie/verrouillage) restent permises.
    INVOICED_PROTECTED_FIELDS = ("hours", "date", "project_id", "task_id", "employee_id")

    def _invoiced_protected_changes(self) -> list[str]:
        """Champs protégés modifiés alors que l'entrée est facturée en base."""
        old = (
            type(self)
            .objects.filter(pk=self.pk)
            .values("is_invoiced", *self.INVOICED_PROTECTED_FIELDS)
            .first()
        )
        if not old or not old["is_invoiced"]:
            return []
        changed = []
        for field in self.INVOICED_PROTECTED_FIELDS:
            new_val, old_val = getattr(self, field), old[field]
            if field == "hours":
                new_val = Decimal(str(new_val)) if new_val is not None else None
                old_val = Decimal(str(old_val)) if old_val is not None else None
            if new_val != old_val:
                changed.append(field)
        return changed

    def save(self, *args, **kwargs):
        # Heures facturées intouchables — garde au niveau modèle pour couvrir
        # TOUS les chemins d'écriture (vues, actions bulk, admin, shell). Le
        # flag is_invoiced lui-même est posé par billing (queryset.update).
        if self.pk and self._invoiced_protected_changes():
            raise ValidationError(
                "Ces heures ont été facturées au client : elles ne sont plus modifiables."
            )
        # La phase est dérivée de la tâche (champ déprécié, conservé pour les
        # rapports/exports). La saisie se fait au niveau tâche.
        if self.task_id:
            self.phase_id = self.task.phase_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} — {self.project} — {self.date} ({self.hours}h)"


@receiver(pre_delete, sender=TimeEntry, dispatch_uid="protect_invoiced_time_entries")
def protect_invoiced_time_entries(sender, instance, **kwargs):
    """Filet de sécurité : aucune suppression d'heures facturées, y compris en
    cascade (suppression d'une tâche ou d'un projet)."""
    if instance.is_invoiced:
        raise models.ProtectedError(
            "Ces heures ont été facturées au client : elles ne peuvent pas "
            "être supprimées.",
            {instance},
        )


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


class TimeEntryBlock(TenantScopedModel):
    """Blocage de saisie : empêche **un employé** d'imputer du temps sur une
    **tâche** (ou sur **toute une phase**). Additif — par défaut tout membre du
    projet peut saisir ; un blocage ferme la possibilité pour CET employé sur la
    cible. Distinct du verrouillage de période (``TimesheetLock``) et de la
    fermeture globale d'une tâche (``Task.is_active``)."""

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="time_entry_blocks"
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="time_entry_blocks",
    )
    phase = models.ForeignKey(
        "projects.Phase", on_delete=models.CASCADE, null=True, blank=True,
        related_name="time_entry_blocks",
    )
    task = models.ForeignKey(
        "projects.Task", on_delete=models.CASCADE, null=True, blank=True,
        related_name="time_entry_blocks",
    )
    reason = models.CharField(max_length=255, blank=True, default="")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="+",
    )

    class Meta:
        db_table = "time_entries_block"
        ordering = ["employee_id", "phase_id", "task_id"]
        constraints = [
            # Cible au plus une portée : tâche, phase, ou aucune (= projet
            # entier). Interdit seulement « phase ET tâche » simultanément.
            models.CheckConstraint(
                condition=~models.Q(phase__isnull=False, task__isnull=False),
                name="time_entry_block_phase_xor_task",
            ),
            models.UniqueConstraint(
                fields=["employee", "task"],
                condition=models.Q(task__isnull=False),
                name="uq_time_entry_block_employee_task",
            ),
            models.UniqueConstraint(
                fields=["employee", "phase"],
                condition=models.Q(phase__isnull=False),
                name="uq_time_entry_block_employee_phase",
            ),
            # Blocage niveau PROJET (ni phase ni tâche) : 1 par (employé, projet).
            models.UniqueConstraint(
                fields=["employee", "project"],
                condition=models.Q(phase__isnull=True, task__isnull=True),
                name="uq_time_entry_block_employee_project",
            ),
        ]

    def __str__(self):
        if self.task_id:
            target = f"task#{self.task_id}"
        elif self.phase_id:
            target = f"phase#{self.phase_id}"
        else:
            target = f"project#{self.project_id}"
        return f"block {self.employee_id} → {target}"

    @classmethod
    def blocks(cls, employee_id, task) -> bool:
        """True si ``employee_id`` est bloqué pour saisir sur ``task`` — via un
        blocage sur la tâche, sur sa phase, ou sur **tout le projet** (ni phase
        ni tâche)."""
        if task is None or employee_id is None:
            return False
        return (
            cls.objects.filter(employee_id=employee_id)
            .filter(
                models.Q(task_id=task.id)
                | models.Q(phase_id=task.phase_id)
                | models.Q(
                    task__isnull=True, phase__isnull=True, project_id=task.project_id
                )
            )
            .exists()
        )
