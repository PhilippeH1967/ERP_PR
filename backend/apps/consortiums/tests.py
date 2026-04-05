"""Tests for Consortium API — FR59."""

from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant
from apps.suppliers.models import ExternalOrganization

from .models import Consortium, ConsortiumMember


@pytest.mark.django_db
class TestConsortiumAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Consortium", slug="consortium-test")
        self.user = User.objects.create_user(username="csrt_user", password="pass123!")
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)
        self.client_obj = Client.objects.create(
            tenant=self.tenant, name="Ville de Montréal", alias="VDM"
        )

    def test_create_consortium(self):
        resp = self.api.post(
            "/api/v1/consortiums/",
            {
                "name": "Consortium Place Ville-Marie",
                "client": self.client_obj.pk,
                "pr_role": "MANDATAIRE",
                "contract_reference": "CT-2026-001",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert resp.status_code == 201
        data = resp.json().get("data", resp.json())
        assert data["name"] == "Consortium Place Ville-Marie"
        assert data["pr_role"] == "MANDATAIRE"

    def test_list_consortiums(self):
        Consortium.objects.create(
            tenant=self.tenant, name="C1", client=self.client_obj
        )
        resp = self.api.get("/api/v1/consortiums/")
        assert resp.status_code == 200

    def test_add_members_with_coefficients(self):
        consortium = Consortium.objects.create(
            tenant=self.tenant, name="C-Members", client=self.client_obj
        )
        org = ExternalOrganization.objects.create(
            tenant=self.tenant, name="Lemay Architecture"
        )
        # Add PR as member
        resp1 = self.api.post(
            f"/api/v1/consortiums/{consortium.pk}/members/",
            {"is_pr": True, "coefficient": "40.00", "specialty": "Architecture"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert resp1.status_code == 201

        # Add external org as member
        resp2 = self.api.post(
            f"/api/v1/consortiums/{consortium.pk}/members/",
            {"organization": org.pk, "coefficient": "60.00", "specialty": "Structure"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert resp2.status_code == 201

        # Verify coefficients sum to 100
        consortium.refresh_from_db()
        assert consortium.total_coefficient == Decimal("100.00")

    def test_validate_coefficients(self):
        consortium = Consortium.objects.create(
            tenant=self.tenant, name="C-Val", client=self.client_obj
        )
        ConsortiumMember.objects.create(
            tenant=self.tenant, consortium=consortium, is_pr=True, coefficient=50
        )
        resp = self.api.get(f"/api/v1/consortiums/{consortium.pk}/validate_coefficients/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["is_valid"] is False
        assert float(data["total_coefficient"]) == 50.0

    def test_consortium_with_project(self):
        """Project.consortium FK works correctly."""
        from apps.projects.models import Project

        consortium = Consortium.objects.create(
            tenant=self.tenant, name="C-Proj", client=self.client_obj
        )
        project = Project.objects.create(
            tenant=self.tenant,
            code="PRJ-C1",
            name="Projet Consortium",
            is_consortium=True,
            consortium=consortium,
        )
        assert project.consortium == consortium
        assert consortium.projects.count() == 1

    def test_delete_member(self):
        consortium = Consortium.objects.create(
            tenant=self.tenant, name="C-Del", client=self.client_obj
        )
        member = ConsortiumMember.objects.create(
            tenant=self.tenant, consortium=consortium, is_pr=True, coefficient=100
        )
        resp = self.api.delete(
            f"/api/v1/consortiums/{consortium.pk}/members/{member.pk}/",
        )
        assert resp.status_code in (200, 204)
        assert ConsortiumMember.objects.filter(pk=member.pk).count() == 0
