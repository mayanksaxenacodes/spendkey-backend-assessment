# Copyright © 2026 SpendKey. All Rights Reserved.
"""API v1 router tests."""
from unittest import mock

import fastapi

from app import config
from app.api.v1 import router


@mock.patch("app.api.v1.router.attach_routes")
def test_api_v1_router(attach_routes: mock.MagicMock) -> None:
    """Should attach an API router to the provided APIRouter instance.

    Args:
        attach_routes: Mocked API router.
    """
    api = fastapi.APIRouter()
    cfg = config.get_config()

    router.attach_routes(api=api, cfg=cfg)
    attach_routes.assert_called_with(api=api, cfg=cfg)


@mock.patch("app.api.v1.router.fastapi.APIRouter")
def test_api_v1_router_prefix(api_router: mock.MagicMock) -> None:
    """Should set a `/v1` prefix.

    Args:
        api_router: Mocked FastAPI APIRouter.
    """
    api = fastapi.APIRouter()
    cfg = config.get_config()

    router.attach_routes(api=api, cfg=cfg)
    assert mock.call(prefix="/v1") in api_router.call_args_list
