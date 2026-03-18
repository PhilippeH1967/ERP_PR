"""Tests for TimeEntry, WeeklyApproval, TimesheetLock models."""

from datetime import date

import pytest
from django.contrib.auth.models import User

from apps.core.models import Tenant
from apps.projects.models import Phase, Project
from apps.time_entries.models import (
    TimeEntry,
    TimesheetLock,
    WeeklyApproval,
)


@pytest.mark.django_db
class TestTimeEntry:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-time")
        self.user = User.objects.create_user(username="emp", password="pass123!")
        self.project = Project.objects.create(
            tenant=self.tenant, code="P1", name="Project"
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept"
        )

    def test_create_entry(self):
        entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, phase=self.phase,
            date=date(2026, 3, 16), hours=7.5,
        )
        assert entry.pk is not None
        assert entry.status == "DRAFT"
        assert entry.version == 1

    def test_unique_constraint(self):
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, phase=self.phase,
            date=date(2026, 3, 16), hours=7.5,
        )
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            TimeEntry.objects.create(
                tenant=self.tenant, employee=self.user,
                project=self.project, phase=self.phase,
                date=date(2026, 3, 16), hours=1,
            )

    def test_history_tracked(self):
        entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, date=date(2026, 3, 16), hours=7,
        )
        entry.hours = 8
        entry.save()
        assert entry.history.count() == 2


@pytest.mark.django_db
class TestWeeklyApproval:
    def test_create_approval(self):
        tenant = Tenant.objects.create(name="T", slug="t-approval")
        user = User.objects.create_user(username="appr", password="pass123!")
        approval = WeeklyApproval.objects.create(
            tenant=tenant, employee=user,
            week_start=date(2026, 3, 16), week_end=date(2026, 3, 22),
        )
        assert approval.pm_status == "PENDING"
        assert approval.finance_status == "PENDING"


@pytest.mark.django_db
class TestTimesheetLock:
    def test_create_phase_lock(self):
        tenant = Tenant.objects.create(name="T", slug="t-lock")
        project = Project.objects.create(tenant=tenant, code="PL", name="Lock")
        phase = Phase.objects.create(tenant=tenant, project=project, name="Ph")
        pm = User.objects.create_user(username="pm_lock", password="pass123!")
        lock = TimesheetLock.objects.create(
            tenant=tenant, project=project, phase=phase,
            lock_type="PHASE", locked_by=pm,
        )
        assert lock.pk is not None
        assert lock.lock_type == "PHASE"
