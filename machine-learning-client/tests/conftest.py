"""Test fixtures and utilities for other tests."""

import os
import pytest


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary DB dir for access test"""
    test_dir.mkdir(parents=True, exist_ok=True)
    return test_dir


@pytest.fixture
def clean_up_temp_dir():
    """Provide a raw temp directory using tempfile, with auto-cleanup."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)
