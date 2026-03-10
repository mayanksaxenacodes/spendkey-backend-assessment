# pylint: disable=unused-variable
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Server exception handler tests."""
import os
import typing as t
from unittest import mock

import fastapi
import pytest
from fastapi import status, testclient
from fastapi.middleware import cors
from requests import Response

from app import config
from app.server import exceptions, schemas


@pytest.fixture(name="exception_client")
def fixture_exception_client() -> t.Iterator[testclient.TestClient]:
    """FastAPI test client fixture.

    This fixture uses a FastAPI instance which includes the exception handler
    used by the application. This isolates these tests, allowing us to cover
    functionality provided by the exception handler.

    Yields:
        FastAPI test client.
    """
    with mock.patch.dict(
        os.environ, {"CORS_ORIGINS": "http://localhost:4200"}
    ):
        app = fastapi.FastAPI()
        cfg = config.get_config()

        # Setup cross-origin resource sharing.
        app.add_middleware(
            cors.CORSMiddleware,
            allow_origins=cfg.cors_origins,
            allow_credentials=True,
            allow_methods=cfg.cors_methods,
            allow_headers=cfg.cors_headers,
        )

        exceptions.attach_exception_handlers(app=app, cfg=cfg)

        @app.get("/")
        def server_error() -> None:  # type: ignore
            """Endpoint for testing the exception handler.

            Raises:
                HTTPException: When the server cannot fulfill the request.
            """
            raise fastapi.HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal error",
            )

        yield testclient.TestClient(app)


def test_server_exceptions(exception_client: testclient.TestClient) -> None:
    """Should respond with a JSON formatted error.

    Args:
        exception_client: API test client.
    """
    response: Response = exception_client.get("/")
    data: dict[str, t.Any] = response.json()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert all(key in data for key in schemas.Error.__fields__.keys())


def test_server_exceptions_cors(
    exception_client: testclient.TestClient,
) -> None:
    """Should respond with CORS enabled.

    Args:
        exception_client: API test client.
    """
    response: Response = exception_client.get("/")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.headers.get(
        "access-control-allow-origin"
    ) == response.headers.get("origin")


def test_server_exceptions_cors_restricted_origins(
    exception_client: testclient.TestClient,
) -> None:
    """Should respond with CORS origin when origins are restricted.

    Args:
        exception_client: API test client.
    """
    headers: dict[str, str] = {
        "origin": "http://localhost:4200",
    }
    response: Response = exception_client.get("/", headers=headers)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.headers.get("vary") == "Origin"
    assert response.headers.get("access-control-allow-origin") == headers.get(
        "origin"
    )


def test_server_exceptions_cors_cookie(
    exception_client: testclient.TestClient,
) -> None:
    """Should respond with specific origin when cookies are set.

    Args:
        exception_client: API test client.
    """
    headers: dict[str, str] = {
        "origin": "http://localhost:4200",
    }
    cookies: dict[str, str] = {"foo": "bar"}
    response: Response = exception_client.get(
        "/", headers=headers, cookies=cookies
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.headers.get("access-control-allow-origin") == headers.get(
        "origin"
    )
