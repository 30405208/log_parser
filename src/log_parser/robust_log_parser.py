#!/usr/bin/env python3
# robust_log_parser.py
import os, csv, json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# --- Module-level helpers ---
def dispatch_log(file_path) -> List[Dict]:
    logs = []
    ext = Path(file_path).suffix.lower()
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
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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

def export_to_csv(logs: List[Dict], prefix="logs") -> str:
    folder = Path("output")
    folder.mkdir(exist_ok=True)
    filename = folder / f"{prefix}.csv"
    with open(filename,"w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp","level","message"])
        writer.writeheader()
        writer.writerows(logs)
    return str(filename)

def select_levels_menu() -> List[str]:
    print("\nChoose which logs to export:")
    print("1. Warnings only")
    print("2. Errors only")
    print("3. Warnings + Errors")
    print("4. Everything")
    choice = input("Enter 1,2,3,4 [4]: ").strip()
    if choice=="1": return ["WARNING"]
    if choice=="2": return ["ERROR"]
    if choice=="3": return ["WARNING","ERROR"]
    return []  # everything

def full_pipeline(folder: str = ".") -> None:
    folder_path = Path(folder)
    all_logs = []
    for ext in ["txt","log","csv","json","xml"]:
        for f in folder_path.glob(f"*.{ext}"):
            all_logs.extend(dispatch_log(f))
    if not all_logs:
        print("No logs found in folder.")
        return
    counts = summarize_logs(all_logs)
    print("\n--- Log Summary ---")
    for k,v in counts.items():
        print(f"{k}: {v}")
    levels_to_export = select_levels_menu()
    if levels_to_export:
        all_logs = filter_logs(all_logs, levels_to_export)
    csv_path = export_to_csv(all_logs, prefix="selected_logs")
    print(f"\nExported CSV to {csv_path}")

# --- Entry point for Poetry ---
def main():
    folder_input = input("Enter folder path containing logs [current]: ").strip() or "."
    full_pipeline(folder_input)