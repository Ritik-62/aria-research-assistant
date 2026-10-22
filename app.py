
from research_planner import create_research_plan
from retrieval_pipeline import retrieve_papers


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

    print("\nPAPER RETRIEVAL")
    print("-" * 60)
    print("1. Sample data (offline)")
    print("2. Semantic Scholar (live API)")

    choice = input("Choose search source [1/2]: ").strip()

    if choice == "1":
        print("\nSearching multiple queries using sample data...")
        result = retrieve_papers(plan["search_queries"])

    elif choice == "2":
        print("\nSearching multiple queries using Semantic Scholar...")
        from semantic_scholar import search_semantic_scholar

        result = retrieve_papers(
            plan["search_queries"],
            search_fn=search_semantic_scholar,
        )

    else:
        print("Invalid choice. Please select 1 or 2.")
        return

    print(f"\nQueries attempted: {result['queries_attempted']}")
    print(f"Failed queries: {len(result['failed_queries'])}")
    print(f"Unique papers retrieved: {len(result['papers'])}")

    if result["errors"]:
        print("\nSearch warnings:")
        for query, error in result["errors"].items():
            print(f"- {query}: {error}")

    papers = result["papers"]

    if not papers:
        print("\nNo papers were retrieved successfully.")
        return

    print("\nRETRIEVED PAPERS")
    print("-" * 60)

    for number, paper in enumerate(papers, start=1):
        print(f"\n{number}. [{paper['paper_id'] or 'No ID'}] {paper['title']}")
        print(f"Authors: {', '.join(paper['authors']) or 'Unknown'}")
        print(f"Year: {paper['year'] or 'Unknown'}")
        print(f"Abstract: {paper['abstract'] or 'Not available'}")
        print(f"Source: {paper['source']}")

        if paper["url"]:
            print(f"Link: {paper['url']}")


if __name__ == "__main__":
    main()
