"""Tests for Project, Phase, Amendment, Template, WBSElement (legacy)
and auxiliary models of the projects app.
"""

from __future__ import annotations

import pytest
from django.db import IntegrityError

from apps.core.models import Tenant
from apps.projects.models import (
    Amendment,
    FinancialPhase,
    Phase,
    Project,
    ProjectTemplate,
    SupportService,
    WBSElement,
)

from .conftest import (
    AmendmentFactory,
    PhaseFactory,
    ProjectFactory,
    ProjectTemplateFactory,
    TaskFactory,
)


@pytest.mark.django_db
class TestProjectModel:
    def test_create_project(self, tenant):
        p = ProjectFactory(tenant=tenant, code="PRJ-2026-001", name="Complexe")
        assert p.pk is not None
        assert p.status == "ACTIVE"
        assert p.version == 1

    def test_project_code_unique_per_tenant(self, tenant):
        ProjectFactory(tenant=tenant, code="PRJ-UNIQ")
        with pytest.raises(IntegrityError):
            ProjectFactory(tenant=tenant, code="PRJ-UNIQ")

    def test_project_code_can_repeat_across_tenants(self, tenant, other_tenant):
        ProjectFactory(tenant=tenant, code="SHARED")
        ProjectFactory(tenant=other_tenant, code="SHARED")
        assert Project.objects.filter(code="SHARED").count() == 2

    def test_project_version_increments_on_save(self, project):
        initial_version = project.version
        project.name = "Updated"
        project.save()
        assert project.version == initial_version + 1

    def test_project_history_tracked_on_create(self, tenant):
        p = ProjectFactory(tenant=tenant, code="PRJ-HIST")
        assert p.history.count() == 1

    def test_project_history_tracked_on_update(self, project):
        project.name = "New name"
        project.save()
        assert project.history.count() == 2
        assert project.history.first().name == "New name"

    def test_project_str(self):
        p = Project(code="PRJ-001", name="Test")
        assert str(p) == "PRJ-001 — Test"


@pytest.mark.django_db
class TestPhaseModel:
    def test_create_phase_defaults(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant, name="Concept")
        assert phase.pk is not None
        assert phase.billing_mode == "FORFAIT"
        assert phase.phase_type == "REALIZATION"
        assert phase.is_mandatory is False
        assert phase.is_locked is False

    def test_phase_str_format(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant, name="Réalisation")
        assert str(phase) == f"{project.code} — Réalisation"

    def test_phase_ordered_by_order_then_name(self, project):
        PhaseFactory(project=project, tenant=project.tenant, name="B", order=2)
        PhaseFactory(project=project, tenant=project.tenant, name="A", order=1)
        PhaseFactory(project=project, tenant=project.tenant, name="C", order=1)
        names = list(project.phases.values_list("name", flat=True))
        assert names == ["A", "C", "B"]

    def test_phase_cascade_delete_with_project(self, project):
        PhaseFactory(project=project, tenant=project.tenant)
        project_pk = project.pk
        project.delete()
        assert Phase.objects.filter(project_id=project_pk).count() == 0


@pytest.mark.django_db
class TestWBSElementLegacy:
    """
    Legacy ``WBSElement`` model — retained while story 12.4 cleanup is pending.
    These tests confirm parent/child hierarchy still works and will be
    removed together with the model.
    """

    def test_create_hierarchy(self, project):
        phase = PhaseFactory(project=project, tenant=project.tenant)
        task = WBSElement.objects.create(
            tenant=project.tenant,
            project=project,
            phase=phase,
            standard_label="Task 1",
            client_facing_label="Tâche 1",
            element_type="TASK",
        )
        subtask = WBSElement.objects.create(
            tenant=project.tenant,
            project=project,
            parent=task,
            standard_label="Subtask 1.1",
            element_type="SUBTASK",
        )
        assert subtask.parent_id == task.pk
        assert task.children.count() == 1

    def test_str_uses_client_label_when_present(self, project):
        elem = WBSElement.objects.create(
            tenant=project.tenant,
            project=project,
            standard_label="Std",
            client_facing_label="Client label",
        )
        assert str(elem) == "Client label"

    def test_str_falls_back_to_standard_label(self, project):
        elem = WBSElement.objects.create(
            tenant=project.tenant, project=project, standard_label="Std only"
        )
        assert str(elem) == "Std only"


