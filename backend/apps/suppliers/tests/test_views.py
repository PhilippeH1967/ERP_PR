"""Tests for ExternalOrganization API."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant
from apps.suppliers.models import ExternalOrganization


@pytest.mark.django_db
class TestExternalOrganizationAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API Test", slug="ext-org-api")
        self.user = User.objects.create_user(username="ext_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_organizations(self):
        response = self.api.get("/api/v1/external_organizations/")
        assert response.status_code == 200

    def test_create_organization(self):
        response = self.api.post(
            "/api/v1/external_organizations/",
            {"name": "WSP", "neq": "1234567890", "type_tags": ["st"]},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_search_organizations(self):
        ExternalOrganization.objects.create(
            tenant=self.tenant, name="SNC Lavalin", neq="111"
        )
        response = self.api.get("/api/v1/external_organizations/?search=SNC")
        assert response.status_code == 200
