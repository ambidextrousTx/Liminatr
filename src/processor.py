from pathlib import Path
import ffmpeg
import logging

logger = logging.getLogger(__name__)


def validate(folder):
    if not folder.exists():
        logger.error(f"Output folder '{folder}' does not exist")
        return False
    if not folder.is_dir():
        logger.error(f"Output folder '{folder}' is not a directory")
        return False
    return True


def strip_audio(input_path: Path, output_path: Path) -> bool:
    """
    Strip audio from video file.
    Just copy without re-encoding, and leave out audio
    ffmpeg.input(src).output(dst, vcodec='copy', an=None).run()
    Returns True if successful, False otherwise.
    """
    if not validate(output_path):
        return False
    try:
        ffmpeg.input(input_path).output(output_path, vcodec='copy', an=None).run()
        return True
    except Exception as e:
        logger.error(f'FFmpeg threw an error: {e}')
        return False
