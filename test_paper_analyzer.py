
import unittest
from unittest.mock import Mock

from paper_analyzer import (
    PaperAnalysisError,
    analyze_papers,
    build_analysis_prompt,
)


class TestPaperAnalyzer(unittest.TestCase):
    def setUp(self):
        self.question = "How is retrieval-augmented generation evaluated?"
        self.papers = [
            {
                "paper_id": "paper-001",
                "title": "Evaluating Retrieval-Augmented Generation",
                "authors": ["A. Researcher", "B. Scientist"],
                "year": 2024,
                "abstract": (
                    "This study evaluates retrieval quality and "
                    "answer correctness."
                ),
                "url": "https://example.org/paper-001",
            }
        ]

    def test_prompt_includes_question_and_paper_evidence(self):
        prompt = build_analysis_prompt(self.question, self.papers)

        self.assertIn(self.question, prompt)
        self.assertIn("Evaluating Retrieval-Augmented Generation", prompt)
        self.assertIn("retrieval quality", prompt)
        self.assertIn("[P1]", prompt)

    def test_prompt_warns_against_invented_evidence(self):
        prompt = build_analysis_prompt(self.question, self.papers)

        self.assertIn("Do not invent facts", prompt)
        self.assertIn("Limitations and uncertainty", prompt)
        self.assertIn("Potential research gaps", prompt)

    def test_accepts_object_papers(self):
        paper = Mock()
        paper.title = "A test paper"
        paper.authors = ["C. Author"]
        paper.year = 2023
        paper.abstract = "A test abstract."
        paper.url = "https://example.org/test"
        paper.paper_id = "test-123"

        prompt = build_analysis_prompt(self.question, [paper])

        self.assertIn("A test paper", prompt)
        self.assertIn("A test abstract", prompt)

    def test_rejects_empty_question(self):
        with self.assertRaises(PaperAnalysisError):
            build_analysis_prompt("   ", self.papers)

    def test_rejects_empty_papers(self):
        with self.assertRaises(PaperAnalysisError):
            build_analysis_prompt(self.question, [])

    def test_rejects_invalid_paper_container(self):
        with self.assertRaises(PaperAnalysisError):
            build_analysis_prompt(self.question, "not a list")

    def test_calls_llm_and_returns_its_analysis(self):
        expected = "## Key findings\nThe supplied abstract reports..."
        llm = Mock()
        llm.generate.return_value = expected

        result = analyze_papers(self.question, self.papers, llm)

        self.assertEqual(result, expected)
        llm.generate.assert_called_once()
        prompt = llm.generate.call_args.args[0]
        self.assertIn(self.question, prompt)
        self.assertIn("Evaluating Retrieval-Augmented Generation", prompt)

    def test_rejects_client_without_generate_method(self):
        with self.assertRaises(PaperAnalysisError):
            analyze_papers(self.question, self.papers, object())


if __name__ == "__main__":
    unittest.main()
