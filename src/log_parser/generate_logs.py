# generate_logs_random.py
# Usage: python3 generate_logs_random.py

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
import random
from pathlib import Path

# --- Core logic: generate logs ---
def generate_logs(folder_path):
    """
    Generate random logs in TXT, LOG, JSON, CSV, and XML formats inside folder_path.
    """
    folder_path = Path(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)

    # Timestamp for filenames
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Random log generation
    users = ["john", "mary", "admin", "alice", "bob", "eve"]
    levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    messages = [
        "logged in", "logged out", "failed login attempt", "disk space low",
        "database connection timeout", "configuration updated", "file deleted",
        "permission denied", "process started", "process terminated"
    ]

    def random_ip():
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

    def random_timestamp():
        now = datetime.now()
        delta = timedelta(seconds=random.randint(0, 86400))
        return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

    logs = []
    for _ in range(random.randint(5, 15)):
        user = random.choice(users)
        level = random.choice(levels)
        message = random.choice(messages)
        ip = random_ip() if "login" in message else None
        full_message = f"{message}" + (f" for user {user} from {ip}" if ip else f" by user {user}")
        logs.append({
            "timestamp": random_timestamp(),
            "level": level,
            "message": full_message
        })

    # TXT & LOG
    txt_filename = folder_path / f"logs_{ts}.txt"
    log_filename = folder_path / f"logs_{ts}.log"
    txt_content = "\n".join(f"{log['timestamp']} {log['level']} {log['message']}" for log in logs)

    txt_filename.write_text(txt_content)
    log_filename.write_text(txt_content)

    # JSON
    json_filename = folder_path / f"logs_{ts}.json"
    json_filename.write_text(json.dumps(logs, indent=4))

    # CSV
    csv_filename = folder_path / f"logs_{ts}.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "level", "message"])
        writer.writeheader()
        writer.writerows(logs)

    # XML
    xml_filename = folder_path / f"logs_{ts}.xml"
    root = ET.Element("logs")
    for log in logs:
        log_elem = ET.SubElement(root, "log")
        ET.SubElement(log_elem, "timestamp").text = log["timestamp"]
        ET.SubElement(log_elem, "level").text = log["level"]
        ET.SubElement(log_elem, "message").text = log["message"]
    tree = ET.ElementTree(root)
    tree.write(xml_filename, encoding="utf-8", xml_declaration=True)

    print(f"All random log files generated in {folder_path}:\n"
          f"- {txt_filename}\n"
          f"- {log_filename}\n"
          f"- {json_filename}\n"
          f"- {csv_filename}\n"
          f"- {xml_filename}")

    return [txt_filename, log_filename, json_filename, csv_filename, xml_filename]


# --- CLI wrapper ---
def main(folder_path=None):
    if folder_path is None:
        folder_path = input("Enter the folder path where logs should be generated: ").strip() or "."
    return generate_logs(folder_path)


if __name__ == "__main__":
    main()