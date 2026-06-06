"""Tests for TimeEntry, WeeklyApproval, TimesheetLock models."""

from datetime import date

import pytest
from django.contrib.auth.models import User

from apps.core.models import Tenant
from apps.projects.models import Phase, Project, Task
from apps.time_entries.models import (
    TimeEntry,
    TimesheetLock,
    WeeklyApproval,
)


@pytest.mark.django_db
class TestTimeEntry:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-time")
        self.user = User.objects.create_user(username="emp", password="pass123!")
        self.project = Project.objects.create(
            tenant=self.tenant, code="P1", name="Project"
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept"
        )
        self.task = Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            wbs_code="1.1", name="Tâche 1",
        )
        self.task2 = Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            wbs_code="1.2", name="Tâche 2",
        )

    def test_create_entry(self):
        entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, task=self.task,
            date=date(2026, 3, 16), hours=7.5,
        )
        assert entry.pk is not None
        assert entry.status == "DRAFT"
        assert entry.version == 1

    def test_phase_derived_from_task(self):
        """La phase est renseignée automatiquement depuis la tâche (rapports)."""
        entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, task=self.task,
            date=date(2026, 3, 16), hours=7.5,
        )
        assert entry.phase_id == self.phase.id

    def test_unique_constraint_on_task(self):
        """Unicité (employé, projet, tâche, date) — pas deux fois la même tâche."""
        from django.db import IntegrityError

        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, task=self.task,
            date=date(2026, 3, 16), hours=7.5,
        )
        with pytest.raises(IntegrityError):
            TimeEntry.objects.create(
                tenant=self.tenant, employee=self.user,
                project=self.project, task=self.task,
                date=date(2026, 3, 16), hours=1,
            )

    def test_two_tasks_same_phase_same_date_ok(self):
        """Régression : deux tâches d'une MÊME phase le même jour ne doivent plus
        entrer en conflit (l'unicité est sur la tâche, pas la phase)."""
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, task=self.task,
            date=date(2026, 3, 16), hours=4,
        )
        # Même phase (Concept), tâche différente, même jour → doit passer
        e2 = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, task=self.task2,
            date=date(2026, 3, 16), hours=3,
        )
        assert e2.pk is not None
        assert e2.phase_id == self.phase.id

    def test_serializer_rejects_parent_task(self):
        """Saisie impossible sur une tâche-mère (regroupement) : choisir une feuille."""
        from apps.time_entries.serializers import TimeEntrySerializer

        # self.task devient une tâche-mère (on lui ajoute une sous-tâche)
        Task.objects.create(
            tenant=self.tenant, project=self.project, phase=self.phase,
            parent=self.task, task_type="SUBTASK", wbs_code="1.1.1", name="Sous-tâche",
        )
        ser = TimeEntrySerializer(data={
            "project": self.project.id, "task": self.task.id,
            "date": "2026-03-16", "hours": "4",
        })
        assert not ser.is_valid()
        assert "task" in ser.errors

    def test_serializer_accepts_leaf_task(self):
        from apps.time_entries.serializers import TimeEntrySerializer

        ser = TimeEntrySerializer(data={
            "project": self.project.id, "task": self.task2.id,
            "date": "2026-03-16", "hours": "4",
        })
        assert ser.is_valid(), ser.errors

    def test_history_tracked(self):
        entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.user,
            project=self.project, date=date(2026, 3, 16), hours=7,
        )
        entry.hours = 8
        entry.save()
        assert entry.history.count() == 2


@pytest.mark.django_db
class TestWeeklyApproval:
    def test_create_approval(self):
        tenant = Tenant.objects.create(name="T", slug="t-approval")
        user = User.objects.create_user(username="appr", password="pass123!")
        approval = WeeklyApproval.objects.create(
            tenant=tenant, employee=user,
            week_start=date(2026, 3, 16), week_end=date(2026, 3, 22),
        )
        assert approval.pm_status == "PENDING"
        assert approval.finance_status == "PENDING"


@pytest.mark.django_db
class TestTimesheetLock:
    def test_create_phase_lock(self):
        tenant = Tenant.objects.create(name="T", slug="t-lock")
        project = Project.objects.create(tenant=tenant, code="PL", name="Lock")
        phase = Phase.objects.create(tenant=tenant, project=project, name="Ph")
        pm = User.objects.create_user(username="pm_lock", password="pass123!")
        lock = TimesheetLock.objects.create(
            tenant=tenant, project=project, phase=phase,
            lock_type="PHASE", locked_by=pm,
        )
        assert lock.pk is not None
        assert lock.lock_type == "PHASE"
