"""F2: admin user-management endpoints must be scoped to the caller's tenant.

Regression tests for the cross-tenant admin takeover finding: an ADMIN of
tenant A must not list / update / delete / reset the password of users
belonging to tenant B, and newly created users must be bound to the
caller's tenant (never an arbitrary ``Tenant.objects.first()``).
"""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation


@pytest.mark.django_db
class TestUserEndpointsTenantScoping:
    def setup_method(self):
        self.tenant_a = Tenant.objects.create(name="A", slug="f2-a")
        self.tenant_b = Tenant.objects.create(name="B", slug="f2-b")

        self.admin_a = User.objects.create_user("admin_a", password="pass123!")
        UserTenantAssociation.objects.create(user=self.admin_a, tenant=self.tenant_a)
        ProjectRole.objects.create(user=self.admin_a, tenant=self.tenant_a, role=Role.ADMIN)

        self.user_b = User.objects.create_user("user_b", password="pass123!", email="b@b.com")
        UserTenantAssociation.objects.create(user=self.user_b, tenant=self.tenant_b)
        ProjectRole.objects.create(user=self.user_b, tenant=self.tenant_b, role=Role.EMPLOYEE)

        self.user_a = User.objects.create_user("user_a", password="pass123!")
        UserTenantAssociation.objects.create(user=self.user_a, tenant=self.tenant_a)

        self.api = APIClient()
        self.api.force_authenticate(user=self.admin_a)

    def test_user_list_excludes_other_tenant(self):
        resp = self.api.get("/api/v1/users/", HTTP_X_TENANT_ID=str(self.tenant_a.pk))
        assert resp.status_code == 200
        usernames = [u["username"] for u in resp.json()["data"]]
        assert "user_a" in usernames
        assert "admin_a" in usernames
        assert "user_b" not in usernames

    def test_user_search_excludes_other_tenant(self):
        resp = self.api.get(
            "/api/v1/users/search/?q=user",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        assert resp.status_code == 200
        usernames = [u["username"] for u in resp.json()["data"]]
        assert "user_a" in usernames
        assert "user_b" not in usernames

    def test_update_cross_tenant_user_is_404(self):
        resp = self.api.patch(
            f"/api/v1/users/{self.user_b.pk}/",
            {"password": "hacked123!"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        assert resp.status_code == 404
        self.user_b.refresh_from_db()
        assert self.user_b.check_password("pass123!"), "password must be unchanged"

    def test_delete_cross_tenant_user_is_404(self):
        resp = self.api.delete(
            f"/api/v1/users/{self.user_b.pk}/delete/",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        assert resp.status_code == 404
        assert User.objects.filter(pk=self.user_b.pk).exists()

    def test_create_binds_to_caller_tenant(self):
        resp = self.api.post(
            "/api/v1/users/create/",
            {"username": "fresh", "password": "pass123!", "role": "EMPLOYEE"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        assert resp.status_code == 201
        fresh = User.objects.get(username="fresh")
        assert fresh.tenant_association.tenant_id == self.tenant_a.pk
        assert ProjectRole.objects.filter(
            user=fresh, tenant=self.tenant_a, role=Role.EMPLOYEE
        ).exists()

    def test_same_tenant_management_still_works(self):
        resp = self.api.patch(
            f"/api/v1/users/{self.user_a.pk}/",
            {"is_active": False},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant_a.pk),
        )
        assert resp.status_code == 200
        self.user_a.refresh_from_db()
        assert self.user_a.is_active is False
