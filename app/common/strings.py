# Copyright © 2026 SpendKey. All Rights Reserved.
"""Utilities for working with strings."""
import typing as t

from app import constants


def is_truthy(val: str) -> bool:
    """Check if the provided value is truthy.

    Examples:
        >>> is_truthy(val="yes")
        True

    Args:
        val: String value to check.

    Returns:
        True if the provided value is truthy, False if it's not.
    """
    return val.casefold().strip() in [
        x.casefold() for x in constants.TRUTHY_VALUES
    ]


def to_list(val: str, lower: t.Optional[bool] = False) -> list[str]:
    """Convert a comma-separated string to a list.

    Examples:
        >>> to_list(val="Foo,Bar")
        ["Foo", "Bar"]

        >>> to_list(val="Foo,bar", lower=True)
        ["foo", "bar"]

    Args:
        val: String containing comma-separated values.
        lower: Convert the string values to lowercase.

    Returns:
        List of string values.
    """
    return [
        x.strip().casefold() if lower else x.strip()
        for x in val.split(",")
        if val.strip()
    ]
