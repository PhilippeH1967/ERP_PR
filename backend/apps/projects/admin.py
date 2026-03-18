from django.contrib import admin

from .models import (
    Amendment,
    EmployeeAssignment,
    FinancialPhase,
    Phase,
    Project,
    ProjectTemplate,
    SupportService,
    WBSElement,
)

admin.site.register(Project)
admin.site.register(Phase)
admin.site.register(WBSElement)
admin.site.register(ProjectTemplate)
admin.site.register(SupportService)
admin.site.register(Amendment)
admin.site.register(FinancialPhase)
admin.site.register(EmployeeAssignment)
