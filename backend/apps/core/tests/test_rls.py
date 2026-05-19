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
            SampleTenantModel.objects.filter(tenant=self.tenant_a).values_list("name", flat=True)
        )
        assert "B-Data-1" not in tenant_a_names
        assert "A-Data-1" in tenant_a_names
        assert "A-Data-2" in tenant_a_names

    def test_postgresql_session_variable_can_be_set(self):
        """Verify we can set and read the app.current_tenant session variable."""
        with connection.cursor() as cursor:
            cursor.execute("SET app.current_tenant = %s", [str(self.tenant_a.pk)])
            cursor.execute("SELECT current_setting('app.current_tenant')")
            result = cursor.fetchone()[0]
            assert int(result) == self.tenant_a.pk


@pytest.mark.django_db
class TestRLSForcedIsolationUnderOwnerConnection:
    """F1: with setup_rls applied, the policy must filter even when the
    connection role owns the tables (the production reality).

    This is the regression test for the inert-RLS finding. It currently
    relies on FORCE ROW LEVEL SECURITY: without FORCE, the owner role
    sees all rows and these assertions fail.
    """

    # A non-superuser, non-owner role: the production-correct shape of the
    # Django connection. Superusers AND table owners bypass RLS, so the
    # regression must be asserted under a role that is neither.
    _APP_ROLE = "erp_rls_test_role"

    def _grant_app_role(self, cursor):
        cursor.execute(
            f"DO $$ BEGIN IF NOT EXISTS ("
            f"SELECT FROM pg_roles WHERE rolname = '{self._APP_ROLE}') THEN "
            f"CREATE ROLE {self._APP_ROLE} NOSUPERUSER NOBYPASSRLS NOLOGIN; "
            f"END IF; END $$;"
        )
        cursor.execute(f"GRANT ALL ON core_sample TO {self._APP_ROLE};")
        cursor.execute(f"GRANT USAGE, SELECT ON SEQUENCE core_sample_id_seq TO {self._APP_ROLE};")

    def _insert_sample(self, cursor, tenant_id, name):
        cursor.execute(
            "INSERT INTO core_sample "
            "(tenant_id, name, version, created_at, updated_at) "
            "VALUES (%s, %s, 1, now(), now())",
            [tenant_id, name],
        )

    def test_owner_connection_is_filtered_by_app_current_tenant(self):
        from io import StringIO

        from django.core.management import call_command

        tenant_a = Tenant.objects.create(name="Owner A", slug="own-a")
        tenant_b = Tenant.objects.create(name="Owner B", slug="own-b")

        # Apply RLS BEFORE inserting tenant-scoped rows (a real migration
        # runs setup_rls outside any data-insert transaction).
        call_command("setup_rls", stdout=StringIO())

        with connection.cursor() as cursor:
            self._grant_app_role(cursor)
            cursor.execute(f"SET ROLE {self._APP_ROLE};")
            try:
                # WITH CHECK forces tenant_id == app.current_tenant on INSERT.
                cursor.execute("SET app.current_tenant = %s", [str(tenant_a.pk)])
                self._insert_sample(cursor, tenant_a.pk, "OA-1")
                self._insert_sample(cursor, tenant_a.pk, "OA-2")
                cursor.execute("SET app.current_tenant = %s", [str(tenant_b.pk)])
                self._insert_sample(cursor, tenant_b.pk, "OB-1")

                cursor.execute("SET app.current_tenant = %s", [str(tenant_a.pk)])
                cursor.execute("SELECT count(*) FROM core_sample")
                assert cursor.fetchone()[0] == 2, (
                    "Non-superuser connection must NOT see tenant B rows"
                )

                cursor.execute("SET app.current_tenant = %s", [str(tenant_b.pk)])
                cursor.execute("SELECT count(*) FROM core_sample")
                assert cursor.fetchone()[0] == 1

                cursor.execute("SELECT name FROM core_sample WHERE name LIKE 'OA%%'")
                assert cursor.fetchall() == [], "Tenant B context must not leak tenant A rows"
            finally:
                cursor.execute("RESET ROLE;")

    def test_with_check_blocks_cross_tenant_insert(self):
        """RLS WITH CHECK must reject an INSERT whose tenant_id differs
        from app.current_tenant (write-side isolation)."""
        from io import StringIO

        from django.core.management import call_command
        from django.db import InternalError, ProgrammingError, transaction

        tenant_a = Tenant.objects.create(name="WC A", slug="wc-a")
        tenant_b = Tenant.objects.create(name="WC B", slug="wc-b")
        call_command("setup_rls", stdout=StringIO())

        with connection.cursor() as cursor:
            self._grant_app_role(cursor)
            cursor.execute(f"SET ROLE {self._APP_ROLE};")
            try:
                cursor.execute("SET app.current_tenant = %s", [str(tenant_a.pk)])
                # Savepoint so the policy violation rolls back cleanly and
                # leaves the connection usable for RESET ROLE / teardown.
                with (
                    pytest.raises((InternalError, ProgrammingError)),
                    transaction.atomic(),
                ):
                    self._insert_sample(cursor, tenant_b.pk, "forged")
            finally:
                cursor.execute("RESET ROLE;")
