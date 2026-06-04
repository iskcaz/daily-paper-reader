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
from urllib.parse import urlparse


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


def is_doi_landing_url(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    try:
        host = urlparse(text).netloc.lower()
    except Exception:
        return False
    return host in {"doi.org", "dx.doi.org", "www.doi.org"}


def is_usable_open_pdf_url(value: Any) -> bool:
    text = str(value or "").strip()
    if not text or is_doi_landing_url(text):
        return False
    try:
        parsed = urlparse(text)
    except Exception:
        return False
    return parsed.scheme.lower() in {"http", "https"}


def normalize_open_pdf_fields(row: dict[str, Any]) -> dict[str, Any]:
    pdf_url = str(row.get("pdf_url") or "").strip()
    if is_usable_open_pdf_url(pdf_url):
        row["open_pdf_status"] = "open_pdf"
        row["open_pdf_available"] = True
        if not str(row.get("open_pdf_source") or "").strip():
            row["open_pdf_source"] = "unknown"
        return row

    if pdf_url and not str(row.get("abs_url") or "").strip():
        row["abs_url"] = pdf_url
    row["pdf_url"] = None
    row["open_pdf_source"] = ""
    row["open_pdf_status"] = "no_open_pdf"
    row["open_pdf_available"] = False
    row["open_pdf_note"] = "No legal open PDF found; skip screenshots and figure extraction."
    return row


def merge_row(existing: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    normalize_open_pdf_fields(existing)
    normalize_open_pdf_fields(incoming)
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
    return normalize_open_pdf_fields(existing)


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
        merged.append(normalize_open_pdf_fields(dict(row)))
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
    rows = [
        normalize_open_pdf_fields(dict(row)) if isinstance(row, dict) else row
        for row in load_rows(input_file)
    ]

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
