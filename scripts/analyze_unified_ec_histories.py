"""Read-only EC corpus and assistant-authored explanation-history review.

Mechanical checks establish quote and event provenance, never understanding,
causal mechanisms, or an abduction success label.
"""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "workstreams/flagship_tasks/reports/unified-matrices-20261016/process/EC"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def corpus():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    root = Path(binding["run_root"])
    design = read(root / "design.json")
    records = []
    for unit in design["schedule"]:
        if unit["system"] != "EC":
            continue
        key = f"{unit['repeat']}/{unit['id']}"
        folder = Path(design.get("retained_units", {}).get(key, root / key))
        result = read(folder / "result.json")
        source = Path(result["source_dir"])
        documents = source / "notebook/experiment_documents"
        notes = [read(p) for p in sorted((documents / "notebook_history").glob("*.json"))]
        ledger = documents / "environment_authoritative_ledger.jsonl"
        events = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
        public = source / "workspace/public/operation_history.jsonl"
        published = [json.loads(line) for line in public.read_text(encoding="utf-8").splitlines()]
        assert events == published[: len(events)], key
        events = published
        cursor = 0
        for note in notes:
            n = note["public_cursor"]["event_count"]
            assert cursor <= n <= len(events), key
            expected = events[n - 1]["event_id"] if n else None
            assert note["public_cursor"]["last_event_id"] == expected, key
            if note.get("reviewed_through"):
                assert note["reviewed_through"] in {e["event_id"] for e in events[:n]}, key
            cursor = n
        assert len(result["source"]["batches"]) == 12, key
        records.append(
            {
                "key": key,
                "slug": key.replace("/", "--"),
                "unit": unit,
                "result_path": str(folder / "result.json"),
                "source_dir": str(source),
                "notes": notes,
                "events": events,
                "result": result,
            }
        )
    assert len(records) == 90
    return records


def report_sections(text):
    parts = re.split(r"\n\s*\n", text)
    return [{"paragraph": i + 1, "text": part} for i, part in enumerate(parts) if part.strip()]


def compact_scientific_view(record):
    """Lossless prose, compact numerical display for actual semantic reading."""
    lines = [reading_view(record).split("ALL SOURCE BATCHES")[0]]
    fields = {
        "electrochemical_conversion": "X",
        "selective_product_yield": "Y",
        "electrochemical_selectivity": "Sel",
        "faradaic_efficiency": "FE",
        "transport_efficiency": "TE",
        "ohmic_efficiency": "OE",
        "energy_efficiency": "EE",
        "precipitation_signal": "precip",
        "score": "score",
    }
    previous_end = 0
    for batch in record["result"]["source"]["batches"]:
        lines.append(f"B{batch['lifecycle_index']} end={batch['end_step']}")
        for event in record["events"][previous_end : batch["end_step"]]:
            action = event["action"]
            if action.get("operation") in {"terminate", "reset"}:
                continue
            if action.get("operation") == "measure":
                estimates = event.get("processed_estimate") or {}
                values = " ".join(
                    f"{short}={estimates[k]:.4f}" for k, short in fields.items() if k in estimates
                )
                lines.append(f" {event['event_id']} {action['instrument']} {values}")
            else:
                lines.append(f" {event['event_id']} {json.dumps(action)}")
            if not event.get("ok", True):
                lines.append(f" FAILURE {event.get('error_message')}")
        values = batch["metrics"]
        lines.append(
            " final " + " ".join(f"{s}={values[k]:.4f}" for k, s in fields.items() if k in values)
        )
        previous_end = batch["end_step"]
    q = record["result"]["posttests"]["Q"]["payload"]
    lines.append("Q: estimates[lower80,upper80]")
    for query in q["predictions"]:
        values = []
        for field, short in fields.items():
            if field not in query:
                continue
            entry = query[field]
            values.append(f"{short}={entry['estimate']}[{entry['lower80']},{entry['upper80']}]")
        lines.append(query["query_id"] + " " + " ".join(values))
    lines += [q["rationale"], str(record["result"].get("recommendation"))]
    return "\n".join(lines)


def reading_view(record, full_reports=False):
    lines = [f"CASE {record['key']}"]
    previous = []
    for note in record["notes"]:
        lines.append(f"NOTE v{note['revision']} cursor={note['public_cursor']['event_count']}")
        current = note["text"].splitlines()
        lines.extend(
            difflib.unified_diff(previous, current, n=1, lineterm="") if previous else current
        )
        previous = current
    lines.append("ALL SOURCE BATCHES")
    for batch in record["result"]["source"]["batches"]:
        conditions = [
            a
            for a in batch["actions"]
            if a["operation"] in {"add_reagent", "add_solvent", "set_potential", "electrolyze"}
        ]
        measurements = [a for a in batch["actions"] if a["operation"] == "measure"]
        values = batch["metrics"]
        values = {
            k: round(values[k], 5)
            for k in [
                "selective_product_yield",
                "score",
                "faradaic_efficiency",
                "electrochemical_selectivity",
                "energy_efficiency",
            ]
        }
        lines.append(
            f"B{batch['lifecycle_index']} end={batch['end_step']} "
            f"{json.dumps(conditions)} measurements={json.dumps(measurements)} "
            f"outcome={json.dumps(values)}"
        )
    for stage in ("K1", "K2"):
        lines.append(stage)
        text = record["result"]["posttests"][stage]["payload"]["report"]
        for part in report_sections(text):
            body = part["text"] if full_reports else part["text"][:420]
            omitted = len(part["text"]) - len(body)
            lines.append(
                f"p{part['paragraph']} {body}"
                + (f" [remaining {omitted} chars]" if omitted else "")
            )
    payload = record["result"]["posttests"]["Q"]["payload"]
    lines.append("Q " + json.dumps(payload, ensure_ascii=False))
    lines.append(
        "RECOMMENDATION " + json.dumps(record["result"].get("recommendation"), ensure_ascii=False)
    )
    return "\n".join(lines)


