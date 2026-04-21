"""Tests for the project budget-summary endpoint (story 12.1 Phase C).

Covers:
- ``Project.objects.with_current_contract_value()`` annotation: original + Σ approved deltas
- Only ``APPROVED`` amendments count (DRAFT/SUBMITTED/REJECTED ignored)
- ``GET /api/v1/projects/{id}/budget-summary/`` endpoint payload
- Permission: authenticated users with tenant access
- Cross-tenant isolation returns 404
- No N+1 query explosion on amendment list
"""

from __future__ import annotations

from decimal import Decimal

import pytest

from apps.core.models import Role
from apps.projects.models import Amendment, Project

from .conftest import AmendmentFactory, ProjectFactory

# --------------------------------------------------------------------------- #
# Queryset annotation
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestCurrentContractValueAnnotation:
    def test_project_with_no_amendments_returns_original_value(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("100000")

    def test_project_with_no_contract_value_returns_zero(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=None)
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("0")

    def test_approved_amendment_is_added_to_contract_value(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("15000"),
        )
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("115000")

    def test_draft_amendment_is_ignored(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.DRAFT,
            budget_impact=Decimal("15000"),
        )
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("100000")

    def test_submitted_amendment_is_ignored(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.SUBMITTED,
            budget_impact=Decimal("15000"),
        )
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("100000")

    def test_rejected_amendment_is_ignored(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.REJECTED,
            budget_impact=Decimal("15000"),
        )
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("100000")

    def test_multiple_approved_amendments_sum(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("15000"),
        )
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=2,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("7500"),
        )
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("122500")

    def test_negative_amendment_reduces_contract_value(self, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("-5000"),
        )
        annotated = Project.objects.with_current_contract_value().get(pk=project.pk)
        assert annotated.current_contract_value == Decimal("95000")


# --------------------------------------------------------------------------- #
# Budget summary endpoint
# --------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestBudgetSummaryEndpoint:
    def test_unauthenticated_returns_401(self, anonymous_client, project):
        response = anonymous_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        assert response.status_code == 401

    def test_authenticated_user_sees_original_and_current(self, admin_client, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("200000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("25000"),
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        assert response.status_code == 200, response.data
        payload = response.json()["data"]
        assert Decimal(payload["original_contract_value"]) == Decimal("200000")
        assert Decimal(payload["current_contract_value"]) == Decimal("225000")
        assert Decimal(payload["total_approved_impact"]) == Decimal("25000")

    def test_payload_includes_amendments_breakdown(self, admin_client, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("10000"),
            description="Ajout scope paysager",
        )
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=2,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("5000"),
            description="Travaux additionnels façade",
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        payload = response.json()["data"]
        assert len(payload["amendments"]) == 2
        numbers = [a["amendment_number"] for a in payload["amendments"]]
        assert 1 in numbers and 2 in numbers

    def test_payload_excludes_non_approved_from_breakdown(self, admin_client, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=1,
            status=Amendment.AmendmentStatus.APPROVED,
            budget_impact=Decimal("10000"),
        )
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=2,
            status=Amendment.AmendmentStatus.DRAFT,
            budget_impact=Decimal("5000"),
        )
        AmendmentFactory(
            project=project,
            tenant=tenant,
            amendment_number=3,
            status=Amendment.AmendmentStatus.REJECTED,
            budget_impact=Decimal("2500"),
        )
        response = admin_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        payload = response.json()["data"]
        assert len(payload["amendments"]) == 1
        assert payload["amendments"][0]["amendment_number"] == 1

    def test_cross_tenant_returns_404(self, other_tenant_admin_client, project):
        response = other_tenant_admin_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        assert response.status_code == 404

    def test_pm_can_access_budget_summary(self, api_client_as, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("50000"))
        client = api_client_as(role=Role.PM)
        response = client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        assert response.status_code == 200, response.data

    def test_no_n_plus_one_on_amendments_breakdown(
        self, admin_client, tenant, django_assert_max_num_queries
    ):
        project = ProjectFactory(tenant=tenant, total_fees=Decimal("100000"))
        for i in range(5):
            AmendmentFactory(
                project=project,
                tenant=tenant,
                amendment_number=i + 1,
                status=Amendment.AmendmentStatus.APPROVED,
                budget_impact=Decimal("1000"),
            )
        with django_assert_max_num_queries(15):
            response = admin_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        assert response.status_code == 200
        assert len(response.json()["data"]["amendments"]) == 5

    def test_project_without_contract_value_returns_zero(self, admin_client, tenant):
        project = ProjectFactory(tenant=tenant, total_fees=None)
        response = admin_client.get(f"/api/v1/projects/{project.pk}/budget-summary/")
        payload = response.json()["data"]
        assert Decimal(payload["original_contract_value"]) == Decimal("0")
        assert Decimal(payload["current_contract_value"]) == Decimal("0")
        assert payload["amendments"] == []
