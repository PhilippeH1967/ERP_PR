"""Tests for Time Entry API endpoints."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant
from apps.projects.models import Phase, Project
from apps.time_entries.models import TimeEntry, WeeklyApproval


@pytest.mark.django_db
class TestTimeEntryAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API", slug="te-api")
        self.project = Project.objects.create(
            tenant=self.tenant, code="TE1", name="TimeProject"
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Ph1"
        )
        self.user = User.objects.create_user(username="te_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_entries(self):
        response = self.api.get("/api/v1/time_entries/")
        assert response.status_code == 200

    def test_create_entry(self):
        response = self.api.post(
            "/api/v1/time_entries/",
            {
                "project": self.project.pk,
                "phase": self.phase.pk,
                "date": "2026-03-16",
                "hours": "7.50",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_submit_week(self):
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, date=date(2026, 3, 16),
            hours=7.5, status="DRAFT",
        )
        response = self.api.post(
            "/api/v1/time_entries/submit_week/",
            {"week_start": "2026-03-16"},
            format="json",
        )
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["submitted_count"] == 1


@pytest.mark.django_db
class TestApprovalAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Appr", slug="appr-api")
        self.employee = User.objects.create_user(username="emp_a", password="pass123!")
        self.pm = User.objects.create_user(username="pm_a", password="pass123!")
        # Give PM role so they can see all approvals
        from apps.core.models import ProjectRole, Role
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.approval = WeeklyApproval.objects.create(
            tenant=self.tenant, employee=self.employee,
            week_start=date(2026, 3, 16), week_end=date(2026, 3, 22),
        )
        self.api = APIClient()

    def test_pm_approve(self):
        self.api.force_authenticate(user=self.pm)
        response = self.api.post(
            f"/api/v1/weekly_approvals/{self.approval.pk}/approve_pm/"
        )
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["pm_status"] == "APPROVED"

    def test_self_approval_blocked(self):
        """Employee cannot approve their own timesheet."""
        self.api.force_authenticate(user=self.employee)
        response = self.api.post(
            f"/api/v1/weekly_approvals/{self.approval.pk}/approve_pm/"
        )
        assert response.status_code == 403