def export(records):
    OUT.mkdir(parents=True, exist_ok=True)
    reviews_path = OUT / "reviews.json"
    reviews = read(reviews_path) if reviews_path.exists() else {}
    index, readings, checks = [], ["# EC逐场过程解释", ""], []
    for record in records:
        key, slug = record["key"], record["slug"]
        case = OUT / "cases" / f"{slug}.md"
        case.parent.mkdir(exist_ok=True)
        result = record["result"]
        lines = [
            f"# {key}",
            "",
            "既有科学公开材料；非provider内部推理。",
            "",
            f"来源：{record['source_dir']}",
            "",
            "## 同期笔记",
        ]
        for note in record["notes"]:
            lines += [
                "",
                f"### v{note['revision']} · 公开事件 {note['public_cursor']['event_count']}",
                "",
                note["text"],
            ]
        lines += ["", "## 实际批次及公开测量", ""]
        for batch in result["source"]["batches"]:
            lines += [
                f"### 批次 {batch['lifecycle_index']} · 终点事件 {batch['end_step']}",
                "",
                "```json",
                json.dumps(batch, ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        for stage in ("K1", "K2"):
            lines += [
                f"## {stage} 封存报告",
                "",
                result["posttests"][stage]["payload"]["report"],
                "",
            ]
        lines += [
            "## Q 封存预测",
            "",
            "```json",
            json.dumps(result["posttests"]["Q"]["payload"], ensure_ascii=False, indent=2),
            "```",
            "",
        ]
        case.write_text("\n".join(lines), encoding="utf-8")
        review = reviews.get(key)
        index.append(
            {
                "key": key,
                "case": f"cases/{slug}.md",
                "versions": len(record["notes"]),
                "events": len(record["events"]),
                "source_batches": 12,
                "review_depth": review.get("depth") if review else "packet_only_not_interpreted",
            }
        )
        if not review:
            continue
        note_map = {n["revision"]: n for n in record["notes"]}
        readings += [f"## [{key}](cases/{slug}.md)", "", review["analysis"], ""]
        for quote in review["quotes"]:
            if "stage" in quote:
                stage = quote["stage"]
                payload = result["posttests"][stage]["payload"]
                if stage == "Q":
                    body = payload["rationale"]
                else:
                    body = report_sections(payload["report"])[quote["paragraph"] - 1]["text"]
                assert quote["text"] in body, (key, quote)
                checks.append(
                    {
                        "key": key,
                        "stage": stage,
                        "paragraph": quote.get("paragraph"),
                        "quote_verified": True,
                        "temporal_scope": "sealed_post_source_not_prospective",
                    }
                )
                readings += [
                    f"> {stage} p{quote.get('paragraph', 'rationale')}: {quote['text']}",
                    "",
                ]
                continue
            note = note_map[quote["revision"]]
            assert quote["text"] in note["text"], (key, quote)
            cursor = note["public_cursor"]["event_count"]
            later = [b for b in result["source"]["batches"] if b["end_step"] > cursor]
            checks.append(
                {
                    "key": key,
                    "revision": quote["revision"],
                    "cursor": cursor,
                    "quote_verified": True,
                    "later_batches": [b["lifecycle_index"] for b in later],
                }
            )
            readings += [f"> v{quote['revision']}，公开事件{cursor}：{quote['text']}", ""]
        readings += ["实际深度：" + review["depth"], ""]
    write(
        OUT / "coverage.json",
        {
            "planned_sessions": 90,
            "loaded_sessions": len(records),
            "notebook_versions_loaded": sum(len(r["notes"]) for r in records),
            "public_events_loaded": sum(len(r["events"]) for r in records),
            "source_batches": sum(len(r["result"]["source"]["batches"]) for r in records),
            "assistant_reviewed_sessions": len(reviews),
            "mechanically_verified_quotes": len(checks),
            "sessions": index,
            "interpretation": (
                "Loading or quote verification is not semantic review; depth is explicit."
            ),
        },
    )
    write(OUT / "quote_checks.json", checks)
    (OUT / "READINGS.md").write_text("\n".join(readings), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--full-reports", action="store_true")
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()
    records = corpus()
    if args.export:
        export(records)
    else:
        for record in records[args.start : args.start + args.count]:
            print(reading_view(record, args.full_reports))


if __name__ == "__main__":
    main()
