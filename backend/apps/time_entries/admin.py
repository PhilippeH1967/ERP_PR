from django.contrib import admin

from .models import PeriodUnlock, TimeEntry, TimesheetLock, WeeklyApproval

admin.site.register(TimeEntry)
admin.site.register(WeeklyApproval)
admin.site.register(TimesheetLock)
admin.site.register(PeriodUnlock)
