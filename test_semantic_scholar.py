
import json
import unittest
from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from semantic_scholar import search_semantic_scholar


SAMPLE_PAYLOAD = {
    "data": [
        {
            "paperId": "abc123",
            "title": "Research with Retrieval-Augmented Generation",
            "authors": [{"name": "Alice"}, {"name": "Bob"}],
            "year": 2025,
            "abstract": "A sample abstract.",
            "url": "https://example.com/paper",
        }
    ]
}


class FakeResponse:
    def __init__(self, payload):
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


class TestSemanticScholar(unittest.TestCase):

    def test_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            search_semantic_scholar("   ")

    def test_rejects_invalid_limit(self):
        for limit in (0, 101, 1.5, True):
            with self.subTest(limit=limit):
                with self.assertRaises(ValueError):
                    search_semantic_scholar("AI research", limit=limit)

    @patch("semantic_scholar.urlopen")
    def test_normalizes_api_results(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(SAMPLE_PAYLOAD)

        papers = search_semantic_scholar("RAG", limit=1)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["paper_id"], "abc123")
        self.assertEqual(papers[0]["authors"], ["Alice", "Bob"])
        self.assertEqual(papers[0]["source"], "Semantic Scholar")

    @patch("semantic_scholar.urlopen")
    def test_empty_api_results_return_empty_list(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse({"data": []})

        self.assertEqual(search_semantic_scholar("unknown topic"), [])

    @patch("semantic_scholar.urlopen")
    def test_handles_rate_limit(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            "https://example.com", 429, "Rate limited", {}, None
        )

        with self.assertRaisesRegex(RuntimeError, "rate limit"):
            search_semantic_scholar("AI research")

    @patch("semantic_scholar.urlopen")
    def test_handles_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            "https://example.com", 500, "Server error", {}, None
        )

        with self.assertRaisesRegex(RuntimeError, "HTTP 500"):
            search_semantic_scholar("AI research")

    @patch("semantic_scholar.urlopen")
    def test_handles_network_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Network unavailable")

        with self.assertRaisesRegex(RuntimeError, "Could not connect"):
            search_semantic_scholar("AI research")

    @patch("semantic_scholar.urlopen")
    def test_handles_invalid_json(self, mock_urlopen):
        response = FakeResponse({})
        response.body = b"not valid JSON"
        mock_urlopen.return_value = response

        with self.assertRaisesRegex(RuntimeError, "invalid data"):
            search_semantic_scholar("AI research")

    @patch("semantic_scholar.urlopen")
    def test_rejects_unexpected_payload(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(["unexpected", "data"])

        with self.assertRaisesRegex(RuntimeError, "unexpected response"):
            search_semantic_scholar("AI research")


if __name__ == "__main__":
    unittest.main()
