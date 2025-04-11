"""
Tests for the find near by stations
"""

from ml_client import find_near_by_stations


def test_find_near_by_stations_within_radius():
    """
    Tests that only fire stations within the appropriate radius are returned.
    """
    stations = [
        {"latitude": 585000, "longitude": 4500000, "functionalities": ["ladder"]},
        {"latitude": 300000, "longitude": 4000000, "functionalities": ["pumper"]},
    ]

    user_lat = 40.644
    user_lon = -73.944

    result = find_near_by_stations(user_lat, user_lon, stations, radius_km=5)
    assert len(result) == 1
    assert result[0]["functionalities"] == ["ladder"]
