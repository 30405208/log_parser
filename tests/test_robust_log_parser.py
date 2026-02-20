import pytest
import csv
import json
import xml.etree.ElementTree as ET
import os
from pathlib import Path

from log_parser.robust_log_parser import dispatch_log, summarize_logs, filter_logs, export_to_csv

# ------------------------------
# Fixtures
# ------------------------------
@pytest.fixture
def sample_logs():
    return [
        {"timestamp": "2026-02-20 12:00:00", "level": "INFO", "message": "ok"},
        {"timestamp": "2026-02-20 12:01:00", "level": "WARNING", "message": "warn"},
        {"timestamp": "2026-02-20 12:02:00", "level": "ERROR", "message": "err"},
    ]

# ------------------------------
# dispatch_log tests
# ------------------------------
def test_dispatch_log_txt(tmp_path):
    txt_file = tmp_path / "sample.log"
    txt_file.write_text("2026-02-20 INFO Everything ok\nBAD LINE HERE")
    logs = dispatch_log(txt_file)
    assert len(logs) == 2
    assert logs[0]["level"] == "INFO"
    assert logs[1]["level"] == ""  # malformed line handled

def test_dispatch_log_csv(tmp_path):
    csv_file = tmp_path / "sample.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp","level","message"])
        writer.writeheader()
        writer.writerow({"timestamp":"t1","level":"info","message":"msg1"})
        writer.writerow({"timestamp":"t2","level":"ERROR","message":"msg2"})
    logs = dispatch_log(csv_file)
    assert logs[0]["level"] == "INFO"
    assert logs[1]["level"] == "ERROR"

def test_dispatch_log_json(tmp_path):
    data = [{"timestamp":"t","level":"info","message":"m"}]
    json_file = tmp_path / "sample.json"
    json_file.write_text(json.dumps(data))
    logs = dispatch_log(json_file)
    assert logs[0]["level"] == "INFO"

def test_dispatch_log_xml(tmp_path):
    root = ET.Element("logs")
    e = ET.SubElement(root, "log")
    ET.SubElement(e,"timestamp").text="t"
    ET.SubElement(e,"level").text="info"
    ET.SubElement(e,"message").text="m"
    tree = ET.ElementTree(root)
    xml_file = tmp_path / "sample.xml"
    tree.write(xml_file)
    logs = dispatch_log(xml_file)
    assert logs[0]["level"] == "INFO"

# ------------------------------
# summarize_logs tests
# ------------------------------
def test_summarize_logs(sample_logs):
    summary = summarize_logs(sample_logs)
    assert summary["INFO"] == 1
    assert summary["WARNING"] == 1
    assert summary["ERROR"] == 1
    assert summary["TOTAL"] == 3

# ------------------------------
# filter_logs tests
# ------------------------------
def test_filter_logs(sample_logs):
    filtered = filter_logs(sample_logs, ["WARNING","ERROR"])
    assert len(filtered) == 2
    assert all(l["level"] in ["WARNING","ERROR"] for l in filtered)

def test_filter_logs_case_insensitive(sample_logs):
    filtered = filter_logs(sample_logs, ["warning"])
    assert len(filtered) == 1
    assert filtered[0]["level"] == "WARNING"

# ------------------------------
# export_to_csv tests
# ------------------------------
def test_export_csv_creates_file(tmp_path, sample_logs):
    csv_path = export_to_csv(sample_logs, prefix=str(tmp_path/"out"))
    assert Path(csv_path).exists()
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 3
        assert rows[0]["level"] == "INFO"

# ------------------------------
# Robustness edge cases
# ------------------------------
def test_empty_logs(tmp_path):
    csv_path = export_to_csv([], prefix=str(tmp_path/"empty"))
    assert Path(csv_path).exists()
    with open(csv_path) as f:
        content = f.read()
        assert "timestamp" in content  # headers still present

def test_malformed_lines_dispatch(tmp_path):
    txt_file = tmp_path / "bad.log"
    txt_file.write_text("MALFORMED LINE\nANOTHER BAD LINE")
    logs = dispatch_log(txt_file)
    assert len(logs) == 2
    assert all("message" in l for l in logs)
    assert all("level" in l for l in logs)  # even if empty

def test_missing_fields_csv(tmp_path):
    csv_file = tmp_path / "missing.csv"
    csv_file.write_text("timestamp,level\n2026-01-01,INFO")
    logs = dispatch_log(csv_file)
    assert logs[0]["message"] == ""  # missing field handled

def test_mixed_case_levels(tmp_path):
    txt_file = tmp_path / "mixed.log"
    txt_file.write_text("2026-01-01 warning Something\n2026-01-01 Error Failed")
    logs = dispatch_log(txt_file)
    assert logs[0]["level"] == "WARNING"
    assert logs[1]["level"] == "ERROR"