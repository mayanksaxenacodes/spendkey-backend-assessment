# pylint: disable=unused-variable
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Server setup and configuration tests."""
import os
from unittest import mock

import fastapi
from fastapi import status, testclient
from requests import Response

from app.server import factory


def test_server_openapi_route_disabled() -> None:
    """The OpenAPI route should be disabled by default."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    response: Response = client.get("/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()


@mock.patch.dict(os.environ, {"ENABLE_OPENAPI_DOCS": "y"})
def test_server_openapi_route_enabled() -> None:
    """The OpenAPI docs should be available when enabled."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    response: Response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_server_not_found() -> None:
    """Should return a JSON formatted error response."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    response: Response = client.get("/404")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()


def test_server_adds_process_time_header() -> None:
    """Should return a response with an x-process-time header."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    response: Response = client.get("/")

    assert "x-process-time" in response.headers


def test_server_adds_secure_headers() -> None:
    """Should return a response with secure headers."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    response: Response = client.get("/")

    assert response.headers.get("x-frame-options") == "SAMEORIGIN"
    assert response.headers.get("x-xss-protection") == "0"
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("cache-control") == "no-store"
    assert (
        response.headers.get("strict-transport-security")
        == "max-age=63072000; includeSubdomains"
    )
    assert (
        response.headers.get("referrer-policy")
        == "no-referrer, strict-origin-when-cross-origin"
    )


@mock.patch.dict(os.environ, {"ENABLE_OPENAPI_DOCS": "y"})
def test_server_cors_disabled() -> None:
    """Should return a response with CORS disabled by default."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    headers: dict[str, str] = {"origin": "http://localhost:4200"}
    response: Response = client.get("/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert "access-control-allow-origin" not in response.headers


@mock.patch.dict(
    os.environ,
    {"ENABLE_OPENAPI_DOCS": "y", "CORS_ORIGINS": "http://localhost:4200"},
)
def test_server_cors_enabled() -> None:
    """Should return a response with CORS enabled when configured."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    headers: dict[str, str] = {
        "origin": "http://localhost:4200",
        "access-control-request-method": "OPTIONS",
    }
    response: Response = client.options("/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("access-control-allow-origin") == headers.get(
        "origin"
    )


@mock.patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:4200"})
def test_server_cors_404() -> None:
    """Should return a 404 error with CORS enabled when configured."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    headers: dict[str, str] = {
        "origin": "http://localhost:4200",
    }
    response: Response = client.get("/404", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.headers.get("access-control-allow-origin") == headers.get(
        "origin"
    )


@mock.patch.dict(
    os.environ,
    {"ENABLE_OPENAPI_DOCS": "y", "CORS_ORIGINS": "http://localhost:4200"},
)
def test_server_cors_auth() -> None:
    """Should support CORS with credentials when configured."""
    app = factory.create_app()
    client = testclient.TestClient(app=app)

    headers: dict[str, str] = {
        "origin": "http://localhost:4200",
        "access-control-request-method": "OPTIONS",
    }
    response: Response = client.options("/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("access-control-allow-credentials")


@mock.patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:4200"})
def test_server_cors_internal_error() -> None:
    """Should return an internal error with CORS enabled when configured."""
    app = factory.create_app()

    @app.get("/")
    def server_error() -> None:  # type: ignore
        """Endpoint for returning errors to the test client.

        Raises:
            HTTPException: When the server cannot fulfill the request.
        """
        raise fastapi.HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    client = testclient.TestClient(app=app)

    headers: dict[str, str] = {
        "origin": "http://localhost:4200",
    }
    response: Response = client.get("/", headers=headers)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.headers.get("access-control-allow-origin") == headers.get(
        "origin"
    )
