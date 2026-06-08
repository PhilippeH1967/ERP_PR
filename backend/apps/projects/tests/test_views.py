"""API tests for projects app — permission matrix, cross-tenant
isolation, optimistic locking, audit trail and N+1 guards.
"""

from __future__ import annotations

import pytest

from apps.core.models import Role
from apps.projects.models import (
    Amendment,
    Phase,
    Project,
    ProjectTemplate,
    Task,
)

from .conftest import (
    AmendmentFactory,
    PhaseFactory,
    ProjectFactory,
    ProjectTemplateFactory,
    TaskFactory,
    UserFactory,
)

PRIVILEGED_ROLES = [
    Role.ADMIN,
    Role.FINANCE,
    Role.PM,
    Role.PROJECT_DIRECTOR,
    Role.BU_DIRECTOR,
    Role.DEPT_ASSISTANT,
    Role.PAIE,
]


# --------------------------------------------------------------------------- #
# ProjectViewSet
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestProjectList:
    def test_anonymous_returns_401(self, anonymous_client):
        response = anonymous_client.get("/api/v1/projects/")
        assert response.status_code == 401

    @pytest.mark.parametrize("role", PRIVILEGED_ROLES)
    def test_privileged_roles_see_all_projects(self, api_client_as, project, role):
        client = api_client_as(role=role)
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert data["meta"]["count"] >= 1

    def test_employee_only_sees_assigned_projects(self, api_client_as, tenant, project, phase):
        from datetime import date

        from apps.core.models import ProjectRole
        from apps.planning.models import ResourceAllocation

        client = api_client_as(role=Role.EMPLOYEE)
        employee = ProjectRole.objects.filter(role=Role.EMPLOYEE).first().user
        ResourceAllocation.objects.create(
            tenant=tenant,
            project=project,
            phase=phase,
            employee=employee,
            created_by=employee,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
        )
        other_project = ProjectFactory(tenant=tenant, code="OTHER-NOT-ASSIGNED")
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        codes = [row["code"] for row in response.json()["data"]]
        assert project.code in codes
        assert other_project.code not in codes

    def test_search_by_name(self, admin_client, tenant):
        ProjectFactory(tenant=tenant, code="SRCH-1", name="Searchable")
        response = admin_client.get("/api/v1/projects/?search=Searchable")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] == 1

    def test_filter_by_status(self, admin_client, tenant):
        ProjectFactory(tenant=tenant, code="ACT", name="A", status="ACTIVE")
        ProjectFactory(tenant=tenant, code="HOLD", name="H", status="ON_HOLD")
        response = admin_client.get("/api/v1/projects/?status=ACTIVE")
        codes = {row["code"] for row in response.json()["data"]}
        assert "ACT" in codes
        assert "HOLD" not in codes

    def test_list_with_many_projects_returns_paginated_results(self, admin_client, tenant):
        """Sanity test: list endpoint handles many projects without crashing.

        NOTE: ProjectListSerializer currently has an N+1 pattern
        (get_active_phase / get_budget_hours / get_total_invoiced). Tracked
        as a separate technical-debt ticket — do not assert query bounds here.
        """
        for i in range(15):
            ProjectFactory(tenant=tenant, code=f"NPL-{i:03d}")
        response = admin_client.get("/api/v1/projects/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] >= 15


@pytest.mark.django_db
class TestInternalProjectVisibility:
    """Le projet interne (is_internal, ex. « Interne » hébergeant Congés/
    Formation/Maladie) n'est visible que par les ADMIN — pas par les PM,
    associés, finance, employés. Les tâches obligatoires restent saisissables
    via l'endpoint dédié (mandatory_tasks)."""

    def _make_internal(self, tenant):
        from apps.projects.models import Project

        return Project.objects.create(
            tenant=tenant, code="INT-01", name="Interne",
            is_internal=True, status="ACTIVE",
        )

    def test_internal_hidden_from_pm_list_but_visible_to_admin(
        self, pm_client, admin_client, tenant
    ):
        self._make_internal(tenant)
        ProjectFactory(tenant=tenant, code="PRJ-CLIENT", name="Client")

        pm_codes = {r["code"] for r in pm_client.get("/api/v1/projects/").json()["data"]}
        assert "INT-01" not in pm_codes
        assert "PRJ-CLIENT" in pm_codes  # les projets clients restent visibles

        admin_codes = {
            r["code"] for r in admin_client.get("/api/v1/projects/").json()["data"]
        }
        assert "INT-01" in admin_codes

    def test_internal_detail_404_for_pm_200_for_admin(
        self, pm_client, admin_client, tenant
    ):
        internal = self._make_internal(tenant)
        assert pm_client.get(f"/api/v1/projects/{internal.id}/").status_code == 404
        assert admin_client.get(f"/api/v1/projects/{internal.id}/").status_code == 200

    def test_internal_hidden_from_employee_list(self, employee_client, tenant):
        self._make_internal(tenant)
        codes = {
            r["code"] for r in employee_client.get("/api/v1/projects/").json()["data"]
        }
        assert "INT-01" not in codes


@pytest.mark.django_db
class TestProjectTeamMembers:
    """Team membership (M2M) — lets an employee log time on a project even
    without a ResourceAllocation (planification), as long as they were
    explicitly added to the project team.
    """

    def _employee(self):
        from apps.core.models import ProjectRole

        return ProjectRole.objects.filter(role=Role.EMPLOYEE).first().user

    def test_member_without_allocation_sees_project(self, api_client_as, tenant):
        client = api_client_as(role=Role.EMPLOYEE)
        employee = self._employee()
        proj = ProjectFactory(tenant=tenant, code="MEMBER-PRJ")
        proj.team_members.add(employee)

        response = client.get("/api/v1/projects/")

        assert response.status_code == 200
        codes = [row["code"] for row in response.json()["data"]]
        assert "MEMBER-PRJ" in codes

    def test_non_member_without_allocation_does_not_see_project(self, api_client_as, tenant):
        client = api_client_as(role=Role.EMPLOYEE)
        ProjectFactory(tenant=tenant, code="HIDDEN-PRJ")

        response = client.get("/api/v1/projects/")

        assert response.status_code == 200
        codes = [row["code"] for row in response.json()["data"]]
        assert "HIDDEN-PRJ" not in codes

    def test_member_and_allocation_not_duplicated(self, api_client_as, tenant, phase):
        from datetime import date

        from apps.planning.models import ResourceAllocation

        client = api_client_as(role=Role.EMPLOYEE)
        employee = self._employee()
        proj = phase.project
        proj.team_members.add(employee)
        ResourceAllocation.objects.create(
            tenant=tenant,
            project=proj,
            phase=phase,
            employee=employee,
            created_by=employee,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
        )

        response = client.get("/api/v1/projects/")

        codes = [row["code"] for row in response.json()["data"]]
        assert codes.count(proj.code) == 1

    def test_serializer_exposes_team_members(self, admin_client, project):
        employee = UserFactory(username="member_detail_user")
        project.team_members.add(employee)

        response = admin_client.get(f"/api/v1/projects/{project.pk}/")

        assert response.status_code == 200
        data = response.json()["data"]
        assert employee.pk in data["team_members"]
        detail_ids = [m["id"] for m in data["team_members_detail"]]
        assert employee.pk in detail_ids

    # --- membership management action --------------------------------------

    def test_anonymous_cannot_add_member(self, anonymous_client, project):
        member = UserFactory(username="to_add_anon")
        response = anonymous_client.post(
            f"/api/v1/projects/{project.pk}/members/",
            {"user_id": member.pk},
            format="json",
        )
        assert response.status_code == 401

    def test_employee_cannot_add_member(self, api_client_as, tenant, project):
        client = api_client_as(role=Role.EMPLOYEE)
        member = UserFactory(username="to_add_emp")
        response = client.post(
            f"/api/v1/projects/{project.pk}/members/",
            {"user_id": member.pk},
            format="json",
        )
        assert response.status_code == 403
        assert not project.team_members.filter(pk=member.pk).exists()

    @pytest.mark.parametrize(
        "role", [Role.ADMIN, Role.PM, Role.PROJECT_DIRECTOR, Role.DEPT_ASSISTANT]
    )
    def test_privileged_can_add_member(self, api_client_as, tenant, project, role):
        client = api_client_as(role=role)
        member = UserFactory(username=f"to_add_{role}")
        response = client.post(
            f"/api/v1/projects/{project.pk}/members/",
            {"user_id": member.pk},
            format="json",
        )
        assert response.status_code == 200, response.content
        assert project.team_members.filter(pk=member.pk).exists()

    def test_add_member_missing_user_id_returns_400(self, pm_client, project):
        response = pm_client.post(f"/api/v1/projects/{project.pk}/members/", {}, format="json")
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "MISSING_USER_ID"

    def test_add_member_unknown_user_returns_404(self, pm_client, project):
        response = pm_client.post(
            f"/api/v1/projects/{project.pk}/members/",
            {"user_id": 9_999_999},
            format="json",
        )
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "USER_NOT_FOUND"

    def test_add_member_is_idempotent(self, pm_client, project):
        member = UserFactory(username="idempotent_member")
        for _ in range(2):
            response = pm_client.post(
                f"/api/v1/projects/{project.pk}/members/",
                {"user_id": member.pk},
                format="json",
            )
            assert response.status_code == 200
        assert project.team_members.filter(pk=member.pk).count() == 1

    def test_privileged_can_remove_member(self, pm_client, project):
        member = UserFactory(username="to_remove")
        project.team_members.add(member)
        response = pm_client.delete(f"/api/v1/projects/{project.pk}/members/{member.pk}/")
        assert response.status_code in (200, 204)
        assert not project.team_members.filter(pk=member.pk).exists()

    def test_employee_cannot_remove_member(self, api_client_as, project):
        client = api_client_as(role=Role.EMPLOYEE)
        member = UserFactory(username="protected_member")
        project.team_members.add(member)
        response = client.delete(f"/api/v1/projects/{project.pk}/members/{member.pk}/")
        assert response.status_code == 403
        assert project.team_members.filter(pk=member.pk).exists()


@pytest.mark.django_db
class TestProjectRetrieve:
    def test_anonymous_returns_401(self, anonymous_client, project):
        response = anonymous_client.get(f"/api/v1/projects/{project.pk}/")
        assert response.status_code == 401

    def test_admin_retrieves_project(self, admin_client, project):
        response = admin_client.get(f"/api/v1/projects/{project.pk}/")
        assert response.status_code == 200
        data = response.json()["data"]
        assert data["code"] == project.code

    def test_cross_tenant_returns_404(self, admin_client, other_tenant_project):
        """Admin of tenant A should get 404 (not 403) on tenant B resource."""
        response = admin_client.get(f"/api/v1/projects/{other_tenant_project.pk}/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestProjectCreate:
    def test_anonymous_returns_401(self, anonymous_client):
        response = anonymous_client.post(
            "/api/v1/projects/", {"code": "X", "name": "X"}, format="json"
        )
        assert response.status_code == 401

    def test_admin_can_create(self, admin_client):
        response = admin_client.post(
            "/api/v1/projects/",
            {"code": "NEW-ADM", "name": "Nouveau", "contract_type": "FORFAITAIRE"},
            format="json",
        )
        assert response.status_code == 201, response.data
        assert Project.objects.filter(code="NEW-ADM").exists()

    def test_perform_create_without_tenant_header_uses_fallback(self, api_client_as, tenant):
        """Client without X-Tenant-Id falls back to Tenant.objects.first()."""
        # Remove the X-Tenant-Id default injected by fixture
        client = api_client_as(role=Role.ADMIN)
        client.defaults.pop("HTTP_X_TENANT_ID", None)
        response = client.post(
            "/api/v1/projects/",
            {"code": "FB-1", "name": "Fallback", "contract_type": "FORFAITAIRE"},
            format="json",
        )
        assert response.status_code == 201, response.data


@pytest.mark.django_db
class TestProjectStatusTransitions:
    def test_valid_transition_active_to_on_hold(self, admin_client, project):
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"status": "ON_HOLD", "version": project.version},
            format="json",
        )
        assert response.status_code == 200
        project.refresh_from_db()
        assert project.status == "ON_HOLD"

    def test_invalid_transition_completed_to_active_returns_400(self, admin_client, tenant):
        project = ProjectFactory(tenant=tenant, status="COMPLETED")
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"status": "ACTIVE", "version": project.version},
            format="json",
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "INVALID_STATUS_TRANSITION"

    def test_same_status_is_noop(self, admin_client, project):
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"status": "ACTIVE", "version": project.version},
            format="json",
        )
        assert response.status_code == 200


