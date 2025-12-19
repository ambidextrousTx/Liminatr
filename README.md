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
