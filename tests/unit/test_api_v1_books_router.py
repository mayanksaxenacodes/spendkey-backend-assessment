# Copyright © 2026 SpendKey. All Rights Reserved.
"""Books router tests."""
import typing as t
from datetime import datetime
from unittest import mock

import fastapi
import pytest
import requests
from fastapi import status, testclient

from app import config
from app.api.v1.books import schemas
from app.api.v1.books.router import import_books
from app.common import errors
from app.server import schemas as server_schema

BASE_PATH: str = "/api/v1/books"


@pytest.fixture(name="total_books")
def fixture_total_books() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the total_books database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.books.crud.total_books") as mocked:
        mocked.return_value = 9
        yield mocked


@pytest.fixture(name="list_books")
def fixture_list_books() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the list_books database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.books.crud.list_books") as mocked:
        row: dict[str, t.Any] = {
            "id": 1,
            "name": "Rust for Rustaceans",
            "description": "For developers who've mastered the basics, Rust "
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
            "isbn": "978-1-7185-0185-0",
            "price": 3699,
            "tags": ["computers", "programming"],
            "author_id": 1,
            "publisher_id": 1,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        mocked.return_value = [row]
        yield mocked


@pytest.fixture(name="create_book")
def fixture_create_book() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the create_books database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.books.crud.create_book") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "Rust for Rustaceans",
            "description": "For developers who've mastered the basics, Rust "
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
            "isbn": "978-1-7185-0185-0",
            "price": 3699,
            "tags": ["computers", "programming"],
            "author_id": 1,
            "publisher_id": 1,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="update_book_by_uid")
def fixture_update_book_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the update_book_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.books.crud.update_book_by_uid") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "Rust for Rustaceans",
            "description": "For developers who've mastered the basics, Rust "
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
            "isbn": "978-1-7185-0185-0",
            "price": 3699,
            "tags": ["computers", "programming"],
            "author_id": 1,
            "publisher_id": 1,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="get_book_by_uid")
def fixture_get_book_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the get_book_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.books.crud.get_book_by_uid") as mocked:
        mocked.return_value = {
            "id": 1,
            "name": "Rust for Rustaceans",
            "description": "For developers who've mastered the basics, Rust "
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
            "isbn": "978-1-7185-0185-0",
            "price": 3699,
            "tags": ["computers", "programming"],
            "author_id": 1,
            "publisher_id": 1,
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }
        yield mocked


@pytest.fixture(name="delete_book_by_uid")
def fixture_delete_book_by_uid() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the delete_book_by_uid database utility.

    Yields:
        Mocked CRUD utility.
    """
    with mock.patch("app.api.v1.books.crud.delete_book_by_uid") as mocked:
        yield mocked


def test_list_books(
    client: testclient.TestClient,
    list_books: mock.MagicMock,
    total_books: mock.MagicMock,
) -> None:
    """Should return a JSON formatted list of books from the database.

    Args:
        client: API test client.
        list_books: Mocked books database utility.
        total_books: Mocked books database utility.
    """
    response: requests.Response = client.get(BASE_PATH)
    data: dict[str, t.Any] = response.json()

    list_books.assert_called()
    total_books.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.BookList(**data)


def test_list_books_paginate_default(
    client: testclient.TestClient,
    list_books: mock.MagicMock,
) -> None:
    """Should paginate the results using defaults.

    Args:
        client: API test client.
        list_books: Mocked books database utility.
    """
    cfg = config.get_config()
    client.get(BASE_PATH)
    list_books.assert_called_with(
        limit=cfg.database_pagination_limit, offset=0
    )


def test_list_books_paginate(
    client: testclient.TestClient,
    list_books: mock.MagicMock,
) -> None:
    """Should paginate the results using the provided query parameters.

    Args:
        client: API test client.
        list_books: Mocked books database utility.
    """
    params: dict[str, int] = {
        "limit": 10,
        "offset": 10,
    }
    client.get(BASE_PATH, params=params)
    list_books.assert_called_with(
        limit=params.get("limit"), offset=params.get("offset")
    )


def test_list_books_validates_limit(
    client: testclient.TestClient,
    list_books: mock.MagicMock,
    total_books: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid limit query param.

    Args:
        client: API test client.
        list_books: Mocked books database utility.
        total_books: Mocked books database utility.
    """
    params: dict[str, int] = {"limit": -10}
    response: requests.Response = client.get(BASE_PATH, params=params)
    data: dict[str, t.Any] = response.json()

    list_books.assert_not_called()
    total_books.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert server_schema.Error(**data)


