
from research_planner import create_research_plan
from paper_search import search_papers


def main():
    print("=" * 60)
    print("ARIA — Academic Research & Innovation Assistant")
    print("=" * 60)

    research_question = input("\nEnter your research question: ")

    try:
        plan = create_research_plan(research_question)
    except ValueError as error:
        print(f"\nInput error: {error}")
        return

    print("\nRESEARCH PLAN")
    print("-" * 60)

    print("\nResearch question:")
    print(plan["research_question"])

    print("\nObjective:")
    print(plan["objective"])

    print("\nSuggested search queries:")
    for number, query in enumerate(plan["search_queries"], start=1):
        print(f"{number}. {query}")

    print("\nInclusion criteria:")
    for criterion in plan["inclusion_criteria"]:
        print(f"- {criterion}")

    print("\nExclusion criteria:")
    for criterion in plan["exclusion_criteria"]:
        print(f"- {criterion}")

    print("\nExpected outputs:")
    for output in plan["expected_outputs"]:
        print(f"- {output}")

    print("\nSAMPLE PAPER SEARCH")
    print("-" * 60)
    print("WARNING: These are fictional development records.")

    papers = search_papers(research_question, limit=5)

    if not papers:
        print("No matching sample records found.")
    else:
        for paper in papers:
            print(f"\n[{paper['paper_id']}] {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            print(f"Year: {paper['year']}")
            print(f"Abstract: {paper['abstract']}")
            print(f"Source type: {paper['source']}")


if __name__ == "__main__":
    main()
