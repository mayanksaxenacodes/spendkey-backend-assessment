# pylint: disable=no-member,too-few-public-methods
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publisher OpenAPI schemas."""
import datetime
import typing as t

import pydantic


class Publisher(pydantic.BaseModel):
    """Row from the publishers table in the database."""

    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PublisherList(pydantic.BaseModel):
    """Properties in the JSON response for listing publishers."""

    total: t.Optional[int] = 0
    data: t.Optional[list[Publisher]] = []


class PublisherBody(pydantic.BaseModel):
    """Properties in the JSON body."""

    name: str
