
from research_planner import create_research_plan
from paper_search import search_papers
from semantic_scholar import search_semantic_scholar


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

    print("\nPAPER SEARCH")
    print("-" * 60)
    print("1. Sample data (offline)")
    print("2. Semantic Scholar (live API)")

    choice = input("Choose search source [1/2]: ").strip()

    try:
        if choice == "2":
            print("\nSearching Semantic Scholar...")
            papers = search_semantic_scholar(
                research_question,
                limit=5,
            )
        elif choice == "1":
            print("\nSearching local sample records...")
            print("WARNING: Sample records are fictional.")
            papers = search_papers(research_question, limit=5)
        else:
            print("Invalid choice. Please select 1 or 2.")
            return

    except (ValueError, RuntimeError) as error:
        print(f"\nSearch error: {error}")
        return

    if not papers:
        print("\nNo matching papers found.")
        return

    print(f"\nFound {len(papers)} paper(s):")

    for paper in papers:
        print(f"\n[{paper['paper_id']}] {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Year: {paper['year'] or 'Unknown'}")
        print(f"Abstract: {paper['abstract'] or 'Not available'}")
        print(f"Source: {paper['source']}")

        if paper.get("url"):
            print(f"Link: {paper['url']}")


if __name__ == "__main__":
    main()
