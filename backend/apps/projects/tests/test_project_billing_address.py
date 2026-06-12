"""Adresse de facturation spécifique au projet (Project.billing_address).

Un client peut avoir plusieurs adresses ; chaque projet peut désigner CELLE
qui s'applique à sa facturation. Sans désignation, l'adresse de facturation
par défaut du client s'applique (comportement aval).
"""

import pytest

from apps.clients.models import Client, ClientAddress
from apps.projects.models import Project


@pytest.fixture
def client_with_addresses(tenant):
    c = Client.objects.create(tenant=tenant, name="Ville de Montréal", alias="VDM")
    a1 = ClientAddress.objects.create(
        tenant=tenant, client=c, address_line_1="275 rue Notre-Dame E",
        city="Montréal", province="QC", postal_code="H2Y 1C6", is_billing=True,
    )
    a2 = ClientAddress.objects.create(
        tenant=tenant, client=c, address_line_1="801 rue Brennan",
        city="Montréal", province="QC", postal_code="H3C 0G4",
    )
    return c, a1, a2


@pytest.mark.django_db
class TestProjectBillingAddress:
    def test_patch_sets_project_billing_address(
        self, admin_client, tenant, client_with_addresses
    ):
        c, _a1, a2 = client_with_addresses
        project = Project.objects.create(
            tenant=tenant, code="BA-1", name="P", client=c
        )
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"billing_address": a2.pk},
            format="json",
        )
        assert resp.status_code == 200, resp.data
        project.refresh_from_db()
        assert project.billing_address_id == a2.pk

    def test_rejects_address_of_another_client(
        self, admin_client, tenant, client_with_addresses
    ):
        c, _a1, _a2 = client_with_addresses
        other = Client.objects.create(tenant=tenant, name="Autre", alias="AU")
        foreign = ClientAddress.objects.create(
            tenant=tenant, client=other, address_line_1="1 rue X", city="Québec"
        )
        project = Project.objects.create(
            tenant=tenant, code="BA-2", name="P", client=c
        )
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"billing_address": foreign.pk},
            format="json",
        )
        assert resp.status_code == 400
        project.refresh_from_db()
        assert project.billing_address_id is None

    def test_null_resets_to_client_default(
        self, admin_client, tenant, client_with_addresses
    ):
        c, a1, _a2 = client_with_addresses
        project = Project.objects.create(
            tenant=tenant, code="BA-3", name="P", client=c, billing_address=a1
        )
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"billing_address": None},
            format="json",
        )
        assert resp.status_code == 200, resp.data
        project.refresh_from_db()
        assert project.billing_address_id is None

    def test_changing_client_clears_stale_billing_address(
        self, admin_client, tenant, client_with_addresses
    ):
        c, a1, _a2 = client_with_addresses
        other = Client.objects.create(tenant=tenant, name="Autre", alias="AU2")
        project = Project.objects.create(
            tenant=tenant, code="BA-4", name="P", client=c, billing_address=a1
        )
        resp = admin_client.patch(
            f"/api/v1/projects/{project.pk}/",
            {"client": other.pk},
            format="json",
        )
        assert resp.status_code == 200, resp.data
        project.refresh_from_db()
        assert project.client_id == other.pk
        assert project.billing_address_id is None  # plus valable → purgée

    def test_detail_exposes_billing_address_label(
        self, admin_client, tenant, client_with_addresses
    ):
        c, a1, _a2 = client_with_addresses
        project = Project.objects.create(
            tenant=tenant, code="BA-5", name="P", client=c, billing_address=a1
        )
        resp = admin_client.get(f"/api/v1/projects/{project.pk}/")
        data = resp.json().get("data", resp.json())
        assert data["billing_address"] == a1.pk
        assert "Notre-Dame" in data["billing_address_label"]
