"""Data operations URL configuration."""

from django.urls import path

from .views import download_template, list_import_types, upload_import

urlpatterns = [
    path("imports/", list_import_types, name="import-types"),
    path("imports/<str:import_key>/template/", download_template, name="import-template"),
    path("imports/<str:import_key>/upload/", upload_import, name="import-upload"),
]
