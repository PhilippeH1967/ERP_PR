from django.contrib import admin

from .models import PlanningStandard


@admin.register(PlanningStandard)
class PlanningStandardAdmin(admin.ModelAdmin):
    list_display = ("name", "phase_code", "time_unit", "is_active", "tenant")
    list_filter = ("phase_code", "time_unit", "is_active", "tenant")
    search_fields = ("name", "description", "phase_code")
