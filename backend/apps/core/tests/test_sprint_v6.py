"""Sprint V6 — Billing module integration tests."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.billing.models import CreditNote, Invoice, InvoiceLine, Payment
from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.projects.models import Phase, Project

User = get_user_model()


class BaseV6Test(TestCase):
    """Shared setUp for all billing tests."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Billing Test", slug="billing-v6")

        # Users
        self.admin = User.objects.create_user(username="v6admin", password="x")
        self.finance = User.objects.create_user(username="v6finance", password="x")
        self.finance2 = User.objects.create_user(username="v6finance2", password="x")
        self.pm = User.objects.create_user(username="v6pm", password="x")
        self.employee = User.objects.create_user(username="v6emp", password="x")
        self.director = User.objects.create_user(username="v6director", password="x")

        for u in [self.admin, self.finance, self.finance2, self.pm, self.employee, self.director]:
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)

        # Roles
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        ProjectRole.objects.create(user=self.finance, tenant=self.tenant, role=Role.FINANCE)
        ProjectRole.objects.create(user=self.finance2, tenant=self.tenant, role=Role.FINANCE)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        ProjectRole.objects.create(user=self.employee, tenant=self.tenant, role=Role.EMPLOYEE)
        ProjectRole.objects.create(user=self.director, tenant=self.tenant, role=Role.PROJECT_DIRECTOR)

        # Client and project
        self.client_obj = Client.objects.create(
            tenant=self.tenant, name="V6 Client Corp", status="active",
        )
        self.project = Project.objects.create(
            tenant=self.tenant, code="V6-001", name="V6 Project Alpha",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
        )

        # Phases with budgeted_cost > 0
        self.phase1 = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept",
            phase_type="REALIZATION", billing_mode="FORFAIT",
            budgeted_cost=Decimal("50000"), order=1,
        )
        self.phase2 = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Plans",
            phase_type="REALIZATION", billing_mode="FORFAIT",
            budgeted_cost=Decimal("30000"), order=2,
        )

    def _api(self, user):
        """Return an APIClient authenticated as user."""
        c = APIClient()
        c.force_authenticate(user=user)
        return c

    def _create_draft_invoice(self, **overrides):
        """Helper to create a DRAFT invoice directly in the DB."""
        defaults = dict(
            tenant=self.tenant,
            project=self.project,
            client=self.client_obj,
            invoice_number="PROV-999999",
            status="DRAFT",
            total_amount=Decimal("10000"),
        )
        defaults.update(overrides)
        return Invoice.objects.create(**defaults)

    def _advance_to_submitted(self, invoice, submitted_by=None):
        """Move invoice to SUBMITTED state."""
        invoice.status = "SUBMITTED"
        invoice.submitted_by = submitted_by or self.finance
        invoice.invoice_number = f"FAC-{timezone.now().year}-00001"
        invoice.save()

    def _advance_to_approved(self, invoice, submitted_by=None, approved_by=None):
        """Move invoice to APPROVED state."""
        self._advance_to_submitted(invoice, submitted_by=submitted_by or self.finance)
        invoice.status = "APPROVED"
        invoice.approved_by = approved_by or self.finance2
        invoice.save()

    def _advance_to_sent(self, invoice):
        """Move invoice to SENT state."""
        self._advance_to_approved(invoice)
        invoice.status = "SENT"
        invoice.date_sent = timezone.now().date()
        invoice.save()


