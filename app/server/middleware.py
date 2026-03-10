# Copyright © 2026 SpendKey. All Rights Reserved.
"""FastAPI HTTP middleware."""
import time
import typing as t

import fastapi
import secure
from fastapi.middleware import cors
from starlette.middleware import base

from app import config

SECURE_HEADERS = secure.Secure()


async def add_secure_response_headers(
    request: fastapi.Request,
    call_next: t.Callable[[fastapi.Request], t.Awaitable[fastapi.Response]],
) -> fastapi.Response:
    """Add a collection of secure HTTP headers to every response.

    For more information, please see the following:
    https://owasp.org/www-project-secure-headers/

    Args:
        request: FastAPI request object.
        call_next: Passes the `request` to the corresponding path operation.

    Returns:
        The response with secure headers included.
    """
    response = await call_next(request)

    SECURE_HEADERS.framework.fastapi(response=response)

    return response


async def add_process_time_header(
    request: fastapi.Request,
    call_next: t.Callable[[fastapi.Request], t.Awaitable[fastapi.Response]],
) -> fastapi.Response:
    """Adds a header which contains the time (in seconds) that it took to
    process the request and return the response.

    This should serve as an example implementation for adding custom middleware
    to this application. For more information, please refer to the following:
    https://fastapi.tiangolo.com/tutorial/middleware/

    Args:
        request: FastAPI request object.
        call_next: Passes the `request` to the corresponding path operation.

    Returns:
        The response with an `x-process-time` header included.
    """
    start_time = time.time()
    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


def attach_middleware(
    app: fastapi.FastAPI, cfg: config.Config
) -> fastapi.FastAPI:
    """Attaches the middleware to the given application instance.

    Args:
        app: FastAPI instance.
        cfg: Config instance.

    Returns:
        FastAPI instance with middleware attached.
    """
    app.add_middleware(
        base.BaseHTTPMiddleware,
        dispatch=add_secure_response_headers,
    )
    app.add_middleware(
        base.BaseHTTPMiddleware, dispatch=add_process_time_header
    )

    # Setup cross-origin resource sharing.
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=cfg.cors_origins,
        allow_credentials=True,
        allow_methods=cfg.cors_methods,
        allow_headers=cfg.cors_headers,
    )

    return app
