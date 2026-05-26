# Copyright © 2026 SpendKey. All Rights Reserved.
"""Database utility tests."""
import os
import typing as t
from unittest import mock

import pytest

from app.common import database


@mock.patch("app.common.database.psycopg_pool.ConnectionPool")
@mock.patch.dict(
    os.environ,
    {
        "DATABASE_USERNAME": "admin",
        "DATABASE_HOST": "127.0.0.1",
        "DATABASE_PORT": "2345",
        "DATABASE_NAME": "test",
    },
)
def test_get_pool(connection_pool: mock.MagicMock) -> None:
    """Should create a connection pool using configurable parameters.

    Args:
        connection_pool: Mock connection pool object.
    """
    expected_connection_info = (
        "user=admin host=127.0.0.1 port=2345 password=postgres dbname=test"
    )
    connection_args = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
    database.get_pool()
    connection_pool.assert_called_once_with(
        expected_connection_info,
        max_lifetime=1800,
        kwargs=connection_args,
        name=mock.ANY,
    )


@mock.patch("app.common.database.psycopg.connect")
@mock.patch.dict(
    os.environ,
    {
        "DATABASE_USERNAME": "admin",
        "DATABASE_HOST": "127.0.0.1",
        "DATABASE_PORT": "2345",
        "DATABASE_NAME": "test",
    },
)
@pytest.mark.parametrize(
    "autocommit, expected",
    [
        (
            None,
            {
                "user": "admin",
                "host": "127.0.0.1",
                "port": 2345,
                "password": "postgres",
                "autocommit": False,
                "dbname": "test",
            },
        ),
        (
            True,
            {
                "user": "admin",
                "host": "127.0.0.1",
                "port": 2345,
                "password": "postgres",
                "autocommit": True,
                "dbname": "test",
            },
        ),
    ],
)
def test_connect_to(
    connection: mock.MagicMock,
    autocommit: bool,
    expected: dict[str, t.Any],
) -> None:
    """Should establish a configurable connection to a database.

    Args:
        connection: Mocked utility function to connect to a database.
        autocommit: Toggle autocommit for the function under test.
        expected: The expected arguments the function should be called with.
    """
    database.connect_to(autocommit=autocommit)
    connection.assert_called_with(**expected)


@mock.patch("app.common.database.psycopg.connect")
@mock.patch.dict(os.environ, {"DATABASE_NAME": ""})
def test_connect_to_no_dbname(mock_connect: mock.MagicMock) -> None:
    """Should connect without dbname if not provided."""
    # We need to clear the lru_cache for config if it's cached, 
    # but here we are patching environ and calling connect_to.
    from app import config
    config.get_config.cache_clear()
    database.connect_to(autocommit=False)
    args, kwargs = mock_connect.call_args
    assert "dbname" not in kwargs


@mock.patch("app.common.database.psycopg_pool.ConnectionPool")
@mock.patch.dict(os.environ, {"DATABASE_NAME": ""})
def test_get_pool_no_dbname(mock_pool: mock.MagicMock) -> None:
    """Should create pool without dbname if not provided."""
    from app import config
    config.get_config.cache_clear()
    database.get_pool.cache_clear()
    database.get_pool()
    # Check if make_conninfo was called without dbname.
    # make_conninfo is called inside get_pool.
