
"""Combine multi-query paper searches into one clean collection."""

from typing import Callable, TypedDict

from paper_search import search_papers
from paper_utils import deduplicate_papers, normalize_papers


class RetrievalResult(TypedDict):
    papers: list[dict]
    queries_attempted: int
    failed_queries: list[str]
    errors: dict[str, str]


def retrieve_papers(
    queries: list[str],
    limit_per_query: int = 5,
    search_fn: Callable[[str, int], list[dict]] | None = None,
) -> RetrievalResult:
    """Search multiple queries, preserving results if some searches fail."""

    if not isinstance(queries, list) or not queries:
        raise ValueError("queries must be a non-empty list")

    if (
        not isinstance(limit_per_query, int)
        or isinstance(limit_per_query, bool)
        or limit_per_query < 1
    ):
        raise ValueError("limit_per_query must be a positive integer")

    if not all(isinstance(query, str) and query.strip() for query in queries):
        raise ValueError("Every query must be a non-empty string")

    # Default to offline mock search.
    if search_fn is None:
        search_fn = search_papers

    all_papers: list[dict] = []
    failed_queries: list[str] = []
    errors: dict[str, str] = {}

    for query in queries:
        try:
            results = search_fn(query, limit_per_query)

            if not isinstance(results, list):
                raise ValueError("Search function must return a list")

            all_papers.extend(results)

        except Exception as error:
            failed_queries.append(query)
            errors[query] = f"{type(error).__name__}: {error}"

    normalized = normalize_papers(all_papers)
    unique_papers = deduplicate_papers(normalized)

    return {
        "papers": unique_papers,
        "queries_attempted": len(queries),
        "failed_queries": failed_queries,
        "errors": errors,
    }
