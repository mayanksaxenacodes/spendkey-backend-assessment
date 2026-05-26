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


from app.api.v1.recommendations import agent

@mock.patch("app.api.v1.recommendations.agent.crud.list_books")
def test_fetch_inventory(mock_list_books: mock.MagicMock) -> None:
    """Should fetch books from crud and update state."""
    mock_list_books.return_value = [{"id": 1, "name": "Book"}]
    state: agent.AgentState = {"query": "test", "books": [], "max_results": 1}
    result = agent._fetch_inventory(state)
    assert result["books"] == [{"id": 1, "name": "Book"}]


@mock.patch("app.api.v1.recommendations.agent.ChatOpenAI")
def test_generate_recommendations(mock_chat: mock.MagicMock) -> None:
    """Should call LLM and update state with recommendations."""
    mock_instance = mock_chat.return_value
    mock_instance.invoke.return_value = mock.MagicMock(content="Recommended Books")
    
    state: agent.AgentState = {
        "query": "test", 
        "books": [{"id": 1, "name": "Book"}], 
        "max_results": 1
    }
    result = agent._generate_recommendations(state)
    assert result["recommendations"] == "Recommended Books"


@mock.patch("app.api.v1.recommendations.agent.ChatOpenAI")
def test_generate_recommendations_json(mock_chat: mock.MagicMock) -> None:
    """Should parse structured JSON recommendations from LLM."""
    mock_instance = mock_chat.return_value
    mock_instance.invoke.return_value = mock.MagicMock(
        content="```json\n{\n  \"recommendations\": [\n    {\n      \"book_id\": 1,\n      \"book_title\": \"Clean Code\",\n      \"relevance_score\": 0.95,\n      \"reasoning\": \"Highly recommended.\"\n    }\n  ]\n}\n```"
    )
    
    state: agent.AgentState = {
        "query": "test", 
        "books": [{"id": 1, "name": "Book"}], 
        "max_results": 1
    }
    result = agent._generate_recommendations(state)
    assert result["recommendations"] == [
        {
            "book_id": 1,
            "book_title": "Clean Code",
            "relevance_score": 0.95,
            "reasoning": "Highly recommended."
        }
    ]


@mock.patch("app.api.v1.recommendations.agent.ChatOpenAI")
def test_generate_recommendations_json_list(mock_chat: mock.MagicMock) -> None:
    """Should parse simple JSON list recommendations from LLM."""
    mock_instance = mock_chat.return_value
    mock_instance.invoke.return_value = mock.MagicMock(
        content="[\n  {\n    \"book_id\": 1,\n    \"book_title\": \"Clean Code\",\n    \"relevance_score\": 0.95,\n    \"reasoning\": \"Highly recommended.\"\n  }\n]"
    )
    
    state: agent.AgentState = {
        "query": "test", 
        "books": [{"id": 1, "name": "Book"}], 
        "max_results": 1
    }
    result = agent._generate_recommendations(state)
    assert result["recommendations"] == [
        {
            "book_id": 1,
            "book_title": "Clean Code",
            "relevance_score": 0.95,
            "reasoning": "Highly recommended."
        }
    ]


def test_should_recommend() -> None:
    """Should return recommend if books present, else END."""
    state_empty: agent.AgentState = {"query": "", "books": [], "max_results": 1}
    assert agent._should_recommend(state_empty) == agent.END
    
    state_full: agent.AgentState = {"query": "", "books": [{"id": 1}], "max_results": 1}
    assert agent._should_recommend(state_full) == "recommend"


def test_build_graph() -> None:
    """Should build a compiled graph."""
    graph = agent.build_graph()
    assert graph is not None