# ---------------------------------------------------------------------------
# TestInvoiceLifecycle (10 tests)
# ---------------------------------------------------------------------------
class TestInvoiceLifecycle(BaseV6Test):

    def test_create_invoice_from_project(self):
        """create_from_project creates invoice with pre-populated lines from phases."""
        c = self._api(self.finance)
        resp = c.post("/api/v1/invoices/create_from_project/", {
            "project_id": self.project.id,
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())
        data = resp.json()
        self.assertTrue(data["invoice_number"].startswith("PROV-"))
        self.assertEqual(data["status"], "DRAFT")
        # Should have at least 2 lines (one per phase with budgeted_cost > 0)
        self.assertGreaterEqual(len(data["lines"]), 2)
        names = [l["deliverable_name"] for l in data["lines"]]
        self.assertIn("Concept", names)
        self.assertIn("Plans", names)

    def test_create_free_invoice(self):
        """Direct POST creates a free invoice (no project required)."""
        c = self._api(self.finance)
        resp = c.post("/api/v1/invoices/", {
            "client": self.client_obj.id,
            "invoice_number": "PROV-FREE01",
            "status": "DRAFT",
            "total_amount": "5000.00",
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())
        data = resp.json()
        self.assertIsNone(data.get("project"))
        self.assertEqual(data["invoice_number"], "PROV-FREE01")

    def test_submit_invoice_assigns_definitive_number(self):
        """Submitting a PROV invoice assigns a FAC-YYYY-XXXXX number."""
        invoice = self._create_draft_invoice()
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/submit/")
        self.assertEqual(resp.status_code, 200, resp.json())
        data = resp.json()
        self.assertTrue(data["invoice_number"].startswith("FAC-"))
        self.assertEqual(data["status"], "SUBMITTED")
        year = str(timezone.now().year)
        self.assertIn(year, data["invoice_number"])

    def test_approve_invoice(self):
        """SUBMITTED invoice can be approved by a different user."""
        invoice = self._create_draft_invoice()
        self._advance_to_submitted(invoice, submitted_by=self.finance)
        c = self._api(self.finance2)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/approve/")
        self.assertEqual(resp.status_code, 200, resp.json())
        self.assertEqual(resp.json()["status"], "APPROVED")

    def test_approve_self_blocked(self):
        """submitted_by cannot approve their own invoice (anti-self-approval)."""
        invoice = self._create_draft_invoice()
        self._advance_to_submitted(invoice, submitted_by=self.finance)
        c = self._api(self.finance)  # same user who submitted
        resp = c.post(f"/api/v1/invoices/{invoice.id}/approve/")
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.json()["error"]["code"], "SELF_APPROVAL")

    def test_send_invoice(self):
        """APPROVED invoice can be sent, sets date_sent."""
        invoice = self._create_draft_invoice()
        self._advance_to_approved(invoice)
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/send/")
        self.assertEqual(resp.status_code, 200, resp.json())
        data = resp.json()
        self.assertEqual(data["status"], "SENT")
        self.assertIsNotNone(data["date_sent"])

    def test_send_without_approve_fails(self):
        """Cannot send a DRAFT invoice directly (must be APPROVED)."""
        invoice = self._create_draft_invoice()
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/send/")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"]["code"], "INVALID_STATUS")

    def test_mark_paid(self):
        """SENT invoice can be marked as paid, sets date_paid."""
        invoice = self._create_draft_invoice()
        self._advance_to_sent(invoice)
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/mark_paid/")
        self.assertEqual(resp.status_code, 200, resp.json())
        data = resp.json()
        self.assertEqual(data["status"], "PAID")
        self.assertIsNotNone(data["date_paid"])

    def test_mark_paid_without_send_fails(self):
        """Cannot mark APPROVED (unsent) invoice as paid."""
        invoice = self._create_draft_invoice()
        self._advance_to_approved(invoice)
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/mark_paid/")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"]["code"], "INVALID_STATUS")

    def test_delete_draft_allowed(self):
        """DRAFT invoice can be deleted."""
        invoice = self._create_draft_invoice()
        c = self._api(self.finance)
        resp = c.delete(f"/api/v1/invoices/{invoice.id}/")
        self.assertIn(resp.status_code, [200, 204])
        self.assertFalse(Invoice.objects.filter(pk=invoice.pk).exists())


