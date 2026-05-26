# Copyright © 2026 SpendKey. All Rights Reserved.
"""LLM integration unit tests."""
import typing as t
from unittest import mock

import pytest

from app.api.v1.books import llm


@pytest.fixture(name="mock_model")
def fixture_mock_model() -> t.Iterator[mock.MagicMock]:
    """Fixture for patching the LLM model instance.

    Yields:
        Mocked model instance.
    """
    with mock.patch("app.api.v1.books.llm._MODEL") as mocked:
        mock_res = mock.MagicMock()
        mock_res.content = "A compelling book about software engineering."
        mocked.invoke.return_value = mock_res
        mocked.return_value = mock_res
        yield mocked


def test_generate_summary(mock_model: mock.MagicMock) -> None:
    """Should generate a summary string for a given book.

    Args:
        mock_model: Mocked model instance.
    """
    result = llm.generate_summary(
        book_title="Clean Code",
        description="A handbook of agile software craftsmanship.",
    )
    assert isinstance(result, str)
    assert result == "A compelling book about software engineering."


def test_generate_summary_no_description(mock_model: mock.MagicMock) -> None:
    """Should handle books with no description gracefully.

    Args:
        mock_model: Mocked model instance.
    """
    result = llm.generate_summary(
        book_title="Unknown Book",
        description=None,
    )
    assert isinstance(result, str)
    assert result == "A compelling book about software engineering."
