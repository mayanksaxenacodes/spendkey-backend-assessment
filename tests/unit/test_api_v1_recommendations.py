# Copyright © 2026 SpendKey. All Rights Reserved.
"""Recommendation agent unit tests."""
import typing as t
from unittest import mock

import pytest
from fastapi import status, testclient

from app.api.v1.recommendations import schemas

BASE_PATH: str = "/api/v1/recommendations"


@mock.patch("app.api.v1.recommendations.agent.build_graph")
def test_recommend_books(
    mock_graph: mock.MagicMock,
    client: testclient.TestClient,
) -> None:
    """Should return book recommendations for a valid query.

    Args:
        mock_graph: Mocked LangGraph workflow.
        client: API test client.
    """
    mock_graph.return_value.invoke.return_value = {
        "query": "books about programming",
        "books": [],
        "max_results": 5,
        "recommendations": [
            {
                "book_id": 1,
                "book_title": "Clean Code",
                "relevance_score": 0.95,
                "reasoning": "Directly about programming best practices.",
            }
        ],
    }

    body = {"query": "books about programming"}
    response = client.post(f"{BASE_PATH}/", json=body)

    assert response.status_code == status.HTTP_200_OK


def test_recommend_books_empty_query(
    client: testclient.TestClient,
) -> None:
    """Should return a 400 error for an empty query string.

    Args:
        client: API test client.
    """
    body = {"query": ""}
    response = client.post(f"{BASE_PATH}/", json=body)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_recommend_books_missing_query(
    client: testclient.TestClient,
) -> None:
    """Should return a 422 error for a missing query field.

    Args:
        client: API test client.
    """
    body: dict[str, t.Any] = {}
    response = client.post(f"{BASE_PATH}/", json=body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
