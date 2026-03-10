# Copyright © 2026 SpendKey. All Rights Reserved.
"""String utility tests."""
from app.common import strings


def test_is_truthy() -> None:
    """Should return True for truthy values."""
    assert strings.is_truthy(val="trUe")
    assert strings.is_truthy(val="yes")
    assert strings.is_truthy(val="y")
    assert strings.is_truthy(val="Y")
    assert strings.is_truthy(val="enable")
    assert strings.is_truthy(val="enaBleD")
    assert strings.is_truthy(val="active")
    assert strings.is_truthy(val="Activated")


def test_not_truthy() -> None:
    """Should return False for non-truthy values."""
    assert not strings.is_truthy(val="no")
    assert not strings.is_truthy(val="n")
    assert not strings.is_truthy(val="0")
    assert not strings.is_truthy(val="disaBled")
    assert not strings.is_truthy(val="false")


def test_to_list() -> None:
    """Should return a list of string values."""
    assert strings.to_list(val="Foo, Bar ") == ["Foo", "Bar"]
    assert strings.to_list(val="foo,bar") == ["foo", "bar"]
    assert strings.to_list(val="") == []


def test_to_list_lower() -> None:
    """Should return a list of lowercase values."""
    assert strings.to_list(val="Foo,Bar", lower=True) == ["foo", "bar"]
    assert strings.to_list(val="FOO ", lower=True) == ["foo"]
    assert strings.to_list(val="", lower=True) == []
