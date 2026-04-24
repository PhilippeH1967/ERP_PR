"""Tests for Planning module."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Phase, Project, Task

from .models import Milestone, PlanningStandard, ResourceAllocation, VirtualResource


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


@pytest.mark.django_db
class TestVirtualResourceModel:
    """Modèle VirtualResource: profils fictifs rattachés à un projet."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Vr", slug="vr-test")
        self.project = Project.objects.create(
            tenant=self.tenant, code="VR-01", name="Virtual Resource Test",
        )

    def test_create_with_required_fields(self):
        vr = VirtualResource.objects.create(
            tenant=self.tenant, project=self.project,
            name="Architecte senior",
        )
        assert vr.pk is not None
        assert vr.default_hourly_rate == 0
        assert vr.is_active is True

    def test_create_with_default_hourly_rate(self):
        vr = VirtualResource.objects.create(
            tenant=self.tenant, project=self.project,
            name="Dessinateur junior",
            default_hourly_rate="55.50",
        )
        assert float(vr.default_hourly_rate) == 55.50

    def test_unique_name_per_project(self):
        from django.db.utils import IntegrityError
        VirtualResource.objects.create(
            tenant=self.tenant, project=self.project, name="Chef de projet",
        )
        with pytest.raises(IntegrityError):
            VirtualResource.objects.create(
                tenant=self.tenant, project=self.project, name="Chef de projet",
            )

    def test_same_name_on_different_project_allowed(self):
        other = Project.objects.create(
            tenant=self.tenant, code="VR-02", name="Other",
        )
        VirtualResource.objects.create(
            tenant=self.tenant, project=self.project, name="Chef de projet",
        )
        # Should not raise
        VirtualResource.objects.create(
            tenant=self.tenant, project=other, name="Chef de projet",
        )


