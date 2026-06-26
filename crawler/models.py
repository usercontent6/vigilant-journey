"""
crawler/models.py
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class QueueMovie:

    external_id: int

    url: str


@dataclass(slots=True)
class HomepageMovie:

    external_id: int

    url: str

    title: str

    image: str | None

    upload_date: datetime | None


@dataclass(slots=True)
class Movie:

    external_id: int

    slug: str

    url: str

    title: str

    description: str

    cover: str | None

    imdb: float | None

    year: int | None

    language: str | None

    original_language: str | None

    runtime: str | None

    quality: str | None

    format: str | None

    filesize: str | None

    genres: list[str] = field(default_factory=list)

    cast: list[str] = field(default_factory=list)

    writers: list[str] = field(default_factory=list)

    directors: list[str] = field(default_factory=list)

    screenshots: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)

    download_links: list[dict] = field(default_factory=list)

    upload_date: datetime | None = None
