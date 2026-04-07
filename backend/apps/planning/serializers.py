"""Planning serializers."""

from rest_framework import serializers

from .models import Availability, Milestone, PhaseDependency, ResourceAllocation


class ResourceAllocationSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    project_code = serializers.CharField(source="project.code", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    phase_name = serializers.CharField(source="phase.name", read_only=True, default="")
    task_name = serializers.CharField(source="task.name", read_only=True, default="")
    total_planned_hours = serializers.DecimalField(
        max_digits=8, decimal_places=1, read_only=True
    )

    class Meta:
        model = ResourceAllocation
        fields = [
            "id", "employee", "employee_name",
            "project", "project_code", "project_name",
            "phase", "phase_name", "task", "task_name",
            "start_date", "end_date", "hours_per_week",
            "total_planned_hours", "status", "notes",
            "created_at",
        ]
        read_only_fields = ["id", "total_planned_hours", "created_at"]

    def get_employee_name(self, obj):
        name = obj.employee.get_full_name()
        return name if name.strip() else obj.employee.username


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
