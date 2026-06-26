"""
services/discovery.py

Business logic for homepage discovery.

This layer sits between the crawler and the database.
"""

from crawler.homepage import HomepageCrawler
from database.repository import repository
from utils.logger import get_logger

logger = get_logger(__name__)


class DiscoveryService:

    WORKER = "homepage"

    def __init__(self):

        self.crawler = HomepageCrawler()

    def discover_page(self, page: int) -> int:
        """
        Crawl one homepage page.

        Returns
        -------
        Number of discovered movies.
        """

        movies = self.crawler.extract(page)

        if not movies:
            return 0

        rows = []

        for movie in movies:

            rows.append(
                (
                    movie.external_id,
                    movie.url,
                )
            )

        repository.queue_urls(rows)

        repository.save_state(
            worker=self.WORKER,
            current_page=page + 1,
            last_external_id=max(
                m.external_id
                for m in movies
            ),
        )

        repository.log_history(
            worker=self.WORKER,
            page=page,
            urls_found=len(rows),
            success=True,
            message="Success",
        )

        logger.info(
            "Discovered %s movies from page %s",
            len(rows),
            page,
        )

        return len(rows)
