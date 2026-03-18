"""Tests for client business logic services."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.clients.services import detect_duplicate_client
from apps.core.models import Tenant


@pytest.mark.django_db
class TestDuplicateDetection:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-dup")
        Client.objects.create(tenant=self.tenant, name="Ville de Montréal", alias="VDM")
        Client.objects.create(tenant=self.tenant, name="SNC Lavalin", alias="SNC")

    def test_exact_alias_match(self):
        result = detect_duplicate_client("vdm", self.tenant.pk)
        assert len(result) >= 1
        assert any(d["match_type"] == "alias_exact" for d in result)

    def test_name_contains_match(self):
        # Exact substring match (with accent) works
        result = detect_duplicate_client("Ville de Montréal", self.tenant.pk)
        assert len(result) >= 1

    def test_partial_name_match(self):
        result = detect_duplicate_client("Ville", self.tenant.pk)
        assert len(result) >= 1

    def test_no_match(self):
        result = detect_duplicate_client("Totally New Corp", self.tenant.pk)
        assert len(result) == 0

    def test_exclude_self(self):
        client = Client.objects.create(tenant=self.tenant, name="Test", alias="TST")
        result = detect_duplicate_client("Test", self.tenant.pk, exclude_id=client.pk)
        assert not any(d["id"] == client.pk for d in result)


@pytest.mark.django_db
class TestCheckDuplicateEndpoint:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API", slug="dup-api")
        Client.objects.create(tenant=self.tenant, name="Provencher Roy", alias="PR")
        self.user = User.objects.create_user(username="dup_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_check_duplicate_returns_matches(self):
        response = self.api.post(
            "/api/v1/clients/check_duplicate/",
            {"name": "Provencher"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert len(payload["duplicates"]) >= 1

    def test_check_duplicate_no_match(self):
        response = self.api.post(
            "/api/v1/clients/check_duplicate/",
            {"name": "Completely New"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert len(payload["duplicates"]) == 0
