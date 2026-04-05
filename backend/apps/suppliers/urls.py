"""Supplier URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ExternalOrganizationViewSet,
    STCreditNoteViewSet,
    STDisputeViewSet,
    STHoldbackViewSet,
    STInvoiceViewSet,
    STPaymentViewSet,
)

router = DefaultRouter()
router.register(r"external_organizations", ExternalOrganizationViewSet, basename="external-org")
router.register(r"st_invoices", STInvoiceViewSet, basename="st-invoice")
router.register(r"st_payments", STPaymentViewSet, basename="st-payment")
router.register(r"st_credit_notes", STCreditNoteViewSet, basename="st-credit-note")
router.register(r"st_disputes", STDisputeViewSet, basename="st-dispute")
router.register(r"st_holdbacks", STHoldbackViewSet, basename="st-holdback")

urlpatterns = [
    path("", include(router.urls)),
]
