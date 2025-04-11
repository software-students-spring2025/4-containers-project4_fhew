"""
Unit test for assign_response_time.
"""

from ml_client import assign_response_time


def test_assign_response_time():
    """
    Test that assign response time accurately classifies values.
    """
    assert assign_response_time(3) == "Quick"
    assert assign_response_time(7) == "Moderate"
    assert assign_response_time(15) == "Slow"
