
import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import app


SAMPLE_PLAN = {
    "research_question": "How is machine learning used in healthcare?",
    "objective": "Review machine learning applications in healthcare.",
    "search_queries": ["machine learning healthcare"],
    "inclusion_criteria": [],
    "exclusion_criteria": [],
    "expected_outputs": [],
}

SAMPLE_PAPER = {
    "paper_id": "P1",
    "title": "Machine Learning in Healthcare",
    "authors": ["A. Researcher"],
    "year": 2024,
    "abstract": "A sample research abstract.",
    "source": "test",
    "url": "https://example.com/paper1",
}

SAMPLE_RESULT = {
    "papers": [SAMPLE_PAPER],
    "queries_attempted": 1,
    "failed_queries": [],
    "errors": {},
}


class FakeLLMClient:
    def generate(self, prompt):
        return "Mock response"


class TestAppIntegration(unittest.TestCase):
    @patch("app.create_research_plan", return_value=SAMPLE_PLAN)
    @patch("app.retrieve_papers", return_value=SAMPLE_RESULT)
    @patch(
        "app.create_offline_analysis",
        return_value="Offline evidence report",
    )
    def test_app_runs_offline_analysis(
        self,
        mock_offline_analysis,
        mock_retrieve,
        mock_plan,
    ):
        with patch(
            "builtins.input",
            side_effect=[
                "How is machine learning used in healthcare?",
                "1",
                "2",
                "n",
            ],
        ):
            output = StringIO()
            with redirect_stdout(output):
                app.main()

        mock_retrieve.assert_called_once()
        mock_offline_analysis.assert_called_once_with(
            SAMPLE_PLAN["research_question"],
            SAMPLE_RESULT["papers"],
        )
        self.assertIn("Offline evidence report", output.getvalue())

    @patch("app.create_research_plan", return_value=SAMPLE_PLAN)
    @patch("app.retrieve_papers", return_value=SAMPLE_RESULT)
    @patch("app.analyze_papers", return_value="Mock AI analysis")
    @patch("llm_client.create_openai_llm_client")
    def test_app_connects_openai_analysis(
        self,
        mock_create_client,
        mock_analyze,
        mock_retrieve,
        mock_plan,
    ):
        mock_client = FakeLLMClient()
        mock_create_client.return_value = mock_client

        with patch(
            "builtins.input",
            side_effect=[
                "How is machine learning used in healthcare?",
                "1",
                "1",
                "n",
            ],
        ):
            output = StringIO()
            with redirect_stdout(output):
                app.main()

        mock_create_client.assert_called_once()
        mock_analyze.assert_called_once_with(
            SAMPLE_PLAN["research_question"],
            SAMPLE_RESULT["papers"],
            mock_client,
        )
        self.assertIn("Mock AI analysis", output.getvalue())


if __name__ == "__main__":
    unittest.main()
