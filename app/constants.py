# Copyright © 2026 SpendKey. All Rights Reserved.
"""Static application runtime values."""
import enum
import typing as t

import pydantic
from psycopg import sql


class TableNames(enum.Enum):
    """Valid database table names."""

    AUTHOR = sql.Identifier("authors", "author")
    BOOK = sql.Identifier("books", "book")
    PUBLISHER = sql.Identifier("publishers", "publisher")


class Tag(pydantic.BaseModel):  # pylint: disable=no-member,too-few-public-methods
    """OpenAPI documentation tag."""

    name: str
    description: t.Optional[str]


# Provides additional information to the router tags.
TAGS_METADATA: list[Tag] = [
    Tag(
        name="authors",
        description="Manage authors of the books we currently have available.",
    ),
    Tag(
        name="books",
        description="Manage books which are currently available.",
    ),
    Tag(
        name="publishers",
        description="Manage the publishers who provide our book inventory.",
    ),
    Tag(
        name="recommendations",
        description="AI-powered book recommendation engine.",
    ),
]

# Values considered truthy when handling user input.
TRUTHY_VALUES: list[str] = [
    "active",
    "activated",
    "true",
    "yes",
    "y",
    "enable",
    "enabled",
]
