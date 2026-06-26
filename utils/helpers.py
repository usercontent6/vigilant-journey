"""
utils/helpers.py
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from urllib.parse import urlparse


ID_REGEX = re.compile(r"/(\d+)-")


def extract_external_id(url: str) -> int:
    """
    https://moviehdtv.com/637490-title.html
                ↑
            returns 637490
    """

    m = ID_REGEX.search(url)

    if not m:
        raise ValueError(f"Cannot extract external id from {url}")

    return int(m.group(1))


def extract_slug(url: str) -> str:

    path = urlparse(url).path

    return path.rsplit("/", 1)[-1]


def page_url(base_url: str, page: int) -> str:

    if page <= 1:
        return base_url

    return f"{base_url}/page/{page}/"


def sha256(text: str) -> str:

    return hashlib.sha256(
        text.encode("utf8")
    ).hexdigest()


def clean_text(text: str | None) -> str:

    if not text:
        return ""

    return " ".join(text.split())


def clean_list(values):

    result = []

    seen = set()

    for value in values:

        value = clean_text(value)

        if not value:
            continue

        if value in seen:
            continue

        seen.add(value)

        result.append(value)

    return result


def safe_float(value):

    try:
        return float(value)
    except Exception:
        return None


def safe_int(value):

    try:
        return int(value)
    except Exception:
        return None


def parse_date(text: str):

    text = clean_text(text)

    try:
        return datetime.strptime(
            text,
            "%d %b %Y"
        )
    except Exception:
        return None
