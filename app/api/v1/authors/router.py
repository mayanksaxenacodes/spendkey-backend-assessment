# Copyright © 2026 SpendKey. All Rights Reserved.
"""Author management API routes."""
import fastapi
from fastapi import status

from app import config
from app.api.v1.authors import crud, schemas, serializers
from app.common import errors, validators
from app.server import schemas as server_schemas

ROUTER = fastapi.APIRouter(prefix="/authors", tags=["authors"])


@ROUTER.get("/", response_model=schemas.AuthorList)
def list_authors(
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
) -> schemas.AuthorList:
    """Returns a paginated list of authors from the database as JSON.
    \f
    Args:
        limit: Number of items included in the results.
        offset: Number of items to skip when paginating results.

    Returns:
        JSON response, containing a list of authors from the database.

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

    rows = crud.list_authors(limit=limit, offset=offset)
    total = crud.total_authors()

    return serializers.to_author_list(rows=rows, total=total)


@ROUTER.post(
    "/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_411_LENGTH_REQUIRED: {"model": server_schemas.Error},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": server_schemas.Error
        },
    },
)
def create_author(
    request: fastapi.Request,
    body: schemas.AuthorBody = fastapi.Body(...),
) -> schemas.Author:
    """Saves a JSON formatted author to the database.
    \f
    Args:
        request: HTTP request object from FastAPI.
        body: JSON request body.

    Returns:
        JSON response, containing the newly created author.

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
    row = crud.create_author(body=body.dict())
    return serializers.to_author(row=row)


@ROUTER.get(
    "/{uid}/",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
        status.HTTP_404_NOT_FOUND: {"model": server_schemas.Error},
    },
    response_model=schemas.Author,
)
def get_author_by_uid(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing author.",
    ),
) -> schemas.Author:
    """Get a author by it's unique row identifier and return it as JSON.
    \f
    Args:
        uid: Unique row identifier for an existing author.

    Returns:
        JSON response, containing the existing author.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        row = crud.get_author_by_uid(uid=uid)
        return serializers.to_author(row=row)
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
    response_model=schemas.Author,
)
def update_author_by_uid(
    request: fastapi.Request,
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing author.",
    ),
    body: schemas.AuthorBody = fastapi.Body(...),
) -> schemas.Author:
    """Update an existing author and return it as JSON.
    \f
    Args:
        request: HTTP request object from FastAPI.
        uid: Unique row identifier for an existing author.
        body: JSON request body.

    Returns:
        JSON response, containing the modified author.

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
        row = crud.update_author_by_uid(uid=uid, body=body.dict())
        return serializers.to_author(row=row)
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
def delete_author_by_uid(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing author.",
    ),
) -> fastapi.Response:
    """Delete an existing author.
    \f
    Args:
        uid: Unique row identifier for an existing author.

    Returns:
        JSON response, containing the modified author.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        crud.delete_author_by_uid(uid=uid)
        return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)
    except errors.NotFound as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )
