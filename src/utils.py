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
