"""
Setting up the test client.
"""

import pytest
from app import app

@pytest.fixture
def test_client():
    """
    Fixture to create test client for Flask.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
