import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def _load_module():
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "src"
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    src_path = root / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("main_pipeline_mod", src_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class MainPipelineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def _write_rrf_input(self, root: Path, token: str) -> Path:
        filtered_dir = root / "archive" / token / "filtered"
        filtered_dir.mkdir(parents=True, exist_ok=True)
        path = filtered_dir / f"arxiv_papers_{token}.json"
        payload = {
            "generated_at": "2026-03-10T00:00:00+00:00",
            "papers": [
                {"id": "p1", "title": "Paper 1", "abstract": "A"},
                {"id": "p2", "title": "Paper 2", "abstract": "B"},
                {"id": "p3", "title": "Paper 3", "abstract": "C"},
            ],
            "queries": [
                {
                    "type": "intent_query",
                    "tag": "query:test",
                    "paper_tag": "query:test",
                    "query_text": "test query",
                    "sim_scores": {
                        "p1": {"score": 0.9, "rank": 1},
                        "p2": {"score": 0.6, "rank": 2},
                        "p3": {"score": 0.2, "rank": 3},
                    },
                }
            ],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_resolve_summary_step_env_uses_summary_overrides(self):
        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "base-key",
                "DEEPSEEK_BASE_URL": "https://api.deepseek.com",
                "SUMMARY_API_KEY": "summary-key",
                "SUMMARY_BASE_URL": "https://summary.example.com/v1",
                "SUMMARY_MODEL": "deepseek-v4-flash",
            },
            clear=True,
        ):
            env = self.mod.resolve_summary_step_env()

        self.assertEqual(env["DEEPSEEK_API_KEY"], "summary-key")
        self.assertEqual(env["SUMMARY_API_KEY"], "summary-key")
        self.assertEqual(env["DEEPSEEK_BASE_URL"], "https://summary.example.com/v1")
        self.assertEqual(env["LLM_PRIMARY_BASE_URL"], "https://summary.example.com/v1")
        self.assertEqual(env["DEEPSEEK_MODEL"], "deepseek-v4-flash")

    def test_merge_paper_lists_dedupes_by_doi_and_preserves_metadata(self):
        merged = self.mod.merge_paper_lists(
            [
                {
                    "id": "journal-old",
                    "doi": "10.1000/test",
                    "title": "Old",
                    "metadata_sources": ["crossref"],
                    "source_weight": 5,
                }
            ],
            [
                {
                    "id": "journal-new",
                    "doi": "10.1000/test",
                    "abstract": "Updated abstract",
                    "metadata_sources": ["openalex"],
                    "source_weight": 10,
                },
                {"id": "arxiv-1", "title": "Other"},
            ],
        )

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["id"], "journal-old")
        self.assertEqual(merged[0]["abstract"], "Updated abstract")
        self.assertEqual(merged[0]["metadata_sources"], ["crossref", "openalex"])
        self.assertEqual(merged[0]["source_weight"], 10)

    def test_journal_sources_enabled_from_runtime_append(self):
        with patch.dict(os.environ, {"DPR_APPEND_PAPER_SOURCES": "journal"}, clear=True):
            self.assertTrue(self.mod.journal_sources_enabled({}))

    def test_fetch_and_merge_journal_sources_writes_into_raw_pool(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            raw_dir = root / "archive" / "20260601" / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw_path = raw_dir / "arxiv_papers_20260601.json"
            raw_path.write_text(
                json.dumps(
                    [
                        {
                            "id": "arxiv-1",
                            "doi": "10.1000/base",
                            "title": "Base paper",
                            "source": "arxiv",
                        }
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            calls = []

            def fake_run_step(label, args, env=None):
                calls.append((label, args, env))
                output_path = Path(args[args.index("--output") + 1])
                output_path.write_text(
                    json.dumps(
                        [
                            {
                                "id": "journal-1",
                                "doi": "10.1000/journal",
                                "title": "PFAS journal paper",
                                "published": "2026-06-15",
                                "source": "journal",
                                "journal_label": "EST",
                                "open_pdf_available": False,
                                "open_pdf_status": "no_open_pdf",
                                "source_weight": 10,
                            }
                        ],
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.dict(
                os.environ,
                {
                    "DPR_ENABLE_JOURNAL_SOURCES": "1",
                    "DPR_JOURNAL_ROWS_PER_JOURNAL": "7",
                    "DPR_JOURNAL_MONTH": "2026-06",
                    "DPR_JOURNAL_QUERY": "PFAS",
                },
                clear=True,
            ):
                self.mod.fetch_and_merge_journal_sources(
                    python=sys.executable,
                    raw_path=str(raw_path),
                    run_date_token="20260601",
                    fetch_days=30,
                    config={},
                )

            self.assertEqual(len(calls), 1)
            label, args, _ = calls[0]
            self.assertEqual(label, "Step 1b - fetch journal sources")
            self.assertIn("--rows-per-journal", args)
            self.assertEqual(args[args.index("--rows-per-journal") + 1], "7")
            self.assertIn("--month", args)
            self.assertEqual(args[args.index("--month") + 1], "2026-06")
            self.assertNotIn("--days", args)
            self.assertIn("--query", args)
            self.assertEqual(args[args.index("--query") + 1], "PFAS")

            merged = json.loads(raw_path.read_text(encoding="utf-8"))
            self.assertEqual([row["id"] for row in merged], ["arxiv-1", "journal-1"])
            self.assertEqual(merged[1]["source"], "journal")
            self.assertEqual(merged[1]["open_pdf_status"], "no_open_pdf")
            latest = json.loads((root / "docs" / "journals" / "journal-papers.json").read_text(encoding="utf-8"))
            month_rows = json.loads((root / "docs" / "journals" / "history" / "2026-06.json").read_text(encoding="utf-8"))
            index = json.loads((root / "docs" / "journals" / "history" / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(latest[0]["id"], "journal-1")
            self.assertEqual(month_rows[0]["doi"], "10.1000/journal")
            self.assertEqual(index["latest"], "2026-06")

    def test_fetch_and_merge_journal_sources_records_empty_month_for_website(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            raw_dir = root / "archive" / "20250601" / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            raw_path = raw_dir / "arxiv_papers_20250601.json"
            raw_path.write_text("[]", encoding="utf-8")

            def fake_run_step(label, args, env=None):
                output_path = Path(args[args.index("--output") + 1])
                output_path.write_text("[]", encoding="utf-8")

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.dict(
                os.environ,
                {
                    "DPR_ENABLE_JOURNAL_SOURCES": "1",
                    "DPR_JOURNAL_MONTH": "2025-06",
                },
                clear=True,
            ):
                self.mod.fetch_and_merge_journal_sources(
                    python=sys.executable,
                    raw_path=str(raw_path),
                    run_date_token="20250601",
                    fetch_days=30,
                    config={},
                )

            latest = json.loads((root / "docs" / "journals" / "journal-papers.json").read_text(encoding="utf-8"))
            month_rows = json.loads((root / "docs" / "journals" / "history" / "2025-06.json").read_text(encoding="utf-8"))
            index = json.loads((root / "docs" / "journals" / "history" / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(latest, [])
            self.assertEqual(month_rows, [])
            self.assertEqual(index["months"][0]["month"], "2025-06")
            self.assertEqual(index["months"][0]["count"], 0)

    def test_fetch_and_merge_journal_sources_refreshes_empty_days_result(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            raw_dir = root / "archive" / "20250601" / "raw"
            latest_dir = root / "docs" / "journals"
            raw_dir.mkdir(parents=True, exist_ok=True)
            latest_dir.mkdir(parents=True, exist_ok=True)
            raw_path = raw_dir / "arxiv_papers_20250601.json"
            raw_path.write_text("[]", encoding="utf-8")
            (latest_dir / "journal-papers.json").write_text(
                json.dumps([{"id": "stale", "published": "2025-05-01"}], ensure_ascii=False),
                encoding="utf-8",
            )

            def fake_run_step(label, args, env=None):
                output_path = Path(args[args.index("--output") + 1])
                output_path.write_text("[]", encoding="utf-8")

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.dict(
                os.environ,
                {"DPR_ENABLE_JOURNAL_SOURCES": "1"},
                clear=True,
            ):
                self.mod.fetch_and_merge_journal_sources(
                    python=sys.executable,
                    raw_path=str(raw_path),
                    run_date_token="20250601",
                    fetch_days=30,
                    config={},
                )

            latest = json.loads((latest_dir / "journal-papers.json").read_text(encoding="utf-8"))
            self.assertEqual(latest, [])

    def test_sync_journal_website_data_from_docs_meta_adds_generated_journal_papers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            docs_dir = root / "docs"
            meta_dir = docs_dir / "202606" / "04"
            latest_dir = docs_dir / "journals"
            history_dir = latest_dir / "history"
            meta_dir.mkdir(parents=True, exist_ok=True)
            latest_dir.mkdir(parents=True, exist_ok=True)
            history_dir.mkdir(parents=True, exist_ok=True)
            (latest_dir / "journal-papers.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "journal-old",
                            "source": "journal",
                            "doi": "10.1021/acs.est.5c16011",
                            "title": "Existing EST paper",
                            "published": "2026-06-03",
                            "journal_label": "EST",
                            "open_pdf_available": False,
                            "open_pdf_status": "no_open_pdf",
                        }
                    ],
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (meta_dir / "papers.meta.json").write_text(
                json.dumps(
                    {
                        "papers": [
                            {
                                "source": "journal",
                                "title_en": "Transit time modeling framework for predicting freshwater salinization in urban catchments",
                                "authors": "Shantanu V. Bhide, Stanley B. Grant",
                                "date": "2026-06-01",
                                "pdf": "https://doi.org/10.1016/j.watres.2026.125692",
                                "link": "",
                                "abstract_en": "Urban catchment salinization abstract.",
                                "doi": "10.1016/j.watres.2026.125692",
                                "journal": "Water Research",
                                "journal_label": "WR",
                                "tags": "query:coastal-pfas",
                            },
                            {
                                "source": "arxiv",
                                "title_en": "Non journal paper",
                                "date": "2026-06-01",
                            },
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            with patch.object(self.mod, "ROOT_DIR", str(root)):
                result = self.mod.sync_journal_website_data_from_docs_meta(str(docs_dir))

            self.assertEqual(result["synced"], 1)
            latest = json.loads((latest_dir / "journal-papers.json").read_text(encoding="utf-8"))
            dois = {row["doi"] for row in latest}
            self.assertIn("10.1021/acs.est.5c16011", dois)
            self.assertIn("10.1016/j.watres.2026.125692", dois)
            wr = next(row for row in latest if row["doi"] == "10.1016/j.watres.2026.125692")
            self.assertEqual(wr["journal_label"], "WR")
            self.assertEqual(wr["authors"], ["Shantanu V. Bhide", "Stanley B. Grant"])
            self.assertEqual(wr["open_pdf_available"], False)
            self.assertEqual(wr["open_pdf_status"], "no_open_pdf")
            self.assertIsNone(wr["pdf_url"])
            self.assertEqual(wr["abs_url"], "https://doi.org/10.1016/j.watres.2026.125692")

            month_rows = json.loads((history_dir / "2026-06.json").read_text(encoding="utf-8"))
            self.assertIn("10.1016/j.watres.2026.125692", {row["doi"] for row in month_rows})
            index = json.loads((history_dir / "index.json").read_text(encoding="utf-8"))
            self.assertEqual(index["latest"], "2026-06")

    def test_main_runs_local_rerank_without_remote_rerank_base(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            token = "20260310"
            self._write_rrf_input(root, token)
            calls = []

            def fake_run_step(label, args, env=None):
                calls.append((label, args, env))

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "resolve_run_date_token", return_value=token
            ), patch.object(
                self.mod, "resolve_sidebar_date_label", return_value=None
            ), patch.object(
                self.mod, "parse_trace_ids", return_value=[]
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.object(
                sys, "argv", ["main.py"]
            ), patch.dict(
                os.environ,
                {"LLM_PRIMARY_BASE_URL": "https://api.openai.com/v1"},
                clear=True,
            ):
                self.mod.main()

            labels = [item[0] for item in calls]
            self.assertIn("Step 3 - Rerank", labels)
            self.assertIn("Step 4 - LLM refine", labels)

    def test_main_keeps_local_rerank_in_deepseek_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src_dir = root / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            token = "20260310"
            self._write_rrf_input(root, token)
            calls = []

            def fake_run_step(label, args, env=None):
                calls.append((label, args, env))

            with patch.object(self.mod, "ROOT_DIR", str(root)), patch.object(
                self.mod, "SRC_DIR", str(src_dir)
            ), patch.object(
                self.mod, "resolve_run_date_token", return_value=token
            ), patch.object(
                self.mod, "resolve_sidebar_date_label", return_value=None
            ), patch.object(
                self.mod, "parse_trace_ids", return_value=[]
            ), patch.object(
                self.mod, "run_step", side_effect=fake_run_step
            ), patch.object(
                sys, "argv", ["main.py"]
            ), patch.dict(
                os.environ,
                {"LLM_PRIMARY_BASE_URL": "https://api.deepseek.com"},
                clear=True,
            ):
                self.mod.main()

            labels = [item[0] for item in calls]
            self.assertIn("Step 3 - Rerank", labels)


if __name__ == "__main__":
    unittest.main()
