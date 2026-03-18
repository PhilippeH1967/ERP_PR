"""
Project, Phase, WBS, Template, and related models.

This is the core domain of the ERP — all time, billing, and resource
modules reference these models.
"""

from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class ContractType(models.TextChoices):
    FORFAITAIRE = "FORFAITAIRE", "Forfaitaire"
    CONSORTIUM = "CONSORTIUM", "Consortium"
    CO_DEV = "CO_DEV", "Co-développement"
    CONCEPTION_CONSTRUCTION = "CONCEPTION_CONSTRUCTION", "Conception-construction"


class ProjectStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ON_HOLD = "ON_HOLD", "On Hold"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class BillingMode(models.TextChoices):
    FORFAIT = "FORFAIT", "Forfait (Fixed Price)"
    HORAIRE = "HORAIRE", "Horaire (Hourly)"


class ProjectTemplate(TenantScopedModel):
    """Pre-configured project template by contract type."""

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, default="")
    contract_type = models.CharField(max_length=30, choices=ContractType.choices)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    phases_config = models.JSONField(
        default=list,
        help_text="Pre-configured phases: [{name, client_label, type, billing_mode, is_mandatory}]",
    )
    support_services_config = models.JSONField(
        default=list,
        help_text="Pre-configured support services: [{name, client_label}]",
    )

    class Meta:
        db_table = "projects_template"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_contract_type_display()})"


class Project(TenantScopedModel, VersionedModel):
    """Main project entity — central to all ERP operations."""

    code = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=255)
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="projects",
        null=True,
        blank=True,
    )
    template = models.ForeignKey(
        ProjectTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
    )
    contract_type = models.CharField(
        max_length=30, choices=ContractType.choices, default=ContractType.FORFAITAIRE
    )
    status = models.CharField(
        max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE
    )
    is_internal = models.BooleanField(default=False)
    business_unit = models.CharField(max_length=100, blank=True, default="")
    legal_entity = models.CharField(max_length=100, blank=True, default="")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    construction_cost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Informational only — construction cost estimate",
    )
    # Leadership
    pm = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="managed_projects",
    )
    associate_in_charge = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="directed_projects",
    )
    invoice_approver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="approved_projects",
    )
    bu_director = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="bu_projects",
    )

    history = HistoricalRecords()

    class Meta:
        db_table = "projects_project"
        constraints = [
            models.UniqueConstraint(
                fields=["code", "tenant"],
                name="uq_projects_code_tenant",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} — {self.name}"


class Phase(TenantScopedModel):
    """Project phase — sequential realization or transversal support."""

    class PhaseType(models.TextChoices):
        REALIZATION = "REALIZATION", "Réalisation"
        SUPPORT = "SUPPORT", "Service de soutien"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="phases")
    code = models.CharField(max_length=50, blank=True, default="")
    name = models.CharField(max_length=255)
    client_facing_label = models.CharField(max_length=255, blank=True, default="")
    phase_type = models.CharField(
        max_length=20, choices=PhaseType.choices, default=PhaseType.REALIZATION
    )
    billing_mode = models.CharField(
        max_length=10, choices=BillingMode.choices, default=BillingMode.FORFAIT
    )
    order = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_mandatory = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    budgeted_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budgeted_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = "projects_phase"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.project.code} — {self.name}"


class WBSElement(TenantScopedModel):
    """Multi-level WBS with standard and client-facing labels."""

    class ElementType(models.TextChoices):
        PHASE = "PHASE", "Phase"
        TASK = "TASK", "Tâche"
        SUBTASK = "SUBTASK", "Sous-tâche"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="wbs_elements")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    phase = models.ForeignKey(
        Phase, on_delete=models.CASCADE, null=True, blank=True, related_name="wbs_elements"
    )
    standard_label = models.CharField(max_length=255)
    client_facing_label = models.CharField(max_length=255, blank=True, default="")
    element_type = models.CharField(
        max_length=10, choices=ElementType.choices, default=ElementType.TASK
    )
    order = models.PositiveIntegerField(default=0)
    budgeted_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budgeted_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    contract_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_billable = models.BooleanField(default=True)

    class Meta:
        db_table = "projects_wbs_element"
        ordering = ["order"]

    def __str__(self):
        return self.client_facing_label or self.standard_label


class SupportService(TenantScopedModel):
    """Transversal support service (BIM, Paysage, DD, etc.)."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="support_services")
    code = models.CharField(max_length=50, blank=True, default="")
    name = models.CharField(max_length=255)
    client_facing_label = models.CharField(max_length=255, blank=True, default="")
    budgeted_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budgeted_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    billing_mode = models.CharField(
        max_length=10, choices=BillingMode.choices, default=BillingMode.FORFAIT
    )
    is_billable = models.BooleanField(default=True)

    class Meta:
        db_table = "projects_support_service"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Amendment(TenantScopedModel, VersionedModel):
    """Contract amendment (avenant) with budget impact tracking."""

    class AmendmentStatus(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        SUBMITTED = "SUBMITTED", "Soumis"
        APPROVED = "APPROVED", "Approuvé"
        REJECTED = "REJECTED", "Rejeté"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="amendments")
    amendment_number = models.PositiveIntegerField()
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=AmendmentStatus.choices, default=AmendmentStatus.DRAFT
    )
    budget_impact = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Positive or negative impact on contract value",
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="requested_amendments",
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="approved_amendments",
    )
    approval_date = models.DateTimeField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        db_table = "projects_amendment"
        constraints = [
            models.UniqueConstraint(
                fields=["project", "amendment_number"],
                name="uq_amendment_project_number",
            ),
        ]
        ordering = ["amendment_number"]

    def __str__(self):
        return f"Avenant {self.amendment_number} — {self.project.code}"


class FinancialPhase(TenantScopedModel):
    """Financial layer grouping realization phases for billing."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="financial_phases")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, default="")
    billing_mode = models.CharField(
        max_length=10, choices=BillingMode.choices, default=BillingMode.FORFAIT
    )
    fixed_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    hourly_budget_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "projects_financial_phase"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} — {self.name}"


class EmployeeAssignment(TenantScopedModel):
    """Real employee assignment to project phase."""

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_assignments"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="assignments")
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "projects_employee_assignment"

    def __str__(self):
        return f"{self.employee} → {self.project.code} ({self.percentage}%)"
