# Copyright © 2026 SpendKey. All Rights Reserved.
"""ETL utilities for bulk book ingestion from CSV and JSON files."""
import csv
import io
import json
import re
import typing as t

import psycopg
from psycopg import rows, sql

from app import constants
from app.common import database


def parse_csv(file_content: str) -> list[dict[str, t.Any]]:
    """Parse raw CSV content into a list of row dictionaries.

    Args:
        file_content: The raw CSV string content.

    Returns:
        A list of parsed row dictionaries.
    """
    reader = csv.DictReader(io.StringIO(file_content))
    return list(reader)


def parse_json(file_content: str) -> list[dict[str, t.Any]]:
    """Parse raw JSON content into a list of row dictionaries.

    Args:
        file_content: The raw JSON string content.

    Returns:
        A list of parsed row dictionaries.
    """
    data = json.loads(file_content)
    if isinstance(data, dict):
        return [data]
    return data


def normalise_price(raw_price: t.Any) -> t.Optional[int]:
    """Convert a price value to an integer in cents.

    Accepts formats like "$42.99", "42.99", 4299, or "4299".

    Args:
        raw_price: The raw price value from the data source.

    Returns:
        Price as an integer in cents, or None if unparseable.
    """
    if raw_price is None or raw_price == "":
        return None

    if isinstance(raw_price, int):
        return raw_price

    price_str = str(raw_price).strip()

    # Handle dollar format like "$42.99".
    if price_str.startswith("$"):
        price_str = price_str[1:]

    if "." in price_str:
        try:
            return int(round(float(price_str) * 100))
        except ValueError:
            return None

    try:
        return int(price_str)
    except ValueError:
        return None


def normalise_isbn(raw_isbn: str) -> t.Optional[str]:
    """Normalise an ISBN to a consistent hyphenated format.

    Args:
        raw_isbn: The raw ISBN string, with or without hyphens.

    Returns:
        The normalised ISBN string, or None if invalid.
    """
    if not raw_isbn or not raw_isbn.strip():
        return None

    digits = re.sub(r"[^0-9X]", "", raw_isbn.strip(), flags=re.IGNORECASE)

    if len(digits) == 13:
        return (
            f"{digits[0:3]}-{digits[3]}-{digits[4:6]}-"
            f"{digits[6:12]}-{digits[12]}"
        )
    if len(digits) == 10:
        return digits

    return None


def normalise_tags(raw_tags: t.Any) -> list[str]:
    """Normalise tags to a consistent list format.

    Args:
        raw_tags: Tags as a comma-separated string or list.

    Returns:
        A cleaned list of tag strings.
    """
    if isinstance(raw_tags, list):
        return [t.strip().lower() for t in raw_tags if t.strip()]
    if isinstance(raw_tags, str):
        return [t.strip().lower() for t in raw_tags.split(",") if t.strip()]
    return []


def resolve_author(
    conn: psycopg.Connection[t.Any],
    author_name: str,
) -> t.Optional[int]:
    """Look up an author by name and return their ID.

    If the author does not exist, a new record is created.

    Args:
        conn: Active database connection.
        author_name: The author's full name.

    Returns:
        The author's database ID, or None if the name is empty.
    """
    if not author_name or not author_name.strip():
        return None

    name = author_name.strip()
    cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
    table = constants.TableNames.AUTHOR.value

    # Check if author exists.
    select = sql.SQL("SELECT id FROM {table} WHERE name = %(name)s").format(
        table=table
    )
    cursor.execute(query=select, params={"name": name})  # type: ignore
    row = cursor.fetchone()

    if row:
        return row["id"]

    # Create new author.
    insert = sql.SQL(
        "INSERT INTO {table} (name) VALUES (%(name)s) RETURNING id"
    ).format(table=table)
    cursor.execute(query=insert, params={"name": name})  # type: ignore
    return cursor.fetchone()["id"]  # type: ignore


def resolve_publisher(
    conn: psycopg.Connection[t.Any],
    publisher_name: str,
) -> t.Optional[int]:
    """Look up a publisher by name and return their ID.

    If the publisher does not exist, a new record is created.

    Args:
        conn: Active database connection.
        publisher_name: The publisher's name.

    Returns:
        The publisher's database ID, or None if the name is empty.
    """
    if not publisher_name or not publisher_name.strip():
        return None

    name = publisher_name.strip()
    cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
    table = constants.TableNames.PUBLISHER.value

    select = sql.SQL("SELECT id FROM {table} WHERE name = %(name)s").format(
        table=table
    )
    cursor.execute(query=select, params={"name": name})  # type: ignore
    row = cursor.fetchone()

    if row:
        return row["id"]

    insert = sql.SQL(
        "INSERT INTO {table} (name) VALUES (%(name)s) RETURNING id"
    ).format(table=table)
    cursor.execute(query=insert, params={"name": name})  # type: ignore
    return cursor.fetchone()["id"]  # type: ignore