@pytest.mark.django_db
class TestProjectTemplate:
    def test_create_template(self, tenant):
        tmpl = ProjectTemplateFactory(tenant=tenant, name="Forfaitaire Standard")
        assert len(tmpl.phases_config) == 2
        assert tmpl.is_active is True

    def test_template_str_includes_contract_type(self, tenant):
        tmpl = ProjectTemplateFactory(tenant=tenant, name="T1", contract_type="FORFAITAIRE")
        assert "Forfaitaire" in str(tmpl)
        assert "T1" in str(tmpl)

    def test_template_default_phases_config_empty(self, tenant):
        tmpl = ProjectTemplate.objects.create(tenant=tenant, name="Minimal", contract_type="CO_DEV")
        assert tmpl.phases_config == []
        assert tmpl.support_services_config == []

    def test_template_ordering_by_name(self, tenant):
        ProjectTemplateFactory(tenant=tenant, name="Zeta")
        ProjectTemplateFactory(tenant=tenant, name="Alpha")
        ProjectTemplateFactory(tenant=tenant, name="Mike")
        ordered = list(ProjectTemplate.objects.values_list("name", flat=True))
        assert ordered == ["Alpha", "Mike", "Zeta"]


@pytest.mark.django_db
class TestAmendment:
    def test_create_amendment_defaults(self, project):
        a = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        assert a.pk is not None
        assert a.status == "DRAFT"
        assert a.version == 1

    def test_amendment_number_unique_per_project(self, project):
        AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        with pytest.raises(IntegrityError):
            AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)

    def test_amendment_number_can_repeat_across_projects(self, tenant):
        p1 = ProjectFactory(tenant=tenant, code="AMD-1")
        p2 = ProjectFactory(tenant=tenant, code="AMD-2")
        AmendmentFactory(project=p1, tenant=tenant, amendment_number=1)
        AmendmentFactory(project=p2, tenant=tenant, amendment_number=1)
        assert Amendment.objects.filter(amendment_number=1).count() == 2

    def test_amendment_str(self, project):
        a = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=7)
        assert str(a) == f"Avenant 7 — {project.code}"

    def test_amendment_version_increments(self, project):
        a = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=1)
        a.description = "Modifié"
        a.save()
        assert a.version == 2

    def test_amendment_history_tracked(self, project):
        a = AmendmentFactory(project=project, tenant=project.tenant, amendment_number=2)
        a.status = "SUBMITTED"
        a.save()
        assert a.history.count() == 2


@pytest.mark.django_db
class TestSupportServiceAndFinancialPhase:
    def test_support_service_defaults(self, project):
        svc = SupportService.objects.create(tenant=project.tenant, project=project, name="BIM")
        assert svc.is_billable is True
        assert svc.billing_mode == "FORFAIT"
        assert str(svc) == "BIM"

    def test_financial_phase_str(self, project):
        fp = FinancialPhase.objects.create(
            tenant=project.tenant, project=project, name="F1", code="FP1"
        )
        assert str(fp) == "FP1 — F1"


@pytest.mark.django_db
class TestTenantIsolation:
    def test_tenant_scoped_relations_independent(self):
        t1 = Tenant.objects.create(name="A", slug="iso-a")
        t2 = Tenant.objects.create(name="B", slug="iso-b")
        p1 = ProjectFactory(tenant=t1, code="ISO-1")
        p2 = ProjectFactory(tenant=t2, code="ISO-1")
        # Objects on p1 must not cross over to p2's related managers
        ph1 = PhaseFactory(project=p1, tenant=t1)
        ph2 = PhaseFactory(project=p2, tenant=t2)
        TaskFactory(project=p2, phase=ph2, tenant=t2, wbs_code="T2.1")
        assert list(p1.phases.all()) == [ph1]
        assert p1.tasks.count() == 0
        assert list(p2.phases.all()) == [ph2]
        assert p2.tasks.count() == 1
