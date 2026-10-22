
import re
from typing import TypedDict


class NormalizedPaper(TypedDict):
    paper_id: str
    title: str
    authors: list[str]
    year: int
    abstract: str
    source: str
    url: str


def normalize_paper(paper: dict) -> NormalizedPaper:
    """Convert a paper record into ARIA's standard format."""

    paper_id = str(
        paper.get("paper_id") or paper.get("paperId") or ""
    ).strip()

    title = str(paper.get("title") or "").strip()

    raw_authors = paper.get("authors") or []

    if isinstance(raw_authors, str):
        raw_authors = [raw_authors]

    authors = []

    if isinstance(raw_authors, list):
        for author in raw_authors:
            if isinstance(author, dict):
                name = author.get("name", "")
            else:
                name = author

            if isinstance(name, str) and name.strip():
                authors.append(name.strip())

    year = paper.get("year")

    if not isinstance(year, int) or isinstance(year, bool):
        year = 0

    abstract = paper.get("abstract") or ""
    if not isinstance(abstract, str):
        abstract = ""

    source = paper.get("source") or "unknown"
    if not isinstance(source, str):
        source = "unknown"

    url = paper.get("url") or ""
    if not isinstance(url, str):
        url = ""

    return {
        "paper_id": paper_id,
        "title": title,
        "authors": authors,
        "year": year,
        "abstract": abstract.strip(),
        "source": source.strip() or "unknown",
        "url": url.strip(),
    }


def normalize_papers(papers: list[dict]) -> list[NormalizedPaper]:
    """Normalize a collection of paper records."""
    return [normalize_paper(paper) for paper in papers]


def _normalize_title(title: str) -> str:
    """Create a comparable key from a paper title."""
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def _merge_missing_metadata(
    existing: NormalizedPaper,
    duplicate: NormalizedPaper,
) -> None:
    """Fill missing fields using metadata from a duplicate record."""

    for field in ("paper_id", "title", "abstract", "url"):
        if not existing[field] and duplicate[field]:
            existing[field] = duplicate[field]

    if not existing["authors"] and duplicate["authors"]:
        existing["authors"] = duplicate["authors"]

    if not existing["year"] and duplicate["year"]:
        existing["year"] = duplicate["year"]

    if (
        existing["source"] == "unknown"
        and duplicate["source"] != "unknown"
    ):
        existing["source"] = duplicate["source"]


def deduplicate_papers(
    papers: list[NormalizedPaper],
) -> list[NormalizedPaper]:
    """Remove duplicate IDs or titles and merge missing metadata."""

    unique_papers: list[NormalizedPaper] = []

    for paper in papers:
        duplicate = None

        for existing in unique_papers:
            same_id = (
                bool(paper["paper_id"])
                and paper["paper_id"].casefold()
                == existing["paper_id"].casefold()
            )

            same_title = (
                bool(paper["title"])
                and _normalize_title(paper["title"])
                == _normalize_title(existing["title"])
            )

            if same_id or same_title:
                duplicate = existing
                break

        if duplicate is None:
            unique_papers.append(paper.copy())
        else:
            _merge_missing_metadata(duplicate, paper)

    return unique_papers