def validate_row(row: dict[str, t.Any]) -> t.Optional[dict[str, t.Any]]:
    """Validate and transform a single row for database insertion.

    Ensures required fields are present and normalises values to match
    the database schema.

    Args:
        row: A dictionary representing a single data row.

    Returns:
        A transformed dictionary ready for insertion, or None if invalid.
    """
    # Map source columns to database schema.
    transformed: dict[str, t.Any] = {
        "name": row.get("title", "").strip() if row.get("title") else None,
        "description": row.get("description", "").strip() if row.get("description") else None,
        "isbn": normalise_isbn(row.get("isbn", "")),
        "price": normalise_price(row.get("price")),
        "tags": normalise_tags(row.get("tags", "")),
        "author": row.get("author", "").strip() if row.get("author") else None,
        "publisher": row.get("publisher", "").strip() if row.get("publisher") else None,
    }

    # Validate required fields.
    if not transformed.get("name"):
        return None

    if not transformed.get("isbn"):
        return None

    if not transformed.get("price"):
        return None

    return transformed


def insert_book(
    conn: psycopg.Connection[t.Any],
    book: dict[str, t.Any],
) -> dict[str, t.Any]:
    """Insert a single book record into the database.

    Args:
        conn: Active database connection.
        book: Validated book dictionary.

    Returns:
        The newly created database row.
    """
    cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
    table = constants.TableNames.BOOK.value
    statement = sql.SQL(
        """INSERT INTO {table}
(name, description, isbn, tags, price, author_id, publisher_id)
VALUES (
%(name)s,
%(description)s,
%(isbn)s,
%(tags)s,
%(price)s,
%(author_id)s,
%(publisher_id)s
)
RETURNING
id, name, description, isbn, price, tags,
author_id, publisher_id, created_at, updated_at"""
    ).format(table=table)
    cursor.execute(query=statement, params=book)  # type: ignore
    return cursor.fetchone()  # type: ignore


def get_existing_isbns() -> set[str]:
    """Retrieve all ISBNs currently stored in the database.

    Returns:
        A set of ISBN strings from the books table.
    """
    with database.get_pool().connection() as conn:
        cursor: psycopg.Cursor[t.Any] = conn.cursor(
            row_factory=rows.dict_row  # type: ignore
        )
        table = constants.TableNames.BOOK.value
        statement = sql.SQL("SELECT isbn FROM {table}").format(table=table)
        cursor.execute(query=statement)  # type: ignore
        return {row["isbn"] for row in cursor.fetchall()}


def process_import(file_content: str, file_type: str = "csv") -> dict[str, t.Any]:
    """Run the full ETL pipeline for a file upload.

    Parses the file content, validates each row, resolves author and
    publisher references, checks for duplicate ISBNs, and inserts valid
    records into the database.

    Args:
        file_content: Raw file string content.
        file_type: The source file format ("csv" or "json").

    Returns:
        A summary dictionary with counts and per-row error details.
    """
    if file_type == "json":
        parsed_rows = parse_json(file_content=file_content)
    else:
        parsed_rows = parse_csv(file_content=file_content)

    existing_isbns = get_existing_isbns()

    imported: list[dict[str, t.Any]] = []
    skipped: int = 0
    errors: list[dict[str, str]] = []

    with database.get_pool().connection() as conn:
        for idx, row in enumerate(parsed_rows):
            validated = validate_row(row=row)

            if validated is None:
                errors.append({
                    "row": idx + 1,
                    "reason": "Validation failed: missing required fields.",
                })
                continue

            if validated["isbn"] in existing_isbns:
                skipped += 1
                continue

            # Resolve author and publisher by name.
            author_id = resolve_author(conn=conn, author_name=validated.pop("author", None))
            publisher_id = resolve_publisher(conn=conn, publisher_name=validated.pop("publisher", None))

            validated["author_id"] = author_id
            validated["publisher_id"] = publisher_id

            record = insert_book(conn=conn, book=validated)
            existing_isbns.add(validated["isbn"])
            imported.append(record)

        conn.commit()

    return {
        "imported": len(imported),
        "skipped": skipped,
        "errors": errors,
        "total_processed": len(parsed_rows),
    }
