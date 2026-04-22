"""Planning URL routes."""

from rest_framework.routers import DefaultRouter

from .views import (
    AvailabilityViewSet,
    GanttViewSet,
    MilestoneViewSet,
    PhaseDependencyViewSet,
    PlanningStandardViewSet,
    ResourceAllocationViewSet,
    VirtualResourceViewSet,
)

router = DefaultRouter()
router.register(r"allocations", ResourceAllocationViewSet, basename="allocation")
router.register(r"milestones", MilestoneViewSet, basename="milestone")
router.register(r"availability", AvailabilityViewSet, basename="availability")
router.register(r"phase_dependencies", PhaseDependencyViewSet, basename="phase-dependency")
router.register(r"gantt", GanttViewSet, basename="gantt")
router.register(r"planning-standards", PlanningStandardViewSet, basename="planning-standard")
router.register(r"virtual-resources", VirtualResourceViewSet, basename="virtual-resource")

urlpatterns = router.urls
