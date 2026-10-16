"""Extract PA/P public histories and verify separately written close readings.

This is a read-only consumer of retained W2-267 evidence.  Loading a record is
not semantic reading, and neither text matches nor notebook length is scored
as scientific understanding.  Provider rollouts and private reasoning are not
read.  Public notebook revisions, the public laboratory ledger, sealed public
answers and native evaluator readouts are the only evidence exported.
"""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import difflib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "workstreams/flagship_tasks/reports/unified-matrices-20261016/process/PA_P"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug(unit):
    return f"{unit['repeat']}__{unit['id']}"


def extract(output):
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    run_root = Path(binding["run_root"])
    design = read(run_root / "design.json")
    units = [u for u in design["schedule"] if u["system"] in ("PA", "P")]
    counts = Counter()
    index = []
    for number, unit in enumerate(units, 1):
        key = f"{unit['repeat']}/{unit['id']}"
        folder = Path(design.get("retained_units", {}).get(key, run_root / key))
        result = read(folder / "result.json")
        source = Path(result.get("source_dir") or result["participant"])
        if not (source / "notebook").is_dir():
            source /= "source"
        note_dir = source / "notebook/experiment_documents/notebook_history"
        notes = [read(p) for p in sorted(note_dir.glob("*.json"))]
        ledger = source / "notebook/experiment_documents/environment_authoritative_ledger.jsonl"
        events = []
        for line in ledger.read_text(encoding="utf-8").splitlines():
            raw = json.loads(line)
            events.append(
                {
                    k: raw.get(k)
                    for k in (
                        "event_id",
                        "action",
                        "observation",
                        "observed_keys",
                        "ok",
                        "error_message",
                        "transaction_status",
                        "lifecycle_experiment_index",
                        "batch_id",
                        "batch_discarded",
                        "experiment_ended",
                        "experiment_completed",
                        "completed_ordinal",
                        "completed_experiment_count",
                        "closed_batch_count",
                        "campaign_ended",
                        "campaign_terminal_reason",
                        "budget_exhausted",
                        "sample_consumed",
                        "constraint_flags",
                    )
                }
            )
        public_prompt = read(source / "source-prompt.txt")
        material = read(source / "workspace/reference/material_information.json")
        stages = {
            name: {
                "payload": result.get("posttests", {}).get(name, {}).get("payload"),
                "failure": result.get("posttests", {}).get(name, {}).get("failure"),
            }
            for name in ("K1", "Q", "K2")
        }
        retest = result.get("recommendation_retest") or {}
        item = {
            "key": key,
            "unit": unit,
            "status": read(folder / "status.json")["status"],
            "source_path": str(source),
            "result_path": str(folder / "result.json"),
            "material_information": material,
            "initial_resources": public_prompt.get("initial_public_state", {}).get(
                "campaign_resources", {}
            ),
            "public_task": {
                k: public_prompt.get("task", {}).get(k)
                for k in (
                    "description",
                    "research_goal",
                    "prediction_metrics",
                    "constraints",
                )
            },
            "notes": notes,
            "events": events,
            "source_summary": {
                k: result["source"].get(k)
                for k in (
                    "operations",
                    "completed_batches",
                    "failure",
                    "exact_replay",
                    "resources",
                )
            },
            "source_batches": result["source"].get("batches", []),
            "posttests": stages,
            "prediction_evaluation": result.get("prediction_evaluation"),
            "recommendation": result.get("recommendation"),
            "recommendation_retest": {
                k: retest.get(k) for k in ("passed", "batches", "failure", "validation_checks")
            },
            "semantic_reading_status": "pending; extraction does not imply close reading",
        }
        write(output / "sessions" / f"{slug(unit)}.json", item)
        index.append(
            {
                "key": key,
                "file": f"sessions/{slug(unit)}.json",
                "system": unit["system"],
                "notes": len(notes),
                "events": len(events),
                "status": item["status"],
            }
        )
        counts[unit["system"] + "_sessions_extracted"] += 1
        counts[unit["system"] + "_notebook_versions_extracted"] += len(notes)
        counts[unit["system"] + "_public_events_extracted"] += len(events)
        print(
            f"extract {number}/{len(units)} {key} notes={len(notes)} events={len(events)}",
            flush=True,
        )
    write(
        output / "index.json",
        {"binding": "work_ii.w2_267_unified_matrices", "counts": counts, "sessions": index},
    )


