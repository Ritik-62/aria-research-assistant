
"""Generate evidence-traceable Markdown research reports."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


class ReportGenerationError(ValueError):
    """Raised when report inputs are invalid."""


def _field(record: Any, *names: str) -> Any:
    """Read a field from a dictionary or an object."""
    for name in names:
        if isinstance(record, Mapping):
            value = record.get(name)
        else:
            value = getattr(record, name, None)

        if value is not None:
            return value

    return None


def _clean(value: Any, default: str = "Not provided") -> str:
    """Convert metadata into a compact, single-line string."""
    if value is None:
        return default

    text = " ".join(str(value).split()).strip()
    if not text:
        return default

    return text.replace("|", "\\|")


def build_research_report(
    research_question: str,
    papers: Sequence[Any],
    analysis: str,
) -> str:
    """Build a Markdown report with references to retrieved papers."""
    if not isinstance(research_question, str) or not research_question.strip():
        raise ReportGenerationError("Research question must not be empty.")

    if isinstance(papers, (str, bytes)) or not isinstance(papers, Sequence):
        raise ReportGenerationError("Papers must be a sequence of paper records.")

    if not papers:
        raise ReportGenerationError("At least one paper is required.")

    if not isinstance(analysis, str) or not analysis.strip():
        raise ReportGenerationError("Analysis must not be empty.")

    lines = [
        "# ARIA Research Report",
        "",
        "## Research question",
        "",
        research_question.strip(),
        "",
        "## Analysis",
        "",
        analysis.strip(),
        "",
        "## Retrieved papers",
        "",
        "The references below identify the records supplied to ARIA. "
        "Their inclusion does not independently verify their findings.",
        "",
    ]

    for index, paper in enumerate(papers, start=1):
        title = _clean(_field(paper, "title"), "Untitled paper")
        paper_id = _clean(
            _field(paper, "paper_id", "paperId", "id"),
            "Not provided",
        )
        authors = _field(paper, "authors")
        year = _clean(_field(paper, "year"), "Unknown")
        source = _clean(_field(paper, "source"), "Unknown")
        url = _clean(_field(paper, "url", "paper_url"), "")

        if isinstance(authors, str):
            authors_text = _clean(authors)
        elif isinstance(authors, Sequence):
            authors_text = _clean(
                ", ".join(str(author) for author in authors)
            )
        else:
            authors_text = "Not provided"

        lines.extend([
            f"### [P{index}] {title}",
            "",
            f"- **Paper ID:** {paper_id}",
            f"- **Authors:** {authors_text}",
            f"- **Year:** {year}",
            f"- **Source:** {source}",
        ])

        if url:
            lines.append(f"- **Link:** <{url}>")

        lines.append("")

    lines.extend([
        "## Limitations and verification",
        "",
        "- Retrieved metadata may be incomplete or inaccurate.",
        "- Search results may not represent all relevant literature.",
        "- Verify important claims against the original papers.",
        "- Do not treat an offline evidence inventory as a verified "
        "scientific synthesis.",
        "",
    ])

    return "\n".join(lines)


def save_research_report(
    report: str,
    output_path: str | Path = "reports/research_report.md",
) -> Path:
    """Save a non-empty Markdown report and return its path."""
    if not isinstance(report, str) or not report.strip():
        raise ReportGenerationError("Report content must not be empty.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report.rstrip() + "\n", encoding="utf-8")

    return path
