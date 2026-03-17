"""Tests for core API views."""

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestApiRoot:
    """Tests for the API root endpoint."""

    def test_api_root_returns_200(self):
        client = APIClient()
        response = client.get("/api/v1/")
        assert response.status_code == 200

    def test_api_root_returns_wrapped_response(self):
        client = APIClient()
        response = client.get("/api/v1/")
        data = response.json()
        assert "data" in data
        assert data["data"]["status"] == "ok"
        assert data["data"]["name"] == "ERP API"
        assert data["data"]["version"] == "1.0.0"
