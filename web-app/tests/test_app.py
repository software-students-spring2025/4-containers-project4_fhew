"""
Testing app.py at 83% coverage.
"""
from unittest.mock import patch, MagicMock

def test_home_route(client):
    """
    Test that the home route renders the home page.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html" in response.data

@patch("app.db")
def test_find_location(mock_insert, client):
    """
    Test that a POST request to /find-location inserts data into the database and returns success.
    """
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "mockid123"
    mock_insert.Request.insert_one.return_value = mock_insert_result

    data = {"lat": 40.0, "long": -70.0}
    response = client.post("/find-location", json=data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Location saved"
    assert json_data["id"] == "mockid123"

@patch("app.db")
def test_show_results(mock_find, client):
    """
    Test that show-results page displays mocked emergency services.
    """
    mock_find.Request.find_one.return_value = {
        "location": {"latitude": 40.0, "longitude": -70.0},
        "resultIDs": [],
        "Timestamp": "2024-04-01T12:00:00",
        "ReqType": "location_capture"
    }

    #ObjectID is a 24 char string
    response = client.get("/show-results/0123456789abcdef01234567")
    assert response.status_code == 200
    assert b"Nearby Emergency Services" in response.data
