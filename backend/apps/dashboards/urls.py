"""Dashboard URL configuration."""

from django.urls import path

from .views import bu_director_kpis, hours_report, pm_financial_kpis, role_dashboard, system_health

urlpatterns = [
    path("dashboard/", role_dashboard, name="role-dashboard"),
    path("dashboard/pm-kpis/", pm_financial_kpis, name="pm-kpis"),
    path("dashboard/bu-kpis/", bu_director_kpis, name="bu-kpis"),
    path("dashboard/system-health/", system_health, name="system-health"),
    path("dashboard/hours-report/", hours_report, name="hours-report"),
]