# ---------------------------------------------------------------------------
# TestInvoicePermissions (5 tests)
# ---------------------------------------------------------------------------
class TestInvoicePermissions(BaseV6Test):

    def test_employee_cannot_view_invoices(self):
        """EMPLOYEE role gets 403 on invoice list."""
        c = self._api(self.employee)
        resp = c.get("/api/v1/invoices/")
        self.assertEqual(resp.status_code, 403)

    def test_pm_can_view_but_not_create(self):
        """PM can GET invoices but cannot POST (create)."""
        self._create_draft_invoice()
        c = self._api(self.pm)
        resp_get = c.get("/api/v1/invoices/")
        self.assertEqual(resp_get.status_code, 200)

        resp_post = c.post("/api/v1/invoices/", {
            "client": self.client_obj.id,
            "invoice_number": "PROV-PM001",
            "status": "DRAFT",
        }, format="json")
        self.assertEqual(resp_post.status_code, 403)

    def test_finance_can_create(self):
        """FINANCE role can create invoices (POST 201)."""
        c = self._api(self.finance)
        resp = c.post("/api/v1/invoices/", {
            "client": self.client_obj.id,
            "invoice_number": "PROV-FIN001",
            "status": "DRAFT",
            "total_amount": "1000.00",
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())

    def test_employee_cannot_submit(self):
        """EMPLOYEE cannot submit an invoice."""
        invoice = self._create_draft_invoice()
        c = self._api(self.employee)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/submit/")
        self.assertEqual(resp.status_code, 403)

    def test_pm_can_submit(self):
        """PM can submit an invoice (PM is in BILLING_SUBMIT_ROLES)."""
        invoice = self._create_draft_invoice()
        c = self._api(self.pm)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/submit/")
        self.assertEqual(resp.status_code, 200, resp.json())
        self.assertEqual(resp.json()["status"], "SUBMITTED")


# ---------------------------------------------------------------------------
# TestInvoiceLines (5 tests)
# ---------------------------------------------------------------------------
class TestInvoiceLines(BaseV6Test):

    def setUp(self):
        super().setUp()
        self.invoice = self._create_draft_invoice(total_amount=Decimal("0"))

    def test_create_line(self):
        """POST creates a new invoice line."""
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{self.invoice.id}/lines/", {
            "deliverable_name": "Esquisse",
            "line_type": "FORFAIT",
            "total_contract_amount": "20000.00",
            "invoiced_to_date": "5000.00",
            "amount_to_bill": "5000.00",
            "order": 1,
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())
        self.assertEqual(resp.json()["deliverable_name"], "Esquisse")

    def test_update_amount_to_bill(self):
        """PATCH updates amount_to_bill on an existing line."""
        line = InvoiceLine.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            deliverable_name="Phase A", line_type="FORFAIT",
            total_contract_amount=Decimal("10000"),
            invoiced_to_date=Decimal("0"),
            amount_to_bill=Decimal("3000"), order=1,
        )
        c = self._api(self.finance)
        resp = c.patch(f"/api/v1/invoices/{self.invoice.id}/lines/{line.id}/", {
            "amount_to_bill": "4500.00",
        }, format="json")
        self.assertEqual(resp.status_code, 200, resp.json())
        line.refresh_from_db()
        self.assertEqual(line.amount_to_bill, Decimal("4500.00"))

    def test_budget_exceeded_requires_confirmation(self):
        """amount_to_bill exceeding remaining budget returns 400 without force_override."""
        line = InvoiceLine.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            deliverable_name="Phase B", line_type="FORFAIT",
            total_contract_amount=Decimal("10000"),
            invoiced_to_date=Decimal("8000"),
            amount_to_bill=Decimal("1000"), order=1,
        )
        c = self._api(self.finance)
        resp = c.patch(f"/api/v1/invoices/{self.invoice.id}/lines/{line.id}/", {
            "amount_to_bill": "5000.00",  # remaining is only 2000
        }, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_budget_exceeded_with_force_override(self):
        """amount_to_bill exceeding budget succeeds with force_override=true."""
        line = InvoiceLine.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            deliverable_name="Phase C", line_type="FORFAIT",
            total_contract_amount=Decimal("10000"),
            invoiced_to_date=Decimal("8000"),
            amount_to_bill=Decimal("1000"), order=1,
        )
        c = self._api(self.finance)
        resp = c.patch(f"/api/v1/invoices/{self.invoice.id}/lines/{line.id}/", {
            "amount_to_bill": "5000.00",
            "force_override": True,
        }, format="json")
        self.assertEqual(resp.status_code, 200, resp.json())
        line.refresh_from_db()
        self.assertEqual(line.amount_to_bill, Decimal("5000.00"))

    def test_delete_line_recalculates_totals(self):
        """Deleting a line recalculates invoice totals."""
        line1 = InvoiceLine.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            deliverable_name="Line 1", line_type="FORFAIT",
            total_contract_amount=Decimal("10000"),
            amount_to_bill=Decimal("3000"), order=1,
        )
        InvoiceLine.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            deliverable_name="Line 2", line_type="FORFAIT",
            total_contract_amount=Decimal("5000"),
            amount_to_bill=Decimal("2000"), order=2,
        )
        # Recalculate to set initial totals
        from django.db.models import Sum
        total = self.invoice.lines.aggregate(t=Sum("amount_to_bill"))["t"] or Decimal("0")
        Invoice.objects.filter(pk=self.invoice.pk).update(total_amount=total)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.total_amount, Decimal("5000"))

        # Delete line 1
        c = self._api(self.finance)
        resp = c.delete(f"/api/v1/invoices/{self.invoice.id}/lines/{line1.id}/")
        self.assertIn(resp.status_code, [200, 204])

        # Invoice total should now be 2000 (only line 2 remains)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.total_amount, Decimal("2000"))


