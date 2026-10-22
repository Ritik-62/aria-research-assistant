
import tempfile
import unittest
from pathlib import Path

from report_generator import (
    ReportGenerationError,
    build_research_report,
    save_research_report,
)


class TestReportGenerator(unittest.TestCase):
    def setUp(self):
        self.question = "How is machine learning used in healthcare?"
        self.papers = [
            {
                "paper_id": "PAPER-001",
                "title": "Machine Learning in Healthcare",
                "authors": ["A. Researcher", "B. Scientist"],
                "year": 2024,
                "source": "test-source",
                "url": "https://example.org/paper-001",
            },
            {
                "paper_id": "PAPER-002",
                "title": "Clinical AI Evaluation",
                "authors": ["C. Researcher"],
                "year": 2025,
                "source": "test-source",
                "url": "",
            },
        ]
        self.analysis = (
            "## Key findings\n"
            "The supplied records discuss healthcare AI [P1]."
        )

    def test_includes_research_question(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )
        self.assertIn(self.question, report)

    def test_includes_analysis(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )
        self.assertIn(self.analysis, report)

    def test_assigns_paper_reference_labels(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )
        self.assertIn("[P1]", report)
        self.assertIn("[P2]", report)

    def test_includes_paper_metadata(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )
        self.assertIn("PAPER-001", report)
        self.assertIn("A. Researcher", report)
        self.assertIn("2024", report)

    def test_includes_available_link(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )
        self.assertIn("https://example.org/paper-001", report)

    def test_notes_verification_limitations(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )
        self.assertIn("Limitations and verification", report)
        self.assertIn("original papers", report)

    def test_rejects_empty_question(self):
        with self.assertRaises(ReportGenerationError):
            build_research_report(" ", self.papers, self.analysis)

    def test_rejects_empty_papers(self):
        with self.assertRaises(ReportGenerationError):
            build_research_report(self.question, [], self.analysis)

    def test_rejects_empty_analysis(self):
        with self.assertRaises(ReportGenerationError):
            build_research_report(self.question, self.papers, " ")

    def test_saves_report_to_disk(self):
        report = build_research_report(
            self.question, self.papers, self.analysis
        )

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "reports" / "report.md"
            saved_path = save_research_report(report, destination)

            self.assertTrue(saved_path.exists())
            self.assertEqual(saved_path.read_text(encoding="utf-8"), report)
            self.assertIn("# ARIA Research Report", report)


if __name__ == "__main__":
    unittest.main()
