"""Client URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientAddressViewSet, ClientViewSet, ContactViewSet

router = DefaultRouter()
router.register(r"clients", ClientViewSet, basename="client")

# Nested routes for contacts and addresses
client_contacts = DefaultRouter()
client_contacts.register(r"contacts", ContactViewSet, basename="client-contact")

client_addresses = DefaultRouter()
client_addresses.register(r"addresses", ClientAddressViewSet, basename="client-address")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "clients/<int:client_pk>/",
        include(client_contacts.urls),
    ),
    path(
        "clients/<int:client_pk>/",
        include(client_addresses.urls),
    ),
]
