"""Celery tasks for core operations."""

import structlog
from celery import shared_task
from django.utils import timezone

logger = structlog.get_logger()


@shared_task
def expire_delegations():
    """
    Auto-expire delegations past their end_date.

    Scheduled via Celery Beat (daily, 1 AM). Runs per active tenant under
    `tenant_context` so it works with a non-superuser DB role (RLS).
    """
    from apps.core.models import Delegation, Tenant
    from apps.core.tenant_context import tenant_context

    today = timezone.now().date()
    expired = 0
    for tenant in Tenant.objects.filter(is_active=True):
        with tenant_context(tenant.id):
            expired += Delegation.objects.filter(
                tenant=tenant,
                is_active=True,
                end_date__lt=today,
            ).update(is_active=False)

    logger.info("delegations_expired", count=expired)
    return {"expired": expired}
