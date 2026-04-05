"""Planning URL routes."""

from rest_framework.routers import DefaultRouter

from .views import AvailabilityViewSet, MilestoneViewSet, ResourceAllocationViewSet

router = DefaultRouter()
router.register(r"allocations", ResourceAllocationViewSet, basename="allocation")
router.register(r"milestones", MilestoneViewSet, basename="milestone")
router.register(r"availability", AvailabilityViewSet, basename="availability")

urlpatterns = router.urls
