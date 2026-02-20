import pytest
from log_parser.log_dispatcher import dispatch_log

@pytest.fixture
def sample_txt(tmp_path):
    file = tmp_path / "sample.log"
    file.write_text("2026-02-20 12:00:00 INFO test message")
    return file

@pytest.fixture
def sample_csv(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text("timestamp,level,message\n2026-02-20 12:00:00,INFO,test message")
    return file

@pytest.fixture
def sample_json(tmp_path):
    file = tmp_path / "sample.json"
    file.write_text('[{"timestamp": "2026-02-20 12:00:00", "level": "INFO", "message": "test message"}]')
    return file

@pytest.fixture
def sample_xml(tmp_path):
    file = tmp_path / "sample.xml"
    file.write_text("""
    <logs>
        <log>
            <timestamp>2026-02-20 12:00:00</timestamp>
            <level>INFO</level>
            <message>test message</message>
        </log>
    </logs>
    """)
    return file

def test_process_txt(sample_txt):
    logs = dispatch_log(sample_txt)
    assert logs[0]["message"] == "test message"

def test_process_csv(sample_csv):
    logs = dispatch_log(sample_csv)
    assert logs[0]["message"] == "test message"

def test_process_json(sample_json):
    logs = dispatch_log(sample_json)
    assert logs[0]["message"] == "test message"

def test_process_xml(sample_xml):
    logs = dispatch_log(sample_xml)
    assert logs[0]["message"] == "test message"