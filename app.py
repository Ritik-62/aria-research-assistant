
from research_planner import create_research_plan


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


if __name__ == "__main__":
    main()
