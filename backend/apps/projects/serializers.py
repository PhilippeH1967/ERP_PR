"""Project serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin
from apps.core.serializer_mixins import CostFieldFilterMixin

from .models import (
    Amendment,
    EmployeeAssignment,
    FinancialPhase,
    Phase,
    Project,
    ProjectTemplate,
    SupportService,
    WBSElement,
)


class PhaseSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = [
            "id", "code", "name", "client_facing_label", "phase_type",
            "billing_mode", "order", "start_date", "end_date",
            "is_mandatory", "is_locked", "budgeted_hours", "budgeted_cost",
        ]
        read_only_fields = ["id"]


class WBSElementSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = WBSElement
        fields = [
            "id", "parent", "phase", "standard_label", "client_facing_label",
            "element_type", "order", "budgeted_hours", "budgeted_cost",
            "contract_value", "is_billable", "children",
        ]
        read_only_fields = ["id"]

    def get_children(self, obj):
        children = obj.children.all()
        return WBSElementSerializer(children, many=True).data


class SupportServiceSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = SupportService
        fields = [
            "id", "code", "name", "client_facing_label",
            "budgeted_hours", "budgeted_cost", "billing_mode", "is_billable",
        ]
        read_only_fields = ["id"]


class ProjectSerializer(CostFieldFilterMixin, OptimisticLockMixin, serializers.ModelSerializer):
    phases = PhaseSerializer(many=True, read_only=True)
    support_services = SupportServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "code", "name", "client", "template", "contract_type",
            "status", "is_internal", "business_unit", "legal_entity",
            "start_date", "end_date", "construction_cost",
            "pm", "associate_in_charge", "invoice_approver", "bu_director",
            "version", "phases", "support_services",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True, default="")

    class Meta:
        model = Project
        fields = [
            "id", "code", "name", "client", "client_name",
            "contract_type", "status", "is_internal",
            "start_date", "end_date", "created_at",
        ]


class ProjectTemplateSerializer(serializers.ModelSerializer):
    projects_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = ProjectTemplate
        fields = [
            "id", "name", "code", "contract_type", "description",
            "is_active", "phases_config", "support_services_config",
            "projects_count",
        ]
        read_only_fields = ["id", "projects_count"]


class AmendmentSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = Amendment
        fields = [
            "id", "amendment_number", "description", "status",
            "budget_impact", "requested_by", "approved_by", "approval_date",
            "version", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class FinancialPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialPhase
        fields = [
            "id", "name", "code", "billing_mode",
            "fixed_amount", "hourly_budget_max",
        ]
        read_only_fields = ["id"]


class EmployeeAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAssignment
        fields = [
            "id", "employee", "project", "phase",
            "percentage", "start_date", "end_date",
        ]
        read_only_fields = ["id"]
