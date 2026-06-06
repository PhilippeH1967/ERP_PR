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

    def test_dates_aggregate_min_max_from_tasks(self, project, phase):
        from datetime import date as d
        TaskFactory(project=project, phase=phase, start_date=d(2026, 3, 1), end_date=d(2026, 4, 30))
        TaskFactory(project=project, phase=phase, start_date=d(2026, 2, 1), end_date=d(2026, 3, 15))
        TaskFactory(project=project, phase=phase)  # sans dates : ignorée
        data = PhaseSerializer(phase).data
        assert data["tasks_start_date"] == "2026-02-01"  # min
        assert data["tasks_end_date"] == "2026-04-30"    # max

    def test_dates_null_when_no_task_dates(self, project, phase):
        TaskFactory(project=project, phase=phase)  # sans dates
        data = PhaseSerializer(phase).data
        assert data["tasks_start_date"] is None
        assert data["tasks_end_date"] is None

    def test_phase_list_no_n_plus_1(self, admin_client, project, django_assert_max_num_queries):
        """L'endpoint liste des phases ne doit pas faire de N+1 sur les agrégats :
        le nombre de requêtes reste borné quel que soit le nombre de phases."""
        from datetime import date as d
        for i in range(6):
            ph = PhaseFactory(project=project, tenant=project.tenant, order=i)
            t = TaskFactory(project=project, phase=ph, budgeted_hours=10,
                            start_date=d(2026, 3, 1), end_date=d(2026, 4, 1))
            _alloc(tenant=project.tenant, project=project, employee=UserFactory(), task=t)
        with django_assert_max_num_queries(15):
            resp = admin_client.get(f"/api/v1/projects/{project.pk}/phases/")
        assert resp.status_code == 200

    def test_has_tasks_flag_and_count(self, project, phase):
        empty = PhaseFactory(project=project)
        TaskFactory(project=project, phase=phase)
        assert PhaseSerializer(phase).data["has_tasks"] is True
        assert PhaseSerializer(phase).data["task_count"] == 1
        assert PhaseSerializer(empty).data["has_tasks"] is False
        assert PhaseSerializer(empty).data["task_count"] == 0


def _invoice_line(*, tenant, project, task, status, invoiced, contract, number):
    """Crée une facture + 1 ligne rattachée à une tâche."""
    from apps.billing.models import Invoice, InvoiceLine
    from apps.clients.models import Client

    client = Client.objects.filter(tenant=tenant).first() or Client.objects.create(
        tenant=tenant, name="ACME"
    )
    inv = Invoice.objects.create(
        tenant=tenant, project=project, client=client,
        invoice_number=number, status=status, total_amount=invoiced,
    )
    return InvoiceLine.objects.create(
        tenant=tenant, invoice=inv, task=task, deliverable_name=task.name,
        total_contract_amount=contract, invoiced_to_date=invoiced,
    )


@pytest.mark.django_db
class TestPhaseFinancialAggregation:
    """Agrégats financiers de phase : coût réel (heures × taux tâche), facturé
    et honoraires contractés (via InvoiceLine, dernière ligne par tâche)."""

    def test_actual_cost_uses_task_hourly_rate(self, project, phase, tenant):
        emp = UserFactory()
        t1 = TaskFactory(project=project, phase=phase, budgeted_cost=1000, hourly_rate=100)
        t2 = TaskFactory(project=project, phase=phase, budgeted_cost=500, hourly_rate=50)
        _entry(tenant=tenant, project=project, employee=emp, task=t1, hours=4)  # 4×100
        _entry(tenant=tenant, project=project, employee=emp, task=t2, hours=2)  # 2×50
        data = PhaseSerializer(phase).data
        assert float(data["actual_cost"]) == 500.0  # 400 + 100

    def test_actual_cost_zero_when_task_has_no_rate(self, project, phase, tenant):
        emp = UserFactory()
        t1 = TaskFactory(project=project, phase=phase, hourly_rate=None)
        _entry(tenant=tenant, project=project, employee=emp, task=t1, hours=4)
        data = PhaseSerializer(phase).data
        assert float(data["actual_cost"]) == 0.0

    def test_invoiced_and_fees_from_finalized_line(self, project, phase, tenant):
        t1 = TaskFactory(project=project, phase=phase)
        _invoice_line(tenant=tenant, project=project, task=t1, status="SENT",
                      invoiced=300, contract=1000, number="INV-1")
        data = PhaseSerializer(phase).data
        assert float(data["invoiced_amount"]) == 300.0
        assert float(data["fees_contract_amount"]) == 1000.0

    def test_invoiced_excludes_draft_invoices(self, project, phase, tenant):
        t1 = TaskFactory(project=project, phase=phase)
        _invoice_line(tenant=tenant, project=project, task=t1, status="DRAFT",
                      invoiced=999, contract=1000, number="INV-DRAFT")
        data = PhaseSerializer(phase).data
        assert float(data["invoiced_amount"]) == 0.0

    def test_invoiced_takes_latest_line_per_task_no_double_count(self, project, phase, tenant):
        # Deux périodes pour la MÊME tâche : invoiced_to_date est cumulatif →
        # on prend la dernière ligne (500), pas la somme (200 + 500).
        t1 = TaskFactory(project=project, phase=phase)
        _invoice_line(tenant=tenant, project=project, task=t1, status="SENT",
                      invoiced=200, contract=1000, number="INV-P1")
        _invoice_line(tenant=tenant, project=project, task=t1, status="SENT",
                      invoiced=500, contract=1000, number="INV-P2")
        data = PhaseSerializer(phase).data
        assert float(data["invoiced_amount"]) == 500.0
        assert float(data["fees_contract_amount"]) == 1000.0


@pytest.mark.django_db
class TestDashboardBudgetHoursBugfix:
    """Bug v1.2 : le dashboard sommait Phase.budgeted_hours (legacy = 0) au lieu
    des budgets de tâches. Le budget doit venir des tâches."""

    def test_budget_hours_comes_from_tasks_not_phase_legacy_field(
        self, admin_client, project, phase
    ):
        # Phase sans budget legacy ; budget réel porté par les tâches.
        phase.budgeted_hours = 0
        phase.save()
        TaskFactory(project=project, phase=phase, budgeted_hours=40)
        TaskFactory(project=project, phase=phase, budgeted_hours=10)
        resp = admin_client.get(f"/api/v1/projects/{project.pk}/dashboard/")
        assert resp.status_code == 200
        body = resp.json().get("data", resp.json())
        assert float(body["budget_hours"]) == 50.0
