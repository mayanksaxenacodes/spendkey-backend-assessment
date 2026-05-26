# pylint: disable=invalid-name
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Book management API routes."""
import fastapi
from fastapi import status

from app import config
from app.api.v1.books import crud, etl, llm, schemas, serializers
from app.common import errors, validators
from app.server import schemas as server_schemas

ROUTER = fastapi.APIRouter(prefix="/books", tags=["books"])


@ROUTER.get("/", response_model=schemas.BookList)
def list_books(
    # Pagination parameters.
    limit: int = fastapi.Query(
        title="Limit",
        description="Number of items included in the results. Can't be "
        " negative or higher than 100.",
        default=config.get_config().database_pagination_limit,
    ),
    offset: int = fastapi.Query(
        title="Offset",
        description="Number of items to skip when paginating results.",
        default=0,
    ),
) -> schemas.BookList:
    """Returns a paginated list of books from the database as JSON.
    \f
    Args:
        limit: Number of items included in the results.
        offset: Number of items to skip when paginating results.

    Returns:
        JSON response, containing a list of books from the database.

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

    rows = crud.list_books(limit=limit, offset=offset)
    total = crud.total_books()

    return serializers.to_book_list(rows=rows, total=total)


@ROUTER.post(
    "/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_411_LENGTH_REQUIRED: {"model": server_schemas.Error},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
            "model": server_schemas.Error
        },
    },
)
def create_book(
    request: fastapi.Request,
    body: schemas.BookBody = fastapi.Body(...),
) -> schemas.Book:
    """Saves a JSON formatted book to the database.
    \f
    Args:
        request: HTTP request object from FastAPI.
        body: JSON request body.

    Returns:
        JSON response, containing the newly created book.

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
    row = crud.create_book(body=body.dict())
    return serializers.to_book(row=row)


@ROUTER.get(
    "/{uid}/",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
        status.HTTP_404_NOT_FOUND: {"model": server_schemas.Error},
    },
    response_model=schemas.Book,
)
def get_book_by_uid(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing book.",
    ),
) -> schemas.Book:
    """Get a book by it's unique row identifier and return it as JSON.
    \f
    Args:
        uid: Unique row identifier for an existing book.

    Returns:
        JSON response, containing the existing book.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        row = crud.get_book_by_uid(uid=uid)
        return serializers.to_book(row=row)
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
    response_model=schemas.Book,
)
def update_book_by_uid(
    request: fastapi.Request,
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing book.",
    ),
    body: schemas.BookBody = fastapi.Body(...),
) -> schemas.Book:
    """Update an existing book and return it as JSON.
    \f
    Args:
        request: HTTP request object from FastAPI.
        uid: Unique row identifier for an existing book.
        body: JSON request body.

    Returns:
        JSON response, containing the modified book.

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
        row = crud.update_book_by_uid(uid=uid, body=body.dict())
        return serializers.to_book(row=row)
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
def delete_book_by_uid(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing book.",
    ),
) -> fastapi.Response:
    """Delete an existing book.
    \f
    Args:
        uid: Unique row identifier for an existing book.

    Returns:
        JSON response, containing the modified book.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        crud.delete_book_by_uid(uid=uid)
        return fastapi.Response(status_code=status.HTTP_204_NO_CONTENT)
    except errors.NotFound as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        )


@ROUTER.post(
    "/{uid}/summarise",
    response_model=schemas.Book,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
        status.HTTP_404_NOT_FOUND: {"model": server_schemas.Error},
    },
)
def summarise_book(
    uid: int = fastapi.Path(
        ...,
        title="UID",
        description="Unique row identifier for an existing book.",
    ),
) -> schemas.Book:
    """Generate an AI summary for a book and persist it.
    \f
    Args:
        uid: Unique row identifier for an existing book.

    Returns:
        JSON response, containing the updated book with AI summary.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not validators.is_identifier(identifier=uid):
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The row identifier '{uid}' is not valid.",
        )

    try:
        row = crud.get_book_by_uid(uid=uid)
    except errors.NotFound as err:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=err.detail,
        ) from err

    summary = llm.generate_summary(
        book_title=row["name"],
        description=row.get("description"),
    )

    row = crud.update_book_summary(uid=uid, summary=summary)
    return serializers.to_book(row=row)


@ROUTER.post(
    "/import",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
    },
)
def import_books(
    file: fastapi.UploadFile = fastapi.File(...),
) -> dict:
    """Import books from a CSV or JSON file upload.
    \f
    Args:
        file: Uploaded data file (CSV or JSON).

    Returns:
        JSON response with import summary statistics.

    Raises:
        HTTPException: If the file cannot be processed.
    """
    filename = file.filename or ""
    if not filename:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A filename is required.",
        )

    if filename.endswith(".csv"):
        file_type = "csv"
    elif file.filename.endswith(".json"):
        file_type = "json"
    else:
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and JSON files are accepted.",
        )

    content = file.file.read().decode("utf-8")
    result = etl.process_import(file_content=content, file_type=file_type)
    return result
