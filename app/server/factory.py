# Copyright © 2026 SpendKey. All Rights Reserved.
"""Application server setup and entrypoint."""
import fastapi

from app import __version__, config, constants
from app.api import router
from app.common import responses
from app.server import middleware


def create_app() -> fastapi.FastAPI:
    """FastAPI factory function.

    Returns:
        A pre-configured FastAPI instance.
    """
    cfg = config.get_config()
    app = fastapi.FastAPI(
        description="RESTful API for managing an online bookstore.",
        docs_url="/" if cfg.enable_openapi_docs else None,
        openapi_tags=[tag.dict() for tag in constants.TAGS_METADATA],
        title="Bookstore API",
        version=__version__,
        default_response_class=responses.OrJSONResponse,
    )

    middleware.attach_middleware(app=app, cfg=cfg)
    router.attach_routes(app=app, cfg=cfg)

    return app
