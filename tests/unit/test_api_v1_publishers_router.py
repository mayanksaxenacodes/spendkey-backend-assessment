# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publisher router tests."""
import typing as t
from datetime import datetime
from unittest import mock

import pytest
import requests
from fastapi import status, testclient

from app import config
from app.api.v1.publishers import schemas
from app.common import errors
from app.server import schemas as server_schema

BASE_PATH: str = "/api/v1/publishers"


@pytest.fixture(name="total_publishers")
def fixture_total_publishers() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the total_publishers database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.publishers.crud.total_publishers") as mocked:
        mocked.return_value = 9
        yield mocked


@pytest.fixture(name="list_publishers")
def fixture_list_publishers() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the list_publishers database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.publishers.crud.list_publishers") as mocked:
        row: dict[str, t.Any] = {
            "id": 1,
            "name": "",
            "created_on": "",
            "updated_on": "",
        }
        mocked.return_value = [row]
        yield mocked


@pytest.fixture(name="create_publisher")
def fixture_create_publisher() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the create_publisher database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.publishers.crud.create_publisher") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "No Starch Press",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="update_publisher_by_uid")
def fixture_update_publisher_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the update_publisher_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch(
        "app.api.v1.publishers.crud.update_publisher_by_uid"
    ) as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "No Starch Press",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="get_publisher_by_uid")
def fixture_get_publisher_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the get_publisher_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch(
        "app.api.v1.publishers.crud.get_publisher_by_uid"
    ) as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "No Starch Press",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="delete_publisher_by_uid")
def fixture_delete_publisher_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the delete_publisher_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch(
        "app.api.v1.publishers.crud.delete_publisher_by_uid"
    ) as mocked:
        yield mocked


def test_list_publishers(
    client: testclient.TestClient,
    list_publishers: mock.MagicMock,
    total_publishers: mock.MagicMock,
) -> None:
    """Should return a JSON formatted list of publishers from the database.

    Args:
        client: API test client.
        list_publishers: Mocked publishers database utility.
        total_publishers: Mocked publishers database utility.
    """
    response: requests.Response = client.get(BASE_PATH)
    data: dict[str, t.Any] = response.json()

    list_publishers.assert_called()
    total_publishers.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.PublisherList(**data)


def test_list_publishers_paginate_default(
    client: testclient.TestClient,
    list_publishers: mock.MagicMock,
) -> None:
    """Should paginate the results using defaults.

    Args:
        client: API test client.
        list_publishers: Mocked publishers database utility.
    """
    cfg = config.get_config()
    client.get(BASE_PATH)
    list_publishers.assert_called_with(
        limit=cfg.database_pagination_limit, offset=0
    )


def test_list_publishers_paginate(
    client: testclient.TestClient,
    list_publishers: mock.MagicMock,
) -> None:
    """Should paginate the results using the provided query parameters.

    Args:
        client: API test client.
        list_publishers: Mocked publishers database utility.
    """
    params: dict[str, int] = {
        "limit": 10,
        "offset": 10,
    }
    client.get(BASE_PATH, params=params)
    list_publishers.assert_called_with(
        limit=params.get("limit"), offset=params.get("offset")
    )


