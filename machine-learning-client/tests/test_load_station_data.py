"""
Unit tests for load_station_data.
"""

import pandas as pd
import tempfile
import os
from ml_client import load_station_data


def test_load_station_data():
    """
    Tests that the csv data is appropriately loaded into the program.
    """
    with tempfile.NamedTemporaryFile(
        mode="w+", delete=False, suffix=".csv"
    ) as temp_csv:
        temp_csv.write("Station Name,x,y\n")
        temp_csv.write("LADDER 1, 585000, 450000\n")
        temp_csv.write("RESCUE 2, 586000, 450100\n")
        temp_csv.write("ENGINE 3, 587000, 450200\n")
        temp_csv_path = temp_csv.name

    stations = load_station_data(temp_csv_path)
    os.unlink(temp_csv_path)

    assert len(stations) == 3
    assert "ladder" in stations[0]["functionalities"]
    assert "rescue" in stations[1]["functionalities"]
    assert "pumper" in stations[2]["functionalities"]
