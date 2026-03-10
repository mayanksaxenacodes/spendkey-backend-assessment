# Copyright © 2026 SpendKey. All Rights Reserved.
"""HTTP response utility tests."""
from fastapi.responses import JSONResponse

from app.common import responses


def test_orjson_response() -> None:
    """Should be an instance of JSONResponse."""
    assert issubclass(responses.OrJSONResponse, JSONResponse)


def test_orjson_media_type() -> None:
    """Should include a media type."""
    response = responses.OrJSONResponse(content={})
    assert hasattr(response, "media_type")


def test_orjson_media_type_charset() -> None:
    """Should set a charset on the media type."""
    response = responses.OrJSONResponse(content={})
    assert response.media_type == "application/json;charset=utf-8"


def test_orjson_response_render() -> None:
    """Should return data as JSON."""
    content: dict[str, str] = {"foo": "bar"}
    response = responses.OrJSONResponse(content={})
    assert response.render(content=content) == b'{"foo":"bar"}'
