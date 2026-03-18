"""Time entry serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import PeriodUnlock, TimeEntry, TimesheetLock, WeeklyApproval


class TimeEntrySerializer(OptimisticLockMixin, serializers.ModelSerializer):
    """TimeEntry with nested project/phase names for grid display."""

    project_code = serializers.CharField(source="project.code", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    phase_name = serializers.SerializerMethodField()
    client_label = serializers.SerializerMethodField()

    class Meta:
        model = TimeEntry
        fields = [
            "id", "employee", "project", "project_code", "project_name",
            "phase", "phase_name", "client_label",
            "date", "hours", "notes", "status", "is_favorite", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "employee", "project_code", "project_name",
            "phase_name", "client_label", "created_at", "updated_at",
        ]

    def get_phase_name(self, obj):
        if obj.phase:
            return obj.phase.name
        return ""

    def get_client_label(self, obj):
        if obj.phase:
            return obj.phase.client_facing_label or obj.phase.name
        return ""


class WeeklyApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyApproval
        fields = [
            "id", "employee", "week_start", "week_end",
            "pm_status", "pm_approved_by", "pm_approved_at",
            "finance_status", "finance_approved_by", "finance_approved_at",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TimesheetLockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetLock
        fields = [
            "id", "project", "phase", "person", "lock_type",
            "locked_by", "locked_at",
        ]
        read_only_fields = ["id", "locked_at"]


class PeriodUnlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodUnlock
        fields = [
            "id", "period_start", "period_end", "reason",
            "justification", "unlocked_by", "unlocked_at",
        ]
        read_only_fields = ["id", "unlocked_at"]