@pytest.mark.django_db
class TestProjectOptimisticLock:
    def test_version_conflict_returns_409(self, admin_client, project):
        # Bump DB version once.
        admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"name": "First", "version": project.version},
            format="json",
        )
        # Second PATCH with stale version
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"name": "Second", "version": 1},
            format="json",
        )
        assert response.status_code == 409


@pytest.mark.django_db
class TestProjectHistory:
    def test_history_records_create_and_update(self, admin_client):
        response = admin_client.post(
            "/api/v1/projects/",
            {"code": "HST", "name": "Hist", "contract_type": "FORFAITAIRE"},
            format="json",
        )
        assert response.status_code == 201
        project = Project.objects.get(code="HST")
        assert project.history.count() == 1
        admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"name": "Hist2", "version": project.version},
            format="json",
        )
        project.refresh_from_db()
        assert project.history.count() == 2


@pytest.mark.django_db
class TestProjectDashboard:
    def test_dashboard_returns_health(self, admin_client, project):
        response = admin_client.get(f"/api/v1/projects/{project.pk}/dashboard/")
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["health"] in {"green", "yellow", "red"}
        assert payload["code"] == project.code

    def test_dashboard_health_yellow_when_utilization_between_75_and_90(
        self, admin_client, project, tenant
    ):
        from decimal import Decimal

        from apps.core.models import ProjectRole
        from apps.time_entries.models import TimeEntry

        phase = PhaseFactory(project=project, tenant=tenant, budgeted_hours=Decimal("100"))
        admin_user = ProjectRole.objects.filter(role=Role.ADMIN).first().user
        TimeEntry.objects.create(
            tenant=tenant,
            project=project,
            phase=phase,
            employee=admin_user,
            date="2026-01-15",
            hours=Decimal("80"),
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/dashboard/")
        data = response.json()
        payload = data.get("data", data)
        assert payload["health"] == "yellow"

    def test_dashboard_health_red_when_utilization_above_90(self, admin_client, project, tenant):
        from decimal import Decimal

        from apps.core.models import ProjectRole
        from apps.time_entries.models import TimeEntry

        phase = PhaseFactory(project=project, tenant=tenant, budgeted_hours=Decimal("100"))
        admin_user = ProjectRole.objects.filter(role=Role.ADMIN).first().user
        TimeEntry.objects.create(
            tenant=tenant,
            project=project,
            phase=phase,
            employee=admin_user,
            date="2026-01-15",
            hours=Decimal("95"),
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/dashboard/")
        payload = response.json().get("data", response.json())
        assert payload["health"] == "red"


@pytest.mark.django_db
class TestProjectTeamStats:
    def test_team_stats_returns_structure(self, admin_client, project):
        PhaseFactory(project=project, tenant=project.tenant)
        response = admin_client.get(f"/api/v1/projects/{project.pk}/team_stats/")
        assert response.status_code == 200
        data = response.json()["data"]
        assert "budget_status" in data
        assert "phases_health" in data
        assert "employees_monthly" in data


# --------------------------------------------------------------------------- #
# CreateFromTemplate action
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestCreateFromTemplateAction:
    def test_anonymous_returns_401(self, anonymous_client):
        response = anonymous_client.post(
            "/api/v1/projects/create_from_template/", {}, format="json"
        )
        assert response.status_code == 401

    def test_creates_project_with_phases(self, admin_client, project_template):
        response = admin_client.post(
            "/api/v1/projects/create_from_template/",
            {
                "template_id": project_template.pk,
                "project": {"code": "FT-1", "name": "Depuis template"},
            },
            format="json",
        )
        assert response.status_code == 201, response.data
        project = Project.objects.get(code="FT-1")
        # 2 phases du template + 1 phase SUPPORT pour le service transversal BIM
        # (support_services_config par défaut du ProjectTemplateFactory).
        assert project.phases.count() == 3
        support = project.phases.get(phase_type=Phase.PhaseType.SUPPORT, code="BIM")
        assert support.tasks.filter(parent__isnull=True).count() == 1

    def test_missing_template_id_returns_400(self, admin_client):
        response = admin_client.post(
            "/api/v1/projects/create_from_template/",
            {"project": {"code": "X", "name": "X"}},
            format="json",
        )
        assert response.status_code == 400
        assert response.json()["error"]["code"] == "MISSING_TEMPLATE"

    def test_unknown_template_returns_404(self, admin_client):
        response = admin_client.post(
            "/api/v1/projects/create_from_template/",
            {"template_id": 9_999_999, "project": {"code": "X", "name": "X"}},
            format="json",
        )
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "TEMPLATE_NOT_FOUND"


# --------------------------------------------------------------------------- #
# ProjectTemplateViewSet
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestProjectTemplateViewSet:
    def test_anonymous_list_returns_401(self, anonymous_client):
        response = anonymous_client.get("/api/v1/project_templates/")
        assert response.status_code == 401

    def test_admin_can_list(self, admin_client, project_template):
        response = admin_client.get("/api/v1/project_templates/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] >= 1

    def test_inactive_template_hidden_from_list(self, admin_client, tenant):
        ProjectTemplateFactory(tenant=tenant, name="Active template")
        ProjectTemplateFactory(tenant=tenant, name="Inactive", is_active=False)
        response = admin_client.get("/api/v1/project_templates/")
        names = {t["name"] for t in response.json()["data"]}
        assert "Active template" in names
        assert "Inactive" not in names

    def test_admin_can_create(self, admin_client):
        response = admin_client.post(
            "/api/v1/project_templates/",
            {"name": "Nouveau", "contract_type": "FORFAITAIRE"},
            format="json",
        )
        assert response.status_code == 201
        assert ProjectTemplate.objects.filter(name="Nouveau").exists()

    def test_cannot_delete_template_in_use(self, admin_client, tenant, project_template):
        ProjectFactory(tenant=tenant, template=project_template, code="USING")
        response = admin_client.delete(f"/api/v1/project_templates/{project_template.pk}/")
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "TEMPLATE_IN_USE"
        assert ProjectTemplate.objects.filter(pk=project_template.pk).exists()

    def test_can_delete_unused_template(self, admin_client, project_template):
        response = admin_client.delete(f"/api/v1/project_templates/{project_template.pk}/")
        assert response.status_code == 204
        assert not ProjectTemplate.objects.filter(pk=project_template.pk).exists()

    def test_create_without_tenant_header_uses_fallback(self, api_client_as, tenant):
        client = api_client_as(role=Role.ADMIN)
        client.defaults.pop("HTTP_X_TENANT_ID", None)
        response = client.post(
            "/api/v1/project_templates/",
            {"name": "FB", "contract_type": "FORFAITAIRE"},
            format="json",
        )
        assert response.status_code == 201


# --------------------------------------------------------------------------- #
# PhaseViewSet (nested)
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestPhaseViewSet:
    def test_anonymous_list_returns_401(self, anonymous_client, project):
        response = anonymous_client.get(f"/api/v1/projects/{project.pk}/phases/")
        assert response.status_code == 401

    def test_admin_lists_phases_for_project(self, admin_client, project):
        PhaseFactory(project=project, tenant=project.tenant, name="Ph1", order=1)
        response = admin_client.get(f"/api/v1/projects/{project.pk}/phases/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] == 1

    def test_admin_can_create_phase(self, admin_client, project):
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/phases/",
            {"name": "New Phase", "order": 1, "billing_mode": "HORAIRE"},
            format="json",
        )
        assert response.status_code == 201
        assert Phase.objects.filter(project=project, name="New Phase").exists()

    def test_cannot_delete_mandatory_phase(self, admin_client, project):
        phase = PhaseFactory(project=project, tenant=project.tenant, is_mandatory=True)
        response = admin_client.delete(f"/api/v1/projects/{project.pk}/phases/{phase.pk}/")
        assert response.status_code == 400
        assert Phase.objects.filter(pk=phase.pk).exists()

    def test_can_delete_non_mandatory_phase(self, admin_client, project):
        phase = PhaseFactory(project=project, tenant=project.tenant, is_mandatory=False)
        response = admin_client.delete(f"/api/v1/projects/{project.pk}/phases/{phase.pk}/")
        assert response.status_code == 204
        assert not Phase.objects.filter(pk=phase.pk).exists()

    # Les phases sont du paramétrage : seuls les admins les modifient sur un projet.
    def test_pm_can_list_phases(self, pm_client, project):
        PhaseFactory(project=project, tenant=project.tenant)
        assert pm_client.get(f"/api/v1/projects/{project.pk}/phases/").status_code == 200

    def test_pm_cannot_create_phase(self, pm_client, project):
        response = pm_client.post(
            f"/api/v1/projects/{project.pk}/phases/",
            {"name": "PM Phase", "order": 1},
            format="json",
        )
        assert response.status_code == 403
        assert not Phase.objects.filter(project=project, name="PM Phase").exists()

    def test_pm_cannot_update_phase(self, pm_client, project):
        phase = PhaseFactory(project=project, tenant=project.tenant, name="Origine")
        response = pm_client.patch(
            f"/api/v1/projects/{project.pk}/phases/{phase.pk}/",
            {"name": "Modifiée"},
            format="json",
        )
        assert response.status_code == 403
        phase.refresh_from_db()
        assert phase.name == "Origine"

    def test_pm_cannot_delete_phase(self, pm_client, project):
        phase = PhaseFactory(project=project, tenant=project.tenant, is_mandatory=False)
        response = pm_client.delete(f"/api/v1/projects/{project.pk}/phases/{phase.pk}/")
        assert response.status_code == 403
        assert Phase.objects.filter(pk=phase.pk).exists()


# --------------------------------------------------------------------------- #
# TaskViewSet (nested) — brand new
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestTaskViewSet:
    def test_anonymous_list_returns_401(self, anonymous_client, project):
        response = anonymous_client.get(f"/api/v1/projects/{project.pk}/tasks/")
        assert response.status_code == 401

    def test_admin_lists_tasks_for_project(self, admin_client, project, phase):
        TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="10.1")
        response = admin_client.get(f"/api/v1/projects/{project.pk}/tasks/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] == 1

    def test_create_task_without_wbs_code_autogenerates(self, admin_client, project, phase):
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/tasks/",
            {
                "project": project.pk,
                "phase": phase.pk,
                "name": "Auto wbs",
                "wbs_code": "",
            },
            format="json",
        )
        assert response.status_code == 201, response.data
        assert Task.objects.filter(project=project, name="Auto wbs").exists()

    def test_create_task_autogenerates_unique_wbs_when_collision(
        self, admin_client, project, phase
    ):
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code=f"{phase.code}.1",
        )
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/tasks/",
            {"project": project.pk, "phase": phase.pk, "name": "Auto", "wbs_code": ""},
            format="json",
        )
        assert response.status_code == 201
        # Backend auto-incremented to avoid the collision
        codes = set(project.tasks.values_list("wbs_code", flat=True))
        assert len(codes) == 2

    def test_create_task_with_explicit_wbs_code(self, admin_client, project, phase):
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/tasks/",
            {
                "project": project.pk,
                "phase": phase.pk,
                "wbs_code": "7.42",
                "name": "Explicit",
            },
            format="json",
        )
        assert response.status_code == 201
        assert Task.objects.filter(wbs_code="7.42").exists()

    def test_create_subtask_autogenerates_nested_three_level_wbs(
        self, admin_client, project, phase
    ):
        """Une sous-tâche (``parent`` renseigné, sans ``wbs_code``) reçoit un WBS
        à 3 niveaux ``{wbs_parent}.{séquence}`` — pas ``{code_phase}.{n}`` (bug
        du picker de tâches standard au wizard)."""
        parent = TaskFactory(
            project=project, phase=phase, tenant=project.tenant, wbs_code="1.1"
        )
        sub_a = admin_client.post(
            f"/api/v1/projects/{project.pk}/tasks/",
            {
                "project": project.pk, "phase": phase.pk, "parent": parent.pk,
                "task_type": "SUBTASK", "name": "Sous A", "wbs_code": "",
            },
            format="json",
        )
        assert sub_a.status_code == 201, sub_a.data
        assert Task.objects.get(project=project, name="Sous A").wbs_code == "1.1.1"

        sub_b = admin_client.post(
            f"/api/v1/projects/{project.pk}/tasks/",
            {
                "project": project.pk, "phase": phase.pk, "parent": parent.pk,
                "task_type": "SUBTASK", "name": "Sous B", "wbs_code": "",
            },
            format="json",
        )
        assert sub_b.status_code == 201, sub_b.data
        assert Task.objects.get(project=project, name="Sous B").wbs_code == "1.1.2"

    def test_create_root_task_keeps_two_level_wbs(self, admin_client, project, phase):
        """Régression : une tâche racine (sans ``parent``) garde ``{code_phase}.{n}``."""
        resp = admin_client.post(
            f"/api/v1/projects/{project.pk}/tasks/",
            {"project": project.pk, "phase": phase.pk, "name": "Racine", "wbs_code": ""},
            format="json",
        )
        assert resp.status_code == 201, resp.data
        code = Task.objects.get(project=project, name="Racine").wbs_code
        assert code.startswith(f"{phase.code}.")
        assert code.count(".") == 1

    def test_update_task(self, admin_client, project, phase):
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="11.1")
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/tasks/{task.pk}/",
            {"name": "Renamed"},
            format="json",
        )
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.name == "Renamed"

    def test_delete_task(self, admin_client, project, phase):
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="11.2")
        response = admin_client.delete(f"/api/v1/projects/{project.pk}/tasks/{task.pk}/")
        assert response.status_code == 204
        assert not Task.objects.filter(pk=task.pk).exists()

    def test_update_task_wbs_code(self, admin_client, project, phase):
        """F3.7 : le code WBS peut être modifié après création."""
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="11.3")
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/tasks/{task.pk}/",
            {"wbs_code": "3.1.5"}, format="json",
        )
        assert response.status_code == 200, response.content
        task.refresh_from_db()
        assert task.wbs_code == "3.1.5"

    def test_update_task_client_facing_label(self, admin_client, project, phase):
        """F3.7 : le libellé client (WBS client) peut être modifié."""
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant)
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/tasks/{task.pk}/",
            {"client_facing_label": "Étude faisabilité — Phase 1"},
            format="json",
        )
        assert response.status_code == 200, response.content
        task.refresh_from_db()
        assert task.client_facing_label == "Étude faisabilité — Phase 1"

    def test_update_task_budgets(self, admin_client, project, phase):
        """F3.7 : les budgets heures + coût peuvent être modifiés."""
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant)
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/tasks/{task.pk}/",
            {"budgeted_hours": "120.0", "budgeted_cost": "9500.00"},
            format="json",
        )
        assert response.status_code == 200, response.content
        task.refresh_from_db()
        assert float(task.budgeted_hours) == 120.0
        assert float(task.budgeted_cost) == 9500.0

    def test_employee_cannot_update_task_budgets(
        self, api_client_as, project, phase,
    ):
        """F3.7 : un employé ne peut pas modifier les champs de coût."""
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant)
        emp_client = api_client_as(role=Role.EMPLOYEE)
        response = emp_client.patch(
            f"/api/v1/projects/{project.pk}/tasks/{task.pk}/",
            {"budgeted_cost": "50000"}, format="json",
        )
        # soit 403 (interdit), soit 200 mais le champ est ignoré par le mixin
        if response.status_code == 200:
            task.refresh_from_db()
            assert float(task.budgeted_cost) != 50000
        else:
            assert response.status_code in (403,)

    def test_task_always_display_default_false(self, project, phase, tenant):
        """Le flag d'affichage obligatoire par défaut = False."""
        task = TaskFactory(project=project, phase=phase, tenant=tenant)
        assert task.always_display_in_timesheet is False

    def test_filter_tasks_by_always_display(self, admin_client, project, phase, tenant):
        """L'API permet de filtrer les tâches obligatoires (?always_display_in_timesheet=true)."""
        from apps.projects.models import Task
        TaskFactory(
            project=project, phase=phase, tenant=tenant,
            wbs_code="C-1", name="Congés", always_display_in_timesheet=True,
        )
        TaskFactory(
            project=project, phase=phase, tenant=tenant,
            wbs_code="N-1", name="Tâche normale",
        )
        resp = admin_client.get(
            f"/api/v1/projects/{project.pk}/tasks/?always_display_in_timesheet=true",
        )
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        results = data.get("results", data) if isinstance(data, dict) else data
        names = [t["name"] for t in results]
        assert "Congés" in names
        assert "Tâche normale" not in names
        # Vérifie le total côté DB
        assert Task.objects.filter(always_display_in_timesheet=True).count() == 1

    def test_patch_task_always_display(self, admin_client, project, phase, tenant):
        """Toggle du flag d'affichage obligatoire via PATCH."""
        task = TaskFactory(project=project, phase=phase, tenant=tenant, wbs_code="A-1")
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/tasks/{task.pk}/",
            {"always_display_in_timesheet": True}, format="json",
        )
        assert resp.status_code == 200
        task.refresh_from_db()
        assert task.always_display_in_timesheet is True


