"""Tests for Planning module."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Phase, Project, Task

from .models import Milestone, PlanningStandard, ResourceAllocation


@pytest.mark.django_db
class TestResourceAllocationAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Plan", slug="plan-test")
        self.pm = User.objects.create_user(username="plan_pm", password="pass123!")
        self.emp = User.objects.create_user(username="plan_emp", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant, code="PL-01", name="Planning Test",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project,
            code="ESQUISSE", name="Esquisse", order=1,
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def test_create_allocation(self):
        resp = self.api.post("/api/v1/allocations/", {
            "employee": self.emp.pk,
            "project": self.project.pk,
            "phase": self.phase.pk,
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
            phase=self.phase,
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
            phase=self.phase,
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
        self.project = Project.objects.create(
            tenant=self.tenant, code="ML-01", name="Milestone Test",
        )
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


@pytest.mark.django_db
class TestAllocationXORValidation:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Xor", slug="xor-test")
        self.pm = User.objects.create_user(username="xor_pm", password="pass123!")
        self.emp = User.objects.create_user(username="xor_emp", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant, code="XR-01", name="XOR Test",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project,
            code="ESQUISSE", name="Esquisse", order=1,
        )
        self.task = Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            wbs_code="1.1", name="Sous-tache 1",
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def _make(self, **overrides):
        return ResourceAllocation(
            tenant=self.tenant, employee=self.emp, project=self.project,
            start_date=date(2026, 5, 4), end_date=date(2026, 5, 31),
            hours_per_week=20, created_by=self.pm,
            **overrides,
        )

    def test_phase_only_is_valid(self):
        alloc = self._make(phase=self.phase)
        alloc.full_clean()  # does not raise

    def test_task_only_is_valid(self):
        alloc = self._make(task=self.task)
        alloc.full_clean()

    def test_both_phase_and_task_raises(self):
        alloc = self._make(phase=self.phase, task=self.task)
        with pytest.raises(ValidationError) as exc:
            alloc.full_clean()
        assert "exactly one" in str(exc.value)

    def test_neither_phase_nor_task_raises(self):
        alloc = self._make()
        with pytest.raises(ValidationError) as exc:
            alloc.full_clean()
        assert "exactly one" in str(exc.value)

    def test_save_enforces_xor_bypass_orm(self):
        """save() override calls full_clean — blocks shell/ORM bypass."""
        with pytest.raises(ValidationError):
            self._make(phase=self.phase, task=self.task).save()

    def test_save_clears_stale_time_breakdown_when_not_manual(self):
        alloc = self._make(
            phase=self.phase,
            distribution_mode="uniform",
            time_breakdown={"2026-W18": 10},
        )
        alloc.save()
        alloc.refresh_from_db()
        assert alloc.time_breakdown is None

    def test_api_rejects_both_set(self):
        resp = self.api.post("/api/v1/allocations/", {
            "employee": self.emp.pk,
            "project": self.project.pk,
            "phase": self.phase.pk,
            "task": self.task.pk,
            "start_date": "2026-05-04", "end_date": "2026-05-31",
            "hours_per_week": 20,
        }, format="json")
        assert resp.status_code == 400

    def test_api_rejects_neither_set(self):
        resp = self.api.post("/api/v1/allocations/", {
            "employee": self.emp.pk,
            "project": self.project.pk,
            "start_date": "2026-05-04", "end_date": "2026-05-31",
            "hours_per_week": 20,
        }, format="json")
        assert resp.status_code == 400


@pytest.mark.django_db
class TestTotalPlannedHoursModes:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Tot", slug="tot-test")
        self.pm = User.objects.create_user(username="tot_pm", password="pass123!")
        self.emp = User.objects.create_user(username="tot_emp", password="pass123!")
        self.project = Project.objects.create(
            tenant=self.tenant, code="TT-01", name="Total Test",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project,
            code="APS", name="APS", order=1,
        )

    def _build(self, **overrides):
        return ResourceAllocation(
            tenant=self.tenant, employee=self.emp, project=self.project,
            phase=self.phase,
            start_date=date(2026, 5, 4), end_date=date(2026, 7, 12),  # ~10 weeks
            hours_per_week=20, created_by=self.pm,
            **overrides,
        )

    def test_uniform_computes_weeks_times_rate(self):
        alloc = self._build(distribution_mode="uniform")
        alloc.save()
        assert alloc.total_weeks == 10
        assert alloc.total_planned_hours == 200.0

    def test_manual_sums_time_breakdown(self):
        alloc = self._build(
            distribution_mode="manual",
            time_breakdown={"2026-W19": 10, "2026-W20": 15},
        )
        alloc.save()
        assert alloc.total_planned_hours == 25.0

    def test_standard_falls_back_to_uniform(self):
        """Sprint 1: standard mode has no breakdown yet → uniform fallback."""
        alloc = self._build(distribution_mode="standard")
        alloc.save()
        assert alloc.total_planned_hours == 200.0

    def test_manual_empty_dict_returns_zero(self):
        alloc = self._build(distribution_mode="manual", time_breakdown={})
        alloc.save()
        assert alloc.total_planned_hours == 0.0

    def test_manual_none_returns_zero(self):
        alloc = self._build(distribution_mode="manual", time_breakdown=None)
        alloc.save()
        assert alloc.total_planned_hours == 0.0


@pytest.mark.django_db
class TestPlanningStandardAPI:
    def setup_method(self):
        self.tenant_a = Tenant.objects.create(name="TA", slug="ta")
        self.tenant_b = Tenant.objects.create(name="TB", slug="tb")
        self.user_a = User.objects.create_user(username="psa", password="pass123!")
        self.user_b = User.objects.create_user(username="psb", password="pass123!")
        ProjectRole.objects.create(user=self.user_a, tenant=self.tenant_a, role=Role.PM)
        ProjectRole.objects.create(user=self.user_b, tenant=self.tenant_b, role=Role.PM)
        self.api_a = APIClient(HTTP_X_TENANT_ID=str(self.tenant_a.pk))
        self.api_a.force_authenticate(user=self.user_a)
        self.api_b = APIClient(HTTP_X_TENANT_ID=str(self.tenant_b.pk))
        self.api_b.force_authenticate(user=self.user_b)

    def _post_a(self, **payload):
        return self.api_a.post("/api/v1/planning-standards/", {
            "name": "Front-loaded",
            "phase_code": "ESQUISSE",
            "time_unit": "week",
            "curve": [0.4, 0.3, 0.2, 0.1],
            **payload,
        }, format="json")

    def test_create_valid_curve(self):
        resp = self._post_a()
        assert resp.status_code == 201
        data = resp.json().get("data", resp.json())
        assert data["phase_code"] == "ESQUISSE"

    def test_factory_allocation_defaults_to_uniform_week(self):
        """Task 17b — migration regression: new rows adopt field defaults."""
        phase = Phase.objects.create(
            tenant=self.tenant_a, project=Project.objects.create(
                tenant=self.tenant_a, code="PS-REG", name="Reg",
            ), code="ESQ", name="Esq", order=1,
        )
        alloc = ResourceAllocation.objects.create(
            tenant=self.tenant_a, employee=self.user_a,
            project=phase.project, phase=phase,
            start_date=date(2026, 5, 4), end_date=date(2026, 5, 31),
            hours_per_week=20, created_by=self.user_a,
        )
        assert alloc.distribution_mode == "uniform"
        assert alloc.time_unit == "week"

    def test_reject_curve_sum_not_one(self):
        resp = self._post_a(curve=[0.5, 0.5, 0.5])
        assert resp.status_code == 400
        body = resp.json()
        err = body.get("errors") or body.get("data") or body
        # Find the curve error regardless of wrap style.
        flat = str(err)
        assert "1.0" in flat

    def test_reject_non_list_curve(self):
        resp = self._post_a(curve="not-a-list")
        assert resp.status_code == 400

    def test_filter_by_phase_code(self):
        self._post_a(phase_code="ESQUISSE")
        self._post_a(name="APS-std", phase_code="APS")
        resp = self.api_a.get("/api/v1/planning-standards/?phase_code=ESQUISSE")
        assert resp.status_code == 200
        body = resp.json()
        items = body.get("data") or body.get("results") or body
        if isinstance(items, dict) and "results" in items:
            items = items["results"]
        assert all(it["phase_code"] == "ESQUISSE" for it in items)
        assert len(items) >= 1

    def test_tenant_isolation(self):
        # Tenant A creates one
        PlanningStandard.objects.create(
            tenant=self.tenant_a, name="A-only",
            phase_code="ESQUISSE", time_unit="week",
            curve=[0.5, 0.5],
        )
        # Tenant B creates another
        PlanningStandard.objects.create(
            tenant=self.tenant_b, name="B-only",
            phase_code="ESQUISSE", time_unit="week",
            curve=[0.5, 0.5],
        )
        # A sees only its own
        resp = self.api_a.get("/api/v1/planning-standards/")
        body = resp.json()
        items = body.get("data") or body.get("results") or body
        if isinstance(items, dict) and "results" in items:
            items = items["results"]
        names = {it["name"] for it in items}
        assert "A-only" in names
        assert "B-only" not in names
