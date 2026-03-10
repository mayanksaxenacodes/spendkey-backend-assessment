# Copyright © 2026 SpendKey. All Rights Reserved.
"""Application runtime configuration.

    See:
        https://fastapi.tiangolo.com/advanced/settings
"""
import functools
from os import environ

from app.common import strings


class Config:
    """Global configuration options."""

    @property
    def enable_debug(self) -> bool:
        """Enable debug logging for development.

        By default, we don't enable this setting to reduce log noise in
        production. When running locally this can be enabled for greater
        visibility.

        Returns:
            True if logging is enabled, False if it's not.
        """
        val = environ.get("ENABLE_DEBUG", default="no")
        return strings.is_truthy(val=val)

    @property
    def app_name(self) -> str:
        """Application name.

        Returns:
            The currently configured application name.
        """
        return environ.get("APP_NAME", "bweb-api")

    @property
    def database_username(self) -> str:
        """Database connection username.

        Returns:
            The currently configured database connection username.
        """
        return environ.get("DATABASE_USERNAME", default="postgres")

    @property
    def database_host(self) -> str:
        """Database connection host.

        Returns:
            The currently configured database connection host.
        """
        return environ.get("DATABASE_HOST", default="localhost")

    @property
    def database_port(self) -> int:
        """Database connection port.

        Returns:
            The currently configured database connection port.
        """
        val = environ.get("DATABASE_PORT", default="5432")
        return int(val)

    @property
    def database_password(self) -> str:
        """Database connection password.

        Returns:
            The currently configured database password.
        """
        return environ.get("DATABASE_PASSWORD", default="postgres")

    @property
    def database_name(self) -> str:
        """Database name.

        Returns:
            The currently configured database name.
        """
        return environ.get("DATABASE_NAME", default="")

    @property
    def database_pagination_limit(self) -> int:
        """The number of items returned when listing database entries.

        Returns:
            The currently configured database pagination limit.
        """
        val = environ.get("DATABASE_PAGINATION_LIMIT", default="9")
        return int(val)

    @property
    def cors_origins(self) -> list[str]:
        """CORS origins which are permitted access.

        These are best configured per deployable environment. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS for more
        information

        Returns:
            List of currently configured CORS origins.
        """
        val = environ.get("CORS_ORIGINS", "")
        return strings.to_list(val=val)

    @property
    def cors_methods(self) -> list[str]:
        """CORS methods which are permitted.

        Working defaults are provided, think carefully before adjusting. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS for more
        information.

        Returns:
            List of currently configured CORS methods.
        """
        default = "get,post,patch,put,delete,options"
        methods = environ.get("CORS_METHODS", default=default)
        return [method.upper().strip() for method in methods.split(",")]

    @property
    def cors_headers(self) -> list[str]:
        """CORS headers which are permitted.

        We permit all headers in order to reduce development friction. These
        can be adjusted per deployment environment for improved security. See
        https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS for more
        information.

        Returns:
            List of currently configured CORS headers.
        """
        val = environ.get("CORS_HEADERS", default="*")
        return strings.to_list(val=val)

    @property
    def enable_openapi_docs(self) -> bool:
        """Configure availability of the OpenAPI interactive docs.

        When deployed this API is expected to be publicly facing. As it's not
        intended to be consumed by third-parties, this configuration parameter
        allows the OpenAPI interactive docs to be disabled.

        Returns:
            True if the docs should be enabled, False if they aren't.
        """
        val = environ.get("ENABLE_OPENAPI_DOCS", default="no")
        return strings.is_truthy(val=val)


@functools.lru_cache()
def get_config() -> Config:
    """Configuration factory function.

    Uses the LRU_CACHE to store/retrieve the instantiated config. See
    https://docs.python.org/3/library/functools.html#functools.lru_cache for
    more information.

    Returns:
        The instantiated application runtime configuration.
    """
    return Config()
