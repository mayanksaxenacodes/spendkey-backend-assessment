# Copyright © 2026 SpendKey. All Rights Reserved.
"""Books serializer tests."""
import typing as t
from datetime import datetime

from app.api.v1.books import schemas, serializers

TOTAL: int = 1
ROW: dict[str, t.Any] = {
    "id": 1,
    "name": "Foo",
    "isbn": "abc-123",
    "price": 999,
    "author_id": 1,
    "publisher_id": 1,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


def to_book() -> None:
    """Should return a book schema."""
    assert isinstance(serializers.to_book(row=ROW), schemas.Book)


def to_book_list() -> None:
    """Should return a book list schema."""
    assert isinstance(
        serializers.to_book_list(rows=[ROW], total=TOTAL), schemas.BookList
    )
