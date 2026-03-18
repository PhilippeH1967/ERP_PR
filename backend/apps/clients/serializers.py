"""Client serializers for REST API."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import Client, ClientAddress, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id", "name", "role", "email", "phone",
            "language_preference", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        fields = [
            "id", "address_line_1", "address_line_2", "city",
            "province", "postal_code", "country", "is_billing", "is_primary",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ClientSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    addresses = ClientAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            "id", "name", "legal_entity", "alias", "sector", "status",
            "payment_terms_days", "default_invoice_template",
            "associe_en_charge", "notes", "version",
            "contacts", "addresses",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ClientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""

    class Meta:
        model = Client
        fields = ["id", "name", "alias", "sector", "status", "created_at"]
