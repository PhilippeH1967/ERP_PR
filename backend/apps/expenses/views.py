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
        from apps.core.models import Tenant, UserTenantAssociation

        tenant_id = getattr(self.request, "tenant_id", None)
        tenant = None
        if tenant_id:
            tenant = Tenant.objects.filter(pk=tenant_id).first()
        if tenant is None:
            assoc = UserTenantAssociation.objects.filter(user=self.request.user).select_related("tenant").first()
            if assoc:
                tenant = assoc.tenant
        if tenant is None:
            tenant = Tenant.objects.first()
        serializer.save(tenant=tenant, employee=self.request.user)

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

    @action(detail=True, methods=["post"], url_path="upload_receipt")
    def upload_receipt(self, request, pk=None):
        """Upload receipt file for an expense line."""
        import os
        from django.conf import settings

        report = self.get_object()
        receipt = request.FILES.get("receipt")
        line_id = request.data.get("line_id")
        if not receipt:
            return Response(
                {"error": {"code": "NO_FILE", "message": "Fichier reçu manquant"}},
                status=400,
            )
        # Save file
        upload_dir = os.path.join(settings.MEDIA_ROOT, "receipts", str(report.pk))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, receipt.name)
        with open(file_path, "wb+") as f:
            for chunk in receipt.chunks():
                f.write(chunk)

        relative_path = f"receipts/{report.pk}/{receipt.name}"

        # Update line if specified
        if line_id:
            ExpenseLine.objects.filter(pk=line_id, report=report).update(receipt_path=relative_path)

        return Response({"receipt_path": relative_path})


class ExpenseLineViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseLineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseLine.objects.filter(report_id=self.kwargs["report_pk"])

    def perform_create(self, serializer):
        report = ExpenseReport.objects.get(pk=self.kwargs["report_pk"])
        # Inherit tenant from parent report (always set)
        serializer.save(report=report, tenant=report.tenant)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["report_pk"] = self.kwargs.get("report_pk")
        return ctx


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
