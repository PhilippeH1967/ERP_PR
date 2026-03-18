"""Tests for management commands."""

from io import StringIO

import pytest
from django.core.management import call_command


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
