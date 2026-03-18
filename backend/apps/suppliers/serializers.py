"""External organization serializers."""

from rest_framework import serializers

from .models import ExternalOrganization


class ExternalOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalOrganization
        fields = [
            "id", "name", "neq", "address", "city", "province",
            "postal_code", "country", "contact_name", "contact_email",
            "contact_phone", "type_tags", "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
