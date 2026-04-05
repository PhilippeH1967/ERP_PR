"""
Planning & Resource Allocation models — Module L (Bloc 2).

Core entities for resource planning, capacity management, and milestones.
Gantt/dependencies and export features deferred to MVP-2.
"""

from django.conf import settings
from django.db import models

from apps.core.models import TenantScopedModel


class AllocationStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    COMPLETED = "COMPLETED", "Terminée"
    CANCELLED = "CANCELLED", "Annulée"


class ResourceAllocation(TenantScopedModel):
    """Employee allocation to a project/phase for a given period."""

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
