"""Test fixtures and utilities for other tests."""

import tempfile
import shutil
from pathlib import Path
import pytest


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary DB dir for access test"""
    test_dir = tmp_pat / "test_data"
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir
