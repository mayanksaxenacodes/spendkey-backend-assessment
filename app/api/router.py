# Copyright © 2026 SpendKey. All Rights Reserved.
"""API HTTP endpoint routing."""
import fastapi

from app import config
from app.api.v1 import router as v1


def attach_routes(app: fastapi.FastAPI, cfg: config.Config) -> fastapi.FastAPI:
    """Attaches the HTTP API routes to the provided FastAPI instance.

    Args:
        app: FastAPI instance.
        cfg: Config instance.

    Returns:
        FastAPI instance with API routes included.
    """
    api_router = fastapi.APIRouter(prefix="/api")

    # Attach the v1 API endpoints.
    v1.attach_routes(api=api_router, cfg=cfg)

    # Attach the API router to the provided application.
    app.include_router(router=api_router)

    return app
