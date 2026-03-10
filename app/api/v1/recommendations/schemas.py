# pylint: disable=no-member,too-few-public-methods
# Copyright © 2026 SpendKey. All Rights Reserved.
"""Recommendation endpoint OpenAPI schemas."""
import typing as t

import pydantic


class RecommendationRequest(pydantic.BaseModel):
    """Request body for the book recommendation endpoint."""

    query: str
    max_results: t.Optional[int] = 5


class BookRecommendation(pydantic.BaseModel):
    """A single book recommendation with reasoning."""

    book_id: int
    book_title: str
    relevance_score: float
    reasoning: str


class RecommendationResponse(pydantic.BaseModel):
    """Response body for the book recommendation endpoint."""

    query: str
    recommendations: list[BookRecommendation]
