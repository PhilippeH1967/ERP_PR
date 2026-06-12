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


def _norm_addr(value: str) -> str:
    """Normalise pour la comparaison anti-doublon : casse + espaces."""
    return "".join(str(value or "").lower().split())


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        fields = [
            "id", "address_line_1", "address_line_2", "city",
            "province", "postal_code", "country", "is_billing", "is_primary",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        """Anti-doublon : refuse une adresse identique (ligne 1 + ville +
        code postal, insensible à la casse et aux espaces) pour le même
        client. L'adresse en cours d'édition est exclue de la comparaison."""
        client_id = (
            self.instance.client_id
            if self.instance is not None
            else self.context.get("view").kwargs.get("client_pk")
            if self.context.get("view")
            else None
        )
        if client_id is None:
            return attrs

        def merged(field: str) -> str:
            if field in attrs:
                return attrs[field]
            return getattr(self.instance, field, "") if self.instance else ""

        key = (
            _norm_addr(merged("address_line_1")),
            _norm_addr(merged("city")),
            _norm_addr(merged("postal_code")),
        )
        qs = ClientAddress.objects.filter(client_id=client_id)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        for existing in qs:
            if key == (
                _norm_addr(existing.address_line_1),
                _norm_addr(existing.city),
                _norm_addr(existing.postal_code),
            ):
                raise serializers.ValidationError(
                    "Cette adresse existe déjà pour ce client."
                )
        return attrs


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
