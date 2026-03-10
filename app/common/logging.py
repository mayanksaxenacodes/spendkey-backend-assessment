# Copyright © 2026 SpendKey. All Rights Reserved.
"""Logging utilities."""
import functools
import logging

from fastapi.logger import logger

from app import config


@functools.lru_cache
def get_logger() -> logging.Logger:
    """Factory function for getting a Gunicorn compatible logger.

    Returns:
        Logger instance.
    """
    cfg = config.get_config()
    glogger = logging.getLogger("gunicorn.error")

    logger.handlers = glogger.handlers
    logger.setLevel(logging.DEBUG if cfg.enable_debug else glogger.level)

    return glogger
