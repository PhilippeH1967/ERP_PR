"""Tests for management commands."""

from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError


@pytest.mark.django_db
class TestSetupRLSCommand:
    """Tests for the setup_rls management command."""

    def test_command_runs_successfully(self):
        """setup_rls should execute without errors."""
        out = StringIO()
        call_command("setup_rls", stdout=out)
        output = out.getvalue()
        assert "Done:" in output

    def test_command_finds_tenant_scoped_models(self):
        """Command should discover SampleTenantModel."""
        out = StringIO()
        call_command("setup_rls", stdout=out)
        output = out.getvalue()
        assert "core_sample" in output

    def test_command_is_idempotent(self):
        """Running setup_rls twice should not error."""
        out1 = StringIO()
        call_command("setup_rls", stdout=out1)
        assert "Done:" in out1.getvalue()

        out2 = StringIO()
        call_command("setup_rls", stdout=out2)
        assert "Done:" in out2.getvalue()
        assert "error" not in out2.getvalue().lower()

    def test_command_forces_rls_on_tables(self):
        """F1: RLS must be FORCED so the table-owner connection is not exempt.

        Without FORCE ROW LEVEL SECURITY, the role owning the tables (the
        Django connection role in this deployment) bypasses every policy,
        making tenant isolation inert. relforcerowsecurity must be true.
        """
        from django.db import connection

        call_command("setup_rls", stdout=StringIO())
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT relrowsecurity, relforcerowsecurity "
                "FROM pg_class WHERE relname = 'core_sample'"
            )
            relrowsecurity, relforcerowsecurity = cursor.fetchone()
        assert relrowsecurity is True, "RLS must be ENABLED on core_sample"
        assert relforcerowsecurity is True, (
            "RLS must be FORCED on core_sample (owner would otherwise bypass)"
        )


@pytest.mark.django_db
class TestSetupDbRolesCommand:
    """F1: least-privilege application DB role."""

    ROLE = "erp_app_unittest"

    def _role_attrs(self, role):
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT rolsuper, rolbypassrls, rolcanlogin FROM pg_roles WHERE rolname = %s",
                [role],
            )
            return cursor.fetchone()

    def test_creates_nonsuperuser_nobypassrls_login_role(self):
        call_command("setup_db_roles", role=self.ROLE, password="s3cret!", stdout=StringIO())
        rolsuper, rolbypassrls, rolcanlogin = self._role_attrs(self.ROLE)
        assert rolsuper is False, "App role must NOT be superuser"
        assert rolbypassrls is False, "App role must NOT bypass RLS"
        assert rolcanlogin is True, "App role must be able to log in"

    def test_grants_dml_on_existing_tables(self):
        from django.db import connection

        call_command("setup_db_roles", role=self.ROLE, password="s3cret!", stdout=StringIO())
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT has_table_privilege(%s, 'core_sample', 'SELECT'), "
                "has_table_privilege(%s, 'core_sample', 'INSERT')",
                [self.ROLE, self.ROLE],
            )
            can_select, can_insert = cursor.fetchone()
        assert can_select is True
        assert can_insert is True

    def test_missing_password_raises(self):
        with pytest.raises(CommandError):
            call_command("setup_db_roles", role=self.ROLE, password="", stdout=StringIO())

    def test_invalid_role_name_raises(self):
        with pytest.raises(CommandError):
            call_command("setup_db_roles", role="bad-role; DROP", password="x", stdout=StringIO())

    def test_idempotent(self):
        call_command("setup_db_roles", role=self.ROLE, password="s3cret!", stdout=StringIO())
        out = StringIO()
        call_command("setup_db_roles", role=self.ROLE, password="s3cret!", stdout=out)
        assert "Done:" in out.getvalue()
