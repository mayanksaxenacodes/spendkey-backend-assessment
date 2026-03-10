# pylint: disable=unused-argument
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Unit test configuration."""
import typing as t
from unittest import mock

import pytest
from fastapi import testclient

from app.server import factory


@pytest.fixture(name="database")
def fixture_database() -> t.Iterator[mock.MagicMock]:
    """Database connection factory fixture.

    This prevents the application from establishing database connections
    during unit testing.

    Yields:
        Mocked database connection pool factory function.
    """
    with mock.patch("app.common.database.get_pool") as mocked:
        yield mocked


@pytest.fixture(name="cursor")
def fixture_cursor(database: mock.MagicMock) -> t.Iterator[mock.MagicMock]:
    """Database cursor fixture.

    Useful for making assertions on database interactions during unit testing.

    Args:
        database: Mocked database connection pool.

    Yields:
        Mocked database cursor.
    """
    cursor = mock.MagicMock()
    mock_context_manager = (
        database.return_value.connection.return_value.__enter__
    )
    mock_context_manager.return_value.cursor.return_value = cursor
    yield cursor


@pytest.fixture(name="client")
def fixture_client(
    database: mock.MagicMock,
) -> t.Iterator[testclient.TestClient]:
    """FastAPI test client fixture.

    Args:
        database: Mocked database connection pool.

    Yields:
        Test client, used for issuing HTTP requests to the application.
    """
    app = factory.create_app()
    yield testclient.TestClient(app=app)
