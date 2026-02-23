#!/usr/bin/env python3
# log_parser.py
import os
import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# --- Module-level helpers ---
def dispatch_log(file_path: Path) -> List[Dict]:
    logs = []
    ext = file_path.suffix.lower()
    with open(file_path, "r", encoding="utf-8") as f:
        if ext in [".txt", ".log"]:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 2)
                if len(parts) < 3 or not is_timestamp(parts[0]):
                    logs.append({"timestamp":"","level":"","message":line})
                    continue
                timestamp, level, message = parts
                logs.append({"timestamp": timestamp, "level": level.upper(), "message": message})
        elif ext == ".csv":
            reader = csv.DictReader(f)
            for row in reader:
                logs.append({
                    "timestamp": row.get("timestamp",""),
                    "level": row.get("level","").upper(),
                    "message": row.get("message","")
                })
        elif ext == ".json":
            data = json.load(f)
            for row in data:
                logs.append({
                    "timestamp": row.get("timestamp",""),
                    "level": row.get("level","").upper(),
                    "message": row.get("message","")
                })
        elif ext == ".xml":
            tree = ET.parse(f)
            root = tree.getroot()
            for log_elem in root.findall("log"):
                logs.append({
                    "timestamp": log_elem.findtext("timestamp",""),
                    "level": log_elem.findtext("level","").upper(),
                    "message": log_elem.findtext("message","")
                })
    return logs

def is_timestamp(s: str) -> bool:
    # Accept ISO date or datetime
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            datetime.strptime(s, fmt)
            return True
        except ValueError:
            continue
    return False

def parse_timestamp(s: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

def summarize_logs(logs: List[Dict]) -> Dict[str,int]:
    counts = {}
    for log in logs:
        lvl = log.get("level","UNKNOWN").upper()
        counts[lvl] = counts.get(lvl,0)+1
    counts["TOTAL"] = len(logs)
    return counts

def filter_logs(logs: List[Dict], levels: List[str]) -> List[Dict]:
    levels_upper = [lvl.upper() for lvl in levels]
    return [l for l in logs if l.get("level","").upper() in levels_upper]

def export_to_csv(logs: List[Dict], output_dir: Path, prefix="logs") -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_dir / f"{prefix}_{timestamp}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp","level","message"])
        writer.writeheader()
        writer.writerows(logs)
    return str(filename)

def select_levels_menu() -> List[str]:
    print("\nChoose which logs to export:")
    print("1. Warnings only")
    print("2. Errors only")
    print("3. Warnings + Errors")
    choice = input("Enter 1,2,3: ").strip()
    if choice=="1": return ["WARNING"]
    if choice=="2": return ["ERROR"]
    if choice=="3": return ["WARNING","ERROR"]
    return ["WARNING","ERROR"] # Default

def filter_last_7_days(logs: List[Dict]) -> List[Dict]:
    seven_days_ago = datetime.now() - timedelta(days=7)
    filtered = []
    for log in logs:
        ts = log.get("timestamp","")
        dt = parse_timestamp(ts)
        if dt and dt >= seven_days_ago:
            filtered.append(log)
    return filtered

def full_pipeline():
    # --- Project-root based folders ---
    base_dir = Path(__file__).parent.parent.parent.resolve()  # Project root
    logs_dir = base_dir / "logs"
    output_dir = base_dir / "output"

    all_logs = []

    if not logs_dir.exists():
        print(f"Logs folder not found: {logs_dir}")
        return

    # Collect logs
    for ext in ["txt","log","csv","json","xml"]:
        for f in logs_dir.glob(f"*.{ext}"):
            print(f"Found log: {f}")
            all_logs.extend(dispatch_log(f))

    if not all_logs:
        print("No logs found in folder.")
        return

    # Optional filter last 7 days
    filter_choice = input("Filter logs from the last 7 days? (y/n) [n]: ").lower()
    if filter_choice == "y":
        all_logs = filter_last_7_days(all_logs)

    # Summary (no timestamps)
    counts = summarize_logs(all_logs)
    print("\n--- Log Summary ---")
    for level in ["ERROR","WARNING"]:
        if level in counts:
            print(f"{level}: {counts[level]}")


    # Filter by export levels
    levels_to_export = select_levels_menu()
    if levels_to_export:
        all_logs = filter_logs(all_logs, levels_to_export)

    # Export
    csv_path = export_to_csv(all_logs, output_dir, prefix="selected_logs")
    print(f"\nExported CSV to {csv_path}")

# --- Entry point ---
def main():
    full_pipeline()

if __name__ == "__main__":
    main()