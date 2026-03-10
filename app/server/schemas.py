# pylint: disable=too-few-public-methods
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Global OpenAPI schemas."""
import pydantic


class Error(pydantic.BaseModel):  # pylint: disable=no-member
    """Server error response properties."""

    detail: str
