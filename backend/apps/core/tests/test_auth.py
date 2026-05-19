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
class TestTokenRevocation:
    """F5: refresh-token revocation via blacklist + logout."""

    def setup_method(self):
        self.user = User.objects.create_user(username="revuser", password="revpass123!")
        self.tenant = Tenant.objects.create(name="Rev", slug="rev")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)
        self.client = APIClient()

    def _login(self):
        resp = self.client.post(
            "/api/v1/auth/token/",
            {"username": "revuser", "password": "revpass123!"},
            format="json",
        )
        payload = resp.json().get("data", resp.json())
        return payload["refresh"]

    def test_logout_blacklists_refresh(self):
        refresh = self._login()
        logout = self.client.post("/api/v1/auth/logout/", {"refresh": refresh}, format="json")
        assert logout.status_code == 200

        reuse = self.client.post("/api/v1/auth/token/refresh/", {"refresh": refresh}, format="json")
        assert reuse.status_code == 401

    def test_logout_without_refresh_is_400(self):
        assert self.client.post("/api/v1/auth/logout/", {}, format="json").status_code == 400

    def test_rotation_blacklists_old_refresh(self):
        old_refresh = self._login()
        rotated = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
            format="json",
        )
        assert rotated.status_code == 200

        # Old refresh must no longer be replayable after rotation.
        replay = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": old_refresh},
            format="json",
        )
        assert replay.status_code == 401


@pytest.mark.django_db
class TestSsoOnlyFailClosed:
    """F6: a non-ADMIN login must fail closed when the tenant association
    is missing (cannot verify sso_only) or when sso_only is enabled."""

    def setup_method(self):
        from apps.core.models import ProjectRole, Role

        self.Role = Role
        self.ProjectRole = ProjectRole
        self.client = APIClient()

    def _login(self, username, password):
        return self.client.post(
            "/api/v1/auth/token/",
            {"username": username, "password": password},
            format="json",
        )

    def test_non_admin_without_association_is_rejected(self):
        User.objects.create_user(username="orphan", password="pass123!")
        assert self._login("orphan", "pass123!").status_code == 400

    def test_non_admin_sso_only_tenant_is_rejected(self):
        u = User.objects.create_user(username="ssouser", password="pass123!")
        tenant = Tenant.objects.create(name="SSO", slug="sso-t", sso_only=True)
        UserTenantAssociation.objects.create(user=u, tenant=tenant)
        assert self._login("ssouser", "pass123!").status_code == 400

    def test_non_admin_normal_tenant_succeeds(self):
        u = User.objects.create_user(username="normal", password="pass123!")
        tenant = Tenant.objects.create(name="Norm", slug="norm-t")
        UserTenantAssociation.objects.create(user=u, tenant=tenant)
        assert self._login("normal", "pass123!").status_code == 200

    def test_admin_without_association_still_logs_in(self):
        admin = User.objects.create_user(username="ssoadmin", password="pass123!")
        tenant = Tenant.objects.create(name="AdmSSO", slug="adm-sso", sso_only=True)
        self.ProjectRole.objects.create(
            user=admin, tenant=tenant, role=self.Role.ADMIN
        )
        assert self._login("ssoadmin", "pass123!").status_code == 200


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
