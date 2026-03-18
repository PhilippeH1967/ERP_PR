"""Tests for expense models."""

from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth.models import User

from apps.core.models import Tenant
from apps.expenses.models import ExpenseCategory, ExpenseLine, ExpenseReport


@pytest.mark.django_db
class TestExpenseReport:
    def test_create_report(self):
        tenant = Tenant.objects.create(name="T", slug="t-expense")
        user = User.objects.create_user(username="exp_user", password="pass123!")
        report = ExpenseReport.objects.create(
            tenant=tenant, employee=user, total_amount=Decimal("500.00"),
        )
        assert report.pk is not None
        assert report.status == "SUBMITTED"

    def test_expense_lines(self):
        tenant = Tenant.objects.create(name="T", slug="t-exp-line")
        user = User.objects.create_user(username="el_user", password="pass123!")
        cat = ExpenseCategory.objects.create(
            tenant=tenant, name="Transport", requires_receipt=True,
        )
        report = ExpenseReport.objects.create(tenant=tenant, employee=user)
        line = ExpenseLine.objects.create(
            tenant=tenant, report=report, category=cat,
            expense_date=date(2026, 3, 15), amount=Decimal("75.50"),
            description="Taxi",
        )
        assert line.pk is not None
        assert report.lines.count() == 1
