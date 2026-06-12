"""Projet interne + tâches obligatoires de la feuille de temps (commande seed).

Régression : le script de nettoyage de la base supprime Project/Phase/Task ;
sans recréation, la grille de saisie n'affiche plus les lignes obligatoires
(Congés, Formation, Maladie, Férié). Cette commande les restaure de façon idempotente,
pour un ou tous les tenants.
"""

from __future__ import annotations

import pytest
from django.core.management import call_command

from apps.projects.models import Project, Task

MANDATORY_NAMES = {"Congés", "Formation", "Maladie", "Férié"}


@pytest.mark.django_db
class TestSeedInternalMandatoryTasks:
    def test_creates_internal_project_and_mandatory_tasks(self, tenant):
        call_command("seed_internal_mandatory_tasks", tenant_id=tenant.id)

        project = Project.objects.get(tenant=tenant, code="INT-01")
        assert project.is_internal is True
        assert project.status == "ACTIVE"

        tasks = Task.objects.filter(tenant=tenant, always_display_in_timesheet=True)
        assert set(tasks.values_list("name", flat=True)) == MANDATORY_NAMES
        # Saisissables (feuilles), actives et non-facturables (temps interne).
        for t in tasks:
            assert t.is_active is True
            assert t.is_billable is False
            assert t.project_id == project.id

    def test_is_idempotent(self, tenant):
        call_command("seed_internal_mandatory_tasks", tenant_id=tenant.id)
        n1 = Task.objects.filter(tenant=tenant, always_display_in_timesheet=True).count()
        call_command("seed_internal_mandatory_tasks", tenant_id=tenant.id)
        n2 = Task.objects.filter(tenant=tenant, always_display_in_timesheet=True).count()
        assert n1 == n2 == 4

    def test_tasks_returned_by_mandatory_endpoint(self, employee_client, tenant):
        """Bout-en-bout : les tâches seedées remontent bien dans la grille."""
        call_command("seed_internal_mandatory_tasks", tenant_id=tenant.id)
        resp = employee_client.get("/api/v1/time_entries/mandatory_tasks/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        names = {t["name"] for t in data}
        assert MANDATORY_NAMES.issubset(names)
