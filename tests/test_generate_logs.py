import sys
from pathlib import Path

# Add the "src" folder to Python path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import os
import pytest
from subprocess import run, PIPE

from src.log_parser import generate_logs  # import your generate_logs script as a module

def test_generate_logs_creates_files(tmp_path):
    # Call the generate function directly with tmp_path
    generate_logs.main(tmp_path)  # <-- your script's main function
    files = list(tmp_path.iterdir())
    assert any(f.suffix in [".txt", ".log", ".json", ".csv", ".xml"] for f in files)