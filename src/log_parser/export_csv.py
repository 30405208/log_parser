# src/log_parser/export_csv.py

import os
import csv
import questionary
from tabulate import tabulate  # optional, makes nice tables in terminal

def export_to_csv_from_logs(logs, default_filename="log_summary.csv", preview_count=5):
    """
    Prompt user to export log data to CSV, with preview of first N entries.
    Creates 'output/' folder in project root if missing.

    Parameters:
        logs (list of dict): processed log entries
        default_filename (str): CSV filename
        preview_count (int): how many rows to preview
    """
    if not logs:
        print("No log data to export.")
        return None

    # ----- Preview in terminal -----
    print("\nPreview of log data to be exported:")
    preview_logs = logs[:preview_count]
    # tabulate nicely if available
    try:
        print(tabulate(preview_logs, headers="keys", tablefmt="grid"))
    except ImportError:
        # fallback plain print
        for row in preview_logs:
            print(row)
    print(f"...and {len(logs) - preview_count} more rows" if len(logs) > preview_count else "")

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
    fieldnames = logs[0].keys()

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)

    print(f"\nCSV exported successfully to: {csv_path}")
    return csv_path
