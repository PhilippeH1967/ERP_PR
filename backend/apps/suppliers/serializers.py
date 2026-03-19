"""External organization and ST invoice serializers."""

from rest_framework import serializers

from .models import ExternalOrganization, STInvoice


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


class STInvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    project_code = serializers.CharField(source="project.code", read_only=True)

    class Meta:
        model = STInvoice
        fields = [
            "id", "project", "project_code", "supplier", "supplier_name",
            "invoice_number", "invoice_date", "amount", "status", "source",
            "version", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
