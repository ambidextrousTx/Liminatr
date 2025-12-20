from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock

from processor import build_ffmpeg_command, strip_audio


def test_build_ffmpeg_command():
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_path = Path(temp_dir)
        input_mp4_path = tmp_path / "small.mp4"
        input_mp4_path.write_bytes(b'x' * 100)

        output_mp4_path = tmp_path / "large.mp4"
        cmd = build_ffmpeg_command(input_mp4_path, output_mp4_path)

        assert cmd is not None
        # Could inspect cmd properties if needed


@patch('processor.ffmpeg')
def test_strip_audio_success(mock_ffmpeg):
    """Test successful audio stripping"""
    # Setup mock
    mock_cmd = MagicMock()
    mock_ffmpeg.input.return_value.output.return_value = mock_cmd

    input_path = Path('/input/video.mp4')
    output_path = Path('/output/video.mp4')

    result = strip_audio(input_path, output_path)

    assert result is True
    mock_cmd.run.assert_called_once_with(quiet=True, overwrite_output=True)
