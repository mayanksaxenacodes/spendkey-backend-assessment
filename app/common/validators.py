# Copyright © 2026 SpendKey. All Rights Reserved.
"""Input validation utilities."""
import fastapi

from app.common import errors


def is_limit(limit: int) -> bool:
    """Validate the limit query parameter used on HTTP listing endpoints.

    The limit value must the following criteria:

    - Be a Python3.7+ int type.
    - Be a positive integer.
    - Be less than or equal to 100.

    Examples:
        >>> is_limit(limit=-10)
        False
        >>> is_limit(limit=1000)
        False
        >>> is_limit(limit=10)
        True

    Args:
        limit: A limit query parameter from a HTTP route.

    Returns:
        True if the provided limit is valid, False if it's not.
    """
    return 0 < limit <= 100


def is_offset(offset: int) -> bool:
    """Validates the offset query parameter used on HTTP listing endpoints.

    The offset value must meet the following criteria:

    - Be a Python3.7+ int type.
    - Be a positive integer.

    Examples:
        >>> is_offset(offset=-1)
        False
        >>>is_offset(offset=10)
        True

    Args:
        offset: An offset query parameter from a HTTP route.

    Returns:
        True if the provided offset is valid, False if it's not.
    """
    return offset >= 0


def is_identifier(identifier: int) -> bool:
    """Validates the path identifier parameter on HTTP endpoints.

    The database automatically generates numeric incrementing identifiers
    when creating a row. These must meet the following criteria:

    - Be a Python3.7+ int type.
    - Be a positive integer.

    Examples:
        >>> is_identifier(identifier=-10)
        False
        >>> is_identifier(identifier=0)
        False
        >>> is_identifier(identifier=10)
        True

    Args:
        identifier: A unique identifier for a database row.

    Returns:
        True if the provided identifier is valid, False if it's not.
    """
    return identifier > 0


def check_content_length(request: fastapi.Request) -> None:
    """Checks the `Content-Length` header on the given request.

    Args:
        request: HTTP request object from FastAPI.

    Raises:
        ContentLengthMissing: If the `content-length` header is missing.
        ContentLengthExceeded: If the request body exceeds the permitted size.
    """
    if "Content-Length" not in request.headers:
        raise errors.ContentLengthMissing(
            detail="Content-Length header required.",
        )

    # Get the Content-Length value and convert it from bytes to kilobytes.
    content_length = round(int(request.headers.get("Content-Length")) / 1024)

    # If the request body is larger than 32MB then we can't accept it.
    if content_length > 32000:
        raise errors.ContentLengthExceeded(detail="Request body too large.")
