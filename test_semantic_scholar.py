
import json
import unittest
from io import BytesIO
from unittest.mock import patch

from semantic_scholar import search_semantic_scholar


SAMPLE_RESPONSE = {
    "total": 1,
    "data": [
        {
            "paperId": "abc123",
            "title": "Example Research Paper",
            "authors": [
                {"authorId": "1", "name": "Alex Researcher"},
                {"authorId": "2", "name": "Sam Scientist"},
            ],
            "year": 2024,
            "abstract": "An example abstract about research.",
            "url": "https://www.semanticscholar.org/paper/abc123",
        }
    ],
}


class TestSemanticScholar(unittest.TestCase):

    @patch("semantic_scholar.urlopen")
    def test_normalizes_api_results(self, mock_urlopen):
        response = BytesIO(json.dumps(SAMPLE_RESPONSE).encode("utf-8"))
        mock_urlopen.return_value.__enter__.return_value = response

        papers = search_semantic_scholar("example research")

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["paper_id"], "abc123")
        self.assertEqual(papers[0]["title"], "Example Research Paper")
        self.assertEqual(
            papers[0]["authors"],
            ["Alex Researcher", "Sam Scientist"],
        )
        self.assertEqual(papers[0]["year"], 2024)
        self.assertEqual(papers[0]["source"], "Semantic Scholar")

    def test_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            search_semantic_scholar("   ")

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            search_semantic_scholar("research", limit=0)

        with self.assertRaises(ValueError):
            search_semantic_scholar("research", limit=101)

    @patch("semantic_scholar.urlopen")
    def test_empty_api_results_return_empty_list(self, mock_urlopen):
        response = BytesIO(
            json.dumps({"total": 0, "data": []}).encode("utf-8")
        )
        mock_urlopen.return_value.__enter__.return_value = response

        self.assertEqual(search_semantic_scholar("unmatched topic"), [])


if __name__ == "__main__":
    unittest.main()
