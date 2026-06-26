"""
utils/request.py

Central HTTP client for the crawler.

Features
--------
✓ Persistent Session
✓ Automatic retries
✓ Random delay
✓ Exponential backoff
✓ HTML requests
✓ JSON requests
✓ Timeout handling
"""

from __future__ import annotations

import random
import time
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.config import config


class RequestClient:

    def __init__(self):

        self.session = requests.Session()

        retries = Retry(
            total=config.MAX_RETRIES,
            connect=config.MAX_RETRIES,
            read=config.MAX_RETRIES,
            backoff_factor=config.BACKOFF_FACTOR,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],
            allowed_methods=[
                "GET",
                "HEAD",
            ],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(
            max_retries=retries,
            pool_connections=20,
            pool_maxsize=20,
        )

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.session.headers.update(
            {
                "User-Agent": config.USER_AGENT,
                "Accept": (
                    "text/html,"
                    "application/xhtml+xml,"
                    "application/xml;q=0.9,"
                    "image/avif,"
                    "image/webp,"
                    "*/*;q=0.8"
                ),
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
            }
        )

    # --------------------------------------------------

    def sleep(self) -> None:
        """
        Random delay between requests.
        """

        delay = random.uniform(
            config.REQUEST_DELAY_MIN,
            config.REQUEST_DELAY_MAX,
        )

        time.sleep(delay)

    # --------------------------------------------------

    def get(
        self,
        url: str,
        *,
        params: Optional[dict] = None,
    ) -> requests.Response:

        self.sleep()

        response = self.session.get(
            url,
            params=params,
            timeout=config.REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response

    # --------------------------------------------------

    def html(
        self,
        url: str,
    ) -> str:

        response = self.get(url)

        return response.text

    # --------------------------------------------------

    def json(
        self,
        url: str,
    ) -> dict:

        response = self.get(url)

        return response.json()

    # --------------------------------------------------

    def download(
        self,
        url: str,
        filepath,
    ):

        response = self.get(url)

        with open(filepath, "wb") as f:
            f.write(response.content)

    # --------------------------------------------------

    def head(
        self,
        url: str,
    ) -> requests.Response:

        self.sleep()

        response = self.session.head(
            url,
            timeout=config.REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

        return response

    # --------------------------------------------------

    def close(self):

        self.session.close()


client = RequestClient()
