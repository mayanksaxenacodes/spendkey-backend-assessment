# Copyright © 2026 SpendKey. All Rights Reserved.
"""Author data serialization utilities."""
import typing as t
from datetime import datetime

from app.api.v1.authors import schemas


def to_author_list(
    rows: list[dict[str, t.Any]], total: int
) -> schemas.AuthorList:
    """Creates an OpenAPI schema formatted authors list.

    Args:
        rows: Rows from the authors table as a list of dict items.
        total: Int representing the total number of rows in the table.

    Returns:
        AuthorList object.
    """
    return schemas.AuthorList(
        data=[to_author(row=row) for row in rows],
        total=total,
    )


def to_author(row: dict[str, t.Any]) -> schemas.Author:
    """Create an OpenAPI schema formatted author.

    Args:
        row: Dict representing a row from the authors table.

    Returns:
        Author object.
    """
    return schemas.Author(
        id=row.get("id", 0),
        name=row.get("name", ""),
        created_at=row.get("created_at", datetime.now()),
        updated_at=row.get("updated_at", datetime.now()),
    )
