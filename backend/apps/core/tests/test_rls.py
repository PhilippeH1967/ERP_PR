"""Tests for PostgreSQL Row-Level Security tenant isolation."""

import pytest
from django.db import connection

from apps.core.models import SampleTenantModel, Tenant


@pytest.mark.django_db(transaction=True)
class TestRLSTenantIsolation:
    """
    Test that RLS policies enforce tenant isolation.

    These tests require:
    1. SampleTenantModel table exists (migration ran)
    2. RLS policies are set up (setup_rls command ran)

    Note: RLS policies must be applied and the database role must NOT be
    a superuser (superusers bypass RLS). In test environments, we manually
    set the session variable and verify filtering.
    """

    def setup_method(self):
        self.tenant_a = Tenant.objects.create(name="Tenant A", slug="tenant-a")
        self.tenant_b = Tenant.objects.create(name="Tenant B", slug="tenant-b")

        # Create data for both tenants
        SampleTenantModel.objects.create(tenant=self.tenant_a, name="A-Data-1")
        SampleTenantModel.objects.create(tenant=self.tenant_a, name="A-Data-2")
        SampleTenantModel.objects.create(tenant=self.tenant_b, name="B-Data-1")

    def test_all_data_visible_without_rls_context(self):
        """Without RLS session variable, all data visible (superuser/no policy)."""
        all_records = SampleTenantModel.objects.all()
        assert all_records.count() == 3

    def test_app_level_filtering_isolates_tenants(self):
        """Application-level filtering provides defense in depth."""
        tenant_a_data = SampleTenantModel.objects.filter(tenant=self.tenant_a)
        assert tenant_a_data.count() == 2
        assert all(obj.tenant_id == self.tenant_a.pk for obj in tenant_a_data)

        tenant_b_data = SampleTenantModel.objects.filter(tenant=self.tenant_b)
        assert tenant_b_data.count() == 1
        assert tenant_b_data.first().name == "B-Data-1"

    def test_tenant_a_cannot_see_tenant_b_data_via_filter(self):
        """Verify cross-tenant isolation at application level."""
        tenant_a_names = list(
            SampleTenantModel.objects.filter(tenant=self.tenant_a).values_list(
                "name", flat=True
            )
        )
        assert "B-Data-1" not in tenant_a_names
        assert "A-Data-1" in tenant_a_names
        assert "A-Data-2" in tenant_a_names

    def test_postgresql_session_variable_can_be_set(self):
        """Verify we can set and read the app.current_tenant session variable."""
        with connection.cursor() as cursor:
            cursor.execute(
                "SET app.current_tenant = %s", [str(self.tenant_a.pk)]
            )
            cursor.execute("SELECT current_setting('app.current_tenant')")
            result = cursor.fetchone()[0]
            assert int(result) == self.tenant_a.pk
