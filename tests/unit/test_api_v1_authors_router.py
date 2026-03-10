# Copyright © 2026 SpendKey. All Rights Reserved.
"""Author router tests."""
import typing as t
from datetime import datetime
from unittest import mock

import pytest
import requests
from fastapi import status, testclient

from app import config
from app.api.v1.authors import schemas
from app.common import errors
from app.server import schemas as server_schema

BASE_PATH: str = "/api/v1/authors"


@pytest.fixture(name="total_authors")
def fixture_total_authors() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the total_authors database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.authors.crud.total_authors") as mocked:
        mocked.return_value = 9
        yield mocked


@pytest.fixture(name="list_authors")
def fixture_list_authors() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the list_authors database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.authors.crud.list_authors") as mocked:
        row: dict[str, t.Any] = {
            "id": 1,
            "name": "",
            "created_on": "",
            "updated_on": "",
        }
        mocked.return_value = [row]
        yield mocked


@pytest.fixture(name="create_author")
def fixture_create_author() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the create_author database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.authors.crud.create_author") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "Jon Gjengset",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="update_author_by_uid")
def fixture_update_author_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the update_author_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.authors.crud.update_author_by_uid") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "Jon Gjengset",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="get_author_by_uid")
def fixture_get_author_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the get_author_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.authors.crud.get_author_by_uid") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "Jon Gjengset",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="delete_author_by_uid")
def fixture_delete_author_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the delete_author_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.authors.crud.delete_author_by_uid") as mocked:
        yield mocked


def test_list_authors(
    client: testclient.TestClient,
    list_authors: mock.MagicMock,
    total_authors: mock.MagicMock,
) -> None:
    """Should return a JSON formatted list of authors from the database.

    Args:
        client: API test client.
        list_authors: Mocked authors database utility.
        total_authors: Mocked authors database utility.
    """
    response: requests.Response = client.get(BASE_PATH)
    data: dict[str, t.Any] = response.json()

    list_authors.assert_called()
    total_authors.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.AuthorList(**data)


def test_list_authors_paginate_default(
    client: testclient.TestClient,
    list_authors: mock.MagicMock,
) -> None:
    """Should paginate the results using defaults.

    Args:
        client: API test client.
        list_authors: Mocked authors database utility.
    """
    cfg = config.get_config()
    client.get(BASE_PATH)
    list_authors.assert_called_with(
        limit=cfg.database_pagination_limit, offset=0
    )


def test_list_authors_paginate(
    client: testclient.TestClient,
    list_authors: mock.MagicMock,
) -> None:
    """Should paginate the results using the provided query parameters.

    Args:
        client: API test client.
        list_authors: Mocked authors database utility.
    """
    params: dict[str, int] = {
        "limit": 10,
        "offset": 10,
    }
    client.get(BASE_PATH, params=params)
    list_authors.assert_called_with(
        limit=params.get("limit"), offset=params.get("offset")
    )


