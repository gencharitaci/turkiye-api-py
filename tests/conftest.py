"""
Pytest configuration and shared fixtures for testing.

This module provides common test fixtures and configuration
used across all test modules.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.data_loader import DataLoader


@pytest.fixture
def client():
    """
    FastAPI test client fixture.

    Returns:
        TestClient: Test client for making HTTP requests to the API
    """
    return TestClient(app)


@pytest.fixture
def data_loader():
    """
    DataLoader singleton instance fixture.

    Returns:
        DataLoader: Singleton data loader instance
    """
    return DataLoader()


@pytest.fixture
def sample_province():
    """
    Sample province data for testing.

    Returns:
        dict: Sample province dictionary
    """
    return {
        "id": 1,
        "name": "Adana",
        "population": 2258718,
        "area": 13844,
        "altitude": 20,
        "isCoastal": True,
        "isMetropolitan": True,
    }


@pytest.fixture
def sample_district():
    """
    Sample district data for testing.

    Returns:
        dict: Sample district dictionary
    """
    return {"id": 1, "provinceId": 1, "province": "Adana", "name": "Aladağ", "population": 16240, "area": 1542}


@pytest.fixture
def sample_neighborhood():
    """
    Sample neighborhood data for testing.

    Returns:
        dict: Sample neighborhood dictionary
    """
    return {
        "id": 1,
        "districtId": 1,
        "provinceId": 1,
        "district": "Aladağ",
        "province": "Adana",
        "name": "Akören",
        "population": 752,
    }
