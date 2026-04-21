"""Tests for the Task model (WBS operational unit, replaces WBSElement)."""

from __future__ import annotations

import pytest
from django.db import IntegrityError

from apps.projects.models import Task

from .conftest import TaskFactory


@pytest.mark.django_db
class TestTaskModel:
    def test_create_task_defaults(self, project, phase):
        task = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="1.1")
        assert task.pk is not None
        assert task.task_type == "TASK"
        assert task.billing_mode == "FORFAIT"
        assert task.is_billable is True
        assert task.is_active is True
        assert task.progress_pct == 0

    def test_task_str_uses_client_label_when_present(self, project, phase):
        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="1.2",
            name="Analyse",
            client_facing_label="Phase 1 — Analyse du site",
        )
        assert str(task) == "1.2 — Phase 1 — Analyse du site"

    def test_task_str_falls_back_to_name_when_no_client_label(self, project, phase):
        task = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="1.3",
            name="Relevé",
            client_facing_label="",
        )
        assert str(task) == "1.3 — Relevé"

    def test_task_wbs_code_unique_per_project(self, project, phase):
        TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="2.1")
        with pytest.raises(IntegrityError):
            TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="2.1")

    def test_task_wbs_code_can_repeat_across_projects(self, tenant):
        from .conftest import PhaseFactory, ProjectFactory

        p1 = ProjectFactory(tenant=tenant, code="A-1")
        p2 = ProjectFactory(tenant=tenant, code="A-2")
        ph1 = PhaseFactory(project=p1, tenant=tenant)
        ph2 = PhaseFactory(project=p2, tenant=tenant)
        TaskFactory(project=p1, phase=ph1, tenant=tenant, wbs_code="1.1")
        # same wbs_code on a different project must be allowed
        TaskFactory(project=p2, phase=ph2, tenant=tenant, wbs_code="1.1")
        assert Task.objects.filter(wbs_code="1.1").count() == 2

    def test_task_parent_children_hierarchy(self, project, phase):
        parent = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="3")
        child = TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="3.1",
            parent=parent,
            task_type="SUBTASK",
        )
        assert child.parent_id == parent.pk
        assert parent.subtasks.count() == 1
        assert parent.subtasks.first().pk == child.pk

    def test_cascade_delete_via_project(self, project, phase):
        TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="9.1")
        project.delete()
        assert Task.objects.count() == 0

    def test_cascade_delete_via_phase(self, project, phase):
        TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="9.2")
        phase.delete()
        assert Task.objects.count() == 0

    def test_cascade_delete_subtasks_when_parent_deleted(self, project, phase):
        parent = TaskFactory(project=project, phase=phase, tenant=project.tenant, wbs_code="4")
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="4.1",
            parent=parent,
        )
        TaskFactory(
            project=project,
            phase=phase,
            tenant=project.tenant,
            wbs_code="4.2",
            parent=parent,
        )
        assert Task.objects.count() == 3
        parent.delete()
        assert Task.objects.count() == 0

    def test_ordering_by_phase_then_order_then_wbs_code(self, project):
        from .conftest import PhaseFactory

        ph_a = PhaseFactory(project=project, tenant=project.tenant, order=1)
        ph_b = PhaseFactory(project=project, tenant=project.tenant, order=2)
        t2 = TaskFactory(
            project=project, phase=ph_b, tenant=project.tenant, wbs_code="2.1", order=0
        )
        t1_second = TaskFactory(
            project=project, phase=ph_a, tenant=project.tenant, wbs_code="1.2", order=1
        )
        t1_first = TaskFactory(
            project=project, phase=ph_a, tenant=project.tenant, wbs_code="1.1", order=0
        )
        ordered_pks = list(Task.objects.values_list("pk", flat=True))
        assert ordered_pks == [t1_first.pk, t1_second.pk, t2.pk]
