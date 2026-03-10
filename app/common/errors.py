# Copyright © 2026 SpendKey. All Rights Reserved.
"""Application error types."""


class ErrorBase(Exception):
    """Base application exception type.

    Attributes:
        detail: Error message details.
    """

    detail: str

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(self.detail)


class Conflict(ErrorBase):
    """Occurs when a duplication is detected."""


class NotFound(ErrorBase):
    """Occurs when the requested database entry isn't found."""


class ContentLengthMissing(ErrorBase):
    """Occurs when the request doesn't include a `Content-Length` header."""


class ContentLengthExceeded(ErrorBase):
    """Occurs when the request `Content-Length` exceeds the permitted size."""
