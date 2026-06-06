"""Catalogue de tâches standard par phase (paramétrage admin) + suggestions.

- Écriture réservée aux ADMIN (les PM ne définissent pas le catalogue).
- Seed idempotent.
- Endpoint task_suggestions : tâches standard groupées par phase du projet,
  avec le drapeau has_tasks (le picker n'est proposé qu'à l'état vide).
"""

from __future__ import annotations

import pytest
from django.core.management import call_command

from apps.projects.models import StandardPhase, StandardTask

URL = "/api/v1/standard_tasks/"


@pytest.mark.django_db
class TestStandardTaskPermissions:
    def test_anonymous_cannot_list(self, anonymous_client):
        assert anonymous_client.get(URL).status_code in (401, 403)

    def test_authenticated_can_list(self, employee_client, tenant):
        sp = StandardPhase.objects.create(tenant=tenant, code="1", name="Concept")
        StandardTask.objects.create(tenant=tenant, standard_phase=sp, name="Esquisse")
        assert employee_client.get(URL).status_code == 200

    def test_admin_can_create(self, admin_client, tenant):
        sp = StandardPhase.objects.create(tenant=tenant, code="1", name="Concept")
        resp = admin_client.post(
            URL,
            {"standard_phase": sp.id, "name": "Esquisse", "billing_mode": "FORFAIT"},
            format="json",
        )
        assert resp.status_code == 201
        assert StandardTask.objects.filter(name="Esquisse").exists()

    def test_pm_cannot_create(self, pm_client, tenant):
        sp = StandardPhase.objects.create(tenant=tenant, code="1", name="Concept")
        resp = pm_client.post(
            URL,
            {"standard_phase": sp.id, "name": "Interdite", "billing_mode": "FORFAIT"},
            format="json",
        )
        assert resp.status_code == 403
        assert not StandardTask.objects.filter(name="Interdite").exists()


@pytest.mark.django_db
class TestSeedStandardTasks:
    def test_seed_creates_catalog(self, tenant):
        call_command("seed_standard_phases", tenant_id=tenant.id)
        call_command("seed_standard_tasks", tenant_id=tenant.id)
        concept = StandardPhase.objects.get(tenant=tenant, code="1")
        names = set(
            StandardTask.objects.filter(standard_phase=concept).values_list("name", flat=True)
        )
        assert "Esquisse et options conceptuelles" in names

    def test_seed_idempotent(self, tenant):
        call_command("seed_standard_phases", tenant_id=tenant.id)
        call_command("seed_standard_tasks", tenant_id=tenant.id)
        n1 = StandardTask.objects.filter(tenant=tenant).count()
        call_command("seed_standard_tasks", tenant_id=tenant.id)
        n2 = StandardTask.objects.filter(tenant=tenant).count()
        assert n1 == n2 and n1 > 0


@pytest.mark.django_db
class TestTaskSuggestionsEndpoint:
    def test_suggestions_grouped_by_phase_when_empty(self, admin_client, tenant):
        call_command("seed_standard_phases", tenant_id=tenant.id)
        call_command("seed_standard_tasks", tenant_id=tenant.id)
        resp = admin_client.post(
            "/api/v1/projects/",
            {"code": "PRJ-S", "name": "Sugg", "is_internal": True},
            format="json",
        )
        pid = resp.json().get("data", resp.json())["id"]
        r = admin_client.get(f"/api/v1/projects/{pid}/task_suggestions/")
        assert r.status_code == 200
        body = r.json().get("data", r.json())
        assert body["has_tasks"] is False
        names = {t["name"] for g in body["groups"] for t in g["tasks"]}
        assert "Esquisse et options conceptuelles" in names

    def test_has_tasks_true_when_project_has_tasks(self, admin_client, project, task):
        r = admin_client.get(f"/api/v1/projects/{project.id}/task_suggestions/")
        body = r.json().get("data", r.json())
        assert body["has_tasks"] is True
