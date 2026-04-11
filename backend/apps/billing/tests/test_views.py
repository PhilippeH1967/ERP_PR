"""Tests for billing API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.billing.models import Invoice
from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import Project


@pytest.mark.django_db
class TestInvoiceAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="API", slug="inv-api")
        self.client_obj = Client.objects.create(tenant=self.tenant, name="C")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PI", name="InvProject",
            client=self.client_obj,
        )
        self.user = User.objects.create_user(username="inv_user", password="pass123!")
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.FINANCE)
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_invoices(self):
        response = self.api.get("/api/v1/invoices/")
        assert response.status_code == 200

    def test_create_invoice(self):
        response = self.api.post(
            "/api/v1/invoices/",
            {
                "project": self.project.pk,
                "client": self.client_obj.pk,
                "invoice_number": "PROV-0001",
                "total_amount": "50000.00",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_submit_invoice(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client_obj,
            invoice_number="PROV-S",
        )
        response = self.api.post(f"/api/v1/invoices/{inv.pk}/submit/")
        assert response.status_code == 200
        data = response.json()
        payload = data.get("data", data)
        assert payload["status"] == "SUBMITTED"

    def test_approve_invoice(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client_obj,
            invoice_number="PROV-A", status="SUBMITTED",
        )
        response = self.api.post(f"/api/v1/invoices/{inv.pk}/approve/")
        assert response.status_code == 200

    def test_self_approval_blocked(self):
        """FAC-008: User who submitted an invoice cannot approve it (anti-self-approval)."""
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client_obj,
            invoice_number="PROV-SELF", status="SUBMITTED",
            submitted_by=self.user,
        )
        response = self.api.post(f"/api/v1/invoices/{inv.pk}/approve/")
        assert response.status_code == 403
        data = response.json()
        assert data["error"]["code"] == "SELF_APPROVAL"

    def test_approval_by_other_user_succeeds(self):
        """FAC-008: An invoice submitted by user A can be approved by user B."""
        # User A submits
        user_a = User.objects.create_user(username="finance_a", password="pass123!")
        ProjectRole.objects.create(user=user_a, tenant=self.tenant, role=Role.FINANCE)
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client_obj,
            invoice_number="PROV-OTHER", status="SUBMITTED",
            submitted_by=user_a,
        )
        # User B (self.user) approves
        response = self.api.post(f"/api/v1/invoices/{inv.pk}/approve/")
        assert response.status_code == 200
        inv.refresh_from_db()
        assert inv.status == "APPROVED"
        assert inv.approved_by == self.user

    def test_aging_analysis(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client_obj,
            invoice_number="PROV-AG",
        )
        response = self.api.get(f"/api/v1/invoices/{inv.pk}/aging_analysis/")
        assert response.status_code == 200

    def test_search_invoices(self):
        Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client_obj,
            invoice_number="PROV-SEARCH",
        )
        response = self.api.get("/api/v1/invoices/?search=SEARCH")
        assert response.status_code == 200
