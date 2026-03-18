"""Tests for JWT authentication and custom token claims."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apps.core.models import Tenant, UserTenantAssociation


@pytest.mark.django_db
class TestJWTTokenObtain:
    """Tests for the token obtain endpoint."""

    def setup_method(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@provencher-roy.com",
            password="testpass123!",
        )
        self.tenant = Tenant.objects.create(name="Test Tenant", slug="test-jwt")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)

    def test_token_obtain_returns_access_and_refresh(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123!"},
            format="json",
        )
        assert response.status_code == 200
        data = response.json()
        # Response wrapped in {"data": ...}
        payload = data.get("data", data)
        assert "access" in payload
        assert "refresh" in payload

    def test_token_contains_custom_claims(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123!"},
            format="json",
        )
        data = response.json()
        payload = data.get("data", data)
        token = AccessToken(payload["access"])

        assert int(token["user_id"]) == self.user.pk
        assert token["email"] == "test@provencher-roy.com"
        assert token["tenant_id"] == self.tenant.pk
        assert isinstance(token["roles"], list)

    def test_token_obtain_invalid_credentials_returns_401(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "wrongpassword"},
            format="json",
        )
        assert response.status_code == 401

    def test_token_refresh_returns_new_access(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123!"},
            format="json",
        )
        data = response.json()
        payload = data.get("data", data)
        refresh_token = payload["refresh"]

        refresh_response = client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )
        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        refresh_payload = refresh_data.get("data", refresh_data)
        assert "access" in refresh_payload

    def test_token_verify_valid_token(self):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "testuser", "password": "testpass123!"},
            format="json",
        )
        data = response.json()
        payload = data.get("data", data)

        verify_response = client.post(
            "/api/v1/auth/token/verify/",
            {"token": payload["access"]},
            format="json",
        )
        assert verify_response.status_code == 200


@pytest.mark.django_db
class TestJWTAuthentication:
    """Tests for JWT-authenticated API requests."""

    def setup_method(self):
        self.user = User.objects.create_user(
            username="authuser",
            email="auth@provencher-roy.com",
            password="authpass123!",
        )
        self.tenant = Tenant.objects.create(name="Auth Tenant", slug="auth-tenant")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)

    def _get_token(self, client):
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "authuser", "password": "authpass123!"},
            format="json",
        )
        data = response.json()
        payload = data.get("data", data)
        return payload["access"]

    def test_authenticated_request_with_jwt(self):
        client = APIClient()
        token = self._get_token(client)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = client.get("/api/v1/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserTenantAssociation:
    """Tests for the UserTenantAssociation model."""

    def test_create_association(self):
        user = User.objects.create_user(username="assocuser", password="pass123!")
        tenant = Tenant.objects.create(name="Assoc Tenant", slug="assoc")
        assoc = UserTenantAssociation.objects.create(user=user, tenant=tenant)
        assert assoc.user == user
        assert assoc.tenant == tenant
        assert str(assoc) == f"{user} → {tenant}"

    def test_one_to_one_constraint(self):
        user = User.objects.create_user(username="oneuser", password="pass123!")
        tenant = Tenant.objects.create(name="One Tenant", slug="one")
        UserTenantAssociation.objects.create(user=user, tenant=tenant)

        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            UserTenantAssociation.objects.create(user=user, tenant=tenant)
