"""Project URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AmendmentViewSet,
    PhaseViewSet,
    ProjectTemplateViewSet,
    ProjectViewSet,
    TaskViewSet,
    WBSElementViewSet,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"project_templates", ProjectTemplateViewSet, basename="project-template")

# Nested routes
phase_router = DefaultRouter()
phase_router.register(r"phases", PhaseViewSet, basename="project-phase")

wbs_router = DefaultRouter()
wbs_router.register(r"wbs", WBSElementViewSet, basename="project-wbs")

amendment_router = DefaultRouter()
amendment_router.register(r"amendments", AmendmentViewSet, basename="project-amendment")

task_router = DefaultRouter()
task_router.register(r"tasks", TaskViewSet, basename="project-task")

urlpatterns = [
    path("", include(router.urls)),
    path("projects/<int:project_pk>/", include(phase_router.urls)),
    path("projects/<int:project_pk>/", include(wbs_router.urls)),
    path("projects/<int:project_pk>/", include(amendment_router.urls)),
    path("projects/<int:project_pk>/", include(task_router.urls)),
]