def test_list_books_validates_offset(
    client: testclient.TestClient,
    list_books: mock.MagicMock,
    total_books: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid offset query param.

    Args:
        client: API test client.
        list_books: Mocked books database utility.
        total_books: Mocked books database utility.
    """
    params: dict[str, int] = {"offset": -10}
    response: requests.Response = client.get(BASE_PATH, params=params)
    data: dict[str, t.Any] = response.json()

    list_books.assert_not_called()
    total_books.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert server_schema.Error(**data)


def test_create_book(
    client: testclient.TestClient,
    create_book: mock.MagicMock,
) -> None:
    """Should create a book from a JSON request body.

    Args:
        client: API test client.
        create_book: Mocked books database utility.
    """
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    create_book.assert_called()

    assert response.status_code == status.HTTP_201_CREATED
    assert schemas.Book(**data)


def test_create_book_invalid(
    client: testclient.TestClient,
    create_book: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid request body.

    Args:
        client: API test client.
        create_book: Mocked books database utility.
    """
    body: dict[str, t.Any] = {}
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)

    create_book.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mock.patch("app.api.v1.books.router.validators.check_content_length")
def test_create_book_missing_content_length(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    create_book: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for no content-length header.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        create_book: Mocked books database utility.
    """
    check_content_length.side_effect = errors.ContentLengthMissing(
        detail="Content length header is missing."
    )

    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    create_book.assert_not_called()

    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.books.router.validators.check_content_length")
def test_create_book_content_length_exceeded(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    create_book: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when the request body is too large.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        create_book: Mocked books database utility.
    """
    check_content_length.side_effect = errors.ContentLengthExceeded(
        detail="Content length exceeded",
    )

    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.post(f"{BASE_PATH}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    create_book.assert_not_called()

    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert server_schema.Error(**data)


def test_get_book_by_uid(
    client: testclient.TestClient, get_book_by_uid: mock.MagicMock
) -> None:
    """Should return a JSON formatted book.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    uid = 1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_book_by_uid.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.Book(**data)


def test_get_book_by_uid_not_found(
    client: testclient.TestClient, get_book_by_uid: mock.MagicMock
) -> None:
    """Should return a JSON formatted error when no book has been found.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    get_book_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = 1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_book_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


def test_get_book_by_uid_invalid_uid(
    client: testclient.TestClient,
    get_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    uid = -1
    response: requests.Response = client.get(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    get_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


def test_update_book_by_uid(
    client: testclient.TestClient,
    update_book_by_uid: mock.MagicMock,
) -> None:
    """Should update an existing book from a JSON request body.

    Args:
        client: API test client.
        update_book_by_uid: Mocked books database utility.
    """
    uid = 1
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    update_book_by_uid.assert_called()

    assert response.status_code == status.HTTP_200_OK
    assert schemas.Book(**data)


def test_update_book_by_uid_not_found(
    client: testclient.TestClient,
    update_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when no book has been found.

    Args:
        client: API test client.
        update_book_by_uid: Mocked books database utility.
    """
    update_book_by_uid.side_effect = errors.NotFound(detail="Not found")

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    update_book_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.books.router.validators.is_identifier")
def test_update_book_by_uid_invalid_uid(
    is_identifier: mock.MagicMock,
    client: testclient.TestClient,
    update_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        is_identifier: Mocked validation utility.
        client: API test client.
        update_book_by_uid: Mocked books database utility.
    """
    is_identifier.return_value = False

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    is_identifier.assert_called()
    update_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.books.router.validators.check_content_length")
def test_update_book_by_uid_content_length_missing(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    update_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for no content-length header.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        update_book_by_uid: Mocked books database utility.
    """
    check_content_length.side_effect = errors.ContentLengthMissing(
        detail="Content length header is missing."
    )

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    update_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert server_schema.Error(**data)


@mock.patch("app.api.v1.books.router.validators.check_content_length")
def test_update_book_by_uid_content_length_exceeded(
    check_content_length: mock.MagicMock,
    client: testclient.TestClient,
    update_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when the request body is too large.

    Args:
        check_content_length: Mocked validation utility.
        client: API test client.
        update_book_by_uid: Mocked books database utility.
    """
    check_content_length.side_effect = errors.ContentLengthExceeded(
        detail="Request body too large."
    )

    uid = 1
    body: dict[str, t.Any] = {
        "name": "Rust for Rustaceans",
        "description": "For developers who've mastered the basics, Rust "
        "for Rustaceans is the next step on your way to "
        "professional level programming in Rust.",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers", "programming"],
        "author_id": 1,
        "publisher_id": 1,
    }
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)
    data: dict[str, t.Any] = response.json()

    check_content_length.assert_called()
    update_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert server_schema.Error(**data)


def test_update_book_by_uid_invalid(
    client: testclient.TestClient,
    update_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid request body.

    Args:
        client: API test client.
        update_book_by_uid: Mocked books database utility.
    """
    uid = 1
    body: dict[str, t.Any] = {}
    response: requests.Response = client.put(f"{BASE_PATH}/{uid}/", json=body)

    update_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_book_by_uid(
    client: testclient.TestClient,
    delete_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a NO_CONTENT response.

    Args:
        client: API test client.
        delete_book_by_uid: Mocked books database utility.
    """
    uid = 1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")

    delete_book_by_uid.assert_called()

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_book_by_uid_not_found(
    client: testclient.TestClient,
    delete_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error when no book has been found.

    Args:
        client: API test client.
        delete_book_by_uid: Mocked books database utility.
    """
    delete_book_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = 1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    delete_book_by_uid.assert_called()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)


def test_delete_book_by_uid_invalid_uid(
    client: testclient.TestClient,
    delete_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a JSON formatted error for an invalid identifier.

    Args:
        client: API test client.
        delete_book_by_uid: Mocked books database utility.
    """
    delete_book_by_uid.side_effect = errors.NotFound(detail="Not Found")

    uid = -1
    response: requests.Response = client.delete(f"{BASE_PATH}/{uid}/")
    data: dict[str, t.Any] = response.json()

    delete_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


def test_summarise_book_success(
    client: testclient.TestClient,
    get_book_by_uid: mock.MagicMock,
) -> None:
    """Should successfully generate and persist a book summary.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    with mock.patch("app.api.v1.books.llm.generate_summary") as mock_gen, \
         mock.patch("app.api.v1.books.crud.update_book_summary") as mock_update:
        
        mock_gen.return_value = "This is a generated AI summary."
        mock_update.return_value = {
            "id": 1,
            "name": "Rust for Rustaceans",
            "description": "For developers who've mastered the basics, Rust "
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
            "isbn": "978-1-7185-0185-0",
            "price": 3699,
            "tags": ["computers", "programming"],
            "author_id": 1,
            "publisher_id": 1,
            "ai_summary": "This is a generated AI summary.",
            "created_on": datetime.now(),
            "updated_on": datetime.now(),
        }

        response: requests.Response = client.post(f"{BASE_PATH}/1/summarise")
        data: dict[str, t.Any] = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data["ai_summary"] == "This is a generated AI summary."
        get_book_by_uid.assert_called_once_with(uid=1)
        mock_gen.assert_called_once_with(
            book_title="Rust for Rustaceans",
            description="For developers who've mastered the basics, Rust "
            "for Rustaceans is the next step on your way to "
            "professional level programming in Rust.",
        )
        mock_update.assert_called_once_with(uid=1, summary="This is a generated AI summary.")


def test_summarise_book_not_found(
    client: testclient.TestClient,
    get_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a 404 response if the book does not exist.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    get_book_by_uid.side_effect = errors.NotFound(detail="Not Found")

    response: requests.Response = client.post(f"{BASE_PATH}/999/summarise")
    data: dict[str, t.Any] = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert server_schema.Error(**data)
    assert data["detail"] == "Not Found"


def test_summarise_book_invalid_uid(
    client: testclient.TestClient,
    get_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a 400 response for an invalid identifier.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    response: requests.Response = client.post(f"{BASE_PATH}/-5/summarise")
    data: dict[str, t.Any] = response.json()

    get_book_by_uid.assert_not_called()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert server_schema.Error(**data)


def test_summarise_book_llm_failure(
    client: testclient.TestClient,
    get_book_by_uid: mock.MagicMock,
) -> None:
    """Should return a 500 response with descriptive error if LLM fails.

    Args:
        client: API test client.
        get_book_by_uid: Mocked books database utility.
    """
    get_book_by_uid.return_value = {
        "id": 1,
        "name": "Rust for Rustaceans",
        "description": "Description",
        "isbn": "978-1-7185-0185-0",
        "price": 3699,
        "tags": ["computers"],
        "author_id": 1,
        "publisher_id": 1,
        "created_on": datetime.now(),
        "updated_on": datetime.now(),
    }
    with mock.patch("app.api.v1.books.llm.generate_summary") as mock_gen:
        mock_gen.side_effect = Exception("OpenAI API key invalid or not provided")

        response: requests.Response = client.post(f"{BASE_PATH}/1/summarise")
        data: dict[str, t.Any] = response.json()

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert server_schema.Error(**data)
        assert "Failed to generate summary: OpenAI API key invalid or not provided" in data["detail"]
