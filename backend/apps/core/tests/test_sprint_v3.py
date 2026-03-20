"""Sprint V3 — Admin + Configuration integration tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.core.models import (
    BusinessUnit, LaborRule, PositionProfile, ProjectRole, Role,
    TaxConfiguration, Tenant, UserTenantAssociation,
)

User = get_user_model()


class TestFR83_BusinessUnits(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v3-bu")
        self.admin = User.objects.create_user(username="v3admin", password="x")
        UserTenantAssociation.objects.create(user=self.admin, tenant=self.tenant)
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        self.c = APIClient()
        self.c.force_authenticate(user=self.admin)

    def test_create_bu(self):
        resp = self.c.post("/api/v1/business_units/", {"name": "Architecture", "code": "ARCH"}, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_bus(self):
        BusinessUnit.objects.create(tenant=self.tenant, name="Design")
        resp = self.c.get("/api/v1/business_units/")
        self.assertEqual(resp.status_code, 200)

    def test_update_bu(self):
        bu = BusinessUnit.objects.create(tenant=self.tenant, name="Old")
        resp = self.c.patch(f"/api/v1/business_units/{bu.id}/", {"name": "New"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_delete_bu(self):
        bu = BusinessUnit.objects.create(tenant=self.tenant, name="Del")
        resp = self.c.delete(f"/api/v1/business_units/{bu.id}/")
        self.assertEqual(resp.status_code, 204)


class TestFR83_PositionProfiles(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v3-pos")
        self.admin = User.objects.create_user(username="v3pos", password="x")
        UserTenantAssociation.objects.create(user=self.admin, tenant=self.tenant)
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        self.c = APIClient()
        self.c.force_authenticate(user=self.admin)

    def test_create_profile(self):
        resp = self.c.post("/api/v1/position_profiles/", {"name": "Architecte", "code": "ARCH", "category": "Professionnel"}, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_profiles(self):
        PositionProfile.objects.create(tenant=self.tenant, name="Urbaniste")
        resp = self.c.get("/api/v1/position_profiles/")
        self.assertEqual(resp.status_code, 200)

    def test_update_profile(self):
        p = PositionProfile.objects.create(tenant=self.tenant, name="Old")
        resp = self.c.patch(f"/api/v1/position_profiles/{p.id}/", {"hourly_cost_rate": "85.00"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_delete_profile(self):
        p = PositionProfile.objects.create(tenant=self.tenant, name="Del")
        resp = self.c.delete(f"/api/v1/position_profiles/{p.id}/")
        self.assertEqual(resp.status_code, 204)


class TestFR83_TaxConfiguration(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v3-tax")
        self.admin = User.objects.create_user(username="v3tax", password="x")
        UserTenantAssociation.objects.create(user=self.admin, tenant=self.tenant)
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        self.c = APIClient()
        self.c.force_authenticate(user=self.admin)

    def test_create_tax_config(self):
        resp = self.c.post("/api/v1/tax_configurations/", {
            "legal_entity": "PR Productions", "tps_rate": "5.000", "tvq_rate": "9.975"
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_update_rates(self):
        t = TaxConfiguration.objects.create(tenant=self.tenant, legal_entity="PRAA", tps_rate=5, tvq_rate=9.975)
        resp = self.c.patch(f"/api/v1/tax_configurations/{t.id}/", {"tvq_rate": "10.000"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_non_admin_blocked(self):
        """Non-admin cannot access tax config."""
        emp = User.objects.create_user(username="v3emp", password="x")
        UserTenantAssociation.objects.create(user=emp, tenant=self.tenant)
        ProjectRole.objects.create(user=emp, tenant=self.tenant, role=Role.EMPLOYEE)
        c2 = APIClient()
        c2.force_authenticate(user=emp)
        resp = c2.get("/api/v1/tax_configurations/")
        self.assertEqual(resp.status_code, 403)


class TestFR78_LaborRules(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v3-lr")
        self.admin = User.objects.create_user(username="v3lr", password="x")
        UserTenantAssociation.objects.create(user=self.admin, tenant=self.tenant)
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        self.c = APIClient()
        self.c.force_authenticate(user=self.admin)

    def test_create_labor_rule(self):
        resp = self.c.post("/api/v1/labor_rules/", {
            "name": "Québec standard", "weekly_hours": "40.0", "daily_hours": "8.0",
            "overtime_threshold_weekly": "40.0", "overtime_threshold_daily": "8.0",
            "statutory_holidays": ["2026-01-01", "2026-07-01"],
            "rest_days": [5, 6],
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_update_rule(self):
        r = LaborRule.objects.create(tenant=self.tenant, name="Old", weekly_hours=40)
        resp = self.c.patch(f"/api/v1/labor_rules/{r.id}/", {"weekly_hours": "37.5"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_holidays_stored(self):
        r = LaborRule.objects.create(
            tenant=self.tenant, name="QC",
            statutory_holidays=["2026-01-01", "2026-07-01", "2026-09-07"],
        )
        resp = self.c.get(f"/api/v1/labor_rules/{r.id}/")
        data = resp.json().get("data", resp.json())
        self.assertEqual(len(data["statutory_holidays"]), 3)

    def test_non_admin_blocked(self):
        emp = User.objects.create_user(username="v3emp_lr", password="x")
        UserTenantAssociation.objects.create(user=emp, tenant=self.tenant)
        ProjectRole.objects.create(user=emp, tenant=self.tenant, role=Role.EMPLOYEE)
        c2 = APIClient()
        c2.force_authenticate(user=emp)
        resp = c2.get("/api/v1/labor_rules/")
        self.assertEqual(resp.status_code, 403)
