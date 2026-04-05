"""Leave serializers."""

from rest_framework import serializers

from .models import LeaveBank, LeaveRequest, LeaveType, PublicHoliday


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            "id", "code", "name", "name_en", "is_paid",
            "requires_medical_cert", "medical_cert_threshold_days",
            "max_days_per_year", "accrual_rate_monthly",
            "can_carry_over", "carry_over_max_days",
            "is_active", "order",
        ]
        read_only_fields = ["id"]


class LeaveBankSerializer(serializers.ModelSerializer):
    leave_type_code = serializers.CharField(source="leave_type.code", read_only=True)
    leave_type_name = serializers.CharField(source="leave_type.name", read_only=True)
    balance = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = LeaveBank
        fields = [
            "id", "employee", "leave_type", "leave_type_code", "leave_type_name",
            "year", "accrued", "used", "carried_over", "manual_adjustment",
            "balance",
        ]
        read_only_fields = ["id", "balance"]


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    leave_type_name = serializers.CharField(source="leave_type.name", read_only=True)
    leave_type_code = serializers.CharField(source="leave_type.code", read_only=True)
    total_hours = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    approved_by_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            "id", "employee", "employee_name",
            "leave_type", "leave_type_code", "leave_type_name",
            "start_date", "end_date", "hours_per_day", "total_days",
            "reason", "status",
            "approved_by", "approved_by_name", "approved_at",
            "rejection_reason",
            "medical_cert_uploaded", "time_entries_created",
            "total_hours",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "employee", "status",
            "approved_by", "approved_at",
            "time_entries_created",
            "created_at", "updated_at",
        ]

    def get_employee_name(self, obj):
        name = obj.employee.get_full_name()
        return name if name.strip() else obj.employee.username

    def get_approved_by_name(self, obj):
        if obj.approved_by:
            name = obj.approved_by.get_full_name()
            return name if name.strip() else obj.approved_by.username
        return ""


class PublicHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicHoliday
        fields = ["id", "name", "date", "is_paid", "labor_rule"]
        read_only_fields = ["id"]
