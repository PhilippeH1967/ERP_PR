from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import PeriodUnlock, TimeEntry, TimesheetLock, WeeklyApproval


@admin.register(TimeEntry)
class TimeEntryAdmin(SimpleHistoryAdmin):
    list_display = ("employee", "project", "phase", "date", "hours", "status")
    list_filter = ("status", "date", "project")
    search_fields = ("employee__username", "project__code")
    date_hierarchy = "date"
    list_per_page = 50


@admin.register(WeeklyApproval)
class WeeklyApprovalAdmin(admin.ModelAdmin):
    list_display = ("employee", "week_start", "pm_status", "finance_status", "tenant")
    list_filter = ("pm_status", "finance_status")
    search_fields = ("employee__username",)


@admin.register(TimesheetLock)
class TimesheetLockAdmin(admin.ModelAdmin):
    list_display = ("phase", "person", "locked_by", "created_at")


@admin.register(PeriodUnlock)
class PeriodUnlockAdmin(admin.ModelAdmin):
    list_display = ("period_start", "period_end", "reason", "unlocked_by")
