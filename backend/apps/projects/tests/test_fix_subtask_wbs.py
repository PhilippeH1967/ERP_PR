"""Tests de la commande fix_subtask_wbs (rétro-correction WBS sous-tâches)."""

from __future__ import annotations

import pytest
from django.core.management import call_command

from .conftest import PhaseFactory, ProjectFactory, TaskFactory


@pytest.mark.django_db
class TestFixSubtaskWbs:
    def _setup(self, tenant, parent_wbs="1.1"):
        project = ProjectFactory(tenant=tenant)
        phase = PhaseFactory(project=project, tenant=tenant, code="1")
        parent = TaskFactory(
            project=project,
            phase=phase,
            tenant=tenant,
            wbs_code=parent_wbs,
            task_type="TASK",
        )
        return project, phase, parent

    def test_fixes_wrong_two_level_subtask(self, tenant):
        project, phase, parent = self._setup(tenant)
        sub = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.2",  # mauvais : 2 niveaux
        )
        call_command("fix_subtask_wbs")
        sub.refresh_from_db()
        assert sub.wbs_code == "1.1.1"

    def test_leaves_correct_subtask_untouched(self, tenant):
        project, phase, parent = self._setup(tenant)
        sub = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.1.1",
        )
        call_command("fix_subtask_wbs")
        sub.refresh_from_db()
        assert sub.wbs_code == "1.1.1"

    def test_two_wrong_subtasks_numbered_sequentially(self, tenant):
        project, phase, parent = self._setup(tenant)
        s1 = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.2", order=0,
        )
        s2 = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.3", order=1,
        )
        call_command("fix_subtask_wbs")
        s1.refresh_from_db()
        s2.refresh_from_db()
        assert (s1.wbs_code, s2.wbs_code) == ("1.1.1", "1.1.2")

    def test_avoids_collision_with_existing_correct_sibling(self, tenant):
        project, phase, parent = self._setup(tenant)
        good = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.1.1", order=0,
        )
        wrong = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.2", order=1,
        )
        call_command("fix_subtask_wbs")
        good.refresh_from_db()
        wrong.refresh_from_db()
        assert good.wbs_code == "1.1.1"
        assert wrong.wbs_code == "1.1.2"

    def test_dry_run_makes_no_change(self, tenant):
        project, phase, parent = self._setup(tenant)
        sub = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.2",
        )
        call_command("fix_subtask_wbs", "--dry-run")
        sub.refresh_from_db()
        assert sub.wbs_code == "1.2"

    def test_idempotent(self, tenant):
        project, phase, parent = self._setup(tenant)
        sub = TaskFactory(
            project=project, phase=phase, tenant=tenant, parent=parent,
            task_type="SUBTASK", wbs_code="1.2",
        )
        call_command("fix_subtask_wbs")
        call_command("fix_subtask_wbs")
        sub.refresh_from_db()
        assert sub.wbs_code == "1.1.1"

    def test_project_id_scope(self, tenant):
        p1, ph1, par1 = self._setup(tenant)
        sub1 = TaskFactory(
            project=p1, phase=ph1, tenant=tenant, parent=par1,
            task_type="SUBTASK", wbs_code="1.2",
        )
        p2, ph2, par2 = self._setup(tenant)
        sub2 = TaskFactory(
            project=p2, phase=ph2, tenant=tenant, parent=par2,
            task_type="SUBTASK", wbs_code="1.2",
        )
        call_command("fix_subtask_wbs", "--project-id", str(p1.pk))
        sub1.refresh_from_db()
        sub2.refresh_from_db()
        assert sub1.wbs_code == "1.1.1"  # corrigé
        assert sub2.wbs_code == "1.2"  # hors scope, inchangé
