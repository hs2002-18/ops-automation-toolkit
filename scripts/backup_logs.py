from pathlib import Path
from datetime import datetime
import zipfile

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backups"

BACKUP_DIR.mkdir(exist_ok=True)


def backup_logs():
    log_files = list(LOG_DIR.glob("*.log"))

    if not log_files:
        print("No log files found.")
        return

    backup_name = BACKUP_DIR / f"logs_{datetime.now():%Y%m%d_%H%M%S}.zip"

    with zipfile.ZipFile(backup_name, "w", zipfile.ZIP_DEFLATED) as archive:
        for log_file in log_files:
            archive.write(log_file, arcname=log_file.name)

    print(f"Backup created: {backup_name}")


if __name__ == "__main__":
    backup_logs()