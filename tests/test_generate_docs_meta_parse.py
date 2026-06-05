import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


class GenerateDocsMetaParseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        if "fitz" not in sys.modules:
            import types

            fitz_stub = types.ModuleType("fitz")
            fitz_stub.open = lambda *args, **kwargs: None
            sys.modules["fitz"] = fitz_stub
        if "llm" not in sys.modules:
            import types

            llm_stub = types.ModuleType("llm")

            class DummyDeepSeekClient:
                def __init__(self, *args, **kwargs):
                    pass

            llm_stub.DeepSeekClient = DummyDeepSeekClient
            llm_stub.resolve_max_output_tokens = lambda default=393216: default
            sys.modules["llm"] = llm_stub

        src_path = root / "src" / "6.generate_docs.py"
        spec = importlib.util.spec_from_file_location("gen6_mod", src_path)
        cls.mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(cls.mod)

    def test_parse_meta_from_front_matter(self):
        md_path = Path("docs/201706/12/1706.03762v1-attention-is-all-you-need.md")
        item = self.mod._parse_generated_md_to_meta(str(md_path), "pid", "quick")
        self.assertEqual(item["title_en"], "Attention Is All You Need")
        self.assertTrue(item["authors"].startswith("Ashish Vaswani"))
        self.assertIn("query:transformer", item["tags"])
        self.assertEqual(item["date"], "20170612")
        self.assertIn("https://arxiv.org/pdf", item["pdf"])
        self.assertEqual(item["selection_source"], "fresh_fetch")

    def test_parse_fallback_to_legacy_meta_lines(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "paper.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "selection_source: fresh_fetch",
                        "title: Legacy title",
                        "---",
                        "**Authors**: Legacy A, Legacy B",
                        "**Date**: 20260301",
                        "**PDF**: https://example.com/paper.pdf",
                        "**TLDR**: legacy tldr text",
                        "",
                        "## Abstract",
                        "abstract body",
                    ]
                ),
                encoding="utf-8",
            )
            item = self.mod._parse_generated_md_to_meta(
                str(path),
                "legacy",
                "deep",
                "cache_hint",
            )
            self.assertEqual(item["authors"], "Legacy A, Legacy B")
            self.assertEqual(item["date"], "20260301")
            self.assertEqual(item["pdf"], "https://example.com/paper.pdf")
            self.assertEqual(item["tldr"], "legacy tldr text")
            self.assertEqual(item["selection_source"], "cache_hint")

    def test_parse_source_from_front_matter(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "paper.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "title: Test title",
                        "source: biorxiv",
                        "selection_source: fresh_fetch",
                        "---",
                        "## Abstract",
                        "abstract body",
                    ]
                ),
                encoding="utf-8",
            )
            item = self.mod._parse_generated_md_to_meta(str(path), "pid", "quick")
            self.assertEqual(item["source"], "biorxiv")
            self.assertEqual(item["selection_source"], "fresh_fetch")

    def test_extract_sidebar_tags_hides_composite_suffix(self):
        paper = {
            "llm_score": 8.0,
            "llm_tags": [
                "query:sr:composite",
                "query:sr",
                "keyword:equation-discovery",
            ],
        }
        tags = self.mod.extract_sidebar_tags(paper)
        self.assertEqual(tags[0], ("score", "8.0"))
        self.assertIn(("query", "sr"), tags)
        self.assertIn(("query", "equation-discovery"), tags)
        self.assertNotIn(("query", "sr:composite"), tags)
        self.assertEqual(tags.count(("query", "sr")), 1)

    def test_build_markdown_content_writes_media_json_front_matter(self):
        paper = {
            "title": "Figure Test",
            "authors": ["Ada Lovelace"],
            "published": "2026-03-26T00:00:00+00:00",
            "link": "https://arxiv.org/pdf/1234.5678",
            "abstract": "abstract body",
            "source": "arxiv",
            "_figure_assets": [
                {
                    "url": "assets/figures/arxiv/1234.5678/fig-001.webp",
                    "caption": "",
                    "page": 2,
                    "index": 1,
                    "width": 1280,
                    "height": 720,
                }
            ],
            "_table_assets": [
                {
                    "url": "assets/tables/arxiv/1234.5678/table-001.webp",
                    "caption": "",
                    "page": 3,
                    "index": 1,
                    "width": 1000,
                    "height": 560,
                }
            ],
        }
        md = self.mod.build_markdown_content(paper, "quick", "", "", [])
        meta = self.mod._parse_front_matter(md)
        self.assertIn("figures_json", meta)
        self.assertIn("tables_json", meta)
        figures = json.loads(meta["figures_json"])
        tables = json.loads(meta["tables_json"])
        self.assertEqual(len(figures), 1)
        self.assertEqual(figures[0]["url"], "assets/figures/arxiv/1234.5678/fig-001.webp")
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0]["url"], "assets/tables/arxiv/1234.5678/table-001.webp")

    def test_journal_without_open_pdf_writes_landing_link_not_pdf(self):
        paper = {
            "title": "Journal Test",
            "authors": ["Ada Lovelace"],
            "published": "2026-06-01T00:00:00+00:00",
            "source": "journal",
            "doi": "10.1000/test",
            "journal": "Environmental Science & Technology",
            "journal_label": "EST",
            "link": "https://doi.org/10.1000/test",
            "abs_url": "https://doi.org/10.1000/test",
            "open_pdf_available": False,
            "open_pdf_status": "no_open_pdf",
            "open_pdf_note": "No legal open PDF found; skip screenshots and figure extraction.",
            "abstract": "",
        }
        md = self.mod.build_markdown_content(paper, "quick", "", "", [])
        meta = self.mod._parse_front_matter(md)
        self.assertNotIn("pdf", meta)
        self.assertEqual(meta["link"], "https://doi.org/10.1000/test")
        self.assertEqual(meta["doi"], "10.1000/test")
        self.assertEqual(meta["journal"], "Environmental Science & Technology")
        self.assertEqual(meta["journal_label"], "EST")
        self.assertEqual(meta["open_pdf_available"], "false")
        self.assertIn("journal metadata sources", md)
        self.assertNotIn("arXiv did not provide an abstract", md)
        self.assertEqual(self.mod.resolve_paper_pdf_url(paper), "")

    def test_journal_with_open_pdf_uses_pdf_url(self):
        paper = {
            "source": "journal",
            "link": "https://doi.org/10.1000/test",
            "pdf_url": "https://example.org/open.pdf",
            "open_pdf_available": True,
        }
        self.assertEqual(self.mod.resolve_paper_pdf_url(paper), "https://example.org/open.pdf")

    def test_journal_doi_landing_page_is_not_used_as_pdf(self):
        paper = {
            "source": "journal",
            "link": "https://doi.org/10.1016/j.jhazmat.2026.142173",
            "pdf_url": "https://doi.org/10.1016/j.jhazmat.2026.142173",
            "open_pdf_available": True,
            "open_pdf_status": "open_pdf",
        }
        self.assertEqual(self.mod.resolve_paper_pdf_url(paper), "")

    def test_parse_generated_meta_preserves_journal_fields(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "paper.md"
            path.write_text(
                "\n".join(
                    [
                        "---",
                        "title: Journal title",
                        "authors: Ada Lovelace",
                        "date: 2026-06-01",
                        "link: https://doi.org/10.1000/test",
                        "source: journal",
                        "doi: 10.1000/test",
                        "journal: Environmental Science & Technology",
                        "journal_label: EST",
                        "open_pdf_status: no_open_pdf",
                        "open_pdf_available: false",
                        "---",
                        "",
                        "## Abstract",
                        "No abstract was available from the journal metadata sources for this paper.",
                    ]
                ),
                encoding="utf-8",
            )

            item = self.mod._parse_generated_md_to_meta(str(path), "journal-id", "quick")

            self.assertEqual(item["source"], "journal")
            self.assertEqual(item["link"], "https://doi.org/10.1000/test")
            self.assertEqual(item["doi"], "10.1000/test")
            self.assertEqual(item["journal"], "Environmental Science & Technology")
            self.assertEqual(item["journal_label"], "EST")
            self.assertEqual(item["open_pdf_status"], "no_open_pdf")
            self.assertEqual(item["open_pdf_available"], "false")
            self.assertIn("journal metadata sources", item["abstract_en"])
            self.assertNotIn("arXiv did not provide an abstract", item["abstract_en"])

    def test_update_sidebar_uses_journal_landing_link(self):
        with tempfile.TemporaryDirectory() as d:
            sidebar = Path(d) / "_sidebar.md"
            sidebar.write_text("* [首页](/)\n* Daily Papers\n", encoding="utf-8")

            self.mod.update_sidebar(
                str(sidebar),
                "20260601",
                [],
                [("202606/01/journal-10-1000-test", "Journal Sidebar Test", [("score", "8.8")])],
                {},
                paper_link_by_id={
                    "202606/01/journal-10-1000-test": "https://doi.org/10.1000/test",
                },
            )

            text = sidebar.read_text(encoding="utf-8")
            self.assertIn("https://doi.org/10.1000/test", text)
            self.assertNotIn("https://arxiv.org/abs/journal-10-1000-test", text)

    def test_resolve_sidebar_url_keeps_arxiv_abs_link(self):
        paper = {
            "source": "arxiv",
            "id": "1706.03762v1",
            "link": "https://arxiv.org/pdf/1706.03762v1",
        }
        self.assertEqual(
            self.mod.resolve_paper_sidebar_url(paper, "#/202606/01/1706.03762v1-test"),
            "https://arxiv.org/abs/1706.03762v1",
        )

    def test_paper_id_single_mode_rejects_non_arxiv_ids(self):
        self.assertTrue(self.mod.looks_like_arxiv_id("https://arxiv.org/abs/1706.03762v1"))
        self.assertFalse(self.mod.looks_like_arxiv_id("10.1000/test"))
        self.assertFalse(self.mod.looks_like_arxiv_id("journal-10-1000-test"))

    def test_maybe_generate_paper_media_accepts_biorxiv(self):
        calls = []

        def fake_ensure_paper_media(**kwargs):
            calls.append(kwargs)
            return (
                [{"url": "assets/figures/biorxiv/pid/fig-001.webp"}],
                [{"url": "assets/tables/biorxiv/pid/table-001.webp"}],
            )

        original = self.mod.ensure_paper_media
        self.mod.ensure_paper_media = fake_ensure_paper_media
        try:
            figures, tables = self.mod.maybe_generate_paper_media(
                {
                    "id": "biorxiv-abc",
                    "source": "biorxiv",
                },
                docs_dir="docs",
                paper_id="202603/26/biorxiv-abc",
                pdf_url="https://www.biorxiv.org/content/test.full.pdf",
            )
        finally:
            self.mod.ensure_paper_media = original

        self.assertEqual(len(figures), 1)
        self.assertEqual(len(tables), 1)
        self.assertEqual(calls[0]["source_key"], "biorxiv")

    def test_maybe_generate_paper_figures_keeps_legacy_return(self):
        original = self.mod.ensure_paper_media
        self.mod.ensure_paper_media = lambda **kwargs: (
            [{"url": "assets/figures/arxiv/pid/fig-001.webp"}],
            [{"url": "assets/tables/arxiv/pid/table-001.webp"}],
        )
        try:
            figures = self.mod.maybe_generate_paper_figures(
                {"id": "1234.5678", "source": "arxiv"},
                docs_dir="docs",
                paper_id="1234.5678",
                pdf_url="https://arxiv.org/pdf/1234.5678",
            )
        finally:
            self.mod.ensure_paper_media = original

        self.assertEqual(figures, [{"url": "assets/figures/arxiv/pid/fig-001.webp"}])

    def test_generate_glance_prompt_requires_richer_fields(self):
        captured = {}

        def fake_call_llm_structured_json(client, messages, **kwargs):
            captured["client"] = client
            captured["messages"] = messages
            captured["kwargs"] = kwargs
            return {
                "tldr": "这是一段足够长的中文速览摘要，用于覆盖研究背景、核心方法和主要贡献。",
                "motivation": "这是一段研究动机说明。",
                "method": "这是一段方法说明。",
                "result": "这是一段结果说明。",
                "conclusion": "这是一段结论说明。",
            }

        fallback_client = object()
        original_client = self.mod.LLM_CLIENT
        original_call = self.mod.call_llm_structured_json
        self.mod.LLM_CLIENT = fallback_client
        self.mod.call_llm_structured_json = fake_call_llm_structured_json
        try:
            out = self.mod.generate_glance_overview("Title", "Abstract")
        finally:
            self.mod.LLM_CLIENT = original_client
            self.mod.call_llm_structured_json = original_call

        self.assertIn("**TLDR**", out)
        self.assertIs(captured["client"], fallback_client)
        self.assertEqual(captured["kwargs"]["max_tokens"], 16 * 1024)
        prompt = captured["messages"][2]["content"]
        self.assertIn("150-220个中文字符", prompt)
        self.assertIn("30-70个中文字符", prompt)
        self.assertIn("问题背景→核心方法→关键结果→贡献意义", prompt)
        self.assertNotIn("每个字段一句话概括", prompt)

    def test_generate_glance_uses_explicit_client(self):
        explicit_client = object()
        global_client = object()
        captured = {}

        def fake_call_llm_structured_json(client, messages, **kwargs):
            captured["client"] = client
            return {
                "tldr": "这是一段足够长的中文速览摘要，用于覆盖研究背景、核心方法和主要贡献。",
                "motivation": "这是一段研究动机说明。",
                "method": "这是一段方法说明。",
                "result": "这是一段结果说明。",
                "conclusion": "这是一段结论说明。",
            }

        original_client = self.mod.LLM_CLIENT
        original_call = self.mod.call_llm_structured_json
        self.mod.LLM_CLIENT = global_client
        self.mod.call_llm_structured_json = fake_call_llm_structured_json
        try:
            out = self.mod.generate_glance_overview("Title", "Abstract", client=explicit_client)
        finally:
            self.mod.LLM_CLIENT = original_client
            self.mod.call_llm_structured_json = original_call

        self.assertIn("**TLDR**", out)
        self.assertIs(captured["client"], explicit_client)

    def test_translate_uses_16k_and_explicit_client(self):
        explicit_client = object()
        global_client = object()
        captured = {}

        def fake_call_llm_structured_json(client, messages, **kwargs):
            captured["client"] = client
            captured["kwargs"] = kwargs
            return {"title_zh": "中文标题", "abstract_zh": "中文摘要"}

        original_client = self.mod.LLM_CLIENT
        original_call = self.mod.call_llm_structured_json
        self.mod.LLM_CLIENT = global_client
        self.mod.call_llm_structured_json = fake_call_llm_structured_json
        try:
            title_zh, abstract_zh = self.mod.translate_title_and_abstract_to_zh(
                "Title",
                "Abstract",
                client=explicit_client,
            )
        finally:
            self.mod.LLM_CLIENT = original_client
            self.mod.call_llm_structured_json = original_call

        self.assertEqual(title_zh, "中文标题")
        self.assertEqual(abstract_zh, "中文摘要")
        self.assertIs(captured["client"], explicit_client)
        self.assertEqual(captured["kwargs"]["max_tokens"], 16 * 1024)

    def test_empty_run_home_keeps_latest_non_empty_quick_report(self):
        with tempfile.TemporaryDirectory() as d:
            docs_dir = Path(d)
            day_dir = docs_dir / "202606" / "04"
            empty_dir = docs_dir / "20260507-20260605"
            day_dir.mkdir(parents=True, exist_ok=True)
            empty_dir.mkdir(parents=True, exist_ok=True)
            (day_dir / "papers.meta.json").write_text(
                json.dumps(
                    {
                        "label": "2026-06-04",
                        "date": "2026-06-04",
                        "count": 1,
                        "papers": [
                            {
                                "paper_id": "202606/04/journal-wr-transit-time",
                                "section": "quick",
                                "title_en": "Transit time modeling framework for predicting freshwater salinization in urban catchments",
                                "score": "6.0",
                                "tags": "query:coastal-pfas",
                                "evidence": "urban salinization",
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (empty_dir / "papers.meta.json").write_text(
                json.dumps(
                    {
                        "label": "2026-05-07 ~ 2026-06-05",
                        "count": 0,
                        "papers": [],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            content = self.mod.build_home_readme_content(
                str(docs_dir),
                "20260507-20260605",
                "2026-05-07 ~ 2026-06-05",
                "2026-06-05 00:00:00 UTC",
                True,
                [],
                [],
                {},
            )

            self.assertIn("2026-06-04", content)
            self.assertIn(
                "Transit time modeling framework for predicting freshwater salinization in urban catchments",
                content,
            )
            self.assertNotIn("2026-05-07 ~ 2026-06-05", content)

    def test_load_journal_quick_papers_merges_history_without_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            docs_dir = Path(d) / "docs"
            journals_dir = docs_dir / "journals"
            history_dir = journals_dir / "history"
            history_dir.mkdir(parents=True, exist_ok=True)
            june_paper = {
                "id": "journal-10-1016-test",
                "source": "journal",
                "doi": "10.1016/test",
                "title": "Transit time modeling framework for predicting freshwater salinization in urban catchments",
                "published": "2026-06-01T00:00:00+00:00",
                "journal": "Water Research",
                "journal_label": "WR",
                "link": "https://doi.org/10.1016/test",
                "abs_url": "https://doi.org/10.1016/test",
                "open_pdf_available": False,
                "open_pdf_status": "no_open_pdf",
                "tags": ["environmental-science"],
            }
            may_paper = {
                "id": "journal-10-1021-may",
                "source": "journal",
                "doi": "10.1021/may",
                "title": "May journal paper",
                "published": "2026-05-15T00:00:00+00:00",
                "journal_label": "EST Letters",
            }
            old_paper = {
                "id": "journal-10-1021-old",
                "source": "journal",
                "doi": "10.1021/old",
                "title": "Old journal paper outside range",
                "published": "2026-04-15T00:00:00+00:00",
                "journal_label": "EST",
            }
            (journals_dir / "journal-papers.json").write_text(
                json.dumps([june_paper], ensure_ascii=False),
                encoding="utf-8",
            )
            (history_dir / "2026-06.json").write_text(
                json.dumps([june_paper], ensure_ascii=False),
                encoding="utf-8",
            )
            (history_dir / "2026-05.json").write_text(
                json.dumps([may_paper, old_paper], ensure_ascii=False),
                encoding="utf-8",
            )
            (history_dir / "index.json").write_text(
                json.dumps(
                    {
                        "months": [
                            {"month": "2026-06", "path": "docs/journals/history/2026-06.json"},
                            {"month": "2026-05", "path": "docs/journals/history/2026-05.json"},
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            original_root = self.mod.ROOT_DIR
            self.mod.ROOT_DIR = str(docs_dir.parent)
            try:
                papers = self.mod.load_journal_quick_papers(str(docs_dir), "20260507-20260605")
            finally:
                self.mod.ROOT_DIR = original_root

            self.assertEqual(len(papers), 2)
            self.assertEqual({paper["doi"] for paper in papers}, {"10.1016/test", "10.1021/may"})
            self.assertEqual(papers[0]["source"], "journal")
            self.assertIn("query:WR", papers[0]["llm_tags"])

            merged = self.mod.merge_journal_papers_into_quick(
                [{"doi": "10.1016/test", "title": "Already selected"}],
                papers,
            )
            self.assertEqual(len(merged), 2)

    def test_prepare_paper_paths_compacts_very_long_journal_titles(self):
        with tempfile.TemporaryDirectory() as d:
            long_title = (
                "A risk nutrition duality framework for assessing drinking water suitability "
                "in an intensively cultivated alluvial plain a case study of Xiayi country "
                "south center Huang Huai plain China"
            )
            md_path, txt_path, paper_id = self.mod.prepare_paper_paths(
                d,
                "20260507-20260605",
                long_title,
                "journal-10-1016-j-jhazmat-2026-142102",
            )

            self.assertLessEqual(len(Path(md_path).name), self.mod.MAX_PAPER_BASENAME_LENGTH + 3)
            self.assertTrue(md_path.endswith(".md"))
            self.assertTrue(txt_path.endswith(".txt"))
            self.assertIn("20260507-20260605/", paper_id)
            self.assertIn("-", Path(md_path).stem[-11:])


if __name__ == "__main__":
    unittest.main()
