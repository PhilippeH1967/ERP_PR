"""Expense API views."""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
