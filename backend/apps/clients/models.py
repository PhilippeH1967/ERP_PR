"""Client & Contact models for client management."""

from django.db import models
from simple_history.models import HistoricalRecords

from apps.core.models import TenantScopedModel, VersionedModel


class Client(TenantScopedModel, VersionedModel):
    """Client master record with 5-tab data structure."""

    name = models.CharField(max_length=255)
    legal_entity = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Legal form: Corporation, LLC, etc.",
    )
    alias = models.CharField(
        max_length=50,
        blank=True,
        default="",
        db_index=True,
        help_text="Unique searchable acronym",
    )
    sector = models.CharField(max_length=100, blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("inactive", "Inactive"), ("archived", "Archived")],
        default="active",
        db_index=True,
    )
    # Billing parameters
    payment_terms_days = models.PositiveIntegerField(default=30)
    default_invoice_template = models.CharField(max_length=100, blank=True, default="")
    # CRM
    associe_en_charge = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    history = HistoricalRecords()

    class Meta:
        db_table = "clients_client"
        constraints = [
            models.UniqueConstraint(
                fields=["alias", "tenant"],
                name="uq_clients_alias_tenant",
                condition=models.Q(alias__gt=""),
            ),
        ]
        ordering = ["name"]

    def __str__(self):
        return self.alias or self.name


class Contact(TenantScopedModel):
    """Client contact person."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    language_preference = models.CharField(
        max_length=2, choices=[("fr", "Français"), ("en", "English")], default="fr"
    )

    class Meta:
        db_table = "clients_contact"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.client})"


class ClientAddress(TenantScopedModel):
    """Client address (billing, shipping, etc.)."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="addresses")
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100, default="Québec")
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="Canada")
    is_billing = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "clients_address"

    def __str__(self):
        return f"{self.address_line_1}, {self.city}"
