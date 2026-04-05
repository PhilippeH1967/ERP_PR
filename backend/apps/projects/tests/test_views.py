"""Tests for Project API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant
from apps.projects.models import Phase, Project, ProjectTemplate


@pytest.mark.django_db
class TestProjectAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API", slug="proj-api")
        self.user = User.objects.create_user(username="proj_user", password="pass123!")
        # Give user ADMIN role so they can see all projects
        from apps.core.models import ProjectRole, Role
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_projects(self):
        response = self.api.get("/api/v1/projects/")
        assert response.status_code == 200

    def test_create_project(self):
        response = self.api.post(
            "/api/v1/projects/",
            {"code": "PRJ-001", "name": "Test Project", "contract_type": "FORFAITAIRE"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_retrieve_project(self):
        p = Project.objects.create(
            tenant=self.tenant, code="PRJ-R", name="Retrieve"
        )
        response = self.api.get(
            f"/api/v1/projects/{p.pk}/",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 200

    def test_search_projects(self):
        Project.objects.create(tenant=self.tenant, code="PRJ-S", name="Searchable")
        response = self.api.get("/api/v1/projects/?search=Searchable")
        assert response.status_code == 200

    def test_filter_by_status(self):
        Project.objects.create(tenant=self.tenant, code="P-A", name="Active", status="ACTIVE")
        Project.objects.create(tenant=self.tenant, code="P-H", name="Hold", status="ON_HOLD")
        response = self.api.get("/api/v1/projects/?status=ACTIVE")
        assert response.status_code == 200

    def test_project_dashboard(self):
        p = Project.objects.create(tenant=self.tenant, code="PD", name="Dash")
        response = self.api.get(
            f"/api/v1/projects/{p.pk}/dashboard/",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["health"] == "green"


@pytest.mark.django_db
class TestCreateFromTemplate:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Tmpl API", slug="tmpl-api")
        self.user = User.objects.create_user(username="tmpl_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)
        self.template = ProjectTemplate.objects.create(
            tenant=self.tenant,
            name="Standard",
            contract_type="FORFAITAIRE",
            phases_config=[
                {"name": "Concept", "type": "REALIZATION"},
                {"name": "Gestion de projet", "type": "SUPPORT", "is_mandatory": True},
            ],
            support_services_config=[{"name": "BIM"}],
        )

    def test_create_from_template(self):
        response = self.api.post(
            "/api/v1/projects/create_from_template/",
            {
                "template_id": self.template.pk,
                "project": {"code": "PRJ-T1", "name": "From Template"},
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201
        # Verify phases were created
        project = Project.objects.get(code="PRJ-T1")
        assert project.phases.count() == 2
        assert project.support_services.count() == 1


@pytest.mark.django_db
class TestPhaseAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Phase API", slug="phase-api")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PP", name="Phase Project"
        )
        self.user = User.objects.create_user(username="phase_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_phases(self):
        Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Ph1", order=1
        )
        response = self.api.get(f"/api/v1/projects/{self.project.pk}/phases/")
        assert response.status_code == 200

    def test_create_phase(self):
        response = self.api.post(
            f"/api/v1/projects/{self.project.pk}/phases/",
            {"name": "New Phase", "order": 1, "billing_mode": "HORAIRE"},
            format="json",
        )
        assert response.status_code == 201
