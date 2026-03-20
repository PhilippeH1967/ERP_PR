"""Core admin registrations."""

from django.contrib import admin

from .models import Delegation, ProjectRole, Tenant, UserTenantAssociation


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
