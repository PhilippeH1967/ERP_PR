"""Core admin registrations."""

from django.contrib import admin

from .models import BusinessUnit, Delegation, LaborRule, PositionProfile, ProjectRole, TaxConfiguration, TaxRate, TaxScheme, Tenant, UserTenantAssociation


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sso_only", "created_at")
    list_filter = ("is_active", "sso_only")
    search_fields = ("name", "slug")
    list_editable = ("sso_only",)


@admin.register(ProjectRole)
class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "project_id", "tenant")
    list_filter = ("role", "tenant")
    search_fields = ("user__username", "user__email")


@admin.register(UserTenantAssociation)
class UserTenantAssociationAdmin(admin.ModelAdmin):
    list_display = ("user", "tenant", "created_at")
    search_fields = ("user__username",)


@admin.register(Delegation)
class DelegationAdmin(admin.ModelAdmin):
    list_display = ("delegator", "delegate", "scope", "start_date", "end_date", "is_active")
    list_filter = ("scope", "is_active")
    search_fields = ("delegator__username", "delegate__username")


@admin.register(BusinessUnit)
class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "director", "is_active", "tenant")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


@admin.register(PositionProfile)
class PositionProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category", "hourly_cost_rate", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "code")


@admin.register(TaxConfiguration)
class TaxConfigurationAdmin(admin.ModelAdmin):
    list_display = ("legal_entity", "tps_rate", "tvq_rate", "is_active")
    list_editable = ("tps_rate", "tvq_rate")


class TaxRateInline(admin.TabularInline):
    model = TaxRate
    extra = 1


@admin.register(TaxScheme)
class TaxSchemeAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "is_default", "is_active")
    list_filter = ("is_default", "is_active")
    inlines = [TaxRateInline]


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ("scheme", "tax_type", "rate", "is_active")


@admin.register(LaborRule)
class LaborRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "weekly_hours", "daily_hours", "overtime_threshold_weekly", "is_active")
    list_editable = ("weekly_hours", "overtime_threshold_weekly")
