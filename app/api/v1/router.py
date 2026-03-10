# Copyright © 2026 SpendKey. All Rights Reserved.
"""Version 1 API endpoint router."""
import fastapi

from app import config
from app.api.v1.authors.router import ROUTER as AUTHORS
from app.api.v1.books.router import ROUTER as BOOKS
from app.api.v1.publishers.router import ROUTER as PUBLISHERS
from app.api.v1.recommendations.router import ROUTER as RECOMMENDATIONS


def attach_routes(
    api: fastapi.APIRouter,
    cfg: config.Config,  # pylint: disable=unused-argument
) -> fastapi.APIRouter:
    """Attaches the v1 HTTP API endpoints to the provided API router.

    Args:
        api: APIRouter instance.
        cfg: Config instance.

    Returns:
        APIRouter instance with v1 routes applied.
    """
    v1_router = fastapi.APIRouter(prefix="/v1")

    # Attach the API routes to the version 1 router.
    v1_router.include_router(router=AUTHORS)
    v1_router.include_router(router=BOOKS)
    v1_router.include_router(router=PUBLISHERS)
    v1_router.include_router(router=RECOMMENDATIONS)

    # Attach the versioned API router to the provided API router instance.
    api.include_router(router=v1_router)

    return api