def test_list_authors_validates_limit(
    client: testclient.TestClient,
    list_authors: mock.MagicMock,
    total_authors: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid limit query param.

    Args:
        client: API test client.
        list_authors: Mocked authors database utility.
        total_authors: Mocked authors database utility.
    """
    params: dict[str, int] = {"limit": -10}
    response: requests.Response = client.get(BASE_PATH, params=params)
    data: dict[str, t.Any] = response.json()

    list_authors.assert_not_called()
    total_authors.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert server_schema.Error(**data)


def test_list_authors_validates_offset(
    client: testclient.TestClient,
    list_authors: mock.MagicMock,
    total_authors: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid offset query param.

    Args:
        client: API test client.
        list_authors: Mocked authors database utility.
        total_authors: Mocked authors database utility.
    """
    params: dict[str, int] = {"offset": -10}
    response: requests.Response = client.get(BASE_PATH, params=params)
    data: dict[str, t.Any] = response.json()

    list_authors.assert_not_called()
    total_authors.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert server_schema.Error(**data)


def test_create_author(
    client: testclient.TestClient,
    create_author: mock.MagicMock,
) -> None:
    """Should create an author from a JSON request body.

    Args:
        client: API test client.
        create_author: Mocked authors database utility.
    """
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    create_author.assert_called()

    assert response.status_code == status.HTTP_201_CREATED
    assert schemas.Author(**data)


def test_create_author_invalid(
    client: testclient.TestClient,
    create_author: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid request body.

    Args:
        client: API test client.
        create_author: Mocked authors database utility.
    """
    body: dict[str, t.Any] = {}
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)

    create_author.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mock.patch("app.api.v1.authors.router.validators.check_content_length")
def test_create_author_missing_content_length(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    create_author: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for no content-length header.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        create_author: Mocked authors database utility.
    """
    check_content_length.side_effect = errors.ContentLengthMissing(
        detail="Content length header is missing."
    )

    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    create_author.assert_not_called()

    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.authors.router.validators.check_content_length")
def test_create_author_content_length_exceeded(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    create_author: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when the request body is too large.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        create_author: Mocked authors database utility.
    """
    check_content_length.side_effect = errors.ContentLengthExceeded(
        detail="Content length exceeded",
    )

    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    create_author.assert_not_called()

    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert server_schema.Error(**data)


def test_get_author_by_uid(
    client: testclient.TestClient, get_author_by_uid: mock.MagicMock
) -> None:
    """Should return a JSON formatted author.

    Args:
        client: API test client.
        get_author_by_uid: Mocked authors database utility.
    """
    uid = 1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_author_by_uid.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.Author(**data)


def test_get_author_by_uid_not_found(
    client: testclient.TestClient, get_author_by_uid: mock.MagicMock
) -> None:
    """Should return a JSON formatted error when no author has been found.

    Args:
        client: API test client.
        get_author_by_uid: Mocked authors database utility.
    """
    get_author_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = 1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_author_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


def test_get_author_by_uid_invalid_uid(
    client: testclient.TestClient,
    get_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        client: API test client.
        get_author_by_uid: Mocked authors database utility.
    """
    uid = -1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_author_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


def test_update_author_by_uid(
    client: testclient.TestClient,
    update_author_by_uid: mock.MagicMock,
) -> None:
    """Should update an existing author from a JSON request body.

    Args:
        client: API test client.
        update_author_by_uid: Mocked authors database utility.
    """
    uid = 1
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    update_author_by_uid.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.Author(**data)


def test_update_author_by_uid_not_found(
    client: testclient.TestClient,
    update_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when no author has been found.

    Args:
        client: API test client.
        update_author_by_uid: Mocked authors database utility.
    """
    update_author_by_uid.side_effect = errors.NotFound(detail="Not found")

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    update_author_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.authors.router.validators.is_identifier")
def test_update_author_by_uid_invalid_uid(
    is_identifier: mock.MagicMock,
    client: testclient.TestClient,
    update_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        is_identifier: Mocked validation utility.
        client: API test client.
        update_author_by_uid: Mocked authors database utility.
    """
    is_identifier.return_value = False

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    is_identifier.assert_called()
    update_author_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.authors.router.validators.check_content_length")
def test_update_author_by_uid_content_length_missing(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    update_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for no content-length header.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        update_author_by_uid: Mocked authors database utility.
    """
    check_content_length.side_effect = errors.ContentLengthMissing(
        detail="Content length header is missing."
    )

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    update_author_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.authors.router.validators.check_content_length")
def test_update_author_by_uid_content_length_exceeded(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    update_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when the request body is too large.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        update_author_by_uid: Mocked authors database utility.
    """
    check_content_length.side_effect = errors.ContentLengthExceeded(
        detail="Request body too large."
    )

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Jon Gjengset",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    update_author_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert server_schema.Error(**data)


def test_update_author_by_uid_invalid(
    client: testclient.TestClient,
    update_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid request body.

    Args:
        client: API test client.
        update_author_by_uid: Mocked authors database utility.
    """
    uid = 1
    body: dict[str, t.Any] = {}
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)

    update_author_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_author_by_uid(
    client: testclient.TestClient,
    delete_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a NO_CONTENT response.

    Args:
        client: API test client.
        delete_author_by_uid: Mocked authors database utility.
    """
    uid = 1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")

    delete_author_by_uid.assert_called()

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_author_by_uid_not_found(
    client: testclient.TestClient,
    delete_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when no author has been found.

    Args:
        client: API test client.
        delete_author_by_uid: Mocked author database utility.
    """
    delete_author_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = 1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    delete_author_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


def test_delete_author_by_uid_invalid_uid(
    client: testclient.TestClient,
    delete_author_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        client: API test client.
        delete_author_by_uid: Mocked author database utility.
    """
    delete_author_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = -1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    delete_author_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)
