from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def validate_source_file_is_mp4(input_path: Path) -> bool:
    if not input_path.exists():
        logger.error(f'Source file {input_path} does not exist')
        return False

    if not input_path.is_file():
        logger.error(f'Source fie {input_path} is not a file')

    return input_path.suffix.lower() in {'.mp4'}


def validate_folder(folder: Path) -> bool:
    if not folder.exists():
        logger.error(f'Folder {folder} does not exist')
        return False
    if not folder.is_dir():
        logger.error(f'Folder {folder} is not a directory')
        return False
    return True
