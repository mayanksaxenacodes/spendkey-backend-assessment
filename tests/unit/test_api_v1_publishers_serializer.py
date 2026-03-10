# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publishers serializer tests."""
import typing as t
from datetime import datetime

from app.api.v1.publishers import schemas, serializers

TOTAL: int = 1
ROW: dict[str, t.Any] = {
    "id": 1,
    "name": "Foo",
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


def to_publisher() -> None:
    """Should return a publisher schema."""
    assert isinstance(serializers.to_publisher(row=ROW), schemas.Publisher)


def to_publisher_list() -> None:
    """Should return a publisher list schema."""
    assert isinstance(
        serializers.to_publisher_list(rows=[ROW], total=TOTAL),
        schemas.PublisherList,
    )
