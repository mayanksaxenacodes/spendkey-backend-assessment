# Copyright © 2026 SpendKey. All Rights Reserved.
"""Authors serializer tests."""
import typing as t
from datetime import datetime

from app.api.v1.authors import schemas, serializers

TOTAL: int = 1
ROW: dict[str, t.Any] = {
    "id": 1,
    "name": "Foo",
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


def to_author() -> None:
    """Should return a author schema."""
    assert isinstance(serializers.to_author(row=ROW), schemas.Author)


def to_author_list() -> None:
    """Should return a author list schema."""
    assert isinstance(
        serializers.to_author_list(rows=[ROW], total=TOTAL), schemas.AuthorList
    )
