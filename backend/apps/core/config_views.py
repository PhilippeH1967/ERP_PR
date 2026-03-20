"""Admin configuration CRUD viewsets (FR78, FR83)."""

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import BusinessUnit, LaborRule, PositionProfile, TaxConfiguration, TaxRate, TaxScheme
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
    """DEPRECATED — kept for backward compatibility."""
    class Meta:
        model = TaxConfiguration
        fields = ["id", "legal_entity", "tps_rate", "tvq_rate", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = ["id", "tax_type", "label", "rate", "is_active"]
        read_only_fields = ["id"]


class TaxSchemeSerializer(serializers.ModelSerializer):
    rates = TaxRateSerializer(many=True, read_only=True)

    class Meta:
        model = TaxScheme
        fields = ["id", "name", "province", "description", "is_default", "is_active", "rates", "created_at"]
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
    """DEPRECATED — use TaxSchemeViewSet."""
    serializer_class = TaxConfigurationSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = TaxConfiguration.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class TaxSchemeViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = TaxSchemeSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = TaxScheme.objects.prefetch_related("rates").all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs


class TaxRateViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = TaxRateSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = TaxRate.objects.all()
        scheme_id = self.kwargs.get("scheme_pk")
        if scheme_id:
            qs = qs.filter(scheme_id=scheme_id)
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs

    def perform_create(self, serializer):
        scheme = TaxScheme.objects.get(pk=self.kwargs["scheme_pk"])
        serializer.save(scheme=scheme, tenant=scheme.tenant)


class LaborRuleViewSet(_TenantCreateMixin, viewsets.ModelViewSet):
    serializer_class = LaborRuleSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        qs = LaborRule.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs
