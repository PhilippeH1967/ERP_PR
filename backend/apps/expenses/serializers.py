"""Expense serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import ExpenseApproval, ExpenseCategory, ExpenseLine, ExpenseReport


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name", "is_refacturable_default", "requires_receipt", "gl_account"]
        read_only_fields = ["id"]


class ExpenseLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseLine
        fields = [
            "id", "category", "expense_date", "amount", "description",
            "receipt_path", "is_refacturable", "refacturable_markup_pct", "tax_type",
        ]
        read_only_fields = ["id"]


class ExpenseReportSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    lines = ExpenseLineSerializer(many=True, read_only=True)

    class Meta:
        model = ExpenseReport
        fields = [
            "id", "employee", "project", "status", "total_amount",
            "version", "submitted_at", "lines", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "employee", "submitted_at", "created_at", "updated_at"]


class ExpenseApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseApproval
        fields = ["id", "report", "approved_by", "role_level", "status", "rejection_reason", "date"]
        read_only_fields = ["id", "date"]
