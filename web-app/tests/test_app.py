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

@patch("app.db.gps_input.insert_one")
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

@patch("app.db.results.find")
def test_show_results(mock_find, client):
    """
    Test that show-results page displays mocked emergency services.
    """
    print("MOCK FIND CALLED")
    mock_find.return_value = [
        {"name": "Hospital", "distance": 1.2, "eta": 30},
        {"name": "Police Station", "distance": 0.8, "eta": 15}
    ]
    response = client.get("/show-results")
    assert response.status_code == 200
    assert b"Hospital" in response.data or b"Police Station" in response.data
