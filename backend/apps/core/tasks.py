"""Celery tasks for core operations."""

import structlog
from celery import shared_task
from django.utils import timezone

logger = structlog.get_logger()


@shared_task
def expire_delegations():
    """
    Auto-expire delegations past their end_date.

    Scheduled via Celery Beat (daily, 1 AM).
    """
    from apps.core.models import Delegation

    today = timezone.now().date()
    expired = Delegation.objects.filter(
        is_active=True,
        end_date__lt=today,
    ).update(is_active=False)

    logger.info("delegations_expired", count=expired)
    return {"expired": expired}
