"""Tests for timesheet reminder/escalation Celery tasks."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.notifications.models import Notification
from apps.time_entries.models import WeeklyApproval
from apps.time_entries.tasks import (
    escalate_missing_timesheets,
    send_timesheet_reminders,
)


def _monday():
    today = timezone.now().date()
    return today - timezone.timedelta(days=today.weekday())


@pytest.mark.django_db
class TestSendTimesheetReminders:
    def test_notifies_users_without_submission(self):
        tenant = Tenant.objects.create(name="R", slug="rem-1")
        missing = User.objects.create_user("missing_u", password="x")
        ok = User.objects.create_user("ok_u", password="x")
        UserTenantAssociation.objects.create(user=missing, tenant=tenant)
        UserTenantAssociation.objects.create(user=ok, tenant=tenant)
        WeeklyApproval.objects.create(
            tenant=tenant,
            employee=ok,
            week_start=_monday(),
            week_end=_monday() + timezone.timedelta(days=6),
        )

        result = send_timesheet_reminders()

        assert result["reminders_sent"] == 1
        notifs = Notification.objects.filter(tenant=tenant, notification_type="timesheet_reminder")
        assert notifs.count() == 1
        assert notifs.first().user_id == missing.id

    def test_isolated_per_tenant(self):
        ta = Tenant.objects.create(name="A", slug="rem-a")
        tb = Tenant.objects.create(name="B", slug="rem-b")
        ua = User.objects.create_user("rem_a", password="x")
        ub = User.objects.create_user("rem_b", password="x")
        UserTenantAssociation.objects.create(user=ua, tenant=ta)
        UserTenantAssociation.objects.create(user=ub, tenant=tb)

        send_timesheet_reminders()

        assert Notification.objects.filter(tenant=ta, user=ua).count() == 1
        assert Notification.objects.filter(tenant=tb, user=ub).count() == 1
        assert Notification.objects.filter(tenant=ta, user=ub).count() == 0


@pytest.mark.django_db
class TestEscalateMissingTimesheets:
    def test_pm_notified_for_missing_team_member(self):
        from apps.planning.models import ResourceAllocation
        from apps.projects.models import Phase, Project

        tenant = Tenant.objects.create(name="E", slug="esc-1")
        pm = User.objects.create_user("pm_esc", password="x")
        emp = User.objects.create_user("emp_esc", password="x")
        UserTenantAssociation.objects.create(user=pm, tenant=tenant)
        UserTenantAssociation.objects.create(user=emp, tenant=tenant)
        ProjectRole.objects.create(user=pm, tenant=tenant, role=Role.PM)
        project = Project.objects.create(
            tenant=tenant, code="ESC-1", name="Esc", pm=pm, status="ACTIVE"
        )
        phase = Phase.objects.create(tenant=tenant, project=project, name="Ph1")
        ResourceAllocation.objects.create(
            tenant=tenant,
            employee=emp,
            project=project,
            phase=phase,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            hours_per_week=10,
            created_by=pm,
        )

        result = escalate_missing_timesheets()

        assert result["escalations_sent"] == 1
        esc = Notification.objects.filter(tenant=tenant, notification_type="timesheet_escalation")
        assert esc.count() == 1
        assert esc.first().user_id == pm.id

    def test_no_escalation_when_all_submitted(self):
        tenant = Tenant.objects.create(name="E2", slug="esc-2")
        pm = User.objects.create_user("pm_esc2", password="x")
        UserTenantAssociation.objects.create(user=pm, tenant=tenant)
        ProjectRole.objects.create(user=pm, tenant=tenant, role=Role.PM)

        result = escalate_missing_timesheets()

        assert result["escalations_sent"] == 0
