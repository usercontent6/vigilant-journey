"""
database/repository.py

High-level database operations.

IMPORTANT:
No SQL should exist outside this file.

Every crawler, parser and updater should call these methods.
"""

from __future__ import annotations

from typing import Iterable

from database.neon import db


class Repository:

    # ==========================================================
    # Queue
    # ==========================================================

    def queue_url(
        self,
        external_id: int,
        url: str,
    ) -> None:

        db.execute(
            """
            INSERT INTO crawl_queue
            (
                external_id,
                url
            )
            VALUES (%s,%s)
            ON CONFLICT (external_id)
            DO NOTHING
            """,
            (
                external_id,
                url,
            ),
        )

    # ----------------------------------------------------------

    def queue_urls(
        self,
        rows: Iterable[tuple[int, str]],
    ) -> None:

        db.executemany(
            """
            INSERT INTO crawl_queue
            (
                external_id,
                url
            )
            VALUES (%s,%s)
            ON CONFLICT (external_id)
            DO NOTHING
            """,
            rows,
        )

    # ==========================================================
    # Queue Reader
    # ==========================================================

    def next_pending(self):

        return db.fetch_one(
            """
            SELECT *

            FROM crawl_queue

            WHERE status='pending'

            ORDER BY
                priority DESC,
                id ASC

            LIMIT 1
            """
        )

    # ----------------------------------------------------------

    def pending_count(self):

        return db.scalar(
            """
            SELECT COUNT(*)

            FROM crawl_queue

            WHERE status='pending'
            """
        )

    # ==========================================================
    # Queue Status
    # ==========================================================

    def mark_processing(
        self,
        queue_id: int,
    ):

        db.execute(
            """
            UPDATE crawl_queue

            SET

                status='processing',

                updated_at=NOW()

            WHERE id=%s
            """,
            (queue_id,),
        )

    # ----------------------------------------------------------

    def mark_complete(
        self,
        queue_id: int,
    ):

        db.execute(
            """
            UPDATE crawl_queue

            SET

                status='done',

                processed_at=NOW(),

                updated_at=NOW()

            WHERE id=%s
            """,
            (queue_id,),
        )

    # ----------------------------------------------------------

    def mark_failed(
        self,
        queue_id: int,
        error: str,
    ):

        db.execute(
            """
            UPDATE crawl_queue

            SET

                status='failed',

                attempts=attempts+1,

                error=%s,

                updated_at=NOW()

            WHERE id=%s
            """,
            (
                error,
                queue_id,
            ),
        )

    # ==========================================================
    # Movies
    # ==========================================================

    def movie_exists(
        self,
        external_id: int,
    ) -> bool:

        return db.exists(
            """
            SELECT 1

            FROM movies

            WHERE external_id=%s
            """,
            (external_id,),
        )

    # ----------------------------------------------------------

    def get_movie(
        self,
        external_id: int,
    ):

        return db.fetch_one(
            """
            SELECT *

            FROM movies

            WHERE external_id=%s
            """,
            (external_id,),
        )

    # ==========================================================
    # State
    # ==========================================================

    def load_state(
        self,
        worker: str,
    ):

        return db.fetch_one(
            """
            SELECT *

            FROM crawler_state

            WHERE worker=%s
            """,
            (worker,),
        )

    # ----------------------------------------------------------

    def save_state(
        self,
        worker: str,
        current_page: int,
        last_external_id: int | None = None,
    ):

        db.execute(
            """
            INSERT INTO crawler_state
            (
                worker,
                current_page,
                last_external_id
            )

            VALUES
            (
                %s,
                %s,
                %s
            )

            ON CONFLICT(worker)

            DO UPDATE SET

                current_page=EXCLUDED.current_page,

                last_external_id=EXCLUDED.last_external_id,

                updated_at=NOW()
            """,
            (
                worker,
                current_page,
                last_external_id,
            ),
        )

    # ==========================================================
    # History
    # ==========================================================

    def log_history(
        self,
        worker: str,
        page: int,
        urls_found: int,
        success: bool,
        message: str,
    ):

        db.execute(
            """
            INSERT INTO crawl_history
            (
                worker,
                page,
                urls_found,
                success,
                message
            )

            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                worker,
                page,
                urls_found,
                success,
                message,
            ),
        )


repository = Repository()
