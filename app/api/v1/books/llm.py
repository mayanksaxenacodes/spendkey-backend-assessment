# Copyright © 2026 SpendKey. All Rights Reserved.
"""LLM integration utilities for book enrichment."""
import os
import typing as t

try:
    from langchain.chat_models import ChatOpenAI
except ImportError:
    from langchain_openai import ChatOpenAI
try:
    from langchain.prompts import ChatPromptTemplate
except ImportError:
    from langchain_core.prompts import ChatPromptTemplate

_MODEL = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_KEY") or "mock-key",
)

_SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that writes concise book summaries "
            "for an online bookstore catalogue.",
        ),
        (
            "human",
            "Write a short summary (2-3 sentences) for the following book.\n\n"
            "Title: {book_title}\n"
            "Description: {description}",
        ),
    ]
)


def generate_summary(
    book_title: str,
    description: t.Optional[str],
) -> str:
    """Generate an AI summary for a book using the configured LLM.

    Args:
        book_title: The title of the book.
        description: The book's existing description text.

    Returns:
        A short AI-generated summary string.
    """
    chain = _SUMMARY_PROMPT | _MODEL
    result = chain.invoke(
        {
            "book_title": book_title,
            "description": description or "No description available.",
        }
    )
    return result.content
