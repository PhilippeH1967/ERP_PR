"""Planning serializers."""

import re

from rest_framework import serializers

from .models import (
    Availability,
    Milestone,
    PhaseDependency,
    PlanningStandard,
    ResourceAllocation,
    VirtualResource,
)

_WEEK_KEY_RE = re.compile(r"^\d{4}-W(0[1-9]|[1-4]\d|5[0-3])$")
_MONTH_KEY_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class ResourceAllocationSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    virtual_resource_name = serializers.CharField(
        source="virtual_resource.name", read_only=True, default="",
    )
    project_code = serializers.CharField(source="project.code", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    phase_name = serializers.CharField(source="phase.name", read_only=True, default="")
    task_name = serializers.CharField(source="task.name", read_only=True, default="")
    total_planned_hours = serializers.SerializerMethodField()

    class Meta:
        model = ResourceAllocation
        fields = [
            "id", "employee", "employee_name",
            "virtual_resource", "virtual_resource_name",
            "project", "project_code", "project_name",
            "phase", "phase_name", "task", "task_name",
            "start_date", "end_date", "hours_per_week",
            "distribution_mode", "time_unit", "time_breakdown", "standard",
            "total_planned_hours", "status", "notes",
            "created_at",
        ]
        read_only_fields = ["id", "total_planned_hours", "created_at"]

    def get_employee_name(self, obj):
        if not obj.employee_id:
            return ""
        name = obj.employee.get_full_name()
        return name if name.strip() else obj.employee.username

    def get_total_planned_hours(self, obj):
        return obj.total_planned_hours

    def validate(self, attrs):
        # XOR phase/task — on PATCH, attrs may omit one; fall back to self.instance.
        has_phase_key = "phase" in attrs
        has_task_key = "task" in attrs
        phase = attrs.get("phase") if has_phase_key else getattr(self.instance, "phase", None)
        task = attrs.get("task") if has_task_key else getattr(self.instance, "task", None)
        if (phase is None) == (task is None):
            raise serializers.ValidationError(
                {"phase": "Allocation must target exactly one of phase or task."}
            )
        # XOR employee/virtual_resource
        has_emp_key = "employee" in attrs
        has_vr_key = "virtual_resource" in attrs
        employee = attrs.get("employee") if has_emp_key else getattr(
            self.instance, "employee", None,
        )
        virtual = attrs.get("virtual_resource") if has_vr_key else getattr(
            self.instance, "virtual_resource", None,
        )
        if (employee is None) == (virtual is None):
            raise serializers.ValidationError(
                {"employee": (
                    "Allocation must target exactly one of employee or virtual_resource."
                )}
            )
        # Date ordering
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "end_date must be on or after start_date."}
            )
        return attrs

    def validate_time_breakdown(self, value):
        if value in (None, {}):
            return value
        if not isinstance(value, dict):
            raise serializers.ValidationError("time_breakdown must be an object.")
        time_unit = self.initial_data.get("time_unit") or getattr(
            self.instance, "time_unit", "week"
        )
        pattern = _WEEK_KEY_RE if time_unit == "week" else _MONTH_KEY_RE
        for k, v in value.items():
            if not pattern.match(str(k)):
                raise serializers.ValidationError(
                    f"Invalid key '{k}' for time_unit={time_unit}. "
                    "Expected format 'YYYY-Www' or 'YYYY-MM'."
                )
            try:
                float(v)
            except (TypeError, ValueError) as exc:
                raise serializers.ValidationError(
                    f"Value for '{k}' must be numeric."
                ) from exc
        return value


class PlanningStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningStandard
        fields = [
            "id", "name", "description", "phase_code",
            "time_unit", "curve", "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_curve(self, value):
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError("Curve must be a non-empty list.")
        try:
            total = sum(float(v) for v in value)
        except (TypeError, ValueError) as exc:
            raise serializers.ValidationError(
                "All curve values must be numeric."
            ) from exc
        if abs(total - 1.0) > 0.01:
            raise serializers.ValidationError(
                f"Curve values must sum to 1.0 ± 0.01 (got {total:.3f})."
            )
        return value


class MilestoneSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source="project.code", read_only=True)

    class Meta:
        model = Milestone
        fields = [
            "id", "project", "project_code",
            "title", "date", "description", "status", "color",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class PhaseDependencySerializer(serializers.ModelSerializer):
    predecessor_name = serializers.CharField(source="predecessor.name", read_only=True)
    successor_name = serializers.CharField(source="successor.name", read_only=True)

    class Meta:
        model = PhaseDependency
        fields = [
            "id", "project", "predecessor", "predecessor_name",
            "successor", "successor_name",
            "dependency_type", "lag_days",
        ]
        read_only_fields = ["id"]


class VirtualResourceSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source="project.code", read_only=True)
    replaced_by_name = serializers.SerializerMethodField()

    class Meta:
        model = VirtualResource
        fields = [
            "id", "project", "project_code",
            "name", "default_hourly_rate", "is_active", "notes",
            "replaced_by", "replaced_by_name", "replaced_at",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "replaced_by", "replaced_at"]

    def get_replaced_by_name(self, obj):
        if not obj.replaced_by_id:
            return ""
        name = obj.replaced_by.get_full_name()
        return name if name.strip() else obj.replaced_by.username


class AvailabilitySerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Availability
        fields = [
            "id", "employee", "employee_name",
            "date", "contractual_hours", "capacity_hours",
            "is_working_day", "leave_type",
        ]
        read_only_fields = ["id"]

    def get_employee_name(self, obj):
        name = obj.employee.get_full_name()
        return name if name.strip() else obj.employee.username
