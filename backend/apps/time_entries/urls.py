"""Time entries URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PeriodUnlockViewSet,
    TimeEntryViewSet,
    TimesheetLockViewSet,
    WeeklyApprovalViewSet,
)

router = DefaultRouter()
router.register(r"time_entries", TimeEntryViewSet, basename="time-entry")
router.register(r"weekly_approvals", WeeklyApprovalViewSet, basename="weekly-approval")
router.register(r"timesheet_locks", TimesheetLockViewSet, basename="timesheet-lock")
router.register(r"period_unlocks", PeriodUnlockViewSet, basename="period-unlock")

urlpatterns = [
    path("", include(router.urls)),
]
