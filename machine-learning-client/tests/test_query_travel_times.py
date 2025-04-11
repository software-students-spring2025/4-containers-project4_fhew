"""
Unit tests for query_travel_time function.
"""

from unittest.mock import patch
from ml_client import query_travel_times


@patch("ml_client.requests.get")
def test_query_travel_times_success(mock_get):
    """
    Tests that query_travel_times correctly parses valid response.
    """
    mock_get.return_value.json.return_value = {
        "destination_addresses": ["50 W 4th St"],
        "rows": [
            {
                "elements": [
                    {
                        "status": "OK",
                        "distance": {"text": "2 km", "value": 2000},
                        "duration": {"text": "5 mins", "value": 300},
                    }
                ]
            }
        ],
    }

    user_lat, user_lon = 40, -74
    destinations = [{"latitude": 40.1, "longitude": -70.1}]
    result = query_travel_times(user_lat, user_lon, destinations)

    assert isinstance(result, list)
    assert result[0]["duration"] == 300
    assert result[0]["distance"] == 2000
    assert result[0]["destination"] == "50 W 4th St"
