# Copyright © 2026 SpendKey. All Rights Reserved.
"""Database connection utilities."""
import functools
import os
import typing as t

import psycopg
import psycopg_pool

from app import config


def connect_to(
    autocommit: t.Optional[bool],
) -> psycopg.Connection[t.Any]:
    """Connect to a Postgres database server.

    Args:
        autocommit: Enable autocommit mode. Transactions are not automatically
            open and commands have no immediate effect.

    Returns:
        A connection object to the database server.
    """
    cfg = config.get_config()

    params: dict[str, t.Union[str, int, bool]] = {
        "user": cfg.database_username,
        "host": cfg.database_host,
        "port": cfg.database_port,
        "password": cfg.database_password,
        "autocommit": autocommit or False,
    }

    if cfg.database_name:
        params["dbname"] = cfg.database_name

    return psycopg.connect(**params)  # type: ignore


@functools.lru_cache
def get_pool():
    """Create a pool of connections to the database.

    Returns:
        A connection pool object to the database server.
    """
    cfg = config.get_config()

    params: dict[str, t.Union[str, int]] = {
        "user": cfg.database_username,
        "host": cfg.database_host,
        "port": cfg.database_port,
        "password": cfg.database_password,
    }

    if cfg.database_name:
        params["dbname"] = cfg.database_name

    conn_info = psycopg.conninfo.make_conninfo(**params)
    conn_args: dict[str, int] = {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

    name = f"pool-{os.getpid()}"
    return psycopg_pool.ConnectionPool(
        conn_info,
        max_lifetime=30 * 60,
        kwargs=conn_args,
        name=name,
    )
