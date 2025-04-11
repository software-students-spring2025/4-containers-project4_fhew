"""
Testing app.py
"""

from unittest.mock import patch, MagicMock


def test_home_route(test_client):
    """
    Test that the home route renders the home page.
    """
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html" in response.data


@patch("app.requests.post")
@patch("app.db")
def test_find_location(mock_insert, mock_post, test_client):
    """
    Test that a POST request to /find-location inserts data into the database and returns success.
    """
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "mockid123"
    mock_insert.Request.insert_one.return_value = mock_insert_result
    mock_post.return_value.status_code = 200

    data = {"lat": 40.0, "long": -70.0}
    response = test_client.post("/find-location", json=data)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["message"] == "Location saved"
    assert json_data["id"] == "mockid123"
    mock_post.assert_called_once()


@patch("app.db")
def test_show_results(mock_find, test_client):
    """
    Test that show-results page displays mocked emergency services.
    """
    mock_find.Request.find_one.return_value = {
        "location": {"latitude": 40.0, "longitude": -70.0},
        "resultIDs": [],
        "risk": "Low",
        "Timestamp": "2024-04-01T12:00:00",
        "ReqType": "location_capture",
    }

    # ObjectID is a 24 char string
    response = test_client.get("/show-results/0123456789abcdef01234567")
    assert response.status_code == 200
    assert b"Nearby Emergency Services" in response.data


@patch("app.db")
def test_show_map(mock_map, test_client):
    """
    Test that the /map route renders correctly.
    """
    mock_map.Request.find_one.return_value = {
        "_id": "0123456789abcdef01234567",
        "resultIDs": ["station1", "station2"],
    }

    mock_map.Result.find_one.side_effect = [
        {"name": "Fire Station 1", "travel_time": "3"},
        {"name": "Fire Station 2", "travel_time": "5"},
    ]

    response = test_client.get("/map/0123456789abcdef01234567")
    assert response.status_code == 200
    assert b"Fire Station 1" in response.data or b"Fire Station 2" in response.data
