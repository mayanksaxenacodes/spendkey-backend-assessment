# Copyright © 2026 SpendKey. All Rights Reserved.
"""Custom FastAPI responses."""
import typing as t

import orjson
from fastapi import responses


class OrJSONResponse(responses.JSONResponse):
    """High-performance JSON encoding."""

    media_type = "application/json;charset=utf-8"

    def render(self, content: t.Any) -> bytes:
        """JSON response encoding which uses orjson.

        Args:
            content: Data to encode as JSON.

        Returns:
            JSON encoded bytes.
        """
        return orjson.dumps(content)  # pylint: disable=no-member
