"""Tests for invoice modes MERGED / AMENDMENT_DEDICATED (story 12.1 Phase D).

Covers:
- Invoice.invoice_mode field: MERGED (default) vs AMENDMENT_DEDICATED
- Invoice.amendment FK (nullable) linking a dedicated invoice to its avenant
- InvoiceLine.amendment FK (nullable) tagging lines per avenant
- Serializer validation matrix:
    * MERGED invoice must have amendment = None
    * AMENDMENT_DEDICATED invoice must have amendment set
    * AMENDMENT_DEDICATED lines must all belong to the invoice's amendment
    * MERGED invoice may mix main and avenant lines
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from rest_framework.exceptions import ValidationError

from apps.billing.models import Invoice, InvoiceLine, InvoiceMode
from apps.billing.serializers import InvoiceSerializer
from apps.clients.models import Client
from apps.core.models import Tenant
from apps.projects.models import Amendment, Phase, Project, Task

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


@pytest.fixture
def billing_setup(db):
    tenant = Tenant.objects.create(name="T", slug="t-phase-d")
    client = Client.objects.create(tenant=tenant, name="Client D")
    project = Project.objects.create(
        tenant=tenant,
        code="PD",
        name="Phase D project",
        client=client,
    )
    phase = Phase.objects.create(
        tenant=tenant,
        project=project,
        code="1",
        name="Main Phase",
        order=0,
    )
    amendment = Amendment.objects.create(
        tenant=tenant,
        project=project,
        amendment_number=1,
        description="Avenant Phase D",
        budget_impact=Decimal("25000"),
        status=Amendment.AmendmentStatus.APPROVED,
    )
    main_task = Task.objects.create(
        tenant=tenant,
        project=project,
        phase=phase,
        wbs_code="1.1",
        name="Main task",
    )
    amendment_phase = Phase.objects.create(
        tenant=tenant,
        project=project,
        amendment=amendment,
        code="AV1",
        name="Avenant Phase",
        order=0,
    )
    amendment_task = Task.objects.create(
        tenant=tenant,
        project=project,
        phase=amendment_phase,
        amendment=amendment,
        wbs_code="AV1.1",
        name="Amendment task",
    )
    return {
        "tenant": tenant,
        "client": client,
        "project": project,
        "phase": phase,
        "amendment": amendment,
        "main_task": main_task,
        "amendment_phase": amendment_phase,
        "amendment_task": amendment_task,
    }


# --------------------------------------------------------------------------- #
# Model-level tests
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestInvoiceMode:
    def test_invoice_mode_defaults_to_merged(self, billing_setup):
        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-001",
        )
        assert inv.invoice_mode == InvoiceMode.MERGED
        assert inv.amendment_id is None

    def test_invoice_can_be_dedicated_to_amendment(self, billing_setup):
        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-002",
            invoice_mode=InvoiceMode.AMENDMENT_DEDICATED,
            amendment=s["amendment"],
        )
        assert inv.invoice_mode == InvoiceMode.AMENDMENT_DEDICATED
        assert inv.amendment_id == s["amendment"].pk

    def test_invoice_line_amendment_is_nullable(self, billing_setup):
        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-003",
        )
        line = InvoiceLine.objects.create(
            tenant=s["tenant"],
            invoice=inv,
            task=s["main_task"],
            deliverable_name="Ligne principale",
            amount_to_bill=Decimal("1000"),
        )
        assert line.amendment_id is None

    def test_invoice_line_can_reference_amendment(self, billing_setup):
        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-004",
        )
        line = InvoiceLine.objects.create(
            tenant=s["tenant"],
            invoice=inv,
            task=s["amendment_task"],
            amendment=s["amendment"],
            deliverable_name="Ligne avenant",
            amount_to_bill=Decimal("2000"),
        )
        assert line.amendment_id == s["amendment"].pk

    def test_reverse_accessor_amendment_invoices(self, billing_setup):
        s = billing_setup
        Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-005",
            invoice_mode=InvoiceMode.AMENDMENT_DEDICATED,
            amendment=s["amendment"],
        )
        assert s["amendment"].invoices.count() == 1


# --------------------------------------------------------------------------- #
# Serializer validation
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestInvoiceModeValidation:
    def test_merged_invoice_must_not_set_amendment(self, billing_setup):
        s = billing_setup
        serializer = InvoiceSerializer(
            data={
                "project": s["project"].pk,
                "client": s["client"].pk,
                "invoice_number": "PROV-D-MERGED-BAD",
                "invoice_mode": InvoiceMode.MERGED,
                "amendment": s["amendment"].pk,
            }
        )
        assert not serializer.is_valid()
        assert "amendment" in serializer.errors or "invoice_mode" in serializer.errors

    def test_dedicated_invoice_requires_amendment(self, billing_setup):
        s = billing_setup
        serializer = InvoiceSerializer(
            data={
                "project": s["project"].pk,
                "client": s["client"].pk,
                "invoice_number": "PROV-D-DED-BAD",
                "invoice_mode": InvoiceMode.AMENDMENT_DEDICATED,
            }
        )
        assert not serializer.is_valid()
        assert "amendment" in serializer.errors or "invoice_mode" in serializer.errors

    def test_merged_invoice_without_amendment_is_valid(self, billing_setup):
        s = billing_setup
        serializer = InvoiceSerializer(
            data={
                "project": s["project"].pk,
                "client": s["client"].pk,
                "invoice_number": "PROV-D-MERGED-OK",
                "invoice_mode": InvoiceMode.MERGED,
            }
        )
        assert serializer.is_valid(), serializer.errors

    def test_dedicated_invoice_with_amendment_is_valid(self, billing_setup):
        s = billing_setup
        serializer = InvoiceSerializer(
            data={
                "project": s["project"].pk,
                "client": s["client"].pk,
                "invoice_number": "PROV-D-DED-OK",
                "invoice_mode": InvoiceMode.AMENDMENT_DEDICATED,
                "amendment": s["amendment"].pk,
            }
        )
        assert serializer.is_valid(), serializer.errors


# --------------------------------------------------------------------------- #
# Line / invoice consistency at save time
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestInvoiceLineConsistency:
    def test_dedicated_invoice_rejects_main_project_line(self, billing_setup):
        """A line without ``amendment`` cannot live on a dedicated invoice."""
        from apps.billing.services import assert_line_belongs_to_invoice

        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-DED-C1",
            invoice_mode=InvoiceMode.AMENDMENT_DEDICATED,
            amendment=s["amendment"],
        )
        with pytest.raises(ValidationError):
            assert_line_belongs_to_invoice(inv, task=s["main_task"], amendment=None)

    def test_dedicated_invoice_rejects_other_amendment_line(self, billing_setup):
        from apps.billing.services import assert_line_belongs_to_invoice

        s = billing_setup
        other_amd = Amendment.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            amendment_number=2,
            description="Avenant autre",
            status=Amendment.AmendmentStatus.APPROVED,
        )
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-DED-C2",
            invoice_mode=InvoiceMode.AMENDMENT_DEDICATED,
            amendment=s["amendment"],
        )
        with pytest.raises(ValidationError):
            assert_line_belongs_to_invoice(inv, task=s["amendment_task"], amendment=other_amd)

    def test_dedicated_invoice_accepts_matching_amendment_line(self, billing_setup):
        from apps.billing.services import assert_line_belongs_to_invoice

        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-DED-C3",
            invoice_mode=InvoiceMode.AMENDMENT_DEDICATED,
            amendment=s["amendment"],
        )
        assert_line_belongs_to_invoice(inv, task=s["amendment_task"], amendment=s["amendment"])

    def test_merged_invoice_accepts_both_main_and_amendment_lines(self, billing_setup):
        from apps.billing.services import assert_line_belongs_to_invoice

        s = billing_setup
        inv = Invoice.objects.create(
            tenant=s["tenant"],
            project=s["project"],
            client=s["client"],
            invoice_number="PROV-D-MERGED-C",
            invoice_mode=InvoiceMode.MERGED,
        )
        assert_line_belongs_to_invoice(inv, task=s["main_task"], amendment=None)
        assert_line_belongs_to_invoice(inv, task=s["amendment_task"], amendment=s["amendment"])