def test_list_publishers_validates_limit(
    client: testclient.TestClient,
    list_publishers: mock.MagicMock,
    total_publishers: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid limit query param.

    Args:
        client: API test client.
        list_publishers: Mocked publishers database utility.
        total_publishers: Mocked publishers database utility.
    """
    params: dict[str, int] = {"limit": -10}
    response: requests.Response = client.get(BASE_PATH, params=params)
    data: dict[str, t.Any] = response.json()

    list_publishers.assert_not_called()
    total_publishers.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert server_schema.Error(**data)


def test_list_publishers_validates_offset(
    client: testclient.TestClient,
    list_publishers: mock.MagicMock,
    total_publishers: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid offset query param.

    Args:
        client: API test client.
        list_publishers: Mocked publishers database utility.
        total_publishers: Mocked publishers database utility.
    """
    params: dict[str, int] = {"offset": -10}
    response: requests.Response = client.get(BASE_PATH, params=params)
    data: dict[str, t.Any] = response.json()

    list_publishers.assert_not_called()
    total_publishers.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert server_schema.Error(**data)


def test_create_publisher(
    client: testclient.TestClient,
    create_publisher: mock.MagicMock,
) -> None:
    """Should create a publisher from a JSON request body.

    Args:
        client: API test client.
        create_publisher: Mocked publishers database utility.
    """
    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    create_publisher.assert_called()

    assert response.status_code == status.HTTP_201_CREATED
    assert schemas.Publisher(**data)


def test_create_publisher_invalid(
    client: testclient.TestClient,
    create_publisher: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid request body.

    Args:
        client: API test client.
        create_publisher: Mocked publishers database utility.
    """
    body: dict[str, t.Any] = {}
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)

    create_publisher.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mock.patch("app.api.v1.publishers.router.validators.check_content_length")
def test_create_publisher_missing_content_length(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    create_publisher: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for no content-length header.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        create_publisher: Mocked publishers database utility.
    """
    check_content_length.side_effect = errors.ContentLengthMissing(
        detail="Content length header is missing."
    )

    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    create_publisher.assert_not_called()

    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.publishers.router.validators.check_content_length")
def test_create_publisher_content_length_exceeded(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    create_publisher: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when the request body is too large.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        create_publisher: Mocked publishers database utility.
    """
    check_content_length.side_effect = errors.ContentLengthExceeded(
        detail="Content length exceeded",
    )

    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    create_publisher.assert_not_called()

    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert server_schema.Error(**data)


def test_get_publisher_by_uid(
    client: testclient.TestClient, get_publisher_by_uid: mock.MagicMock
) -> None:
    """Should return a JSON formatted publisher.

    Args:
        client: API test client.
        get_publisher_by_uid: Mocked publishers database utility.
    """
    uid = 1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_publisher_by_uid.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.Publisher(**data)


def test_get_publisher_by_uid_not_found(
    client: testclient.TestClient, get_publisher_by_uid: mock.MagicMock
) -> None:
    """Should return a JSON formatted error when no publisher has been found.

    Args:
        client: API test client.
        get_publisher_by_uid: Mocked publishers database utility.
    """
    get_publisher_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = 1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_publisher_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


def test_get_publisher_by_uid_invalid_uid(
    client: testclient.TestClient,
    get_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        client: API test client.
        get_publisher_by_uid: Mocked publishers database utility.
    """
    uid = -1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_publisher_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


def test_update_publisher_by_uid(
    client: testclient.TestClient,
    update_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should update an existing publisher from a JSON request body.

    Args:
        client: API test client.
        update_publisher_by_uid: Mocked publishers database utility.
    """
    uid = 1
    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    update_publisher_by_uid.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.Publisher(**data)


def test_update_publisher_by_uid_not_found(
    client: testclient.TestClient,
    update_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when no publisher has been found.

    Args:
        client: API test client.
        update_publisher_by_uid: Mocked publishers database utility.
    """
    update_publisher_by_uid.side_effect = errors.NotFound(detail="Not found")

    uid = 1
    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    update_publisher_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.publishers.router.validators.is_identifier")
def test_update_publisher_by_uid_invalid_uid(
    is_identifier: mock.MagicMock,
    client: testclient.TestClient,
    update_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        is_identifier: Mocked validation utility.
        client: API test client.
        update_publisher_by_uid: Mocked publishers database utility.
    """
    is_identifier.return_value = False

    uid = 1
    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    is_identifier.assert_called()
    update_publisher_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.publishers.router.validators.check_content_length")
def test_update_publisher_by_uid_content_length_missing(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    update_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for no content-length header.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        update_publisher_by_uid: Mocked publishers database utility.
    """
    check_content_length.side_effect = errors.ContentLengthMissing(
        detail="Content length header is missing."
    )

    uid = 1
    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    update_publisher_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.publishers.router.validators.check_content_length")
def test_update_publisher_by_uid_content_length_exceeded(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    update_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when the request body is too large.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        update_publisher_by_uid: Mocked publishers database utility.
    """
    check_content_length.side_effect = errors.ContentLengthExceeded(
        detail="Request body too large."
    )

    uid = 1
    body: dict[str, t.Any] = {
        "name": "No Starch Press",
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    update_publisher_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert server_schema.Error(**data)


def test_update_publisher_by_uid_invalid(
    client: testclient.TestClient,
    update_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid request body.

    Args:
        client: API test client.
        update_publisher_by_uid: Mocked publishers database utility.
    """
    uid = 1
    body: dict[str, t.Any] = {}
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)

    update_publisher_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_publisher_by_uid(
    client: testclient.TestClient,
    delete_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a NO_CONTENT response.

    Args:
        client: API test client.
        delete_publisher_by_uid: Mocked publishers database utility.
    """
    uid = 1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")

    delete_publisher_by_uid.assert_called()

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_publisher_by_uid_not_found(
    client: testclient.TestClient,
    delete_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when no publisher has been found.

    Args:
        client: API test client.
        delete_publisher_by_uid: Mocked publishers database utility.
    """
    delete_publisher_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = 1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    delete_publisher_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


def test_delete_publisher_by_uid_invalid_uid(
    client: testclient.TestClient,
    delete_publisher_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        client: API test client.
        delete_publisher_by_uid: Mocked publishers database utility.
    """
    delete_publisher_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = -1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    delete_publisher_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)
