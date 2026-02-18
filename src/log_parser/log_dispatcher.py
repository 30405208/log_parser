import os
import json
import csv
import xml.etree.ElementTree as ET
from .export_csv import export_to_csv_from_logs

# --------------------------
# Parser functions
# --------------------------
def process_txt(path):
    """Parse TXT or LOG files"""
    print(f"Processing TXT log: {path}")
    logs = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Example format: "2026-02-17 09:15:21 INFO User logged in"
            parts = line.split(" ", 2)
            if len(parts) == 3:
                timestamp = parts[0] + " " + parts[1]
                level = parts[2].split(" ")[0]
                message = " ".join(parts[2].split(" ")[1:])
                logs.append({"timestamp": timestamp, "level": level, "message": message})

    export_to_csv_from_logs(logs, default_filename=os.path.basename(path).replace(".txt", "_summary.csv"))
    return logs


def process_json(path):
    """Parse JSON log files"""
    print(f"Processing JSON log: {path}")
    logs = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for entry in data:
            logs.append({
                "timestamp": entry.get("timestamp", ""),
                "level": entry.get("level", ""),
                "message": entry.get("message", "")
            })
    export_to_csv_from_logs(logs, default_filename=os.path.basename(path).replace(".json", "_summary.csv"))
    return logs


def process_csv(path):
    """Parse CSV log files"""
    print(f"Processing CSV log: {path}")
    logs = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append({
                "timestamp": row.get("timestamp", ""),
                "level": row.get("level", ""),
                "message": row.get("message", "")
            })
    export_to_csv_from_logs(logs, default_filename=os.path.basename(path).replace(".csv", "_summary.csv"))
    return logs


def process_xml(path):
    """Parse XML log files"""
    print(f"Processing XML log: {path}")
    logs = []
    tree = ET.parse(path)
    root = tree.getroot()
    for log_elem in root.findall("log"):
        logs.append({
            "timestamp": log_elem.findtext("timestamp", ""),
            "level": log_elem.findtext("level", ""),
            "message": log_elem.findtext("message", "")
        })
    export_to_csv_from_logs(logs, default_filename=os.path.basename(path).replace(".xml", "_summary.csv"))
    return logs

# --------------------------
# Fast heuristic detector
# --------------------------
def detect_log_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.txt', '.log']:
        return 'txt'
    if ext == '.json':
        return 'json'
    if ext == '.csv':
        return 'csv'
    if ext == '.xml':
        return 'xml'

    # Read first 5 lines for heuristics
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f.readline().strip() for _ in range(5)]
    except Exception:
        return 'txt'

    if not lines or lines[0] == '':
        return 'txt'

    first = lines[0]

    # JSON heuristic
    if first.startswith('{') or first.startswith('['):
        last = lines[-1] if lines else ''
        if last.endswith('}') or last.endswith(']'):
            return 'json'

    # XML heuristic
    if first.startswith('<') and any('</' in line for line in lines):
        return 'xml'

    # CSV heuristic
    if ',' in first and all(first.count(',') == line.count(',') for line in lines[1:]):
        return 'csv'

    return 'txt'

# --------------------------
# Edge-case verification
# --------------------------
def verify_edge_case(file_path, log_type):
    if log_type == 'json':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError:
            log_type = 'txt'
    elif log_type == 'xml':
        try:
            ET.parse(file_path)
        except ET.ParseError:
            log_type = 'txt'
    elif log_type == 'csv':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = ''.join([next(f) for _ in range(5)])
                csv.Sniffer().sniff(sample)
        except Exception:
            log_type = 'txt'
    return log_type

# --------------------------
# Dispatcher
# --------------------------
def dispatch_log(file_path):
    log_type = detect_log_file_type(file_path)
    log_type = verify_edge_case(file_path, log_type)
    print(f"Detected log type: {log_type}")

    if log_type == 'txt':
        return process_txt(file_path)
    elif log_type == 'json':
        return process_json(file_path)
    elif log_type == 'csv':
        return process_csv(file_path)
    elif log_type == 'xml':
        return process_xml(file_path)
    else:
        raise ValueError(f"Unknown log type: {file_path}")