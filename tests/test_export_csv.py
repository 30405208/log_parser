import os
import pytest
from unittest.mock import patch
from log_parser import export_csv

sample_logs = [
    {"timestamp":"2026-02-18 12:00:00","level":"INFO","message":"ok"},
    {"timestamp":"2026-02-18 12:01:00","level":"ERROR","message":"fail"},
    {"timestamp":"2026-02-18 12:02:00","level":"WARNING","message":"warn"}
]

def test_summarize_logs_counts():
    summary = export_csv.summarize_logs(sample_logs)
    metrics = {row["Metric"]: row["Count"] for row in summary}
    assert metrics["Total Lines"] == 3
    assert metrics["ERROR"] == 1

def test_filter_logs_errors_only(monkeypatch):
    monkeypatch.setattr("questionary.select", lambda *a, **k: type("", (), {"ask": lambda s: "Errors only"})())
    filtered = export_csv.filter_logs(sample_logs)
    assert all(log["level"] == "ERROR" for log in filtered)

def test_export_to_csv_creates_file(tmp_path, monkeypatch):
    output_prefix = tmp_path / "test"
    monkeypatch.setattr("questionary.select", lambda *a, **k: type("", (), {"ask": lambda s: "Everything"})())
    monkeypatch.setattr("questionary.confirm", lambda *a, **k: type("", (), {"ask": lambda s: True})())
    
    path = export_csv.export_to_csv_from_logs(sample_logs, default_prefix=str(tmp_path / "testfile"))
    assert os.path.exists(path)
    assert path.endswith(".csv")