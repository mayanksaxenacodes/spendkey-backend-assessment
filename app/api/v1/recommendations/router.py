# pylint: disable=invalid-name
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Book recommendation API routes."""
import fastapi
from fastapi import status

from app.api.v1.recommendations import agent, schemas
from app.server import schemas as server_schemas

ROUTER = fastapi.APIRouter(prefix="/recommendations", tags=["recommendations"])


@ROUTER.post(
    "/",
    response_model=schemas.RecommendationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": server_schemas.Error},
    },
)
def recommend_books(
    body: schemas.RecommendationRequest = fastapi.Body(...),
) -> schemas.RecommendationResponse:
    """Generate book recommendations based on a natural language query.
    \f
    Args:
        body: JSON request body containing the user's query.

    Returns:
        JSON response containing a list of book recommendations.

    Raises:
        HTTPException: If the request cannot be fulfilled.
    """
    if not body.query or not body.query.strip():
        raise fastapi.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A non-empty query string is required.",
        )

    graph = agent.build_graph()
    result = graph.invoke(
        {
            "query": body.query,
            "books": [],
            "max_results": body.max_results or 5,
        }
    )

    return schemas.RecommendationResponse(
        query=body.query,
        recommendations=result.get("recommendations", []),
    )
