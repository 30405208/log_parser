# src/log_parser/parser.py

import os
import questionary
from .log_dispatcher import dispatch_log

# --------------------------
# Logs folder path
# --------------------------
LOGS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs"))

# --------------------------
# Interactive file picker
# --------------------------
def choose_log_file(folder_path):
    # Only include supported log file types
    supported_exts = ['.txt', '.log', '.json', '.csv', '.xml']

    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in supported_exts]

    if not files:
        print("No log files found in logs folder.")
        exit(1)

    selected_file = questionary.select(
        "Select a log file:",
        choices=files
    ).ask()

    if selected_file is None:
        print("No file selected. Exiting.")
        exit(0)

    return os.path.join(folder_path, selected_file)



# --------------------------
# Main function
# --------------------------
def main():
    log_file = choose_log_file(LOGS_FOLDER)
    dispatch_log(log_file)

# --------------------------
# Run as CLI
# --------------------------
if __name__ == "__main__":
    main()