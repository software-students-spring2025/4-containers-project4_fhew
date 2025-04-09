# web-app/tests/test_app.py

from unittest.mock import patch, MagicMock
from app import app

def test_home_route(client):
    """
    Test that the home route renders the home page.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html" in response.data

@patch("app.db.locations.insert_one")
def test_find_location(mock_insert, client):
    """
    Test that a POST request to /find-location inserts data into the database and returns success.
    """
    print("MOCK INSERT CALLED")
    data = {"latitude": 40.0, "longitude": -70.0}
    mock_insert.return_value = MagicMock()
    
    response = client.post("/find-location", json=data)
    assert response.status_code == 200
    assert response.json == {"message": "Location found"}
    mock_insert.assert_called_once_with(data)

@patch("app.db")
def test_show_results(mock_find, client):
    """
    Test that show-results page displays mocked emergency services.
    """
    print("MOCK FIND CALLED")
    mock_find.analysis.find_one.return_value = mock_db.analysis.find_one.return_value = {
        "risk_level": "low risk",
        "nearby_stations": [
            {"station_name": "Hospital", "distance": 1.2, "functionalities": ["rescue"]},
            {"station_name": "Police Station", "distance": 0.8, "functionalities": ["law"]}
        ]
    }
    response = client.get("/show-results")
    assert response.status_code == 200
    assert b"Hospital" in response.data or b"Police Station" in response.data
