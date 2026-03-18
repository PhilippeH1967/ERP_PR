"""Tests for ExternalOrganization model."""

import pytest

from apps.core.models import Tenant
from apps.suppliers.models import ExternalOrganization


@pytest.mark.django_db
class TestExternalOrganization:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-ext-org")

    def test_create_organization(self):
        org = ExternalOrganization.objects.create(
            tenant=self.tenant,
            name="WSP Global",
            neq="1234567890",
            type_tags=["st", "partner"],
        )
        assert org.pk is not None
        assert str(org) == "WSP Global"

    def test_type_tags_json(self):
        org = ExternalOrganization.objects.create(
            tenant=self.tenant, name="Arup", type_tags=["competitor"]
        )
        assert org.type_tags == ["competitor"]

    def test_same_org_multiple_tags(self):
        """Same org can be ST on one project and partner on another (FR88b)."""
        org = ExternalOrganization.objects.create(
            tenant=self.tenant,
            name="Multi-Role Corp",
            type_tags=["st", "partner", "competitor"],
        )
        assert "st" in org.type_tags
        assert "partner" in org.type_tags
        assert "competitor" in org.type_tags
