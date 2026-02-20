# src/log_parser/export_csv.py
import os
import csv

def export_to_csv_from_logs(logs, default_prefix="log_summary", preview_count=5, prompt=False):
    """
    Export log data to CSV. Optionally prompts user for confirmation.
    """
    if not logs:
        print("No log data to export.")
        return None

    # Skip prompt in automated tests
    if prompt:
        import questionary
        answer = questionary.confirm("Would you like to export these logs to CSV?").ask()
        if not answer:
            return None

    # Build output folder
    output_folder = os.path.join(os.getcwd(), "output")
    os.makedirs(output_folder, exist_ok=True)

    # Filename
    csv_filename = os.path.join(output_folder, f"{default_prefix}.csv")

    # Write CSV
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "level", "message"])
        writer.writeheader()
        writer.writerows(logs)

    print(f"Exported CSV to {csv_filename}")
    return csv_filename


def summarize_logs(logs):
    """
    Return list of dicts counting log levels + total lines.
    Example: [{"Metric": "INFO", "Count": 3}, {"Metric": "Total Lines", "Count": 4}]
    """
    counts = {}
    for log in logs:
        level = log.get("level", "UNKNOWN")
        counts[level] = counts.get(level, 0) + 1

    result = [{"Metric": k, "Count": v} for k, v in counts.items()]
    result.append({"Metric": "Total Lines", "Count": len(logs)})
    return result


def filter_logs(logs, level="ERROR"):
    """Return only logs of a specific level"""
    return [log for log in logs if log.get("level") == level]