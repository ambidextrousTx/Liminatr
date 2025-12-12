import argparse
from pathlib import Path
from utils import validate_folder
from processor import strip_audio
import logging

logger = logging.getLogger(__name__)


def process(input_path: Path, output_path: Path, max_size_mb: int, dry_run: bool = False) -> tuple[int, int]:
    successful = 0
    failed = 0

    if not validate_folder(input_path) or not validate_folder(output_path):
        logger.error(f'{input_path} or {output_path} is not valid')
        return successful, failed

    max_size_bytes = max_size_mb * 1024 * 1024
    mp4_files = [f for f in input_path.rglob('*') if f.is_file()
                 and f.suffix.lower() == '.mp4'
                 and f.stat().st_size <= max_size_bytes]
    if not mp4_files:
        logger.error(f'No valid MP4 files found in {input_path}')
        return successful, failed

    logger.info(f'Found {len(mp4_files)} files within the max size of {max_size_mb} MB')

    if args.dry_run:
        logger.info(f'Would process {len(mp4_files)} files')
        for f in mp4_files:
            logger.info(f'  - {f}')
        return 0, 0

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
    parser.add_argument('--verbose', '-v', action='store_true', help='increase output verbosity')
    parser.add_argument('--dry-run', '-d', action='store_true', help='show files to be processed without processing them')
    parser.add_argument('--max-size-mb', '-m', type=int, default=1000, help='maximum file size to process (in MB)')
    args = parser.parse_args()
    max_size_mb = args.max_size_mb
    verbose = args.verbose
    dry_run = args.dry_run
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    successful, failed = process(Path(args.source), Path(args.destination), max_size_mb, dry_run)
