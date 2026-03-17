"""Shared pytest fixtures for the ERP project."""

import os

import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")


@pytest.fixture
def api_client():
    """Return a DRF API test client."""
    from rest_framework.test import APIClient

    return APIClient()
