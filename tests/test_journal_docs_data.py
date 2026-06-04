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

        sorted_months = sorted(seen, reverse=True)
        self.assertEqual(index.get("latest"), sorted_months[0])


if __name__ == "__main__":
    unittest.main()
