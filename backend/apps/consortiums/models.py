"""
Consortium models — FR59 (MVP-1.5).

A consortium groups multiple external organizations (firms) working together
on one or more projects for a shared client (donneur d'ouvrage).

Key rules:
  - Each member has a coefficient (%) — all coefficients MUST sum to 100%.
  - Provencher Roy can be mandataire (lead) or partenaire (partner).
  - Projects link to a consortium via Project.consortium FK.
  - Consortium client revenue is excluded from PR's CA (FR62, enforced later).
"""

from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class PRRole(models.TextChoices):
    MANDATAIRE = "MANDATAIRE", "Mandataire (responsable)"
    PARTENAIRE = "PARTENAIRE", "Partenaire"


class ConsortiumStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Actif"
    COMPLETED = "COMPLETED", "Terminé"
    CANCELLED = "CANCELLED", "Annulé"


class Consortium(TenantScopedModel, VersionedModel):
    """Consortium entity linking multiple firms on shared projects."""

    name = models.CharField(max_length=255)
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.PROTECT,
        related_name="consortiums",
        help_text="Donneur d'ouvrage — the end client",
    )
    pr_role = models.CharField(
        max_length=20,
        choices=PRRole.choices,
        default=PRRole.MANDATAIRE,
        help_text="Role of Provencher Roy in this consortium",
    )
    contract_reference = models.CharField(
        max_length=100, blank=True, default="",
        help_text="External contract or agreement reference number",
    )
    status = models.CharField(
        max_length=20,
        choices=ConsortiumStatus.choices,
        default=ConsortiumStatus.ACTIVE,
    )
    description = models.TextField(blank=True, default="")

    history = HistoricalRecords()

    class Meta:
        db_table = "consortiums_consortium"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_pr_role_display()})"

    @property
    def total_coefficient(self):
        """Sum of all member coefficients — should equal 100."""
        return self.members.aggregate(
            total=models.Sum("coefficient")
        )["total"] or 0


class ConsortiumMember(TenantScopedModel):
    """A firm participating in a consortium with a coefficient (%)."""

    consortium = models.ForeignKey(
        Consortium,
        on_delete=models.CASCADE,
        related_name="members",
    )
    organization = models.ForeignKey(
        "suppliers.ExternalOrganization",
        on_delete=models.PROTECT,
        related_name="consortium_memberships",
        null=True,
        blank=True,
        help_text="External organization (null = Provencher Roy itself)",
    )
    is_pr = models.BooleanField(
        default=False,
        help_text="True if this member row represents Provencher Roy",
    )
    name_override = models.CharField(
        max_length=255, blank=True, default="",
        help_text="Display name override (used when is_pr=True or for custom labels)",
    )
    coefficient = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Participation percentage (all members must sum to 100)",
    )
    contact_name = models.CharField(max_length=255, blank=True, default="")
    contact_email = models.EmailField(blank=True, default="")
    specialty = models.CharField(
        max_length=255, blank=True, default="",
        help_text="Firm specialty in this consortium (e.g., structure, MEP)",
    )

    class Meta:
        db_table = "consortiums_member"
        ordering = ["-is_pr", "-coefficient"]
        constraints = [
            models.UniqueConstraint(
                fields=["consortium", "organization"],
                name="uq_consortium_member_org",
                condition=models.Q(organization__isnull=False),
            ),
        ]

    def __str__(self):
        name = self.display_name
        return f"{name} — {self.coefficient}%"

    @property
    def display_name(self):
        if self.name_override:
            return self.name_override
        if self.is_pr:
            return "Provencher Roy"
        if self.organization:
            return self.organization.name
        return "—"
