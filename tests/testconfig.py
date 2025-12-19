import pytest
from pathlib import Path


@pytest.fixture
def sample_mp4(tmp_path):
    """Create a fake MP4 file for testing"""
    mp4_file = tmp_path / "sample.mp4"
    mp4_file.write_bytes(b'x' * 1024)  # 1KB fake file
    return mp4_file


@pytest.fixture
def input_output_dirs(tmp_path):
    """Create input and output directories"""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return input_dir, output_dir
