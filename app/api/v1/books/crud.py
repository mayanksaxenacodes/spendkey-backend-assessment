# Copyright © 2026 SpendKey. All Rights Reserved.
"""Book database utilities."""
import typing as t
from datetime import datetime

import psycopg
from psycopg import rows, sql

from app import constants
from app.common import database, errors


def list_books(
    limit: int,
    offset: int,
) -> list[dict[str, t.Any]]:
    """Retrieve a list of books from the database.

    Args:
        limit: Number of books to return from the database.
        offset: Number of books to skip during pagination.

    Returns:
        List of dict items from the books table.
    """
    with database.get_pool().connection() as conn:
        cursor: psycopg.Cursor[t.Any] = conn.cursor(
            row_factory=rows.dict_row  # type: ignore
        )
        table = constants.TableNames.BOOK.value
        statement = sql.SQL(
            "SELECT * FROM {table} LIMIT %(limit)s OFFSET %(offset)s;"
        ).format(table=table)
        params = {
            "limit": limit,
            "offset": offset,
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        return cursor.fetchall()


def total_books() -> int:
    """Get the total number of books stored within the database.

    Returns:
        An int representing the total number of book rows in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.BOOK.value
        statement = sql.SQL("SELECT COUNT(*) AS count FROM {table}").format(
            table=table
        )
        cursor.execute(query=statement)  # type: ignore
        result = t.cast(dict[str, int], cursor.fetchone())
        return result.get("count", 0)


def create_book(body: dict[str, t.Any]) -> dict[str, t.Any]:
    """Save a book to the database.

    Args:
        body: HTTP request body.

    Returns:
        The newly created database row.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.BOOK.value
        statement = sql.SQL(
            """INSERT INTO {table}
(name, description, isbn, tags, price)
VALUES (
%(name)s,
%(description)s,
%(isbn)s,
%(tags)s,
%(price)s
)
RETURNING
id,
name,
description,
isbn,
price,
tags,
ai_summary,
created_at,
updated_at"""
        ).format(table=table)
        params: dict[str, t.Any] = {
            "name": body.get("name"),
            "description": body.get("description"),
            "isbn": body.get("isbn"),
            "price": body.get("price"),
            "tags": body.get("tags"),
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        return cursor.fetchone()  # type: ignore


def get_book_by_uid(uid: int) -> dict[str, t.Any]:
    """Retrieve a book from the database by the given row identifier.

    Args:
        uid: An integer value for an existing book row.

    Returns:
        An existing row from the books table as a dict.

    Raises:
        NotFound: If the book does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.BOOK.value
        statement = sql.SQL(
            """SELECT * FROM {table} WHERE id = %(uid)s"""
        ).format(table=table)
        params: dict[str, int] = {
            "uid": uid,
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        row: t.Optional[dict[str, t.Any]] = cursor.fetchone()  # type: ignore
        if not row:
            raise errors.NotFound(
                detail=f"The book 'id:{uid}' has not been found."
            )
        return row


def update_book_by_uid(uid: int, body: dict[str, t.Any]) -> dict[str, t.Any]:
    """Update an existing book in the database by the given row identifier.

    Args:
        uid: An integer value for an existing book row.
        body: HTTP request body.

    Returns:
        An existing row from the books table as a dict.

    Raises:
        NotFound: If the book does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.BOOK.value
        statement = sql.SQL(
            """UPDATE {table}
SET
name = %(name)s,
description = %(description)s,
isbn = %(isbn)s,
price = %(price)s,
tags = %(tags)s,
updated_at = %(updated_at)s
WHERE
id = %(uid)s
RETURNING
id,
name,
description,
isbn,
price,
tags,
ai_summary,
updated_at,
created_at"""
        ).format(table=table)
        params: dict[str, t.Any] = {
            "uid": uid,
            "name": body.get("name"),
            "description": body.get("description"),
            "isbn": body.get("isbn"),
            "price": body.get("price"),
            "tags": body.get("tags"),
            "updated_at": datetime.now(),
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        row: t.Optional[dict[str, t.Any]] = cursor.fetchone()  # type: ignore
        if not row:
            raise errors.NotFound(
                detail=f"The book 'id:{uid}' has not been found."
            )
        return row


def delete_book_by_uid(uid: int) -> None:
    """Remove a book from the database by the given row identifier.

    Args:
        uid: An integer value for an existing book row.

    Raises:
        NotFound: If the book does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.BOOK.value
        statement = sql.SQL(
            """DELETE FROM {table} WHERE id = %(uid)s RETURNING 1"""
        ).format(table=table)
        params: dict[str, int] = {
            "uid": uid,
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        if not cursor.fetchone():
            raise errors.NotFound(
                detail=f"The book 'id:{uid}' has not been found."
            )


def update_book_summary(uid: int, summary: str) -> dict[str, t.Any]:
    """Update the AI summary for an existing book in the database.

    Args:
        uid: An integer value for an existing book row.
        summary: The AI summary string.

    Returns:
        The updated database row.

    Raises:
        NotFound: If the book does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.BOOK.value
        statement = sql.SQL(
            """UPDATE {table}
SET
ai_summary = %(ai_summary)s,
updated_at = %(updated_at)s
WHERE
id = %(uid)s
RETURNING *"""
        ).format(table=table)
        params: dict[str, t.Any] = {
            "uid": uid,
            "ai_summary": summary,
            "updated_at": datetime.now(),
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        row: t.Optional[dict[str, t.Any]] = cursor.fetchone()  # type: ignore
        if not row:
            raise errors.NotFound(
                detail=f"The book 'id:{uid}' has not been found."
            )
        return row
