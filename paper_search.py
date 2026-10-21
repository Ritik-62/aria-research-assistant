
import re
from typing import TypedDict


class Paper(TypedDict):
    paper_id: str
    title: str
    authors: list[str]
    year: int
    abstract: str
    source: str


SAMPLE_PAPERS: list[Paper] = [
    {
        "paper_id": "MOCK-001",
        "title": "AI-Assisted Academic Literature Review",
        "authors": ["Sample Author A", "Sample Author B"],
        "year": 2024,
        "abstract": (
            "This sample discusses artificial intelligence, "
            "academic literature reviews, research workflows, "
            "and methods for organizing scholarly evidence."
        ),
        "source": "mock",
    },
    {
        "paper_id": "MOCK-002",
        "title": "Retrieval-Augmented Generation for Research Assistants",
        "authors": ["Sample Author C"],
        "year": 2025,
        "abstract": (
            "This sample explores retrieval augmented generation, "
            "research assistants, document retrieval, and "
            "evidence-grounded answers."
        ),
        "source": "mock",
    },
    {
        "paper_id": "MOCK-003",
        "title": "Evaluating Search Systems for Scientific Discovery",
        "authors": ["Sample Author D", "Sample Author E"],
        "year": 2023,
        "abstract": (
            "This sample examines scholarly search, query matching, "
            "ranking methods, information retrieval, and evaluation "
            "of scientific discovery systems."
        ),
        "source": "mock",
    },
]




STOP_WORDS = {
    "a", "an", "and", "are", "can", "for", "how", "in", "is",
    "of", "on", "or", "the", "to", "what", "with", "improve",
}


def tokenize(text: str) -> set[str]:
    """Convert text into lowercase searchable words."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {word for word in words if word not in STOP_WORDS}


def search_papers(query: str, limit: int = 5) -> list[Paper]:
    """Search sample paper records using simple keyword matching."""
    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    query_words = tokenize(query)

    if not query_words:
        return []

    results: list[tuple[int, Paper]] = []

    for paper in SAMPLE_PAPERS:
        searchable_text = paper["title"] + " " + paper["abstract"]
        paper_words = tokenize(searchable_text)
        score = len(query_words & paper_words)

        if score > 0:
            results.append((score, paper))

    # Highest keyword overlap first.
    results.sort(key=lambda item: item[0], reverse=True)

    return [paper for _, paper in results[:limit]]

