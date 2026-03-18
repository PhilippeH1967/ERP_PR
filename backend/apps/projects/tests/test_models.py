"""Tests for Project, Phase, WBS, Template, and Amendment models."""

import pytest

from apps.core.models import Tenant
from apps.projects.models import (
    Amendment,
    Phase,
    Project,
    ProjectTemplate,
    WBSElement,
)


@pytest.mark.django_db
class TestProjectModel:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-proj")

    def test_create_project(self):
        p = Project.objects.create(
            tenant=self.tenant, code="PRJ-2026-001", name="Complexe Desjardins"
        )
        assert p.pk is not None
        assert p.status == "ACTIVE"
        assert p.version == 1

    def test_project_code_unique_per_tenant(self):
        Project.objects.create(tenant=self.tenant, code="PRJ-001", name="A")
        from django.db import IntegrityError
        with pytest.raises(IntegrityError):
            Project.objects.create(tenant=self.tenant, code="PRJ-001", name="B")

    def test_project_history_tracked(self):
        p = Project.objects.create(tenant=self.tenant, code="PRJ-H", name="Hist")
        p.name = "History Updated"
        p.save()
        assert p.history.count() == 2

    def test_project_str(self):
        p = Project(code="PRJ-001", name="Test")
        assert str(p) == "PRJ-001 — Test"


@pytest.mark.django_db
class TestPhaseModel:
    def test_create_phase(self):
        tenant = Tenant.objects.create(name="T", slug="t-phase")
        project = Project.objects.create(tenant=tenant, code="P1", name="P")
        phase = Phase.objects.create(
            tenant=tenant, project=project, name="Concept",
            client_facing_label="Phase Concept", order=1
        )
        assert phase.pk is not None
        assert phase.billing_mode == "FORFAIT"


@pytest.mark.django_db
class TestWBSElement:
    def test_create_hierarchy(self):
        tenant = Tenant.objects.create(name="T", slug="t-wbs")
        project = Project.objects.create(tenant=tenant, code="P2", name="P")
        phase = Phase.objects.create(tenant=tenant, project=project, name="Ph1")
        task = WBSElement.objects.create(
            tenant=tenant, project=project, phase=phase,
            standard_label="Task 1", client_facing_label="Tâche 1",
            element_type="TASK"
        )
        subtask = WBSElement.objects.create(
            tenant=tenant, project=project, parent=task,
            standard_label="Subtask 1.1", element_type="SUBTASK"
        )
        assert subtask.parent_id == task.pk
        assert task.children.count() == 1


@pytest.mark.django_db
class TestProjectTemplate:
    def test_create_template(self):
        tenant = Tenant.objects.create(name="T", slug="t-tmpl")
        tmpl = ProjectTemplate.objects.create(
            tenant=tenant, name="Forfaitaire Standard",
            contract_type="FORFAITAIRE",
            phases_config=[
                {"name": "Concept", "type": "REALIZATION", "is_mandatory": False},
                {"name": "Gestion de projet", "type": "SUPPORT", "is_mandatory": True},
            ],
        )
        assert len(tmpl.phases_config) == 2


@pytest.mark.django_db
class TestAmendment:
    def test_create_amendment(self):
        tenant = Tenant.objects.create(name="T", slug="t-amend")
        project = Project.objects.create(tenant=tenant, code="PA", name="P")
        a = Amendment.objects.create(
            tenant=tenant, project=project, amendment_number=1,
            description="Budget increase", budget_impact="50000.00"
        )
        assert a.pk is not None
        assert a.version == 1
