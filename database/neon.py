"""
database/neon.py

Central PostgreSQL / Neon database layer.

Features
--------
✓ Connection Pool
✓ Transactions
✓ Automatic reconnect
✓ Execute
✓ Fetch One
✓ Fetch All
✓ Bulk Execute
✓ UPSERT ready
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterable

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from config.config import config


POOL = ConnectionPool(
    conninfo=config.NEON_DATABASE_URL,
    min_size=1,
    max_size=10,
    kwargs={
        "autocommit": False,
        "row_factory": dict_row,
    },
)


class Database:

    def __init__(self):
        self.pool = POOL

    # -----------------------------------------------------

    @contextmanager
    def connection(self):

        with self.pool.connection() as conn:
            try:
                yield conn
                conn.commit()

            except Exception:
                conn.rollback()
                raise

    # -----------------------------------------------------

    def execute(
        self,
        sql: str,
        params: tuple | None = None,
    ) -> None:

        with self.connection() as conn:
            conn.execute(sql, params)

    # -----------------------------------------------------

    def fetch_one(
        self,
        sql: str,
        params: tuple | None = None,
    ) -> dict | None:

        with self.connection() as conn:

            cur = conn.execute(sql, params)

            return cur.fetchone()

    # -----------------------------------------------------

    def fetch_all(
        self,
        sql: str,
        params: tuple | None = None,
    ) -> list[dict]:

        with self.connection() as conn:

            cur = conn.execute(sql, params)

            return cur.fetchall()

    # -----------------------------------------------------

    def executemany(
        self,
        sql: str,
        rows: Iterable[tuple],
    ) -> None:

        with self.connection() as conn:

            with conn.cursor() as cur:
                cur.executemany(sql, rows)

    # -----------------------------------------------------

    def exists(
        self,
        sql: str,
        params: tuple | None = None,
    ) -> bool:

        row = self.fetch_one(sql, params)

        return row is not None

    # -----------------------------------------------------

    def scalar(
        self,
        sql: str,
        params: tuple | None = None,
    ) -> Any:

        row = self.fetch_one(sql, params)

        if row is None:
            return None

        return next(iter(row.values()))

    # -----------------------------------------------------

    def close(self):

        self.pool.close()


db = Database()
