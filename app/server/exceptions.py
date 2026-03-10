# Copyright © 2026 SpendKey. All Rights Reserved.
"""FastAPI custom exception handlers."""
import fastapi
from fastapi import status

from app import config
from app.common import responses


def attach_exception_handlers(
    app: fastapi.FastAPI, cfg: config.Config
) -> fastapi.FastAPI:
    """Attaches custom exception handlers to the provided FastAPI instance.

    Args:
        app: FastAPI instance.
        cfg: Optional application runtime configuration.

    Returns:
        FastAPI instance with exception handlers attached.
    """

    @app.exception_handler(  # type: ignore
        status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    def cors_exception_handler(  # type: ignore
        request: fastapi.Request,
        err: Exception,  # pylint: disable=unused-argument
    ) -> responses.OrJSONResponse:  # pragma: no cover
        response = responses.OrJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "The server has encountered an unrecoverable "
                "error, see log for details.",
            },
        )

        # Since the CORSMiddleware is not executed during an unhandled server
        # exception, we need to manually set the CORS headers ourselves if we
        # want the FE to receive a proper JSON 500 error, as apposed to a CORS
        # error which is misleading.
        #
        # Setting CORS headers on server errors is a contentious topic in many
        # frameworks, and it is not handled in FastAPI. See DotNET Core for a
        # recent discussion, where ultimately it was decided to return CORS
        # headers on server failures.
        #
        # https://github.com/dotnet/aspnetcore/issues/2378
        origin = request.headers.get("origin")

        if origin:
            # response.headers.update(cors.simple_headers)
            has_cookie = "cookie" in request.headers

            # If the request includes any cookie headers, then we must
            # respond with the specific origin.
            if cfg.cors_origins and has_cookie:
                response.headers["Access-Control-Allow-Origin"] = origin

            # If we only allow specific origins then we have to mirror back
            # the Origin header in the response.
            elif not cfg.cors_origins and origin in cfg.cors_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers.add_vary_header("Origin")

        return response

    return app
