"""Time entry serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import PeriodUnlock, TimeEntry, TimesheetLock, WeeklyApproval


class TimeEntrySerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = [
            "id", "employee", "project", "phase", "date", "hours",
            "notes", "status", "is_favorite", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "employee", "created_at", "updated_at"]


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
