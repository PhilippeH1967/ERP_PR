"""Supplier URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExternalOrganizationViewSet

router = DefaultRouter()
router.register(r"external_organizations", ExternalOrganizationViewSet, basename="external-org")

urlpatterns = [
    path("", include(router.urls)),
]
