"""F8: SSO single-tenant provisioning guard."""

import pytest
from django.contrib.auth.models import User
from django.test import override_settings

from apps.core.models import Tenant, UserTenantAssociation
from apps.core.signals import (
    ensure_user_tenant_association,
    get_or_create_default_tenant,
)


@pytest.mark.django_db
class TestSsoSingleTenantGuard:
    def test_default_tenant_slug_is_configurable(self):
        with override_settings(SSO_DEFAULT_TENANT_SLUG="provencher-roy"):
            tenant = get_or_create_default_tenant()
        assert tenant.slug == "provencher-roy"

    def test_association_created_for_new_user(self):
        user = User.objects.create_user(username="sso1", password="x")
        ensure_user_tenant_association(user)
        assert UserTenantAssociation.objects.filter(user=user).exists()

    def test_multi_tenant_ambiguity_is_logged(self, capsys):
        Tenant.objects.create(name="Org A", slug="org-a")
        Tenant.objects.create(name="Org B", slug="org-b")
        user = User.objects.create_user(username="sso2", password="x")

        with override_settings(SSO_ALLOW_MULTI_TENANT=False):
            ensure_user_tenant_association(user)

        assert "sso_multi_tenant_ambiguous" in capsys.readouterr().out
        # Behaviour preserved: user still provisioned (to the default slug).
        assert UserTenantAssociation.objects.filter(user=user).exists()

    def test_no_warning_when_multi_tenant_allowed(self, capsys):
        Tenant.objects.create(name="Org C", slug="org-c")
        Tenant.objects.create(name="Org D", slug="org-d")
        user = User.objects.create_user(username="sso3", password="x")

        with override_settings(SSO_ALLOW_MULTI_TENANT=True):
            ensure_user_tenant_association(user)

        assert "sso_multi_tenant_ambiguous" not in capsys.readouterr().out
