"""
config/config.py

Central configuration for the MovieHDTV crawler.

Loads environment variables, validates required settings,
and exposes a singleton Config object.
"""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

# ----------------------------------------------------------
# Load .env
# ----------------------------------------------------------

load_dotenv()

# ----------------------------------------------------------
# Project paths
# ----------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

CACHE_DIR = ROOT_DIR / "cache"
HTML_CACHE_DIR = CACHE_DIR / "html"
JSON_CACHE_DIR = CACHE_DIR / "json"

LOG_DIR = ROOT_DIR / "logs"

STATE_DIR = ROOT_DIR / "state"

REPORT_DIR = ROOT_DIR / "reports"

# Create directories automatically
for directory in (
    CACHE_DIR,
    HTML_CACHE_DIR,
    JSON_CACHE_DIR,
    LOG_DIR,
    STATE_DIR,
    REPORT_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------
# Configuration
# ----------------------------------------------------------

@dataclass(frozen=True)
class Config:

    # --------------------------------------------------
    # Target
    # --------------------------------------------------

    BASE_URL: str = os.getenv(
        "BASE_URL",
        "https://moviehdtv.com"
    ).rstrip("/")

    START_PAGE: int = int(
        os.getenv("START_PAGE", "1")
    )

    MAX_PAGES: int = int(
        os.getenv("MAX_PAGES", "0")
    )
    # 0 = unlimited

    # --------------------------------------------------
    # Network
    # --------------------------------------------------

    USER_AGENT: str = os.getenv(
        "USER_AGENT",
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        ),
    )

    REQUEST_TIMEOUT: int = int(
        os.getenv("REQUEST_TIMEOUT", "30")
    )

    REQUEST_DELAY_MIN: float = float(
        os.getenv("REQUEST_DELAY_MIN", "0.75")
    )

    REQUEST_DELAY_MAX: float = float(
        os.getenv("REQUEST_DELAY_MAX", "1.50")
    )

    MAX_RETRIES: int = int(
        os.getenv("MAX_RETRIES", "5")
    )

    BACKOFF_FACTOR: float = float(
        os.getenv("BACKOFF_FACTOR", "2")
    )

    # --------------------------------------------------
    # Workers
    # --------------------------------------------------

    MAX_WORKERS: int = int(
        os.getenv("MAX_WORKERS", "5")
    )

    # --------------------------------------------------
    # GitHub Actions
    # --------------------------------------------------

    RUNNING_IN_GITHUB: bool = (
        os.getenv("GITHUB_ACTIONS", "").lower() == "true"
    )

    # --------------------------------------------------
    # Database
    # --------------------------------------------------

    NEON_DATABASE_URL: str = os.getenv(
        "NEON_DATABASE_URL",
        ""
    )

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    LOG_LEVEL: str = os.getenv(
        "LOG_LEVEL",
        "INFO"
    ).upper()

    # --------------------------------------------------
    # Cache
    # --------------------------------------------------

    ENABLE_HTML_CACHE: bool = (
        os.getenv("ENABLE_HTML_CACHE", "true").lower() == "true"
    )

    ENABLE_JSON_CACHE: bool = (
        os.getenv("ENABLE_JSON_CACHE", "false").lower() == "true"
    )

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def validate(self) -> None:

        if not self.NEON_DATABASE_URL:
            raise RuntimeError(
                "Missing environment variable: NEON_DATABASE_URL"
            )

        if self.REQUEST_DELAY_MIN < 0:
            raise ValueError("REQUEST_DELAY_MIN cannot be negative.")

        if self.REQUEST_DELAY_MAX < self.REQUEST_DELAY_MIN:
            raise ValueError(
                "REQUEST_DELAY_MAX must be >= REQUEST_DELAY_MIN."
            )

        if self.MAX_WORKERS < 1:
            raise ValueError(
                "MAX_WORKERS must be at least 1."
            )


config = Config()

config.validate()
