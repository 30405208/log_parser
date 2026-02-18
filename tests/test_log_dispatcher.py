import os
import pytest
import csv
import json
import xml.etree.ElementTree as ET
from log_parser import log_dispatcher

def test_process_txt(tmp_path):
    path = tmp_path / "test.txt"
    path.write_text("2026-02-18 12:00:00 INFO test message")
    logs = log_dispatcher.process_txt(str(path))
    assert logs[0]["level"] == "INFO"
    assert "test message" in logs[0]["message"]

def test_process_json(tmp_path):
    path = tmp_path / "test.json"
    data = [{"timestamp": "2026-02-18 12:00:00", "level": "ERROR", "message": "fail"}]
    json.dump(data, open(path, "w"))
    logs = log_dispatcher.process_json(str(path))
    assert logs[0]["level"] == "ERROR"

def test_process_csv(tmp_path):
    path = tmp_path / "test.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "level", "message"])
        writer.writeheader()
        writer.writerow({"timestamp":"2026-02-18","level":"WARNING","message":"warn"})
    logs = log_dispatcher.process_csv(str(path))
    assert logs[0]["level"] == "WARNING"

def test_process_xml(tmp_path):
    path = tmp_path / "test.xml"
    root = ET.Element("logs")
    log_elem = ET.SubElement(root, "log")
    ET.SubElement(log_elem, "timestamp").text = "2026-02-18 12:00:00"
    ET.SubElement(log_elem, "level").text = "INFO"
    ET.SubElement(log_elem, "message").text = "xml test"
    ET.ElementTree(root).write(path)
    logs = log_dispatcher.process_xml(str(path))
    assert logs[0]["message"] == "xml test"