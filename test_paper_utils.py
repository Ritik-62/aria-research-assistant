
import unittest

from paper_utils import (
    deduplicate_papers,
    normalize_paper,
    normalize_papers,
)


class TestPaperUtils(unittest.TestCase):

    def test_normalizes_semantic_scholar_style_fields(self):
        paper = normalize_paper({
            "paperId": "ABC123",
            "title": "  Research Paper  ",
            "authors": [
                {"name": "Alex Researcher"},
                {"name": "Sam Scientist"},
            ],
            "year": 2024,
            "abstract": "  An abstract.  ",
            "url": "https://example.com/paper",
        })

        self.assertEqual(paper["paper_id"], "ABC123")
        self.assertEqual(paper["title"], "Research Paper")
        self.assertEqual(
            paper["authors"],
            ["Alex Researcher", "Sam Scientist"],
        )
        self.assertEqual(paper["year"], 2024)
        self.assertEqual(paper["abstract"], "An abstract.")
        self.assertEqual(paper["source"], "unknown")

    def test_handles_missing_or_invalid_metadata(self):
        paper = normalize_paper({
            "title": None,
            "authors": None,
            "year": "unknown",
            "abstract": None,
        })

        self.assertEqual(paper["paper_id"], "")
        self.assertEqual(paper["title"], "")
        self.assertEqual(paper["authors"], [])
        self.assertEqual(paper["year"], 0)
        self.assertEqual(paper["abstract"], "")
        self.assertEqual(paper["source"], "unknown")

    def test_normalizes_authors_as_strings(self):
        paper = normalize_paper({
            "title": "Author Test",
            "authors": [" Alice ", "", "Bob"],
        })

        self.assertEqual(paper["authors"], ["Alice", "Bob"])

    def test_normalizes_multiple_papers(self):
        papers = normalize_papers([
            {"paper_id": "1", "title": "Paper One"},
            {"paperId": "2", "title": "Paper Two"},
        ])

        self.assertEqual(len(papers), 2)
        self.assertEqual(papers[0]["paper_id"], "1")
        self.assertEqual(papers[1]["paper_id"], "2")

    def test_deduplicates_matching_paper_ids(self):
        papers = normalize_papers([
            {
                "paper_id": "ABC",
                "title": "Original Title",
                "abstract": "",
            },
            {
                "paperId": "abc",
                "title": "Improved Title",
                "abstract": "New abstract.",
            },
        ])

        result = deduplicate_papers(papers)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Original Title")
        self.assertEqual(result[0]["abstract"], "New abstract.")

    def test_deduplicates_equivalent_titles(self):
        papers = normalize_papers([
            {"paper_id": "1", "title": "Retrieval-Augmented Generation"},
            {"paper_id": "2", "title": "Retrieval Augmented Generation!"},
        ])

        result = deduplicate_papers(papers)

        self.assertEqual(len(result), 1)

    def test_preserves_distinct_papers(self):
        papers = normalize_papers([
            {"paper_id": "1", "title": "Paper Alpha"},
            {"paper_id": "2", "title": "Paper Beta"},
        ])

        self.assertEqual(len(deduplicate_papers(papers)), 2)

    def test_merges_missing_metadata_from_duplicate(self):
        papers = normalize_papers([
            {
                "paper_id": "ABC",
                "title": "A Research Paper",
                "authors": [],
                "year": 0,
                "abstract": "",
                "source": "unknown",
                "url": "",
            },
            {
                "paper_id": "ABC",
                "title": "A Research Paper",
                "authors": ["Taylor Researcher"],
                "year": 2025,
                "abstract": "Useful abstract.",
                "source": "Semantic Scholar",
                "url": "https://example.com/paper",
            },
        ])

        result = deduplicate_papers(papers)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["authors"], ["Taylor Researcher"])
        self.assertEqual(result[0]["year"], 2025)
        self.assertEqual(result[0]["abstract"], "Useful abstract.")
        self.assertEqual(result[0]["source"], "Semantic Scholar")
        self.assertEqual(result[0]["url"], "https://example.com/paper")


if __name__ == "__main__":
    unittest.main()
