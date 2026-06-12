"""Discipline de soumission des feuilles de temps.

- ``unsubmitted_weeks`` : semaines passées avec des entrées encore en
  brouillon (non soumises).
- Blocage : s'il reste une semaine non soumise vieille de 2 semaines ou plus,
  la saisie dans la semaine courante est refusée (mais la régularisation des
  semaines en retard reste possible).
- Heures facturées (is_invoiced) : ni modifiables ni supprimables.
"""

from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant
from apps.projects.models import Phase, Project, Task
from apps.time_entries.models import TimeEntry


def _monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


@pytest.fixture
def env(db):
    tenant = Tenant.objects.create(name="T", slug="t-disc")
    project = Project.objects.create(tenant=tenant, code="DIS1", name="P")
    phase = Phase.objects.create(tenant=tenant, project=project, name="Ph")
    task = Task.objects.create(
        tenant=tenant, project=project, phase=phase, wbs_code="1.1", name="T1"
    )
    user = User.objects.create_user(username="emp_disc", password="x")
    api = APIClient()
    api.force_authenticate(user=user)
    return {"tenant": tenant, "project": project, "task": task, "user": user, "api": api}


@pytest.mark.django_db
class TestUnsubmittedWeeks:
    def test_lists_past_weeks_with_draft_entries(self, env):
        this_monday = _monday(date.today())
        w1 = this_monday - timedelta(days=7)   # semaine précédente
        w3 = this_monday - timedelta(days=21)  # il y a 3 semaines
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=w1 + timedelta(days=1), hours=7, status="DRAFT",
        )
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=w3, hours=7, status="DRAFT",
        )
        # Une semaine soumise n'apparaît pas
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=this_monday - timedelta(days=14), hours=7,
            status="SUBMITTED",
        )
        resp = env["api"].get(
            "/api/v1/time_entries/unsubmitted_weeks/",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["weeks"] == sorted([w3.isoformat(), w1.isoformat()])
        assert data["blocking"] is True  # w3 a ≥ 2 semaines

    def test_only_previous_week_late_is_not_blocking(self, env):
        this_monday = _monday(date.today())
        w1 = this_monday - timedelta(days=7)
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=w1, hours=7, status="DRAFT",
        )
        data = env["api"].get(
            "/api/v1/time_entries/unsubmitted_weeks/",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        ).json().get("data")
        assert data["weeks"] == [w1.isoformat()]
        assert data["blocking"] is False


@pytest.mark.django_db
class TestLateSubmissionBlocksCurrentWeek:
    def _post(self, env, d: date):
        return env["api"].post(
            "/api/v1/time_entries/",
            {"project": env["project"].pk, "task": env["task"].pk,
             "date": d.isoformat(), "hours": "4"},
            format="json", HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )

    def test_current_week_entry_blocked_when_2w_late(self, env):
        this_monday = _monday(date.today())
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=this_monday - timedelta(days=21), hours=7,
            status="DRAFT",
        )
        resp = self._post(env, this_monday)
        assert resp.status_code == 400
        assert "soumettre" in str(resp.data).lower() or "soumise" in str(resp.data).lower()

    def test_late_week_can_still_be_completed(self, env):
        this_monday = _monday(date.today())
        late_monday = this_monday - timedelta(days=21)
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=late_monday, hours=7, status="DRAFT",
        )
        # Régulariser la semaine en retard reste permis (autre jour, même semaine)
        resp = self._post(env, late_monday + timedelta(days=1))
        assert resp.status_code == 201, resp.data

    def test_current_week_ok_when_only_previous_week_late(self, env):
        this_monday = _monday(date.today())
        TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=this_monday - timedelta(days=7), hours=7,
            status="DRAFT",
        )
        resp = self._post(env, this_monday)
        assert resp.status_code == 201, resp.data


@pytest.mark.django_db
class TestInvoicedEntriesImmutable:
    def _entry(self, env, **kw):
        return TimeEntry.objects.create(
            tenant=env["tenant"], employee=env["user"], project=env["project"],
            task=env["task"], date=date(2026, 3, 16), hours=7,
            status="PM_APPROVED", is_invoiced=True, **kw,
        )

    def test_update_invoiced_entry_rejected(self, env):
        e = self._entry(env)
        resp = env["api"].patch(
            f"/api/v1/time_entries/{e.pk}/",
            {"hours": "2", "version": e.version},
            format="json", HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 400
        assert "factur" in str(resp.data).lower()
        e.refresh_from_db()
        assert float(e.hours) == 7

    def test_delete_invoiced_entry_rejected(self, env):
        e = self._entry(env)
        resp = env["api"].delete(
            f"/api/v1/time_entries/{e.pk}/",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 400
        assert TimeEntry.objects.filter(pk=e.pk).exists()
