"""Tests for Planning module."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Project

from .models import Milestone, ResourceAllocation


@pytest.mark.django_db
class TestResourceAllocationAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Plan", slug="plan-test")
        self.pm = User.objects.create_user(username="plan_pm", password="pass123!")
        self.emp = User.objects.create_user(username="plan_emp", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(tenant=self.tenant, code="PL-01", name="Planning Test")
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def test_create_allocation(self):
        resp = self.api.post("/api/v1/allocations/", {
            "employee": self.emp.pk,
            "project": self.project.pk,
            "start_date": "2026-04-06",
            "end_date": "2026-06-26",
            "hours_per_week": 20,
        }, format="json")
        assert resp.status_code == 201
        data = resp.json().get("data", resp.json())
        assert float(data["hours_per_week"]) == 20.0

    def test_global_planning(self):
        ResourceAllocation.objects.create(
            tenant=self.tenant, employee=self.emp, project=self.project,
            start_date=date(2026, 4, 6), end_date=date(2026, 6, 26),
            hours_per_week=35, created_by=self.pm,
        )
        resp = self.api.get("/api/v1/allocations/global_planning/", {
            "start_date": "2026-04-01", "end_date": "2026-04-30",
        })
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert len(data["employees"]) == 1
        assert data["employees"][0]["load_percent"] > 0

    def test_load_alerts_overload(self):
        ResourceAllocation.objects.create(
            tenant=self.tenant, employee=self.emp, project=self.project,
            start_date=date(2026, 4, 6), end_date=date(2026, 12, 31),
            hours_per_week=50, created_by=self.pm,
        )
        resp = self.api.get("/api/v1/allocations/load_alerts/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        alerts = data["alerts"]
        assert len(alerts) >= 1
        assert alerts[0]["alert_type"] in ("overload", "critical")


@pytest.mark.django_db
class TestMilestoneAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Mile", slug="mile-test")
        self.user = User.objects.create_user(username="mile_user", password="pass123!")
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(tenant=self.tenant, code="ML-01", name="Milestone Test")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_create_milestone(self):
        resp = self.api.post("/api/v1/milestones/", {
            "project": self.project.pk,
            "title": "Livraison phase 1",
            "date": "2026-06-15",
        }, format="json")
        assert resp.status_code == 201

    def test_auto_update_overdue(self):
        Milestone.objects.create(
            tenant=self.tenant, project=self.project,
            title="Old milestone", date=date(2025, 1, 1), status="UPCOMING",
        )
        resp = self.api.post("/api/v1/milestones/auto_update_status/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["updated_to_overdue"] >= 1
