import logging
from pathlib import Path


def get_logger():
    logger = logging.getLogger("ops_toolkit")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    try:
        base_dir = Path(__file__).resolve().parent.parent
        log_dir = base_dir / "logs"
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(log_dir / "app.log")

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except PermissionError:
        # Fallback for pytest or permission issues
        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )

        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.propagate = False

    return logger


logger = get_logger()