"""Création de projet : les phases héritent du jeu global StandardPhase."""

from __future__ import annotations

import pytest

from apps.projects.models import Phase, StandardPhase
from apps.projects.services import create_project_from_template

from .conftest import ProjectTemplateFactory


@pytest.mark.django_db
class TestProjectInheritsStandardPhases:
    def _template(self, tenant):
        # Template dont les phases diffèrent du jeu standard, pour vérifier
        # que c'est bien le jeu standard qui prime.
        return ProjectTemplateFactory(
            tenant=tenant,
            phases_config=[{"name": "TemplatePhase", "code": "T", "type": "REALIZATION"}],
        )

    def test_uses_standard_set_when_present(self, tenant):
        StandardPhase.objects.create(tenant=tenant, code="1", name="Concept", order=0)
        StandardPhase.objects.create(
            tenant=tenant, code="G", name="Gestion de projet",
            phase_type="SUPPORT", order=1, is_mandatory=True,
        )
        # Phase désactivée : ne doit pas être instanciée
        StandardPhase.objects.create(
            tenant=tenant, code="X", name="Inactive", order=2, is_active=False
        )
        tmpl = self._template(tenant)

        project = create_project_from_template(
            tmpl.id, {"code": "PR-STD", "name": "Std"}, tenant_id=tenant.id
        )

        phases = Phase.objects.filter(project=project).order_by("order")
        names = list(phases.values_list("name", flat=True))
        assert names == ["Concept", "Gestion de projet"]  # pas "TemplatePhase", pas "Inactive"
        assert phases.get(code="G").is_mandatory is True
        # Les phases standard sont des regroupements vides (aucune tâche)
        assert project.tasks.count() == 0

    def test_falls_back_to_template_when_no_standard(self, tenant):
        tmpl = self._template(tenant)
        project = create_project_from_template(
            tmpl.id, {"code": "PR-LEG", "name": "Legacy"}, tenant_id=tenant.id
        )
        names = list(Phase.objects.filter(project=project).values_list("name", flat=True))
        assert names == ["TemplatePhase"]
