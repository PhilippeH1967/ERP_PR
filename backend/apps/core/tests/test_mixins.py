"""Tests for OptimisticLockMixin."""

import pytest
from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin, VersionConflictError
from apps.core.models import SampleTenantModel, Tenant


class SampleSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = SampleTenantModel
        fields = ["id", "name", "version"]


@pytest.mark.django_db
class TestOptimisticLockMixin:
    """Tests for version conflict detection in serializer updates."""

    def setup_method(self):
        self.tenant = Tenant.objects.create(name="Test", slug="test-lock")
        self.obj = SampleTenantModel.objects.create(
            tenant=self.tenant, name="Original"
        )

    def test_update_with_matching_version_succeeds(self):
        serializer = SampleSerializer(
            self.obj,
            data={"name": "Updated", "version": 1},
            partial=True,
            context={"if_match_version": "1"},
        )
        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "Updated"
        assert updated.version == 2  # Version incremented after save

    def test_update_with_mismatching_version_raises_409(self):
        serializer = SampleSerializer(
            self.obj,
            data={"name": "Conflict"},
            partial=True,
            context={"if_match_version": "99"},
        )
        assert serializer.is_valid()
        with pytest.raises(VersionConflictError) as exc_info:
            serializer.save()
        assert exc_info.value.status_code == 409

    def test_update_without_version_proceeds(self):
        """Updates without If-Match header should proceed (backward compat)."""
        serializer = SampleSerializer(
            self.obj,
            data={"name": "No Version Check"},
            partial=True,
            context={},
        )
        assert serializer.is_valid()
        updated = serializer.save()
        assert updated.name == "No Version Check"

    def test_version_conflict_error_attributes(self):
        err = VersionConflictError()
        assert err.status_code == 409
        assert err.default_code == "VERSION_CONFLICT"
