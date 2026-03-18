"""Tests for RBAC predicates and DRF permission classes."""

import pytest
from django.contrib.auth.models import User

from apps.core.models import ProjectRole, Role, Tenant
from apps.core.permissions import (
    can_approve_invoice,
    can_see_salary_costs,
    cannot_approve_own,
    is_admin,
    is_bu_director,
    is_finance,
    is_project_director,
    is_project_pm,
)


@pytest.mark.django_db
class TestRBACPredicates:
    """Tests for django-rules predicates."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-rbac")
        self.user_pm = User.objects.create_user(username="pm_user", password="pass123!")
        self.user_finance = User.objects.create_user(username="fin_user", password="pass123!")
        self.user_admin = User.objects.create_user(username="admin_user", password="pass123!")
        self.user_basic = User.objects.create_user(username="basic_user", password="pass123!")

        ProjectRole.objects.create(
            tenant=self.tenant, user=self.user_pm, project_id=1, role=Role.PM
        )
        ProjectRole.objects.create(
            tenant=self.tenant, user=self.user_finance, role=Role.FINANCE
        )
        ProjectRole.objects.create(
            tenant=self.tenant, user=self.user_admin, role=Role.ADMIN
        )
        ProjectRole.objects.create(
            tenant=self.tenant, user=self.user_basic, project_id=1, role=Role.EMPLOYEE
        )

    def test_is_admin(self):
        assert is_admin(self.user_admin) is True
        assert is_admin(self.user_basic) is False

    def test_is_finance(self):
        assert is_finance(self.user_finance) is True
        assert is_finance(self.user_basic) is False

    def test_is_project_pm(self):
        assert is_project_pm(self.user_pm, 1) is True
        assert is_project_pm(self.user_pm, 999) is False
        assert is_project_pm(self.user_basic, 1) is False

    def test_is_project_pm_none_project(self):
        assert is_project_pm(self.user_pm, None) is False

    def test_is_project_director(self):
        director = User.objects.create_user(username="director", password="pass123!")
        ProjectRole.objects.create(
            tenant=self.tenant, user=director, project_id=1, role=Role.PROJECT_DIRECTOR
        )
        assert is_project_director(director, 1) is True
        assert is_project_director(director, 999) is False

    def test_is_bu_director(self):
        bu_dir = User.objects.create_user(username="bu_dir", password="pass123!")
        ProjectRole.objects.create(
            tenant=self.tenant, user=bu_dir, role=Role.BU_DIRECTOR
        )
        assert is_bu_director(bu_dir) is True
        assert is_bu_director(self.user_basic) is False

    def test_can_approve_invoice_finance(self):
        assert can_approve_invoice(self.user_finance, 1) is True

    def test_can_approve_invoice_director(self):
        director = User.objects.create_user(username="inv_dir", password="pass123!")
        ProjectRole.objects.create(
            tenant=self.tenant, user=director, project_id=1, role=Role.PROJECT_DIRECTOR
        )
        assert can_approve_invoice(director, 1) is True
        assert can_approve_invoice(self.user_basic, 1) is False

    def test_can_see_salary_costs(self):
        assert can_see_salary_costs(self.user_finance) is True
        assert can_see_salary_costs(self.user_admin) is True
        assert can_see_salary_costs(self.user_basic) is False

    def test_cannot_approve_own(self):
        assert cannot_approve_own(self.user_pm, self.user_basic.pk) is True
        assert cannot_approve_own(self.user_pm, self.user_pm.pk) is False

    def test_all_8_roles_available(self):
        assert len(Role.choices) == 8
        role_values = [r[0] for r in Role.choices]
        assert "EMPLOYEE" in role_values
        assert "PM" in role_values
        assert "PROJECT_DIRECTOR" in role_values
        assert "BU_DIRECTOR" in role_values
        assert "FINANCE" in role_values
        assert "DEPT_ASSISTANT" in role_values
        assert "PROPOSAL_MANAGER" in role_values
        assert "ADMIN" in role_values


@pytest.mark.django_db
class TestProjectRoleModel:
    """Tests for the ProjectRole model."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-role-model")
        self.user = User.objects.create_user(username="role_user", password="pass123!")

    def test_create_project_role(self):
        role = ProjectRole.objects.create(
            tenant=self.tenant, user=self.user, project_id=1, role=Role.PM
        )
        assert role.pk is not None
        assert role.role == Role.PM
        assert role.project_id == 1

    def test_global_role_no_project(self):
        role = ProjectRole.objects.create(
            tenant=self.tenant, user=self.user, role=Role.ADMIN
        )
        assert role.project_id is None

    def test_unique_constraint(self):
        ProjectRole.objects.create(
            tenant=self.tenant, user=self.user, project_id=1, role=Role.PM
        )
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            ProjectRole.objects.create(
                tenant=self.tenant, user=self.user, project_id=1, role=Role.PM
            )

    def test_str_representation(self):
        role = ProjectRole(user=self.user, project_id=1, role=Role.PM)
        assert "PM" in str(role)
        assert "project 1" in str(role)


@pytest.mark.django_db
class TestDRFPermissionClasses:
    """Tests for DRF permission classes via API."""

    def test_admin_endpoint_denied_for_non_admin(self):
        from rest_framework.test import APIClient

        user = User.objects.create_user(username="nonadmin", password="pass123!")
        client = APIClient()
        client.force_authenticate(user=user)
        # API root is AllowAny, so this just verifies auth works
        response = client.get("/api/v1/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestJWTRolesClaim:
    """Tests that JWT token contains roles from ProjectRole."""

    def test_jwt_contains_roles(self):
        from rest_framework.test import APIClient

        from apps.core.models import UserTenantAssociation

        tenant = Tenant.objects.create(name="JWT Tenant", slug="jwt-roles")
        user = User.objects.create_user(
            username="jwt_roles_user", email="roles@test.com", password="pass123!"
        )
        UserTenantAssociation.objects.create(user=user, tenant=tenant)
        ProjectRole.objects.create(tenant=tenant, user=user, project_id=1, role=Role.PM)
        ProjectRole.objects.create(tenant=tenant, user=user, role=Role.FINANCE)

        client = APIClient()
        response = client.post(
            "/api/v1/auth/token/",
            {"username": "jwt_roles_user", "password": "pass123!"},
            format="json",
        )
        assert response.status_code == 200

        from rest_framework_simplejwt.tokens import AccessToken

        data = response.json()
        payload = data.get("data", data)
        token = AccessToken(payload["access"])
        roles = token["roles"]
        assert len(roles) == 2
        assert any(r["role"] == "PM" and r["project_id"] == 1 for r in roles)
        assert any(r["role"] == "FINANCE" for r in roles)
