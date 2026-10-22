
"""Command-line entry point for ARIA."""

from research_planner import create_research_plan
from retrieval_pipeline import retrieve_papers
from paper_analyzer import analyze_papers, create_offline_analysis
from report_generator import (
    build_research_report,
    save_research_report,
)


def main():
    print("=" * 60)
    print("ARIA — Academic Research & Innovation Assistant")
    print("=" * 60)

    # Step 1: Create the research plan.
    research_question = input("\nEnter your research question: ")

    try:
        plan = create_research_plan(research_question)
    except ValueError as error:
        print(f"\nInput error: {error}")
        return

    print("\nRESEARCH PLAN")
    print("-" * 60)
    print(f"\nResearch question:\n{plan['research_question']}")
    print(f"\nObjective:\n{plan['objective']}")

    print("\nSuggested search queries:")
    for number, query in enumerate(plan["search_queries"], start=1):
        print(f"{number}. {query}")

    # Step 2: Retrieve papers.
    print("\nPAPER RETRIEVAL")
    print("-" * 60)
    print("1. Sample data (offline)")
    print("2. Semantic Scholar (live API)")

    search_choice = input("Choose search source [1/2]: ").strip()

    if search_choice == "1":
        print("\nSearching sample data...")
        result = retrieve_papers(plan["search_queries"])

    elif search_choice == "2":
        print("\nSearching Semantic Scholar...")
        from semantic_scholar import search_semantic_scholar

        result = retrieve_papers(
            plan["search_queries"],
            search_fn=search_semantic_scholar,
        )

    else:
        print("Invalid search choice. Please select 1 or 2.")
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
        print(
            f"\n{number}. "
            f"[{paper['paper_id'] or 'No ID'}] {paper['title']}"
        )
        print(f"Authors: {', '.join(paper['authors']) or 'Unknown'}")
        print(f"Year: {paper['year'] or 'Unknown'}")
        print(f"Abstract: {paper['abstract'] or 'Not available'}")
        print(f"Source: {paper['source']}")

        if paper["url"]:
            print(f"Link: {paper['url']}")

    # Step 3: Analyze the retrieved papers.
    print("\nPAPER ANALYSIS")
    print("-" * 60)
    print("1. OpenAI analysis (sends a live API request)")
    print("2. Offline evidence report (no OpenAI API call)")

    analysis_choice = input("Choose analysis mode [1/2]: ").strip()

    if analysis_choice == "2":
        try:
            analysis = create_offline_analysis(
                plan["research_question"],
                papers,
            )
        except ValueError as error:
            print(f"\nCould not create offline analysis: {error}")
            return

        print("\nOFFLINE PAPER ANALYSIS")
        print("-" * 60)
        print(analysis)

    elif analysis_choice == "1":
        from llm_client import (
            create_openai_llm_client,
            LLMConfigurationError,
            LLMProviderError,
        )

        try:
            llm_client = create_openai_llm_client()
            analysis = analyze_papers(
                plan["research_question"],
                papers,
                llm_client,
            )
        except (LLMConfigurationError, LLMProviderError) as error:
            print(f"\nOpenAI analysis could not be completed: {error}")
            return
        except ValueError as error:
            print(f"\nInvalid analysis input: {error}")
            return

        print("\nAI PAPER ANALYSIS")
        print("-" * 60)
        print(analysis)

    else:
        print("Invalid analysis choice. Please select 1 or 2.")
        return

    # Step 4: Generate the Markdown research report.
    try:
        report = build_research_report(
            research_question=plan["research_question"],
            papers=papers,
            analysis=analysis,
        )
    except ValueError as error:
        print(f"\nCould not generate research report: {error}")
        return

    print("\n" + "=" * 60)
    print("ARIA RESEARCH REPORT")
    print("=" * 60)
    print(report)

    # Step 5: Optionally save the report.
    save_choice = input(
        "\nSave this report as a Markdown file? (y/n): "
    ).strip().lower()

    if save_choice == "y":
        try:
            saved_path = save_research_report(
                report,
                "reports/research_report.md",
            )
            print(f"Report saved to: {saved_path}")
        except OSError as error:
            print(f"\nCould not save report: {error}")

    elif save_choice == "n":
        print("Report was not saved.")

    else:
        print("Unrecognized choice. Report was not saved.")


if __name__ == "__main__":
    main()
