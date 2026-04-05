"""Leave URL routes."""

from rest_framework.routers import DefaultRouter

from .views import LeaveBankViewSet, LeaveRequestViewSet, LeaveTypeViewSet, PublicHolidayViewSet

router = DefaultRouter()
router.register(r"leave_types", LeaveTypeViewSet, basename="leave-type")
router.register(r"leave_banks", LeaveBankViewSet, basename="leave-bank")
router.register(r"leave_requests", LeaveRequestViewSet, basename="leave-request")
router.register(r"public_holidays", PublicHolidayViewSet, basename="public-holiday")

urlpatterns = router.urls
