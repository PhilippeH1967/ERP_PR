"""Tests for custom exception handler and response format."""

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestExceptionHandler:
    """Tests for the custom DRF exception handler."""

    def test_api_root_returns_json_success(self):
        """Verify that DRF views return JSON wrapped responses."""
        client = APIClient()
        response = client.get("/api/v1/", format="json")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "data" in data

    def test_method_not_allowed_returns_error_format(self):
        """Verify DRF error responses use standardized error format."""
        client = APIClient()
        response = client.post("/api/v1/", data={}, format="json")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        data = response.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert "details" in data["error"]
