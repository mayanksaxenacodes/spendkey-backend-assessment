# pylint: disable=no-member,too-few-public-methods
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Book OpenAPI schemas."""
import datetime
import typing as t

import pydantic


class Book(pydantic.BaseModel):
    """Row from the books table in the database."""

    id: int
    name: str
    description: t.Optional[str]
    isbn: str
    tags: list[str]
    price: t.Optional[int]
    author_id: t.Optional[int]
    publisher_id: t.Optional[int]
    ai_summary: t.Optional[str] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class BookList(pydantic.BaseModel):
    """Properties in the JSON response for listing books."""

    total: t.Optional[int] = 0
    data: t.Optional[list[Book]] = []


class BookBody(pydantic.BaseModel):
    """Properties in the JSON request body."""

    name: str
    description: t.Optional[str]
    isbn: str
    tags: list[str]
    price: t.Optional[int]
    author_id: t.Optional[int]
    publisher_id: t.Optional[int]