@pytest.mark.django_db
class TestResourceAllocationVirtualXOR:
    """ResourceAllocation accepte employee OU virtual_resource, pas les deux, pas aucun."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Vrx", slug="vrx-test")
        self.pm = User.objects.create_user(username="vrx_pm", password="pass123!")
        self.emp = User.objects.create_user(username="vrx_emp", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant, code="VX-01", name="Virtual XOR",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project,
            code="ESQUISSE", name="Esquisse", order=1,
        )
        self.virtual = VirtualResource.objects.create(
            tenant=self.tenant, project=self.project, name="Architecte junior",
        )

    def _make(self, **overrides):
        return ResourceAllocation(
            tenant=self.tenant, project=self.project, phase=self.phase,
            start_date=date(2026, 5, 4), end_date=date(2026, 5, 31),
            hours_per_week=20, created_by=self.pm,
            **overrides,
        )

    def test_virtual_only_is_valid(self):
        alloc = self._make(virtual_resource=self.virtual)
        alloc.full_clean()  # does not raise

    def test_both_employee_and_virtual_raises(self):
        alloc = self._make(employee=self.emp, virtual_resource=self.virtual)
        with pytest.raises(ValidationError) as exc:
            alloc.full_clean()
        assert "exactly one" in str(exc.value) or "employee" in str(exc.value)

    def test_neither_employee_nor_virtual_raises(self):
        alloc = self._make()
        with pytest.raises(ValidationError):
            alloc.full_clean()

    def test_virtual_allocation_persists(self):
        alloc = self._make(virtual_resource=self.virtual)
        alloc.save()
        alloc.refresh_from_db()
        assert alloc.virtual_resource_id == self.virtual.pk
        assert alloc.employee_id is None


@pytest.mark.django_db
class TestVirtualResourceAPI:
    """API CRUD + filtrage + isolation tenant pour VirtualResource."""

    def setup_method(self):
        self.tenant_a = Tenant.objects.create(name="VrA", slug="vra")
        self.tenant_b = Tenant.objects.create(name="VrB", slug="vrb")
        self.user_a = User.objects.create_user(username="vra_u", password="pass123!")
        self.user_b = User.objects.create_user(username="vrb_u", password="pass123!")
        ProjectRole.objects.create(user=self.user_a, tenant=self.tenant_a, role=Role.PM)
        ProjectRole.objects.create(user=self.user_b, tenant=self.tenant_b, role=Role.PM)
        self.project_a = Project.objects.create(
            tenant=self.tenant_a, code="VA-01", name="A",
        )
        self.project_b = Project.objects.create(
            tenant=self.tenant_b, code="VB-01", name="B",
        )
        self.api_a = APIClient(HTTP_X_TENANT_ID=str(self.tenant_a.pk))
        self.api_a.force_authenticate(user=self.user_a)
        self.api_b = APIClient(HTTP_X_TENANT_ID=str(self.tenant_b.pk))
        self.api_b.force_authenticate(user=self.user_b)

    def test_create_virtual_resource(self):
        resp = self.api_a.post("/api/v1/virtual-resources/", {
            "project": self.project_a.pk,
            "name": "Architecte senior",
            "default_hourly_rate": "85.00",
        }, format="json")
        assert resp.status_code == 201, resp.content
        data = resp.json().get("data", resp.json())
        assert data["name"] == "Architecte senior"
        assert float(data["default_hourly_rate"]) == 85.0

    def test_requires_authentication(self):
        anon = APIClient()
        resp = anon.post("/api/v1/virtual-resources/", {
            "project": self.project_a.pk, "name": "X",
        }, format="json")
        assert resp.status_code in (401, 403)

    def test_filter_by_project(self):
        VirtualResource.objects.create(
            tenant=self.tenant_a, project=self.project_a, name="P1-role",
        )
        other = Project.objects.create(
            tenant=self.tenant_a, code="VA-02", name="Other A",
        )
        VirtualResource.objects.create(
            tenant=self.tenant_a, project=other, name="P2-role",
        )
        resp = self.api_a.get(f"/api/v1/virtual-resources/?project={self.project_a.pk}")
        assert resp.status_code == 200
        body = resp.json()
        items = body.get("data") or body.get("results") or body
        if isinstance(items, dict) and "results" in items:
            items = items["results"]
        names = {it["name"] for it in items}
        assert names == {"P1-role"}

    def test_tenant_isolation(self):
        VirtualResource.objects.create(
            tenant=self.tenant_a, project=self.project_a, name="A-virtual",
        )
        VirtualResource.objects.create(
            tenant=self.tenant_b, project=self.project_b, name="B-virtual",
        )
        resp = self.api_a.get("/api/v1/virtual-resources/")
        body = resp.json()
        items = body.get("data") or body.get("results") or body
        if isinstance(items, dict) and "results" in items:
            items = items["results"]
        names = {it["name"] for it in items}
        assert "A-virtual" in names
        assert "B-virtual" not in names


@pytest.mark.django_db
class TestAllocationAPIWithVirtual:
    """API Allocation : accepter virtual_resource au lieu d'employee."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Avr", slug="avr-test")
        self.pm = User.objects.create_user(username="avr_pm", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant, code="AV-01", name="Alloc Virtual",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project,
            code="ESQUISSE", name="Esquisse", order=1,
        )
        self.virtual = VirtualResource.objects.create(
            tenant=self.tenant, project=self.project, name="Architecte principal",
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def test_create_allocation_with_virtual_resource(self):
        resp = self.api.post("/api/v1/allocations/", {
            "virtual_resource": self.virtual.pk,
            "project": self.project.pk,
            "phase": self.phase.pk,
            "start_date": "2026-04-06",
            "end_date": "2026-06-26",
            "hours_per_week": 20,
        }, format="json")
        assert resp.status_code == 201, resp.content
        data = resp.json().get("data", resp.json())
        assert data["virtual_resource"] == self.virtual.pk
        assert data["employee"] is None

    def test_create_allocation_rejects_both_employee_and_virtual(self):
        emp = User.objects.create_user(username="avr_emp", password="pass123!")
        resp = self.api.post("/api/v1/allocations/", {
            "employee": emp.pk,
            "virtual_resource": self.virtual.pk,
            "project": self.project.pk,
            "phase": self.phase.pk,
            "start_date": "2026-04-06",
            "end_date": "2026-06-26",
            "hours_per_week": 20,
        }, format="json")
        assert resp.status_code == 400

    def test_create_allocation_rejects_neither_employee_nor_virtual(self):
        resp = self.api.post("/api/v1/allocations/", {
            "project": self.project.pk,
            "phase": self.phase.pk,
            "start_date": "2026-04-06",
            "end_date": "2026-06-26",
            "hours_per_week": 20,
        }, format="json")
        assert resp.status_code == 400


@pytest.mark.django_db
class TestVirtualResourceReplaceWithEmployee:
    """Action POST /virtual-resources/{id}/replace_with_employee/.

    Toutes les allocations du profil virtuel sont réassignées à l'employé,
    et le profil virtuel est désactivé (is_active=False).
    """

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Rep", slug="rep-test")
        self.pm = User.objects.create_user(username="rep_pm", password="pass123!")
        self.emp = User.objects.create_user(username="rep_emp", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant, code="RP-01", name="Replace",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project,
            code="ESQUISSE", name="Esquisse", order=1,
        )
        self.virtual = VirtualResource.objects.create(
            tenant=self.tenant, project=self.project, name="Architecte senior",
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def _make_alloc(self):
        return ResourceAllocation.objects.create(
            tenant=self.tenant, virtual_resource=self.virtual,
            project=self.project, phase=self.phase,
            start_date=date(2026, 5, 4), end_date=date(2026, 5, 31),
            hours_per_week=20, created_by=self.pm,
        )

    def test_replaces_all_allocations_and_deactivates_virtual(self):
        a1 = self._make_alloc()
        a2 = self._make_alloc()
        resp = self.api.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {"employee": self.emp.pk}, format="json",
        )
        assert resp.status_code == 200, resp.content
        data = resp.json().get("data", resp.json())
        assert data["replaced_count"] == 2

        a1.refresh_from_db()
        a2.refresh_from_db()
        self.virtual.refresh_from_db()
        assert a1.employee_id == self.emp.pk
        assert a1.virtual_resource_id is None
        assert a2.employee_id == self.emp.pk
        assert a2.virtual_resource_id is None
        assert self.virtual.is_active is False

    def test_missing_employee_returns_400(self):
        resp = self.api.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {}, format="json",
        )
        assert resp.status_code == 400

    def test_invalid_employee_returns_400(self):
        resp = self.api.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {"employee": 999_999}, format="json",
        )
        assert resp.status_code == 400

    def test_unauthenticated_returns_401(self):
        anon = APIClient()
        resp = anon.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {"employee": self.emp.pk}, format="json",
        )
        assert resp.status_code in (401, 403)

    def test_replacement_tracks_who_and_when(self):
        """Après remplacement, le virtuel mémorise l'employé remplaçant et la date."""
        self._make_alloc()
        resp = self.api.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {"employee": self.emp.pk}, format="json",
        )
        assert resp.status_code == 200, resp.content
        self.virtual.refresh_from_db()
        assert self.virtual.is_active is False
        assert self.virtual.replaced_by_id == self.emp.pk
        assert self.virtual.replaced_at is not None

    def test_inactive_virtual_returned_by_list_endpoint(self):
        """L'endpoint liste retourne aussi les virtuels inactifs pour historique."""
        self._make_alloc()
        self.api.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {"employee": self.emp.pk}, format="json",
        )
        resp = self.api.get(
            f"/api/v1/virtual-resources/?project={self.project.pk}",
        )
        assert resp.status_code == 200
        payload = resp.json().get("data", resp.json())
        results = payload.get("results", payload) if isinstance(payload, dict) else payload
        ids = [v["id"] for v in results]
        assert self.virtual.pk in ids, "Le virtuel inactif doit être listé"

    def test_serializer_exposes_replaced_by_name(self):
        """Le serializer expose replaced_by_name pour affichage UI."""
        self._make_alloc()
        self.emp.first_name = "Alice"
        self.emp.last_name = "Martin"
        self.emp.save()
        self.api.post(
            f"/api/v1/virtual-resources/{self.virtual.pk}/replace_with_employee/",
            {"employee": self.emp.pk}, format="json",
        )
        resp = self.api.get(f"/api/v1/virtual-resources/{self.virtual.pk}/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data.get("replaced_by_name") in ("Alice Martin", self.emp.username)
