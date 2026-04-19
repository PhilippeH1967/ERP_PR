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
    Task,
    WBSElement,
)


class PhaseSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    tasks_budgeted_hours = serializers.SerializerMethodField()
    planned_hours = serializers.SerializerMethodField()
    actual_hours = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = [
            "id", "code", "name", "client_facing_label", "phase_type",
            "billing_mode", "order", "start_date", "end_date",
            "is_mandatory", "is_locked", "budgeted_hours", "budgeted_cost",
            "tasks_budgeted_hours", "planned_hours", "actual_hours",
        ]
        read_only_fields = ["id"]

    def get_tasks_budgeted_hours(self, obj):
        """Sum of budgeted_hours from all tasks in this phase."""
        from django.db.models import Sum
        total = obj.tasks.aggregate(s=Sum("budgeted_hours"))["s"]
        return float(total) if total else 0

    def get_planned_hours(self, obj):
        """Sum of planned hours from ResourceAllocations for this phase."""
        total = 0
        for alloc in obj.resource_allocations.filter(status="ACTIVE"):
            total += alloc.total_planned_hours
        return total

    def get_actual_hours(self, obj):
        """Sum of actual hours from TimeEntries for this phase."""
        from django.db.models import Sum
        from apps.time_entries.models import TimeEntry
        total = TimeEntry.objects.filter(phase=obj).aggregate(s=Sum("hours"))["s"]
        return float(total) if total else 0


class TaskSerializer(serializers.ModelSerializer):
    phase_name = serializers.CharField(source="phase.name", read_only=True)
    display_label = serializers.SerializerMethodField()
    planned_hours = serializers.SerializerMethodField()
    actual_hours = serializers.SerializerMethodField()
    wbs_code = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")

    class Meta:
        model = Task
        fields = [
            "id", "project", "phase", "phase_name", "parent",
            "wbs_code", "name", "client_facing_label", "display_label",
            "task_type", "billing_mode", "order",
            "start_date", "end_date",
            "budgeted_hours", "budgeted_cost", "hourly_rate",
            "is_billable", "is_active", "progress_pct",
            "planned_hours", "actual_hours",
        ]
        read_only_fields = ["id", "display_label", "phase_name", "planned_hours", "actual_hours"]

    def get_display_label(self, obj):
        return obj.client_facing_label or obj.name

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "end_date must be on or after start_date."}
            )
        return attrs

    def get_planned_hours(self, obj):
        """Sum of planned hours from ResourceAllocations for this task."""
        total = 0
        for alloc in obj.resource_allocations.filter(status="ACTIVE"):
            total += alloc.total_planned_hours
        return total

    def get_actual_hours(self, obj):
        """Sum of actual hours from TimeEntries for this task."""
        from django.db.models import Sum
        from apps.time_entries.models import TimeEntry
        total = TimeEntry.objects.filter(task=obj).aggregate(s=Sum("hours"))["s"]
        return float(total) if total else 0


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
    client_name = serializers.CharField(source="client.name", read_only=True, default="")
    consortium_name = serializers.CharField(source="consortium.name", read_only=True, default="")

    class Meta:
        model = Project
        fields = [
            "id", "code", "name", "client", "client_name", "template", "contract_type",
            "status", "is_internal", "is_public", "is_consortium", "consortium", "consortium_name",
            "services_transversaux", "business_unit", "legal_entity",
            "start_date", "end_date", "construction_cost",
            "address", "city", "postal_code", "country",
            "surface", "surface_unit", "currency", "tags", "title_on_invoice",
            "pm", "associate_in_charge", "invoice_approver", "bu_director",
            "total_fees", "fee_calculation_method", "fee_rate_pct",
            "version", "phases", "support_services",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True, default="")
    pm_name = serializers.SerializerMethodField()
    active_phase = serializers.SerializerMethodField()
    budget_hours = serializers.SerializerMethodField()
    total_invoiced = serializers.SerializerMethodField()

    def get_pm_name(self, obj):
        if obj.pm:
            name = obj.pm.get_full_name()
            return name if name.strip() else obj.pm.username
        return ""

    def get_active_phase(self, obj):
        """Return the first non-locked realization phase name."""
        phase = obj.phases.filter(
            phase_type="REALIZATION", is_locked=False
        ).order_by("order").first()
        return phase.name if phase else ""

    def get_budget_hours(self, obj):
        """Sum of budgeted hours across all tasks (or phases if no tasks)."""
        from django.db.models import Sum
        total = obj.tasks.aggregate(s=Sum("budgeted_hours"))["s"]
        if total:
            return float(total)
        total = obj.phases.aggregate(s=Sum("budgeted_hours"))["s"]
        return float(total) if total else 0

    def get_total_invoiced(self, obj):
        """Sum of approved/sent/paid invoice amounts."""
        from django.db.models import Sum
        from apps.billing.models import Invoice
        total = Invoice.objects.filter(
            project=obj, status__in=["APPROVED", "SENT", "PAID"]
        ).aggregate(s=Sum("total_amount"))["s"]
        return float(total) if total else 0

    class Meta:
        model = Project
        fields = [
            "id", "code", "name", "client", "client_name",
            "contract_type", "status", "is_internal", "is_public", "is_consortium",
            "business_unit", "pm", "pm_name",
            "active_phase", "budget_hours", "total_invoiced",
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
        read_only_fields = ["id", "amendment_number", "requested_by", "approved_by", "approval_date", "created_at", "updated_at"]


class FinancialPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialPhase
        fields = [
            "id", "name", "code", "billing_mode",
            "fixed_amount", "hourly_budget_max",
        ]
        read_only_fields = ["id"]


class EmployeeAssignmentSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    phase_name = serializers.CharField(source="phase.name", read_only=True, default="")

    class Meta:
        model = EmployeeAssignment
        fields = [
            "id", "employee", "employee_name", "project", "phase", "phase_name",
            "percentage", "start_date", "end_date",
        ]
        read_only_fields = ["id", "project", "employee_name", "phase_name"]

    def get_employee_name(self, obj):
        if obj.employee:
            name = obj.employee.get_full_name()
            return name if name.strip() else obj.employee.username
        return ""
