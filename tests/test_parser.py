import sys
from pathlib import Path

# Add the "src" folder to Python path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import os
import pytest
from unittest.mock import patch
from log_parser import parser, log_dispatcher

LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))

def test_choose_log_file_returns_valid_path(tmp_path):
    # create a dummy log file
    dummy_file = tmp_path / "test.log"
    dummy_file.write_text("2026-02-18 12:00:00 INFO test")
    
    with patch('questionary.select') as mock_select:
        mock_select.return_value.ask.return_value = str(dummy_file.name)
        selected = parser.choose_log_file(tmp_path)
        assert selected.endswith("test.log")

def test_choose_log_file_no_files(tmp_path):
    with patch('builtins.print') as mock_print:
        with pytest.raises(SystemExit):
            parser.choose_log_file(tmp_path)
        mock_print.assert_called_with("No log files found in logs folder.")

def test_main_calls_dispatch_log(tmp_path):
    dummy_file = tmp_path / "test.log"
    dummy_file.write_text("2026-02-18 12:00:00 INFO test")
    with patch('src.log_parser.parser.dispatch_log') as mock_dispatch, \
         patch('questionary.select') as mock_select:
        mock_select.return_value.ask.return_value = str(dummy_file)
        parser.main()
        mock_dispatch.assert_called_once()