"""Tests for the projects serializers — validation, computed fields,
optimistic locking and cost-field filtering.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from apps.core.mixins import VersionConflictError
from apps.core.models import ProjectRole, Role
from apps.projects.serializers import (
    AmendmentSerializer,
    FinancialPhaseSerializer,
    PhaseSerializer,
    ProjectListSerializer,
    ProjectSerializer,
    ProjectTemplateSerializer,
    SupportServiceSerializer,
    TaskSerializer,
    WBSElementSerializer,
)

from .conftest import (
    AmendmentFactory,
    PhaseFactory,
    ProjectFactory,
    ProjectTemplateFactory,
    TaskFactory,
    UserFactory,
)


def _request_with_user(user):
    """Build a DRF request tied to ``user`` for serializer contexts."""

    rf = APIRequestFactory()
    raw = rf.get("/")
    raw.user = user
    req = Request(raw)
    req.user = user
    return req


# --------------------------------------------------------------------------- #
# TaskSerializer
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestTaskSerializer:
    def test_end_date_must_be_on_or_after_start_date(self, project, phase):
        data = {
            "project": project.pk,
            "phase": phase.pk,
            "wbs_code": "1.1",
            "name": "T",
            "start_date": "2026-06-10",
            "end_date": "2026-06-05",
        }
        s = TaskSerializer(data=data)
        assert not s.is_valid()
        assert "end_date" in s.errors

    def test_end_date_equal_start_date_is_valid(self, project, phase):
        data = {
            "project": project.pk,
            "phase": phase.pk,
            "wbs_code": "1.2",
            "name": "T",
            "start_date": "2026-06-10",
            "end_date": "2026-06-10",
        }
        s = TaskSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_display_label_uses_client_facing_label(self, project, phase):
        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="1.3",
            name="Technical",
            client_facing_label="Client facing",
        )
        data = TaskSerializer(task).data
        assert data["display_label"] == "Client facing"
        assert data["phase_name"] == phase.name

    def test_display_label_falls_back_to_name(self, project, phase):
        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="1.4",
            name="Raw name",
            client_facing_label="",
        )
        data = TaskSerializer(task).data
        assert data["display_label"] == "Raw name"

    def test_update_preserves_existing_start_date(self, project, phase):
        """Partial update where start_date is absent must reuse instance.start_date."""
        from datetime import date

        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="1.5",
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 30),
        )
        s = TaskSerializer(task, data={"end_date": "2026-05-31"}, partial=True)
        assert not s.is_valid()
        assert "end_date" in s.errors

    def test_amendment_exposed_as_null_by_default(self, project, phase):
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="2.1")
        data = TaskSerializer(task).data
        assert "amendment" in data
        assert data["amendment"] is None

    def test_amendment_exposed_when_task_attached(self, project, phase):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.1",
            amendment=amd,
        )
        data = TaskSerializer(task).data
        assert data["amendment"] == amd.pk

    def test_amendment_writable_on_create(self, project, phase):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        s = TaskSerializer(
            data={
                "project": project.pk,
                "phase": phase.pk,
                "wbs_code": "AV1.2",
                "name": "Task avenant",
                "amendment": amd.pk,
            }
        )
        assert s.is_valid(), s.errors
        task = s.save(tenant=project.tenant)
        assert task.amendment_id == amd.pk

    def test_amendment_patchable_on_existing_task(self, project, phase):
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="2.2")
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        s = TaskSerializer(task, data={"amendment": amd.pk}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        task.refresh_from_db()
        assert task.amendment_id == amd.pk


# --------------------------------------------------------------------------- #
# PhaseSerializer (aggregation fields)
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestPhaseSerializer:
    def test_computed_hours_with_no_tasks_returns_zero(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant)
        data = PhaseSerializer(phase).data
        assert data["tasks_budgeted_hours"] == 0
        assert data["planned_hours"] == 0
        assert data["actual_hours"] == 0

    def test_tasks_budgeted_hours_sums_tasks(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant)
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="3.1",
            budgeted_hours=Decimal("10.00"),
        )
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="3.2",
            budgeted_hours=Decimal("15.50"),
        )
        data = PhaseSerializer(phase).data
        assert data["tasks_budgeted_hours"] == 25.5

    def test_amendment_exposed_as_null_by_default(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant)
        data = PhaseSerializer(phase).data
        assert "amendment" in data
        assert data["amendment"] is None

    def test_amendment_exposed_when_phase_attached(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        phase = PhaseFactory(project=project, tenant=project.tenant, amendment=amd)
        data = PhaseSerializer(phase).data
        assert data["amendment"] == amd.pk

    def test_amendment_writable_on_create(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        s = PhaseSerializer(
            data={
                "name": "Phase ajoutee par avenant",
                "amendment": amd.pk,
                "budgeted_hours": "10.00",
            }
        )
        assert s.is_valid(), s.errors
        phase = s.save(project=project, tenant=project.tenant)
        assert phase.amendment_id == amd.pk

    def test_amendment_patchable_on_existing_phase(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant)
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        s = PhaseSerializer(phase, data={"amendment": amd.pk}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        phase.refresh_from_db()
        assert phase.amendment_id == amd.pk

    def test_amendment_can_be_cleared_via_patch(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        phase = PhaseFactory(project=project, tenant=project.tenant, amendment=amd)
        s = PhaseSerializer(phase, data={"amendment": None}, partial=True)
        assert s.is_valid(), s.errors
        s.save()
        phase.refresh_from_db()
        assert phase.amendment_id is None


# --------------------------------------------------------------------------- #
# ProjectSerializer — cost-field filtering + optimistic lock
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestProjectSerializerCostFilter:
    def test_cost_fields_hidden_for_employee(self, project):
        user = UserFactory()
        ProjectRole.objects.create(user=user, tenant=project.tenant, role=Role.EMPLOYEE)
        s = ProjectSerializer(project, context={"request": _request_with_user(user)})
        assert "construction_cost" not in s.data

    def test_cost_fields_visible_for_pm(self, project):
        user = UserFactory()
        ProjectRole.objects.create(user=user, tenant=project.tenant, role=Role.PM)
        s = ProjectSerializer(project, context={"request": _request_with_user(user)})
        assert "construction_cost" in s.data

    def test_cost_fields_present_for_unauthenticated_context(self, project):
        """Without an authenticated request the mixin leaves fields untouched."""
        from django.contrib.auth.models import AnonymousUser

        rf = APIRequestFactory()
        raw = rf.get("/")
        raw.user = AnonymousUser()
        req = Request(raw)
        req.user = AnonymousUser()
        s = ProjectSerializer(project, context={"request": req})
        assert "construction_cost" in s.data


@pytest.mark.django_db
class TestProjectSerializerOptimisticLock:
    def test_version_mismatch_raises_conflict(self, project):
        project.name = "Advanced by another session"
        project.save()
        # Current DB version is 2 (incremented by save); client sends 1.
        s = ProjectSerializer(
            project,
            data={"name": "Mine"},
            partial=True,
            context={"if_match_version": "1"},
        )
        assert s.is_valid(), s.errors
        with pytest.raises(VersionConflictError) as excinfo:
            s.save()
        assert excinfo.value.status_code == 409

    def test_version_match_saves_successfully(self, project):
        # Fresh project has version 1.
        s = ProjectSerializer(
            project,
            data={"name": "Renamed"},
            partial=True,
            context={"if_match_version": str(project.version)},
        )
        assert s.is_valid(), s.errors
        s.save()
        project.refresh_from_db()
        assert project.name == "Renamed"
        assert project.version == 2

    def test_version_in_payload_falls_back_when_header_missing(self, project):
        s = ProjectSerializer(
            project,
            data={"name": "Patched", "version": project.version},
            partial=True,
        )
        assert s.is_valid(), s.errors
        s.save()
        project.refresh_from_db()
        assert project.name == "Patched"

    def test_invalid_version_header_is_ignored(self, project):
        s = ProjectSerializer(
            project,
            data={"name": "Bypass"},
            partial=True,
            context={"if_match_version": "not-a-number"},
        )
        assert s.is_valid(), s.errors
        # Invalid header → no lock enforced → save succeeds
        s.save()
        project.refresh_from_db()
        assert project.name == "Bypass"


# --------------------------------------------------------------------------- #
# ProjectListSerializer — computed fields
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestProjectListSerializer:
    def test_pm_name_uses_full_name(self, tenant):
        pm = UserFactory(first_name="Alice", last_name="Martin")
        p = ProjectFactory(tenant=tenant, pm=pm)
        data = ProjectListSerializer(p).data
        assert data["pm_name"] == "Alice Martin"

    def test_pm_name_falls_back_to_username(self, tenant):
        pm = UserFactory(first_name="", last_name="", username="bob42")
        p = ProjectFactory(tenant=tenant, pm=pm)
        data = ProjectListSerializer(p).data
        assert data["pm_name"] == "bob42"

    def test_pm_name_empty_when_no_pm(self, project):
        data = ProjectListSerializer(project).data
        assert data["pm_name"] == ""

    def test_active_phase_returns_first_non_locked_realization(self, project):
        PhaseFactory(
            project=project,
            tenant=project.tenant,
            name="Locked",
            phase_type="REALIZATION",
            is_locked=True,
            order=0,
        )
        PhaseFactory(
            project=project,
            tenant=project.tenant,
            name="Active",
            phase_type="REALIZATION",
            is_locked=False,
            order=1,
        )
        data = ProjectListSerializer(project).data
        assert data["active_phase"] == "Active"

    def test_active_phase_empty_when_no_realization_phase(self, project):
        PhaseFactory(
            project=project,
            tenant=project.tenant,
            phase_type="SUPPORT",
            is_locked=False,
        )
        data = ProjectListSerializer(project).data
        assert data["active_phase"] == ""

    def test_budget_hours_prefers_tasks_over_phases(self, project):
        phase = PhaseFactory(
            project=project,
            tenant=project.tenant,
            budgeted_hours=Decimal("99"),
        )
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="4.1",
            budgeted_hours=Decimal("12.5"),
        )
        data = ProjectListSerializer(project).data
        assert data["budget_hours"] == 12.5

    def test_budget_hours_falls_back_to_phases_when_no_tasks(self, project):
        PhaseFactory(project=project, tenant=project.tenant, budgeted_hours=Decimal("42.00"))
        data = ProjectListSerializer(project).data
        assert data["budget_hours"] == 42.0

    def test_budget_hours_zero_when_no_data(self, project):
        data = ProjectListSerializer(project).data
        assert data["budget_hours"] == 0

    def test_total_invoiced_zero_when_no_invoices(self, project):
        data = ProjectListSerializer(project).data
        assert data["total_invoiced"] == 0


# --------------------------------------------------------------------------- #
# AmendmentSerializer — optimistic lock
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestAmendmentSerializer:
    def test_optimistic_lock_on_amendment_update(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        amd.description = "Bumped elsewhere"
        amd.save()
        s = AmendmentSerializer(
            amd,
            data={"description": "Mine"},
            partial=True,
            context={"if_match_version": "1"},
        )
        assert s.is_valid(), s.errors
        with pytest.raises(VersionConflictError):
            s.save()


# --------------------------------------------------------------------------- #
# Lightweight serializers — field presence / meta
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestLightweightSerializers:
    def test_wbs_element_serializer_returns_empty_children(self, project):
        from apps.projects.models import WBSElement

        elem = WBSElement.objects.create(
            tenant=project.tenant, project=project, standard_label="Root"
        )
        data = WBSElementSerializer(elem).data
        assert data["children"] == []
        assert data["standard_label"] == "Root"

    def test_support_service_serializer_fields(self, project):
        from apps.projects.models import SupportService

        svc = SupportService.objects.create(tenant=project.tenant, project=project, name="BIM")
        data = SupportServiceSerializer(svc).data
        assert data["name"] == "BIM"
        assert data["is_billable"] is True

    def test_project_template_serializer_exposes_projects_count(self, tenant):
        tmpl = ProjectTemplateFactory(tenant=tenant)
        data = ProjectTemplateSerializer(tmpl).data
        assert data["projects_count"] == 0

    def test_financial_phase_serializer_shape(self, project):
        from apps.projects.models import FinancialPhase

        fp = FinancialPhase.objects.create(tenant=project.tenant, project=project, name="F1")
        data = FinancialPhaseSerializer(fp).data
        assert set(data.keys()) == {
            "id",
            "name",
            "code",
            "billing_mode",
            "fixed_amount",
            "hourly_budget_max",
        }
