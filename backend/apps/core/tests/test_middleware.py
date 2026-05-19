"""Tests for TenantMiddleware."""

import pytest
from django.test import RequestFactory, override_settings
from rest_framework.test import APIClient

from apps.core.middleware import TenantMiddleware
from apps.core.models import Tenant


@pytest.mark.django_db
class TestTenantHeaderFallbackGate:
    """F3: the X-Tenant-Id header fallback must be disabled in production
    (it lets any caller without a tenant JWT claim choose a tenant)."""

    def _resolve(self, tenant_pk):
        captured = {}

        def get_response(request):
            from django.http import HttpResponse

            captured["tenant_id"] = request.tenant_id
            return HttpResponse()

        mw = TenantMiddleware(get_response)
        request = RequestFactory().get("/api/v1/clients/", HTTP_X_TENANT_ID=str(tenant_pk))
        mw(request)
        return captured["tenant_id"]

    @override_settings(TENANT_HEADER_FALLBACK=True)
    def test_header_honored_when_enabled(self):
        tenant = Tenant.objects.create(name="HF on", slug="hf-on")
        assert self._resolve(tenant.pk) == tenant.pk

    @override_settings(TENANT_HEADER_FALLBACK=False)
    def test_header_ignored_when_disabled(self):
        tenant = Tenant.objects.create(name="HF off", slug="hf-off")
        assert self._resolve(tenant.pk) is None


@pytest.mark.django_db
class TestJwtSignatureVerifiedForTenant:
    """F4: the tenant claim driving the RLS SET must come from a
    signature-verified token, not a forged/expired one."""

    def _resolve(self, bearer):
        captured = {}

        def get_response(request):
            from django.http import HttpResponse

            captured["tenant_id"] = request.tenant_id
            return HttpResponse()

        mw = TenantMiddleware(get_response)
        request = RequestFactory().get("/api/v1/clients/", HTTP_AUTHORIZATION=f"Bearer {bearer}")
        mw(request)
        return captured["tenant_id"]

    @override_settings(TENANT_HEADER_FALLBACK=False)
    def test_valid_token_resolves_tenant(self):
        from rest_framework_simplejwt.tokens import AccessToken

        tenant = Tenant.objects.create(name="JWT ok", slug="jwt-ok")
        token = AccessToken()
        token["tenant_id"] = tenant.pk
        assert self._resolve(str(token)) == tenant.pk

    @override_settings(TENANT_HEADER_FALLBACK=False)
    def test_tampered_signature_token_is_rejected(self):
        from rest_framework_simplejwt.tokens import AccessToken

        tenant = Tenant.objects.create(name="JWT bad", slug="jwt-bad")
        token = AccessToken()
        token["tenant_id"] = tenant.pk
        forged = str(token)[:-3] + "AAA"  # corrupt the signature
        assert self._resolve(forged) is None

    @override_settings(TENANT_HEADER_FALLBACK=False)
    def test_expired_token_is_rejected(self):
        from datetime import timedelta

        from rest_framework_simplejwt.tokens import AccessToken

        tenant = Tenant.objects.create(name="JWT exp", slug="jwt-exp")
        token = AccessToken()
        token["tenant_id"] = tenant.pk
        token.set_exp(lifetime=timedelta(seconds=-10))
        assert self._resolve(str(token)) is None


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
