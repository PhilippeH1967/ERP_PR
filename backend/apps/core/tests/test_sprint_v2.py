"""Sprint V2 — Clients + Organizations integration tests."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.clients.models import Client, ClientAddress, Contact
from apps.core.models import ProjectRole, Role, Tenant, UserTenantAssociation
from apps.suppliers.models import ExternalOrganization

User = get_user_model()


class TestFR86_ClientCRUD(TestCase):
    """FR86: Client 5-tab interface with CRUD."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-v2")
        self.user = User.objects.create_user(username="v2user", password="Test123!")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)

    def test_create_client(self):
        resp = self.client_api.post("/api/v1/clients/", {
            "name": "Test Client", "alias": "TC", "sector": "Public", "status": "active",
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_list_clients(self):
        Client.objects.create(tenant=self.tenant, name="C1", status="active")
        resp = self.client_api.get("/api/v1/clients/")
        self.assertEqual(resp.status_code, 200)

    def test_update_client(self):
        c = Client.objects.create(tenant=self.tenant, name="Old", status="active")
        resp = self.client_api.patch(f"/api/v1/clients/{c.id}/", {"name": "New"}, format="json")
        self.assertEqual(resp.status_code, 200)
        c.refresh_from_db()
        self.assertEqual(c.name, "New")

    def test_delete_client(self):
        c = Client.objects.create(tenant=self.tenant, name="Del", status="active")
        resp = self.client_api.delete(f"/api/v1/clients/{c.id}/")
        self.assertEqual(resp.status_code, 204)

    def test_search_by_alias(self):
        Client.objects.create(tenant=self.tenant, name="Ville Montreal", alias="VDM", status="active")
        resp = self.client_api.get("/api/v1/clients/?search=VDM")
        data = resp.json().get("data", resp.json())
        results = data if isinstance(data, list) else data.get("results", [])
        self.assertTrue(any("VDM" in str(r) for r in results))

    def test_add_contact(self):
        c = Client.objects.create(tenant=self.tenant, name="CC", status="active")
        resp = self.client_api.post(f"/api/v1/clients/{c.id}/contacts/", {
            "name": "Jean Dupont", "email": "jean@test.com", "role": "Directeur",
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_delete_contact(self):
        c = Client.objects.create(tenant=self.tenant, name="CC2", status="active")
        contact = Contact.objects.create(client=c, tenant=self.tenant, name="Del Contact")
        resp = self.client_api.delete(f"/api/v1/clients/{c.id}/contacts/{contact.id}/")
        self.assertEqual(resp.status_code, 204)

    def test_add_address(self):
        c = Client.objects.create(tenant=self.tenant, name="CA", status="active")
        resp = self.client_api.post(f"/api/v1/clients/{c.id}/addresses/", {
            "address_line_1": "100 rue Test", "city": "Montreal", "province": "QC", "postal_code": "H2X 1Y4",
        }, format="json")
        self.assertEqual(resp.status_code, 201)

    def test_delete_address(self):
        c = Client.objects.create(tenant=self.tenant, name="CA2", status="active")
        addr = ClientAddress.objects.create(client=c, tenant=self.tenant, address_line_1="Del", city="MTL")
        resp = self.client_api.delete(f"/api/v1/clients/{c.id}/addresses/{addr.id}/")
        self.assertEqual(resp.status_code, 204)


class TestFR86b_DuplicateDetection(TestCase):
    """FR86b: Duplicate client detection."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-dup")
        self.user = User.objects.create_user(username="dupuser", password="Test123!")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)
        Client.objects.create(tenant=self.tenant, name="Provencher Roy", alias="PR", status="active")

    def test_detect_name_duplicate(self):
        resp = self.client_api.post("/api/v1/clients/check_duplicate/", {"name": "Provencher"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json().get("data", resp.json()).get("duplicates", resp.json().get("duplicates", []))) > 0)

    def test_no_duplicate_for_unique(self):
        resp = self.client_api.post("/api/v1/clients/check_duplicate/", {"name": "ZZZZZZZ"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json().get("data", resp.json()).get("duplicates", resp.json().get("duplicates", []))), 0)


class TestFR86e_FinancialHistory(TestCase):
    """FR86e: Client financial summary."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-fin")
        self.user = User.objects.create_user(username="finuser", password="Test123!")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)
        self.test_client = Client.objects.create(tenant=self.tenant, name="FinClient", status="active")

    def test_financial_summary_endpoint(self):
        resp = self.client_api.get(f"/api/v1/clients/{self.test_client.id}/financial_summary/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        inner = data.get("data", data)
        self.assertIn("total_ca", inner)
        self.assertIn("aging", inner)


class TestFR88_Organizations(TestCase):
    """FR88: External organizations registry."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-org")
        self.user = User.objects.create_user(username="orguser", password="Test123!")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)

    def test_create_organization(self):
        resp = self.client_api.post("/api/v1/external_organizations/", {
            "name": "WSP Global", "neq": "1234567890", "city": "Montreal",
            "type_tags": ["st"], "banking_info": {"institution": "815", "transit": "30000"},
        }, format="json")
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        inner = data.get("data", data)
        self.assertIn("banking_info", inner)

    def test_banking_info_in_response(self):
        org = ExternalOrganization.objects.create(
            tenant=self.tenant, name="BankTest", banking_info={"institution": "815"},
        )
        resp = self.client_api.get(f"/api/v1/external_organizations/{org.id}/")
        data = resp.json()
        inner = data.get("data", data)
        self.assertEqual(inner["banking_info"]["institution"], "815")

    def test_search_by_neq(self):
        ExternalOrganization.objects.create(tenant=self.tenant, name="NEQ Org", neq="9999999")
        resp = self.client_api.get("/api/v1/external_organizations/?search=9999999")
        data = resp.json()
        results = data if isinstance(data, list) else data.get("results", data.get("data", []))
        if isinstance(results, list):
            self.assertTrue(len(results) > 0)

    def test_type_tags(self):
        org = ExternalOrganization.objects.create(
            tenant=self.tenant, name="TagOrg", type_tags=["st", "partner"],
        )
        resp = self.client_api.get(f"/api/v1/external_organizations/{org.id}/")
        data = resp.json().get("data", resp.json())
        self.assertEqual(data["type_tags"], ["st", "partner"])


class TestFR88b_OrgDuplicateDetection(TestCase):
    """FR88b: Organization duplicate detection."""

    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-orgdup")
        self.user = User.objects.create_user(username="orgdupuser", password="Test123!")
        UserTenantAssociation.objects.create(user=self.user, tenant=self.tenant)
        ProjectRole.objects.create(user=self.user, tenant=self.tenant, role=Role.ADMIN)
        self.client_api = APIClient()
        self.client_api.force_authenticate(user=self.user)
        ExternalOrganization.objects.create(
            tenant=self.tenant, name="BPA Ingénierie", neq="1122334455",
        )

    def test_detect_neq_duplicate(self):
        resp = self.client_api.post("/api/v1/external_organizations/check_duplicate/", {
            "neq": "1122334455",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        dups = resp.json().get("data", resp.json()).get("duplicates", resp.json().get("duplicates", []))
        self.assertTrue(any(d["match_type"] == "neq_exact" for d in dups))

    def test_detect_name_duplicate(self):
        resp = self.client_api.post("/api/v1/external_organizations/check_duplicate/", {
            "name": "BPA",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json().get("data", resp.json()).get("duplicates", resp.json().get("duplicates", []))) > 0)

    def test_no_duplicate(self):
        resp = self.client_api.post("/api/v1/external_organizations/check_duplicate/", {
            "name": "ZZZZZZZ", "neq": "0000000000",
        }, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json().get("data", resp.json()).get("duplicates", resp.json().get("duplicates", []))), 0)

    def test_unique_neq_constraint(self):
        """Creating org with duplicate NEQ should fail."""
        from django.db import IntegrityError
        try:
            resp = self.client_api.post("/api/v1/external_organizations/", {
                "name": "Autre Org", "neq": "1122334455",
            }, format="json")
            # If we get a response, it should be an error
            self.assertIn(resp.status_code, [400, 409, 500])
        except IntegrityError:
            pass  # Constraint works — this is expected
