import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("ops_toolkit")
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = logging.FileHandler(LOG_DIR / "app.log")
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.propagate = False