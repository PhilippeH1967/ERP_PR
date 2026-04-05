"""External organization and ST invoice serializers."""

from rest_framework import serializers

from .models import (
    ExternalOrganization,
    STCreditNote,
    STDispute,
    STHoldback,
    STInvoice,
    STPayment,
)


class ExternalOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalOrganization
        fields = [
            "id", "name", "neq", "address", "city", "province",
            "postal_code", "country", "contact_name", "contact_email",
            "contact_phone", "type_tags", "banking_info", "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class STPaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source="invoice.invoice_number", read_only=True)
    supplier_name = serializers.CharField(source="invoice.supplier.name", read_only=True)

    class Meta:
        model = STPayment
        fields = [
            "id", "invoice", "invoice_number", "supplier_name",
            "amount", "payment_date", "payment_method", "reference",
            "version", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class STCreditNoteSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)

    class Meta:
        model = STCreditNote
        fields = [
            "id", "supplier", "supplier_name", "invoice",
            "credit_number", "credit_date", "amount", "reason",
            "version", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class STDisputeSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source="st_invoice.invoice_number", read_only=True)
    supplier_name = serializers.CharField(source="st_invoice.supplier.name", read_only=True)

    class Meta:
        model = STDispute
        fields = [
            "id", "st_invoice", "invoice_number", "supplier_name",
            "description", "status", "expected_resolution",
            "version", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class STHoldbackSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    project_code = serializers.CharField(source="project.code", read_only=True)

    class Meta:
        model = STHoldback
        fields = [
            "id", "project", "project_code", "supplier", "supplier_name",
            "percentage_rate", "accumulated", "released", "remaining",
            "status", "version", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class STInvoiceSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    project_code = serializers.CharField(source="project.code", read_only=True)

    class Meta:
        model = STInvoice
        fields = [
            "id", "project", "project_code", "supplier", "supplier_name",
            "invoice_number", "invoice_date", "amount", "status", "source",
            "budget_internal", "budget_refacturable", "budget_absorbed",
            "version", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
