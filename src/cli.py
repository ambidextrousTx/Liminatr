import argparse
from pathlib import Path
from utils import validate_folder
from processor import strip_audio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def process(input_path: Path, output_path: Path) -> tuple[int, int]:
    successful = 0
    failed = 0

    if not validate_folder(input_path) or not validate_folder(output_path):
        logger.error(f'{input_path} or {output_path} is not valid')
        return successful, failed

    mp4_files = [f for f in input_path.rglob('*') if f.is_file() and f.suffix.lower() == '.mp4']
    if not mp4_files:
        logger.error(f'No valid MP4 files found in {input_path}')
        return successful, failed

    logger.info(f'Found {len(mp4_files)} files')

    for mp4_file in mp4_files:
        relative_path = mp4_file.relative_to(input_path)
        output_file_path = output_path / relative_path
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        if strip_audio(mp4_file, output_file_path):
            successful += 1
        else:
            failed += 1

    if failed > 0:
        logger.warning(f'Successfully processed {successful}/{len(mp4_files)} files. {failed} failed.')
    else:
        logger.info(f'Successfully processed all {successful} files!')

    return successful, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Strip out audio from video files in a folder')
    parser.add_argument('source', type=str, help='the source folder')
    parser.add_argument('destination', type=str, help='the destination folder')
    # parser.add_argument('--verbose', '-v', action='store_true', help='increase output verbosity')
    args = parser.parse_args()
    successful, failed = process(Path(args.source), Path(args.destination))

