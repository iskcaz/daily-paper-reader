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

    def test_keyword_haystack_includes_enriched_metadata(self):
        paper = {
            "title": "Vegetable uptake study",
            "abstract": "",
            "openalex_concepts": ["Environmental chemistry"],
            "semantic_fields_of_study": ["PFAS remediation"],
        }

        self.assertTrue(self.mod._keyword_hit(self.mod.keyword_haystack(paper), ["PFAS"]))

    def test_fetch_filters_keywords_after_openalex_enrichment(self):
        original_load_watchlist = self.mod.load_watchlist
        original_fetch_crossref_journal = self.mod.fetch_crossref_journal
        original_enrich_openalex = self.mod.enrich_with_openalex
        original_enrich_semantic = self.mod.enrich_with_semantic_scholar_batch
        original_enrich_unpaywall = self.mod.enrich_with_unpaywall
        try:
            self.mod.load_watchlist = lambda path: {
                "default_tags": ["environmental-science"],
                "journals": [
                    {
                        "key": "est",
                        "name": "Environmental Science & Technology",
                        "short_label": "EST",
                        "issns": ["0013-936X"],
                        "source_weight": 10,
                    }
                ],
            }
            self.mod.fetch_crossref_journal = lambda *args, **kwargs: [
                {
                    "DOI": "10.1021/acs.est.enriched",
                    "type": "journal-article",
                    "title": ["Vegetable uptake study"],
                    "container-title": ["Environmental Science & Technology"],
                    "published-online": {"date-parts": [[2026, 6, 1]]},
                    "URL": "https://doi.org/10.1021/acs.est.enriched",
                }
            ]

            def enrich_openalex(paper, **kwargs):
                paper["abstract"] = "This enriched abstract discusses PFAS uptake in crops."
                paper["metadata_sources"].append("openalex")

            self.mod.enrich_with_openalex = enrich_openalex
            self.mod.enrich_with_semantic_scholar_batch = lambda papers, **kwargs: None
            self.mod.enrich_with_unpaywall = lambda paper, **kwargs: None

            import tempfile

            with tempfile.TemporaryDirectory() as d:
                output = pathlib.Path(d) / "journal.json"
                papers = self.mod.fetch_journal_sources(
                    days=30,
                    output_file=str(output),
                    watchlist_file="unused.yaml",
                    query="PFAS",
                    enrich_semantic=True,
                    enrich_unpaywall=True,
                    sleep_seconds=0,
                )

            self.assertEqual(len(papers), 1)
            self.assertEqual(papers[0]["doi"], "10.1021/acs.est.enriched")
            self.assertIn("openalex", papers[0]["metadata_sources"])
        finally:
            self.mod.load_watchlist = original_load_watchlist
            self.mod.fetch_crossref_journal = original_fetch_crossref_journal
            self.mod.enrich_with_openalex = original_enrich_openalex
            self.mod.enrich_with_semantic_scholar_batch = original_enrich_semantic
            self.mod.enrich_with_unpaywall = original_enrich_unpaywall

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
