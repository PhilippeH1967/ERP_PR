"""Tests for the admin db-dump endpoint."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation


@pytest.mark.django_db
class TestDbDumpEndpoint:
    """GET /api/v1/admin/db-dump/ — admin-only DB dump for support /
    debugging. Wraps pg_dump and returns the file as an attachment."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="DD", slug="dd-dump")
        self.admin = User.objects.create_user("dd_admin", password="x")
        UserTenantAssociation.objects.create(user=self.admin, tenant=self.tenant)
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        self.regular = User.objects.create_user("dd_regular", password="x")
        UserTenantAssociation.objects.create(user=self.regular, tenant=self.tenant)
        self.api = APIClient()

    def test_unauthenticated_returns_401(self):
        resp = APIClient().get("/api/v1/admin/db-dump/")
        assert resp.status_code == 401

    def test_non_admin_returns_403(self):
        self.api.force_authenticate(user=self.regular)
        resp = self.api.get("/api/v1/admin/db-dump/")
        assert resp.status_code == 403

    def test_admin_receives_pg_dump_attachment(self):
        self.api.force_authenticate(user=self.admin)
        resp = self.api.get("/api/v1/admin/db-dump/")
        assert resp.status_code == 200
        assert resp["Content-Type"] == "application/octet-stream"
        cd = resp["Content-Disposition"]
        assert "attachment" in cd
        assert ".dump" in cd
        # pg_dump custom format files start with the magic bytes "PGDMP".
        body = b"".join(resp.streaming_content) if resp.streaming else resp.content
        assert body.startswith(b"PGDMP"), "Expected pg_dump custom-format file (starts with PGDMP)"
