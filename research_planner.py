from typing import TypedDict


class ResearchPlan(TypedDict):
    research_question: str
    objective: str
    search_queries: list[str]
    inclusion_criteria: list[str]
    exclusion_criteria: list[str]
    expected_outputs: list[str]



def create_research_plan(research_question: str) -> ResearchPlan:
    """Create a basic, structured plan for a literature review."""
    question = research_question.strip()

    if not question:
        raise ValueError("Research question cannot be empty.")

    if len(question) < 10:
        raise ValueError(
            "Please provide a more specific research question "
            "(at least 10 characters)."
        )

    plan: ResearchPlan = {
        "research_question": question,
        "objective": (
            "Identify relevant academic literature, compare "
            "existing approaches, and investigate potential "
            "research gaps."
        ),
        "search_queries": [
            question,
            f"{question} systematic review",
            f"{question} limitations future research",
        ],
        "inclusion_criteria": [
            "Academic papers relevant to the research question",
            "Studies that describe their methods or findings",
            "Sources with enough information to assess relevance",
        ],
        "exclusion_criteria": [
            "Duplicate records",
            "Sources unrelated to the research question",
            "Records without enough information to assess relevance",
        ],
        "expected_outputs": [
            "List of relevant papers",
            "Comparison of methods and findings",
            "Evidence-supported research-gap hypotheses",
        ],
    }

    return plan