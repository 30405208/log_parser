import pytest
from log_parser.log_dispatcher import dispatch_log

@pytest.fixture
def sample_txt(tmp_path):
    file = tmp_path / "parser_test.log"
    file.write_text("2026-02-20 12:00:00 INFO parser test message")
    return file

def test_main_calls_dispatch_log(sample_txt):
    logs = dispatch_log(sample_txt)
    assert logs[0]["message"] == "parser test message"