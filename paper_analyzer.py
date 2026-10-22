
"""Evidence-conscious academic paper analysis for ARIA."""

from collections.abc import Mapping, Sequence
from typing import Any


class PaperAnalysisError(ValueError):
    """Raised when research analysis inputs are invalid."""


def _get_field(paper: Any, *names: str) -> Any:
    """Read the first available field from a mapping or an object."""
    for name in names:
        if isinstance(paper, Mapping):
            value = paper.get(name)
        else:
            value = getattr(paper, name, None)

        if value is not None:
            return value

    return None


def _format_authors(authors: Any) -> str:
    """Convert common author representations into readable text."""
    if not authors:
        return "Not provided"

    if isinstance(authors, str):
        return authors.strip() or "Not provided"

    if isinstance(authors, Sequence) and not isinstance(
        authors, (str, bytes)
    ):
        names = []
        for author in authors:
            if isinstance(author, str):
                name = author.strip()
            elif isinstance(author, Mapping):
                name = author.get("name") or author.get("author_name")
                if name is None:
                    name = str(author)
            else:
                name = getattr(author, "name", None) or str(author)

            if name:
                names.append(str(name).strip())

        return ", ".join(names) if names else "Not provided"

    return str(authors)


def _format_paper(paper: Any, index: int) -> str:
    """Format one paper without inventing missing metadata."""
    title = _get_field(paper, "title") or "Untitled paper"
    authors = _format_authors(_get_field(paper, "authors", "author"))
    year = _get_field(paper, "year", "publication_year")
    abstract = _get_field(paper, "abstract")
    url = _get_field(paper, "url", "paper_url")
    paper_id = _get_field(paper, "paper_id", "paperId", "id")

    return (
        f"[P{index}]\n"
        f"Title: {title}\n"
        f"Authors: {authors}\n"
        f"Year: {year if year is not None else 'Not provided'}\n"
        f"Paper ID: {paper_id or 'Not provided'}\n"
        f"URL: {url or 'Not provided'}\n"
        f"Abstract: {abstract or 'Not provided'}"
    )


def build_analysis_prompt(
    research_question: str,
    papers: Sequence[Any],
) -> str:
    """Build an evidence-conscious prompt from a question and papers."""
    if not isinstance(research_question, str) or not research_question.strip():
        raise PaperAnalysisError("Research question must not be empty.")

    if isinstance(papers, (str, bytes)) or not isinstance(papers, Sequence):
        raise PaperAnalysisError("Papers must be a sequence of paper records.")

    if not papers:
        raise PaperAnalysisError("At least one paper is required.")

    formatted_papers = "\n\n".join(
        _format_paper(paper, index)
        for index, paper in enumerate(papers, start=1)
    )

    return f"""
You are ARIA, an academic research assistant.

Research question:
{research_question.strip()}

Source papers:
{formatted_papers}

Instructions:
1. Use only the information supplied in the source-paper records.
2. Do not invent facts, results, methods, quotations, or citations.
3. Distinguish what the sources explicitly state from your own cautious
   interpretation.
4. If the supplied metadata or abstracts do not support a conclusion,
   state that the evidence is insufficient.
5. Do not claim to have read a full paper when only its metadata or
   abstract was provided.
6. Refer to supplied records using their identifiers, such as [P1]
   and [P2]. Do not invent bibliographic details.
7. Avoid treating a missing abstract as evidence that a paper has no
   relevant findings.

Return the analysis using these sections:

## Research question
Restate the question briefly.

## Key findings
Summarize relevant findings supported by the supplied records.
Attach [P#] references to claims where possible.

## Evidence by paper
For each relevant paper, explain what the supplied information supports
and identify whether the assessment is based on metadata or an abstract.

## Limitations and uncertainty
Identify missing information, methodological details not provided,
and conclusions that cannot be drawn reliably.

## Potential research gaps
List possible unanswered questions suggested by the available records.
Label these as preliminary possibilities, not proven gaps in the literature.

## Overall assessment
Give a concise answer to the research question and state how strong
the supplied evidence is.
""".strip()


def analyze_papers(
    research_question: str,
    papers: Sequence[Any],
    llm_client: Any,
) -> str:
    """Generate an analysis using an existing ARIA-compatible LLM client."""
    prompt = build_analysis_prompt(research_question, papers)

    if llm_client is None or not callable(
        getattr(llm_client, "generate", None)
    ):
        raise PaperAnalysisError(
            "llm_client must provide a callable generate(prompt) method."
        )

    return llm_client.generate(prompt)
