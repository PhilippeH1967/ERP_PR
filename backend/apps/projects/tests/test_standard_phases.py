"""Jeu global de phases standard (paramétrage admin)."""

from __future__ import annotations

import pytest
from django.core.management import call_command
from django.db import IntegrityError

from apps.projects.models import StandardPhase

URL = "/api/v1/standard_phases/"


@pytest.mark.django_db
class TestStandardPhaseModel:
    def test_unique_code_per_tenant(self, tenant):
        StandardPhase.objects.create(tenant=tenant, code="1", name="Concept")
        with pytest.raises(IntegrityError):
            StandardPhase.objects.create(tenant=tenant, code="1", name="Doublon")


@pytest.mark.django_db
class TestStandardPhasePermissions:
    def test_anonymous_cannot_list(self, anonymous_client):
        assert anonymous_client.get(URL).status_code in (401, 403)

    def test_authenticated_can_list(self, employee_client, tenant):
        StandardPhase.objects.create(tenant=tenant, code="1", name="Concept")
        resp = employee_client.get(URL)
        assert resp.status_code == 200

    def test_admin_can_create(self, admin_client):
        resp = admin_client.post(
            URL, {"code": "1", "name": "Concept", "phase_type": "REALIZATION"}, format="json"
        )
        assert resp.status_code == 201
        assert StandardPhase.objects.filter(code="1").exists()

    def test_pm_cannot_create(self, pm_client):
        resp = pm_client.post(
            URL, {"code": "9", "name": "Interdite", "phase_type": "REALIZATION"}, format="json"
        )
        assert resp.status_code == 403
        assert not StandardPhase.objects.filter(code="9").exists()

    def test_employee_cannot_delete(self, employee_client, admin_client, tenant):
        sp = StandardPhase.objects.create(tenant=tenant, code="2", name="Préliminaire")
        assert employee_client.delete(f"{URL}{sp.id}/").status_code == 403
        assert admin_client.delete(f"{URL}{sp.id}/").status_code == 204


@pytest.mark.django_db
class TestSeedStandardPhases:
    def test_seed_creates_standard_set(self, tenant):
        call_command("seed_standard_phases", tenant_id=tenant.id)
        codes = set(StandardPhase.objects.filter(tenant=tenant).values_list("code", flat=True))
        assert {"1", "G", "Q"}.issubset(codes)
        assert StandardPhase.objects.filter(tenant=tenant, code="G", is_mandatory=True).exists()

    def test_seed_is_idempotent(self, tenant):
        call_command("seed_standard_phases", tenant_id=tenant.id)
        n1 = StandardPhase.objects.filter(tenant=tenant).count()
        call_command("seed_standard_phases", tenant_id=tenant.id)
        n2 = StandardPhase.objects.filter(tenant=tenant).count()
        assert n1 == n2 and n1 > 0


@pytest.mark.django_db
class TestProjectCreationInstantiatesStandardPhases:
    """Tout projet hérite du jeu standard à la création — y compris sans
    template (le wizard ne crée plus de phase manuellement)."""

    def test_plain_create_instantiates_standard_phases(self, admin_client, tenant):
        from apps.projects.models import Project

        StandardPhase.objects.create(tenant=tenant, code="1", name="Concept", order=0)
        StandardPhase.objects.create(
            tenant=tenant, code="G", name="Gestion de projet", order=1, is_mandatory=True
        )
        resp = admin_client.post(
            "/api/v1/projects/",
            {"code": "PRJ-NEW", "name": "Nouveau", "is_internal": True},
            format="json",
        )
        assert resp.status_code == 201
        pid = resp.json().get("data", resp.json())["id"]
        project = Project.objects.get(pk=pid)
        codes = set(project.phases.values_list("code", flat=True))
        assert {"1", "G"}.issubset(codes)
        # La phase obligatoire conserve son flag.
        assert project.phases.filter(code="G", is_mandatory=True).exists()

    def test_plain_create_instantiates_support_phases_from_transversaux(
        self, admin_client, tenant
    ):
        """Chaque service transversal sélectionné au wizard devient une **phase
        SUPPORT** (regroupement) contenant **une tâche feuille imputable** du
        même nom — pas un ``SupportService`` non imputable."""
        from apps.projects.models import Phase, Project, Task

        resp = admin_client.post(
            "/api/v1/projects/",
            {
                "code": "PRJ-SVC", "name": "Avec services", "is_internal": True,
                "services_transversaux": ["BIM", "DD"],
            },
            format="json",
        )
        assert resp.status_code == 201
        pid = resp.json().get("data", resp.json())["id"]
        project = Project.objects.get(pk=pid)

        support_phases = project.phases.filter(phase_type=Phase.PhaseType.SUPPORT)
        codes = set(support_phases.values_list("code", flat=True))
        assert {"BIM", "DD"}.issubset(codes)
        bim = support_phases.get(code="BIM")
        # Nom lisible (label), pas seulement le code.
        assert "BIM" in bim.name
        # La phase porte une tâche feuille imputable (sans enfant).
        bim_task = Task.objects.get(project=project, phase=bim)
        assert bim_task.parent is None
        assert "BIM" in bim_task.name
        # Idempotent : pas de doublon de phase de service.
        assert support_phases.filter(code="BIM").count() == 1
        # Aucun SupportService (modèle déprécié) n'est créé.
        assert project.support_services.count() == 0
