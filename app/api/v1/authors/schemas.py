# pylint: disable=no-member,too-few-public-methods
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Author OpenAPI schemas."""
import datetime
import typing as t

import pydantic


class Author(pydantic.BaseModel):
    """Row from the authors table in the database."""

    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AuthorList(pydantic.BaseModel):
    """Properties in the JSON response for listing authors."""

    total: t.Optional[int] = 0
    data: t.Optional[list[Author]] = []


class AuthorBody(pydantic.BaseModel):
    """Properties in the JSON request body."""

    name: str
