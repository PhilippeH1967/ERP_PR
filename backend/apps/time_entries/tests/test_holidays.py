"""Jours fériés dans la feuille de temps.

- Fériés paramétrés par régime de travail (LaborRule = lieu/province) ou pour
  tous (labor_rule null). Deux provinces peuvent avoir des fériés différents,
  y compris à la même date.
- Endpoint ``time_entries/holidays`` : fériés de la semaine pour l'employé
  courant, avec SES heures/jour (override personnel → /5, sinon daily_hours du
  régime, sinon 8).
- Action ``prefill_holidays`` : pré-remplit la tâche obligatoire « Férié » au
  max d'heures/jour de la personne. Idempotente.
"""

import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.test import APIClient

from apps.core.models import LaborRule, Tenant, UserTenantAssociation
from apps.leaves.models import PublicHoliday
from apps.projects.models import Phase, Project, Task
from apps.time_entries.models import TimeEntry


@pytest.fixture
def env(db):
    tenant = Tenant.objects.create(name="T", slug="t-holidays")
    qc = LaborRule.objects.create(tenant=tenant, name="Québec 37.5h", weekly_hours=37.5, daily_hours=7.5)
    on = LaborRule.objects.create(tenant=tenant, name="Ontario 40h", weekly_hours=40, daily_hours=8)
    user = User.objects.create_user(username="emp_hol", password="x")
    assoc = UserTenantAssociation.objects.create(user=user, tenant=tenant, labor_rule=qc)
    # Tâche obligatoire « Férié » (projet interne)
    project = Project.objects.create(tenant=tenant, code="INT-01", name="Interne", is_internal=True)
    phase = Phase.objects.create(tenant=tenant, project=project, code="ABS", name="Absences")
    ferie = Task.objects.create(
        tenant=tenant, project=project, phase=phase, wbs_code="ABS.4",
        name="Férié", always_display_in_timesheet=True, is_billable=False,
    )
    api = APIClient()
    api.force_authenticate(user=user)
    return {
        "tenant": tenant, "qc": qc, "on": on, "user": user, "assoc": assoc,
        "project": project, "ferie": ferie, "api": api,
    }


@pytest.mark.django_db
class TestPublicHolidayConstraints:
    def test_same_date_two_provinces_allowed(self, env):
        PublicHoliday.objects.create(
            tenant=env["tenant"], name="Fête nationale", date="2026-06-24", labor_rule=env["qc"]
        )
        h2 = PublicHoliday.objects.create(
            tenant=env["tenant"], name="Autre férié", date="2026-06-24", labor_rule=env["on"]
        )
        assert h2.pk is not None

    def test_duplicate_same_rule_rejected(self, env):
        PublicHoliday.objects.create(
            tenant=env["tenant"], name="Noël", date="2026-12-25", labor_rule=env["qc"]
        )
        with pytest.raises(IntegrityError):
            PublicHoliday.objects.create(
                tenant=env["tenant"], name="Noël bis", date="2026-12-25", labor_rule=env["qc"]
            )

    def test_duplicate_global_rejected(self, env):
        PublicHoliday.objects.create(tenant=env["tenant"], name="Jour de l'an", date="2027-01-01")
        with pytest.raises(IntegrityError):
            PublicHoliday.objects.create(tenant=env["tenant"], name="Bis", date="2027-01-01")


