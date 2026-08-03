from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import psutil

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "app.log"
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)


def analyze_logs():
    levels = Counter()
    actions = Counter()

    if not LOG_FILE.exists():
        return levels, actions

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if "INFO" in line:
                levels["INFO"] += 1
            elif "WARNING" in line:
                levels["WARNING"] += 1
            elif "ERROR" in line:
                levels["ERROR"] += 1
            elif "CRITICAL" in line:
                levels["CRITICAL"] += 1

            if "User created" in line:
                actions["Created"] += 1
            elif "User updated" in line:
                actions["Updated"] += 1
            elif "User deleted" in line:
                actions["Deleted"] += 1
            elif "User not found" in line:
                actions["Not Found"] += 1

    return levels, actions


def generate_report():
    levels, actions = analyze_logs()

    report = REPORT_DIR / f"report_{datetime.now(UTC):%Y%m%d_%H%M%S}.txt"

    with open(report, "w", encoding="utf-8") as file:
        file.write("========== Operations Report ==========\n\n")
        file.write(f"Generated : {datetime.now(UTC)}\n\n")

        file.write("System Information\n")
        file.write("------------------------------\n")
        file.write(f"CPU Usage    : {psutil.cpu_percent()}%\n")
        file.write(f"Memory Usage : {psutil.virtual_memory().percent}%\n")
        file.write(f"Disk Usage   : {psutil.disk_usage('/').percent}%\n\n")

        file.write("Log Summary\n")
        file.write("------------------------------\n")
        file.writelines(f"{level:<10}: {levels[level]}\n" for level in ["INFO", "WARNING", "ERROR", "CRITICAL"])

        file.write("\nUser Operations\n")
        file.write("------------------------------\n")
        file.writelines(f"{action:<10}: {actions[action]}\n" for action in ["Created", "Updated", "Deleted", "Not Found"])

    print(f"Report generated: {report}")


if __name__ == "__main__":
    generate_report()