"""Tests for amendment state-machine workflow (story 12.1 Phase A).

Covers:
- Service submit/approve/reject with @transaction.atomic
- Permission: only PROJECT_DIRECTOR (Associé en charge) approves/rejects
- Invalid state transitions raise
- HistoricalRecords captures actor on each transition
- ViewSet actions /submit/ /approve/ /reject/
"""

from __future__ import annotations

import pytest

from apps.core.models import ProjectRole, Role
from apps.projects.models import Amendment
from apps.projects.services import (
    AmendmentTransitionError,
    approve_amendment,
    reject_amendment,
    submit_amendment,
)

from .conftest import AmendmentFactory, UserFactory

# --------------------------------------------------------------------------- #
# Service layer — state machine
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestSubmitAmendment:
    def test_submit_draft_moves_to_submitted(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
        )
        user = UserFactory()
        result = submit_amendment(amd, actor=user)
        assert result.status == Amendment.AmendmentStatus.SUBMITTED
        amd.refresh_from_db()
        assert amd.status == Amendment.AmendmentStatus.SUBMITTED

    def test_submit_already_submitted_raises(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        with pytest.raises(AmendmentTransitionError):
            submit_amendment(amd, actor=UserFactory())

    def test_submit_approved_raises(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
        )
        with pytest.raises(AmendmentTransitionError):
            submit_amendment(amd, actor=UserFactory())


@pytest.mark.django_db
class TestApproveAmendment:
    def test_project_director_approves_submitted_amendment(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        director = UserFactory()
        ProjectRole.objects.create(
            user=director,
            tenant=project.tenant,
            role=Role.PROJECT_DIRECTOR,
        )
        result = approve_amendment(amd, actor=director)
        assert result.status == Amendment.AmendmentStatus.APPROVED
        assert result.approved_by_id == director.pk
        assert result.approval_date is not None

    def test_pm_cannot_approve(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        pm = UserFactory()
        ProjectRole.objects.create(user=pm, tenant=project.tenant, role=Role.PM)
        with pytest.raises(PermissionError):
            approve_amendment(amd, actor=pm)

    def test_finance_cannot_approve(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        finance = UserFactory()
        ProjectRole.objects.create(user=finance, tenant=project.tenant, role=Role.FINANCE)
        with pytest.raises(PermissionError):
            approve_amendment(amd, actor=finance)

    def test_dept_assistant_cannot_approve(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        assistant = UserFactory()
        ProjectRole.objects.create(
            user=assistant,
            tenant=project.tenant,
            role=Role.DEPT_ASSISTANT,
        )
        with pytest.raises(PermissionError):
            approve_amendment(amd, actor=assistant)

    def test_cannot_approve_draft(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
        )
        director = UserFactory()
        ProjectRole.objects.create(
            user=director,
            tenant=project.tenant,
            role=Role.PROJECT_DIRECTOR,
        )
        with pytest.raises(AmendmentTransitionError):
            approve_amendment(amd, actor=director)


@pytest.mark.django_db
class TestRejectAmendment:
    def test_project_director_rejects_submitted_amendment(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        director = UserFactory()
        ProjectRole.objects.create(
            user=director,
            tenant=project.tenant,
            role=Role.PROJECT_DIRECTOR,
        )
        result = reject_amendment(amd, actor=director, reason="Budget insuffisant")
        assert result.status == Amendment.AmendmentStatus.REJECTED

    def test_pm_cannot_reject(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        pm = UserFactory()
        ProjectRole.objects.create(user=pm, tenant=project.tenant, role=Role.PM)
        with pytest.raises(PermissionError):
            reject_amendment(amd, actor=pm, reason="nope")

    def test_cannot_reject_approved(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
        )
        director = UserFactory()
        ProjectRole.objects.create(
            user=director,
            tenant=project.tenant,
            role=Role.PROJECT_DIRECTOR,
        )
        with pytest.raises(AmendmentTransitionError):
            reject_amendment(amd, actor=director, reason="too late")


@pytest.mark.django_db
class TestHistoryTracksTransitions:
    def test_history_grows_on_each_transition(self, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
        )
        baseline = amd.history.count()
        submit_amendment(amd, actor=UserFactory())
        director = UserFactory()
        ProjectRole.objects.create(
            user=director,
            tenant=project.tenant,
            role=Role.PROJECT_DIRECTOR,
        )
        approve_amendment(amd, actor=director)
        amd.refresh_from_db()
        assert amd.history.count() == baseline + 2


# --------------------------------------------------------------------------- #
# ViewSet actions
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestAmendmentViewSetActions:
    def test_submit_action_moves_to_submitted(self, admin_client, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
        )
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/submit/",
        )
        assert response.status_code == 200, response.data
        amd.refresh_from_db()
        assert amd.status == Amendment.AmendmentStatus.SUBMITTED

    def test_approve_action_by_project_director_succeeds(self, api_client_as, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        client = api_client_as(role=Role.PROJECT_DIRECTOR)
        response = client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/approve/",
        )
        assert response.status_code == 200, response.data
        amd.refresh_from_db()
        assert amd.status == Amendment.AmendmentStatus.APPROVED

    def test_approve_action_by_pm_returns_403(self, api_client_as, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        client = api_client_as(role=Role.PM)
        response = client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/approve/",
        )
        assert response.status_code == 403

    def test_approve_invalid_state_returns_400(self, api_client_as, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
        )
        client = api_client_as(role=Role.PROJECT_DIRECTOR)
        response = client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/approve/",
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "INVALID_AMENDMENT_TRANSITION"

    def test_reject_action_by_project_director_succeeds(self, api_client_as, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        client = api_client_as(role=Role.PROJECT_DIRECTOR)
        response = client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/reject/",
            {"reason": "Hors périmètre"},
            format="json",
        )
        assert response.status_code == 200, response.data
        amd.refresh_from_db()
        assert amd.status == Amendment.AmendmentStatus.REJECTED

    def test_reject_by_finance_returns_403(self, api_client_as, project):
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
        )
        client = api_client_as(role=Role.FINANCE)
        response = client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/reject/",
            {"reason": "nope"},
            format="json",
        )
        assert response.status_code == 403

    def test_submit_approve_flow_via_api(self, admin_client, api_client_as, project):
        """End-to-end: DRAFT → SUBMITTED (any role) → APPROVED (director only)."""
        amd = AmendmentFactory(
            project=project,
            tenant=project.tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
        )
        r1 = admin_client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/submit/",
        )
        assert r1.status_code == 200

        director_client = api_client_as(role=Role.PROJECT_DIRECTOR)
        r2 = director_client.post(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/approve/",
        )
        assert r2.status_code == 200
        amd.refresh_from_db()
        assert amd.status == Amendment.AmendmentStatus.APPROVED
