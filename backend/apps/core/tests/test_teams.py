"""Équipes (paramétrage) : CRUD réservé Finance/Paie/Admin + affectation projet.

- Lecture : tout utilisateur authentifié.
- Écriture (création / édition / suppression) : Finance, Paie, Admin.
- Affecter une équipe à un projet ajoute tous ses membres aux membres du projet
  (réservé aux gestionnaires de projet : PM / Admin / …).
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Team, Tenant

URL = "/api/v1/teams/"


def _client(tenant, role=None, suffix=""):
    c = APIClient()
    if role is None:
        return c
    u = User.objects.create_user(username=f"u_{role}_{tenant.id}{suffix}", password="pass123!")
    ProjectRole.objects.create(user=u, tenant=tenant, role=role)
    c.force_authenticate(user=u)
    c.defaults["HTTP_X_TENANT_ID"] = str(tenant.pk)
    return c


@pytest.mark.django_db
class TestTeamPermissions:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-teams")

    def test_anonymous_cannot_list(self):
        assert APIClient().get(URL).status_code in (401, 403)

    def test_authenticated_can_list(self):
        Team.objects.create(tenant=self.tenant, name="Studio A")
        assert _client(self.tenant, Role.EMPLOYEE).get(URL).status_code == 200

    @pytest.mark.parametrize("role", [Role.FINANCE, Role.PAIE, Role.ADMIN])
    def test_finance_paie_admin_can_create(self, role):
        resp = _client(self.tenant, role).post(URL, {"name": f"Équipe {role}"}, format="json")
        assert resp.status_code == 201
        assert Team.objects.filter(name=f"Équipe {role}").exists()

    @pytest.mark.parametrize("role", [Role.PM, Role.EMPLOYEE, Role.PROJECT_DIRECTOR])
    def test_others_cannot_create(self, role):
        resp = _client(self.tenant, role).post(URL, {"name": "Interdite"}, format="json")
        assert resp.status_code == 403
        assert not Team.objects.filter(name="Interdite").exists()

    def test_create_with_members(self):
        m1 = User.objects.create_user(username="m1", password="x")
        m2 = User.objects.create_user(username="m2", password="x")
        resp = _client(self.tenant, Role.FINANCE).post(
            URL, {"name": "Avec membres", "members": [m1.id, m2.id]}, format="json"
        )
        assert resp.status_code == 201
        team = Team.objects.get(name="Avec membres")
        assert set(team.members.values_list("id", flat=True)) == {m1.id, m2.id}


@pytest.mark.django_db
class TestAssignTeamToProject:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-assign")
        from apps.projects.models import Project

        self.project = Project.objects.create(
            tenant=self.tenant, code="P-AS", name="Assign", status="ACTIVE"
        )

    def test_assign_team_adds_all_members(self):
        m1 = User.objects.create_user(username="am1", password="x")
        m2 = User.objects.create_user(username="am2", password="x")
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        team.members.add(m1, m2)

        admin = _client(self.tenant, Role.ADMIN)
        resp = admin.post(
            f"/api/v1/projects/{self.project.id}/assign_team/",
            {"team_id": team.id},
            format="json",
        )
        assert resp.status_code == 200
        assert set(self.project.team_members.values_list("id", flat=True)) >= {m1.id, m2.id}

    def test_assign_team_forbidden_for_employee(self):
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        resp = _client(self.tenant, Role.EMPLOYEE).post(
            f"/api/v1/projects/{self.project.id}/assign_team/",
            {"team_id": team.id},
            format="json",
        )
        assert resp.status_code in (403, 404)


@pytest.mark.django_db
class TestAssignTeamToPhase:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-assign-ph")
        from apps.projects.models import Phase, Project

        self.project = Project.objects.create(
            tenant=self.tenant, code="P-PH", name="Assign", status="ACTIVE"
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept"
        )

    def _url(self):
        return f"/api/v1/projects/{self.project.id}/assign_team_to_phase/"

    def test_creates_allocation_per_member_on_phase(self):
        from apps.planning.models import ResourceAllocation

        m1 = User.objects.create_user(username="ph1", password="x")
        m2 = User.objects.create_user(username="ph2", password="x")
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        team.members.add(m1, m2)

        resp = _client(self.tenant, Role.ADMIN).post(
            self._url(),
            {"team_id": team.id, "phase_id": self.phase.id, "hours_per_week": 6},
            format="json",
        )
        assert resp.status_code == 200, resp.data
        allocs = ResourceAllocation.objects.filter(project=self.project, phase=self.phase)
        assert set(allocs.values_list("employee_id", flat=True)) == {m1.id, m2.id}
        assert all(float(a.hours_per_week) == 6 for a in allocs)
        # Allocations sur la PHASE (pas de tâche).
        assert all(a.task_id is None for a in allocs)

    def test_idempotent_skips_existing_active_allocation(self):
        from apps.planning.models import ResourceAllocation

        m1 = User.objects.create_user(username="ph3", password="x")
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        team.members.add(m1)
        admin = _client(self.tenant, Role.ADMIN)
        admin.post(self._url(), {"team_id": team.id, "phase_id": self.phase.id}, format="json")
        admin.post(self._url(), {"team_id": team.id, "phase_id": self.phase.id}, format="json")
        assert (
            ResourceAllocation.objects.filter(
                project=self.project, phase=self.phase, employee=m1
            ).count()
            == 1
        )

    def test_forbidden_for_employee(self):
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        resp = _client(self.tenant, Role.EMPLOYEE).post(
            self._url(), {"team_id": team.id, "phase_id": self.phase.id}, format="json"
        )
        assert resp.status_code in (403, 404)

    def test_missing_params_returns_400(self):
        resp = _client(self.tenant, Role.ADMIN).post(
            self._url(), {"team_id": None}, format="json"
        )
        assert resp.status_code == 400


@pytest.mark.django_db
class TestAssignTeamToTask:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-assign-tk")
        from apps.projects.models import Phase, Project, Task

        self.project = Project.objects.create(
            tenant=self.tenant, code="P-TK", name="Assign", status="ACTIVE"
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept"
        )
        self.task = Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            wbs_code="1.1", name="Feuille",
        )

    def _url(self):
        return f"/api/v1/projects/{self.project.id}/assign_team_to_task/"

    def test_creates_allocation_per_member_on_task(self):
        from apps.planning.models import ResourceAllocation

        m1 = User.objects.create_user(username="tk1", password="x")
        m2 = User.objects.create_user(username="tk2", password="x")
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        team.members.add(m1, m2)

        resp = _client(self.tenant, Role.ADMIN).post(
            self._url(), {"team_id": team.id, "task_id": self.task.id}, format="json"
        )
        assert resp.status_code == 200, resp.data
        allocs = ResourceAllocation.objects.filter(project=self.project, task=self.task)
        assert set(allocs.values_list("employee_id", flat=True)) == {m1.id, m2.id}
        # Allocation sur la TÂCHE (pas de phase).
        assert all(a.phase_id is None for a in allocs)

    def test_idempotent_skips_existing(self):
        from apps.planning.models import ResourceAllocation

        m1 = User.objects.create_user(username="tk3", password="x")
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        team.members.add(m1)
        admin = _client(self.tenant, Role.ADMIN)
        admin.post(self._url(), {"team_id": team.id, "task_id": self.task.id}, format="json")
        admin.post(self._url(), {"team_id": team.id, "task_id": self.task.id}, format="json")
        assert (
            ResourceAllocation.objects.filter(
                project=self.project, task=self.task, employee=m1
            ).count()
            == 1
        )

    def test_forbidden_for_employee(self):
        team = Team.objects.create(tenant=self.tenant, name="Studio")
        resp = _client(self.tenant, Role.EMPLOYEE).post(
            self._url(), {"team_id": team.id, "task_id": self.task.id}, format="json"
        )
        assert resp.status_code in (403, 404)

    def test_missing_params_returns_400(self):
        resp = _client(self.tenant, Role.ADMIN).post(
            self._url(), {"team_id": None}, format="json"
        )
        assert resp.status_code == 400
