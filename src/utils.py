from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def validate_folder(folder: Path) -> bool:
    if not folder.exists():
        logger.error(f'Folder {folder} does not exist')
        return False
    if not folder.is_dir():
        logger.error(f'Folder {folder} is not a directory')
        return False
    return True


def filter_small_mp4s(input_path, max_size_bytes):
    return [f for f in input_path.rglob('*') if f.is_file()
            and f.suffix.lower() == '.mp4'
            and f.stat().st_size <= max_size_bytes]
