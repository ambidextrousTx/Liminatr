# Liminatr
Eliminate audio from short video files

## Usage

```bash
uv run src/cli.py cli.py [-h] [--verbose] 
[--dry-run] [--max-size-mb MAX_SIZE_MB] 
[--max-workers MAX_WORKERS] source destination
```

Strips audio from MP4 files within a given size in a source
folder, placing the output files in the destination folder,
maintaining the original directory structure. Uses
multiprocessing. Shows a progress bar. Provides a dry-run
option for inspecting the files to be processed. Provides
a verbose option for additional logs.

## Project summary

### Core Functionality

* ✅ Video processing: Strip audio from MP4 files using FFmpeg
* ✅ Batch processing: Handle entire directories recursively
* ✅ Directory structure preservation: Maintain folder hierarchy in output
* ✅ Size filtering: Process only files under a specified size limit
* ✅ Multiprocessing: Parallel processing with configurable worker count
* ✅ Progress tracking: Visual feedback with tqdm

### CLI Features

* ✅ Dry-run mode: Preview what would be processed
* ✅ Verbosity control: Adjustable logging levels
* ✅ Flexible arguments: Source, destination, size limits, worker count
* ✅ Sensible defaults: Works out of the box with minimal configuration

### Code Quality

* ✅ Type hints: Fully typed Python throughout
* ✅ Modular architecture: Clean separation of concerns (processor, utils, CLI)
* ✅ Error handling: Graceful failure with detailed logging
* ✅ Testability: Functions designed for unit testing (testing may be enhanced with dependency injection)
* ✅ Documentation: Clear docstrings and helpful error messages
