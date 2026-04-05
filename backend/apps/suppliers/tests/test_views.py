"""Tests for ExternalOrganization and ST Invoice API."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Project
from apps.suppliers.models import ExternalOrganization, STHoldback, STInvoice


@pytest.mark.django_db
class TestExternalOrganizationAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API Test", slug="ext-org-api")
        self.user = User.objects.create_user(username="ext_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_organizations(self):
        response = self.api.get("/api/v1/external_organizations/")
        assert response.status_code == 200

    def test_create_organization(self):
        response = self.api.post(
            "/api/v1/external_organizations/",
            {"name": "WSP", "neq": "1234567890", "type_tags": ["st"]},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_search_organizations(self):
        ExternalOrganization.objects.create(
            tenant=self.tenant, name="SNC Lavalin", neq="111"
        )
        response = self.api.get("/api/v1/external_organizations/?search=SNC")
        assert response.status_code == 200


@pytest.mark.django_db
class TestSTInvoiceWorkflow:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="ST", slug="st-wf-test")
        self.user = User.objects.create_user(username="st_wf_user", password="pass123!")
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.FINANCE)
        self.project = Project.objects.create(tenant=self.tenant, code="ST-P1", name="ST Project")
        self.org = ExternalOrganization.objects.create(tenant=self.tenant, name="BPA Structures")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_authorize_invoice(self):
        inv = STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.org,
            invoice_number="ST-002", invoice_date="2026-04-01",
            amount=10000, status="received",
        )
        resp = self.api.post(f"/api/v1/st_invoices/{inv.pk}/authorize/")
        assert resp.status_code == 200
        inv.refresh_from_db()
        assert inv.status == "authorized"

    def test_batch_authorize(self):
        inv1 = STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.org,
            invoice_number="ST-B1", invoice_date="2026-04-01", amount=5000, status="received",
        )
        inv2 = STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.org,
            invoice_number="ST-B2", invoice_date="2026-04-01", amount=7000, status="received",
        )
        resp = self.api.post("/api/v1/st_invoices/batch_authorize/", {
            "invoice_ids": [inv1.pk, inv2.pk],
        }, format="json")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["authorized_count"] == 2

    def test_dispute_invoice(self):
        inv = STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.org,
            invoice_number="ST-D1", invoice_date="2026-04-01", amount=8000, status="received",
        )
        resp = self.api.post(f"/api/v1/st_invoices/{inv.pk}/dispute/", {
            "reason": "Montant erroné",
        }, format="json")
        assert resp.status_code == 200
        inv.refresh_from_db()
        assert inv.status == "disputed"

    def test_holdback_release(self):
        holdback = STHoldback.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.org,
            percentage_rate=10, accumulated=2000, released=0, remaining=2000,
        )
        resp = self.api.post(f"/api/v1/st_holdbacks/{holdback.pk}/release/", {
            "amount": 1000,
        }, format="json")
        assert resp.status_code == 200
        holdback.refresh_from_db()
        assert float(holdback.released) == 1000

    def test_summary_by_supplier(self):
        STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.org,
            invoice_number="ST-S1", invoice_date="2026-04-01", amount=5000, status="received",
        )
        resp = self.api.get("/api/v1/st_invoices/summary_by_supplier/")
        assert resp.status_code == 200
