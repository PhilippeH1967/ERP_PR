"""Tests for amendment-scoped phases/tasks (story 12.1 Phase B).

A Phase or Task can optionally belong to an Amendment (nullable FK).
Covers:
- Default value is NULL (phases/tasks belong to the main project)
- Reverse accessors amendment.phases / amendment.tasks
- Cascade delete when amendment is removed
- QuerySet helpers to filter main vs amendment-scoped items
"""

from __future__ import annotations

import pytest

from apps.projects.models import Phase, Task

from .conftest import AmendmentFactory, PhaseFactory, TaskFactory


@pytest.mark.django_db
class TestAmendmentScopeOnPhase:
    def test_phase_amendment_is_nullable_by_default(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant)
        assert phase.amendment_id is None

    def test_phase_can_be_attached_to_amendment(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        phase = PhaseFactory(
            project=project, tenant=project.tenant, amendment=amd, name="Scope addition"
        )
        assert phase.amendment_id == amd.pk

    def test_reverse_accessor_amendment_phases(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        PhaseFactory(project=project, tenant=project.tenant, amendment=amd, name="P1")
        PhaseFactory(project=project, tenant=project.tenant, amendment=amd, name="P2")
        PhaseFactory(project=project, tenant=project.tenant, name="Main")
        assert amd.phases.count() == 2

    def test_deleting_amendment_cascades_its_phases(self, project):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        PhaseFactory(project=project, tenant=project.tenant, amendment=amd)
        main_phase = PhaseFactory(project=project, tenant=project.tenant)
        amd.delete()
        # Only the main-project phase remains
        assert Phase.objects.filter(project=project).count() == 1
        assert Phase.objects.filter(pk=main_phase.pk).exists()


@pytest.mark.django_db
class TestAmendmentScopeOnTask:
    def test_task_amendment_is_nullable_by_default(self, project, phase):
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="T1")
        assert task.amendment_id is None

    def test_task_can_be_attached_to_amendment(self, project, phase):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.1",
            amendment=amd,
        )
        assert task.amendment_id == amd.pk

    def test_reverse_accessor_amendment_tasks(self, project, phase):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.1",
            amendment=amd,
        )
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.2",
            amendment=amd,
        )
        TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="MAIN.1")
        assert amd.tasks.count() == 2

    def test_deleting_amendment_cascades_its_tasks(self, project, phase):
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.1",
            amendment=amd,
        )
        main_task = TaskFactory(
            project=project, phase=phase, tenant=project.tenant, wbs_code="MAIN.1"
        )
        amd.delete()
        assert Task.objects.filter(project=project).count() == 1
        assert Task.objects.filter(pk=main_task.pk).exists()


@pytest.mark.django_db
class TestAmendmentScopeQuerysets:
    def test_main_project_phases_exclude_amendment_phases(self, project):
        """project.phases.filter(amendment__isnull=True) returns only main phases."""
        amd = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        PhaseFactory(project=project, tenant=project.tenant, name="Main 1")
        PhaseFactory(project=project, tenant=project.tenant, name="Main 2")
        PhaseFactory(project=project, tenant=project.tenant, amendment=amd, name="Avenant 1")
        main = project.phases.filter(amendment__isnull=True)
        assert main.count() == 2
        assert set(main.values_list("name", flat=True)) == {"Main 1", "Main 2"}

    def test_amendment_tasks_grouped_by_amendment(self, project, phase):
        amd1 = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        amd2 = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=2)
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.1",
            amendment=amd1,
        )
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV1.2",
            amendment=amd1,
        )
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="AV2.1",
            amendment=amd2,
        )
        assert amd1.tasks.count() == 2
        assert amd2.tasks.count() == 1
