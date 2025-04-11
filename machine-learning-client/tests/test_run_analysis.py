"""
Unit tests for run_analysis.
"""

from unittest.mock import patch
from ml_client import run_analysis


@patch("ml_client.db")
@patch("ml_client.save_travel_times")
@patch("ml_client.query_travel_times")
@patch("ml_client.load_station_data")
def test_run_analysis(mock_load_data, mock_query_times, mock_save, mock_db):
    """
    Tests that run_analysis can process a request using mocked dependencies.
    """
    mock_db.Request.find_one.return_value = {
        "location": {"latitude": 40.7, "longitude": -74.0}
    }

    mock_station = {
        "latitude": 585000,
        "longitude": 4500000,
        "station_name": "ENGINE 1",
        "functionalities": ["pumper"],
    }
    mock_load_data.return_value = [mock_station]

    mock_query_times.return_value = [
        {
            "destination": "50 W 4th St",
            "lat": 40.7,
            "lon": -74.0,
            "distance": 1000,
            "distance_text": "1 km",
            "duration": 300,
            "duration_text": "5 mins",
        }
    ]

    mock_save.return_value = ["mockid123"]
    mock_db.Result.find_one.return_value = {"urgency": "Quick"}

    result = run_analysis("0123456789abcdef01234567")
    assert result["id"] == "0123456789abcdef01234567"
    assert "nearby_stations" in result
    assert "travel_times" in result
