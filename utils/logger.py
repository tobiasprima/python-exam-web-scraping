import logging
from pathlib import Path
import datetime

def get_logger(class_name: str, case_name: str | None = None) -> logging.Logger:
    """
    Create or get a logger.
    If case_name is provided, logs go into logs/<case_name>/scraper_<timestamp>.log.
    """
    logs_dir = Path("logs")
    if case_name:
        # sanitize directory name
        safe_case = case_name.replace(" ", "_").replace("/", "-")
        logs_dir = logs_dir / safe_case

    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / f"{class_name}.log"
    logger = logging.getLogger(f"{class_name}_{case_name or 'default'}")

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

