"""Data operations URL configuration."""

from django.urls import path

from .db_dump import db_dump
from .views import download_template, export_csv, list_import_types, upload_import

urlpatterns = [
    path("imports/", list_import_types, name="import-types"),
    path("imports/<str:import_key>/template/", download_template, name="import-template"),
    path("imports/<str:import_key>/upload/", upload_import, name="import-upload"),
    # Intacct Phase 1 — CSV exports
    path("exports/<str:export_type>/", export_csv, name="export-csv"),
    # Admin DB dump (wraps pg_dump) — support / debug download
    path("admin/db-dump/", db_dump, name="admin-db-dump"),
]
