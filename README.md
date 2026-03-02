# Log Parser
## "Logs for daaaaays bro"

![Python](https://img.shields.io/badge/python-3.13-blue)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blueviolet)
![Status](https://img.shields.io/badge/status-active-success)



# Tl:Dr: 
- Drop your logs in to the logs folder
- You need Python and Poetry
- Open Terminal a fnd put poetry run log_parser
- Output folder has your log.

## Project Status

This project is **functionally complete**:

- All functions are implemented and tested with unit tests.
- Tests pass locally and cover all key functionality.
- Logs are parsed, filtered, and exported as intended.
- README is complete and formatted for clarity.

### Notes / Future Improvements

- CI (Continuous Integration) via GitHub Actions can be added to automatically run tests on push or pull requests.
- Optional linting/formatting checks (e.g., `black`, `flake8`) can be added for code style enforcement.
- Coverage reporting and badges can be added to track test coverage and status.

These improvements are **nice-to-have** but not required for the current functionality.

------------------------------------------------------------------------

A lightweight, multi-format log parsing utility built with Python and
managed using Poetry.

It scans a `logs/` directory, parses supported log formats, summarizes
warnings and errors, optionally filters logs from the last 7 days, and
exports selected results to CSV.

------------------------------------------------------------------------

## Table of Contents

-   Features
-   Project Structure
-   Installation (Poetry)
-   Usage
-   Running Tests
-   Supported Formats
-   Example Output
-   License

------------------------------------------------------------------------

## Features

-   Supports `.txt`, `.log`, `.csv`, `.json`, `.xml`
-   Normalizes log levels to uppercase
-   Gracefully handles malformed log lines
-   Optional filtering for logs from the last 7 days
-   Export options:
    -   Warnings only
    -   Errors only
    -   Warnings + Errors
-   Timestamped CSV export
-   Clean summary output (no timestamp clutter)

------------------------------------------------------------------------

## Project Structure

```

.
├── logs
│   ├── logs_20260218_115837.csv
│   ├── logs_20260218_115837.json
│   ├── logs_20260218_115837.log
│   ├── logs_20260218_115837.txt
│   └── logs_20260218_115837.xml
├── output (Created automatically when needed - after 1st run.)
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   └── log_parser
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-313.pyc
│       │   └── log_parser.cpython-313.pyc
│       └── log_parser.py
└── tests
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-313.pyc
    │   └── test_robust_log_parser.cpython-313-pytest-9.0.2.pyc
    └── test_robust_log_parser.py

```

Notes: - `logs/` → Input log files - `output/` → Generated CSV exports -
`src/log_parser/` → Application source code - `tests/` → Pytest test
suite - `pyproject.toml` → Poetry configuration

------------------------------------------------------------------------

## Installation (Poetry)

This project uses Poetry for dependency management and packaging.

### 1. Install Poetry

https://python-poetry.org/docs/

### 2. Install dependencies

From the project root:

    poetry install

### 3. Activate the virtual environment

    poetry env activate

Or run commands directly with:

    poetry run <command>

------------------------------------------------------------------------

## Usage

Run the application with:

    poetry run python src/log_parser/log_parser.py

You will be prompted to:

1.  Optionally filter logs from the last 7 days
2.  Choose which log levels to export

The resulting CSV file will be written to:

    output/selected_logs_YYYYMMDD_HHMMSS.csv

------------------------------------------------------------------------

## Running Tests

Tests are written using pytest.

Run tests with:

    poetry run pytest

------------------------------------------------------------------------

## Supported Formats

### TXT / LOG

Expected format:

    YYYY-MM-DD LEVEL Message text
    YYYY-MM-DD HH:MM:SS LEVEL Message text

Malformed lines are preserved but assigned empty timestamp and level
fields.

### CSV

Required headers:

    timestamp,level,message

### JSON

Structure:

    [
      {"timestamp": "...", "level": "...", "message": "..."},
      ...
    ]

### XML

Structure:

    <logs>
      <log>
        <timestamp>...</timestamp>
        <level>...</level>
        <message>...</message>
      </log>
    </logs>

------------------------------------------------------------------------

## Example Output

--- Log Summary --- ERROR: 12 WARNING: 6

Exported CSV to output/selected_logs_20260223_133908.csv

------------------------------------------------------------------------

## License

MIT License --- free to use and modify.
