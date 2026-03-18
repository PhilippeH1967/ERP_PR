"""
Management command to create PostgreSQL Row-Level Security policies
for all models inheriting TenantScopedModel.

Usage:
    python manage.py setup_rls

Idempotent: safe to run multiple times. Drops and recreates policies.
"""

import structlog
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, transaction

logger = structlog.get_logger()


class Command(BaseCommand):
    help = "Create PostgreSQL RLS policies for all tenant-scoped models"

    def handle(self, *args, **options):
        from apps.core.models import TenantScopedModel

        tenant_models = []
        for model in apps.get_models():
            if (
                issubclass(model, TenantScopedModel)
                and not model._meta.abstract
                and model._meta.managed
            ):
                tenant_models.append(model)

        if not tenant_models:
            self.stdout.write(self.style.WARNING("No tenant-scoped models found."))
            return

        self.stdout.write(f"Found {len(tenant_models)} tenant-scoped model(s).")
        created = 0
        errors = 0

        try:
            with transaction.atomic(), connection.cursor() as cursor:
                    for model in tenant_models:
                        table = model._meta.db_table
                        # Use quote_name to prevent SQL injection
                        quoted_table = connection.ops.quote_name(table)
                        try:
                            cursor.execute(
                                f"ALTER TABLE {quoted_table} ENABLE ROW LEVEL SECURITY;"
                            )
                            cursor.execute(
                                f"DROP POLICY IF EXISTS tenant_isolation ON {quoted_table};"
                            )
                            rls_condition = (
                                "tenant_id = current_setting("
                                "'app.current_tenant')::int"
                            )
                            cursor.execute(
                                f"CREATE POLICY tenant_isolation ON {quoted_table} "
                                f"USING ({rls_condition}) "
                                f"WITH CHECK ({rls_condition});"
                            )
                            created += 1
                            self.stdout.write(
                                self.style.SUCCESS(f"  ✓ {table} — RLS policy created")
                            )
                            logger.info("rls_policy_created", table=table)
                        except Exception as e:
                            errors += 1
                            self.stdout.write(
                                self.style.ERROR(f"  ✗ {table} — {e}")
                            )
                            logger.error("rls_policy_failed", table=table, error=str(e))
                            raise  # Re-raise to trigger transaction rollback
        except Exception:
            if errors:
                self.stdout.write(
                    self.style.ERROR(
                        f"Rolled back: {errors} error(s) encountered. No policies applied."
                    )
                )
                return

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"Done: {created} policies created successfully.")
        )
