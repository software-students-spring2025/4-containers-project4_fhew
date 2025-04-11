"""
Tests for the Machine Learning risk analysis
"""

from ml_client import haversine_distance


def test_haversine_zero_distance():
    """
    Tests that the haversine distance between the same coords is zero.
    """
    assert haversine_distance(40.7, -74.0, 40.7, -74.0) == 0.0


def test_haversine_known_distance():
    """
    Tests that haversine distance between two known points is within an appropriate range.
    """
    # Manhattan to Brooklyn (approx 8-10 km)
    d = haversine_distance(40.7831, -73.9712, 40.6782, -73.9442)
    assert 8 <= d <= 12
