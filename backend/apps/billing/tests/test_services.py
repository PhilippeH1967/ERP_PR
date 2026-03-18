"""Tests for billing business logic services."""

from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.auth.models import User

from apps.billing.models import Invoice, Payment
from apps.billing.services import (
    calculate_ca_salary_ratio,
    get_aging_analysis,
    get_client_financial_summary,
)
from apps.clients.models import Client
from apps.core.models import Tenant
from apps.projects.models import Project
from apps.time_entries.models import TimeEntry


@pytest.mark.django_db
class TestClientFinancialSummary:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-fin-svc")
        self.client = Client.objects.create(tenant=self.tenant, name="C")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PF", name="P", client=self.client,
        )

    def test_empty_summary(self):
        result = get_client_financial_summary(self.client.pk, self.tenant.pk)
        assert result["total_ca"] == "0"
        assert result["invoices_outstanding"] == "0"

    def test_with_invoices_and_payments(self):
        inv = Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="INV-1", total_amount=Decimal("50000"),
        )
        Payment.objects.create(
            tenant=self.tenant, invoice=inv,
            amount=Decimal("20000"), payment_date=date.today(),
        )
        result = get_client_financial_summary(self.client.pk, self.tenant.pk)
        assert Decimal(result["total_ca"]) == Decimal("50000")
        assert Decimal(result["invoices_outstanding"]) == Decimal("30000")


@pytest.mark.django_db
class TestAgingAnalysis:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="t-aging")
        self.client = Client.objects.create(tenant=self.tenant, name="C")
        self.project = Project.objects.create(
            tenant=self.tenant, code="PA", name="P", client=self.client,
        )

    def test_empty_aging(self):
        result = get_aging_analysis(self.client.pk, self.tenant.pk)
        assert result["0_30"] == "0"
        assert result["90_plus"] == "0"

    def test_aging_buckets(self):
        today = date.today()
        # 15 days old
        Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="A1", total_amount=Decimal("10000"),
            status="SENT", date_sent=today - timedelta(days=15),
        )
        # 45 days old
        Invoice.objects.create(
            tenant=self.tenant, project=self.project, client=self.client,
            invoice_number="A2", total_amount=Decimal("20000"),
            status="SENT", date_sent=today - timedelta(days=45),
        )
        result = get_aging_analysis(self.client.pk, self.tenant.pk)
        assert Decimal(result["0_30"]) == Decimal("10000")
        assert Decimal(result["31_60"]) == Decimal("20000")


@pytest.mark.django_db
class TestCASalaryRatio:
    def test_ratio_calculation(self):
        tenant = Tenant.objects.create(name="T", slug="t-ratio")
        client = Client.objects.create(tenant=tenant, name="C")
        project = Project.objects.create(
            tenant=tenant, code="PR", name="P", client=client,
        )
        user = User.objects.create_user(username="ratio_user", password="pass123!")
        Invoice.objects.create(
            tenant=tenant, project=project, client=client,
            invoice_number="R1", total_amount=Decimal("100000"),
        )
        TimeEntry.objects.create(
            tenant=tenant, employee=user, project=project,
            date=date.today(), hours=Decimal("100"),
        )
        result = calculate_ca_salary_ratio(project.pk, tenant.pk)
        assert Decimal(result["hours_consumed"]) == Decimal("100")
        assert Decimal(result["invoiced"]) == Decimal("100000")
        # ratio = 100000 / (100 * 85) * 100 = 1176.47%
        assert Decimal(result["ratio_percent"]) > 0
