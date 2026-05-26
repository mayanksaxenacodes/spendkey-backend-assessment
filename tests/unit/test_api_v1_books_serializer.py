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
    "ai_summary": "A great book.",
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
}


def test_to_book() -> None:
    """Should return a book schema."""
    res = serializers.to_book(row=ROW)
    assert isinstance(res, schemas.Book)
    assert res.ai_summary == "A great book."


def test_to_book_list() -> None:
    """Should return a book list schema."""
    res = serializers.to_book_list(rows=[ROW], total=TOTAL)
    assert isinstance(res, schemas.BookList)
    assert res.data[0].ai_summary == "A great book."
