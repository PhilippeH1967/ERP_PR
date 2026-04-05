"""Tests for Leave/Absence module."""

from datetime import date

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant

from .models import LeaveBank, LeaveRequest, LeaveType, RequestStatus


@pytest.mark.django_db
class TestLeaveTypeAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Leave", slug="leave-test")
        self.user = User.objects.create_user(username="leave_admin", password="pass123!")
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_seed_leave_types(self):
        resp = self.api.post("/api/v1/leave_types/seed/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["created"] >= 7

    def test_list_leave_types(self):
        LeaveType.objects.create(
            tenant=self.tenant, code="VAC", name="Vacances"
        )
        resp = self.api.get("/api/v1/leave_types/")
        assert resp.status_code == 200


@pytest.mark.django_db
class TestLeaveRequestAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="LReq", slug="lreq-test")
        self.employee = User.objects.create_user(username="emp_leave", password="pass123!")
        self.pm = User.objects.create_user(username="pm_leave", password="pass123!")
        ProjectRole.objects.create(user=self.pm, tenant=self.tenant, role=Role.PM)
        self.leave_type = LeaveType.objects.create(
            tenant=self.tenant, code="VAC", name="Vacances",
            is_paid=True, max_days_per_year=10,
        )
        # Create bank with 10 days accrued
        LeaveBank.objects.create(
            tenant=self.tenant, employee=self.employee,
            leave_type=self.leave_type, year=2026, accrued=10,
        )
        self.api = APIClient()

    def test_employee_creates_request(self):
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/leave_requests/", {
            "leave_type": self.leave_type.pk,
            "start_date": "2026-07-06",
            "end_date": "2026-07-10",
            "total_days": "5.00",
            "reason": "Vacances d'été",
        }, format="json")
        assert resp.status_code == 201
        data = resp.json().get("data", resp.json())
        assert data["status"] == "PENDING"

    def test_pm_approves_request(self):
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/leave_requests/", {
            "leave_type": self.leave_type.pk,
            "start_date": "2026-07-06",
            "end_date": "2026-07-10",
            "total_days": "5.00",
        }, format="json")
        request_id = resp.json().get("data", resp.json())["id"]

        self.api.force_authenticate(user=self.pm)
        resp2 = self.api.post(f"/api/v1/leave_requests/{request_id}/approve/")
        assert resp2.status_code == 200
        data = resp2.json().get("data", resp2.json())
        assert data["status"] == "APPROVED"
        assert data.get("time_entries_created_count", 0) >= 1

    def test_self_approval_blocked(self):
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/leave_requests/", {
            "leave_type": self.leave_type.pk,
            "start_date": "2026-07-06",
            "end_date": "2026-07-07",
            "total_days": "2.00",
        }, format="json")
        request_id = resp.json().get("data", resp.json())["id"]
        resp2 = self.api.post(f"/api/v1/leave_requests/{request_id}/approve/")
        assert resp2.status_code == 403

    def test_pm_rejects_request(self):
        req = LeaveRequest.objects.create(
            tenant=self.tenant, employee=self.employee,
            leave_type=self.leave_type,
            start_date=date(2026, 8, 3), end_date=date(2026, 8, 7),
            total_days=5, status=RequestStatus.PENDING,
        )
        self.api.force_authenticate(user=self.pm)
        resp = self.api.post(
            f"/api/v1/leave_requests/{req.pk}/reject/",
            {"reason": "Période chargée"},
            format="json",
        )
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["status"] == "REJECTED"

    def test_employee_cancels_request(self):
        req = LeaveRequest.objects.create(
            tenant=self.tenant, employee=self.employee,
            leave_type=self.leave_type,
            start_date=date(2026, 9, 1), end_date=date(2026, 9, 2),
            total_days=2, status=RequestStatus.PENDING,
        )
        self.api.force_authenticate(user=self.employee)
        resp = self.api.post(f"/api/v1/leave_requests/{req.pk}/cancel/")
        assert resp.status_code == 200
        data = resp.json().get("data", resp.json())
        assert data["status"] == "CANCELLED"

    def test_insufficient_balance_blocked(self):
        # Use up all days
        bank = LeaveBank.objects.get(
            employee=self.employee, leave_type=self.leave_type, year=2026,
        )
        bank.used = 9
        bank.save()

        self.api.force_authenticate(user=self.employee)
        resp = self.api.post("/api/v1/leave_requests/", {
            "leave_type": self.leave_type.pk,
            "start_date": "2026-10-06",
            "end_date": "2026-10-10",
            "total_days": "5.00",
        }, format="json")
        request_id = resp.json().get("data", resp.json())["id"]

        self.api.force_authenticate(user=self.pm)
        resp2 = self.api.post(f"/api/v1/leave_requests/{request_id}/approve/")
        assert resp2.status_code == 400
        assert "INSUFFICIENT_BALANCE" in resp2.json().get("error", {}).get("code", "")
