# generate_logs_random.py
# Usage: python3 generate_logs.py

import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os
import random

# --- Prompt for folder path ---
folder_path = input("Enter the folder path where logs should be generated: ").strip()
if not folder_path:
    folder_path = "."  # default to current directory
os.makedirs(folder_path, exist_ok=True)

# --- Timestamp for filenames ---
ts = datetime.now().strftime("%Y%m%d_%H%M%S")

# --- Random log generation ---
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
    # Random timestamp within last 24 hours
    now = datetime.now()
    delta = timedelta(seconds=random.randint(0, 86400))
    return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

logs = []
for _ in range(random.randint(5, 15)):  # generate 5-15 logs
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

# --- TXT & LOG ---
txt_filename = os.path.join(folder_path, f"logs_{ts}.txt")
log_filename = os.path.join(folder_path, f"logs_{ts}.log")
txt_content = "\n".join(f"{log['timestamp']} {log['level']} {log['message']}" for log in logs)

with open(txt_filename, "w") as f:
    f.write(txt_content)
with open(log_filename, "w") as f:
    f.write(txt_content)

# --- JSON ---
json_filename = os.path.join(folder_path, f"logs_{ts}.json")
with open(json_filename, "w") as f:
    json.dump(logs, f, indent=4)

# --- CSV ---
csv_filename = os.path.join(folder_path, f"logs_{ts}.csv")
with open(csv_filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["timestamp", "level", "message"])
    writer.writeheader()
    writer.writerows(logs)

# --- XML ---
xml_filename = os.path.join(folder_path, f"logs_{ts}.xml")
root = ET.Element("logs")
for log in logs:
    log_elem = ET.SubElement(root, "log")
    ET.SubElement(log_elem, "timestamp").text = log["timestamp"]
    ET.SubElement(log_elem, "level").text = log["level"]
    ET.SubElement(log_elem, "message").text = log["message"]

tree = ET.ElementTree(root)
tree.write(xml_filename, encoding="utf-8", xml_declaration=True)

print(f"All random log files generated in {folder_path}:\n- {txt_filename}\n- {log_filename}\n- {json_filename}\n- {csv_filename}\n- {xml_filename}")