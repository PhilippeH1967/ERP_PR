"""
Planning & Resource Allocation models — Module L (Bloc 2).

Core entities for resource planning, capacity management, and milestones.
Gantt/dependencies and export features deferred to MVP-2.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import TenantScopedModel


class AllocationStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Terminée"
    CANCELLED = "CANCELLED", "Annulée"


class ResourceAllocation(TenantScopedModel):
    """Employee allocation to a project/phase for a given period."""

    class DistributionMode(models.TextChoices):
        UNIFORM = "uniform", "Uniforme"
        STANDARD = "standard", "Standard"
        MANUAL = "manual", "Manuelle"

    class TimeUnit(models.TextChoices):
        WEEK = "week", "Semaine"
        MONTH = "month", "Mois"

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resource_allocations",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="resource_allocations",
    )
    phase = models.ForeignKey(
        "projects.Phase",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="resource_allocations",
    )
    task = models.ForeignKey(
        "projects.Task",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="resource_allocations",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    hours_per_week = models.DecimalField(
        max_digits=5, decimal_places=1, default=40,
        help_text="Planned hours per week on this allocation (min 0.5)",
    )
    distribution_mode = models.CharField(
        max_length=10,
        choices=DistributionMode.choices,
        default=DistributionMode.UNIFORM,
    )
    time_unit = models.CharField(
        max_length=10,
        choices=TimeUnit.choices,
        default=TimeUnit.WEEK,
    )
    time_breakdown = models.JSONField(
        null=True, blank=True,
        help_text=(
            'For manual/standard modes: {"2026-W18": 20, ...} (week) '
            'or {"2026-05": 80, ...} (month)'
        ),
    )
    standard = models.ForeignKey(
        "planning.PlanningStandard",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="applied_allocations",
    )
    status = models.CharField(
        max_length=20,
        choices=AllocationStatus.choices,
        default=AllocationStatus.ACTIVE,
    )
    notes = models.TextField(blank=True, default="")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, related_name="+",
    )

    class Meta:
        db_table = "planning_allocation"
        ordering = ["start_date", "employee__username"]

    def clean(self):
        super().clean()
        has_phase = self.phase_id is not None
        has_task = self.task_id is not None
        if has_phase == has_task:
            raise ValidationError(
                "Allocation must target exactly one of phase or task (not both, not neither)."
            )

    def save(self, *args, **kwargs):
        # Clear stale breakdown when mode is not manual
        if self.distribution_mode != self.DistributionMode.MANUAL:
            self.time_breakdown = None
        # Enforce clean() on every persistence path (ORM, admin, shell)
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.username} → {self.project.code} ({self.hours_per_week}h/sem)"

    @property
    def total_weeks(self):
        if not self.start_date or not self.end_date:
            return 0
        delta = (self.end_date - self.start_date).days
        return max(1, round(delta / 7))

    @property
    def total_planned_hours(self):
        if self.distribution_mode == self.DistributionMode.MANUAL:
            if not self.time_breakdown:
                return 0.0
            try:
                return float(sum(float(v) for v in self.time_breakdown.values()))
            except (TypeError, ValueError):
                return 0.0
        # uniform or standard (Sprint 1: standard falls back to uniform)
        return float(self.hours_per_week) * self.total_weeks


class MilestoneStatus(models.TextChoices):
    UPCOMING = "UPCOMING", "À venir"
    ACHIEVED = "ACHIEVED", "Atteint"
    OVERDUE = "OVERDUE", "En retard"


class Milestone(TenantScopedModel):
    """Project milestone (jalon) for tracking key dates."""

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="milestones",
    )
    title = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=MilestoneStatus.choices,
        default=MilestoneStatus.UPCOMING,
    )
    color = models.CharField(
        max_length=7, default="#3B82F6",
        help_text="Hex color for visual display",
    )

    class Meta:
        db_table = "planning_milestone"
        ordering = ["date"]

    def __str__(self):
        return f"{self.project.code} — {self.title} ({self.date})"


class Availability(TenantScopedModel):
    """Daily availability for an employee (computed from contract - leaves)."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_records",
    )
    date = models.DateField(db_index=True)
    contractual_hours = models.DecimalField(
        max_digits=4, decimal_places=1, default=8,
    )
    capacity_hours = models.DecimalField(
        max_digits=4, decimal_places=1, default=8,
        help_text="Available hours after absence deductions",
    )
    is_working_day = models.BooleanField(default=True)
    leave_type = models.CharField(
        max_length=30, blank=True, default="",
        help_text="If absent: leave type code (VACANCES, MALADIE, etc.)",
    )

    class Meta:
        db_table = "planning_availability"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "date", "tenant"],
                name="uq_availability_employee_date",
            ),
        ]
        ordering = ["date"]

    def __str__(self):
        return f"{self.employee.username} {self.date} — {self.capacity_hours}h"


class DependencyType(models.TextChoices):
    FS = "FS", "Finish-to-Start"
    SS = "SS", "Start-to-Start"


class PhaseDependency(TenantScopedModel):
    """Dependency between two project phases for Gantt scheduling."""

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="phase_dependencies",
    )
    predecessor = models.ForeignKey(
        "projects.Phase",
        on_delete=models.CASCADE,
        related_name="successors",
    )
    successor = models.ForeignKey(
        "projects.Phase",
        on_delete=models.CASCADE,
        related_name="predecessors",
    )
    dependency_type = models.CharField(
        max_length=2,
        choices=DependencyType.choices,
        default=DependencyType.FS,
    )
    lag_days = models.IntegerField(
        default=0,
        help_text="Delay in days (can be negative)",
    )

    class Meta:
        db_table = "planning_phase_dependency"
        constraints = [
            models.UniqueConstraint(
                fields=["predecessor", "successor"],
                name="uq_phase_dependency",
            ),
        ]

    def __str__(self):
        return f"{self.predecessor.name} → {self.successor.name} ({self.dependency_type})"


class PlanningStandard(TenantScopedModel):
    """Reusable load curve template, bound to a phase code (e.g., ESQUISSE, APS)."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    phase_code = models.CharField(
        max_length=50, db_index=True,
        help_text="Matches projects.Phase.code (e.g., ESQUISSE, APS, DD, CHANTIER)",
    )
    time_unit = models.CharField(
        max_length=10,
        choices=ResourceAllocation.TimeUnit.choices,
        default=ResourceAllocation.TimeUnit.WEEK,
    )
    curve = models.JSONField(
        default=list,
        help_text=(
            "Normalized relative distribution: [0.4, 0.3, 0.2, 0.1] — "
            "sum must equal 1.0 ± 0.01"
        ),
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "planning_standard"
        ordering = ["phase_code", "name"]

    def __str__(self):
        return f"{self.name} [{self.phase_code}]"

    def clean(self):
        super().clean()
        if not isinstance(self.curve, list) or not self.curve:
            raise ValidationError("Curve must be a non-empty list of floats.")
        try:
            total = sum(float(v) for v in self.curve)
        except (TypeError, ValueError) as exc:
            raise ValidationError("All curve values must be numeric.") from exc
        if abs(total - 1.0) > 0.01:
            raise ValidationError(
                f"Curve values must sum to 1.0 ± 0.01, got {total:.3f}."
            )
