"""Billing URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CreditNoteViewSet,
    HoldbackViewSet,
    InvoiceLineViewSet,
    InvoiceTemplateViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    WriteOffViewSet,
)

router = DefaultRouter()
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"credit_notes", CreditNoteViewSet, basename="credit-note")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"holdbacks", HoldbackViewSet, basename="holdback")
router.register(r"write_offs", WriteOffViewSet, basename="write-off")
router.register(r"invoice_templates", InvoiceTemplateViewSet, basename="invoice-template")

line_router = DefaultRouter()
line_router.register(r"lines", InvoiceLineViewSet, basename="invoice-line")

urlpatterns = [
    path("", include(router.urls)),
    path("invoices/<int:invoice_pk>/", include(line_router.urls)),
]
