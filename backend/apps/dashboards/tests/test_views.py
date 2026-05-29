"""Tests for dashboard KPI endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestDashboardEndpoints:
    def setup_method(self):
        self.user = User.objects.create_user(username="dash_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_role_dashboard_requires_auth(self):
        client = APIClient()
        response = client.get("/api/v1/dashboard/")
        assert response.status_code == 401

    def test_role_dashboard_authenticated(self):
        response = self.api.get("/api/v1/dashboard/")
        assert response.status_code == 200

    def test_pm_kpis(self):
        response = self.api.get("/api/v1/dashboard/pm-kpis/")
        assert response.status_code == 200

    def test_system_health(self):
        response = self.api.get("/api/v1/dashboard/system-health/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestSidebarBadgesApprovalsScoping:
    """S-080/S-081 regression: the `approvals` badge must reflect what the
    connected user can actually act on — for a PM, only WeeklyApprovals
    whose employee has timesheet entries on the PM's projects. ADMIN /
    PAIE / FINANCE keep tenant-wide visibility."""

    def setup_method(self):
        from datetime import date

        from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
        from apps.projects.models import Project
        from apps.time_entries.models import TimeEntry, WeeklyApproval

        self.Tenant = Tenant
        self.tenant = Tenant.objects.create(name="SB", slug="sb-app")
        self.pm = User.objects.create_user("sb_pm", password="x")
        self.other_pm = User.objects.create_user("sb_other_pm", password="x")
        self.emp_mine = User.objects.create_user("sb_emp_mine", password="x")
        self.emp_other = User.objects.create_user("sb_emp_other", password="x")
        for u in (self.pm, self.other_pm, self.emp_mine, self.emp_other):
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)

        mine = Project.objects.create(
            tenant=self.tenant, code="SB-1", name="Mine", pm=self.pm, status="ACTIVE"
        )
        other = Project.objects.create(
            tenant=self.tenant, code="SB-2", name="Other", pm=self.other_pm, status="ACTIVE"
        )

        week_start = date(2026, 3, 16)
        week_end = date(2026, 3, 22)
        TimeEntry.objects.create(
            tenant=self.tenant,
            employee=self.emp_mine,
            project=mine,
            date=week_start,
            hours=8,
            status="SUBMITTED",
        )
        TimeEntry.objects.create(
            tenant=self.tenant,
            employee=self.emp_other,
            project=other,
            date=week_start,
            hours=8,
            status="SUBMITTED",
        )
        WeeklyApproval.objects.create(
            tenant=self.tenant,
            employee=self.emp_mine,
            week_start=week_start,
            week_end=week_end,
            pm_status="PENDING",
        )
        WeeklyApproval.objects.create(
            tenant=self.tenant,
            employee=self.emp_other,
            week_start=week_start,
            week_end=week_end,
            pm_status="PENDING",
        )

        self.api = APIClient()

    def _get(self, user):
        self.api.force_authenticate(user=user)
        resp = self.api.get(
            "/api/v1/sidebar/badges/",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert resp.status_code == 200
        return resp.json()["data"]["badges"]

    def test_pm_badge_only_counts_own_projects(self):
        badges = self._get(self.pm)
        assert badges["approvals"] == 1, (
            "PM badge must count only WeeklyApprovals on the PM's projects"
        )

    def test_admin_badge_counts_tenant_wide(self):
        from apps.core.models import ProjectRole, Role

        admin = User.objects.create_user("sb_admin", password="x")
        ProjectRole.objects.create(user=admin, tenant=self.tenant, role=Role.ADMIN)
        badges = self._get(admin)
        assert badges["approvals"] == 2


@pytest.mark.django_db
class TestActionCenterPMScoping:
    """S-080/S-081 (suite): le compteur 'Feuilles a approuver' de la
    section 'A faire' (/action_center/) doit suivre la même règle que
    le badge sidebar — PM-scopé pour un PM, tenant-wide pour ADMIN."""

    def setup_method(self):
        from datetime import date

        from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
        from apps.projects.models import Project
        from apps.time_entries.models import TimeEntry, WeeklyApproval

        self.tenant = Tenant.objects.create(name="AC", slug="ac-scope")
        self.pm = User.objects.create_user("ac_pm", password="x")
        self.other_pm = User.objects.create_user("ac_other", password="x")
        self.emp_mine = User.objects.create_user("ac_emp_mine", password="x")
        self.emp_other = User.objects.create_user("ac_emp_other", password="x")
        for u in (self.pm, self.other_pm, self.emp_mine, self.emp_other):
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)

        mine = Project.objects.create(
            tenant=self.tenant, code="AC-1", name="Mine", pm=self.pm, status="ACTIVE"
        )
        other = Project.objects.create(
            tenant=self.tenant, code="AC-2", name="Other", pm=self.other_pm, status="ACTIVE"
        )
        ws, we = date(2026, 5, 4), date(2026, 5, 10)
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.emp_mine, project=mine,
            date=ws, hours=8, status="SUBMITTED",
        )
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.emp_other, project=other,
            date=ws, hours=8, status="SUBMITTED",
        )
        WeeklyApproval.objects.create(
            tenant=self.tenant, employee=self.emp_mine,
            week_start=ws, week_end=we, pm_status="PENDING",
        )
        WeeklyApproval.objects.create(
            tenant=self.tenant, employee=self.emp_other,
            week_start=ws, week_end=we, pm_status="PENDING",
        )
        self.api = APIClient()

    def _count(self, user, key):
        self.api.force_authenticate(user=user)
        resp = self.api.get(
            "/api/v1/action_center/", HTTP_X_TENANT_ID=str(self.tenant.pk)
        )
        assert resp.status_code == 200
        actions = resp.json()["data"]["actions"]
        match = next((a for a in actions if a["key"] == key), None)
        return match["count"] if match else 0

    def test_pm_only_counts_own_projects(self):
        assert self._count(self.pm, "timesheets_to_approve") == 1

    def test_admin_counts_tenant_wide(self):
        from apps.core.models import ProjectRole, Role

        admin = User.objects.create_user("ac_admin", password="x")
        ProjectRole.objects.create(user=admin, tenant=self.tenant, role=Role.ADMIN)
        assert self._count(admin, "timesheets_to_approve") == 2
