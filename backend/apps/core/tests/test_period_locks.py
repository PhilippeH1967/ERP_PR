"""Period lock/unlock acceptance tests — ATDD for lock enforcement across all operations.

These tests are designed to FAIL until the corresponding lock-enforcement logic
is fully wired in views.py.  Each test documents one acceptance criterion.
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.projects.models import Phase, Project
from apps.time_entries.models import (
    PeriodFreeze,
    PeriodUnlock,
    TimeEntry,
    TimesheetLock,
    WeeklyApproval,
)

User = get_user_model()

# ── Constant dates (Sunday 2026-03-01 to Saturday 2026-03-07) ──
WEEK_START = date(2026, 3, 1)   # Sunday
WEEK_END = date(2026, 3, 7)     # Saturday
MONDAY = date(2026, 3, 2)
TUESDAY = date(2026, 3, 3)

# A second week for copy_previous_week target
NEXT_WEEK_START = WEEK_START + timedelta(weeks=1)  # Sunday 2026-03-08


class PeriodLockBaseTest(TestCase):
    """Common fixtures for all period-lock tests."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="LockTenant", slug="lock-tenant")

        # Users
        self.admin = User.objects.create_user(username="lock_admin", password="x")
        self.finance = User.objects.create_user(username="lock_finance", password="x")
        self.paie = User.objects.create_user(username="lock_paie", password="x")
        self.pm = User.objects.create_user(username="lock_pm", password="x")
        self.employee = User.objects.create_user(username="lock_emp", password="x")

        for u in [self.admin, self.finance, self.paie, self.pm, self.employee]:
            UserTenantAssociation.objects.create(user=u, tenant=self.tenant)

        # Roles
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        ProjectRole.objects.create(user=self.finance, tenant=self.tenant, role=Role.FINANCE)
        ProjectRole.objects.create(user=self.paie, tenant=self.tenant, role=Role.PAIE)
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        ProjectRole.objects.create(user=self.employee, tenant=self.tenant, role=Role.EMPLOYEE)

        # Project + phase
        self.client_obj = Client.objects.create(
            tenant=self.tenant, name="Lock Client", status="active",
        )
        self.project = Project.objects.create(
            tenant=self.tenant, code="LK-001", name="Lock Project",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
            pm=self.pm,
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Design",
            phase_type="REALIZATION", billing_mode="FORFAIT",
        )
        self.phase2 = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Dev",
            phase_type="REALIZATION", billing_mode="FORFAIT",
        )

        self.api = APIClient()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. Period lock blocks entry creation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodLockBlocksCreation(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Create a LOCKED entry on MONDAY — makes that date "locked"
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="LOCKED",
        )

    def test_create_entry_on_locked_date_returns_400(self):
        """AC-1: Creating a new entry on a date with LOCKED entries is rejected."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/", {
            "project": self.project.id,
            "phase": self.phase2.id,  # different phase, same date
            "date": MONDAY.isoformat(),
            "hours": "4",
        }, format="json")
        self.assertEqual(resp.status_code, 400)
        data = resp.json().get("data", resp.json())
        error = data.get("error", {})
        self.assertEqual(error.get("code"), "PERIOD_LOCKED")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. Period lock blocks entry update
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodLockBlocksUpdate(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        self.locked_entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="LOCKED",
        )

    def test_update_locked_entry_returns_400(self):
        """AC-2: Updating an entry whose status is LOCKED is rejected."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.patch(
            f"/api/v1/time_entries/{self.locked_entry.id}/",
            {"hours": "6"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.json().get("data", resp.json())
        error = data.get("error", {})
        self.assertEqual(error.get("code"), "ENTRY_LOCKED")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Period lock blocks entry deletion
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodLockBlocksDeletion(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        self.locked_entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="LOCKED",
        )

    def test_delete_locked_entry_returns_400(self):
        """AC-3: Deleting a LOCKED entry is rejected."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.delete(f"/api/v1/time_entries/{self.locked_entry.id}/")
        self.assertEqual(resp.status_code, 400)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. Period lock blocks submit_week
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodLockBlocksSubmitWeek(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # One DRAFT entry + one LOCKED entry in the same week
        self.draft_entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=TUESDAY, hours=7, status="DRAFT",
        )
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase2, date=MONDAY, hours=8, status="LOCKED",
        )

    def test_submit_week_on_locked_period_returns_400(self):
        """AC-4: submit_week fails if any day in the week has LOCKED entries."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/submit_week/", {
            "week_start": WEEK_START.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 400)
        data = resp.json().get("data", resp.json())
        error = data.get("error", {})
        self.assertEqual(error.get("code"), "PERIOD_LOCKED")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. Period lock blocks copy_previous_week to locked target
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodLockBlocksCopyPreviousWeek(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Previous week has a copyable entry
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="DRAFT",
        )
        # Target week (next week) has LOCKED entries
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase2, date=NEXT_WEEK_START + timedelta(days=1),
            hours=8, status="LOCKED",
        )

    def test_copy_previous_week_to_locked_target_returns_400(self):
        """AC-5: copy_previous_week fails if the target week has LOCKED entries."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/copy_previous_week/", {
            "week_start": NEXT_WEEK_START.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 400)
        data = resp.json().get("data", resp.json())
        error = data.get("error", {})
        self.assertEqual(error.get("code"), "PERIOD_LOCKED")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. PeriodFreeze blocks creation on frozen dates (no existing entries)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodFreezeBlocksCreation(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Freeze everything before 2026-03-15 — MONDAY (2026-03-02) is frozen
        PeriodFreeze.objects.create(
            tenant=self.tenant,
            freeze_before=date(2026, 3, 15),
            frozen_by=self.admin,
        )

    def test_create_entry_on_frozen_date_returns_400(self):
        """AC-6: Creating an entry before freeze_before date is rejected even with no existing entries."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/", {
            "project": self.project.id,
            "phase": self.phase.id,
            "date": MONDAY.isoformat(),
            "hours": "7.5",
        }, format="json")
        self.assertEqual(resp.status_code, 400)
        data = resp.json().get("data", resp.json())
        error = data.get("error", {})
        self.assertEqual(error.get("code"), "PERIOD_FROZEN")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. PeriodUnlock exception allows creation on frozen dates
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestPeriodUnlockAllowsCreation(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Freeze before 2026-03-15
        PeriodFreeze.objects.create(
            tenant=self.tenant,
            freeze_before=date(2026, 3, 15),
            frozen_by=self.admin,
        )
        # But unlock the first week (2026-03-01 to 2026-03-07)
        PeriodUnlock.objects.create(
            tenant=self.tenant,
            period_start=WEEK_START,
            period_end=WEEK_END,
            reason="CORRECTION",
            justification="Employee correction needed",
            unlocked_by=self.admin,
        )

    def test_create_entry_on_unlocked_frozen_date_succeeds(self):
        """AC-7: PeriodUnlock exception allows entry creation on otherwise frozen dates."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/", {
            "project": self.project.id,
            "phase": self.phase.id,
            "date": MONDAY.isoformat(),
            "hours": "7.5",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201],
                       f"Expected 200/201 but got {resp.status_code}: {resp.json()}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. Revoking PeriodUnlock re-locks entries
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestRevokeUnlockRelocksEntries(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Create an unlock
        self.unlock = PeriodUnlock.objects.create(
            tenant=self.tenant,
            period_start=WEEK_START,
            period_end=WEEK_END,
            reason="CORRECTION",
            unlocked_by=self.admin,
        )
        # Create entries in that period that were edited during unlock window
        self.entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="SUBMITTED",
        )

    def test_deleting_unlock_relocks_entries(self):
        """AC-8: Deleting a PeriodUnlock re-locks all non-LOCKED entries in that period."""
        self.api.force_authenticate(user=self.admin)
        resp = self.api.delete(f"/api/v1/period_unlocks/{self.unlock.id}/")
        self.assertIn(resp.status_code, [200, 204])
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.status, "LOCKED",
                         "Entry should be re-locked after PeriodUnlock is revoked")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 9. Only ADMIN/FINANCE/PAIE can lock (PM gets 403)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestLockRoleEnforcement(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Create a SUBMITTED entry so there is something to lock
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="SUBMITTED",
        )

    def test_pm_cannot_lock_period(self):
        """AC-9a: PM cannot call lock_period — gets 403."""
        self.api.force_authenticate(user=self.pm)
        resp = self.api.post("/api/v1/time_entries/lock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 403)

    def test_employee_cannot_lock_period(self):
        """AC-9b: EMPLOYEE cannot call lock_period — gets 403."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/lock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 403)

    def test_admin_can_lock_period(self):
        """AC-9c: ADMIN can call lock_period successfully."""
        self.api.force_authenticate(user=self.admin)
        resp = self.api.post("/api/v1/time_entries/lock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_finance_can_lock_period(self):
        """AC-9d: FINANCE can call lock_period successfully."""
        self.api.force_authenticate(user=self.finance)
        resp = self.api.post("/api/v1/time_entries/lock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_paie_can_lock_period(self):
        """AC-9e: PAIE can call lock_period successfully."""
        self.api.force_authenticate(user=self.paie)
        resp = self.api.post("/api/v1/time_entries/lock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_pm_cannot_lock_before(self):
        """AC-9f: PM cannot call lock_before — gets 403."""
        self.api.force_authenticate(user=self.pm)
        resp = self.api.post("/api/v1/time_entries/lock_before/", {
            "before_date": date(2026, 3, 15).isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 403)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 10. Only ADMIN/FINANCE/PAIE can unlock (EMPLOYEE gets 403)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestUnlockRoleEnforcement(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Lock some entries first
        TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="LOCKED",
        )

    def test_employee_cannot_unlock_period(self):
        """AC-10a: EMPLOYEE cannot call unlock_period — gets 403."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/unlock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 403)

    def test_pm_cannot_unlock_period(self):
        """AC-10b: PM cannot call unlock_period — gets 403."""
        self.api.force_authenticate(user=self.pm)
        resp = self.api.post("/api/v1/time_entries/unlock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 403)

    def test_admin_can_unlock_period(self):
        """AC-10c: ADMIN can call unlock_period successfully."""
        self.api.force_authenticate(user=self.admin)
        resp = self.api.post("/api/v1/time_entries/unlock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_finance_can_unlock_period(self):
        """AC-10d: FINANCE can call unlock_period successfully."""
        self.api.force_authenticate(user=self.finance)
        resp = self.api.post("/api/v1/time_entries/unlock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 11. TimesheetLock (phase-level) blocks entry creation on locked phase
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestTimesheetLockBlocksCreation(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Lock phase "Design" at the phase level
        TimesheetLock.objects.create(
            tenant=self.tenant,
            project=self.project,
            phase=self.phase,
            lock_type="PHASE",
            locked_by=self.admin,
        )

    def test_create_entry_on_phase_locked_returns_400(self):
        """AC-11: Creating an entry on a phase with an active TimesheetLock is rejected."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/", {
            "project": self.project.id,
            "phase": self.phase.id,
            "date": MONDAY.isoformat(),
            "hours": "7.5",
        }, format="json")
        self.assertEqual(resp.status_code, 400,
                         f"Expected 400 for phase-locked entry but got {resp.status_code}: {resp.json()}")
        data = resp.json().get("data", resp.json())
        error = data.get("error", {})
        self.assertEqual(error.get("code"), "PHASE_LOCKED")

    def test_create_entry_on_unlocked_phase_succeeds(self):
        """AC-11b: Creating an entry on a different, unlocked phase still works."""
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/time_entries/", {
            "project": self.project.id,
            "phase": self.phase2.id,  # phase2 is NOT locked
            "date": MONDAY.isoformat(),
            "hours": "7.5",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201],
                       f"Expected 200/201 but got {resp.status_code}: {resp.json()}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 12. unlock_period reverts to SUBMITTED not DRAFT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class TestUnlockPeriodRevertsToSubmitted(PeriodLockBaseTest):
    def setUp(self):
        super().setUp()
        # Simulate a locked entry that was previously SUBMITTED
        self.entry = TimeEntry.objects.create(
            tenant=self.tenant, employee=self.employee, project=self.project,
            phase=self.phase, date=MONDAY, hours=8, status="LOCKED",
        )

    def test_unlock_period_sets_status_to_submitted(self):
        """AC-12: unlock_period reverts LOCKED entries to SUBMITTED, not DRAFT."""
        self.api.force_authenticate(user=self.admin)
        resp = self.api.post("/api/v1/time_entries/unlock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.status, "SUBMITTED",
                         "unlock_period must revert to SUBMITTED, not DRAFT")
        # Also verify it did NOT revert to DRAFT
        self.assertNotEqual(self.entry.status, "DRAFT",
                            "unlock_period must NOT revert to DRAFT")

    def test_unlock_period_returns_count(self):
        """AC-12b: unlock_period response includes the count of unlocked entries."""
        self.api.force_authenticate(user=self.admin)
        resp = self.api.post("/api/v1/time_entries/unlock_period/", {
            "period_start": WEEK_START.isoformat(),
            "period_end": WEEK_END.isoformat(),
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json().get("data", resp.json())
        self.assertEqual(data["unlocked_count"], 1)
