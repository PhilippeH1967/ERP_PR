"""Tests for Time Entry API endpoints."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant
from apps.projects.models import Phase, Project, Task
from apps.time_entries.models import TimeEntry, WeeklyApproval


@pytest.mark.django_db
class TestTimeEntryAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API", slug="te-api")
        self.project = Project.objects.create(tenant=self.tenant, code="TE1", name="TimeProject")
        self.phase = Phase.objects.create(tenant=self.tenant, project=self.project, name="Ph1")
        self.user = User.objects.create_user(username="te_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_entries(self):
        response = self.api.get("/api/v1/time_entries/")
        assert response.status_code == 200

    def test_create_entry_on_leaf_task_ok(self):
        """Saisie autorisée sur une tâche saisissable (feuille)."""
        leaf = Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            wbs_code="1.1", name="Feuille",
        )
        response = self.api.post(
            "/api/v1/time_entries/",
            {"project": self.project.pk, "task": leaf.pk, "date": "2026-03-16", "hours": "4"},
            format="json", HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_create_entry_on_parent_task_rejected(self):
        """API : saisie refusée (400) sur une tâche-mère (regroupement)."""
        parent = Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            wbs_code="1.0", name="Mère",
        )
        Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            parent=parent, task_type="SUBTASK", wbs_code="1.0.1", name="Sous",
        )
        response = self.api.post(
            "/api/v1/time_entries/",
            {"project": self.project.pk, "task": parent.pk, "date": "2026-03-16", "hours": "4"},
            format="json", HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 400

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

    def test_create_entry_negative_hours_rejected(self):
        """TS-014: Negative hours must be rejected."""
        response = self.api.post(
            "/api/v1/time_entries/",
            {
                "project": self.project.pk,
                "phase": self.phase.pk,
                "date": "2026-03-16",
                "hours": "-2.0",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 400

    def test_create_entry_excessive_hours_rejected(self):
        """TS-014: Hours >24 must be rejected."""
        response = self.api.post(
            "/api/v1/time_entries/",
            {
                "project": self.project.pk,
                "phase": self.phase.pk,
                "date": "2026-03-16",
                "hours": "25.0",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 400

    def test_submit_week(self):
        TimeEntry.objects.create(
            tenant=self.tenant,
            employee=self.user,
            project=self.project,
            date=date(2026, 3, 16),
            hours=7.5,
            status="DRAFT",
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
class TestMandatoryTasksAPI:
    """Endpoint GET /time_entries/mandatory_tasks/ — pour la grille timesheet."""

    def setup_method(self):
        from apps.projects.models import Task

        self.tenant = Tenant.objects.create(name="MT", slug="mt-api")
        self.user = User.objects.create_user(username="emp_m", password="pass123!")
        self.project = Project.objects.create(
            tenant=self.tenant,
            code="INT-01",
            name="Interne",
            status="ACTIVE",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant,
            project=self.project,
            code="C",
            name="Catalogue",
            order=1,
        )
        # Tâches obligatoires
        Task.objects.create(
            tenant=self.tenant,
            project=self.project,
            phase=self.phase,
            wbs_code="C.1",
            name="Congés",
            always_display_in_timesheet=True,
        )
        Task.objects.create(
            tenant=self.tenant,
            project=self.project,
            phase=self.phase,
            wbs_code="C.2",
            name="Administration",
            always_display_in_timesheet=True,
        )
        # Tâche normale (ne doit pas être retournée)
        Task.objects.create(
            tenant=self.tenant,
            project=self.project,
            phase=self.phase,
            wbs_code="C.3",
            name="Tâche normale",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_returns_only_mandatory_tasks(self):
        resp = self.client.get("/api/v1/time_entries/mandatory_tasks/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        names = [t["name"] for t in data]
        assert "Congés" in names
        assert "Administration" in names
        assert "Tâche normale" not in names

    def test_excludes_inactive_projects(self):
        from apps.projects.models import Task

        # Désactive le projet
        self.project.status = "COMPLETED"
        self.project.save()
        # Mais la transition 'COMPLETED' est valide depuis ACTIVE — vérifier blocage absent
        resp = self.client.get("/api/v1/time_entries/mandatory_tasks/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        # Aucune tâche retournée car projet COMPLETED
        assert len(data) == 0
        # Reactiver pour le suivant
        Task.objects.filter(project=self.project).update(is_active=True)

    def test_excludes_inactive_tasks(self):
        from apps.projects.models import Task

        Task.objects.filter(name="Administration").update(is_active=False)
        resp = self.client.get("/api/v1/time_entries/mandatory_tasks/")
        data = resp.json().get("data", resp.json())
        names = [t["name"] for t in data]
        assert "Congés" in names
        assert "Administration" not in names

    def test_anonymous_returns_401(self):
        anon = APIClient()
        resp = anon.get("/api/v1/time_entries/mandatory_tasks/")
        assert resp.status_code in (401, 403)


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
            tenant=self.tenant,
            employee=self.employee,
            week_start=date(2026, 3, 16),
            week_end=date(2026, 3, 22),
        )
        self.api = APIClient()

    def test_pm_approve(self):
        self.api.force_authenticate(user=self.pm)
        response = self.api.post(f"/api/v1/weekly_approvals/{self.approval.pk}/approve_pm/")
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["pm_status"] == "APPROVED"

    def test_self_approval_blocked(self):
        """Employee cannot approve their own timesheet."""
        self.api.force_authenticate(user=self.employee)
        response = self.api.post(f"/api/v1/weekly_approvals/{self.approval.pk}/approve_pm/")
        assert response.status_code == 403


@pytest.mark.django_db
class TestPMDashboardWeekAutodetect:
    """Sans ?week_start, pm_dashboard doit cibler la plus ancienne semaine
    avec des feuilles SUBMITTED en attente (pas la semaine courante)."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="DashAuto", slug="dash-auto")
        self.pm = User.objects.create_user(username="pm_d", password="pass123!")
        self.emp = User.objects.create_user(username="emp_d", password="pass123!")
        from apps.core.models import ProjectRole, Role

        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant,
            code="DASH-1",
            name="Dash",
            pm=self.pm,
            status="ACTIVE",
        )
        # Feuille soumise sur une semaine PASSÉE (loin de la semaine courante)
        TimeEntry.objects.create(
            tenant=self.tenant,
            employee=self.emp,
            project=self.project,
            date=date(2026, 3, 4),
            hours=8,
            status="SUBMITTED",
        )
        WeeklyApproval.objects.create(
            tenant=self.tenant,
            employee=self.emp,
            week_start=date(2026, 3, 2),
            week_end=date(2026, 3, 8),
            pm_status="PENDING",
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def test_pm_dashboard_finds_submitted_week_without_param(self):
        resp = self.api.get("/api/v1/weekly_approvals/pm_dashboard/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        # La semaine retournée doit être celle du 2026-03-04 (lundi 2026-03-02)
        assert data["week_start"] == "2026-03-02"
        assert len(data["employees"]) == 1
        assert data["employees"][0]["week_start"] == "2026-03-02"


@pytest.mark.django_db
class TestPMDashboardAnchorsOnWeeklyApproval:
    """S-080/S-081: la semaine "oldest pending" doit dériver de
    WeeklyApproval(pm_status=PENDING) et pas du statut des TimeEntry.
    Sinon, dès qu'une feuille passe en PM_APPROVED (sans clore le
    WeeklyApproval), le dashboard retombe sur la semaine courante et
    paraît vide alors que le badge en compte encore 1."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Anchor", slug="dash-anchor")
        self.pm = User.objects.create_user(username="pm_anch", password="x")
        self.emp = User.objects.create_user(username="emp_anch", password="x")
        from apps.core.models import ProjectRole, Role, UserTenantAssociation

        UserTenantAssociation.objects.create(user=self.pm, tenant=self.tenant)
        UserTenantAssociation.objects.create(user=self.emp, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant,
            code="ANC-1",
            name="Anchor",
            pm=self.pm,
            status="ACTIVE",
        )
        # Entries déplacées hors de SUBMITTED, mais WeeklyApproval reste PENDING
        TimeEntry.objects.create(
            tenant=self.tenant,
            employee=self.emp,
            project=self.project,
            date=date(2026, 3, 4),
            hours=8,
            status="PM_APPROVED",
        )
        WeeklyApproval.objects.create(
            tenant=self.tenant,
            employee=self.emp,
            week_start=date(2026, 3, 2),
            week_end=date(2026, 3, 8),
            pm_status="PENDING",
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def test_pm_dashboard_lands_on_week_of_pending_approval(self):
        resp = self.api.get("/api/v1/weekly_approvals/pm_dashboard/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["week_start"] == "2026-03-02", (
            "Doit cibler la semaine du WeeklyApproval pending, pas la semaine courante"
        )
        assert len(data["employees"]) == 1
        assert data["employees"][0]["employee_id"] == self.emp.id


@pytest.mark.django_db
class TestPaieDashboardMultiWeek:
    """Sans ?week_start, paie_dashboard doit lister une ligne par
    WeeklyApproval paie_status=PENDING actionnable (finance-approved OU
    interne sans PM), aligné avec le badge — pas tous les employés du
    tenant pour une semaine unique."""

    def setup_method(self):
        from datetime import date

        from apps.core.models import ProjectRole, Role, UserTenantAssociation

        self.tenant = Tenant.objects.create(name="PM", slug="paie-mw")
        self.paie = User.objects.create_user("paie_mw", password="x")
        self.emp = User.objects.create_user("emp_mw", password="x")
        # Plusieurs autres employés actifs (qui n'ont rien à valider)
        self.extras = [
            User.objects.create_user(f"e_mw_{i}", password="x") for i in range(5)
        ]
        UserTenantAssociation.objects.create(user=self.paie, tenant=self.tenant)
        UserTenantAssociation.objects.create(user=self.emp, tenant=self.tenant)
        for e in self.extras:
            UserTenantAssociation.objects.create(user=e, tenant=self.tenant)
        ProjectRole.objects.create(user=self.paie, tenant=self.tenant, role=Role.PAIE)
        self.internal = Project.objects.create(
            tenant=self.tenant, code="INT-CG", name="Congés",
            is_internal=True, pm=None, status="ACTIVE",
        )
        # 2 semaines congés-only en attente paie
        for ws, we in [
            (date(2026, 4, 20), date(2026, 4, 26)),
            (date(2026, 5, 11), date(2026, 5, 17)),
        ]:
            TimeEntry.objects.create(
                tenant=self.tenant, employee=self.emp, project=self.internal,
                date=ws, hours=8, status="SUBMITTED",
            )
            WeeklyApproval.objects.create(
                tenant=self.tenant, employee=self.emp,
                week_start=ws, week_end=we,
                pm_status="PENDING", finance_status="PENDING", paie_status="PENDING",
            )
        self.api = APIClient()
        self.api.force_authenticate(user=self.paie)

    def test_default_lists_only_pending_paie_rows(self):
        resp = self.api.get("/api/v1/weekly_approvals/paie_dashboard/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        weeks = [e["week_start"] for e in data["employees"]]
        assert weeks == ["2026-04-20", "2026-05-11"], (
            "Doit lister une ligne par WA pending paie (multi-semaines), "
            "pas tous les employés actifs"
        )
        assert all(e["employee_id"] == self.emp.id for e in data["employees"])

    def test_explicit_week_start_keeps_compliance_view(self):
        """Avec ?week_start=..., on garde l'ancien comportement
        (tous les employés actifs pour cette semaine)."""
        resp = self.api.get(
            "/api/v1/weekly_approvals/paie_dashboard/?week_start=2026-04-20"
        )
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        # Tous les employés (sauf paie) doivent apparaître
        assert len(data["employees"]) >= 1 + len(self.extras)


@pytest.mark.django_db
class TestPaieValidatesCongesDirectly:
    """Règle métier : une semaine congés/admin (projet interne sans PM) est
    validée par la Paie directement, sans étape PM ni Finance."""

    def setup_method(self):
        from apps.core.models import ProjectRole, Role, UserTenantAssociation

        self.tenant = Tenant.objects.create(name="Conge", slug="conge-paie")
        self.paie = User.objects.create_user("paie_u", password="x")
        self.emp = User.objects.create_user("emp_cg", password="x")
        UserTenantAssociation.objects.create(user=self.paie, tenant=self.tenant)
        UserTenantAssociation.objects.create(user=self.emp, tenant=self.tenant)
        ProjectRole.objects.create(user=self.paie, tenant=self.tenant, role=Role.PAIE)
        self.internal = Project.objects.create(
            tenant=self.tenant,
            code="INT-CG",
            name="Congés",
            is_internal=True,
            pm=None,
            status="ACTIVE",
        )
        self.entry = TimeEntry.objects.create(
            tenant=self.tenant,
            employee=self.emp,
            project=self.internal,
            date=date(2026, 5, 11),
            hours=8,
            status="SUBMITTED",
        )
        self.wa = WeeklyApproval.objects.create(
            tenant=self.tenant,
            employee=self.emp,
            week_start=date(2026, 5, 11),
            week_end=date(2026, 5, 17),
            pm_status="PENDING",
            finance_status="PENDING",
            paie_status="PENDING",
        )
        self.api = APIClient()
        self.api.force_authenticate(user=self.paie)

    def test_paie_can_validate_conges_without_pm_approval(self):
        resp = self.api.post(f"/api/v1/weekly_approvals/{self.wa.pk}/validate_paie/")
        assert resp.status_code == 200
        self.wa.refresh_from_db()
        self.entry.refresh_from_db()
        assert self.wa.paie_status == "APPROVED"
        assert self.entry.status == "PAIE_VALIDATED"

    def test_normal_week_still_requires_pm_approval(self):
        pm_user = User.objects.create_user("pm_cg", password="x")
        proj = Project.objects.create(
            tenant=self.tenant,
            code="P-CG",
            name="Real",
            pm=pm_user,
            status="ACTIVE",
        )
        emp2 = User.objects.create_user("emp2_cg", password="x")
        TimeEntry.objects.create(
            tenant=self.tenant,
            employee=emp2,
            project=proj,
            date=date(2026, 5, 11),
            hours=8,
            status="SUBMITTED",
        )
        wa2 = WeeklyApproval.objects.create(
            tenant=self.tenant,
            employee=emp2,
            week_start=date(2026, 5, 11),
            week_end=date(2026, 5, 17),
            pm_status="PENDING",
            finance_status="PENDING",
            paie_status="PENDING",
        )
        resp = self.api.post(f"/api/v1/weekly_approvals/{wa2.pk}/validate_paie/")
        assert resp.status_code == 400


@pytest.mark.django_db
class TestPMDashboardMultiWeek:
    """S-080/S-081: la vue CP doit lister TOUTES les feuilles en attente du
    PM, toutes semaines confondues (pas seulement une semaine), une ligne
    par (employé, semaine), triées de la plus ancienne à la plus récente."""

    def setup_method(self):
        from apps.core.models import ProjectRole, Role, UserTenantAssociation

        self.tenant = Tenant.objects.create(name="MW", slug="dash-mw")
        self.pm = User.objects.create_user(username="pm_mw", password="x")
        self.emp = User.objects.create_user(username="emp_mw", password="x")
        UserTenantAssociation.objects.create(user=self.pm, tenant=self.tenant)
        UserTenantAssociation.objects.create(user=self.emp, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.project = Project.objects.create(
            tenant=self.tenant,
            code="MW-1",
            name="Multi",
            pm=self.pm,
            status="ACTIVE",
        )
        # Deux semaines en attente pour le même employé
        for ws, we in [
            (date(2026, 3, 2), date(2026, 3, 8)),
            (date(2026, 3, 9), date(2026, 3, 15)),
        ]:
            TimeEntry.objects.create(
                tenant=self.tenant,
                employee=self.emp,
                project=self.project,
                date=ws,
                hours=8,
                status="SUBMITTED",
            )
            WeeklyApproval.objects.create(
                tenant=self.tenant,
                employee=self.emp,
                week_start=ws,
                week_end=we,
                pm_status="PENDING",
            )
        self.api = APIClient()
        self.api.force_authenticate(user=self.pm)

    def test_lists_all_pending_weeks(self):
        resp = self.api.get("/api/v1/weekly_approvals/pm_dashboard/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        weeks = [e["week_start"] for e in data["employees"]]
        assert weeks == ["2026-03-02", "2026-03-09"], (
            "Les deux semaines en attente doivent apparaître, triées"
        )
        assert data["kpis"]["pending_count"] == 2

    def test_week_start_param_still_scopes_to_one_week(self):
        resp = self.api.get("/api/v1/weekly_approvals/pm_dashboard/?week_start=2026-03-09")
        data = resp.json().get("data", resp.json())
        weeks = [e["week_start"] for e in data["employees"]]
        assert weeks == ["2026-03-09"]
