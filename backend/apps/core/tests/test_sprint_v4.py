"""Sprint V4 — Projects + WBS + Resources integration tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.clients.models import Client
from apps.core.models import BusinessUnit, ProjectRole, Role, Tenant, UserTenantAssociation
from apps.projects.models import Phase, Project, ProjectTemplate, WBSElement

User = get_user_model()


class BaseV4Test(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v4")
        self.admin = User.objects.create_user(username="v4admin", password="x")
        UserTenantAssociation.objects.create(user=self.admin, tenant=self.tenant)
        ProjectRole.objects.create(user=self.admin, tenant=self.tenant, role=Role.ADMIN)
        self.client_obj = Client.objects.create(tenant=self.tenant, name="Test Client", status="active")
        self.c = APIClient()
        self.c.force_authenticate(user=self.admin)


class TestProjectCreation(BaseV4Test):
    def test_create_project_with_client(self):
        resp = self.c.post("/api/v1/projects/", {
            "code": "PR-001", "name": "Test Project",
            "client": self.client_obj.id, "contract_type": "FORFAITAIRE",
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])

    def test_create_from_template(self):
        tmpl = ProjectTemplate.objects.create(
            tenant=self.tenant, name="Test", code="TPL",
            contract_type="FORFAITAIRE",
            phases_config=[{"name": "Concept", "client_label": "Phase 1", "billing_mode": "FORFAIT"}],
        )
        resp = self.c.post("/api/v1/projects/create_from_template/", {
            "template_id": tmpl.id,
            "project": {"code": "PR-002", "name": "From Template", "client": self.client_obj.id},
        }, format="json")
        self.assertIn(resp.status_code, [200, 201])


class TestStatusTransitions(BaseV4Test):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            tenant=self.tenant, code="PR-ST", name="Status Test",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
        )

    def test_valid_transition_active_to_on_hold(self):
        resp = self.c.patch(f"/api/v1/projects/{self.project.id}/", {"status": "ON_HOLD"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_valid_transition_active_to_completed(self):
        resp = self.c.patch(f"/api/v1/projects/{self.project.id}/", {"status": "COMPLETED"}, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_invalid_transition_completed_to_active(self):
        self.project.status = "COMPLETED"
        self.project.save(skip_version_increment=True)
        resp = self.c.patch(f"/api/v1/projects/{self.project.id}/", {"status": "ACTIVE"}, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("INVALID_STATUS_TRANSITION", resp.json().get("error", {}).get("code", ""))

    def test_invalid_transition_cancelled_to_active(self):
        self.project.status = "CANCELLED"
        self.project.save(skip_version_increment=True)
        resp = self.c.patch(f"/api/v1/projects/{self.project.id}/", {"status": "ACTIVE"}, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_on_hold_to_active(self):
        self.project.status = "ON_HOLD"
        self.project.save(skip_version_increment=True)
        resp = self.c.patch(f"/api/v1/projects/{self.project.id}/", {"status": "ACTIVE"}, format="json")
        self.assertEqual(resp.status_code, 200)


class TestWBSCrud(BaseV4Test):
    def setUp(self):
        super().setUp()
        self.project = Project.objects.create(
            tenant=self.tenant, code="PR-WBS", name="WBS Test",
            client=self.client_obj, status="ACTIVE", contract_type="FORFAITAIRE",
        )
        self.phase = Phase.objects.create(
            tenant=self.tenant, project=self.project, name="Concept",
            phase_type="REALIZATION", billing_mode="FORFAIT",
        )

    def test_create_wbs_element(self):
        resp = self.c.post(f"/api/v1/projects/{self.project.id}/wbs/", {
            "standard_label": "Études préliminaires",
            "client_facing_label": "Phase 1 — Études",
            "element_type": "TASK",
            "budgeted_hours": "100",
            "phase": self.phase.id,
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_update_wbs_element(self):
        wbs = WBSElement.objects.create(
            tenant=self.tenant, project=self.project,
            standard_label="Old", element_type="TASK",
        )
        resp = self.c.patch(f"/api/v1/projects/{self.project.id}/wbs/{wbs.id}/", {
            "standard_label": "New Label",
        }, format="json")
        self.assertEqual(resp.status_code, 200)

    def test_delete_wbs_element(self):
        wbs = WBSElement.objects.create(
            tenant=self.tenant, project=self.project,
            standard_label="Del", element_type="TASK",
        )
        resp = self.c.delete(f"/api/v1/projects/{self.project.id}/wbs/{wbs.id}/")
        self.assertEqual(resp.status_code, 204)


# TestAssignment supprimé: EmployeeAssignment déprécié au profit de ResourceAllocation.
# La planification d'équipe se fait désormais via /api/v1/allocations/ (module planning).


class TestUserSearch(BaseV4Test):
    def test_search_by_username(self):
        User.objects.create_user(username="jean.dupont", email="jean@test.com", password="x")
        resp = self.c.get("/api/v1/users/search/?q=jean")
        self.assertEqual(resp.status_code, 200)
        data = resp.json().get("data", resp.json())
        results = data if isinstance(data, list) else []
        self.assertTrue(any("jean" in str(r) for r in results))

    def test_search_empty_query(self):
        resp = self.c.get("/api/v1/users/search/")
        self.assertEqual(resp.status_code, 200)

    def test_search_accessible_to_non_admin(self):
        emp = User.objects.create_user(username="emp_search", password="x")
        UserTenantAssociation.objects.create(user=emp, tenant=self.tenant)
        ProjectRole.objects.create(user=emp, tenant=self.tenant, role=Role.EMPLOYEE)
        c2 = APIClient()
        c2.force_authenticate(user=emp)
        resp = c2.get("/api/v1/users/search/?q=admin")
        self.assertEqual(resp.status_code, 200)


class TestBusinessUnitDropdown(BaseV4Test):
    def test_list_business_units(self):
        BusinessUnit.objects.create(tenant=self.tenant, name="Architecture", code="ARCH")
        resp = self.c.get("/api/v1/business_units/")
        self.assertEqual(resp.status_code, 200)
