from pathlib import Path
import tempfile

from processor import build_ffmpeg_command


def test_build_ffmpeg_command():
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_path = Path(temp_dir)
        input_mp4_path = tmp_path / "small.mp4"
        input_mp4_path.write_bytes(b'x' * 100)

        output_mp4_path = tmp_path / "large.mp4"
        cmd = build_ffmpeg_command(input_mp4_path, output_mp4_path)

        assert cmd is not None
        # Could inspect cmd properties if needed
