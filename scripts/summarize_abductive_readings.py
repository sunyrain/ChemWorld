"""Verify public quotation anchors and summarize the three manual reading shards.

This reads sealed exports only. It does not classify explanations or run research.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def anchors(value):
    if isinstance(value, dict):
        if "stage" in value and "quote" in value:
            yield value
        for item in value.values():
            yield from anchors(item)
    elif isinstance(value, list):
        for item in value:
            yield from anchors(item)


def verify_anchor(anchor, session):
    stage = anchor["stage"]
    quote = anchor["quote"]
    if not isinstance(quote, str) or not quote:
        return "empty_quote"
    if stage == "notebook":
        note = next(
            (v for v in session["versions"] if v["revision"] == anchor.get("revision")),
            None,
        )
        if note is None:
            return "unknown_revision"
        if quote not in note["text"]:
            return "quote_not_in_specified_revision"
        if anchor.get("public_cursor", note["public_cursor"]) != note["public_cursor"]:
            return "incorrect_public_cursor"
    elif stage in {"K1", "Q", "K2"}:
        payload = session.get("posttests", {}).get(stage, {}).get("payload")
        if not payload:
            return "unavailable_sealed_payload"
        if stage == "Q" and anchor.get("query_id"):
            payload = next(
                (q for q in payload["predictions"] if q["query_id"] == anchor["query_id"]),
                None,
            )
        if not any(quote in text for text in strings(payload)):
            return "quote_not_in_specified_stage_or_query"
    else:
        return "unknown_stage"
    return None


def summarize(report):
    expected = {
        (row["repeat"], row["id"])
        for path in (report / "sessions").glob("*/*.json")
        for row in [read(path)]
    }
    rows, issues, seen = [], [], set()
    for number in (1, 2, 3):
        shard = read(report / f"semantic_repeat{number:02d}.json")
        repeat = shard["repeat"]
        for record in shard["records"]:
            key = repeat, record["id"]
            if key in seen:
                raise ValueError(f"Duplicate manual session: {key}")
            seen.add(key)
            scope = record.get("review_scope", {})
            if not isinstance(scope, dict):
                issues.append({"session": key, "error": "review_scope_must_list_read_material"})
                continue
            if "notebook_revisions" not in scope:
                continue
            source = report / "sessions" / repeat / f"{record['id']}.json"
            if not source.exists():
                issues.append({"session": key, "error": "review_without_sealed_export"})
                continue
            session = read(source)
            available_notes = {v["revision"] for v in session["versions"]}
            available_stages = {
                s for s, value in session["posttests"].items() if value.get("payload")
            }
            read_notes, read_stages = set(scope["notebook_revisions"]), set(scope["sealed_stages"])
            if read_notes != available_notes or read_stages != available_stages:
                issues.append({"session": key, "error": "incomplete_or_unavailable_reading_scope"})
            quoted = list(anchors(record))
            for index, anchor in enumerate(quoted):
                error = verify_anchor(anchor, session)
                if error:
                    issues.append({"session": key, "anchor": index, "error": error})
            rows.append(
                {
                    "repeat": repeat,
                    "id": record["id"],
                    "source_status": session["status"],
                    "notebook_versions_read": len(read_notes),
                    "sealed_stages_read": sorted(read_stages),
                    "focal_histories": len(record["histories"]),
                    "quote_anchors": len(quoted),
                }
            )
    if len(seen) != 30:
        issues.append({"error": "manual_plan_does_not_contain_30_unique_sessions"})
    summary = {
        "planned_sessions": 30,
        "sealed_export_sessions": len(expected),
        "reviewed_sessions": len(rows),
        "notebook_versions_read": sum(r["notebook_versions_read"] for r in rows),
        "sealed_stages_read": dict(Counter(s for r in rows for s in r["sealed_stages_read"])),
        "focal_histories": sum(r["focal_histories"] for r in rows),
        "quote_anchors": sum(r["quote_anchors"] for r in rows),
        "issues": issues,
        "sessions": rows,
        "interpretation": (
            "Internal AI-assisted focal-history analysis. Quote and coverage checks verify "
            "provenance, not scientific truth or independent semantic agreement. "
            "No cohort-wide abduction success rate is estimated."
        ),
    }
    (report / "reading-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in summary.items() if k != "sessions"}, ensure_ascii=False))
    return not issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    return 0 if summarize(args.report) else 1


if __name__ == "__main__":
    raise SystemExit(main())
