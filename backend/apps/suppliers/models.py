"""External organizations shared registry."""

from django.db import models

from apps.core.models import TenantScopedModel


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

    def __str__(self):
        return self.name
