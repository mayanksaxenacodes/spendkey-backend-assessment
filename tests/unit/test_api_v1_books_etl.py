# Copyright © 2026 SpendKey. All Rights Reserved.
"""ETL pipeline unit tests."""
import typing as t
from unittest import mock

import pytest

from app.api.v1.books import etl


# --- parse tests ---


SAMPLE_CSV = """title,author,publisher,description,isbn,price,tags
"The Pragmatic Programmer","David Thomas","Addison-Wesley","A guide","978-0-13-595705-9","$42.99","programming,software"
"Clean Code","Robert C. Martin","Prentice Hall","A handbook","978-0-13-235088-4",3899,"programming,clean-code"
"Design Patterns","Erich Gamma","Addison-Wesley","Elements of reusable OO","978-0201633610","$45.99","programming,design"
"""

SAMPLE_JSON = """[
  {"title": "SICP", "author": "Harold Abelson", "publisher": "MIT Press",
   "description": "CS fundamentals", "isbn": "978-0-26-251087-5",
   "price": "$54.99", "tags": ["computer-science", "programming"]},
  {"title": "", "author": "Nobody", "publisher": "None",
   "description": "Invalid", "isbn": "978-0-00-000001-7",
   "price": "$9.99", "tags": ["invalid"]}
]"""


def test_parse_csv() -> None:
    """Should parse CSV content into a list of dictionaries."""
    rows = etl.parse_csv(file_content=SAMPLE_CSV)
    assert len(rows) == 3
    assert rows[0]["title"] == "The Pragmatic Programmer"
    assert rows[0]["isbn"] == "978-0-13-595705-9"


def test_parse_json() -> None:
    """Should parse JSON content into a list of dictionaries."""
    rows = etl.parse_json(file_content=SAMPLE_JSON)
    assert len(rows) == 2
    assert rows[0]["title"] == "SICP"


# --- normalisation tests ---


def test_normalise_price_dollar_format() -> None:
    """Should convert dollar string to cents integer."""
    assert etl.normalise_price("$42.99") == 4299


def test_normalise_price_integer() -> None:
    """Should pass through an integer price unchanged."""
    assert etl.normalise_price(3899) == 3899


def test_normalise_price_integer_string() -> None:
    """Should convert a plain integer string to int."""
    assert etl.normalise_price("3899") == 3899


def test_normalise_price_empty() -> None:
    """Should return None for empty or missing price."""
    assert etl.normalise_price("") is None
    assert etl.normalise_price(None) is None


def test_normalise_isbn_hyphenated() -> None:
    """Should preserve a correctly hyphenated ISBN-13."""
    result = etl.normalise_isbn("978-0-13-595705-9")
    assert result is not None
    assert len(result.replace("-", "")) == 13


def test_normalise_isbn_no_hyphens() -> None:
    """Should add hyphens to a raw 13-digit ISBN."""
    result = etl.normalise_isbn("9780201633610")
    assert result is not None
    assert "-" in result


def test_normalise_isbn_empty() -> None:
    """Should return None for an empty ISBN."""
    assert etl.normalise_isbn("") is None


def test_normalise_tags_string() -> None:
    """Should split a comma-separated string into a list."""
    result = etl.normalise_tags("programming, design")
    assert result == ["programming", "design"]


def test_normalise_tags_list() -> None:
    """Should clean up a list of tags."""
    result = etl.normalise_tags(["Programming", " Design "])
    assert result == ["programming", "design"]


# --- validation tests ---


def test_validate_row_valid() -> None:
    """Should return a transformed dict for a valid row."""
    row = {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "description": "A handbook of agile software craftsmanship.",
        "isbn": "978-0-13-235088-4",
        "price": "3899",
        "tags": "programming,clean-code",
    }
    result = etl.validate_row(row=row)
    assert result is not None
    assert result["name"] == "Clean Code"
    assert result["isbn"] is not None


def test_validate_row_missing_title() -> None:
    """Should return None for a row with an empty title."""
    row = {
        "title": "",
        "author": "Someone",
        "publisher": "Some Press",
        "description": "No title.",
        "isbn": "978-0-00-000000-0",
        "price": "1999",
        "tags": "unknown",
    }
    result = etl.validate_row(row=row)
    assert result is None


def test_validate_row_missing_isbn() -> None:
    """Should return None for a row with no ISBN."""
    row = {
        "title": "No ISBN Book",
        "author": "Author",
        "publisher": "Publisher",
        "description": "Missing ISBN.",
        "isbn": "",
        "price": "2999",
        "tags": "unknown",
    }
    result = etl.validate_row(row=row)
    assert result is None


# --- process import tests ---


@mock.patch("app.api.v1.books.etl.insert_book")
@mock.patch("app.api.v1.books.etl.resolve_publisher")
@mock.patch("app.api.v1.books.etl.resolve_author")
@mock.patch("app.api.v1.books.etl.get_existing_isbns")
@mock.patch("app.api.v1.books.etl.database")
def test_process_import_csv(
    mock_database: mock.MagicMock,
    mock_get_isbns: mock.MagicMock,
    mock_resolve_author: mock.MagicMock,
    mock_resolve_publisher: mock.MagicMock,
    mock_insert: mock.MagicMock,
) -> None:
    """Should import valid CSV rows and report counts.

    Args:
        mock_database: Mocked database module.
        mock_get_isbns: Mocked ISBN retrieval function.
        mock_resolve_author: Mocked author resolver.
        mock_resolve_publisher: Mocked publisher resolver.
        mock_insert: Mocked insert function.
    """
    mock_get_isbns.return_value = set()
    mock_resolve_author.return_value = 1
    mock_resolve_publisher.return_value = 1
    mock_insert.return_value = {"id": 1}

    result = etl.process_import(file_content=SAMPLE_CSV, file_type="csv")

    assert result["total_processed"] == 3
    assert result["imported"] == 3
    assert result["skipped"] == 0
    assert len(result["errors"]) == 0


@mock.patch("app.api.v1.books.etl.insert_book")
@mock.patch("app.api.v1.books.etl.resolve_publisher")
@mock.patch("app.api.v1.books.etl.resolve_author")
@mock.patch("app.api.v1.books.etl.get_existing_isbns")
@mock.patch("app.api.v1.books.etl.database")
def test_process_import_json(
    mock_database: mock.MagicMock,
    mock_get_isbns: mock.MagicMock,
    mock_resolve_author: mock.MagicMock,
    mock_resolve_publisher: mock.MagicMock,
    mock_insert: mock.MagicMock,
) -> None:
    """Should import valid JSON rows and reject invalid ones.

    Args:
        mock_database: Mocked database module.
        mock_get_isbns: Mocked ISBN retrieval function.
        mock_resolve_author: Mocked author resolver.
        mock_resolve_publisher: Mocked publisher resolver.
        mock_insert: Mocked insert function.
    """
    mock_get_isbns.return_value = set()
    mock_resolve_author.return_value = 1
    mock_resolve_publisher.return_value = 1
    mock_insert.return_value = {"id": 1}

    result = etl.process_import(file_content=SAMPLE_JSON, file_type="json")

    assert result["total_processed"] == 2
    assert result["imported"] == 1
    assert len(result["errors"]) == 1
