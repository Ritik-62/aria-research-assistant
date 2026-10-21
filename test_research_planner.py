import unittest
from research_planner import create_research_plan


class TestResearchPlanner(unittest.TestCase):

    def test_creates_plan_for_valid_question(self):
        question = (
            "How can retrieval-augmented generation "
            "improve academic literature reviews?"
        )

        plan = create_research_plan(question)

        self.assertEqual(plan["research_question"], question)
        self.assertTrue(plan["objective"])
        self.assertGreaterEqual(len(plan["search_queries"]), 3)
        self.assertTrue(plan["inclusion_criteria"])
        self.assertTrue(plan["exclusion_criteria"])
        self.assertTrue(plan["expected_outputs"])

    def test_removes_extra_whitespace(self):
        plan = create_research_plan(
            "   How does AI support scientific discovery?   "
        )

        self.assertEqual(
            plan["research_question"],
            "How does AI support scientific discovery?"
        )

    def test_rejects_empty_question(self):
        with self.assertRaises(ValueError):
            create_research_plan("   ")

    def test_rejects_question_that_is_too_short(self):
        with self.assertRaises(ValueError):
            create_research_plan("AI")


if __name__ == "__main__":
    unittest.main()