# Copyright © 2026 SpendKey. All Rights Reserved.
"""Authors database utility tests."""
import typing as t
from unittest import mock

import pytest
from psycopg import sql

from app import constants
from app.api.v1.authors import crud
from app.common import errors


def test_list_authors(cursor: mock.MagicMock) -> None:
    """Should retrieve a list of authors from the database.

    Args:
        cursor: Mocked database cursor.
    """
    table = constants.TableNames.AUTHOR.value
    expected_params = {
        "limit": 1,
        "offset": 0,
    }
    expected_query = sql.SQL(
        "SELECT * FROM {table} LIMIT %(limit)s OFFSET %(offset)s;"
    ).format(table=table)

    crud.list_authors(limit=1, offset=0)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_total_authors(cursor: mock.MagicMock) -> None:
    """Should return the total number of rows in the database.

    Args:
        cursor: Mocked database cursor.
    """
    table = constants.TableNames.AUTHOR.value
    expected_query = sql.SQL(
        "SELECT COUNT(*) AS count FROM {table}",
    ).format(table=table)
    cursor.fetchone.return_value = {"count": 1}  # type: ignore
    total = crud.total_authors()
    assert total == 1
    cursor.execute.assert_called_with(query=expected_query)  # type: ignore


def test_create_author(cursor: mock.MagicMock) -> None:
    """Should save an author to the database.

    Args:
        cursor: Mocked database cursor.
    """
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    table = constants.TableNames.AUTHOR.value
    expected_query = sql.SQL(
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
    expected_params: dict[str, t.Any] = {
        "name": body.get("name"),
    }

    crud.create_author(body=body)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_get_author_by_uid(cursor: mock.MagicMock) -> None:
    """Should return a author from the given row identifier.

    Args:
        cursor: Mocked database cursor.
    """
    row = {
        "name": "Jon Gjengset",
    }
    table = constants.TableNames.AUTHOR.value
    expected_query = sql.SQL(
        "SELECT * FROM {table} WHERE id = %(uid)s",
    ).format(table=table)
    expected_params: dict[str, t.Any] = {"uid": 1}
    cursor.fetchone.return_value = row  # type: ignore
    assert crud.get_author_by_uid(uid=1) == row
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_get_author_by_uid_not_found(cursor: mock.MagicMock) -> None:
    """Should raise an exception when no author is found.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        table = constants.TableNames.AUTHOR.value
        expected_query = sql.SQL(
            "SELECT * FROM {table} WHERE id = %(uid)s",
        ).format(table=table)
        expected_params: dict[str, t.Any] = {"uid": 1}
        crud.get_author_by_uid(uid=1)
        cursor.execute.assert_called_with(  # type: ignore
            query=expected_query,
            params=expected_params,
        )


def test_update_author_by_id(cursor: mock.MagicMock) -> None:
    """Should update an existing author within the database.

    Args:
        cursor: Mocked database cursor.
    """
    uid: int = 1
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    table = constants.TableNames.AUTHOR.value
    expected_query = sql.SQL(
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
    expected_params: dict[str, t.Any] = {
        "uid": uid,
        "name": body.get("name"),
        "updated_at": mock.ANY,
    }

    crud.update_author_by_uid(uid=uid, body=body)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_update_author_by_id_not_found(cursor: mock.MagicMock) -> None:
    """Should raise an exception when no author is found.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        uid: int = 1
        body: dict[str, t.Any] = {
            "name": "Jon Gjengset",
        }
        crud.update_author_by_uid(uid=uid, body=body)


def test_delete_author(cursor: mock.MagicMock) -> None:
    """Should remove a author from the database.

    Args:
        cursor: Mocked database cursor.
    """
    table = constants.TableNames.AUTHOR.value
    expected_query = sql.SQL(
        "DELETE FROM {table} WHERE id = %(uid)s RETURNING 1",
    ).format(table=table)
    expected_params: dict[str, int] = {"uid": 1}
    cursor.fetchone.return_value = {"row": 1}  # type: ignore
    crud.delete_author_by_uid(uid=1)
    cursor.execute.assert_called_with(  # type: ignore
        query=expected_query,
        params=expected_params,
    )


def test_delete_author_not_found(cursor: mock.MagicMock) -> None:
    """Should raise an exception when no author is found.

    Args:
        cursor: Mocked database cursor.
    """
    cursor.fetchone.return_value = None  # type: ignore
    with pytest.raises(errors.NotFound):
        crud.delete_author_by_uid(uid=1)
