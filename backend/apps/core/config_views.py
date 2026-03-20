"""Admin configuration CRUD viewsets (FR78, FR83)."""

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import BusinessUnit, LaborRule, PositionProfile, TaxConfiguration
from .permissions import IsAdmin


class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = ["id", "name", "code", "director", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class PositionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionProfile
        fields = ["id", "name", "code", "category", "hourly_cost_rate", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaxConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxConfiguration
        fields = ["id", "legal_entity", "tps_rate", "tvq_rate", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class LaborRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaborRule
        fields = [
            "id", "name", "weekly_hours", "daily_hours",
            "overtime_threshold_weekly", "overtime_threshold_daily",
            "statutory_holidays", "rest_days", "is_active", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class _TenantCreateMixin:
    """Mixin to auto-assign tenant on create."""

    def perform_create(self, serializer):
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            from .models import Tenant
            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            from .models import Tenant
            serializer.save(tenant=Tenant.objects.first())


class BusinessUnitViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = BusinessUnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = BusinessUnit.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class PositionProfileViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = PositionProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = PositionProfile.objects.filter(is_active=True)
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class TaxConfigurationViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = TaxConfigurationSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = TaxConfiguration.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class LaborRuleViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = LaborRuleSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = LaborRule.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs
