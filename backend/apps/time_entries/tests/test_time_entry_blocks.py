"""Tests du blocage de saisie par personne (TimeEntryBlock) — Lot 2.

Couvre le modèle (contrainte XOR phase/tâche, unicité, helper blocks()),
l'enforcement à la saisie (employé bloqué → 400) et le ViewSet CRUD/permissions.
"""

import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Phase, Project, Task
from apps.time_entries.models import TimeEntryBlock


@pytest.fixture
def setup(db):
    tenant = Tenant.objects.create(name="Blk", slug="te-blk")
    project = Project.objects.create(tenant=tenant, code="BLK1", name="P")
    phase = Phase.objects.create(tenant=tenant, project=project, name="Ph")
    task = Task.objects.create(
        tenant=tenant, project=project, phase=phase, wbs_code="1.1", name="Feuille"
    )
    user = User.objects.create_user(username="emp_blk", password="pass123!")
    return {
        "tenant": tenant, "project": project, "phase": phase,
        "task": task, "user": user,
    }


@pytest.mark.django_db
class TestTimeEntryBlockModel:
    def test_phase_xor_task_rejects_both(self, setup):
        with pytest.raises(IntegrityError):
            TimeEntryBlock.objects.create(
                tenant=setup["tenant"], project=setup["project"],
                employee=setup["user"], phase=setup["phase"], task=setup["task"],
            )

    def test_phase_xor_task_rejects_neither(self, setup):
        with pytest.raises(IntegrityError):
            TimeEntryBlock.objects.create(
                tenant=setup["tenant"], project=setup["project"],
                employee=setup["user"],
            )

    def test_unique_employee_task(self, setup):
        TimeEntryBlock.objects.create(
            tenant=setup["tenant"], project=setup["project"],
            employee=setup["user"], task=setup["task"],
        )
        with pytest.raises(IntegrityError):
            TimeEntryBlock.objects.create(
                tenant=setup["tenant"], project=setup["project"],
                employee=setup["user"], task=setup["task"],
            )

    def test_blocks_classmethod_task(self, setup):
        TimeEntryBlock.objects.create(
            tenant=setup["tenant"], project=setup["project"],
            employee=setup["user"], task=setup["task"],
        )
        assert TimeEntryBlock.blocks(setup["user"].pk, setup["task"]) is True

    def test_blocks_classmethod_via_phase(self, setup):
        # Blocage au niveau phase → bloque toute tâche de la phase.
        other_task = Task.objects.create(
            tenant=setup["tenant"], project=setup["project"], phase=setup["phase"],
            wbs_code="1.2", name="Autre",
        )
        TimeEntryBlock.objects.create(
            tenant=setup["tenant"], project=setup["project"],
            employee=setup["user"], phase=setup["phase"],
        )
        assert TimeEntryBlock.blocks(setup["user"].pk, other_task) is True

    def test_blocks_false_when_no_block(self, setup):
        assert TimeEntryBlock.blocks(setup["user"].pk, setup["task"]) is False


@pytest.mark.django_db
class TestTimeEntryBlockEnforcement:
    def _api(self, user):
        api = APIClient()
        api.force_authenticate(user=user)
        return api

    def test_blocked_employee_cannot_log_on_task(self, setup):
        TimeEntryBlock.objects.create(
            tenant=setup["tenant"], project=setup["project"],
            employee=setup["user"], task=setup["task"],
        )
        resp = self._api(setup["user"]).post(
            "/api/v1/time_entries/",
            {"project": setup["project"].pk, "task": setup["task"].pk,
             "date": "2026-03-16", "hours": "4"},
            format="json", HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert resp.status_code == 400
        assert "task" in str(resp.data).lower() or "bloqu" in str(resp.data).lower()

    def test_phase_block_blocks_its_tasks(self, setup):
        TimeEntryBlock.objects.create(
            tenant=setup["tenant"], project=setup["project"],
            employee=setup["user"], phase=setup["phase"],
        )
        resp = self._api(setup["user"]).post(
            "/api/v1/time_entries/",
            {"project": setup["project"].pk, "task": setup["task"].pk,
             "date": "2026-03-16", "hours": "4"},
            format="json", HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert resp.status_code == 400

    def test_unblocked_employee_can_log(self, setup):
        # Un blocage qui vise QUELQU'UN D'AUTRE ne gêne pas self.user.
        other = User.objects.create_user(username="other_blk", password="x")
        TimeEntryBlock.objects.create(
            tenant=setup["tenant"], project=setup["project"],
            employee=other, task=setup["task"],
        )
        resp = self._api(setup["user"]).post(
            "/api/v1/time_entries/",
            {"project": setup["project"].pk, "task": setup["task"].pk,
             "date": "2026-03-16", "hours": "4"},
            format="json", HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert resp.status_code == 201


@pytest.mark.django_db
class TestTimeEntryBlockViewSet:
    def _api(self, user):
        api = APIClient()
        api.force_authenticate(user=user)
        return api

    def test_anonymous_cannot_list(self, setup):
        resp = APIClient().get("/api/v1/time_entry_blocks/")
        assert resp.status_code in (401, 403)

    def test_non_manager_cannot_create(self, setup):
        resp = self._api(setup["user"]).post(
            "/api/v1/time_entry_blocks/",
            {"project": setup["project"].pk, "employee": setup["user"].pk,
             "task": setup["task"].pk},
            format="json", HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert resp.status_code == 403

    def test_pm_can_create_and_delete(self, setup):
        pm = User.objects.create_user(username="pm_blk", password="x")
        ProjectRole.objects.create(tenant=setup["tenant"], user=pm, role=Role.PM)
        api = self._api(pm)
        resp = api.post(
            "/api/v1/time_entry_blocks/",
            {"project": setup["project"].pk, "employee": setup["user"].pk,
             "task": setup["task"].pk},
            format="json", HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert resp.status_code == 201, resp.data
        block_id = resp.data.get("data", resp.data)["id"]
        # Le blocage existe et bloque bien l'employé.
        assert TimeEntryBlock.blocks(setup["user"].pk, setup["task"]) is True
        # Suppression → débloque.
        d = api.delete(
            f"/api/v1/time_entry_blocks/{block_id}/",
            HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert d.status_code == 204
        assert TimeEntryBlock.blocks(setup["user"].pk, setup["task"]) is False

    def test_create_rejects_both_phase_and_task(self, setup):
        pm = User.objects.create_user(username="pm_blk2", password="x")
        ProjectRole.objects.create(tenant=setup["tenant"], user=pm, role=Role.ADMIN)
        resp = self._api(pm).post(
            "/api/v1/time_entry_blocks/",
            {"project": setup["project"].pk, "employee": setup["user"].pk,
             "phase": setup["phase"].pk, "task": setup["task"].pk},
            format="json", HTTP_X_TENANT_ID=str(setup["tenant"].pk),
        )
        assert resp.status_code == 400
