# pylint: disable=invalid-name
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Publishers management API routes."""
import fastapi
from fastapi import status

from app import config
from app.api.v1.publishers import crud, schemas, serializers
from app.common import errors, validators
from app.server import schemas as server_schemas

ROUTER = fastapi.APIRouter(prefix="/publishers", tags=["publishers"])


@ROUTER.get("/", response_model=schemas.PublisherList)
def list_publishers(
    # Pagination paramters.
    limit: int = fastapi.Query(
        title="Limit",
        description="Number of items included in the results. Can't be "
        "negative or higher than 100.",
        default=config.get_config().database_pagination_limit,
    ),
    offset: int = fastapi.Query(
        title="Offset",
        description="Number of items to skip when paginating results.",
        default=0,
    ),
) -> schemas.PublisherList:
    """Returns a paginated list of publishers from the database as JSON.
    \f
    Args:
        limit: Number of items included in the results.
        offset: Number of items to skip when paginating results.

    Returns:
        JSON response, containing a list of publishers from the database.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_limit(limit=limit):
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"The provided limit '{limit}' is not valid.",
        )

    if not validators.is_offset(offset=offset):
        raise fastapi.HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"The provided offset '{offset}' is not valid.",
        )

    rows = crud.list_publishers(limit=limit, offset=offset)
    total = crud.total_publishers()

    return serializers.to_publisher_list(rows=rows, total=total)


@ROUTER.post(
    "/",
    response_model=schemas.Publisher,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_411_LENGTH_REQUIRED: {"model": server_schemas.Error},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": server_schemas.Error
        },
    },
)
def create_publisher(
    request: fastapi.Request,
    body: schemas.PublisherBody = fastapi.Body(...),
) -> schemas.Publisher:
    """Saves a JSON formatted publisher to the database.
    \f
    Args:
        request: HTTP request object from FastAPI.
        body: JSON request body.

    Returns:
        JSON response, containing the newly created publisher.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    try:
        validators.check_content_length(request=request)
    except errors.ContentLengthMissing as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail=err.detail,
        ) from err
    except errors.ContentLengthExceeded as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=err.detail,
        ) from err
    row = crud.create_publisher(body=body.dict())
    return serializers.to_publisher(row=row)


@ROUTER.get(
    "/{uid}/",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
        status.HTTP_404_NOT_FOUND: {"model": server_schemas.Error},
    },
    response_model=schemas.Publisher,
)
def get_publisher_by_uid(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing publisher.",
    ),
) -> schemas.Publisher:
    """Get a publisher by it's unique row identifier and return it as JSON.
    \f
    Args:
        uid: Unique row identifier for an existing publisher.

    Returns:
        JSON response, containing the existing publisher.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        row = crud.get_publisher_by_uid(uid=uid)
        return serializers.to_publisher(row=row)
    except errors.NotFound as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,  # type: ignore
        ) from err


@ROUTER.put(
    "/{uid}/",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
        status.HTTP_404_NOT_FOUND: {"model": server_schemas.Error},
        status.HTTP_411_LENGTH_REQUIRED: {"model": server_schemas.Error},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": server_schemas.Error
        },
    },
    response_model=schemas.Publisher,
)
def update_publisher_by_uid(
    request: fastapi.Request,
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing publisher.",
    ),
    body: schemas.PublisherBody = fastapi.Body(...),
) -> schemas.Publisher:
    """Update an existing publisher and return it as JSON.
    \f
    Args:
        request: HTTP request object from FastAPI.
        uid: Unique row identifier for an existing publisher.
        body: JSON request body.

    Returns:
        JSON response, containing the modified publisher.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        validators.check_content_length(request=request)
    except errors.ContentLengthMissing as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_411_LENGTH_REQUIRED,
            detail=err.detail,
        ) from err
    except errors.ContentLengthExceeded as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=err.detail,
        ) from err

    try:
        row = crud.update_publisher_by_uid(uid=uid, body=body.dict())
        return serializers.to_publisher(row=row)
    except errors.NotFound as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )


@ROUTER.delete(
    "/{uid}/",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
        status.HTTP_404_NOT_FOUND: {"model": server_schemas.Error},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_publisher_by_uid(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing publisher.",
    ),
) -> fastapi.Response:
    """Delete an existing publisher.
    \f
    Args:
        uid: Unique row identifier for an existing publisher.

    Returns:
        JSON response, containing the modified publisher.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        crud.delete_publisher_by_uid(uid=uid)
        return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)
    except errors.NotFound as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )
