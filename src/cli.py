import argparse
import os
from pathlib import Path
from utils import validate_folder, filter_small_mp4s
from processor import strip_audio
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

DEFAULT_MAX_SIZE_MB = 1000


def process(input_path: Path, output_path: Path,
            max_size_mb: int = DEFAULT_MAX_SIZE_MB, dry_run: bool = False,
            max_workers: int = None) \
        -> tuple[int, int]:
    successful = 0
    failed = 0

    if not validate_folder(input_path) or not validate_folder(output_path):
        logger.error(f'{input_path} or {output_path} is not valid')
        return successful, failed

    max_size_bytes = max_size_mb * 1024 * 1024
    mp4_files = filter_small_mp4s(input_path, max_size_bytes)
    if not mp4_files:
        logger.error(f'No valid MP4 files found in {input_path}')
        return successful, failed

    logger.info(f'Found {len(mp4_files)} files within the max size of '
                f'{max_size_mb} MB')

    if dry_run:
        logger.info(f'Would process {len(mp4_files)} files')
        for f in mp4_files:
            logger.info(f'  - {f}')
        return 0, 0

    if max_workers is None:
        max_workers = os.cpu_count() - 1 or 1

    # Pre-create all output directories before multiprocessing
    for mp4_file in mp4_files:
        relative_path = mp4_file.relative_to(input_path)
        output_file_path = output_path / relative_path
        output_file_path.parent.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures_to_file = {
            executor.submit(strip_audio, mp4_file,
                            output_path / mp4_file.relative_to(input_path)
                            ): mp4_file for mp4_file in mp4_files
        }

        for future in tqdm(as_completed(futures_to_file), total=len(mp4_files),
                           desc="Stripping audio"):
            mp4_file = futures_to_file[future]
            try:
                if future.result():
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f'Unexpected error processing {mp4_file}: {e}')

    if failed > 0:
        logger.warning(f'Successfully processed {successful}/{len(mp4_files)}'
                       f' files. {failed} failed.')
    else:
        logger.info(f'Successfully processed all {successful} files!')

    return successful, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Strip out audio from video files in a folder')
    parser.add_argument('source', type=str, help='the source folder')
    parser.add_argument('destination', type=str, help='the destination folder')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='increase output verbosity')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='show files to be processed without processing')
    parser.add_argument('--max-size-mb', '-m', type=int,
                        default=DEFAULT_MAX_SIZE_MB,
                        help='maximum file size to process (in MB)')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    successful, failed = process(Path(args.source), Path(args.destination),
                                 args.max_size_mb, args.dry_run)
