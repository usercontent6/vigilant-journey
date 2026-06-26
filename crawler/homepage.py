"""
crawler/homepage.py

Discovers movie URLs from homepage pages.
"""

from __future__ import annotations

from bs4 import BeautifulSoup

from config.config import config

from crawler.models import HomepageMovie

from crawler import selectors

from utils.request import client

from utils.helpers import (
    extract_external_id,
    page_url,
    parse_date,
)


class HomepageCrawler:

    def fetch(self, page: int):

        url = page_url(
            config.BASE_URL,
            page,
        )

        html = client.html(url)

        return BeautifulSoup(
            html,
            "lxml",
        )

    # -------------------------------------------------

    def extract(self, page: int):

        soup = self.fetch(page)

        movies = []

        for article in soup.select(
            selectors.ARTICLE
        ):

            a = article.select_one(
                selectors.ARTICLE_LINK
            )

            if not a:
                continue

            href = a["href"]

            title = a.get_text(strip=True)

            image = None

            img = article.select_one(
                selectors.ARTICLE_IMAGE
            )

            if img:
                image = img.get("src")

            date = None

            span = article.select_one(
                selectors.ARTICLE_DATE
            )

            if span:
                date = parse_date(
                    span.get_text()
                )

            movies.append(

                HomepageMovie(

                    external_id=extract_external_id(
                        href
                    ),

                    url=href,

                    title=title,

                    image=image,

                    upload_date=date,
                )

            )

        return movies
