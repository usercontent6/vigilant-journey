"""
database/init_db.py

Creates the database schema if it doesn't already exist.
"""

from pathlib import Path

from database.neon import db


def initialize_database():

    schema = (
        Path(__file__)
        .parent
        .joinpath("schema.sql")
        .read_text(encoding="utf8")
    )

    db.execute(schema)

    print("✓ Database initialized")


if __name__ == "__main__":
    initialize_database()
