# Copyright © 2026 SpendKey. All Rights Reserved.
"""Book data serialization utilities."""
import typing as t
from datetime import datetime

from app.api.v1.books import schemas


def to_book_list(rows: list[dict[str, t.Any]], total: int) -> schemas.BookList:
    """Creates an OpenAPI schema formatted book list.

    Args:
        rows: Rows from the books table as a list of dict items.
        total: Int representing the total number of rows in the books table.

    Returns:
        BookList object.
    """
    return schemas.BookList(
        data=[to_book(row=row) for row in rows],
        total=total,
    )


def to_book(row: dict[str, t.Any]) -> schemas.Book:
    """Create an OpenAPI schema formatted book.

    Args:
        row: Dict representing a row from the books table.

    Returns:
        Book object.
    """
    return schemas.Book(
        id=row.get("id", 0),
        name=row.get("name", ""),
        description=row.get("description"),
        isbn=row.get("isbn", ""),
        tags=[tag.strip() for tag in row.get("tags", [])],
        price=row.get("price"),
        author_id=row.get("author_id"),
        publisher_id=row.get("publisher_id"),
        created_at=row.get("created_at", datetime.now()),
        updated_at=row.get("updated_at", datetime.now()),
    )
