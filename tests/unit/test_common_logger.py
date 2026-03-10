# Copyright © 2026 SpendKey. All Rights Reserved.
"""Logging utility tests."""
from logging import Logger

from app.common import logging


def test_get_logger() -> None:
    """Should return a Logger instance."""
    assert isinstance(logging.get_logger(), Logger)
