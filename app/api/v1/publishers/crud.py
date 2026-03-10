# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publisher database utilities."""
import typing as t
from datetime import datetime

import psycopg
from psycopg import rows, sql

from app import constants
from app.common import database, errors


def list_publishers(
    limit: int,
    offset: int,
) -> list[dict[str, t.Any]]:
    """Retrieve a list of publishers from the database.

    Args:
        limit: Number of publishers to return from the database.
        offset: Number of publishers to skip during pagination.

    Returns:
        List of dict items from the publishers table.
    """
    with database.get_pool().connection() as conn:
        cursor: psycopg.Cursor[t.Any] = conn.cursor(
            row_factory=rows.dict_row  # type: ignore
        )
        table = constants.TableNames.PUBLISHER.value
        statement = sql.SQL(
            "SELECT * FROM {table} LIMIT %(limit)s OFFSET %(offset)s;"
        ).format(table=table)
        params = {
            "limit": limit,
            "offset": offset,
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        return cursor.fetchall()


def total_publishers() -> int:
    """Get the total number of publishers stored within the database.

    Returns:
        An int representing the total number of publisher rows in the table.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.PUBLISHER.value
        statement = sql.SQL("SELECT COUNT(*) AS count FROM {table}").format(
            table=table
        )
        cursor.execute(query=statement)  # type: ignore
        result = t.cast(dict[str, int], cursor.fetchone())
        return result.get("count", 0)


def create_publisher(body: dict[str, t.Any]) -> dict[str, t.Any]:
    """Save a publisher to the database.

    Args:
        body: HTTP request body.

    Returns:
        The newly created database row.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.PUBLISHER.value
        statement = sql.SQL(
            """INSERT INTO {table}
(name, description, isbn, tags, price)
VALUES (
%(name)s
)
RETURNING
id,
name,
created_at,
updated_at"""
        ).format(table=table)
        params: dict[str, t.Any] = {
            "name": body.get("name"),
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        return cursor.fetchone()  # type: ignore


def get_publisher_by_uid(uid: int) -> dict[str, t.Any]:
    """Retrieve a publisher from the database by the given row identifier.

    Args:
        uid: An integer value for an existing book row.

    Returns:
        An existing row from the publishers table as a dict.

    Raises:
        NotFound: If the publisher does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.PUBLISHER.value
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
                detail=f"The publisher 'id:{uid}' has not been found."
            )
        return row


def update_publisher_by_uid(
    uid: int, body: dict[str, t.Any]
) -> dict[str, t.Any]:
    """Update an existing publisher in the database by the given row
    identifier.

    Args:
        uid: An integer value for an existing publisher row.
        body: HTTP request body.

    Returns:
        An existing row from the publishers table as a dict.

    Raises:
        NotFound: If the publisher does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.PUBLISHER.value
        statement = sql.SQL(
            """UPDATE {table}
SET
name = %(name)s,
updated_at = %(updated_at)s
WHERE
id = %(uid)s
RETURNING
id,
name,
updated_at,
created_at"""
        ).format(table=table)
        params: dict[str, t.Any] = {
            "uid": uid,
            "name": body.get("name"),
            "updated_at": datetime.now(),
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        row: t.Optional[dict[str, t.Any]] = cursor.fetchone()  # type: ignore
        if not row:
            raise errors.NotFound(
                detail=f"The publisher 'id:{uid}' has not been found."
            )
        return row


def delete_publisher_by_uid(uid: int) -> None:
    """Remove a publisher from the database by the given row identifier.

    Args:
        uid: An integer value for an existing publisher row.

    Raises:
        NotFound: If the publisher does not exist in the database.
    """
    with database.get_pool().connection() as conn:
        cursor = conn.cursor(row_factory=rows.dict_row)  # type: ignore
        table = constants.TableNames.PUBLISHER.value
        statement = sql.SQL(
            """DELETE FROM {table} WHERE id = %(uid)s RETURNING 1"""
        ).format(table=table)
        params: dict[str, int] = {
            "uid": uid,
        }
        cursor.execute(query=statement, params=params)  # type: ignore
        if not cursor.fetchone():
            raise errors.NotFound(
                detail=f"The publisher 'id:{uid}' has not been found."
            )
