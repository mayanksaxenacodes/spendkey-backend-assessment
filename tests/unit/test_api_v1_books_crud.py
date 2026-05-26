# Copyright © 2026 SpendKey. All Rights Reserved.
"""Books database utility tests."""
import typing as t
from unittest import mock

import pytest
from psycopg import sql

from app import constants
from app.api.v1.books import crud
from app.common import errors


def test_list_books(cursor: mock.MagicMock) -> None:
    """Should retrieve a list of books from the database.

    Args:
        cursor: Mocked database cursor.
    """
    table = constants.TableNames.BOOK.value
    expected_params = {
        "limit": 1,
        "offset": 0,
    }
    expected_query = sql.SQL(
        "SELECT * FROM {table} LIMIT %(limit)s OFFSET %(offset)s;"
    ).format(table=table)

    crud.list_books(limit=1, offset=0)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_total_books(cursor: mock.MagicMock) -> None:
    """Should return the total number of rows in the database.

    Args:
        cursor: Mocked database cursor.
    """
    table = constants.TableNames.BOOK.value
    expected_query = sql.SQL(
        "SELECT COUNT(*) AS count FROM {table}",
    ).format(table=table)
    cursor.fetchone.return_value = {"count": 1}  # type: ignore
    assert crud.total_books() == 1
    cursor.execute.assert_called_with(query=expected_query)  # type: ignore


def test_create_book(cursor: mock.MagicMock) -> None:
    """Should save a book to the database.

    Args:
        cursor: Mocked database cursor.
    """
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust for "
        "Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
    }
    table = constants.TableNames.BOOK.value
    expected_query = sql.SQL(
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
    expected_params: dict[str, t.Any] = {
        "name": body.get("name"),
        "description": body.get("description"),
        "isbn": body.get("isbn"),
        "price": body.get("price"),
        "tags": body.get("tags"),
    }

    crud.create_book(body=body)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_get_book_by_uid(cursor: mock.MagicMock) -> None:
    """Should return a book from the given row identifier.

    Args:
        cursor: Mocked database cursor.
    """
    row = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust for "
        "Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
    }
    table = constants.TableNames.BOOK.value
    expected_query = sql.SQL(
        "SELECT * FROM {table} WHERE id = %(uid)s",
    ).format(table=table)
    expected_params: dict[str, t.Any] = {"uid": 1}
    cursor.fetchone.return_value = row  # type: ignore
    assert crud.get_book_by_uid(uid=1) == row
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_get_book_by_uid_not_found(cursor: mock.MagicMock) -> None:
    """Should raise an exception when no book is found.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        table = constants.TableNames.BOOK.value
        expected_query = sql.SQL(
            "SELECT * FROM {table} WHERE id = %(uid)s",
        ).format(table=table)
        expected_params: dict[str, t.Any] = {"uid": 1}
        crud.get_book_by_uid(uid=1)
        cursor.execute.assert_called_with(  # type: ignore
            query=expected_query,
            params=expected_params,
        )


def test_update_book_by_id(cursor: mock.MagicMock) -> None:
    """Should update an existing book within the database.

    Args:
        cursor: Mocked database cursor.
    """
    uid: int = 1
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust for "
        "Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
    }
    table = constants.TableNames.BOOK.value
    expected_query = sql.SQL(
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
    expected_params: dict[str, t.Any] = {
        "uid": uid,
        "name": body.get("name"),
        "description": body.get("description"),
        "isbn": body.get("isbn"),
        "price": body.get("price"),
        "tags": body.get("tags"),
        "updated_at": mock.ANY,
    }

    crud.update_book_by_uid(uid=uid, body=body)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_update_book_by_id_not_found(cursor: mock.MagicMock) -> None:
    """Should raise an exception when no book is found.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        uid: int = 1
        body: dict[str, t.Any] = {
            "name": "Rust for Rustaceans",
            "description": "For developers who've mastered the basics, Rust"
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
            "isbn": "978-1-7185-0185-0",
            "price": 3699,
            "tags": ["computers", "programming"],
        }
        crud.update_book_by_uid(uid=uid, body=body)


def test_delete_book(cursor: mock.MagicMock) -> None:
    """Should remove a book from the database.

    Args:
        cursor: Mocked database cursor.
    """
    table = constants.TableNames.BOOK.value
    expected_query = sql.SQL(
        "DELETE FROM {table} WHERE id = %(uid)s RETURNING 1",
    ).format(table=table)
    expected_params: dict[str, int] = {"uid": 1}
    cursor.fetchone.return_value = {"row": 1}  # type: ignore
    crud.delete_book_by_uid(uid=1)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_delete_book_not_found(cursor: mock.MagicMock) -> None:
    """Should raise an exception when no book is found.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        crud.delete_book_by_uid(uid=1)


def test_update_book_summary(cursor: mock.MagicMock) -> None:
    """Should update the ai_summary for a book in the database.

    Args:
        cursor: Mocked database cursor.
    """
    uid = 1
    summary = "A great and concise book summary."
    table = constants.TableNames.BOOK.value
    expected_query = sql.SQL(
        """UPDATE {table}
SET
ai_summary = %(ai_summary)s,
updated_at = %(updated_at)s
WHERE
id = %(uid)s
RETURNING *"""
    ).format(table=table)
    expected_params = {
        "uid": uid,
        "ai_summary": summary,
        "updated_at": mock.ANY,
    }
    cursor.fetchone.return_value = {"id": uid, "ai_summary": summary}  # type: ignore
    
    res = crud.update_book_summary(uid=uid, summary=summary)
    assert res == {"id": uid, "ai_summary": summary}
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_update_book_summary_not_found(cursor: mock.MagicMock) -> None:
    """Should raise NotFound when updating summary of non-existent book.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        crud.update_book_summary(uid=1, summary="Summary")
