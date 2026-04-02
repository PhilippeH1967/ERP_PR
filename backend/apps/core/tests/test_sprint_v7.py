"""Sprint V7 — Expenses integration tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.expenses.models import ExpenseCategory, ExpenseLine, ExpenseReport
from apps.projects.models import Project

User = get_user_model()


class BaseV7Test(TestCase):
    def _api(self, user):
        """Return an APIClient authenticated as user with tenant header."""
        c = APIClient()
        c.force_authenticate(user=user)
        c.credentials(HTTP_X_TENANT_ID=str(self.tenant.id))
        return c

    def _d(self, resp):
        """Unwrap API response data envelope."""
        d = resp.data
        if isinstance(d, dict) and "data" in d and isinstance(d["data"], dict):
            return d["data"]
        return d

    def _list(self, resp):
        """Unwrap API list response envelope."""
        d = resp.data
        if isinstance(d, dict) and "data" in d:
            return d["data"]
        return d

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test V7", slug="test-v7")
        self.pm = User.objects.create_user(username="v7pm", password="x")
        self.employee = User.objects.create_user(username="v7emp", password="x")
        self.finance = User.objects.create_user(username="v7fin", password="x")
        for u in [self.pm, self.employee, self.finance]:
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        ProjectRole.objects.create(user=self.employee, tenant=self.tenant, role=Role.EMPLOYEE)
        ProjectRole.objects.create(user=self.finance, tenant=self.tenant, role=Role.FINANCE)
        self.client_obj = Client.objects.create(
            tenant=self.tenant, name="V7 Client", status="active",
        )
        self.project = Project.objects.create(
            tenant=self.tenant, code="V7-001", name="V7 Project",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
        )
        self.category = ExpenseCategory.objects.create(
            tenant=self.tenant, name="Transport",
            is_refacturable_default=False, requires_receipt=True,
        )


class TestExpenseReportLifecycle(BaseV7Test):
    """Full expense report lifecycle: create -> submit -> PM approve -> finance approve -> paid."""

    def test_create_expense_report(self):
        """Employee creates a new expense report."""
        c = self._api(self.employee)
        resp = c.post("/api/v1/expense_reports/", {
            "project": self.project.id,
            "total_amount": "150.00",
            "status": "SUBMITTED",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])
        data = self._d(resp)
        self.assertEqual(data["employee"], self.employee.id)
        self.assertEqual(data["status"], "SUBMITTED")

    def test_submit_expense_report(self):
        """Employee submits a REJECTED expense report for re-approval."""
        report = ExpenseReport.objects.create(
            tenant=self.tenant, employee=self.employee,
            project=self.project, status="REJECTED", total_amount=100,
        )
        c = self._api(self.employee)
        resp = c.post(f"/api/v1/expense_reports/{report.id}/submit/")
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "SUBMITTED")

    def test_approve_pm(self):
        """PM approves a submitted expense report."""
        report = ExpenseReport.objects.create(
            tenant=self.tenant, employee=self.employee,
            project=self.project, status="SUBMITTED", total_amount=200,
        )
        c = self._api(self.pm)
        resp = c.post(f"/api/v1/expense_reports/{report.id}/approve_pm/")
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "PM_APPROVED")

    def test_approve_finance(self):
        """Finance validates a PM-approved expense report."""
        report = ExpenseReport.objects.create(
            tenant=self.tenant, employee=self.employee,
            project=self.project, status="PM_APPROVED", total_amount=300,
        )
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/expense_reports/{report.id}/approve_finance/")
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "FINANCE_VALIDATED")

    def test_reject(self):
        """PM rejects a submitted expense report."""
        report = ExpenseReport.objects.create(
            tenant=self.tenant, employee=self.employee,
            project=self.project, status="SUBMITTED", total_amount=50,
        )
        c = self._api(self.pm)
        resp = c.post(f"/api/v1/expense_reports/{report.id}/reject/")
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "REJECTED")

    def test_mark_paid(self):
        """Finance marks a validated expense report as paid."""
        report = ExpenseReport.objects.create(
            tenant=self.tenant, employee=self.employee,
            project=self.project, status="FINANCE_VALIDATED", total_amount=500,
        )
        c = self._api(self.finance)
        resp = c.post(f"/api/v1/expense_reports/{report.id}/mark_paid/")
        self.assertEqual(resp.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, "PAID")


class TestExpenseLines(BaseV7Test):
    """Expense line CRUD within an expense report."""

    def setUp(self):
        super().setUp()
        self.report = ExpenseReport.objects.create(
            tenant=self.tenant, employee=self.employee,
            project=self.project, status="SUBMITTED", total_amount=0,
        )

    def test_create_expense_line(self):
        """Add a line item to an expense report."""
        c = self._api(self.employee)
        resp = c.post(
            f"/api/v1/expense_reports/{self.report.id}/lines/",
            {
                "category": self.category.id,
                "expense_date": "2026-03-20",
                "amount": "75.50",
                "description": "Taxi aeroport",
                "is_refacturable": False,
                "tax_type": "HT",
            },
            format="json",
        )
        self.assertIn(resp.status_code, [200, 201])
        self.assertEqual(ExpenseLine.objects.filter(report=self.report).count(), 1)

    def test_list_lines_for_report(self):
        """List all lines for a given expense report."""
        ExpenseLine.objects.create(
            tenant=self.tenant, report=self.report, category=self.category,
            expense_date="2026-03-20", amount=50, description="Repas",
        )
        ExpenseLine.objects.create(
            tenant=self.tenant, report=self.report, category=self.category,
            expense_date="2026-03-21", amount=30, description="Taxi",
        )
        c = self._api(self.employee)
        resp = c.get(f"/api/v1/expense_reports/{self.report.id}/lines/")
        self.assertEqual(resp.status_code, 200)
        results = self._list(resp)
        if isinstance(results, dict):
            results = results.get("results", results)
        self.assertEqual(len(results), 2)

    def test_delete_line(self):
        """Delete a line item from an expense report."""
        line = ExpenseLine.objects.create(
            tenant=self.tenant, report=self.report, category=self.category,
            expense_date="2026-03-20", amount=25, description="Parking",
        )
        c = self._api(self.employee)
        resp = c.delete(f"/api/v1/expense_reports/{self.report.id}/lines/{line.id}/")
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(ExpenseLine.objects.filter(report=self.report).count(), 0)


class TestExpenseCategories(BaseV7Test):
    """Expense category management."""

    def test_list_categories(self):
        """List all expense categories for the tenant."""
        c = self._api(self.employee)
        resp = c.get("/api/v1/expense_categories/")
        self.assertEqual(resp.status_code, 200)
        results = self._list(resp)
        if isinstance(results, dict):
            results = results.get("results", results)
        # At least the one created in setUp
        self.assertGreaterEqual(len(results), 1)

    def test_create_category(self):
        """Create a new expense category."""
        c = self._api(self.finance)
        resp = c.post("/api/v1/expense_categories/", {
            "name": "Hebergement",
            "is_refacturable_default": True,
            "requires_receipt": True,
            "gl_account": "6200",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])
        self.assertTrue(
            ExpenseCategory.objects.filter(name="Hebergement").exists()
        )
