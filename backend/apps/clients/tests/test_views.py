"""Tests for Client API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.clients.models import Client, Contact
from apps.core.models import Tenant


@pytest.mark.django_db
class TestClientAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API Test", slug="api-test")
        self.user = User.objects.create_user(username="api_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_clients_empty(self):
        response = self.api.get("/api/v1/clients/")
        assert response.status_code == 200

    def test_create_client(self):
        response = self.api.post(
            "/api/v1/clients/",
            {"name": "New Client", "alias": "NC", "status": "active"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_retrieve_client(self):
        client = Client.objects.create(
            tenant=self.tenant, name="Retrieve Me", alias="RM"
        )
        response = self.api.get(f"/api/v1/clients/{client.pk}/")
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["name"] == "Retrieve Me"

    def test_update_client_with_version(self):
        client = Client.objects.create(
            tenant=self.tenant, name="Update Me", alias="UM"
        )
        response = self.api.patch(
            f"/api/v1/clients/{client.pk}/",
            {"name": "Updated"},
            format="json",
            HTTP_IF_MATCH="1",
        )
        assert response.status_code == 200

    def test_search_clients(self):
        Client.objects.create(tenant=self.tenant, name="Provencher Roy", alias="PR")
        Client.objects.create(tenant=self.tenant, name="SNC Lavalin", alias="SNC")
        response = self.api.get("/api/v1/clients/?search=Provencher")
        assert response.status_code == 200

    def test_filter_by_status(self):
        Client.objects.create(tenant=self.tenant, name="Active", status="active")
        Client.objects.create(tenant=self.tenant, name="Inactive", status="inactive")
        response = self.api.get("/api/v1/clients/?status=active")
        assert response.status_code == 200

    def test_financial_summary_endpoint(self):
        client = Client.objects.create(tenant=self.tenant, name="Financial")
        response = self.api.get(f"/api/v1/clients/{client.pk}/financial_summary/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestContactAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Contact API", slug="contact-api")
        self.client_obj = Client.objects.create(
            tenant=self.tenant, name="Client With Contacts"
        )
        self.user = User.objects.create_user(username="contact_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_contacts(self):
        Contact.objects.create(
            tenant=self.tenant, client=self.client_obj,
            name="Contact 1", email="c1@test.com"
        )
        response = self.api.get(
            f"/api/v1/clients/{self.client_obj.pk}/contacts/"
        )
        assert response.status_code == 200

    def test_create_contact(self):
        response = self.api.post(
            f"/api/v1/clients/{self.client_obj.pk}/contacts/",
            {"name": "New Contact", "email": "new@test.com", "role": "PM"},
            format="json",
        )
        assert response.status_code == 201


@pytest.mark.django_db
class TestClientAddressDedup:
    """Anti-doublon : une même adresse (ligne 1 + ville + code postal,
    insensible à la casse/espaces) ne peut pas être créée deux fois pour un
    même client."""

    def _setup(self):
        from apps.clients.models import Client, ClientAddress
        from apps.core.models import Tenant

        tenant = Tenant.objects.create(name="T", slug="t-addr-dedup")
        client = Client.objects.create(tenant=tenant, name="VDM", alias="VDM")
        addr = ClientAddress.objects.create(
            tenant=tenant, client=client,
            address_line_1="275 rue Notre-Dame E", city="Montréal",
            province="QC", postal_code="H2Y 1C6",
        )
        from django.contrib.auth.models import User
        from rest_framework.test import APIClient

        user = User.objects.create_user(username="addr_user", password="x")
        api = APIClient()
        api.force_authenticate(user=user)
        return tenant, client, addr, api

    def test_duplicate_rejected_case_and_space_insensitive(self):
        tenant, client, _addr, api = self._setup()
        resp = api.post(
            f"/api/v1/clients/{client.pk}/addresses/",
            {"address_line_1": "  275 RUE notre-dame e ", "city": "MONTRÉAL",
             "postal_code": "h2y1c6"},
            format="json", HTTP_X_TENANT_ID=str(tenant.pk),
        )
        assert resp.status_code == 400
        assert "existe déjà" in str(resp.data)

    def test_different_city_accepted(self):
        tenant, client, _addr, api = self._setup()
        resp = api.post(
            f"/api/v1/clients/{client.pk}/addresses/",
            {"address_line_1": "275 rue Notre-Dame E", "city": "Québec",
             "postal_code": "G1R 4S9"},
            format="json", HTTP_X_TENANT_ID=str(tenant.pk),
        )
        assert resp.status_code == 201, resp.data

    def test_update_own_address_not_flagged_as_duplicate(self):
        tenant, client, addr, api = self._setup()
        resp = api.patch(
            f"/api/v1/clients/{client.pk}/addresses/{addr.pk}/",
            {"address_line_2": "Bureau 400"},
            format="json", HTTP_X_TENANT_ID=str(tenant.pk),
        )
        assert resp.status_code == 200, resp.data


@pytest.mark.django_db
class TestClientAddressDedupFuzzy:
    """Anti-doublon renforcé : accents, ponctuation, particules (d', de…),
    abréviations de voie (av/avenue…) — et le code postal ne « sauve » pas un
    doublon (une adresse civique = un seul code postal)."""

    def _setup(self, line1="4553 av oxford", city="Montreal", postal="H4A2Y9"):
        from apps.clients.models import Client, ClientAddress
        from apps.core.models import Tenant

        tenant = Tenant.objects.create(name="T", slug=f"t-fz-{line1[:6].strip()}")
        client = Client.objects.create(tenant=tenant, name="C", alias="C")
        ClientAddress.objects.create(
            tenant=tenant, client=client,
            address_line_1=line1, city=city, postal_code=postal,
        )
        from django.contrib.auth.models import User
        from rest_framework.test import APIClient

        user = User.objects.create_user(username=f"fz{tenant.pk}", password="x")
        api = APIClient()
        api.force_authenticate(user=user)
        return tenant, client, api

    def _post(self, tenant, client, api, **payload):
        return api.post(
            f"/api/v1/clients/{client.pk}/addresses/", payload,
            format="json", HTTP_X_TENANT_ID=str(tenant.pk),
        )

    def test_cas_terrain_apostrophe_particule_et_postal_different(self):
        tenant, client, api = self._setup()
        resp = self._post(
            tenant, client, api,
            address_line_1="4553 Av d'Oxford", city="Montreal", postal_code="H4A 2Y8",
        )
        assert resp.status_code == 400
        assert "existe déjà" in str(resp.data)

    def test_accents_et_abreviation_avenue(self):
        tenant, client, api = self._setup(line1="1 avenue Émile-Zola", city="Montréal")
        resp = self._post(
            tenant, client, api,
            address_line_1="1 av Emile Zola", city="Montreal", postal_code="H1H 1H1",
        )
        assert resp.status_code == 400

    def test_numero_civique_different_accepte(self):
        tenant, client, api = self._setup()
        resp = self._post(
            tenant, client, api,
            address_line_1="4555 av Oxford", city="Montreal", postal_code="H4A 2Y9",
        )
        assert resp.status_code == 201, resp.data


@pytest.mark.django_db
class TestClientAddressDeleteProtection:
    """Suppression d'adresse : interdite si l'adresse est utilisée comme
    adresse de facturation d'un projet."""

    def _setup(self):
        from apps.clients.models import Client, ClientAddress
        from apps.core.models import Tenant

        tenant = Tenant.objects.create(name="T", slug="t-addr-del")
        client = Client.objects.create(tenant=tenant, name="VDM", alias="VDM")
        addr = ClientAddress.objects.create(
            tenant=tenant, client=client,
            address_line_1="275 rue Notre-Dame E", city="Montréal",
        )
        from django.contrib.auth.models import User
        from rest_framework.test import APIClient

        user = User.objects.create_user(username="del_user", password="x")
        api = APIClient()
        api.force_authenticate(user=user)
        return tenant, client, addr, api

    def test_delete_blocked_when_used_as_project_billing_address(self):
        from apps.clients.models import ClientAddress
        from apps.projects.models import Project

        tenant, client, addr, api = self._setup()
        Project.objects.create(
            tenant=tenant, code="PRJ-X", name="P", client=client, billing_address=addr
        )
        resp = api.delete(
            f"/api/v1/clients/{client.pk}/addresses/{addr.pk}/",
            HTTP_X_TENANT_ID=str(tenant.pk),
        )
        assert resp.status_code == 409
        assert "PRJ-X" in str(resp.data)
        assert ClientAddress.objects.filter(pk=addr.pk).exists()

    def test_delete_allowed_when_unused(self):
        from apps.clients.models import ClientAddress

        tenant, client, addr, api = self._setup()
        resp = api.delete(
            f"/api/v1/clients/{client.pk}/addresses/{addr.pk}/",
            HTTP_X_TENANT_ID=str(tenant.pk),
        )
        assert resp.status_code == 204
        assert not ClientAddress.objects.filter(pk=addr.pk).exists()
