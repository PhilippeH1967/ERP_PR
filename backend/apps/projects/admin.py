from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Amendment, FinancialPhase, Phase, Project, ProjectTemplate, SupportService, WBSElement


class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 0
    fields = ("name", "client_facing_label", "phase_type", "billing_mode", "budgeted_hours", "is_locked")


@admin.register(Project)
class ProjectAdmin(SimpleHistoryAdmin):
    list_display = ("code", "name", "client", "contract_type", "status", "pm", "tenant", "created_at")
    list_filter = ("status", "contract_type", "is_internal", "tenant")
    search_fields = ("code", "name", "client__name")
    list_editable = ("status",)
    inlines = [PhaseInline]
    list_per_page = 25


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "phase_type", "billing_mode", "budgeted_hours", "is_locked")
    list_filter = ("phase_type", "billing_mode", "is_locked")
    search_fields = ("name", "project__code")


@admin.register(WBSElement)
class WBSElementAdmin(admin.ModelAdmin):
    list_display = ("standard_label", "client_facing_label", "project", "element_type", "budgeted_hours")
    list_filter = ("element_type",)
    search_fields = ("standard_label", "client_facing_label")


@admin.register(ProjectTemplate)
class ProjectTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "contract_type", "is_active", "tenant")
    list_filter = ("contract_type", "is_active")


@admin.register(SupportService)
class SupportServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "billing_mode", "budgeted_hours")


@admin.register(Amendment)
class AmendmentAdmin(admin.ModelAdmin):
    list_display = ("project", "amendment_number", "description", "status", "budget_impact", "created_at")
    list_filter = ("status",)


@admin.register(FinancialPhase)
class FinancialPhaseAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "billing_mode")
