"""Tests for expense API endpoints."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from apps.core.models import Tenant


@pytest.mark.django_db
class TestExpenseReportAPI:
    def setup_method(self):
        self.tenant = Tenant.objects.create(name="T", slug="exp-api")
        self.user = User.objects.create_user(username="exp_user", password="pass123!")
        self.api = APIClient()
        self.api.force_authenticate(user=self.user)

    def test_list_reports(self):
        response = self.api.get("/api/v1/expense_reports/")
        assert response.status_code == 200

    def test_create_report(self):
        response = self.api.post(
            "/api/v1/expense_reports/",
            {"total_amount": "150.00"},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201

    def test_list_categories(self):
        response = self.api.get("/api/v1/expense_categories/")
        assert response.status_code == 200

    def test_create_category(self):
        response = self.api.post(
            "/api/v1/expense_categories/",
            {"name": "Transport", "requires_receipt": True},
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant.pk),
        )
        assert response.status_code == 201
