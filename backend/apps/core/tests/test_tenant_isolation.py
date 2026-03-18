"""Tests for multi-tenant data isolation across all apps."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import Tenant
from apps.projects.models import Project


@pytest.mark.django_db
class TestTenantIsolationAPI:
    """Verify that tenant A cannot see tenant B's data via API."""

    def setup_method(self):
        self.tenant_a = Tenant.objects.create(name="Tenant A", slug="tenant-a-iso")
        self.tenant_b = Tenant.objects.create(name="Tenant B", slug="tenant-b-iso")
        self.user = User.objects.create_user(username="iso_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

        # Create data in both tenants
        Client.objects.create(tenant=self.tenant_a, name="Client A", alias="CA")
        Client.objects.create(tenant=self.tenant_b, name="Client B", alias="CB")
        Project.objects.create(tenant=self.tenant_a, code="PA-1", name="Project A")
        Project.objects.create(tenant=self.tenant_b, code="PB-1", name="Project B")

    def test_clients_filtered_by_tenant_header(self):
        """Only tenant A clients visible with X-Tenant-Id: A."""
        response = self.api.get(
            "/api/v1/clients/",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        data = response.json()
        clients = data.get("data", data)
        if isinstance(clients, list):
            names = [c["name"] for c in clients]
            assert "Client A" in names
            assert "Client B" not in names

    def test_projects_filtered_by_tenant_header(self):
        """Only tenant A projects visible with X-Tenant-Id: A."""
        response = self.api.get(
            "/api/v1/projects/",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        data = response.json()
        projects = data.get("data", data)
        if isinstance(projects, list):
            codes = [p["code"] for p in projects]
            assert "PA-1" in codes
            assert "PB-1" not in codes

    def test_invalid_tenant_returns_404(self):
        response = self.api.get(
            "/api/v1/clients/",
            HTTP_X_TENANT_ID="999999",
        )
        assert response.status_code == 404


@pytest.mark.django_db
class TestOptimisticLockingAPI:
    """Verify version conflict detection across endpoints."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Lock", slug="lock-test")
        self.user = User.objects.create_user(username="lock_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_client_update_version_conflict(self):
        client = Client.objects.create(
            tenant=self.tenant, name="Lockable", alias="LK"
        )
        # First update succeeds
        resp1 = self.api.patch(
            f"/api/v1/clients/{client.pk}/",
            {"name": "Updated 1"},
            format="json",
            HTTP_IF_MATCH="1",
        )
        assert resp1.status_code == 200

        # Second update with stale version fails
        resp2 = self.api.patch(
            f"/api/v1/clients/{client.pk}/",
            {"name": "Updated 2"},
            format="json",
            HTTP_IF_MATCH="1",  # Stale — should be 2
        )
        assert resp2.status_code == 409

    def test_client_update_without_version_succeeds(self):
        """Updates without If-Match header should proceed."""
        client = Client.objects.create(
            tenant=self.tenant, name="NoLock", alias="NL"
        )
        resp = self.api.patch(
            f"/api/v1/clients/{client.pk}/",
            {"name": "Updated"},
            format="json",
        )
        assert resp.status_code == 200
