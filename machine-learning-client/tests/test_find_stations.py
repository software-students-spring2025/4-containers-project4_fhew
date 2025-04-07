"""Tests for the find near by stations"""

def test_extracting_coordinates():
    "Test 1.0: Verify the coordinates are numbers and valid values"
    pass

def test_station_types_parameter():
    "Test 1.1: Verify that classifying the station type is correct"
    pass

def test_basic_counting():
    "Test 1.2: Verify that correct number of fire stations are counted"
    pass

def test_find_near_by_stations_within_radius():
    stations = [
        {"latitude": 40.5410, "longitude": -74.1510, "functionalities": ["ladder"]},
        {"latitude": 41.0000, "longitude": -75.0000, "functionalities": ["pumper"]}
    ]
    result = find_near_by_stations(40.5412, -74.1515, stations, radius_km=5)
    assert len(result) == 1
    assert result[0]["functionalities"] == ["ladder"]