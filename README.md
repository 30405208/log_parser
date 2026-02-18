# Log Parser

A command-line tool that detects and parses multiple log file formats,
extracts log levels, and summarises activity.

## Features

-   Automatic file type detection (TXT, LOG, JSON, CSV, XML)
-   Fast heuristic verification
-   Interactive log selection
-   Error / Warning / Info extraction
-   Summary reporting

------------------------------------------------------------------------

## Project Structure

    log_parser/
    ├── logs/                # Generated test logs
    ├── src/log_parser/
    │   ├── parser.py        # CLI entry point
    │   ├── log_dispatcher.py
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

------------------------------------------------------------------------

## Planned Improvements

-   CLI flags (`--errors-only`)
-   Export summary to CSV
-   Time-based filtering
-   Pattern detection
-   Recurring error analysis
