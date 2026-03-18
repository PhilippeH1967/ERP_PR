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
