# src/log_parser/export_csv.py

import os
import csv
import questionary
from tabulate import tabulate  # optional, makes nice tables in terminal

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def summarize_logs(logs):
    """
    Generate a summary of log entries with counts and unusual activity detection.
    Returns a list of dicts for pretty printing.
    """
    total_lines = len(logs)
    info_count = sum(1 for log in logs if log.get("level", "").upper() == "INFO")
    warning_count = sum(1 for log in logs if log.get("level", "").upper() == "WARNING")
    error_count = sum(1 for log in logs if log.get("level", "").upper() == "ERROR")
    
    # Detect unusual activity (simple heuristic: warnings + errors > 20% of total)
    unusual = (warning_count + error_count) / total_lines > 0.2 if total_lines else False

    # Determine traffic-light colors
    info_color = Colors.GREEN
    warning_color = Colors.YELLOW if warning_count > 0 else Colors.GREEN
    error_color = Colors.RED if error_count > 0 else Colors.GREEN
    unusual_color = Colors.RED if unusual else Colors.GREEN

    summary = [
        {"Metric": "Total Lines", "Count": total_lines, "Color": Colors.GREEN},
        {"Metric": "INFO", "Count": info_count, "Color": info_color},
        {"Metric": "WARNING", "Count": warning_count, "Color": warning_color},
        {"Metric": "ERROR", "Count": error_count, "Color": error_color},
        {"Metric": "Unusual Activity", "Count": "Yes" if unusual else "No", "Color": unusual_color}
    ]
    return summary

def print_summary(summary):
    """
    Print the summary with colors in terminal.
    """
    for row in summary:
        print(f"{row['Metric']}: {row['Color']}{row['Count']}{Colors.RESET}")

def filter_logs(logs):
    """
    Ask user which entries to include in CSV:
    - Everything
    - Errors only
    - Warnings only
    - Suspicious lines (default)
    """
    choices = [
        "Suspicious lines (default)",
        "Errors only",
        "Warnings only",
        "Everything"
    ]
    selection = questionary.select(
        "Which log entries would you like to include in the CSV?",
        choices=choices,
        default=choices[0]
    ).ask()

    if selection == "Suspicious lines (default)":
        # Simple heuristic: errors + warnings
        return [log for log in logs if log.get("level", "").upper() in ["ERROR", "WARNING"]]
    elif selection == "Errors only":
        return [log for log in logs if log.get("level", "").upper() == "ERROR"]
    elif selection == "Warnings only":
        return [log for log in logs if log.get("level", "").upper() == "WARNING"]
    else:  # Everything
        return logs

def export_to_csv_from_logs(logs, default_filename="log_summary.csv", preview_count=5):
    """
    Prompt user to export log data to CSV, with preview of first N entries.
    Creates 'output/' folder in project root if missing.
    """
    if not logs:
        print("No log data to export.")
        return None

    # ----- Preview in terminal -----
    print("\nPreview of log data to be exported:")
    preview_logs = logs[:preview_count]
    try:
        print(tabulate(preview_logs, headers="keys", tablefmt="grid"))
    except ImportError:
        for row in preview_logs:
            print(row)
    if len(logs) > preview_count:
        print(f"...and {len(logs) - preview_count} more rows")

    # ----- Summary below preview -----
    summary = summarize_logs(logs)
    print("\n--- Log Summary ---")
    print_summary(summary)

    # ----- Filter logs -----
    filtered_logs = filter_logs(logs)
    if not filtered_logs:
        print("\nNo log entries match your selection. CSV will not be created.")
        return None

    # ----- Ask user if they want to export -----
    should_export = questionary.confirm("Would you like to export these logs to CSV?").ask()
    if not should_export:
        print("Skipping CSV export.")
        return None

    # ----- Ensure output folder exists -----
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    output_folder = os.path.join(project_root, "output")
    os.makedirs(output_folder, exist_ok=True)

    # ----- Write CSV -----
    csv_path = os.path.join(output_folder, default_filename)
    fieldnames = filtered_logs[0].keys()

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_logs)

    print(f"\nCSV exported successfully to: {csv_path}")
    return csv_path