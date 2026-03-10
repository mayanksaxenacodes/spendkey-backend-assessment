# Copyright © 2026 SpendKey. All Rights Reserved.
"""API router tests."""
from unittest import mock

import fastapi

from app import config
from app.api import router


@mock.patch("app.api.router.attach_routes")
def test_api_router(attach_routes: mock.MagicMock) -> None:
    """Should attach an API router to the provided FastAPI instance.

    Args:
        attach_routes: Mocked API router.
    """
    app = fastapi.FastAPI()
    cfg = config.get_config()

    router.attach_routes(app=app, cfg=cfg)
    attach_routes.assert_called_with(app=app, cfg=cfg)


@mock.patch("app.api.router.fastapi.APIRouter")
def test_api_router_prefix(api_router: mock.MagicMock) -> None:
    """Should set an `/api` prefix.

    Args:
        api_router: Mocked FastAPI APIRouter.
    """
    app = fastapi.FastAPI()
    cfg = config.get_config()

    router.attach_routes(app=app, cfg=cfg)
    assert mock.call(prefix="/api") in api_router.call_args_list
