"""Tests for dashboard KPI endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestDashboardEndpoints:
    def setup_method(self):
        self.user = User.objects.create_user(username="dash_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_role_dashboard_requires_auth(self):
        client = APIClient()
        response = client.get("/api/v1/dashboard/")
        assert response.status_code == 401

    def test_role_dashboard_authenticated(self):
        response = self.api.get("/api/v1/dashboard/")
        assert response.status_code == 200

    def test_pm_kpis(self):
        response = self.api.get("/api/v1/dashboard/pm-kpis/")
        assert response.status_code == 200

    def test_system_health(self):
        response = self.api.get("/api/v1/dashboard/system-health/")
        assert response.status_code == 200
