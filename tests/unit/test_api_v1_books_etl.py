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


def test_parse_json_list() -> None:
    """Should parse JSON list content into a list of dictionaries."""
    rows = etl.parse_json(file_content=SAMPLE_JSON)
    assert len(rows) == 2
    assert rows[0]["title"] == "SICP"


def test_parse_json_dict() -> None:
    """Should parse a single JSON object into a list containing one dictionary."""
    content = '{"title": "Single Book", "isbn": "123"}'
    rows = etl.parse_json(file_content=content)
    assert len(rows) == 1
    assert rows[0]["title"] == "Single Book"


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


def test_normalise_price_invalid_float() -> None:
    """Should return None for invalid floating point string."""
    assert etl.normalise_price("abc.def") is None


def test_normalise_price_invalid_int() -> None:
    """Should return None for invalid integer string."""
    assert etl.normalise_price("not-a-number") is None


def test_normalise_isbn_hyphenated() -> None:
    """Should preserve a correctly hyphenated ISBN-13."""
    result = etl.normalise_isbn("978-0-13-595705-9")
    assert result is not None
    assert len(result.replace("-", "")) == 13


def test_normalise_isbn_no_hyphens() -> None:
    """Should add hyphens to a raw 13-digit ISBN."""
    result = etl.normalise_isbn("9780201633610")
    assert result == "978-0-20-163361-0"


def test_normalise_isbn_10_digit() -> None:
    """Should return a 10-digit ISBN as is if valid."""
    assert etl.normalise_isbn("0201633610") == "0201633610"
    assert etl.normalise_isbn("020163361X") == "020163361X"


def test_normalise_isbn_invalid_length() -> None:
    """Should return None for ISBN with incorrect number of digits."""
    assert etl.normalise_isbn("123456789") is None
    assert etl.normalise_isbn("12345678901") is None


def test_normalise_isbn_empty() -> None:
    """Should return None for an empty ISBN."""
    assert etl.normalise_isbn("") is None
    assert etl.normalise_isbn("   ") is None


def test_normalise_tags_string() -> None:
    """Should split a comma-separated string into a list."""
    result = etl.normalise_tags("programming, design")
    assert result == ["programming", "design"]


def test_normalise_tags_list() -> None:
    """Should clean up a list of tags."""
    result = etl.normalise_tags(["Programming", " Design ", ""])
    assert result == ["programming", "design"]


def test_normalise_tags_invalid() -> None:
    """Should return an empty list for invalid input types."""
    assert etl.normalise_tags(None) == []
    assert etl.normalise_tags(123) == []


# --- resolve tests ---


def test_resolve_author_empty() -> None:
    """Should return None for empty author name."""
    conn = mock.MagicMock()
    assert etl.resolve_author(conn, "") is None
    assert etl.resolve_author(conn, "  ") is None


def test_resolve_author_existing(mock_conn: mock.MagicMock) -> None:
    """Should return existing author ID."""
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {"id": 123}
    
    result = etl.resolve_author(mock_conn, "Existing Author")
    assert result == 123
    assert mock_cursor.execute.call_count == 1


def test_resolve_author_new(mock_conn: mock.MagicMock) -> None:
    """Should create new author and return ID."""
    mock_cursor = mock_conn.cursor.return_value
    # First call to check existence returns None, second call to insert returns ID
    mock_cursor.fetchone.side_effect = [None, {"id": 456}]
    
    result = etl.resolve_author(mock_conn, "New Author")
    assert result == 456
    assert mock_cursor.execute.call_count == 2


def test_resolve_publisher_empty() -> None:
    """Should return None for empty publisher name."""
    conn = mock.MagicMock()
    assert etl.resolve_publisher(conn, "") is None


def test_resolve_publisher_existing(mock_conn: mock.MagicMock) -> None:
    """Should return existing publisher ID."""
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {"id": 789}
    
    result = etl.resolve_publisher(mock_conn, "Existing Publisher")
    assert result == 789


