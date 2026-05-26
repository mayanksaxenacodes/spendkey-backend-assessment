# Copyright © 2026 SpendKey. All Rights Reserved.
"""LangGraph agent for book recommendations."""
import os
import typing as t

try:
    from langchain.chat_models import ChatOpenAI
except ImportError:
    from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from app.api.v1.books import crud

# Agent state type definition.
AgentState = t.TypedDict(
    "AgentState",
    {
        "query": str,
        "books": list[dict[str, t.Any]],
        "max_results": int,
    },
)


def _fetch_inventory(state: AgentState) -> AgentState:
    """Retrieve the current book inventory from the database.

    Args:
        state: The current agent state.

    Returns:
        Updated state with book inventory loaded.
    """
    books = crud.list_books(limit=100, offset=0)
    state["books"] = books
    return state


def _generate_recommendations(state: AgentState) -> AgentState:
    """Use the LLM to generate book recommendations.

    Analyses the user query against the available book inventory and
    produces reasoned recommendations.

    Args:
        state: The current agent state with inventory loaded.

    Returns:
        Updated state with recommendations generated.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=os.environ.get("OPENAI_KEY"),
    )

    books_context = "\n".join(
        f"- ID: {b['id']}, Title: {b['name']}, "
        f"Description: {b.get('description', 'N/A')}, "
        f"Tags: {b.get('tags', [])}"
        for b in state["books"]
    )

    prompt = (
        f"Based on the following book inventory:\n\n{books_context}\n\n"
        f"Recommend up to {state['max_results']} books that best match "
        f"this query: '{state['query']}'\n\n"
        f"For each recommendation, provide the book ID, title, a relevance "
        f"score (0.0-1.0), and a brief reasoning."
    )

    result = llm.invoke(prompt)
    state["recommendations"] = result.content  # noqa: E501
    return state


def _should_recommend(state: AgentState) -> str:
    """Determine whether to proceed with generating recommendations.

    Args:
        state: The current agent state.

    Returns:
        The name of the next node to execute.
    """
    if len(state.get("books", [])) > 0:
        return END
    return END


def build_graph() -> StateGraph:
    """Construct the recommendation agent workflow graph.

    Returns:
        A compiled LangGraph StateGraph ready for invocation.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("fetch_inventory", _fetch_inventory)
    workflow.add_node("recommend", _generate_recommendations)

    workflow.set_entry_point("fetch_inventory")
    workflow.add_conditional_edges(
        "fetch_inventory",
        _should_recommend,
        {
            "recommend": "recommend",
            END: END,
        },
    )
    workflow.add_edge("recommend", END)

    return workflow.compile()
