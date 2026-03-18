"""Tests for TenantMiddleware."""

import pytest
from rest_framework.test import APIClient

from apps.core.models import Tenant


@pytest.mark.django_db
class TestTenantMiddleware:
    """Tests for the TenantMiddleware."""

    def test_request_with_valid_tenant_id(self):
        tenant = Tenant.objects.create(name="Test", slug="test-mw")
        client = APIClient()
        response = client.get("/api/v1/", HTTP_X_TENANT_ID=str(tenant.pk))
        assert response.status_code == 200

    def test_request_without_tenant_id_passes_through(self):
        """Requests without X-Tenant-Id should pass (auth handles enforcement)."""
        client = APIClient()
        response = client.get("/api/v1/")
        assert response.status_code == 200

    def test_request_with_invalid_tenant_id_returns_400(self):
        client = APIClient()
        response = client.get("/api/v1/", HTTP_X_TENANT_ID="not-a-number")
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "INVALID_TENANT"

    def test_request_with_nonexistent_tenant_returns_404(self):
        """Requests with valid integer but non-existent tenant return 404."""
        client = APIClient()
        response = client.get("/api/v1/", HTTP_X_TENANT_ID="999999")
        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "TENANT_NOT_FOUND"

    def test_request_with_inactive_tenant_returns_404(self):
        """Inactive tenants should be rejected."""
        tenant = Tenant.objects.create(name="Inactive", slug="inactive", is_active=False)
        client = APIClient()
        response = client.get("/api/v1/", HTTP_X_TENANT_ID=str(tenant.pk))
        assert response.status_code == 404

    def test_health_endpoint_exempt_from_tenant(self):
        client = APIClient()
        response = client.get("/api/v1/health/")
        assert response.status_code == 200

    def test_schema_endpoint_exempt_from_tenant(self):
        client = APIClient()
        response = client.get("/api/schema/", HTTP_ACCEPT="application/json")
        assert response.status_code == 200
