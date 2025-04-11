"""
Unit test file for analyze_route method
"""

import pytest
from unittest.mock import patch, MagicMock
from ml_client import app


@pytest.fixture
def test_client():
    """
    Fixture to create test client for Flask.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_analyze(test_client):
    """
    Tests that /analyze route triggers analysis and returns correct response.
    """
    with patch("ml_client.run_analysis") as mock_run_analysis, patch(
        "ml_client.visualize_stations"
    ) as mock_visualize, patch("ml_client.reqDB.find_one") as mock_find_one:

        mock_run_analysis.return_value = {
            "id": "123",
            "nearby_stations": [],
            "travel_times": [],
        }
        mock_val = MagicMock()
        mock_val.location = {"latitude": 40.7, "longitude": -74.0}
        mock_find_one.return_value = mock_val

        response = test_client.post("/analyze", json={"reqID": "123"})

        assert response.status_code == 200
        assert response.json["id"] == "123"
