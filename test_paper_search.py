
import unittest

from paper_search import search_papers


class TestPaperSearch(unittest.TestCase):

    def test_finds_relevant_papers(self):
        results = search_papers(
            "retrieval augmented generation research assistant"
        )
        self.assertGreater(len(results), 0)
        self.assertIn(
            "MOCK-002",
            [paper["paper_id"] for paper in results],
        )

    def test_search_is_case_insensitive(self):
        lower = search_papers("academic literature review")
        upper = search_papers("ACADEMIC LITERATURE REVIEW")

        self.assertEqual(
            [paper["paper_id"] for paper in lower],
            [paper["paper_id"] for paper in upper],
        )

    def test_limit_is_respected(self):
        results = search_papers("research", limit=1)
        self.assertLessEqual(len(results), 1)

    def test_empty_query_is_rejected(self):
        with self.assertRaises(ValueError):
            search_papers("   ")

    def test_invalid_limit_is_rejected(self):
        with self.assertRaises(ValueError):
            search_papers("research", limit=0)

    def test_unrelated_query_returns_no_results(self):
        results = search_papers(
            "underwater volcanoes on distant planets"
        )
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
