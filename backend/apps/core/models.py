"""
Core infrastructure models for ERP multi-tenancy, versioning, and audit.

All tenant-scoped models inherit TenantScopedModel for RLS isolation.
Financial models additionally inherit VersionedModel and add HistoricalRecords().
"""

from django.conf import settings
from django.db import models


class Tenant(models.Model):
    """Multi-tenant root model. Each tenant represents an isolated organization."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    sso_only = models.BooleanField(
        default=False,
        help_text="When True, only SSO login is allowed (except ADMIN users).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_tenant"

    def __str__(self):
        return self.name


class TimestampedModel(models.Model):
    """Abstract base providing created_at and updated_at timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TenantScopedModel(TimestampedModel):
    """
    Abstract base for all tenant-isolated models.

    Provides:
    - tenant FK (indexed for RLS policy performance)
    - created_at / updated_at timestamps

    PostgreSQL RLS policies filter on tenant_id = current_setting('app.current_tenant').
    Use `python manage.py setup_rls` to create policies after migrations.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",
        db_index=True,
    )

    class Meta:
        abstract = True


class VersionedModel(models.Model):
    """
    Abstract base providing optimistic locking via version field.

    Version auto-increments on every save (update only, not create).
    Use OptimisticLockMixin in serializers to enforce If-Match version checks.
    """

    version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk and not kwargs.pop("skip_version_increment", False):
            self.version = models.F("version") + 1
        super().save(*args, **kwargs)
        if self.pk:
            # Refresh from DB to get actual version value after F() expression
            self.refresh_from_db(fields=["version"])


# AuditMixin pattern:
# Models requiring audit trail add `history = HistoricalRecords()` field.
# django-simple-history automatically tracks history_user, history_date,
# history_change_reason on every save/delete.
#
# Example:
#   from simple_history.models import HistoricalRecords
#
#   class Invoice(TenantScopedModel, VersionedModel):
#       amount = models.DecimalField(max_digits=12, decimal_places=2)
#       history = HistoricalRecords()


class Role(models.TextChoices):
    """The 8 RBAC roles for per-project authorization."""

    EMPLOYEE = "EMPLOYEE", "Employee"
    PM = "PM", "Project Manager"
    PROJECT_DIRECTOR = "PROJECT_DIRECTOR", "Associé en charge"
    BU_DIRECTOR = "BU_DIRECTOR", "Directeur d'unité"
    FINANCE = "FINANCE", "Finance"
    DEPT_ASSISTANT = "DEPT_ASSISTANT", "Adjoint(e) de département"
    PROPOSAL_MANAGER = "PROPOSAL_MANAGER", "Gestionnaire de propositions"
    ADMIN = "ADMIN", "Administrateur"


class ProjectRole(TenantScopedModel):
    """
    Per-project role assignment. A user can have different roles on different projects.

    project_id is IntegerField (not FK) because Project model doesn't exist yet (Epic 3).
    Will be migrated to FK when apps.projects is created.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_roles",
    )
    project_id = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Null for global roles (ADMIN, FINANCE)",
    )
    role = models.CharField(max_length=30, choices=Role.choices)

    class Meta:
        db_table = "core_project_role"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project_id", "tenant"],
                name="uq_project_role_user_project_tenant",
            ),
        ]

    def __str__(self):
        project = f"project {self.project_id}" if self.project_id else "global"
        return f"{self.user} — {self.role} ({project})"


class UserTenantAssociation(models.Model):
    """Links a Django User to a Tenant. Created on first SSO login."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenant_association",
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="user_associations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_user_tenant"

    def __str__(self):
        return f"{self.user} → {self.tenant}"


class Delegation(TenantScopedModel):
    """
    Delegation of authority — allows one user to act on behalf of another.

    Scope can be a specific project or entire module ('all').
    Auto-expires when end_date passes.
    """

    delegator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="delegations_given",
    )
    delegate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="delegations_received",
    )
    scope = models.CharField(
        max_length=20,
        choices=[("project", "Projet spécifique"), ("all", "Tous les projets")],
        default="all",
    )
    project_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="Required when scope is 'project'",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "core_delegation"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.delegator} → {self.delegate} ({self.scope})"


class SampleTenantModel(TenantScopedModel, VersionedModel):
    """
    Concrete model for testing TenantScopedModel, VersionedModel, and RLS policies.
    TODO: Remove when real tenant-scoped models are created (Epic 2+).
    """

    name = models.CharField(max_length=255)

    class Meta:
        db_table = "core_sample"

    def __str__(self):
        return self.name
