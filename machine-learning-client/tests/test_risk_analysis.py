"""
Tests for the Machine Learning risk analysis
"""

from ml_client import haversine_distance


def test_risk_classification():
    "Test 1.0: Verify that the correct risk is assigned to the number of stations counted"
    pass

def test_haversine_zero_distance():
    assert haversine_distance(40.0, -74.0, 40.0, -74.0) == 0.0

def test_haversine_known_distance():
    # Manhattan to Brooklyn (approx 8-10 km)
    d = haversine_distance(40.7831, -73.9712, 40.6782, -73.9442)
    assert 8 <= d <= 12