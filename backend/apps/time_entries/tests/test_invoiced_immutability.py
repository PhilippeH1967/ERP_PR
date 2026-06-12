"""Heures facturées intouchables — tous les chemins d'écriture.

La PR #73 a posé le garde ENTRY_INVOICED sur update()/destroy() uniquement.
Ces tests couvrent les chemins restants :

- ``bulk_correct`` / ``transfer_hours`` (Finance) refusent les entrées facturées ;
- les rejets (``reject_entries``, ``reject_pm``) n'ont pas le droit de repasser
  une entrée facturée en DRAFT ;
- garde au niveau modèle : ``save()`` refuse de modifier les champs protégés,
  la suppression (directe ou en cascade depuis la tâche) est refusée.
"""

from datetime import date

import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import ProtectedError
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Phase, Project, Task
from apps.time_entries.models import TimeEntry, WeeklyApproval


@pytest.fixture
def env(db):
    tenant = Tenant.objects.create(name="T", slug="t-inv")
    pm = User.objects.create_user(username="pm_inv", password="x")
    project = Project.objects.create(tenant=tenant, code="INV1", name="P", pm=pm)
    phase = Phase.objects.create(tenant=tenant, project=project, name="Ph")
    task = Task.objects.create(
        tenant=tenant, project=project, phase=phase, wbs_code="1.1", name="T1"
    )
    employee = User.objects.create_user(username="emp_inv", password="x")
    finance = User.objects.create_user(username="fin_inv", password="x")
    ProjectRole.objects.create(tenant=tenant, user=finance, role=Role.FINANCE)
    ProjectRole.objects.create(tenant=tenant, user=pm, role=Role.PM)
    api = APIClient()
    return {
        "tenant": tenant,
        "project": project,
        "phase": phase,
        "task": task,
        "employee": employee,
        "pm": pm,
        "finance": finance,
        "api": api,
    }


def _entry(env, *, invoiced: bool, status: str = "PM_APPROVED", **kw):
    defaults = {
        "tenant": env["tenant"],
        "employee": env["employee"],
        "project": env["project"],
        "task": env["task"],
        "date": date(2026, 3, 16),
        "hours": 7,
        "status": status,
        "is_invoiced": invoiced,
    }
    defaults.update(kw)
    return TimeEntry.objects.create(**defaults)


