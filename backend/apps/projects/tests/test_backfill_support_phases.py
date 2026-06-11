"""Tests de la commande backfill_support_phases.

Rattrape les projets créés avant la conversion « services transversaux →
phases SUPPORT imputables » : services présents dans le JSON
``services_transversaux`` mais sans phase SUPPORT, ou phase SUPPORT sans
tâche feuille.
"""

import pytest
from django.core.management import call_command

from apps.projects.models import Phase, Task

from .conftest import ProjectFactory


@pytest.mark.django_db
class TestBackfillSupportPhases:
    def test_creates_missing_support_phase_and_task(self, tenant):
        project = ProjectFactory(
            tenant=tenant, code="BF-1", services_transversaux=["BIM", "DD"]
        )
        assert project.phases.count() == 0

        call_command("backfill_support_phases")

        phases = project.phases.filter(phase_type=Phase.PhaseType.SUPPORT)
        assert set(phases.values_list("code", flat=True)) == {"BIM", "DD"}
        for ph in phases:
            assert Task.objects.filter(phase=ph, parent__isnull=True).count() == 1

    def test_adds_leaf_task_to_taskless_support_phase(self, tenant):
        project = ProjectFactory(tenant=tenant, code="BF-2", services_transversaux=[])
        ph = Phase.objects.create(
            tenant=tenant, project=project, code="BIM",
            name="BIM / Modélisation", phase_type=Phase.PhaseType.SUPPORT,
        )
        call_command("backfill_support_phases")
        tasks = Task.objects.filter(phase=ph)
        assert tasks.count() == 1
        assert tasks.first().name == "BIM / Modélisation"

    def test_idempotent(self, tenant):
        project = ProjectFactory(
            tenant=tenant, code="BF-3", services_transversaux=["BIM"]
        )
        call_command("backfill_support_phases")
        call_command("backfill_support_phases")
        assert (
            project.phases.filter(
                phase_type=Phase.PhaseType.SUPPORT, code="BIM"
            ).count()
            == 1
        )
        assert Task.objects.filter(project=project).count() == 1

    def test_untouched_project_stays_untouched(self, tenant):
        project = ProjectFactory(tenant=tenant, code="BF-4", services_transversaux=[])
        call_command("backfill_support_phases")
        assert project.phases.count() == 0

    def test_dry_run_changes_nothing(self, tenant):
        project = ProjectFactory(
            tenant=tenant, code="BF-5", services_transversaux=["BIM"]
        )
        call_command("backfill_support_phases", "--dry-run")
        assert project.phases.count() == 0