def test_resolve_publisher_new(mock_conn: mock.MagicMock) -> None:
    """Should create new publisher and return ID."""
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.side_effect = [None, {"id": 101}]
    
    result = etl.resolve_publisher(mock_conn, "New Publisher")
    assert result == 101


@pytest.fixture
def mock_conn() -> mock.MagicMock:
    """Fixture for a mocked database connection."""
    return mock.MagicMock()


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
        "isbn": "978-0-00-000000-0",
        "price": "1999",
    }
    result = etl.validate_row(row=row)
    assert result is None


def test_validate_row_missing_isbn() -> None:
    """Should return None for a row with no ISBN."""
    row = {
        "title": "No ISBN Book",
        "isbn": "",
        "price": "2999",
    }
    result = etl.validate_row(row=row)
    assert result is None


def test_validate_row_missing_price() -> None:
    """Should return None for a row with no price."""
    row = {
        "title": "No Price Book",
        "isbn": "978-0-00-000000-0",
        "price": "",
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
    """Should import valid CSV rows and report counts."""
    mock_get_isbns.return_value = set()
    mock_resolve_author.return_value = 1
    mock_resolve_publisher.return_value = 1
    mock_insert.return_value = {"id": 1}
    
    # Mock pool and connection
    mock_conn = mock.MagicMock()
    mock_database.get_pool.return_value.connection.return_value.__enter__.return_value = mock_conn

    result = etl.process_import(file_content=SAMPLE_CSV, file_type="csv")

    assert result["total_processed"] == 3
    assert result["imported"] == 3
    assert result["skipped"] == 0
    assert len(result["errors"]) == 0
    mock_conn.commit.assert_called_once()


@mock.patch("app.api.v1.books.etl.insert_book")
@mock.patch("app.api.v1.books.etl.resolve_publisher")
@mock.patch("app.api.v1.books.etl.resolve_author")
@mock.patch("app.api.v1.books.etl.get_existing_isbns")
@mock.patch("app.api.v1.books.etl.database")
def test_process_import_json_with_skips_and_errors(
    mock_database: mock.MagicMock,
    mock_get_isbns: mock.MagicMock,
    mock_resolve_author: mock.MagicMock,
    mock_resolve_publisher: mock.MagicMock,
    mock_insert: mock.MagicMock,
) -> None:
    """Should handle duplicate ISBNs and validation errors in JSON."""
    # First ISBN in SAMPLE_JSON is "978-0-26-251087-5"
    mock_get_isbns.return_value = {"978-0-26-251087-5"}
    mock_resolve_author.return_value = 1
    mock_resolve_publisher.return_value = 1
    
    mock_conn = mock.MagicMock()
    mock_database.get_pool.return_value.connection.return_value.__enter__.return_value = mock_conn

    result = etl.process_import(file_content=SAMPLE_JSON, file_type="json")

    # SAMPLE_JSON has 2 items: 
    # 1. Existing ISBN (skipped)
    # 2. Missing title (validation error)
    assert result["total_processed"] == 2
    assert result["imported"] == 0
    assert result["skipped"] == 1
    assert len(result["errors"]) == 1
    assert result["errors"][0]["reason"].startswith("Validation failed")


@mock.patch("app.api.v1.books.etl.database")
def test_get_existing_isbns(mock_database: mock.MagicMock) -> None:
    """Should return set of ISBNs from database."""
    mock_conn = mock.MagicMock()
    mock_database.get_pool.return_value.connection.return_value.__enter__.return_value = mock_conn
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchall.return_value = [{"isbn": "123"}, {"isbn": "456"}]
    
    result = etl.get_existing_isbns()
    assert result == {"123", "456"}


def test_insert_book(mock_conn: mock.MagicMock) -> None:
    """Should execute insert statement and return row."""
    mock_cursor = mock_conn.cursor.return_value
    mock_cursor.fetchone.return_value = {"id": 1, "name": "Test Book"}
    
    book_data = {"name": "Test Book", "isbn": "123", "author_id": 1, "publisher_id": 1}
    result = etl.insert_book(mock_conn, book_data)
    
    assert result["id"] == 1
    assert mock_cursor.execute.call_count == 1
