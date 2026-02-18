# log_dispatcher.py

########
# Dispatcher
########


# Dispacher - Returns the file type

# Support for .txt
# Support for .log
# Support for .json
# Support for .csv
# Support for .xml

# Generate logs in 
# /Users/andy/Library/CloudStorage/GoogleDrive-wells.andrew.uk@gmail.com/My Drive/work/python/log_parser/logs
# Usage: python3 generate_logs.py


#here’s a complete Python dispatcher that:
#Reads minimal lines/bytes
#Detects TXT/LOG, JSON, CSV, XML
#Uses fast heuristics first
#Falls back to lightweight parsing for the edge cases (the 1%)
#Dispatches to the correct parser function

# log_dispatcher.py
import os
import json
import csv
import xml.etree.ElementTree as ET

# --------------------------
# Parser functions
# --------------------------
def process_txt(path):
    print(f"Processing TXT log: {path}")

    error_lines = []
    warning_lines = []
    info_lines = []
    total_lines = 0

    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                lower = line.lower()

                if "error" in lower:
                    error_lines.append(line.strip())
                elif "warning" in lower:
                    warning_lines.append(line.strip())
                elif "info" in lower:
                    info_lines.append(line.strip())

    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    # ---- Summary ----
    print("\n--- Log Summary ---")
    print(f"Total lines: {total_lines}")
    print(f"INFO: {len(info_lines)}")
    print(f"WARNING: {len(warning_lines)}")
    print(f"ERROR: {len(error_lines)}")

    # ---- Show Errors ----
    if error_lines:
        print("\n--- Error Lines ---")
        for line in error_lines:
            print(line)
    else:
        print("\nNo errors found.")

def process_json(path):
    print(f"Processing JSON log: {path}")

    error_lines = []
    warning_lines = []
    info_lines = []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            data = [data]

        total = len(data)

        for entry in data:
            level = str(entry.get("level", "")).lower()

            if "error" in level:
                error_lines.append(entry)
            elif "warning" in level:
                warning_lines.append(entry)
            elif "info" in level:
                info_lines.append(entry)

    except Exception as e:
        print(f"Failed to process JSON: {e}")
        return

    print("\n--- Log Summary ---")
    print(f"Total entries: {total}")
    print(f"INFO: {len(info_lines)}")
    print(f"WARNING: {len(warning_lines)}")
    print(f"ERROR: {len(error_lines)}")

    if error_lines:
        print("\n--- Error Entries ---")
        for e in error_lines:
            print(e)

def process_csv(path):
    print(f"Processing CSV log: {path}")

    error_lines = []
    warning_lines = []
    info_lines = []
    total = 0

    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                total += 1
                level = str(row.get("level", "")).lower()

                if "error" in level:
                    error_lines.append(row)
                elif "warning" in level:
                    warning_lines.append(row)
                elif "info" in level:
                    info_lines.append(row)

    except Exception as e:
        print(f"Failed to process CSV: {e}")
        return

    print("\n--- Log Summary ---")
    print(f"Total rows: {total}")
    print(f"INFO: {len(info_lines)}")
    print(f"WARNING: {len(warning_lines)}")
    print(f"ERROR: {len(error_lines)}")

    if error_lines:
        print("\n--- Error Rows ---")
        for e in error_lines:
            print(e)

def process_xml(path):
    print(f"Processing XML log: {path}")

    error_lines = []
    warning_lines = []
    info_lines = []
    total = 0

    try:
        tree = ET.parse(path)
        root = tree.getroot()

        for entry in root.iter():
            level = entry.find("level")
            if level is not None:
                total += 1
                lvl = level.text.lower()

                if "error" in lvl:
                    error_lines.append(ET.tostring(entry, encoding='unicode'))
                elif "warning" in lvl:
                    warning_lines.append(ET.tostring(entry, encoding='unicode'))
                elif "info" in lvl:
                    info_lines.append(ET.tostring(entry, encoding='unicode'))

    except Exception as e:
        print(f"Failed to process XML: {e}")
        return

    print("\n--- Log Summary ---")
    print(f"Total entries: {total}")
    print(f"INFO: {len(info_lines)}")
    print(f"WARNING: {len(warning_lines)}")
    print(f"ERROR: {len(error_lines)}")

    if error_lines:
        print("\n--- Error Entries ---")
        for e in error_lines:
            print(e)

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
        process_txt(file_path)
    elif log_type == 'json':
        process_json(file_path)
    elif log_type == 'csv':
        process_csv(file_path)
    elif log_type == 'xml':
        process_xml(file_path)
    else:
        raise ValueError(f"Unknown log type: {file_path}")