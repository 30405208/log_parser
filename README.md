# Log Parser

A command-line tool that detects and parses multiple log file formats,
extracts log levels, and summarises activity.

## Features

-   Automatic file type detection (TXT, LOG, JSON, CSV, XML)
-   Fast heuristic verification
-   Interactive log selection
-   Error / Warning / Info extraction
-   Summary reporting
-   Optional CSV export with preview

------------------------------------------------------------------------

## Project Structure

    log_parser/
    ├── logs/                # Generated test logs
    ├── output/              # CSV export folder
    ├── src/log_parser/
    │   ├── parser.py        # CLI entry point
    │   ├── log_dispatcher.py
    │   ├── export_csv.py
    │   └── generate_logs.py
    └── pyproject.toml

------------------------------------------------------------------------

## Installation

Requires:

-   Python 3.13+
-   Poetry

Install dependencies:

``` bash
poetry install
```

**Optional:** for prettier CSV preview tables in the terminal:

``` bash
poetry add tabulate
```

If `tabulate` is not installed, the preview will still appear in plain text.

------------------------------------------------------------------------

## Generate Test Logs

Generate up to 15 random logs:

``` bash
poetry run python src/log_parser/generate_logs.py
```

When prompted, set the output directory to:

    logs

Logs will be written to the `/logs` folder.

------------------------------------------------------------------------

## Run the Log Parser

Launch the interactive CLI:

``` bash
poetry run log-parser
```

You will:

1.  See a list of available logs in `../../logs/`
2.  Select one using arrow keys
3.  Press Enter
4.  View a structured summary
5.  Optionally export the processed logs to CSV (with a preview)

------------------------------------------------------------------------

## Example Output

    ? Select a log file: logs_20260218_115837.txt

    Detected log type: txt
    Processing TXT log...

    --- Log Summary ---
    Total lines: 500
    INFO: 420
    WARNING: 60
    ERROR: 20

    --- Error Lines ---
    2026-02-18 11:58:39 ERROR Database connection failed
    2026-02-18 12:01:12 ERROR Timeout occurred

    --- CSV Export Preview ---
    +---------------------+---------+-------------------------------+
    | timestamp           | level   | message                       |
    +---------------------+---------+-------------------------------+
    | 2026-02-18 11:50:12 | INFO    | User logged in                |
    | 2026-02-18 11:51:07 | WARNING | Disk space low                |
    | 2026-02-18 11:52:34 | ERROR   | Failed login attempt          |
    +---------------------+---------+-------------------------------+
    ...and 497 more rows

------------------------------------------------------------------------

## Supported Formats

-   .txt
-   .log
-   .json
-   .csv
-   .xml

The parser automatically detects file type and dispatches to the correct
processor.

------------------------------------------------------------------------

## What It Does

For each log file:

-   Reads entries efficiently
-   Extracts log level (INFO / WARNING / ERROR)
-   Counts occurrences
-   Prints summary statistics
-   Displays full error entries
-   Optionally previews and exports logs to CSV

------------------------------------------------------------------------

## Planned Improvements

-   CLI flags (`--errors-only`)
-   Export summary to CSV
-   Time-based filtering
-   Pattern detection
-   Recurring error analysis

