"""Consortium serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import Consortium, ConsortiumMember


class ConsortiumMemberSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(read_only=True)
    organization_name = serializers.CharField(
        source="organization.name", read_only=True, default=""
    )

    class Meta:
        model = ConsortiumMember
        fields = [
            "id", "consortium", "organization", "organization_name",
            "is_pr", "name_override", "display_name",
            "coefficient", "contact_name", "contact_email", "specialty",
        ]
        read_only_fields = ["id", "consortium", "display_name", "organization_name"]


class ConsortiumSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    members = ConsortiumMemberSerializer(many=True, read_only=True)
    client_name = serializers.CharField(
        source="client.name", read_only=True, default=""
    )
    total_coefficient = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True
    )
    projects_count = serializers.SerializerMethodField()

    class Meta:
        model = Consortium
        fields = [
            "id", "name", "client", "client_name",
            "pr_role", "contract_reference", "status", "description",
            "total_coefficient", "projects_count",
            "members", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "total_coefficient", "projects_count",
            "created_at", "updated_at",
        ]

    def get_projects_count(self, obj):
        return obj.projects.count()


class ConsortiumListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(
        source="client.name", read_only=True, default=""
    )
    members_count = serializers.SerializerMethodField()
    total_coefficient = serializers.DecimalField(
        max_digits=5, decimal_places=2, read_only=True
    )

    class Meta:
        model = Consortium
        fields = [
            "id", "name", "client", "client_name",
            "pr_role", "status", "contract_reference",
            "members_count", "total_coefficient",
            "created_at",
        ]

    def get_members_count(self, obj):
        return obj.members.count()
