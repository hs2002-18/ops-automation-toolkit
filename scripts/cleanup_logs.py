from datetime import UTC, datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

DAYS_TO_KEEP = 30


def cleanup_logs():
    cutoff = datetime.now(UTC) - timedelta(days=DAYS_TO_KEEP)

    deleted = 0

    for log_file in LOG_DIR.glob("*.log"):
        modified = datetime.fromtimestamp(
            log_file.stat().st_mtime,
            tz=UTC,
            )

        if modified < cutoff:
            log_file.unlink()
            deleted += 1
            print(f"Deleted: {log_file.name}")

    print(f"\nTotal deleted: {deleted}")


if __name__ == "__main__":
    cleanup_logs()