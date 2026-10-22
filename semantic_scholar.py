
import json
from typing import TypedDict
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


class SemanticPaper(TypedDict):
    paper_id: str
    title: str
    authors: list[str]
    year: int
    abstract: str
    source: str
    url: str


def search_semantic_scholar(
    query: str,
    limit: int = 5,
) -> list[SemanticPaper]:
    """Search Semantic Scholar and normalize returned paper metadata."""

    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be empty.")

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")

    params = urlencode({
        "query": query,
        "limit": limit,
        "fields": "paperId,title,authors,year,abstract,url",
    })

    request = Request(
        f"{API_URL}?{params}",
        headers={
            "User-Agent": "ARIA-Research-Assistant/0.1",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        if error.code == 429:
            raise RuntimeError(
                "Semantic Scholar rate limit reached. "
                "Wait before trying again."
            ) from error

        raise RuntimeError(
            f"Semantic Scholar returned HTTP {error.code}."
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not connect to Semantic Scholar: {error.reason}"
        ) from error

    except (TimeoutError, json.JSONDecodeError) as error:
        raise RuntimeError(
            "The request timed out or the API returned invalid JSON."
        ) from error

    papers: list[SemanticPaper] = []

    for item in payload.get("data", []):
        paper_id = item.get("paperId")
        title = item.get("title")

        # Ignore records without the minimum useful identifiers.
        if not paper_id or not title:
            continue

        authors = [
            author["name"]
            for author in (item.get("authors") or [])
            if author.get("name")
        ]

        papers.append({
            "paper_id": paper_id,
            "title": title,
            "authors": authors,
            "year": item.get("year") or 0,
            "abstract": item.get("abstract") or "",
            "source": "Semantic Scholar",
            "url": item.get("url") or (
                f"https://www.semanticscholar.org/paper/{paper_id}"
            ),
        })

    return papers