@pytest.mark.django_db
class TestBulkCorrectInvoiced:
    def test_bulk_correct_invoiced_entry_rejected(self, env):
        e = _entry(env, invoiced=True)
        env["api"].force_authenticate(user=env["finance"])
        resp = env["api"].post(
            "/api/v1/time_entries/bulk_correct/",
            {"corrections": [{"entry_id": e.pk, "hours": "2"}]},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["corrected_count"] == 0
        assert any("factur" in err["message"].lower() for err in data["errors"])
        e.refresh_from_db()
        assert float(e.hours) == 7

    def test_bulk_correct_non_invoiced_still_works(self, env):
        e = _entry(env, invoiced=False)
        env["api"].force_authenticate(user=env["finance"])
        resp = env["api"].post(
            "/api/v1/time_entries/bulk_correct/",
            {"corrections": [{"entry_id": e.pk, "hours": "2"}]},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        data = resp.json().get("data", resp.json())
        assert data["corrected_count"] == 1
        e.refresh_from_db()
        assert float(e.hours) == 2


@pytest.mark.django_db
class TestTransferHoursInvoiced:
    def _other_project(self, env):
        return Project.objects.create(tenant=env["tenant"], code="INV2", name="P2")

    def test_transfer_invoiced_entry_rejected(self, env):
        e = _entry(env, invoiced=True)
        target = self._other_project(env)
        env["api"].force_authenticate(user=env["finance"])
        resp = env["api"].post(
            "/api/v1/time_entries/transfer_hours/",
            {"entry_ids": [e.pk], "target_project": target.pk},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 400
        assert "factur" in str(resp.data).lower()
        e.refresh_from_db()
        assert e.project_id == env["project"].pk

    def test_transfer_non_invoiced_ok(self, env):
        e = _entry(env, invoiced=False)
        target = self._other_project(env)
        env["api"].force_authenticate(user=env["finance"])
        resp = env["api"].post(
            "/api/v1/time_entries/transfer_hours/",
            {"entry_ids": [e.pk], "target_project": target.pk},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 200
        e.refresh_from_db()
        assert e.project_id == target.pk


@pytest.mark.django_db
class TestRejectExcludesInvoiced:
    def test_reject_entries_skips_invoiced(self, env):
        invoiced = _entry(env, invoiced=True, status="SUBMITTED")
        normal = _entry(env, invoiced=False, status="SUBMITTED", date=date(2026, 3, 17))
        env["api"].force_authenticate(user=env["pm"])
        resp = env["api"].post(
            "/api/v1/time_entries/reject_entries/",
            {"entry_ids": [invoiced.pk, normal.pk], "reason": "erreur"},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["rejected_count"] == 1
        invoiced.refresh_from_db()
        normal.refresh_from_db()
        assert invoiced.status == "SUBMITTED"
        assert normal.status == "DRAFT"

    def test_reject_pm_weekly_skips_invoiced(self, env):
        week_start = date(2026, 3, 16)  # un lundi
        invoiced = _entry(env, invoiced=True, status="SUBMITTED")
        normal = _entry(env, invoiced=False, status="SUBMITTED", date=date(2026, 3, 17))
        approval = WeeklyApproval.objects.create(
            tenant=env["tenant"],
            employee=env["employee"],
            week_start=week_start,
            week_end=date(2026, 3, 22),
        )
        env["api"].force_authenticate(user=env["pm"])
        resp = env["api"].post(
            f"/api/v1/weekly_approvals/{approval.pk}/reject_pm/",
            {"reason": "erreur"},
            format="json",
            HTTP_X_TENANT_ID=str(env["tenant"].pk),
        )
        assert resp.status_code == 200
        invoiced.refresh_from_db()
        normal.refresh_from_db()
        assert invoiced.status == "SUBMITTED"
        assert normal.status == "DRAFT"


@pytest.mark.django_db
class TestModelLevelGuard:
    def test_save_modifying_invoiced_hours_raises(self, env):
        e = _entry(env, invoiced=True)
        e.hours = 2
        with pytest.raises(ValidationError):
            e.save()

    def test_save_moving_invoiced_entry_raises(self, env):
        e = _entry(env, invoiced=True)
        other = Project.objects.create(tenant=env["tenant"], code="INV3", name="P3")
        e.project = other
        e.task = None
        with pytest.raises(ValidationError):
            e.save()

    def test_save_status_transition_allowed_on_invoiced(self, env):
        e = _entry(env, invoiced=True, status="PM_APPROVED")
        e.status = "LOCKED"
        e.save()
        e.refresh_from_db()
        assert e.status == "LOCKED"

    def test_setting_invoiced_flag_via_save_allowed(self, env):
        e = _entry(env, invoiced=False)
        e.is_invoiced = True
        e.save()
        e.refresh_from_db()
        assert e.is_invoiced is True

    def test_delete_invoiced_raises_protected(self, env):
        e = _entry(env, invoiced=True)
        # transaction.atomic : le collector Django supprime avec savepoint=False,
        # il faut un savepoint englobant pour interroger la base après l'erreur.
        with pytest.raises(ProtectedError), transaction.atomic():
            e.delete()
        assert TimeEntry.objects.filter(pk=e.pk).exists()

    def test_task_delete_blocked_when_invoiced_entries(self, env):
        e = _entry(env, invoiced=True)
        with pytest.raises(ProtectedError), transaction.atomic():
            env["task"].delete()
        assert TimeEntry.objects.filter(pk=e.pk).exists()
        assert Task.objects.filter(pk=env["task"].pk).exists()

    def test_task_delete_ok_without_invoiced_entries(self, env):
        _entry(env, invoiced=False)
        env["task"].delete()
        assert not Task.objects.filter(pk=env["task"].pk).exists()


@pytest.mark.django_db
class TestTaskApiDestroyGuard:
    def _url(self, env):
        return f"/api/v1/projects/{env['project'].pk}/tasks/{env['task'].pk}/"

    def test_api_task_destroy_with_invoiced_entries_rejected(self, env):
        _entry(env, invoiced=True)
        env["api"].force_authenticate(user=env["pm"])
        resp = env["api"].delete(self._url(env), HTTP_X_TENANT_ID=str(env["tenant"].pk))
        assert resp.status_code == 400
        assert "factur" in str(resp.data).lower()
        assert Task.objects.filter(pk=env["task"].pk).exists()

    def test_api_task_destroy_without_invoiced_entries_ok(self, env):
        _entry(env, invoiced=False)
        env["api"].force_authenticate(user=env["pm"])
        resp = env["api"].delete(self._url(env), HTTP_X_TENANT_ID=str(env["tenant"].pk))
        assert resp.status_code == 204
        assert not Task.objects.filter(pk=env["task"].pk).exists()
