import importlib.util
import pathlib
import sys
import unittest


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class FetchJournalSourcesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = pathlib.Path(__file__).resolve().parents[1]
        src_dir = root / "src"
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
        cls.mod = _load_module(
            "fetch_journal_sources_mod",
            src_dir / "maintain" / "fetchers" / "fetch_journal_sources.py",
        )

    def test_normalize_crossref_item_outputs_project_paper_shape(self):
        raw = {
            "DOI": "10.1021/acs.est.5c00001",
            "type": "journal-article",
            "title": ["PFAS transport in estuarine sediments"],
            "container-title": ["Environmental Science & Technology"],
            "ISSN": ["0013-936X"],
            "author": [{"given": "Jane", "family": "Doe"}],
            "published-online": {"date-parts": [[2026, 6, 1]]},
            "URL": "https://doi.org/10.1021/acs.est.5c00001",
        }
        journal = {
            "key": "est",
            "name": "Environmental Science & Technology",
            "short_label": "EST",
            "source_weight": 10,
            "tags": ["core-journal"],
        }

        paper = self.mod.normalize_crossref_item(raw, journal, default_tags=["environmental-science"])

        self.assertIsNotNone(paper)
        self.assertEqual(paper["source"], "journal")
        self.assertEqual(paper["source_detail"], "crossref")
        self.assertEqual(paper["doi"], "10.1021/acs.est.5c00001")
        self.assertEqual(paper["journal_label"], "EST")
        self.assertEqual(paper["source_weight"], 10)
        self.assertIn("environmental-science", paper["categories"])
        self.assertEqual(paper["authors"], ["Jane Doe"])

    def test_openalex_inverted_index_to_abstract(self):
        raw = {"PFAS": [0], "transport": [1], "sediment": [2]}
        self.assertEqual(
            self.mod.abstract_from_openalex_inverted_index(raw),
            "PFAS transport sediment",
        )

    def test_month_arg_resolves_full_month(self):
        start, end = self.mod.parse_month_arg("2025-06")
        self.assertEqual(start.isoformat(), "2025-06-01")
        self.assertEqual(end.isoformat(), "2025-06-30")

    def test_resolve_fetch_date_window_prefers_month(self):
        start, end = self.mod.resolve_fetch_date_window(
            days=30,
            from_date="2024-01-01",
            until_date="2024-01-31",
            month="2025-02",
        )
        self.assertEqual(start.isoformat(), "2025-02-01")
        self.assertEqual(end.isoformat(), "2025-02-28")

    def test_finalize_marks_no_open_pdf(self):
        paper = {"abs_url": "https://doi.org/10.1/test", "pdf_url": ""}

        self.mod.finalize_open_pdf_status(paper)

        self.assertEqual(paper["open_pdf_status"], "no_open_pdf")
        self.assertIn("skip screenshots", paper["open_pdf_note"])
        self.assertEqual(paper["link"], "https://doi.org/10.1/test")

    def test_dedupe_by_doi_merges_metadata_sources(self):
        rows = [
            {"doi": "10.1/ABC", "title": "A", "metadata_sources": ["crossref"], "source_weight": 5},
            {"doi": "https://doi.org/10.1/abc", "abstract": "B", "metadata_sources": ["openalex"], "source_weight": 10},
        ]

        merged = self.mod.dedupe_by_doi(rows)

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["abstract"], "B")
        self.assertEqual(merged[0]["source_weight"], 10)
        self.assertEqual(merged[0]["metadata_sources"], ["crossref", "openalex"])


if __name__ == "__main__":
    unittest.main()
