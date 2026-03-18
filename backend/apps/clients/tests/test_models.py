"""Tests for Client, Contact, and ClientAddress models."""

import pytest

from apps.clients.models import Client, ClientAddress, Contact
from apps.core.models import Tenant


@pytest.mark.django_db
class TestClientModel:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-client")

    def test_create_client(self):
        client = Client.objects.create(
            tenant=self.tenant, name="Ville de Montréal", alias="VDM"
        )
        assert client.pk is not None
        assert client.status == "active"
        assert client.version == 1

    def test_client_str(self):
        client = Client(name="Test Corp", alias="TC")
        assert str(client) == "TC"

    def test_client_str_no_alias(self):
        client = Client(name="Test Corp", alias="")
        assert str(client) == "Test Corp"

    def test_client_version_increments(self):
        client = Client.objects.create(
            tenant=self.tenant, name="Versioned", alias="VER"
        )
        assert client.version == 1
        client.name = "Versioned Updated"
        client.save()
        assert client.version == 2

    def test_client_history_tracked(self):
        client = Client.objects.create(
            tenant=self.tenant, name="Audited", alias="AUD"
        )
        client.name = "Audited Changed"
        client.save()
        assert client.history.count() == 2

    def test_client_cascade_on_tenant_delete(self):
        Client.objects.create(tenant=self.tenant, name="Cascade")
        self.tenant.delete()
        assert Client.objects.count() == 0


@pytest.mark.django_db
class TestContactModel:
    def test_create_contact(self):
        tenant = Tenant.objects.create(name="T", slug="t-contact")
        client = Client.objects.create(tenant=tenant, name="C")
        contact = Contact.objects.create(
            tenant=tenant, client=client, name="Jean Tremblay",
            email="jean@test.com", role="PM"
        )
        assert contact.pk is not None
        assert str(contact) == "Jean Tremblay (C)"


@pytest.mark.django_db
class TestClientAddressModel:
    def test_create_address(self):
        tenant = Tenant.objects.create(name="T", slug="t-addr")
        client = Client.objects.create(tenant=tenant, name="C")
        addr = ClientAddress.objects.create(
            tenant=tenant, client=client,
            address_line_1="100 rue Sainte-Catherine",
            city="Montréal", postal_code="H2X 1K3",
            is_billing=True
        )
        assert addr.pk is not None
        assert "Sainte-Catherine" in str(addr)
