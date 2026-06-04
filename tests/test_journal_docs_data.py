import json
import pathlib
import unittest


class JournalDocsDataTest(unittest.TestCase):
    def test_committed_journal_history_index_matches_month_files(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        history_dir = root / "docs" / "journals" / "history"
        index_path = history_dir / "index.json"

        self.assertTrue(index_path.exists(), "docs/journals/history/index.json should be committed")
        index = json.loads(index_path.read_text(encoding="utf-8"))
        months = index.get("months")
        self.assertIsInstance(months, list)
        self.assertGreater(len(months), 0)

        seen = set()
        for entry in months:
            month = entry.get("month")
            rel_path = entry.get("path")
            self.assertRegex(month, r"^\d{4}-\d{2}$")
            self.assertEqual(rel_path, f"docs/journals/history/{month}.json")
            self.assertNotIn(month, seen)
            seen.add(month)

            month_path = root / rel_path
            self.assertTrue(month_path.exists(), f"{rel_path} should exist")
            rows = json.loads(month_path.read_text(encoding="utf-8"))
            self.assertIsInstance(rows, list)
            self.assertEqual(entry.get("count"), len(rows))
            for row in rows:
                if not isinstance(row, dict):
                    continue
                pdf_url = str(row.get("pdf_url") or "")
                self.assertFalse(
                    pdf_url.startswith(("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/")),
                    f"{rel_path} contains DOI landing page as pdf_url: {pdf_url}",
                )

        sorted_months = sorted(seen, reverse=True)
        self.assertEqual(index.get("latest"), sorted_months[0])

    def test_latest_journal_data_does_not_mark_doi_landing_pages_as_pdf(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        latest_path = root / "docs" / "journals" / "journal-papers.json"
        rows = json.loads(latest_path.read_text(encoding="utf-8"))

        self.assertIsInstance(rows, list)
        for row in rows:
            if not isinstance(row, dict):
                continue
            pdf_url = str(row.get("pdf_url") or "")
            is_doi_page = pdf_url.startswith(("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/"))
            self.assertFalse(is_doi_page, f"latest journal data contains DOI landing page as pdf_url: {pdf_url}")
            if row.get("open_pdf_status") == "open_pdf":
                self.assertTrue(pdf_url, f"open_pdf row must include a direct PDF URL: {row.get('doi') or row.get('id')}")


if __name__ == "__main__":
    unittest.main()