@pytest.mark.django_db
class TestHolidaysWeekEndpoint:
    def _get(self, env, week="2026-06-22"):
        return env["api"].get(
            "/api/v1/time_entries/holidays/",
            {"week_start": week},
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )

    def test_returns_user_jurisdiction_and_global_holidays(self, env):
        PublicHoliday.objects.create(tenant=env["tenant"], name="Fête nationale", date="2026-06-24", labor_rule=env["qc"])
        PublicHoliday.objects.create(tenant=env["tenant"], name="Férié Ontario", date="2026-06-25", labor_rule=env["on"])
        PublicHoliday.objects.create(tenant=env["tenant"], name="Global", date="2026-06-26")
        resp = self._get(env)
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        dates = {h["date"] for h in data}
        assert dates == {"2026-06-24", "2026-06-26"}  # pas le férié Ontario

    def test_daily_hours_from_labor_rule(self, env):
        PublicHoliday.objects.create(tenant=env["tenant"], name="FN", date="2026-06-24", labor_rule=env["qc"])
        data = self._get(env).json().get("data")
        assert data[0]["daily_hours"] == 7.5  # daily_hours du régime QC

    def test_daily_hours_from_personal_override(self, env):
        env["assoc"].contract_hours_override = 30  # temps partiel → 6 h/jour
        env["assoc"].save()
        PublicHoliday.objects.create(tenant=env["tenant"], name="FN", date="2026-06-24", labor_rule=env["qc"])
        data = self._get(env).json().get("data")
        assert data[0]["daily_hours"] == 6.0


@pytest.mark.django_db
class TestPrefillHolidays:
    def _prefill(self, env, week="2026-06-22"):
        return env["api"].post(
            "/api/v1/time_entries/prefill_holidays/",
            {"week_start": week},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )

    def test_creates_draft_entry_on_ferie_task_with_personal_daily_hours(self, env):
        PublicHoliday.objects.create(tenant=env["tenant"], name="FN", date="2026-06-24", labor_rule=env["qc"])
        resp = self._prefill(env)
        assert resp.status_code == 200, resp.data
        entry = TimeEntry.objects.get(employee=env["user"], date="2026-06-24")
        assert entry.task_id == env["ferie"].pk
        assert float(entry.hours) == 7.5
        assert entry.status == "DRAFT"

    def test_idempotent_and_respects_user_edits(self, env):
        PublicHoliday.objects.create(tenant=env["tenant"], name="FN", date="2026-06-24", labor_rule=env["qc"])
        self._prefill(env)
        # L'employé corrige à 4 h (a travaillé une partie du férié)
        TimeEntry.objects.filter(employee=env["user"], date="2026-06-24").update(hours=4)
        self._prefill(env)
        entries = TimeEntry.objects.filter(employee=env["user"], date="2026-06-24")
        assert entries.count() == 1
        assert float(entries.first().hours) == 4.0  # pas écrasé

    def test_other_province_holiday_not_prefilled(self, env):
        PublicHoliday.objects.create(tenant=env["tenant"], name="ON only", date="2026-06-25", labor_rule=env["on"])
        self._prefill(env)
        assert not TimeEntry.objects.filter(employee=env["user"], date="2026-06-25").exists()

    def test_unpaid_holiday_not_prefilled(self, env):
        PublicHoliday.objects.create(
            tenant=env["tenant"], name="Non payé", date="2026-06-24",
            labor_rule=env["qc"], is_paid=False,
        )
        self._prefill(env)
        assert not TimeEntry.objects.filter(employee=env["user"], date="2026-06-24").exists()

    def test_no_ferie_task_returns_zero(self, env):
        env["ferie"].delete()
        PublicHoliday.objects.create(tenant=env["tenant"], name="FN", date="2026-06-24", labor_rule=env["qc"])
        resp = self._prefill(env)
        assert resp.status_code == 200
        assert resp.json().get("data", resp.json())["created"] == 0


@pytest.mark.django_db
class TestPublicHolidayPermissions:
    def test_employee_cannot_create_holiday(self, env):
        resp = env["api"].post(
            "/api/v1/public_holidays/",
            {"name": "Hack", "date": "2026-07-01"},
            format="json", HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 403

    def test_admin_can_create_holiday(self, env):
        from apps.core.models import ProjectRole, Role

        admin = User.objects.create_user(username="adm_hol", password="x")
        ProjectRole.objects.create(tenant=env["tenant"], user=admin, role=Role.ADMIN)
        api = APIClient()
        api.force_authenticate(user=admin)
        resp = api.post(
            "/api/v1/public_holidays/",
            {"name": "Fête du Canada", "date": "2026-07-01", "labor_rule": env["on"].pk},
            format="json", HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 201, resp.data
