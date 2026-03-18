"""Tests for core infrastructure models: Tenant, TenantScopedModel, VersionedModel."""

import pytest
from django.db import IntegrityError

from apps.core.models import SampleTenantModel, Tenant


@pytest.mark.django_db
class TestTenantModel:
    """Tests for the Tenant model."""

    def test_create_tenant(self):
        tenant = Tenant.objects.create(name="Provencher Roy", slug="provencher-roy")
        assert tenant.pk is not None
        assert tenant.name == "Provencher Roy"
        assert tenant.slug == "provencher-roy"
        assert tenant.is_active is True
        assert tenant.created_at is not None

    def test_tenant_slug_unique(self):
        Tenant.objects.create(name="Tenant A", slug="tenant-a")
        with pytest.raises(IntegrityError):
            Tenant.objects.create(name="Tenant B", slug="tenant-a")

    def test_tenant_str(self):
        tenant = Tenant(name="Test Tenant")
        assert str(tenant) == "Test Tenant"


@pytest.mark.django_db
class TestTenantScopedModel:
    """Tests for the TenantScopedModel abstract base."""

    def test_sample_model_has_tenant_fk(self):
        tenant = Tenant.objects.create(name="Test", slug="test")
        obj = SampleTenantModel.objects.create(tenant=tenant, name="Sample")
        assert obj.tenant_id == tenant.pk
        assert obj.created_at is not None
        assert obj.updated_at is not None

    def test_sample_model_cascade_delete(self):
        tenant = Tenant.objects.create(name="Test", slug="test-cascade")
        SampleTenantModel.objects.create(tenant=tenant, name="Will be deleted")
        assert SampleTenantModel.objects.count() == 1
        tenant.delete()
        assert SampleTenantModel.objects.count() == 0


@pytest.mark.django_db
class TestVersionedModel:
    """Tests for VersionedModel optimistic locking."""

    def test_initial_version_is_1(self):
        tenant = Tenant.objects.create(name="Test", slug="test-version")
        obj = SampleTenantModel.objects.create(tenant=tenant, name="V1")
        assert obj.version == 1

    def test_version_increments_on_save(self):
        tenant = Tenant.objects.create(name="Test", slug="test-version-inc")
        obj = SampleTenantModel.objects.create(tenant=tenant, name="V1")
        assert obj.version == 1

        obj.name = "V2"
        obj.save()
        assert obj.version == 2

        obj.name = "V3"
        obj.save()
        assert obj.version == 3

    def test_version_does_not_increment_on_create(self):
        tenant = Tenant.objects.create(name="Test", slug="test-version-create")
        obj = SampleTenantModel.objects.create(tenant=tenant, name="New")
        assert obj.version == 1

    def test_version_persists_in_db(self):
        tenant = Tenant.objects.create(name="Test", slug="test-version-db")
        obj = SampleTenantModel.objects.create(tenant=tenant, name="Test")
        obj.name = "Updated"
        obj.save()

        obj_from_db = SampleTenantModel.objects.get(pk=obj.pk)
        assert obj_from_db.version == 2
