#!/usr/bin/env python3
"""Generate smart-query candidates through a server-side GitHub Actions run."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def normalize_base_url(value: str) -> str:
    text = (value or "").strip().rstrip("/")
    if text.lower().endswith("/chat/completions"):
        text = re.sub(r"/chat/completions$", "", text, flags=re.IGNORECASE)
    return text.rstrip("/")


def build_endpoints(base_url: str) -> list[str]:
    base = normalize_base_url(base_url)
    if not base:
        return []
    if re.search(r"/v\d+$", base, flags=re.IGNORECASE):
        return [f"{base}/chat/completions", f"{base}/v1/chat/completions"]
    return [f"{base}/v1/chat/completions", f"{base}/chat/completions"]


def extract_json_text(data: dict[str, Any]) -> str:
    choices = data.get("choices") if isinstance(data, dict) else None
    if isinstance(choices, list) and choices:
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and isinstance(item.get("text"), str):
                    parts.append(item["text"])
            return "\n".join(parts).strip()
    if isinstance(data.get("output_text"), str):
        return str(data["output_text"]).strip()
    return json.dumps(data, ensure_ascii=False)


def load_json_lenient(text: str) -> dict[str, Any]:
    raw = (text or "").strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE).strip()
    raw = re.sub(r"\s*```$", "", raw).strip()
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            value = json.loads(match.group(0))
            return value if isinstance(value, dict) else {}
    return {}


def post_chat_completion(
    endpoint: str,
    *,
    api_key: str,
    model: str,
    prompt: str,
    use_response_format: bool,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a retrieval planning assistant and can only return valid JSON. "
                    "The response must be fully based on the current user input and must not "
                    "reference prior conversation history."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }
    if use_response_format:
        payload["response_format"] = {"type": "json_object"}

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as res:
        body = res.read().decode("utf-8", errors="replace")
    return json.loads(body)


def call_model(api_key: str, base_url: str, model: str, prompt: str) -> dict[str, Any]:
    endpoints = build_endpoints(base_url)
    if not endpoints:
        raise RuntimeError("missing model base url")

    last_error = ""
    for endpoint in endpoints:
        for use_response_format in (True, False):
            try:
                data = post_chat_completion(
                    endpoint,
                    api_key=api_key,
                    model=model,
                    prompt=prompt,
                    use_response_format=use_response_format,
                )
                parsed = load_json_lenient(extract_json_text(data))
                if parsed:
                    return parsed
                last_error = "model returned empty or non-json content"
            except urllib.error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                last_error = f"HTTP {exc.code}: {body[:1000]}"
                if exc.code == 400 and use_response_format:
                    continue
                if exc.code in {429, 500, 502, 503, 504}:
                    time.sleep(2)
                    continue
                break
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                break
    raise RuntimeError(last_error or "model request failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", default=os.getenv("DPR_SQ_REQUEST_ID", ""))
    parser.add_argument("--tag", default=os.getenv("DPR_SQ_TAG", ""))
    parser.add_argument("--description", default=os.getenv("DPR_SQ_DESCRIPTION", ""))
    parser.add_argument("--prompt", default=os.getenv("DPR_SQ_PROMPT", ""))
    parser.add_argument("--output-dir", default="docs/smart-query-results")
    args = parser.parse_args()
    if not args.request_id or not args.tag or not args.description or not args.prompt:
        raise RuntimeError("missing smart query request inputs")

    api_key = (
        os.getenv("DEEPSEEK_API_KEY")
        or os.getenv("SUMMARY_API_KEY")
        or os.getenv("Summarized_LLM_API_KEY")
        or ""
    ).strip()
    base_url = (
        os.getenv("DEEPSEEK_BASE_URL")
        or os.getenv("SUMMARY_BASE_URL")
        or os.getenv("Summarized_LLM_BASE_URL")
        or "https://jsyai.xinglian.work/v1"
    ).strip()
    model = (
        os.getenv("DEEPSEEK_MODEL")
        or os.getenv("SUMMARY_MODEL")
        or os.getenv("Summarized_LLM_MODEL")
        or "gpt-5.4"
    ).strip()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.request_id}.json"

    result: dict[str, Any] = {
        "ok": False,
        "request_id": args.request_id,
        "tag": args.tag,
        "description": args.description,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        if not api_key:
            raise RuntimeError("missing DEEPSEEK_API_KEY or SUMMARY_API_KEY GitHub secret")
        candidates = call_model(api_key, base_url, model, args.prompt)
        result.update(
            {
                "ok": True,
                "model": model,
                "base_url": base_url,
                "candidates": candidates,
            }
        )
    except Exception as exc:  # noqa: BLE001
        result["error"] = str(exc)

    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
