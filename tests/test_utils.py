import pytest
import tempfile
from pathlib import Path
from utils import validate_folder, filter_small_mp4s


def test_validate_folder_exists():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert validate_folder(Path(tmpdirname)) is True


def test_validate_folder_not_exists():
    assert validate_folder(Path('/nonexistent')) is False


def test_validate_folder_is_file():
    with tempfile.NamedTemporaryFile() as tmp_file:
        assert validate_folder(Path(tmp_file.name)) is False


def test_filter_small_mp4s():
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_path = Path(temp_dir)
        small_mp4 = tmp_path / "small.mp4"
        small_mp4.write_bytes(b'x' * 100)  # 100 bytes

        large_mp4 = tmp_path / "large.mp4"
        large_mp4.write_bytes(b'x' * 1000)  # 1000 bytes

        txt_file = tmp_path / "not_video.txt"
        txt_file.write_bytes(b'x' * 50)

        # Filter with 500 byte limit
        results = filter_small_mp4s(tmp_path, max_size_bytes=500)

        assert len(results) == 1
        assert results[0] == small_mp4
