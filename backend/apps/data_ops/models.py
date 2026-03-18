"""Import/Export jobs and operations log (Epic 11 + data ops)."""

from django.conf import settings
from django.db import models

from apps.core.models import TenantScopedModel


class ImportJob(TenantScopedModel):
    """Bulk data import job (ChangePoint migration, Excel, etc.)."""

    import_type = models.CharField(max_length=50)
    file_path = models.CharField(max_length=500)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "En attente"), ("processing", "En cours"),
            ("completed", "Terminé"), ("failed", "Échoué"),
        ],
        default="pending",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, default="")
    record_count = models.IntegerField(default=0)

    class Meta:
        db_table = "data_ops_import_job"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Import {self.import_type} ({self.status})"


class ExportJob(TenantScopedModel):
    """Bulk data export job (CSV, Excel, PDF, Intacct)."""

    export_type = models.CharField(max_length=50)
    format = models.CharField(
        max_length=10,
        choices=[("csv", "CSV"), ("excel", "Excel"), ("pdf", "PDF")],
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "En attente"), ("processing", "En cours"),
            ("completed", "Terminé"), ("failed", "Échoué"),
        ],
        default="pending",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    file_url = models.CharField(max_length=500, blank=True, default="")
    record_count = models.IntegerField(default=0)

    class Meta:
        db_table = "data_ops_export_job"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Export {self.export_type} ({self.status})"


class OperationsLog(TenantScopedModel):
    """Audit journal for bulk operations."""

    operation_type = models.CharField(max_length=50)
    source_table = models.CharField(max_length=100)
    record_count = models.IntegerField(default=0)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    performed_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    class Meta:
        db_table = "data_ops_operations_log"
        ordering = ["-performed_at"]

    def __str__(self):
        return f"{self.operation_type} — {self.source_table} ({self.record_count} records)"
