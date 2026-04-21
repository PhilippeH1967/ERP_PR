"""Tests for apps.projects.services — project creation from templates."""

from __future__ import annotations

from decimal import Decimal

import pytest

from apps.clients.models import Client
from apps.projects.models import (
    Phase,
    Project,
    ProjectTemplate,
    SupportService,
    Task,
)
from apps.projects.services import create_project_from_template

from .conftest import ProjectTemplateFactory, UserFactory


@pytest.mark.django_db
class TestCreateProjectFromTemplate:
    def test_creates_project_phases_tasks_support_services(self, tenant):
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant,
            name="Full",
            contract_type="FORFAITAIRE",
            phases_config=[
                {
                    "name": "Concept",
                    "code": "1",
                    "type": "REALIZATION",
                    "billing_mode": "FORFAIT",
                    "tasks": [
                        {
                            "wbs_code": "1.1",
                            "name": "Analyse",
                            "budgeted_hours": 10,
                            "budgeted_cost": 1000,
                            "is_billable": True,
                        },
                        {"wbs_code": "1.2", "name": "Relevé", "budgeted_hours": 5},
                    ],
                },
                {
                    "name": "Gestion",
                    "code": "G",
                    "type": "SUPPORT",
                    "is_mandatory": True,
                    "tasks": [],
                },
            ],
            support_services_config=[
                {"name": "BIM", "client_label": "Service BIM"},
                {"name": "DD"},
            ],
        )
        project = create_project_from_template(
            tmpl.pk,
            {"code": "PRJ-NEW", "name": "New project"},
            tenant_id=tenant.pk,
        )
        assert project.pk is not None
        assert project.code == "PRJ-NEW"
        assert project.template_id == tmpl.pk
        assert project.tenant_id == tenant.pk
        assert project.contract_type == "FORFAITAIRE"

        phases = list(project.phases.order_by("order"))
        assert len(phases) == 2
        assert phases[0].name == "Concept"
        assert phases[0].is_mandatory is False
        assert phases[1].name == "Gestion"
        assert phases[1].is_mandatory is True

        tasks_concept = list(phases[0].tasks.order_by("order"))
        assert len(tasks_concept) == 2
        assert tasks_concept[0].wbs_code == "1.1"
        assert tasks_concept[0].budgeted_hours == Decimal("10")
        assert tasks_concept[1].wbs_code == "1.2"
        assert tasks_concept[1].budgeted_hours == Decimal("5")

        assert phases[1].tasks.count() == 0

        services = list(project.support_services.order_by("name"))
        assert {s.name for s in services} == {"BIM", "DD"}

    def test_raises_when_template_missing(self, tenant):
        with pytest.raises(ProjectTemplate.DoesNotExist):
            create_project_from_template(9_999_999, {"code": "X", "name": "X"}, tenant_id=tenant.pk)

    def test_falls_back_to_template_tenant_when_no_tenant_id(self, tenant):
        tmpl = ProjectTemplateFactory(tenant=tenant)
        project = create_project_from_template(
            tmpl.pk, {"code": "PRJ-TENANT", "name": "T"}, tenant_id=None
        )
        assert project.tenant_id == tenant.pk

    def test_phase_budget_overrides(self, tenant):
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant,
            name="Budget override",
            contract_type="FORFAITAIRE",
            phases_config=[
                {
                    "name": "Concept",
                    "type": "REALIZATION",
                    "budgeted_hours": 10,
                    "budgeted_cost": 500,
                    "tasks": [],
                }
            ],
        )
        project = create_project_from_template(
            tmpl.pk,
            {
                "code": "PRJ-OV",
                "name": "Override",
                "phase_budgets": {
                    "0": {"budgeted_hours": 42, "budgeted_cost": 9999},
                },
            },
            tenant_id=tenant.pk,
        )
        phase = project.phases.get()
        assert phase.budgeted_hours == Decimal("42")
        assert phase.budgeted_cost == Decimal("9999")

    def test_phase_budget_override_keyed_by_int_index(self, tenant):
        """Phase budgets dict may be keyed by int instead of str."""
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant,
            name="Int keys",
            contract_type="FORFAITAIRE",
            phases_config=[{"name": "Phase", "type": "REALIZATION", "tasks": []}],
        )
        project = create_project_from_template(
            tmpl.pk,
            {
                "code": "PRJ-INT",
                "name": "IntKey",
                "phase_budgets": {0: {"budgeted_hours": 7}},
            },
            tenant_id=tenant.pk,
        )
        assert project.phases.get().budgeted_hours == Decimal("7")

    def test_empty_phases_config_creates_empty_project(self, tenant):
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant,
            name="Empty",
            contract_type="FORFAITAIRE",
            phases_config=[],
            support_services_config=[],
        )
        project = create_project_from_template(
            tmpl.pk, {"code": "PRJ-EMPTY", "name": "Empty"}, tenant_id=tenant.pk
        )
        assert project.phases.count() == 0
        assert project.support_services.count() == 0

    def test_fk_shortcut_fields_are_normalized(self, tenant):
        """`"client": 5` should be accepted as `client_id=5`."""
        client = Client.objects.create(tenant=tenant, name="Client A", alias="CA")
        pm = UserFactory()
        tmpl = ProjectTemplateFactory(tenant=tenant, phases_config=[])
        project = create_project_from_template(
            tmpl.pk,
            {
                "code": "PRJ-FK",
                "name": "FK shortcut",
                "client": client.pk,
                "pm": pm.pk,
            },
            tenant_id=tenant.pk,
        )
        assert project.client_id == client.pk
        assert project.pm_id == pm.pk

    def test_fk_shortcut_accepts_string_ids(self, tenant):
        client = Client.objects.create(tenant=tenant, name="B", alias="B")
        tmpl = ProjectTemplateFactory(tenant=tenant, phases_config=[])
        project = create_project_from_template(
            tmpl.pk,
            {"code": "PRJ-FKS", "name": "str id", "client": str(client.pk)},
            tenant_id=tenant.pk,
        )
        assert project.client_id == client.pk

    def test_unknown_fields_are_ignored(self, tenant):
        tmpl = ProjectTemplateFactory(tenant=tenant, phases_config=[])
        project = create_project_from_template(
            tmpl.pk,
            {
                "code": "PRJ-UNK",
                "name": "Unknown field test",
                "nonexistent_field": "should be silently dropped",
            },
            tenant_id=tenant.pk,
        )
        assert project.pk is not None
        assert project.code == "PRJ-UNK"

    def test_none_values_in_fk_are_skipped(self, tenant):
        tmpl = ProjectTemplateFactory(tenant=tenant, phases_config=[])
        project = create_project_from_template(
            tmpl.pk,
            {"code": "PRJ-NONE", "name": "None FK", "client": None, "pm_id": None},
            tenant_id=tenant.pk,
        )
        assert project.client_id is None
        assert project.pm_id is None

    def test_tasks_inherit_phase_billing_mode_when_not_specified(self, tenant):
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant,
            name="Inherit",
            contract_type="FORFAITAIRE",
            phases_config=[
                {
                    "name": "Horaire phase",
                    "type": "REALIZATION",
                    "billing_mode": "HORAIRE",
                    "tasks": [{"wbs_code": "1.1", "name": "Task w/o billing"}],
                }
            ],
        )
        project = create_project_from_template(
            tmpl.pk, {"code": "PRJ-INH", "name": "Inherit"}, tenant_id=tenant.pk
        )
        task = project.tasks.get()
        assert task.billing_mode == "HORAIRE"

    def test_creates_count_matches_template_totals(self, tenant):
        """Integration sanity: created counts equal config counts."""
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant,
            name="Counts",
            contract_type="FORFAITAIRE",
            phases_config=[
                {"name": "A", "tasks": [{"name": "a1"}, {"name": "a2"}]},
                {"name": "B", "tasks": [{"name": "b1"}]},
                {"name": "C", "tasks": []},
            ],
            support_services_config=[{"name": "S1"}, {"name": "S2"}, {"name": "S3"}],
        )
        before_projects = Project.objects.count()
        project = create_project_from_template(
            tmpl.pk, {"code": "CNT", "name": "Counts"}, tenant_id=tenant.pk
        )
        assert Project.objects.count() == before_projects + 1
        assert Phase.objects.filter(project=project).count() == 3
        assert Task.objects.filter(project=project).count() == 3
        assert SupportService.objects.filter(project=project).count() == 3
