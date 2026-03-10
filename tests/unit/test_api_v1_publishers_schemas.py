# pylint: disable=no-member
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publisher schema tests."""
import typing as t

import pydantic
import pytest

from app.api.v1.publishers import schemas


def test_publisher() -> None:
    """Should be a Pydantic model."""
    assert issubclass(schemas.Publisher, pydantic.BaseModel)  # type: ignore


@pytest.mark.parametrize(
    "attr",
    [
        "id",
        "name",
        "created_at",
        "updated_at",
    ],
)
def test_book_attributes(attr: str) -> None:
    """Should have the expected attributes.

    Args:
        attr: Expected schema attribute.
    """
    properties: dict[str, t.Any] = schemas.Publisher.schema().get(
        "properties", {}
    )
    assert attr in properties


def test_book_list() -> None:
    """Should be a Pydantic model."""
    assert issubclass(schemas.PublisherList, pydantic.BaseModel)


@pytest.mark.parametrize(
    "attr",
    [
        "total",
        "data",
    ],
)
def test_book_list_attributes(attr: str) -> None:
    """Should have the expected attributes.

    Args:
        attr: Expected schema attribute.
    """
    properties: dict[str, t.Any] = schemas.PublisherList.schema().get(
        "properties", {}
    )
    assert attr in properties
