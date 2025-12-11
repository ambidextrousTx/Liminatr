from pathlib import Path
from typing import Optional
from utils import validate_folder, validate_source_file_is_mp4
from processor import strip_audio
import logging

logger = logging.getLogger(__name__)


def process(input_path: Path, output_path: Path) -> bool:
    if not validate_folder(input_path) or not validate_folder(output_path):
        logger.error(f'{input_path} or {output_path} is not valid')
        return False

    mp4_files = [f for f in input_path.rglob('*') if validate_source_file_is_mp4(f)]
    if not mp4_files:
        logger.error(f'No valid MP4 files found in {input_path}')
        return False

    logger.info(f'Found {len(mp4_files)} files')

    for mp4_file in mp4_files:
        output_file_path = output_path / mp4_file.name
        strip_audio(mp4_file, output_file_path)

    return True
