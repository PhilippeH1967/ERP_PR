"""Supplier URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExternalOrganizationViewSet, STInvoiceViewSet

router = DefaultRouter()
router.register(r"external_organizations", ExternalOrganizationViewSet, basename="external-org")
router.register(r"st_invoices", STInvoiceViewSet, basename="st-invoice")

urlpatterns = [
    path("", include(router.urls)),
]
