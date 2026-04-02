"""Sprint V8 — Suppliers/ST integration tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.projects.models import Project
from apps.suppliers.models import ExternalOrganization, STInvoice

User = get_user_model()


class BaseV8Test(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test V8", slug="test-v8")
        self.pm = User.objects.create_user(username="v8pm", password="x")
        self.employee = User.objects.create_user(username="v8emp", password="x")
        self.finance = User.objects.create_user(username="v8fin", password="x")
        for u in [self.pm, self.employee, self.finance]:
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        ProjectRole.objects.create(user=self.employee, tenant=self.tenant, role=Role.EMPLOYEE)
        ProjectRole.objects.create(user=self.finance, tenant=self.tenant, role=Role.FINANCE)
        self.client_obj = Client.objects.create(
            tenant=self.tenant, name="V8 Client", status="active",
        )
        self.project = Project.objects.create(
            tenant=self.tenant, code="V8-001", name="V8 Project",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
        )


class TestExternalOrganization(BaseV8Test):
    """External organization registry CRUD + duplicate check."""

    def test_create_organization(self):
        """Create a new external organization (supplier)."""
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.post("/api/v1/external_organizations/", {
            "name": "Sous-traitant ABC",
            "neq": "1234567890",
            "city": "Montreal",
            "province": "Quebec",
            "contact_name": "Jean Dupont",
            "contact_email": "jean@abc.ca",
            "type_tags": ["st"],
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])
        data = resp.json()
        self.assertEqual(data["name"], "Sous-traitant ABC")
        self.assertEqual(data["neq"], "1234567890")

    def test_list_organizations(self):
        """List all external organizations for the tenant."""
        ExternalOrganization.objects.create(
            tenant=self.tenant, name="Fournisseur X", neq="1111111111",
        )
        ExternalOrganization.objects.create(
            tenant=self.tenant, name="Fournisseur Y", neq="2222222222",
        )
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.get("/api/v1/external_organizations/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        self.assertGreaterEqual(len(results), 2)

    def test_check_duplicate(self):
        """Duplicate check returns matches by NEQ and name similarity."""
        ExternalOrganization.objects.create(
            tenant=self.tenant, name="Acme Solutions", neq="9999999999",
        )
        c = APIClient()
        c.force_authenticate(user=self.pm)
        # Check by NEQ exact match
        resp = c.post("/api/v1/external_organizations/check_duplicate/", {
            "name": "",
            "neq": "9999999999",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertGreaterEqual(len(data["duplicates"]), 1)
        self.assertEqual(data["duplicates"][0]["match_type"], "neq_exact")

    def test_update_organization(self):
        """Update an existing external organization."""
        org = ExternalOrganization.objects.create(
            tenant=self.tenant, name="Old Name", neq="5555555555",
        )
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.patch(f"/api/v1/external_organizations/{org.id}/", {
            "name": "New Name",
            "contact_email": "new@org.ca",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        org.refresh_from_db()
        self.assertEqual(org.name, "New Name")
        self.assertEqual(org.contact_email, "new@org.ca")


class TestSTInvoice(BaseV8Test):
    """Subcontractor invoice CRUD + workflow (authorize, mark_paid)."""

    def setUp(self):
        super().setUp()
        self.supplier = ExternalOrganization.objects.create(
            tenant=self.tenant, name="ST Partner", neq="7777777777",
            type_tags=["st"],
        )

    def test_create_st_invoice(self):
        """Create a new subcontractor invoice."""
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.post("/api/v1/st_invoices/", {
            "project": self.project.id,
            "supplier": self.supplier.id,
            "invoice_number": "ST-2026-001",
            "invoice_date": "2026-03-15",
            "amount": "12500.00",
            "source": "manual",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])
        data = resp.json()
        self.assertEqual(data["status"], "received")
        self.assertEqual(data["invoice_number"], "ST-2026-001")

    def test_authorize_st_invoice(self):
        """PM authorizes a received ST invoice."""
        invoice = STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.supplier,
            invoice_number="ST-2026-002", invoice_date="2026-03-16",
            amount=8000, status="received",
        )
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.post(f"/api/v1/st_invoices/{invoice.id}/authorize/")
        self.assertEqual(resp.status_code, 200)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "authorized")

    def test_mark_paid_st_invoice(self):
        """Finance marks an authorized ST invoice as paid."""
        invoice = STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.supplier,
            invoice_number="ST-2026-003", invoice_date="2026-03-17",
            amount=5000, status="authorized",
        )
        c = APIClient()
        c.force_authenticate(user=self.finance)
        resp = c.post(f"/api/v1/st_invoices/{invoice.id}/mark_paid/")
        self.assertEqual(resp.status_code, 200)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "paid")

    def test_list_st_invoices(self):
        """List all ST invoices, optionally filtered by status."""
        STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.supplier,
            invoice_number="ST-2026-010", invoice_date="2026-03-10",
            amount=3000, status="received",
        )
        STInvoice.objects.create(
            tenant=self.tenant, project=self.project, supplier=self.supplier,
            invoice_number="ST-2026-011", invoice_date="2026-03-11",
            amount=4000, status="authorized",
        )
        c = APIClient()
        c.force_authenticate(user=self.pm)
        # List all
        resp = c.get("/api/v1/st_invoices/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        self.assertGreaterEqual(len(results), 2)
        # Filter by status
        resp2 = c.get("/api/v1/st_invoices/?status=received")
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        results2 = data2.get("results", data2) if isinstance(data2, dict) else data2
        for item in results2:
            self.assertEqual(item["status"], "received")
