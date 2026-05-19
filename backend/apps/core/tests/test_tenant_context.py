"""Tests for tenant_context (non-request tenant binding)."""

import pytest
from django.db import connection

from apps.core.models import SampleTenantModel, Tenant
from apps.core.tenant_context import tenant_context


@pytest.mark.django_db
class TestTenantContextGuc:
    def test_sets_and_resets_app_current_tenant(self):
        with tenant_context(42), connection.cursor() as cur:
            cur.execute("SELECT current_setting('app.current_tenant')")
            assert cur.fetchone()[0] == "42"

        with connection.cursor() as cur:
            cur.execute("SELECT current_setting('app.current_tenant', true)")
            # Reset → empty (no leak into the next task/iteration).
            assert cur.fetchone()[0] in ("", None)

    def test_none_tenant_id_raises(self):
        with pytest.raises(ValueError), tenant_context(None):
            pass


@pytest.mark.django_db
class TestTenantContextEnforcedUnderAppRole:
    """Proves the helper makes RLS bite for a non-superuser connection —
    the exact DB_APP_USER production scenario."""

    _ROLE = "erp_tc_test_role"

    def test_context_scopes_queries_under_non_superuser(self):
        from io import StringIO

        from django.core.management import call_command

        ta = Tenant.objects.create(name="TC A", slug="tc-a")
        tb = Tenant.objects.create(name="TC B", slug="tc-b")
        call_command("setup_rls", stdout=StringIO())

        with connection.cursor() as cur:
            cur.execute(
                f"DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles "
                f"WHERE rolname='{self._ROLE}') THEN CREATE ROLE {self._ROLE} "
                f"NOSUPERUSER NOBYPASSRLS NOLOGIN; END IF; END $$;"
            )
            cur.execute(f"GRANT ALL ON core_sample TO {self._ROLE};")
            cur.execute(f"GRANT USAGE, SELECT ON SEQUENCE core_sample_id_seq TO {self._ROLE};")
            cur.execute(f"SET ROLE {self._ROLE};")
            try:
                with tenant_context(ta.pk):
                    cur.execute(
                        "INSERT INTO core_sample "
                        "(tenant_id, name, version, created_at, updated_at) "
                        "VALUES (%s, 'A1', 1, now(), now())",
                        [ta.pk],
                    )
                with tenant_context(tb.pk):
                    cur.execute(
                        "INSERT INTO core_sample "
                        "(tenant_id, name, version, created_at, updated_at) "
                        "VALUES (%s, 'B1', 1, now(), now())",
                        [tb.pk],
                    )
                with tenant_context(ta.pk):
                    cur.execute("SELECT count(*) FROM core_sample")
                    assert cur.fetchone()[0] == 1
                    cur.execute("SELECT name FROM core_sample")
                    assert cur.fetchone()[0] == "A1"
            finally:
                cur.execute("RESET ROLE;")

    def test_sample_model_exists(self):
        # guard: model import used so the suite fails loudly if it moves
        assert SampleTenantModel._meta.db_table == "core_sample"
