"""
Setting up the test client.
"""

import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture to create test client for Flask.
    """
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