# ---------------------------------------------------------------------------
# TestInvoicedHours (3 tests)
# ---------------------------------------------------------------------------
class TestInvoicedHours(BaseV6Test):

    def setUp(self):
        super().setUp()
        from apps.time_entries.models import TimeEntry

        # Phase with HORAIRE billing mode for time entry tracking
        self.horaire_phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Surveillance",
            phase_type="REALIZATION", billing_mode="HORAIRE",
            budgeted_cost=Decimal("20000"), order=3,
        )
        # Create approved, uninvoiced time entries
        self.entry1 = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.horaire_phase, date="2026-03-16", hours=8,
            status="PM_APPROVED", is_invoiced=False,
        )
        self.entry2 = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.horaire_phase, date="2026-03-17", hours=7,
            status="PM_APPROVED", is_invoiced=False,
        )

    def test_mark_hours_invoiced_on_sent_invoice(self):
        """mark_hours_invoiced marks time entries as invoiced on a SENT invoice."""
        invoice = self._create_draft_invoice()
        InvoiceLine.objects.create(
            tenant=self.tenant, invoice=invoice,
            deliverable_name="Surveillance", line_type="HORAIRE",
            total_contract_amount=Decimal("20000"),
            amount_to_bill=Decimal("1275"), order=1,
        )
        self._advance_to_sent(invoice)

        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/mark_hours_invoiced/")
        self.assertEqual(resp.status_code, 200, resp.json())
        self.assertGreaterEqual(resp.json()["marked_count"], 1)

        self.entry1.refresh_from_db()
        self.assertTrue(self.entry1.is_invoiced)

    def test_mark_hours_not_on_draft(self):
        """mark_hours_invoiced fails on DRAFT invoice."""
        invoice = self._create_draft_invoice()
        InvoiceLine.objects.create(
            tenant=self.tenant, invoice=invoice,
            deliverable_name="Surveillance", line_type="HORAIRE",
            total_contract_amount=Decimal("20000"),
            amount_to_bill=Decimal("1275"), order=1,
        )
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/invoices/{invoice.id}/mark_hours_invoiced/")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["error"]["code"], "INVALID_STATUS")

    def test_uninvoiced_hours_only_in_new_invoice(self):
        """create_from_project only includes uninvoiced hours for HORAIRE lines."""
        from apps.time_entries.models import TimeEntry

        # Mark entry1 as already invoiced
        self.entry1.is_invoiced = True
        self.entry1.save()

        c = self._api(self.finance)
        resp = c.post("/api/v1/invoices/create_from_project/", {
            "project_id": self.project.id,
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())
        data = resp.json()

        # Find the HORAIRE line
        horaire_lines = [l for l in data["lines"] if l["line_type"] == "HORAIRE"]
        self.assertTrue(len(horaire_lines) > 0)
        horaire_line = horaire_lines[0]

        # amount_to_bill should be based only on entry2 (7h * 85 = 595)
        # entry1 is already invoiced and should be excluded
        self.assertEqual(
            Decimal(str(horaire_line["amount_to_bill"])),
            Decimal("595.00"),  # 7h * 85$/h
        )


# ---------------------------------------------------------------------------
# TestPaymentCRUD (3 tests)
# ---------------------------------------------------------------------------
class TestPaymentCRUD(BaseV6Test):

    def setUp(self):
        super().setUp()
        self.invoice = self._create_draft_invoice()
        self._advance_to_sent(self.invoice)

    def test_create_payment(self):
        """FINANCE can create a payment against an invoice."""
        c = self._api(self.finance)
        resp = c.post("/api/v1/payments/", {
            "invoice": self.invoice.id,
            "amount": "5000.00",
            "payment_date": "2026-04-01",
            "reference": "CHQ-12345",
            "method": "cheque",
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())
        self.assertEqual(Decimal(resp.json()["amount"]), Decimal("5000.00"))

    def test_list_payments(self):
        """FINANCE can list payments."""
        Payment.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            amount=Decimal("2500"), payment_date="2026-04-01",
            reference="VIR-001", method="virement",
        )
        c = self._api(self.finance)
        resp = c.get("/api/v1/payments/")
        self.assertEqual(resp.status_code, 200)
        results = resp.json().get("results", resp.json())
        self.assertGreaterEqual(len(results), 1)

    def test_employee_cannot_create_payment(self):
        """EMPLOYEE role gets 403 when creating a payment."""
        c = self._api(self.employee)
        resp = c.post("/api/v1/payments/", {
            "invoice": self.invoice.id,
            "amount": "1000.00",
            "payment_date": "2026-04-01",
        }, format="json")
        self.assertEqual(resp.status_code, 403)


# ---------------------------------------------------------------------------
# TestCreditNoteCRUD (2 tests)
# ---------------------------------------------------------------------------
class TestCreditNoteCRUD(BaseV6Test):

    def setUp(self):
        super().setUp()
        self.invoice = self._create_draft_invoice()

    def test_create_credit_note(self):
        """FINANCE can create a credit note."""
        c = self._api(self.finance)
        resp = c.post("/api/v1/credit_notes/", {
            "invoice": self.invoice.id,
            "project": self.project.id,
            "credit_note_number": "AV-2026-00001",
            "amount": "1500.00",
            "reason": "Erreur de facturation",
            "status": "DRAFT",
        }, format="json")
        self.assertEqual(resp.status_code, 201, resp.json())
        self.assertEqual(resp.json()["credit_note_number"], "AV-2026-00001")

    def test_delete_credit_note(self):
        """FINANCE can delete a credit note."""
        cn = CreditNote.objects.create(
            tenant=self.tenant, invoice=self.invoice, project=self.project,
            credit_note_number="AV-2026-00002", amount=Decimal("500"),
            reason="Test", status="DRAFT",
        )
        c = self._api(self.finance)
        resp = c.delete(f"/api/v1/credit_notes/{cn.id}/")
        self.assertIn(resp.status_code, [200, 204])
        self.assertFalse(CreditNote.objects.filter(pk=cn.pk).exists())
