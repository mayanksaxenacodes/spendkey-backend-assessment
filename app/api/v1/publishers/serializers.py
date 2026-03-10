# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publisher data serialization utilities."""
import typing as t
from datetime import datetime

from app.api.v1.publishers import schemas


def to_publisher_list(
    rows: list[dict[str, t.Any]], total: int
) -> schemas.PublisherList:
    """Creates an OpenAPI schema formatted publisher list.

    Args:
        rows: Rows from the publishers table as a list of dict items.
        total: Int representing the total number of rows in the table.

    Returns:
        PublisherList object.
    """
    return schemas.PublisherList(
        data=[to_publisher(row=row) for row in rows],
        total=total,
    )


def to_publisher(row: dict[str, t.Any]) -> schemas.Publisher:
    """Create an OpenAPI schema formatted publisher.

    Args:
        row: Dict representing a row from the publishers table.

    Returns:
        Publisher object.
    """
    return schemas.Publisher(
        id=row.get("id", 0),
        name=row.get("name", ""),
        created_at=row.get("created_at", datetime.now()),
        updated_at=row.get("updated_at", datetime.now()),
    )