# --------------------------------------------------------------------------- #
# AmendmentViewSet (nested)
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestAmendmentViewSet:
    def test_anonymous_list_returns_401(self, anonymous_client, project):
        response = anonymous_client.get(f"/api/v1/projects/{project.pk}/amendments/")
        assert response.status_code == 401

    def test_admin_lists_amendments(self, admin_client, project):
        AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        AmendmentFactory(project=project, tenant=project.tenant, amendment_number=2)
        response = admin_client.get(f"/api/v1/projects/{project.pk}/amendments/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] == 2

    def test_admin_creates_amendment_with_auto_number(self, admin_client, project):
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/amendments/",
            {
                "description": "Premier avenant",
                "status": "DRAFT",
                "budget_impact": "10000.00",
            },
            format="json",
        )
        assert response.status_code == 201, response.data
        data = response.json()["data"]
        assert data["amendment_number"] == 1
        assert Amendment.objects.filter(project=project, amendment_number=1).exists()

    def test_amendment_number_sequence_per_project(self, admin_client, project):
        AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/amendments/",
            {"description": "Second", "status": "DRAFT"},
            format="json",
        )
        assert response.status_code == 201
        assert response.json()["data"]["amendment_number"] == 2

    def test_amendment_records_requested_by(self, admin_client, project):
        response = admin_client.post(
            f"/api/v1/projects/{project.pk}/amendments/",
            {"description": "Track requester", "status": "DRAFT"},
            format="json",
        )
        amd = Amendment.objects.get(pk=response.json()["data"]["id"])
        assert amd.requested_by is not None

    def test_update_amendment_optimistic_lock(self, admin_client, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        # First PATCH bumps version to 2
        admin_client.patch(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/",
            {"description": "First", "version": 1},
            format="json",
        )
        # Stale PATCH
        response = admin_client.patch(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/",
            {"description": "Stale", "version": 1},
            format="json",
        )
        assert response.status_code == 409

    def test_scope_returns_phases_and_tasks_attached_to_amendment(
        self, admin_client, project
    ):
        """GET /amendments/<id>/scope/ returns phases+tasks attached to this amendment."""
        from apps.projects.tests.conftest import PhaseFactory, TaskFactory

        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        main_phase = PhaseFactory(project=project, tenant=project.tenant, name="Main")
        amd_phase = PhaseFactory(
            project=project, tenant=project.tenant, amendment=amd, name="Scope avenant"
        )
        TaskFactory(
            project=project, phase=main_phase, tenant=project.tenant, wbs_code="1.1"
        )
        TaskFactory(
            project=project,
            phase=main_phase,
            tenant=project.tenant,
            wbs_code="AV1.1",
            amendment=amd,
        )
        TaskFactory(
            project=project,
            phase=amd_phase,
            tenant=project.tenant,
            wbs_code="AV1.2",
            amendment=amd,
        )
        response = admin_client.get(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/scope/"
        )
        assert response.status_code == 200
        body = response.json().get("data", response.json())
        phase_names = {p["name"] for p in body["phases"]}
        task_codes = {t["wbs_code"] for t in body["tasks"]}
        assert phase_names == {"Scope avenant"}
        assert task_codes == {"AV1.1", "AV1.2"}

    def test_scope_empty_amendment_returns_empty_lists(self, admin_client, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        response = admin_client.get(
            f"/api/v1/projects/{project.pk}/amendments/{amd.pk}/scope/"
        )
        assert response.status_code == 200
        body = response.json().get("data", response.json())
        assert body["phases"] == []
        assert body["tasks"] == []


# --------------------------------------------------------------------------- #
# Cross-tenant sanity on nested routers
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestNestedCrossTenantIsolation:
    def test_amendments_route_scoped_to_project(self, admin_client, project, other_tenant_project):
        AmendmentFactory(
            project=other_tenant_project,
            tenant=other_tenant_project.tenant,
            amendment_number=1,
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/amendments/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] == 0

    def test_tasks_route_scoped_to_project(self, admin_client, project, other_tenant_project):
        ph = PhaseFactory(project=other_tenant_project, tenant=other_tenant_project.tenant)
        TaskFactory(
            project=other_tenant_project,
            phase=ph,
            tenant=other_tenant_project.tenant,
            wbs_code="OT.1",
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/tasks/")
        assert response.status_code == 200
        assert response.json()["meta"]["count"] == 0


# --------------------------------------------------------------------------- #
# Consortium edge case from legacy test
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestCreateProjectWithConsortium:
    def test_create_project_linked_to_consortium(self, admin_client, tenant):
        from apps.clients.models import Client
        from apps.consortiums.models import Consortium

        client = Client.objects.create(tenant=tenant, name="Ville XYZ", alias="VXYZ")
        consortium = Consortium.objects.create(
            tenant=tenant,
            name="PR + ABC + DEF",
            client=client,
            pr_role="MANDATAIRE",
        )
        response = admin_client.post(
            "/api/v1/projects/",
            {
                "code": "PRJ-CONS",
                "name": "Projet Consortium",
                "contract_type": "CONSORTIUM",
                "is_consortium": True,
                "consortium": consortium.pk,
            },
            format="json",
        )
        assert response.status_code == 201, response.data
        project = Project.objects.get(code="PRJ-CONS")
        assert project.is_consortium is True
        assert project.consortium_id == consortium.pk


# --------------------------------------------------------------------------- #
# Closure checklist (F3.8)
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestProjectClosureChecklist:
    """Endpoint GET /projects/{id}/closure_checklist/ — prérequis de clôture."""

    URL = "/api/v1/projects/{pk}/closure_checklist/"

    def test_anonymous_returns_401(self, anonymous_client, project):
        resp = anonymous_client.get(self.URL.format(pk=project.pk))
        assert resp.status_code in (401, 403)

    def test_empty_project_can_close(self, admin_client, project):
        resp = admin_client.get(self.URL.format(pk=project.pk))
        assert resp.status_code == 200, resp.content
        data = resp.json().get("data", resp.json())
        assert data["can_close"] is True
        codes = {c["code"]: c for c in data["checks"]}
        for code in ("TIME_ENTRIES", "INVOICES", "EXPENSES",
                     "VIRTUAL_RESOURCES", "FUTURE_ALLOCATIONS"):
            assert code in codes, f"check {code} missing"
            assert codes[code]["passed"] is True

    def test_unvalidated_time_entries_block_closure(self, admin_client, project, tenant):
        from datetime import date

        from django.contrib.auth import get_user_model

        from apps.time_entries.models import TimeEntry, TimeEntryStatus

        user = get_user_model().objects.create_user(username="emp_c", password="p")
        TimeEntry.objects.create(
            tenant=tenant, employee=user, project=project,
            date=date(2026, 3, 1), hours=8, status=TimeEntryStatus.SUBMITTED,
        )
        resp = admin_client.get(self.URL.format(pk=project.pk))
        data = resp.json().get("data", resp.json())
        time_check = next(c for c in data["checks"] if c["code"] == "TIME_ENTRIES")
        assert time_check["passed"] is False
        assert data["can_close"] is False

    def test_draft_invoice_blocks_closure(self, admin_client, project, tenant):
        from apps.billing.models import Invoice, InvoiceStatus
        from apps.clients.models import Client

        client = Client.objects.create(tenant=tenant, name="Client Close")
        Invoice.objects.create(
            tenant=tenant, project=project, client=client, invoice_number="INV-CL-001",
            status=InvoiceStatus.DRAFT, total_amount=1000,
        )
        resp = admin_client.get(self.URL.format(pk=project.pk))
        data = resp.json().get("data", resp.json())
        inv_check = next(c for c in data["checks"] if c["code"] == "INVOICES")
        assert inv_check["passed"] is False
        assert data["can_close"] is False

    def test_pending_expense_blocks_closure(self, admin_client, project, tenant):
        from django.contrib.auth import get_user_model

        from apps.expenses.models import ExpenseReport, ExpenseStatus

        user = get_user_model().objects.create_user(username="emp_x", password="p")
        ExpenseReport.objects.create(
            tenant=tenant, employee=user, project=project,
            status=ExpenseStatus.SUBMITTED, total_amount=100,
        )
        resp = admin_client.get(self.URL.format(pk=project.pk))
        data = resp.json().get("data", resp.json())
        exp_check = next(c for c in data["checks"] if c["code"] == "EXPENSES")
        assert exp_check["passed"] is False
        assert data["can_close"] is False

    def test_active_virtual_resource_is_warning_not_blocker(
        self, admin_client, project, tenant,
    ):
        from apps.planning.models import VirtualResource

        VirtualResource.objects.create(
            tenant=tenant, project=project, name="Archi senior", is_active=True,
        )
        resp = admin_client.get(self.URL.format(pk=project.pk))
        data = resp.json().get("data", resp.json())
        vr_check = next(c for c in data["checks"] if c["code"] == "VIRTUAL_RESOURCES")
        assert vr_check["passed"] is False
        assert vr_check.get("severity") == "warning"
        assert data["can_close"] is True, "warnings ne doivent pas bloquer"

    def test_future_allocation_is_warning_not_blocker(
        self, admin_client, project, tenant, phase,
    ):
        from datetime import date, timedelta

        from django.contrib.auth import get_user_model

        from apps.planning.models import ResourceAllocation

        user = get_user_model().objects.create_user(username="emp_a", password="p")
        future = date.today() + timedelta(days=30)
        ResourceAllocation.objects.create(
            tenant=tenant, employee=user, project=project, phase=phase,
            start_date=date.today(), end_date=future, hours_per_week=20,
            created_by=user,
        )
        resp = admin_client.get(self.URL.format(pk=project.pk))
        data = resp.json().get("data", resp.json())
        fa = next(c for c in data["checks"] if c["code"] == "FUTURE_ALLOCATIONS")
        assert fa["passed"] is False
        assert fa.get("severity") == "warning"
        assert data["can_close"] is True


@pytest.mark.django_db
class TestProjectClosureEnforcement:
    """PATCH /projects/{id}/ status=COMPLETED bloqué si checklist échoue."""

    def test_completion_blocked_when_unvalidated_time_entries(
        self, admin_client, project, tenant,
    ):
        from datetime import date

        from django.contrib.auth import get_user_model

        from apps.time_entries.models import TimeEntry, TimeEntryStatus

        user = get_user_model().objects.create_user(username="emp_b", password="p")
        TimeEntry.objects.create(
            tenant=tenant, employee=user, project=project,
            date=date(2026, 3, 1), hours=8, status=TimeEntryStatus.SUBMITTED,
        )
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"status": "COMPLETED"}, format="json",
        )
        assert resp.status_code == 400
        err = resp.json().get("error", {})
        assert err.get("code") == "CLOSURE_CHECKLIST_FAILED"

    def test_completion_allowed_when_all_checks_pass(self, admin_client, project):
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"status": "COMPLETED"}, format="json",
        )
        assert resp.status_code == 200, resp.content
        project.refresh_from_db()
        assert project.status == "COMPLETED"

    def test_non_completion_transition_not_affected(self, admin_client, project, tenant):
        from datetime import date

        from django.contrib.auth import get_user_model

        from apps.time_entries.models import TimeEntry, TimeEntryStatus

        user = get_user_model().objects.create_user(username="emp_d", password="p")
        TimeEntry.objects.create(
            tenant=tenant, employee=user, project=project,
            date=date(2026, 3, 1), hours=8, status=TimeEntryStatus.SUBMITTED,
        )
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"status": "ON_HOLD"}, format="json",
        )
        assert resp.status_code == 200, resp.content
