"""Sprint V5 — Timesheets + Approvals integration tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.projects.models import Phase, Project
from apps.time_entries.models import TimeEntry, WeeklyApproval

User = get_user_model()


class BaseV5Test(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v5")
        self.pm = User.objects.create_user(username="v5pm", password="x")
        self.employee = User.objects.create_user(username="v5emp", password="x")
        self.finance = User.objects.create_user(username="v5fin", password="x")
        for u in [self.pm, self.employee, self.finance]:
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        ProjectRole.objects.create(user=self.employee, tenant=self.tenant, role=Role.EMPLOYEE)
        ProjectRole.objects.create(user=self.finance, tenant=self.tenant, role=Role.FINANCE)
        self.client_obj = Client.objects.create(tenant=self.tenant, name="V5 Client", status="active")
        self.project = Project.objects.create(
            tenant=self.tenant, code="V5-001", name="V5 Project",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept",
            phase_type="REALIZATION", billing_mode="FORFAIT",
        )


class TestTimeEntryWorkflow(BaseV5Test):
    def test_create_entry(self):
        c = APIClient()
        c.force_authenticate(user=self.employee)
        resp = c.post("/api/v1/time_entries/", {
            "project": self.project.id, "phase": self.phase.id,
            "date": "2026-03-16", "hours": "7.5",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])

    def test_submit_week(self):
        c = APIClient()
        c.force_authenticate(user=self.employee)
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date="2026-03-16", hours=7.5, status="DRAFT",
        )
        resp = c.post("/api/v1/time_entries/submit_week/", {"week_start": "2026-03-16"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_copy_previous_week(self):
        c = APIClient()
        c.force_authenticate(user=self.employee)
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date="2026-03-09", hours=8, status="DRAFT",
        )
        resp = c.post("/api/v1/time_entries/copy_previous_week/", {"week_start": "2026-03-16"}, format="json")
        self.assertEqual(resp.status_code, 200)


class TestApprovalWorkflow(BaseV5Test):
    def setUp(self):
        super().setUp()
        self.approval = WeeklyApproval.objects.create(
            tenant=self.tenant, employee=self.employee,
            week_start="2026-03-16", week_end="2026-03-22", pm_status="PENDING", finance_status="PENDING",
        )

    def test_pm_approve(self):
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.post(f"/api/v1/weekly_approvals/{self.approval.id}/approve_pm/")
        self.assertEqual(resp.status_code, 200)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.pm_status, "APPROVED")

    def test_pm_reject(self):
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.post(f"/api/v1/weekly_approvals/{self.approval.id}/reject_pm/", {"reason": "Heures incorrectes"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.pm_status, "REJECTED")

    def test_pm_reject_reverts_entries_to_draft(self):
        """Rejecting reverts SUBMITTED entries back to DRAFT."""
        entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date="2026-03-16", hours=7.5, status="SUBMITTED",
        )
        c = APIClient()
        c.force_authenticate(user=self.pm)
        c.post(f"/api/v1/weekly_approvals/{self.approval.id}/reject_pm/", {"reason": "Fix"}, format="json")
        entry.refresh_from_db()
        self.assertEqual(entry.status, "DRAFT")

    def test_finance_approve(self):
        self.approval.pm_status = "APPROVED"
        self.approval.save()
        c = APIClient()
        c.force_authenticate(user=self.finance)
        resp = c.post(f"/api/v1/weekly_approvals/{self.approval.id}/approve_finance/")
        self.assertEqual(resp.status_code, 200)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.finance_status, "APPROVED")

    def test_finance_reject(self):
        self.approval.pm_status = "APPROVED"
        self.approval.save()
        c = APIClient()
        c.force_authenticate(user=self.finance)
        resp = c.post(f"/api/v1/weekly_approvals/{self.approval.id}/reject_finance/")
        self.assertEqual(resp.status_code, 200)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.finance_status, "REJECTED")

    def test_self_approval_blocked(self):
        c = APIClient()
        c.force_authenticate(user=self.employee)
        resp = c.post(f"/api/v1/weekly_approvals/{self.approval.id}/approve_pm/")
        self.assertEqual(resp.status_code, 403)

    def test_reject_already_approved_fails(self):
        self.approval.pm_status = "APPROVED"
        self.approval.save()
        c = APIClient()
        c.force_authenticate(user=self.pm)
        resp = c.post(f"/api/v1/weekly_approvals/{self.approval.id}/reject_pm/", {"reason": "Too late"}, format="json")
        self.assertEqual(resp.status_code, 400)


class TestPeriodUnlock(BaseV5Test):
    def test_create_unlock(self):
        c = APIClient()
        c.force_authenticate(user=self.finance)
        resp = c.post("/api/v1/period_unlocks/", {
            "period_start": "2026-03-16", "period_end": "2026-03-22",
            "reason": "CORRECTION",
            "justification": "Erreur de saisie signalée par employé",
        }, format="json")
        if resp.status_code not in [200, 201]:
            print("UNLOCK ERROR:", resp.json())
        self.assertIn(resp.status_code, [200, 201])
