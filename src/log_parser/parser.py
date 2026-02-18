#print("Hello, World!")

#Take in data

# Example log line: "2026-02-17 10:00 ERROR Something failed"

with open("../../logs/sample.log", "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()  # remove newline
        if not line:
            continue  # skip empty lines

        # Split the line into parts
        parts = line.split(" ")

        # Create a dictionary for this line
        log_entry = {
            "date": parts[0],
            "time": parts[1],
            "level": parts[2],
            "message": " ".join(parts[3:])  # join the rest of the line
        }

        # Now you can access fields like a structured object
        #print(log_entry["date"], log_entry["level"], log_entry["message"])

        x = log_entry["date"]
        print(x)