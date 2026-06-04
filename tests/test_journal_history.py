import importlib.util
import pathlib
import unittest


def _load_module(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class JournalHistoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = pathlib.Path(__file__).resolve().parents[1]
        cls.mod = _load_module(
            "journal_history_mod",
            root / "src" / "maintain" / "journal_history.py",
        )

    def test_normalize_open_pdf_fields_rejects_doi_landing_page(self):
        row = {
            "doi": "10.1016/j.jhazmat.2026.142173",
            "abs_url": "https://doi.org/10.1016/j.jhazmat.2026.142173",
            "pdf_url": "https://doi.org/10.1016/j.jhazmat.2026.142173",
            "open_pdf_status": "open_pdf",
            "open_pdf_source": "openalex",
            "open_pdf_available": True,
        }

        normalized = self.mod.normalize_open_pdf_fields(row)

        self.assertIsNone(normalized["pdf_url"])
        self.assertEqual(normalized["open_pdf_status"], "no_open_pdf")
        self.assertEqual(normalized["open_pdf_source"], "")
        self.assertFalse(normalized["open_pdf_available"])

    def test_merge_rows_keeps_real_pdf_over_old_no_pdf_metadata(self):
        merged = self.mod.merge_rows(
            [
                {
                    "doi": "10.1000/test",
                    "title": "Old",
                    "pdf_url": "https://doi.org/10.1000/test",
                    "open_pdf_status": "open_pdf",
                    "open_pdf_available": True,
                }
            ],
            [
                {
                    "doi": "10.1000/test",
                    "pdf_url": "https://example.org/open.pdf",
                    "open_pdf_status": "open_pdf",
                    "open_pdf_source": "unpaywall",
                    "open_pdf_available": True,
                }
            ],
        )

        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["pdf_url"], "https://example.org/open.pdf")
        self.assertEqual(merged[0]["open_pdf_status"], "open_pdf")
        self.assertTrue(merged[0]["open_pdf_available"])
        self.assertEqual(merged[0]["open_pdf_source"], "unpaywall")


if __name__ == "__main__":
    unittest.main()
