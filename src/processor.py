from pathlib import Path
import ffmpeg
import logging

logger = logging.getLogger(__name__)


def strip_audio(input_path: Path, output_path: Path) -> bool:
    """
    Strip audio from video file.
    Just copy without re-encoding, and leave out audio
    ffmpeg.input(src).output(dst, vcodec='copy', an=None).run()
    Returns True if successful, False otherwise.
    """
    try:
        (ffmpeg.input(input_path)
         .output(str(output_path), vcodec='copy', an=None)
         .run(quiet=True, overwrite_output=True))
        return True
    except ffmpeg.Error as e:
        stderr = e.stderr.decode()[:500]
        logger.error(f'FFmpeg error: {stderr} processing {input_path}')
        return False
