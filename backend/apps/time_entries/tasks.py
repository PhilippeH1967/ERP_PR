"""Celery tasks for automated timesheet reminders (FR26)."""

import structlog
from celery import shared_task
from django.utils import timezone

logger = structlog.get_logger()


def _get_current_monday():
    today = timezone.now().date()
    return today - timezone.timedelta(days=today.weekday())


def _find_missing_users(tenant, monday):
    """Find active users who haven't submitted their timesheet for the week."""
    from django.contrib.auth import get_user_model

    from apps.core.models import UserTenantAssociation
    from apps.time_entries.models import WeeklyApproval

    User = get_user_model()

    user_ids = UserTenantAssociation.objects.filter(
        tenant=tenant,
    ).values_list("user_id", flat=True)

    submitted_user_ids = WeeklyApproval.objects.filter(
        tenant=tenant,
        week_start=monday,
    ).values_list("employee_id", flat=True)

    return User.objects.filter(
        id__in=user_ids, is_active=True,
    ).exclude(id__in=submitted_user_ids)


@shared_task
def send_timesheet_reminders():
    """
    Send reminders to employees with incomplete timesheets.

    FR26 — Scheduled Wed 17h and Fri 12h via Celery Beat.
    Creates in-app notifications + email for missing submissions.
    """
    from apps.core.models import Tenant
    from apps.notifications.models import Notification

    monday = _get_current_monday()
    today = timezone.now().date()
    is_friday = today.weekday() == 4  # More urgent on Friday

    count = 0
    for tenant in Tenant.objects.filter(is_active=True):
        missing = _find_missing_users(tenant, monday)

        for user in missing:
            urgency = "urgent" if is_friday else "reminder"
            message = (
                f"{'URGENT : ' if is_friday else ''}Rappel — votre feuille de temps "
                f"pour la semaine du {monday.strftime('%d/%m/%Y')} n'est pas encore soumise."
            )
            Notification.objects.create(
                tenant=tenant,
                user=user,
                notification_type="timesheet_reminder",
                message=message,
            )
            # Email sending (Django's send_mail) — only if user has email
            if user.email:
                try:
                    from django.core.mail import send_mail

                    send_mail(
                        subject=f"{'[URGENT] ' if is_friday else ''}Rappel feuille de temps — semaine du {monday.strftime('%d/%m/%Y')}",
                        message=message,
                        from_email=None,  # Uses DEFAULT_FROM_EMAIL
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception:
                    logger.warning("email_send_failed", user=user.email)
            count += 1

    logger.info("timesheet_reminders_sent", count=count, urgency="friday" if is_friday else "wednesday")
    return {"reminders_sent": count}


@shared_task
def escalate_missing_timesheets():
    """
    FR26 escalation — notify managers about employees with missing timesheets.

    Runs Friday 17h. Alerts PM/managers about their team members who haven't submitted.
    """
    from django.db.models import Q

    from apps.core.models import ProjectRole, Role, Tenant
    from apps.notifications.models import Notification
    from apps.projects.models import EmployeeAssignment

    monday = _get_current_monday()

    count = 0
    for tenant in Tenant.objects.filter(is_active=True):
        missing_users = _find_missing_users(tenant, monday)
        if not missing_users.exists():
            continue

        missing_ids = set(missing_users.values_list("id", flat=True))

        # Find PMs who manage these employees (via project assignments)
        pm_user_ids = set(
            ProjectRole.objects.filter(
                tenant=tenant,
                role__in=[Role.PM, Role.PROJECT_DIRECTOR],
            ).values_list("user_id", flat=True)
        )

        for pm_id in pm_user_ids:
            # Find which missing employees are assigned to PM's projects
            managed_projects = EmployeeAssignment.objects.filter(
                project__pm_id=pm_id,
            ).values_list("employee_id", flat=True)
            my_missing = missing_ids & set(managed_projects)
            if not my_missing:
                continue

            missing_names = list(
                missing_users.filter(id__in=my_missing).values_list("username", flat=True)
            )
            Notification.objects.create(
                tenant=tenant,
                user_id=pm_id,
                notification_type="timesheet_escalation",
                message=(
                    f"Escalade : {len(missing_names)} employé(s) n'ont pas soumis "
                    f"leur feuille de temps (semaine du {monday.strftime('%d/%m/%Y')}) : "
                    f"{', '.join(missing_names[:5])}{'...' if len(missing_names) > 5 else ''}"
                ),
            )
            count += 1

    logger.info("timesheet_escalation_sent", count=count)
    return {"escalations_sent": count}
