
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
    """Search Semantic Scholar and normalize paper metadata."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError("Limit must be an integer between 1 and 100.")

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")

    query = query.strip()

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

        if error.code == 401 or error.code == 403:
            raise RuntimeError(
                f"Semantic Scholar access denied (HTTP {error.code})."
            ) from error

        raise RuntimeError(
            f"Semantic Scholar returned HTTP {error.code}."
        ) from error

    except URLError as error:
        raise RuntimeError(
            f"Could not connect to Semantic Scholar: {error.reason}"
        ) from error

    except (TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as error:
        raise RuntimeError(
            "The request timed out or the API returned invalid data."
        ) from error

    if not isinstance(payload, dict):
        raise RuntimeError("Semantic Scholar returned an unexpected response.")

    data = payload.get("data", [])

    if not isinstance(data, list):
        raise RuntimeError("Semantic Scholar returned an invalid papers list.")

    papers: list[SemanticPaper] = []

    for item in data:
        if not isinstance(item, dict):
            continue

        paper_id = item.get("paperId")
        title = item.get("title")

        if not isinstance(paper_id, str) or not paper_id.strip():
            continue

        if not isinstance(title, str) or not title.strip():
            continue

        raw_authors = item.get("authors") or []
        authors = []

        if isinstance(raw_authors, list):
            authors = [
                author["name"]
                for author in raw_authors
                if isinstance(author, dict)
                and isinstance(author.get("name"), str)
                and author["name"].strip()
            ]

        year = item.get("year")
        if not isinstance(year, int) or isinstance(year, bool):
            year = 0

        abstract = item.get("abstract")
        if not isinstance(abstract, str):
            abstract = ""

        url = item.get("url")
        if not isinstance(url, str) or not url.strip():
            url = f"https://www.semanticscholar.org/paper/{paper_id}"

        papers.append({
            "paper_id": paper_id,
            "title": title.strip(),
            "authors": authors,
            "year": year,
            "abstract": abstract,
            "source": "Semantic Scholar",
            "url": url,
        })

    return papers
