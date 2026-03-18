"""Dashboard URL configuration."""

from django.urls import path

from .views import pm_financial_kpis, role_dashboard, system_health

urlpatterns = [
    path("dashboard/", role_dashboard, name="role-dashboard"),
    path("dashboard/pm-kpis/", pm_financial_kpis, name="pm-kpis"),
    path("dashboard/system-health/", system_health, name="system-health"),
]
