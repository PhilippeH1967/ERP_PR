"""Tests for custom DRF renderers."""

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestWrappedJSONRenderer:
    """Tests for the WrappedJSONRenderer."""

    def test_success_response_wrapped_in_data(self):
        client = APIClient()
        response = client.get("/api/v1/")
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], dict)

    def test_already_wrapped_response_not_double_wrapped(self):
        client = APIClient()
        response = client.get("/api/v1/")
        data = response.json()
        # Should not have nested {"data": {"data": ...}}
        assert "data" not in data.get("data", {}) or data["data"].get("data") is None
