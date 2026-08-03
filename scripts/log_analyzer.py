import argparse
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG = BASE_DIR / "logs" / "app.log"

def read_logs(log_file):
    try:
        with open(log_file, "r", encoding="utf-8") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
        exit(1)


def analyze_logs(lines):
    levels = Counter()
    actions = Counter()

    for line in lines:
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


def print_report(levels, actions, total):
    print("=" * 45)
    print("Log Analysis Report")
    print("=" * 45)

    print(f"Total Log Entries : {total}\n")

    print("Log Levels")
    print("-" * 20)
    for level in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
        print(f"{level:<10}: {levels[level]}")

    print("\nUser Operations")
    print("-" * 20)
    for action in ["Created", "Updated", "Deleted", "Not Found"]:
        print(f"{action:<10}: {actions[action]}")


def main():
    parser = argparse.ArgumentParser(description="Analyze application logs")
    parser.add_argument(
        "--logfile",
        default=str(DEFAULT_LOG),
        help="Path to log file"
    )

    args = parser.parse_args()

    log_path = Path(args.logfile)

    lines = read_logs(log_path)

    levels, actions = analyze_logs(lines)

    print_report(levels, actions, len(lines))


if __name__ == "__main__":
    main()