"""Expense API views with approval workflow."""

from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ExpenseCategory, ExpenseLine, ExpenseReport
from .serializers import (
    ExpenseCategorySerializer,
    ExpenseLineSerializer,
    ExpenseReportSerializer,
)


class ExpenseReportViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ExpenseReport.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.prefetch_related("lines")

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(
                tenant=Tenant.objects.get(pk=tenant_id),
                employee=self.request.user,
            )
        else:
            serializer.save(employee=self.request.user)

    def _transition(self, request, pk, from_statuses, to_status):
        """Generic status transition helper."""
        report = self.get_object()
        if report.status not in from_statuses:
            raise serializers.ValidationError(
                f"Transition impossible depuis le statut '{report.status}'."
            )
        report.status = to_status
        report.save(skip_version_increment=False)
        return Response(ExpenseReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def submit(self, request, pk=None):
        """Employee submits expense report for PM approval."""
        return self._transition(request, pk, ["DRAFT", "REJECTED"], "SUBMITTED")

    @action(detail=True, methods=["post"])
    def approve_pm(self, request, pk=None):
        """PM approves expense report."""
        report = self.get_object()
        if report.status != "SUBMITTED":
            raise serializers.ValidationError("Le rapport doit être soumis.")
        if report.employee == request.user:
            raise serializers.ValidationError("Auto-approbation interdite.")
        report.status = "PM_APPROVED"
        report.save(skip_version_increment=False)
        return Response(ExpenseReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def approve_finance(self, request, pk=None):
        """Finance analyst validates expense report."""
        return self._transition(request, pk, ["PM_APPROVED"], "FINANCE_VALIDATED")

    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        """Finance marks expense as paid."""
        return self._transition(request, pk, ["FINANCE_VALIDATED"], "PAID")

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """Reject expense report with reason."""
        report = self.get_object()
        if report.status not in ["SUBMITTED", "PM_APPROVED"]:
            raise serializers.ValidationError("Impossible de refuser à ce statut.")
        report.status = "REJECTED"
        report.save(skip_version_increment=False)
        return Response(ExpenseReportSerializer(report).data)

    @action(detail=True, methods=["post"])
    def reverse(self, request, pk=None):
        """Reverse a paid expense report."""
        return self._transition(request, pk, ["PAID"], "REVERSED")


class ExpenseLineViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseLine.objects.filter(report_id=self.kwargs["report_pk"])

    def perform_create(self, serializer):
        report = ExpenseReport.objects.get(pk=self.kwargs["report_pk"])
        serializer.save(report=report, tenant=report.tenant)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = ExpenseCategory.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from apps.core.models import Tenant

            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            serializer.save()
