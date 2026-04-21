"""
Shared fixtures & factories for `apps.projects` tests.

Conventions:
- Every fixture is scoped ``function`` unless explicitly marked otherwise.
- ``api_client_as(role=...)`` returns an authenticated APIClient with the
  requested role attached to the shared ``tenant`` fixture.
- ``other_tenant`` fixture provides a second tenant for cross-tenant tests.
"""

from __future__ import annotations

import factory
import pytest
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient

from apps.core.models import ProjectRole, Role, Tenant
from apps.projects.models import (
    Amendment,
    Phase,
    Project,
    ProjectTemplate,
    Task,
)

User = get_user_model()


# --------------------------------------------------------------------------- #
# Factories
# --------------------------------------------------------------------------- #


class TenantFactory(DjangoModelFactory):
    class Meta:
        model = Tenant
        django_get_or_create = ("slug",)

    name = factory.Sequence(lambda n: f"Tenant {n}")
    slug = factory.Sequence(lambda n: f"tenant-{n}")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.local")
    first_name = "Test"
    last_name = "User"


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    tenant = factory.SubFactory(TenantFactory)
    code = factory.Sequence(lambda n: f"PRJ-{n:04d}")
    name = factory.Sequence(lambda n: f"Projet {n}")
    contract_type = "FORFAITAIRE"
    status = "ACTIVE"


class PhaseFactory(DjangoModelFactory):
    class Meta:
        model = Phase

    tenant = factory.SelfAttribute("project.tenant")
    project = factory.SubFactory(ProjectFactory)
    code = factory.Sequence(lambda n: f"PH-{n}")
    name = factory.Sequence(lambda n: f"Phase {n}")
    order = factory.Sequence(lambda n: n)
    billing_mode = "FORFAIT"


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    tenant = factory.SelfAttribute("project.tenant")
    project = factory.SubFactory(ProjectFactory)
    phase = factory.SubFactory(
        PhaseFactory,
        project=factory.SelfAttribute("..project"),
        tenant=factory.SelfAttribute("..tenant"),
    )
    wbs_code = factory.Sequence(lambda n: f"1.{n}")
    name = factory.Sequence(lambda n: f"Tâche {n}")
    budgeted_hours = 10
    is_billable = True


class AmendmentFactory(DjangoModelFactory):
    class Meta:
        model = Amendment

    tenant = factory.SelfAttribute("project.tenant")
    project = factory.SubFactory(ProjectFactory)
    amendment_number = factory.Sequence(lambda n: n + 1)
    description = "Avenant de test"
    status = "DRAFT"
    budget_impact = 0


class ProjectTemplateFactory(DjangoModelFactory):
    class Meta:
        model = ProjectTemplate

    tenant = factory.SubFactory(TenantFactory)
    name = factory.Sequence(lambda n: f"Template {n}")
    contract_type = "FORFAITAIRE"
    phases_config = [
        {"name": "Concept", "code": "1", "type": "REALIZATION", "is_mandatory": False},
        {
            "name": "Gestion de projet",
            "code": "G",
            "type": "SUPPORT",
            "is_mandatory": True,
        },
    ]
    support_services_config = [{"name": "BIM", "client_label": "Service BIM"}]


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #


@pytest.fixture
def tenant(db) -> Tenant:
    return TenantFactory()


@pytest.fixture
def other_tenant(db) -> Tenant:
    return TenantFactory()


@pytest.fixture
def project(tenant) -> Project:
    return ProjectFactory(tenant=tenant)


@pytest.fixture
def phase(project) -> Phase:
    return PhaseFactory(project=project, tenant=project.tenant)


@pytest.fixture
def task(project, phase) -> Task:
    return TaskFactory(project=project, phase=phase, tenant=project.tenant)


@pytest.fixture
def amendment(project) -> Amendment:
    return AmendmentFactory(project=project, tenant=project.tenant)


@pytest.fixture
def project_template(tenant) -> ProjectTemplate:
    return ProjectTemplateFactory(tenant=tenant)


@pytest.fixture
def other_tenant_project(other_tenant) -> Project:
    return ProjectFactory(tenant=other_tenant, code="OTHER-001")


@pytest.fixture
def api_client_as(tenant):
    """
    Factory fixture: ``api_client_as(role="PM")`` returns an authenticated
    APIClient with the given role on ``tenant``. ``role=None`` returns an
    anonymous client.
    """

    def _make(role: str | None = None, user_tenant: Tenant | None = None) -> APIClient:
        client = APIClient()
        if role is None:
            return client
        target_tenant = user_tenant or tenant
        user = UserFactory()
        ProjectRole.objects.create(user=user, tenant=target_tenant, role=role)
        client.force_authenticate(user=user)
        client.defaults["HTTP_X_TENANT_ID"] = str(target_tenant.pk)
        return client

    return _make


@pytest.fixture
def admin_client(api_client_as):
    return api_client_as(role=Role.ADMIN)


@pytest.fixture
def pm_client(api_client_as):
    return api_client_as(role=Role.PM)


@pytest.fixture
def finance_client(api_client_as):
    return api_client_as(role=Role.FINANCE)


@pytest.fixture
def employee_client(api_client_as):
    return api_client_as(role=Role.EMPLOYEE)


@pytest.fixture
def director_client(api_client_as):
    return api_client_as(role=Role.PROJECT_DIRECTOR)


@pytest.fixture
def anonymous_client() -> APIClient:
    return APIClient()


@pytest.fixture
def other_tenant_admin_client(api_client_as, other_tenant):
    """Admin of a different tenant — used to verify cross-tenant isolation."""
    return api_client_as(role=Role.ADMIN, user_tenant=other_tenant)
