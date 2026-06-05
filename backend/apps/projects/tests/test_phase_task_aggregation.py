"""Agrégation Phase ⇇ Tâche ⇇ Sous-tâche.

Règle métier : seules les tâches **saisissables** (sans sous-tâche) portent
budget / heures / planification / saisie. La phase et la tâche-mère ne font
que **sommer** leurs descendants saisissables, en lecture seule.

- ``is_chargeable``           : True si la tâche n'a pas de sous-tâche
- ``effective_budgeted_hours`` : budget propre (saisissable) ou Σ sous-tâches (mère)
- ``planned_hours`` / ``actual_hours`` : remontés des saisissables, jamais doublés
- Phase : ``tasks_budgeted_hours`` = Σ des tâches saisissables (pas les mères)
"""

from __future__ import annotations

from datetime import date

import pytest

from apps.planning.models import ResourceAllocation
from apps.projects.serializers import PhaseSerializer, TaskSerializer
from apps.time_entries.models import TimeEntry

from .conftest import PhaseFactory, TaskFactory, UserFactory


def _entry(*, tenant, project, employee, task, hours, day=date(2026, 6, 1)):
    return TimeEntry.objects.create(
        tenant=tenant, project=project, employee=employee,
        task=task, phase=None, hours=hours, date=day,
    )


def _alloc(*, tenant, project, employee, task, hours_per_week=20):
    """Allocation d'1 semaine → total_planned_hours == hours_per_week."""
    return ResourceAllocation.objects.create(
        tenant=tenant, project=project, employee=employee, task=task,
        start_date=date(2026, 6, 1), end_date=date(2026, 6, 5),
        hours_per_week=hours_per_week, status="ACTIVE", created_by=employee,
    )


@pytest.mark.django_db
class TestTaskChargeable:
    def test_leaf_task_is_chargeable(self, project, phase):
        leaf = TaskFactory(project=project, phase=phase, budgeted_hours=8)
        data = TaskSerializer(leaf).data
        assert data["is_chargeable"] is True

    def test_parent_task_is_not_chargeable(self, project, phase):
        parent = TaskFactory(project=project, phase=phase, budgeted_hours=99)
        TaskFactory(project=project, phase=phase, parent=parent, task_type="SUBTASK")
        data = TaskSerializer(parent).data
        assert data["is_chargeable"] is False


@pytest.mark.django_db
class TestParentTaskRollup:
    def test_parent_budget_is_sum_of_subtasks_not_own(self, project, phase):
        # La mère a un budget propre (99) qui DOIT être ignoré au profit du Σ.
        parent = TaskFactory(project=project, phase=phase, budgeted_hours=99)
        TaskFactory(project=project, phase=phase, parent=parent,
                    task_type="SUBTASK", budgeted_hours=5)
        TaskFactory(project=project, phase=phase, parent=parent,
                    task_type="SUBTASK", budgeted_hours=3)
        data = TaskSerializer(parent).data
        assert float(data["effective_budgeted_hours"]) == 8

    def test_leaf_effective_budget_is_own(self, project, phase):
        leaf = TaskFactory(project=project, phase=phase, budgeted_hours=7)
        data = TaskSerializer(leaf).data
        assert float(data["effective_budgeted_hours"]) == 7

    def test_parent_actual_hours_rolls_up_subtasks(self, project, phase, tenant):
        emp = UserFactory()
        parent = TaskFactory(project=project, phase=phase, budgeted_hours=99)
        s1 = TaskFactory(project=project, phase=phase, parent=parent, task_type="SUBTASK")
        s2 = TaskFactory(project=project, phase=phase, parent=parent, task_type="SUBTASK")
        _entry(tenant=tenant, project=project, employee=emp, task=s1, hours=3)
        _entry(tenant=tenant, project=project, employee=emp, task=s2, hours=4)
        data = TaskSerializer(parent).data
        assert float(data["actual_hours"]) == 7

    def test_parent_planned_hours_rolls_up_subtasks(self, project, phase, tenant):
        emp = UserFactory()
        parent = TaskFactory(project=project, phase=phase)
        s1 = TaskFactory(project=project, phase=phase, parent=parent, task_type="SUBTASK")
        _alloc(tenant=tenant, project=project, employee=emp, task=s1, hours_per_week=15)
        data = TaskSerializer(parent).data
        assert float(data["planned_hours"]) == 15


@pytest.mark.django_db
class TestPhaseAggregation:
    def test_budget_excludes_parent_tasks_no_double_count(self, project, phase):
        # Mère (budget propre 10) + 2 sous-tâches (5 + 5) + 1 tâche saisissable (7)
        parent = TaskFactory(project=project, phase=phase, budgeted_hours=10)
        TaskFactory(project=project, phase=phase, parent=parent,
                    task_type="SUBTASK", budgeted_hours=5)
        TaskFactory(project=project, phase=phase, parent=parent,
                    task_type="SUBTASK", budgeted_hours=5)
        TaskFactory(project=project, phase=phase, budgeted_hours=7)
        data = PhaseSerializer(phase).data
        # Σ des saisissables = 5 + 5 + 7 = 17 (le 10 de la mère est exclu)
        assert float(data["tasks_budgeted_hours"]) == 17

    def test_actual_hours_sums_task_entries_not_phase_level(self, project, phase, tenant):
        emp = UserFactory()
        t1 = TaskFactory(project=project, phase=phase)
        t2 = TaskFactory(project=project, phase=phase)
        _entry(tenant=tenant, project=project, employee=emp, task=t1, hours=6)
        _entry(tenant=tenant, project=project, employee=emp, task=t2, hours=4)
        data = PhaseSerializer(phase).data
        assert float(data["actual_hours"]) == 10

    def test_planned_hours_sums_task_allocations(self, project, phase, tenant):
        emp = UserFactory()
        t1 = TaskFactory(project=project, phase=phase)
        _alloc(tenant=tenant, project=project, employee=emp, task=t1, hours_per_week=12)
        data = PhaseSerializer(phase).data
        assert float(data["planned_hours"]) == 12

    def test_has_tasks_flag_and_count(self, project, phase):
        empty = PhaseFactory(project=project)
        TaskFactory(project=project, phase=phase)
        assert PhaseSerializer(phase).data["has_tasks"] is True
        assert PhaseSerializer(phase).data["task_count"] == 1
        assert PhaseSerializer(empty).data["has_tasks"] is False
        assert PhaseSerializer(empty).data["task_count"] == 0
