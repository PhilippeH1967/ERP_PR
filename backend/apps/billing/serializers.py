"""Billing serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import (
    BillingDossier,
    ClientLabel,
    CreditNote,
    DunningAction,
    DunningLevel,
    Holdback,
    Invoice,
    InvoiceLine,
    InvoiceTemplate,
    Payment,
    PaymentAllocation,
    WriteOff,
)


class InvoiceLineSerializer(serializers.ModelSerializer):
    project_id = serializers.SerializerMethodField()
    phase_name = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceLine
        fields = [
            "id", "financial_phase", "deliverable_name", "line_type",
            "total_contract_amount", "invoiced_to_date",
            "pct_billing_advancement", "pct_hours_advancement",
            "amount_to_bill", "pct_after_billing", "order",
            "project_id", "phase_name",
        ]
        read_only_fields = ["id", "project_id", "phase_name"]

    def get_project_id(self, obj):
        return obj.invoice.project_id if obj.invoice else None

    def get_phase_name(self, obj):
        if obj.financial_phase:
            return obj.financial_phase.name
        return ""

    def validate(self, data):
        amount_to_bill = data.get("amount_to_bill")
        if amount_to_bill is None and self.instance:
            amount_to_bill = self.instance.amount_to_bill
        if amount_to_bill is None:
            return data

        total_contract = data.get("total_contract_amount") or (self.instance.total_contract_amount if self.instance else 0)
        invoiced_to_date = data.get("invoiced_to_date") or (self.instance.invoiced_to_date if self.instance else 0)

        if float(amount_to_bill) < 0:
            raise serializers.ValidationError({
                "amount_to_bill": "Le montant à facturer ne peut pas être négatif."
            })

        # Warning: if amount exceeds contract, add a flag but don't block
        # Blocking is only if force_override is not set in context
        if float(total_contract) > 0:
            remaining = float(total_contract) - float(invoiced_to_date)
            if float(amount_to_bill) > remaining:
                request = self.context.get("request")
                force = request.data.get("force_override") if request else False
                if not force:
                    raise serializers.ValidationError({
                        "amount_to_bill": f"Le montant à facturer ({amount_to_bill}) dépasse le solde disponible ({remaining:.2f}). Confirmez pour continuer.",
                        "requires_confirmation": True,
                    })
        return data


class InvoiceSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id", "project", "client", "invoice_number", "status",
            "total_amount", "tax_tps", "tax_tvq",
            "submitted_by", "approved_by", "template",
            "date_created", "date_sent", "date_paid",
            "version", "lines", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "date_created", "created_at", "updated_at"]


class InvoiceListSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source="project.code", read_only=True)
    client_name = serializers.CharField(source="client.name", read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_number", "project", "project_code",
            "client", "client_name", "status", "total_amount",
            "date_created", "date_sent",
        ]


class CreditNoteSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = CreditNote
        fields = [
            "id", "invoice", "project", "credit_note_number",
            "amount", "reason", "status", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PaymentSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "invoice", "amount", "payment_date",
            "reference", "method", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PaymentAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAllocation
        fields = ["id", "payment", "invoice", "allocated_amount"]
        read_only_fields = ["id"]


class HoldbackSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = Holdback
        fields = [
            "id", "project", "invoice", "percentage_rate",
            "accumulated", "released", "remaining",
            "release_date", "status", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class WriteOffSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = WriteOff
        fields = [
            "id", "invoice", "amount", "reason", "status", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class InvoiceTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceTemplate
        fields = ["id", "name", "description", "template_config", "is_active"]
        read_only_fields = ["id"]


class ClientLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientLabel
        fields = ["id", "project", "wbs_code", "client_label"]
        read_only_fields = ["id"]


class DunningLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DunningLevel
        fields = ["id", "level", "days_overdue", "email_template"]
        read_only_fields = ["id"]


class DunningActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DunningAction
        fields = ["id", "invoice", "dunning_level", "sent_at"]
        read_only_fields = ["id", "sent_at"]


class BillingDossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingDossier
        fields = [
            "id", "invoice", "annexes_config", "status",
            "file_url", "generated_at",
        ]
        read_only_fields = ["id", "generated_at"]