def packet(output, query, part, delta):
    matches = [x for x in read(output / "index.json")["sessions"] if query in x["key"]]
    for match in matches:
        item = read(output / match["file"])
        print(f"\n=== {item['key']} ({item['status']}) ===")
        if part in ("all", "notes"):
            previous = ""
            for note in item["notes"]:
                print(f"\nREVISION {note['revision']} cursor={note['public_cursor']}")
                text = note["text"]
                if delta and previous:
                    print(
                        "\n".join(
                            difflib.unified_diff(previous.splitlines(), text.splitlines(), n=1)
                        )
                    )
                else:
                    print(text)
                previous = text
        if part in ("all", "events"):
            for event in item["events"]:
                action = event["action"] or {}
                line = f"{event['event_id']} {json.dumps(action, ensure_ascii=False)}"
                if action.get("operation") == "measure":
                    obs = {
                        k: v
                        for k, v in (event["observation"] or {}).items()
                        if k not in ("cost", "safety_risk")
                    }
                    line += " => " + json.dumps(obs, ensure_ascii=False)
                if event["error_message"]:
                    line += " REJECTED: " + event["error_message"]
                print(line)
        if part in ("all", "material"):
            print(
                "MATERIAL", json.dumps(item["material_information"], ensure_ascii=False, indent=2)
            )
        for stage in ("K1", "Q", "K2"):
            if part in ("all", stage):
                print(stage, json.dumps(item["posttests"][stage], ensure_ascii=False, indent=2))
        if part == "metrics":
            print(json.dumps(item["prediction_evaluation"], ensure_ascii=False, indent=2))
        if part == "batches":
            # Exact action-list diffs, not an inferred scientific summary. Every
            # public observation and rejection is printed separately below.
            previous = []
            batch = []
            groups = []
            for event in item["events"]:
                batch.append(event)
                if event.get("batch_discarded") or (
                    event["action"].get("instrument") == "final_assay"
                    and event.get("ok")
                    and event.get("completed_ordinal")
                ):
                    groups.append(batch)
                    batch = []
            if batch:
                groups.append(batch)
            for number, batch in enumerate(groups, 1):
                print(f"BATCH {number} events={batch[0]['event_id']}..{batch[-1]['event_id']}")
                actions = [
                    json.dumps(e["action"], ensure_ascii=False, sort_keys=True) for e in batch
                ]
                if previous:
                    changes = list(difflib.unified_diff(previous, actions, n=0))
                    print("\n".join(changes) if changes else "Actions identical to previous batch.")
                else:
                    print("\n".join(actions))
                previous = actions
                for event in batch:
                    if event["action"].get("operation") == "measure":
                        print(
                            event["event_id"],
                            event["action"].get("instrument"),
                            json.dumps(event["observation"], ensure_ascii=False),
                        )
                    if event.get("error_message"):
                        print(event["event_id"], "REJECTED", event["error_message"])


