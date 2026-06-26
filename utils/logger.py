"""
utils/logger.py
"""

from __future__ import annotations

import logging
from pathlib import Path

from config.config import LOG_DIR, config


LOG_FILE = LOG_DIR / "crawler.log"


def get_logger(name: str):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(config.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file = logging.FileHandler(
        LOG_FILE,
        encoding="utf8",
    )
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    logger.propagate = False

    return logger
