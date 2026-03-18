"""Tests for billing models."""

from decimal import Decimal

import pytest

from apps.billing.models import (
    CreditNote,
    Holdback,
    Invoice,
    InvoiceLine,
    Payment,
    PaymentAllocation,
)
from apps.clients.models import Client
from apps.core.models import Tenant
from apps.projects.models import Project


@pytest.mark.django_db
class TestInvoice:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-billing")
        self.client = Client.objects.create(tenant=self.tenant, name="Client")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PB", name="BillingProject",
            client=self.client,
        )

    def test_create_invoice(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="PROV-0001", total_amount=Decimal("50000.00"),
        )
        assert inv.pk is not None
        assert inv.status == "DRAFT"
        assert inv.version == 1

    def test_invoice_history(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="PROV-H", total_amount=Decimal("10000"),
        )
        inv.status = "SUBMITTED"
        inv.save()
        assert inv.history.count() == 2

    def test_invoice_lines(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="PROV-L",
        )
        line = InvoiceLine.objects.create(
            tenant=self.tenant, invoice=inv,
            deliverable_name="Concept",
            total_contract_amount=Decimal("100000"),
            amount_to_bill=Decimal("25000"),
            pct_billing_advancement=Decimal("25.00"),
        )
        assert line.pk is not None
        assert inv.lines.count() == 1


@pytest.mark.django_db
class TestPaymentAndHoldback:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-pay")
        self.client = Client.objects.create(tenant=self.tenant, name="C")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PP", name="P", client=self.client,
        )
        self.invoice = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="INV-001", total_amount=Decimal("50000"),
        )

    def test_create_payment(self):
        p = Payment.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            amount=Decimal("25000"), payment_date="2026-03-15",
        )
        assert p.pk is not None

    def test_payment_allocation(self):
        p = Payment.objects.create(
            tenant=self.tenant, invoice=self.invoice,
            amount=Decimal("10000"), payment_date="2026-03-15",
        )
        alloc = PaymentAllocation.objects.create(
            tenant=self.tenant, payment=p, invoice=self.invoice,
            allocated_amount=Decimal("10000"),
        )
        assert alloc.pk is not None

    def test_holdback(self):
        h = Holdback.objects.create(
            tenant=self.tenant, project=self.project,
            percentage_rate=Decimal("5.00"),
            accumulated=Decimal("2500"),
            released=Decimal("0"),
            remaining=Decimal("2500"),
        )
        assert h.remaining == Decimal("2500")

    def test_credit_note(self):
        cn = CreditNote.objects.create(
            tenant=self.tenant, project=self.project, invoice=self.invoice,
            credit_note_number="NC-001", amount=Decimal("5000"),
            reason="Adjustment",
        )
        assert cn.status == "DRAFT"