def verify(output):
    index = read(output / "index.json")
    items = {s["key"]: read(output / s["file"]) for s in index["sessions"]}
    paths = sorted((output / "readings").glob("*.json"))
    counts = Counter()
    audit = []
    for path in paths:
        reading = read(path)
        item = items[reading["key"]]
        quotes = []
        event_ids = {e["event_id"] for e in item["events"]}
        event_positions = {e["event_id"]: i for i, e in enumerate(item["events"], 1)}
        for anchor in reading["anchors"]:
            if "revision" in anchor:
                note = next(n for n in item["notes"] if n["revision"] == anchor["revision"])
                text = note["text"]
                cursor = note["public_cursor"]
            else:
                text = json.dumps(item["posttests"][anchor["stage"]]["payload"], ensure_ascii=False)
                # Reports are plain prose; use original payload rather than escaped JSON.
                payload = item["posttests"][anchor["stage"]]["payload"]
                if isinstance(payload, dict) and isinstance(payload.get("report"), str):
                    text = payload["report"]
                if isinstance(payload, dict) and "field" in anchor:
                    text = payload[anchor["field"]]
                cursor = None
            assert anchor["quote"] in text, (reading["key"], anchor)
            refs = anchor.get("events", [])
            assert all(e in event_ids for e in refs), (reading["key"], refs)
            quotes.append(
                {
                    "quote_verified": True,
                    "events_verified": refs,
                    "cursor": cursor,
                    "event_timing": [
                        {
                            "event": event,
                            "public_position": event_positions[event],
                            "relative_to_note": (
                                "sealed_stage_after_source"
                                if cursor is None
                                else "available_at_note"
                                if event_positions[event] <= cursor["event_count"]
                                else "later_action_or_evidence"
                            ),
                        }
                        for event in refs
                    ],
                }
            )
        for e in reading.get("event_anchors", []):
            assert e in event_ids, (reading["key"], e)
        assert reading["read_coverage"]["notebook_revisions"] == len(item["notes"])
        assert reading["read_coverage"]["public_events"] == len(item["events"])
        assert set(reading["read_coverage"]["sealed_stages"]) == {"K1", "Q", "K2"}
        counts[item["unit"]["system"] + "_sessions_close_read"] += 1
        counts["notebook_versions_close_read"] += len(item["notes"])
        counts["exact_quotes_verified"] += len(quotes)
        audit.append(
            {
                "key": reading["key"],
                "quote_verification": quotes,
                "event_anchors": reading.get("event_anchors", []),
            }
        )
        sections = [
            f"# {reading['title']}",
            "",
            f"`{reading['key']}`",
            "",
            "阅读覆盖：" + reading["read_coverage"]["method"],
            "",
            f"[完整公开记录](../sessions/{path.stem}.json)",
            "",
        ]
        for field, title in (
            ("question_and_prior", "问题与先验"),
            ("expectation_and_test", "预期与实验"),
            ("evidence", "实际证据"),
            ("revision", "修订"),
            ("subsequent_use", "后续采用"),
            ("unresolved_and_limits", "未解决问题及解释限制"),
        ):
            sections.extend([f"## {title}", "", reading[field], ""])
        sections.extend(["## 已核验引文与事件锚点", ""])
        for anchor, checked in zip(reading["anchors"], quotes, strict=True):
            where = (
                f"v{anchor['revision']} / cursor {checked['cursor']}"
                if "revision" in anchor
                else anchor["stage"]
            )
            sections.extend([where, "", "> " + anchor["quote"], ""])
            if anchor.get("events"):
                sections.extend(["事件：" + ", ".join(anchor["events"]), ""])
        path.with_suffix(".md").write_text("\n".join(sections), encoding="utf-8")
    write(
        output / "reading-audit.json",
        {
            "counts": counts,
            "readings": audit,
            "limits": (
                "Exact text and event existence checks do not certify semantic correctness, "
                "causal attribution or independent coding."
            ),
        },
    )
    write(
        output / "reading-progress.json",
        {
            "extracted": index["counts"],
            "close_read": counts,
            "completed_keys": [a["key"] for a in audit],
            "pending_keys": sorted(set(items) - {a["key"] for a in audit}),
        },
    )
    print(json.dumps(counts, ensure_ascii=False, indent=2))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("extract", "packet", "verify"))
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--query", default="")
    parser.add_argument(
        "--part",
        choices=("all", "notes", "events", "batches", "material", "K1", "Q", "K2", "metrics"),
        default="all",
    )
    parser.add_argument("--delta", action="store_true")
    args = parser.parse_args()
    if args.mode == "extract":
        extract(args.output)
    elif args.mode == "packet":
        packet(args.output, args.query, args.part, args.delta)
    else:
        verify(args.output)


if __name__ == "__main__":
    main()
