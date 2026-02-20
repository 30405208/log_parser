# src/log_parser/log_dispatcher.py
import os
import json
import csv
import xml.etree.ElementTree as ET
from pathlib import Path
from .export_csv import export_to_csv_from_logs

# --- TXT / LOG processor ---
def process_txt(file_path):
    logs = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Correct splitting: timestamp (19 chars) + level + message
            if len(line) < 21:  # skip malformed lines
                continue
            timestamp = line[:19]  # "YYYY-MM-DD HH:MM:SS"
            rest = line[20:].strip().split(" ", 1)  # level + message
            if len(rest) != 2:
                continue
            level, message = rest
            logs.append({"timestamp": timestamp, "level": level, "message": message})
    export_to_csv_from_logs(logs, default_prefix="txt_logs", prompt=False)
    return logs

# --- CSV processor ---
def process_csv(file_path):
    logs = []
    with open(file_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    export_to_csv_from_logs(logs, default_prefix="csv_logs", prompt=False)
    return logs

# --- JSON processor ---
def process_json(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        logs = json.load(f)
    export_to_csv_from_logs(logs, default_prefix="json_logs", prompt=False)
    return logs

# --- XML processor ---
def process_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    logs = []
    for log_elem in root.findall("log"):
        logs.append({
            "timestamp": log_elem.findtext("timestamp"),
            "level": log_elem.findtext("level"),
            "message": log_elem.findtext("message"),
        })
    export_to_csv_from_logs(logs, default_prefix="xml_logs", prompt=False)
    return logs

# --- Dispatcher ---
def main(file_path=None):
    if file_path is None:
        file_path = input("Enter log file path to process: ").strip()
        if not file_path:
            raise ValueError("No file path provided")

    ext = Path(file_path).suffix.lower()
    if ext in [".txt", ".log"]:
        return process_txt(file_path)
    elif ext == ".csv":
        return process_csv(file_path)
    elif ext == ".json":
        return process_json(file_path)
    elif ext == ".xml":
        return process_xml(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

# --- Legacy dispatcher for tests ---
def dispatch_log(file_path):
    if file_path is None:
        raise ValueError("dispatch_log requires file_path in tests")
    return main(file_path)

# --- CLI ---
if __name__ == "__main__":
    main()