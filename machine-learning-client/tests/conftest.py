"""Test fixtures and utilities for other tests."""

import pytest
from ml_client import app


@pytest.fixture
def test_client():
    """
    Fixture to create test client for Flask.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary DB dir for access test"""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir
