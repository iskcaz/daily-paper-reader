#!/usr/bin/env python

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List
from urllib.parse import quote

import requests

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


SCRIPT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
WATCHLIST_FILE = os.path.join(ROOT_DIR, "journal_watchlist.yaml")
CROSSREF_API = "https://api.crossref.org"
OPENALEX_API = "https://api.openalex.org"
SEMANTIC_API = "https://api.semanticscholar.org/graph/v1"
UNPAYWALL_API = "https://api.unpaywall.org/v2"
DATE_TOKEN_RE = re.compile(r"^\d{8}$")
RANGE_TOKEN_RE = re.compile(r"^\d{8}-\d{8}$")
TAG_RE = re.compile(r"<[^>]+>")


def log(message: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {message}", flush=True)


def _norm(value: Any) -> str:
    return str(value or "").strip()


def _clean_html(value: Any) -> str:
    text = html.unescape(_norm(value))
    if not text:
        return ""
    text = TAG_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def _slugify(raw: str) -> str:
    text = _norm(raw).lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "item"


def normalize_doi(value: Any) -> str:
    text = _norm(value)
    if not text:
        return ""
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text, flags=re.I)
    text = re.sub(r"^doi:\s*", "", text, flags=re.I)
    return text.strip().lower()


def parse_crossref_date(raw: Any) -> str | None:
    if not isinstance(raw, dict):
        return None
    parts = raw.get("date-parts")
    if not isinstance(parts, list) or not parts:
        return None
    first = parts[0]
    if not isinstance(first, list) or not first:
        return None
    try:
        year = int(first[0])
        month = int(first[1]) if len(first) > 1 else 1
        day = int(first[2]) if len(first) > 2 else 1
        return datetime(year, month, day, tzinfo=timezone.utc).isoformat()
    except Exception:
        return None


def parse_date_arg(value: str) -> date | None:
    text = _norm(value)
    if not text:
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except Exception as exc:
        raise ValueError(f"invalid date, expected YYYY-MM-DD: {text}") from exc


def parse_month_arg(value: str) -> tuple[date, date] | None:
    text = _norm(value)
    if not text:
        return None
    try:
        start = datetime.strptime(text, "%Y-%m").date().replace(day=1)
    except Exception as exc:
        raise ValueError(f"invalid month, expected YYYY-MM: {text}") from exc
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1)
    else:
        next_month = start.replace(month=start.month + 1)
    return start, next_month - timedelta(days=1)


def resolve_fetch_date_window(*, days: int, from_date: str = "", until_date: str = "", month: str = "") -> tuple[date, date]:
    month_window = parse_month_arg(month)
    if month_window is not None:
        return month_window

    explicit_start = parse_date_arg(from_date)
    explicit_end = parse_date_arg(until_date)
    if explicit_start or explicit_end:
        end = explicit_end or datetime.now(timezone.utc).date()
        start = explicit_start or end
        if start > end:
            raise ValueError(f"from-date must be <= until-date: {start} > {end}")
        return start, end

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=max(int(days or 1), 1) - 1)
    return start, end


def parse_crossref_authors(raw: Any) -> List[str]:
    if not isinstance(raw, list):
        return []
    out: List[str] = []
    seen = set()
    for item in raw:
        if not isinstance(item, dict):
            continue
        literal = _norm(item.get("name"))
        given = _norm(item.get("given"))
        family = _norm(item.get("family"))
        name = literal or " ".join(part for part in (given, family) if part).strip()
        if not name or name in seen:
            continue
        seen.add(name)
        out.append(name)
    return out


def abstract_from_openalex_inverted_index(raw: Any) -> str:
    if not isinstance(raw, dict) or not raw:
        return ""
    words: List[tuple[int, str]] = []
    for token, positions in raw.items():
        if not isinstance(positions, list):
            continue
        for pos in positions:
            if isinstance(pos, int):
                words.append((pos, str(token)))
    if not words:
        return ""
    words.sort(key=lambda item: item[0])
    return " ".join(token for _, token in words).strip()


def build_headers(mailto: str = "") -> Dict[str, str]:
    contact = _norm(mailto or os.getenv("CROSSREF_MAILTO") or os.getenv("DPR_CONTACT_EMAIL"))
    ua = "daily-paper-reader/1.0"
    if contact:
        ua = f"{ua} (mailto:{contact})"
    return {"User-Agent": ua}


def load_watchlist(path: str = WATCHLIST_FILE) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required to load journal_watchlist.yaml")
    with open(path, "r", encoding="utf-8") as f:
        payload = yaml.safe_load(f) or {}
    if not isinstance(payload, dict):
        raise RuntimeError(f"watchlist must be a mapping: {path}")
    journals = payload.get("journals") or []
    if not isinstance(journals, list):
        raise RuntimeError("watchlist journals must be a list")
    return payload


def _keyword_hit(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    for keyword in keywords:
        token = _norm(keyword).lower()
        if token and token in lowered:
            return True
    return False


def parse_query_terms(query: str) -> List[str]:
    return [_norm(part) for part in re.split(r"[;,\n]+", _norm(query)) if _norm(part)]


def is_noise_article(paper: Dict[str, Any]) -> bool:
    title = _norm(paper.get("title")).lower()
    noise_prefixes = (
        "corrigendum",
        "correction",
        "erratum",
        "retraction",
        "expression of concern",
    )
    return title.startswith(noise_prefixes)


def normalize_crossref_item(
    item: Dict[str, Any],
    journal: Dict[str, Any],
    *,
    default_tags: Iterable[str] = (),
) -> Dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    if _norm(item.get("type")) and _norm(item.get("type")) != "journal-article":
        return None
    doi = normalize_doi(item.get("DOI"))
    title_values = item.get("title") if isinstance(item.get("title"), list) else []
    title = _clean_html(title_values[0] if title_values else item.get("title"))
    if not doi or not title:
        return None
    journal_name_values = item.get("container-title") if isinstance(item.get("container-title"), list) else []
    journal_name = _norm(journal.get("name")) or _norm(journal_name_values[0] if journal_name_values else "")
    short_label = _norm(journal.get("short_label") or journal.get("key") or journal_name)
    issns = item.get("ISSN") if isinstance(item.get("ISSN"), list) else []
    configured_issns = journal.get("issns") if isinstance(journal.get("issns"), list) else []
    source_tags: List[str] = []
    for raw in list(default_tags) + list(journal.get("tags") or []):
        tag = _norm(raw)
        if tag and tag not in source_tags:
            source_tags.append(tag)
    published = (
        parse_crossref_date(item.get("published-print"))
        or parse_crossref_date(item.get("published-online"))
        or parse_crossref_date(item.get("published"))
        or parse_crossref_date(item.get("issued"))
    )
    url = _norm(item.get("URL")) or (f"https://doi.org/{doi}" if doi else "")
    return {
        "id": f"journal-{_slugify(doi)}",
        "source": "journal",
        "source_detail": "crossref",
        "source_paper_id": doi,
        "doi": doi,
        "title": title,
        "abstract": _clean_html(item.get("abstract")),
        "authors": parse_crossref_authors(item.get("author")),
        "primary_category": "environmental-science",
        "categories": source_tags,
        "published": published,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "link": url,
        "abs_url": url,
        "pdf_url": None,
        "journal": journal_name,
        "journal_key": _norm(journal.get("key")),
        "journal_label": short_label,
        "journal_issn": issns or configured_issns,
        "source_weight": int(journal.get("source_weight") or 5),
        "open_pdf_status": "unknown",
        "open_pdf_source": "",
        "metadata_sources": ["crossref"],
        "tags": source_tags,
    }


def fetch_crossref_journal(
    journal: Dict[str, Any],
    *,
    from_date: str,
    until_date: str,
    rows: int,
    mailto: str = "",
    timeout: int = 60,
) -> List[Dict[str, Any]]:
    issns = journal.get("issns") if isinstance(journal.get("issns"), list) else []
    primary_issn = _norm(issns[0] if issns else "")
    if not primary_issn:
        return []
    params = {
        "filter": f"from-pub-date:{from_date},until-pub-date:{until_date},type:journal-article",
        "sort": "published",
        "order": "desc",
        "rows": str(max(int(rows or 1), 1)),
    }
    contact = _norm(mailto or os.getenv("CROSSREF_MAILTO") or os.getenv("DPR_CONTACT_EMAIL"))
    if contact:
        params["mailto"] = contact
    resp = requests.get(
        f"{CROSSREF_API}/journals/{quote(primary_issn)}/works",
        params=params,
        headers=build_headers(mailto),
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json() or {}
    message = data.get("message") if isinstance(data, dict) else {}
    items = message.get("items") if isinstance(message, dict) else []
    return items if isinstance(items, list) else []


def enrich_with_openalex(paper: Dict[str, Any], *, api_key: str = "", mailto: str = "", timeout: int = 30) -> None:
    doi = normalize_doi(paper.get("doi"))
    if not doi:
        return
    params: Dict[str, str] = {}
    key = _norm(api_key or os.getenv("OPENALEX_API_KEY"))
    contact = _norm(mailto or os.getenv("OPENALEX_MAILTO") or os.getenv("DPR_CONTACT_EMAIL"))
    if key:
        params["api_key"] = key
    if contact:
        params["mailto"] = contact
    resp = requests.get(
        f"{OPENALEX_API}/works/https://doi.org/{quote(doi, safe='')}",
        params=params,
        headers=build_headers(contact),
        timeout=timeout,
    )
    if resp.status_code == 404:
        return
    resp.raise_for_status()
    data = resp.json() or {}
    if not isinstance(data, dict):
        return
    paper.setdefault("metadata_sources", []).append("openalex")
    if not _norm(paper.get("abstract")):
        paper["abstract"] = abstract_from_openalex_inverted_index(data.get("abstract_inverted_index"))
    open_access = data.get("open_access") if isinstance(data.get("open_access"), dict) else {}
    if open_access:
        paper["is_oa"] = bool(open_access.get("is_oa"))
        paper["oa_status"] = _norm(open_access.get("oa_status"))
        oa_url = _norm(open_access.get("oa_url"))
        if oa_url and not _norm(paper.get("pdf_url")):
            paper["pdf_url"] = oa_url
            paper["open_pdf_status"] = "open_pdf"
            paper["open_pdf_source"] = "openalex"
    primary_location = data.get("primary_location") if isinstance(data.get("primary_location"), dict) else {}
    if primary_location:
        landing = _norm(primary_location.get("landing_page_url"))
        pdf = _norm(primary_location.get("pdf_url"))
        if landing and not _norm(paper.get("abs_url")):
            paper["abs_url"] = landing
        if pdf and not _norm(paper.get("pdf_url")):
            paper["pdf_url"] = pdf
            paper["open_pdf_status"] = "open_pdf"
            paper["open_pdf_source"] = "openalex"
    concepts = data.get("concepts") if isinstance(data.get("concepts"), list) else []
    concept_names = []
    for concept in concepts[:8]:
        if isinstance(concept, dict):
            name = _norm(concept.get("display_name"))
            if name:
                concept_names.append(name)
    if concept_names:
        paper["openalex_concepts"] = concept_names


def enrich_with_semantic_scholar_batch(
    papers: List[Dict[str, Any]],
    *,
    api_key: str = "",
    timeout: int = 60,
) -> None:
    doi_to_paper = {normalize_doi(p.get("doi")): p for p in papers if normalize_doi(p.get("doi"))}
    if not doi_to_paper:
        return
    headers = build_headers()
    key = _norm(api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY"))
    if key:
        headers["x-api-key"] = key
    fields = ",".join(
        [
            "title",
            "abstract",
            "citationCount",
            "influentialCitationCount",
            "openAccessPdf",
            "externalIds",
            "url",
            "year",
            "venue",
            "publicationDate",
            "fieldsOfStudy",
            "s2FieldsOfStudy",
        ]
    )
    dois = list(doi_to_paper.keys())
    for start in range(0, len(dois), 100):
        chunk = dois[start : start + 100]
        resp = requests.post(
            f"{SEMANTIC_API}/paper/batch",
            params={"fields": fields},
            json={"ids": [f"DOI:{doi}" for doi in chunk]},
            headers=headers,
            timeout=timeout,
        )
        resp.raise_for_status()
        results = resp.json() or []
        if not isinstance(results, list):
            continue
        for result in results:
            if not isinstance(result, dict):
                continue
            external = result.get("externalIds") if isinstance(result.get("externalIds"), dict) else {}
            doi = normalize_doi(external.get("DOI"))
            paper = doi_to_paper.get(doi)
            if paper is None:
                continue
            paper.setdefault("metadata_sources", []).append("semantic_scholar")
            if not _norm(paper.get("abstract")) and _norm(result.get("abstract")):
                paper["abstract"] = _norm(result.get("abstract"))
            paper["citation_count"] = result.get("citationCount")
            paper["influential_citation_count"] = result.get("influentialCitationCount")
            if _norm(result.get("url")) and not _norm(paper.get("abs_url")):
                paper["abs_url"] = _norm(result.get("url"))
            oa_pdf = result.get("openAccessPdf") if isinstance(result.get("openAccessPdf"), dict) else {}
            pdf_url = _norm(oa_pdf.get("url"))
            if pdf_url and not _norm(paper.get("pdf_url")):
                paper["pdf_url"] = pdf_url
                paper["open_pdf_status"] = "open_pdf"
                paper["open_pdf_source"] = "semantic_scholar"
            fields_of_study = result.get("fieldsOfStudy")
            if isinstance(fields_of_study, list):
                paper["semantic_fields_of_study"] = [_norm(x) for x in fields_of_study if _norm(x)]


def enrich_with_unpaywall(
    paper: Dict[str, Any],
    *,
    email: str = "",
    timeout: int = 30,
) -> None:
    doi = normalize_doi(paper.get("doi"))
    contact = _norm(email or os.getenv("UNPAYWALL_EMAIL") or os.getenv("DPR_CONTACT_EMAIL") or os.getenv("CROSSREF_MAILTO"))
    if not doi or not contact:
        return
    resp = requests.get(
        f"{UNPAYWALL_API}/{quote(doi, safe='')}",
        params={"email": contact},
        headers=build_headers(contact),
        timeout=timeout,
    )
    if resp.status_code == 404:
        return
    resp.raise_for_status()
    data = resp.json() or {}
    if not isinstance(data, dict):
        return
    paper.setdefault("metadata_sources", []).append("unpaywall")
    best = data.get("best_oa_location") if isinstance(data.get("best_oa_location"), dict) else {}
    pdf_url = _norm(best.get("url_for_pdf"))
    landing = _norm(best.get("url"))
    if pdf_url and not _norm(paper.get("pdf_url")):
        paper["pdf_url"] = pdf_url
        paper["open_pdf_status"] = "open_pdf"
        paper["open_pdf_source"] = "unpaywall"
    if landing and not _norm(paper.get("abs_url")):
        paper["abs_url"] = landing
    paper["is_oa"] = bool(data.get("is_oa", paper.get("is_oa", False)))
    paper["oa_status"] = _norm(data.get("oa_status") or paper.get("oa_status"))


def finalize_open_pdf_status(paper: Dict[str, Any]) -> None:
    if _norm(paper.get("pdf_url")):
        paper["open_pdf_status"] = "open_pdf"
        paper["open_pdf_available"] = True
        if not _norm(paper.get("open_pdf_source")):
            paper["open_pdf_source"] = "unknown"
    else:
        paper["open_pdf_status"] = "no_open_pdf"
        paper["open_pdf_available"] = False
        paper["open_pdf_note"] = "No legal open PDF found; skip screenshots and figure extraction."
        paper["link"] = _norm(paper.get("abs_url") or paper.get("link"))


def dedupe_by_doi(papers: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for paper in papers:
        doi = normalize_doi(paper.get("doi"))
        key = doi or _norm(paper.get("id"))
        if not key:
            continue
        existing = out.get(key)
        if existing is None:
            out[key] = paper
            continue
        for field, value in paper.items():
            if field == "metadata_sources":
                merged = list(dict.fromkeys(list(existing.get(field) or []) + list(value or [])))
                existing[field] = merged
            elif not existing.get(field) and value:
                existing[field] = value
        existing["source_weight"] = max(int(existing.get("source_weight") or 0), int(paper.get("source_weight") or 0))
    return list(out.values())


def fetch_journal_sources(
    *,
    days: int,
    output_file: str,
    watchlist_file: str = WATCHLIST_FILE,
    from_date: str = "",
    until_date: str = "",
    month: str = "",
    rows_per_journal: int = 25,
    query: str = "",
    enrich_openalex: bool = True,
    enrich_semantic: bool = True,
    enrich_unpaywall: bool = True,
    sleep_seconds: float = 0.12,
) -> List[Dict[str, Any]]:
    watchlist = load_watchlist(watchlist_file)
    journals = watchlist.get("journals") if isinstance(watchlist.get("journals"), list) else []
    default_tags = watchlist.get("default_tags") if isinstance(watchlist.get("default_tags"), list) else []
    query_terms = parse_query_terms(query)
    keywords = query_terms or [_norm(x) for x in (watchlist.get("keyword_filters") or []) if _norm(x)]
    start_date, end_date = resolve_fetch_date_window(
        days=days,
        from_date=from_date,
        until_date=until_date,
        month=month,
    )
    all_papers: List[Dict[str, Any]] = []
    for journal in journals:
        label = _norm(journal.get("short_label") or journal.get("name") or journal.get("key"))
        log(f"[Crossref] fetch {label}: {start_date.isoformat()} to {end_date.isoformat()}")
        try:
            items = fetch_crossref_journal(
                journal,
                from_date=start_date.isoformat(),
                until_date=end_date.isoformat(),
                rows=rows_per_journal,
            )
        except Exception as exc:
            log(f"[WARN] Crossref failed for {label}: {exc}")
            continue
        for item in items:
            paper = normalize_crossref_item(item, journal, default_tags=default_tags)
            if paper is None:
                continue
            if is_noise_article(paper):
                continue
            if keywords:
                haystack = f"{paper.get('title') or ''}\n{paper.get('abstract') or ''}"
                if not _keyword_hit(haystack, keywords):
                    continue
            all_papers.append(paper)
        time.sleep(max(float(sleep_seconds or 0), 0.0))

    papers = dedupe_by_doi(all_papers)
    if enrich_openalex:
        for paper in papers:
            try:
                enrich_with_openalex(paper)
            except Exception as exc:
                log(f"[WARN] OpenAlex enrich failed for {paper.get('doi')}: {exc}")
            time.sleep(max(float(sleep_seconds or 0), 0.0))
    if enrich_semantic:
        try:
            enrich_with_semantic_scholar_batch(papers)
        except Exception as exc:
            log(f"[WARN] Semantic Scholar enrich failed: {exc}")
    if enrich_unpaywall:
        for paper in papers:
            try:
                enrich_with_unpaywall(paper)
            except Exception as exc:
                log(f"[WARN] Unpaywall enrich failed for {paper.get('doi')}: {exc}")
            time.sleep(max(float(sleep_seconds or 0), 0.0))
    for paper in papers:
        finalize_open_pdf_status(paper)

    def _published_ts(paper: Dict[str, Any]) -> float:
        published = _norm(paper.get("published"))
        if not published:
            return 0.0
        try:
            return datetime.fromisoformat(published.replace("Z", "+00:00")).timestamp()
        except Exception:
            return 0.0

    def _sort_key(paper: Dict[str, Any]) -> tuple[int, float, str, str]:
        return (
            -int(paper.get("source_weight") or 0),
            -_published_ts(paper),
            _norm(paper.get("journal_label")),
            _norm(paper.get("title")),
        )

    papers.sort(key=_sort_key)
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    log(f"[JournalSources] wrote {len(papers)} papers: {output_file}")
    return papers


def get_run_date_token(end_date: datetime, days: int) -> str:
    token = _norm(os.getenv("DPR_RUN_DATE"))
    if DATE_TOKEN_RE.match(token) or RANGE_TOKEN_RE.match(token):
        return token
    if days > 1:
        start = (end_date - timedelta(days=days - 1)).date()
        return f"{start:%Y%m%d}-{end_date.date():%Y%m%d}"
    return end_date.strftime("%Y%m%d")


def get_output_token(*, days: int, from_date: str = "", until_date: str = "", month: str = "") -> str:
    if _norm(month):
        return _norm(month).replace("-", "")
    start_date, end_date = resolve_fetch_date_window(
        days=days,
        from_date=from_date,
        until_date=until_date,
        month=month,
    )
    if start_date != end_date:
        return f"{start_date:%Y%m%d}-{end_date:%Y%m%d}"
    return f"{end_date:%Y%m%d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch environmental journal papers from Crossref and enrich metadata.")
    parser.add_argument("--days", type=int, default=9)
    parser.add_argument("--month", type=str, default="", help="按整月抓取，例如 2025-06。优先级高于 --days。")
    parser.add_argument("--from-date", type=str, default="", help="开始日期，格式 YYYY-MM-DD。")
    parser.add_argument("--until-date", type=str, default="", help="结束日期，格式 YYYY-MM-DD。")
    parser.add_argument("--rows-per-journal", type=int, default=25)
    parser.add_argument("--watchlist", type=str, default=WATCHLIST_FILE)
    parser.add_argument("--output", type=str, default="")
    parser.add_argument("--query", type=str, default="")
    parser.add_argument("--skip-openalex", action="store_true")
    parser.add_argument("--skip-semantic-scholar", action="store_true")
    parser.add_argument("--skip-unpaywall", action="store_true")
    parser.add_argument("--sleep", type=float, default=0.12)
    args = parser.parse_args()

    days = max(int(args.days or 1), 1)
    output = _norm(args.output)
    if not output:
        token = get_output_token(
            days=days,
            from_date=args.from_date,
            until_date=args.until_date,
            month=args.month,
        )
        output = os.path.join(ROOT_DIR, "archive", token, "raw", f"journal_papers_{token}.json")
    elif not os.path.isabs(output):
        output = os.path.abspath(os.path.join(ROOT_DIR, output))

    fetch_journal_sources(
        days=days,
        output_file=output,
        watchlist_file=args.watchlist,
        from_date=args.from_date,
        until_date=args.until_date,
        month=args.month,
        rows_per_journal=args.rows_per_journal,
        query=args.query,
        enrich_openalex=not args.skip_openalex,
        enrich_semantic=not args.skip_semantic_scholar,
        enrich_unpaywall=not args.skip_unpaywall,
        sleep_seconds=args.sleep,
    )


if __name__ == "__main__":
    main()
