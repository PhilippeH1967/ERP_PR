"""Celery tasks for automated timesheet reminders (Story 4.6)."""

import structlog
from celery import shared_task

logger = structlog.get_logger()


@shared_task
def send_timesheet_reminders():
    """
    Send reminders to employees with incomplete timesheets.

    Scheduled via Celery Beat (e.g., Thursday 5pm).
    """
    # TODO: Query employees without submitted timesheets for current week
    # TODO: Send in-app notification + email
    logger.info("timesheet_reminders_sent", count=0)
    return {"reminders_sent": 0}
