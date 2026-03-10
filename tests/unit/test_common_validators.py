# Copyright © 2026 SpendKey. All Rights Reserved.
"""Input validation utility tests."""
from unittest import mock

import pytest

from app.common import errors, validators


def test_is_limit() -> None:
    """Should validate `limit` query parameter."""

    assert validators.is_limit(limit=1)
    assert validators.is_limit(limit=10)
    assert validators.is_limit(limit=100)

    assert not validators.is_limit(limit=0)
    assert not validators.is_limit(limit=-1)
    assert not validators.is_limit(limit=101)


def test_is_offset() -> None:
    """Should validate the `offset` query parameter."""

    assert validators.is_offset(offset=0)
    assert validators.is_offset(offset=1)
    assert validators.is_offset(offset=10)
    assert validators.is_offset(offset=100)

    assert not validators.is_offset(offset=-1)
    assert not validators.is_offset(offset=-100)


def test_is_identifier() -> None:
    """Should validate a row's unique identifier."""

    assert validators.is_identifier(identifier=1)
    assert validators.is_identifier(identifier=10)
    assert validators.is_identifier(identifier=100)

    assert not validators.is_identifier(identifier=0)
    assert not validators.is_identifier(identifier=-10)


def test_check_content_length_missing() -> None:
    """Should raise an exception if the content-length header is missing."""
    with pytest.raises(errors.ContentLengthMissing):
        request = mock.MagicMock()
        request.headers = {}
        validators.check_content_length(request=request)


def test_check_content_length_exceeded() -> None:
    """Should raise an exception if the content-length is too large."""
    content_length = 512000 * 1000
    with pytest.raises(errors.ContentLengthExceeded):
        request = mock.MagicMock()
        request.headers = {
            "Content-Length": f"{content_length}",
        }
        validators.check_content_length(request=request)
