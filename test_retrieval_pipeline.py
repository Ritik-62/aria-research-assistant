
import unittest

from retrieval_pipeline import retrieve_papers


def make_paper(paper_id, title):
    return {
        "paper_id": paper_id,
        "title": title,
        "authors": ["Test Author"],
        "year": 2024,
        "abstract": "Test abstract",
        "source": "test",
        "url": "",
    }


class TestRetrievalPipeline(unittest.TestCase):

    def test_combines_results_from_multiple_queries(self):
        def fake_search(query, limit):
            return [make_paper(query, f"Research on {query}")]

        result = retrieve_papers(
            ["machine learning", "medical imaging"],
            search_fn=fake_search,
        )

        self.assertEqual(result["queries_attempted"], 2)
        self.assertEqual(len(result["papers"]), 2)
        self.assertEqual(result["failed_queries"], [])
        self.assertEqual(result["errors"], {})

    def test_deduplicates_results_from_different_queries(self):
        def fake_search(query, limit):
            return [make_paper("PAPER-1", "A Shared Research Paper")]

        result = retrieve_papers(
            ["query one", "query two"],
            search_fn=fake_search,
        )

        self.assertEqual(len(result["papers"]), 1)

    def test_continues_when_one_query_fails(self):
        def fake_search(query, limit):
            if query == "broken query":
                raise RuntimeError("Temporary search failure")
            return [make_paper("PAPER-2", "Successful Research")]

        result = retrieve_papers(
            ["broken query", "working query"],
            search_fn=fake_search,
        )

        self.assertEqual(len(result["papers"]), 1)
        self.assertEqual(result["failed_queries"], ["broken query"])
        self.assertIn("broken query", result["errors"])

    def test_reports_when_all_queries_fail(self):
        def failing_search(query, limit):
            raise RuntimeError("Search unavailable")

        result = retrieve_papers(
            ["query one", "query two"],
            search_fn=failing_search,
        )

        self.assertEqual(result["papers"], [])
        self.assertEqual(len(result["failed_queries"]), 2)
        self.assertEqual(len(result["errors"]), 2)

    def test_rejects_empty_queries(self):
        with self.assertRaises(ValueError):
            retrieve_papers([])

    def test_rejects_invalid_limit(self):
        for limit in (0, -1, 1.5, True):
            with self.subTest(limit=limit):
                with self.assertRaises(ValueError):
                    retrieve_papers(["test query"], limit_per_query=limit)


if __name__ == "__main__":
    unittest.main()
