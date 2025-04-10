"""
Tests for machine learning visualization.
"""

import os
from ml_client import visualize_stations

def test_visualize_stations_creates_image(tmp_path):
    user_loc = {"latitude": 40.7, "longitude": -74.0}
    stations = [
        {"latitude": 40.705, "longitude": -74.01, "station_name": "ENGINE 1"},
        {"latitude": 40.71, "longitude": -74.02, "station_name": "LADDER 2"},
    ]
    img_path = visualize_stations(user_loc, stations, radius_km=2, image_name="test.png", output_dir=tmp_path)
    assert os.path.exists(img_path)