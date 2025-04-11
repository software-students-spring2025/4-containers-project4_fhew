"""
Tests for save_travel_times
"""

from unittest.mock import patch, MagicMock
from ml_client import save_travel_times


@patch("ml_client.db")
def test_save_travel_times(mock_db):
    """
    Tests that save_travel_time correctly formats data into the database
    and correctly returns the id of the inserted data.
    """
    mock_inserted = MagicMock()
    mock_inserted.inserted_id = "mockid123"
    mock_db.Result.insert_one.return_value = mock_inserted

    mock_response = [
        {
            "destination": "50 W 4th St",
            "lat": 40.7,
            "lon": -74.0,
            "distance": 5000,
            "distance_text": "5 km",
            "duration": 300,
            "duration_text": "5 mins",
        }
    ]

    result = save_travel_times(mock_response)
    assert result == ["mockid123"]
    mock_db.Result.insert_one.assert_called_once()
