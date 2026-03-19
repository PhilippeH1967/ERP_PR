"""Celery tasks for automated timesheet reminders (Story 4.6)."""

import structlog
from celery import shared_task
from django.utils import timezone

logger = structlog.get_logger()


@shared_task
def send_timesheet_reminders():
    """
    Send reminders to employees with incomplete timesheets.

    Scheduled via Celery Beat (e.g., Thursday 5pm).
    Creates in-app notifications for users who haven't submitted.
    """
    from django.contrib.auth import get_user_model

    from apps.core.models import Tenant, UserTenantAssociation
    from apps.notifications.models import Notification
    from apps.time_entries.models import WeeklyApproval

    User = get_user_model()

    # Get current week Monday
    today = timezone.now().date()
    monday = today - timezone.timedelta(days=today.weekday())

    count = 0
    for tenant in Tenant.objects.filter(is_active=True):
        # Get all users in this tenant
        user_ids = UserTenantAssociation.objects.filter(
            tenant=tenant,
        ).values_list("user_id", flat=True)

        # Find who already submitted
        submitted_user_ids = WeeklyApproval.objects.filter(
            tenant=tenant,
            week_start=monday,
        ).values_list("employee_id", flat=True)

        # Users who haven't submitted
        missing = User.objects.filter(
            id__in=user_ids, is_active=True,
        ).exclude(id__in=submitted_user_ids)

        for user in missing:
            Notification.objects.create(
                tenant=tenant,
                user=user,
                notification_type="timesheet_reminder",
                message=f"Rappel : votre feuille de temps pour la semaine du {monday.strftime('%d/%m/%Y')} n'est pas encore soumise.",
            )
            count += 1

    logger.info("timesheet_reminders_sent", count=count)
    return {"reminders_sent": count}
