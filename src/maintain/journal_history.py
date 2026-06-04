#!/usr/bin/env python
"""Maintain website-visible journal source history files."""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_LATEST_PATH = ROOT_DIR / "docs" / "journals" / "journal-papers.json"
DEFAULT_HISTORY_DIR = ROOT_DIR / "docs" / "journals" / "history"


def parse_month(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).strftime("%Y-%m")
    except ValueError:
        return text[:7] if len(text) >= 7 and text[4] == "-" else ""


def row_key(row: Any) -> str:
    if not isinstance(row, dict):
        return ""
    for field in ("doi", "id", "source_paper_id", "title"):
        value = str(row.get(field) or "").strip().lower()
        if value:
            return f"{field}:{value}"
    return ""


def merge_row(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    for field, value in incoming.items():
        if field == "metadata_sources" and isinstance(value, list):
            old = existing.get(field) if isinstance(existing.get(field), list) else []
            existing[field] = list(dict.fromkeys([*old, *value]))
            continue
        if field == "categories" and isinstance(value, list):
            old = existing.get(field) if isinstance(existing.get(field), list) else []
            existing[field] = list(dict.fromkeys([*old, *value]))
            continue
        if field == "source_weight":
            try:
                existing[field] = max(int(existing.get(field) or 0), int(value or 0))
            except Exception:
                if not existing.get(field) and value not in (None, "", []):
                    existing[field] = value
            continue
        if field in {"pdf_url", "open_pdf_url", "open_pdf_source"} and value:
            existing[field] = value
            continue
        if field == "open_pdf_available" and value is True:
            existing[field] = True
            continue
        if field == "open_pdf_status" and value and value != "no_open_pdf":
            existing[field] = value
            continue
        if not existing.get(field) and value not in (None, "", []):
            existing[field] = value
    return existing


def merge_rows(existing_rows: list[Any], incoming_rows: list[Any]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    key_to_index: dict[str, int] = {}
    for row in list(existing_rows or []) + list(incoming_rows or []):
        if not isinstance(row, dict):
            continue
        key = row_key(row)
        if key and key in key_to_index:
            merge_row(merged[key_to_index[key]], row)
            continue
        if key:
            key_to_index[key] = len(merged)
        merged.append(dict(row))
    return merged


def load_rows(path: Path) -> list[Any]:
    rows = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    if not isinstance(rows, list):
        raise ValueError(f"{path} must contain a JSON array")
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_journal_history(
    *,
    input_path: str | os.PathLike[str],
    latest_path: str | os.PathLike[str] = DEFAULT_LATEST_PATH,
    history_dir: str | os.PathLike[str] = DEFAULT_HISTORY_DIR,
    fallback_month: str = "",
) -> dict[str, Any]:
    input_file = Path(input_path)
    latest_file = Path(latest_path)
    history_path = Path(history_dir)
    rows = load_rows(input_file)

    write_json(latest_file, rows)
    history_path.mkdir(parents=True, exist_ok=True)

    safe_fallback_month = parse_month(fallback_month) or datetime.now(timezone.utc).strftime("%Y-%m")
    grouped: dict[str, list[Any]] = defaultdict(list)
    for row in rows:
        month = parse_month(row.get("published") if isinstance(row, dict) else "") or safe_fallback_month
        grouped[month].append(row)
    if not grouped:
        grouped[safe_fallback_month] = []

    updated_months: list[str] = []
    for month, month_rows in sorted(grouped.items()):
        month_path = history_path / f"{month}.json"
        try:
            existing_rows = load_rows(month_path)
        except Exception as exc:
            print(f"[WARN] journal history load failed, rewriting {month_path}: {exc}", flush=True)
            existing_rows = []
        merged = merge_rows(existing_rows, month_rows)
        write_json(month_path, merged)
        updated_months.append(month)

    months = []
    for path in sorted(history_path.glob("????-??.json"), reverse=True):
        try:
            month_rows = load_rows(path)
        except Exception:
            month_rows = []
        months.append(
            {
                "month": path.stem,
                "path": f"docs/journals/history/{path.name}",
                "count": len(month_rows),
            }
        )

    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "latest": months[0]["month"] if months else "",
        "months": months,
    }
    write_json(history_path / "index.json", index)
    return {
        "latest_path": str(latest_file),
        "history_dir": str(history_path),
        "row_count": len(rows),
        "updated_months": updated_months,
        "month_count": len(months),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Update docs/journals history from a journal paper JSON file.")
    parser.add_argument("--input", required=True, help="JSON array produced by fetch_journal_sources.py")
    parser.add_argument("--latest-output", default=str(DEFAULT_LATEST_PATH))
    parser.add_argument("--history-dir", default=str(DEFAULT_HISTORY_DIR))
    parser.add_argument("--fallback-month", default="")
    args = parser.parse_args()

    result = update_journal_history(
        input_path=args.input,
        latest_path=args.latest_output,
        history_dir=args.history_dir,
        fallback_month=args.fallback_month,
    )
    print(
        "journal history updated: "
        f"rows={result['row_count']} months={result['month_count']} "
        f"updated={','.join(result['updated_months'])}",
        flush=True,
    )


if __name__ == "__main__":
    main()
