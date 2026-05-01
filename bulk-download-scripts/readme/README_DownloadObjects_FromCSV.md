# Download Objects From CSV

## Contents
Click below to go directly to the section you need.

- **[Overview](#overview)**
- **[Prerequisites](#prerequisites)**
- **[Usage](#usage)**
- **[Script Breakdown](#script-breakdown)**
- **[Output](#output)**
- **[Notes](#notes)**
- **[Troubleshooting](#troubleshooting)**

## Overview
This script reads CSV file(s) produced by `GenerateObjectURLs_NoDownload_AllChildRecords.py` (or similar CSVs containing object URLs) and downloads the listed digital objects.

> [!IMPORTANT]
> This script does NOT call the National Archives Catalog API, so it will not impact your query limit. It only reads CSVs and downloads URLs.

## Prerequisites
- **Python 3.x** installed on your machine.
- **requests** Python package installed (`pip install requests`).

## Usage

#### Basic usage, downloading a single CSV:
```bash
python scripts/DownloadObjects_FromCSV_RateLimited.py --csv ObjectsList_123456789_1.csv
```

#### Download all CSVs from a directory:
```bash
python scripts/DownloadObjects_FromCSV_RateLimited.py --dir /path/to/csvs --output-dir /data/downloads
```

#### Common options
- `--workers`: Number of concurrent download workers (default 4)
- `--base-delay`: Base per-request delay in seconds (default 0.5)
- `--jitter`: Max randomized jitter in seconds added to sleeps (default 0.5)
- `--batch-size`: Number of downloads per batch before a longer sleep (default 50)
- `--batch-sleep`: Seconds to sleep after each batch (default 10s)
- `--max-retries`: Max retries per file on failure (default 4)
- `--base-backoff`: Base backoff seconds for exponential retry (default 1s)
- `--timeout`: HTTP request timeout in seconds (default 30s)

### Script Breakdown
- The script parses CSV files and enqueues download tasks.
- Worker threads download files concurrently (configurable).
- Each download uses streaming writes to avoid large memory use.
- On transient HTTP errors (e.g., 429, 5xx), the worker performs exponential backoff with jitter before retrying.
- After every `--batch-size` completed downloads the script sleeps for `--batch-sleep` seconds to give servers a breather.
- Existing files are skipped to make the process restart-safe.

> [!NOTE]
> The script expect the below CSV format.
#### CSV format
- Expected columns (header row optional): `Parent NAID`, `Title`, `Digital Object URL`
- The script supports simple variants: lines with just the URL, or 2-column rows (parent,url).

## Output
- Downloaded files are stored under `--output-dir` in subdirectories named by `Parent NAID` (default `downloads/{parent_naid}/{filename}`).
- A summary log `download_log.csv` is written to the output directory after the run.

## Notes
- Start with `GenerateObjectURLs_NoDownload_AllChildRecords.py` to produce CSVs and inspect URLs first.
- Use moderate concurrency (4 workers is a good default). Increase only if you understand the server load implications.
- Keep `--batch-size` and `--batch-sleep` conservative for large runs.
- Monitor your network and the server responses; adjust delays if you see many 429s.
- If a download is interrupted, re-run the script; it will skip already-downloaded files and continue.

## Troubleshooting
- **File Write Errors**: Verify that you have write permissions in the directory where the script is running.
- **Insufficient Disk Space**: High-resolution image collections require significant disk space. Ensure your system has enough free space for downloaded files.
