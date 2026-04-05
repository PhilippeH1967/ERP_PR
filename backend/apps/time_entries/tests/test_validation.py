"""Tests for time entry validation and workflow enforcement."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant
from apps.projects.models import Phase, Project
from apps.time_entries.models import TimeEntry, WeeklyApproval


@pytest.mark.django_db
class TestTimeEntryValidation:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-val")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PV", name="Validation"
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Ph"
        )
        self.user = User.objects.create_user(username="val_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_duplicate_entry_rejected(self):
        """Same employee+project+phase+date cannot have two entries."""
        from django.db import IntegrityError as DjangoIntegrityError

        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, phase=self.phase,
            date=date(2026, 3, 16), hours=7,
        )
        # DB unique constraint prevents duplicate — raises IntegrityError
        with pytest.raises(DjangoIntegrityError):
            TimeEntry.objects.create(
                tenant=self.tenant, employee=self.user,
                project=self.project, phase=self.phase,
                date=date(2026, 3, 16), hours=8,
            )

    def test_copy_previous_week(self):
        """Copy entries from previous week as DRAFT."""
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, phase=self.phase,
            date=date(2026, 3, 9), hours=7.5,
        )
        response = self.api.post(
            "/api/v1/time_entries/copy_previous_week/",
            {"week_start": "2026-03-16"},
            format="json",
        )
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["copied_count"] >= 1

    def test_weekly_stats_endpoint(self):
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, date=date(2026, 3, 16), hours=8,
        )
        response = self.api.get("/api/v1/time_entries/weekly_stats/")
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert "contract_hours" in payload
        assert "average_4_weeks" in payload

    def test_submit_week_changes_status(self):
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, date=date(2026, 3, 16),
            hours=8, status="DRAFT",
        )
        response = self.api.post(
            "/api/v1/time_entries/submit_week/",
            {"week_start": "2026-03-16"},
            format="json",
        )
        assert response.status_code == 200
        # Verify status changed
        entry = TimeEntry.objects.get(
            employee=self.user, project=self.project, date=date(2026, 3, 16)
        )
        assert entry.status == "SUBMITTED"


@pytest.mark.django_db
class TestApprovalWorkflow:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-wf")
        self.employee = User.objects.create_user(username="wf_emp", password="pass123!")
        self.pm = User.objects.create_user(username="wf_pm", password="pass123!")
        self.finance = User.objects.create_user(username="wf_fin", password="pass123!")
        # Give roles so they can see approvals
        from apps.core.models import ProjectRole, Role
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        ProjectRole.objects.create(user=self.finance, tenant=self.tenant, role=Role.FINANCE)
        self.approval = WeeklyApproval.objects.create(
            tenant=self.tenant, employee=self.employee,
            week_start=date(2026, 3, 16), week_end=date(2026, 3, 22),
        )
        self.api = APIClient()

    def test_pm_can_approve(self):
        self.api.force_authenticate(user=self.pm)
        response = self.api.post(
            f"/api/v1/weekly_approvals/{self.approval.pk}/approve_pm/"
        )
        assert response.status_code == 200
        self.approval.refresh_from_db()
        assert self.approval.pm_status == "APPROVED"

    def test_finance_can_approve_after_pm(self):
        # First PM approves
        self.approval.pm_status = "APPROVED"
        self.approval.save()
        # Then finance approves
        self.api.force_authenticate(user=self.finance)
        response = self.api.post(
            f"/api/v1/weekly_approvals/{self.approval.pk}/approve_finance/"
        )
        assert response.status_code == 200
        self.approval.refresh_from_db()
        assert self.approval.finance_status == "APPROVED"

    def test_employee_cannot_self_approve(self):
        self.api.force_authenticate(user=self.employee)
        response = self.api.post(
            f"/api/v1/weekly_approvals/{self.approval.pk}/approve_pm/"
        )
        assert response.status_code == 403
