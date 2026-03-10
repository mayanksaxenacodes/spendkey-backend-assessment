# Copyright © 2026 SpendKey. All Rights Reserved.
"""Configuration tests."""
import os
from unittest import mock

from app import config


def test_get_config() -> None:
    """Should return a cached configuration object."""
    assert isinstance(config.get_config(), config.Config)
    config.get_config.cache_clear()


def test_config_defaults() -> None:
    """Config should include default values."""
    cfg = config.Config()

    assert not cfg.enable_debug
    assert cfg.app_name == "bweb-api"
    assert cfg.database_username == "postgres"
    assert cfg.database_host == "localhost"
    assert cfg.database_port == 5432
    assert cfg.database_password == "postgres"
    assert cfg.database_name == ""
    assert cfg.database_pagination_limit == 9
    assert cfg.cors_origins == []
    assert all(
        method
        in [
            "GET",
            "POST",
            "PATCH",
            "PUT",
            "DELETE",
            "OPTIONS",
        ]
        for method in cfg.cors_methods
    )
    assert cfg.cors_headers == ["*"]
    assert not cfg.enable_openapi_docs


@mock.patch.dict(
    os.environ,
    {
        "ENABLE_DEBUG": "yes",
        "APP_NAME": "foobar",
        "DATABASE_USERNAME": "foo",
        "DATABASE_HOST": "example.com",
        "DATABASE_PORT": "9876",
        "DATABASE_PASSWORD": "bar",
        "DATABASE_NAME": "test",
        "DATABASE_PAGINATION_LIMIT": "5",
        "CORS_ORIGINS": "http://localhost:3000,http://localhost:4200",
        "CORS_METHODS": "GET,POST",
        "CORS_HEADERS": "Authorization,X-Rate-Limit",
        "ENABLE_OPENAPI_DOCS": "yes",
    },
)
def test_config_env() -> None:
    """Properties should be configurable using env variables."""
    cfg = config.Config()

    assert cfg.enable_debug
    assert cfg.app_name == "foobar"
    assert cfg.database_username == "foo"
    assert cfg.database_host == "example.com"
    assert cfg.database_port == 9876
    assert cfg.database_password == "bar"
    assert cfg.database_name == "test"
    assert cfg.database_pagination_limit == 5
    assert cfg.cors_origins == [
        "http://localhost:3000",
        "http://localhost:4200",
    ]
    assert cfg.cors_methods == ["GET", "POST"]
    assert cfg.cors_headers == ["Authorization", "X-Rate-Limit"]
    assert cfg.enable_openapi_docs
