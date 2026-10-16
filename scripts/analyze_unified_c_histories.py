"""Read retained C opportunity histories; no participant or simulator calls."""
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from scripts.analyze_inquiry_trajectories import public_events
from scripts.run_unified_matrices import folder

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "workstreams/flagship_tasks/reports/unified-matrices-20261016/process/C"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def execution_summary(events):
    """Keep requested doses separate from changes actually committed by the world."""
    output = []
    for batch in sorted({e["batch"] for e in events}):
        operations = [e for e in events if e["batch"] == batch]
        seeds = [e for e in operations if e["action"].get("operation") == "seed_crystals"]
        output.append(
            {
                "batch": batch,
                "operation_status_counts": dict(
                    Counter(e["transaction_status"] for e in operations)
                ),
                "seed_requested_g": sum(e["action"].get("seed_mass_g", 0) for e in seeds),
                "seed_committed_g": sum(
                    e["action"].get("seed_mass_g", 0)
                    for e in seeds
                    if e["transaction_status"] == "committed"
                ),
                "rejected_seed_cursors": [
                    e["cursor"] for e in seeds if e["transaction_status"] != "committed"
                ],
            }
        )
    return output


def extract():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    root = Path(binding["run_root"])
    design = read(root / "design.json")
    records = []
    for unit in sorted(design["schedule"], key=lambda u: (u["repeat"], u["id"])):
        if unit["system"] != "C":
            continue
        base = folder(root, unit, design)
        result = read(base / "result.json")
        source = Path(result["source_dir"]) if result.get("source_dir") else None
        notes = []
        events = []
        if source and source.exists():
            history = source / "notebook/experiment_documents/notebook_history"
            for p in sorted(history.glob("*.json")):
                note = read(p)
                notes.append({k: note[k] for k in ("revision", "text", "public_cursor")})
            trajectory = source / "trajectory.jsonl"
            if trajectory.exists():
                events = public_events(trajectory)
        stages = {}
        for stage in ("K1", "Q", "K2"):
            native = result.get("posttests", {}).get(stage, {})
            stages[stage] = native.get("payload")
        row = {
            "key": f"{unit['repeat']}/{unit['id']}",
            "unit": unit,
            "source_result": str(base / "result.json"),
            "status": result["status"],
            "notes": notes,
            "events": events,
            "stages": stages,
            "batches": result.get("source", {}).get("batches", []),
            "batch_actions_scope": "Native actions include rejected requests; check event status.",
            "execution_summary": execution_summary(events),
            "recommendation": result.get("recommendation"),
            "prediction_evaluation": result.get("prediction_evaluation"),
        }
        records.append(row)
        write(OUT / "sessions" / unit["repeat"] / f"{unit['id']}.json", row)
    counts = {
        "sessions": len(records),
        "notes": sum(len(r["notes"]) for r in records),
        "events": sum(len(r["events"]) for r in records),
        "research_sessions": sum(bool(r["events"]) for r in records),
        "stages": sum(v is not None for r in records for v in r["stages"].values()),
        "status": dict(Counter(r["status"] for r in records)),
        "interpretation": "Extraction only; semantic reading tracked separately.",
    }
    write(OUT / "extraction.json", counts)
    print(json.dumps(counts))


def rows():
    return [read(p) for p in sorted((OUT / "sessions").glob("repeat-*/*.json"))]


def seed_execution_report():
    research = [r for r in rows() if r["events"]]
    batches = [{"key": r["key"], **batch} for r in research for batch in r["execution_summary"]]
    changed = [r for r in batches if r["rejected_seed_cursors"]]
    result = {
        "scope": (
            "Mechanical comparison of requested and committed seed additions; "
            "not a count of scientific misunderstanding. No simulation or provider calls."
        ),
        "sessions": len(research),
        "batches": len(batches),
        "sessions_with_rejected_seed_requests": len({r["key"] for r in changed}),
        "batches_with_rejected_seed_requests": len(changed),
        "rejected_seed_requests": sum(len(r["rejected_seed_cursors"]) for r in changed),
        "frozen_cumulative_limit_g": 0.05,
        "source_commit": "d2b05e98",
        "source_files": [
            "src/chemworld/world/operations.py",
            "src/chemworld/operation_validator.py",
        ],
        "batches_with_differences": changed,
    }
    write(OUT / "operation-semantics/seed-execution.json", result)
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}))


def packet(key, part):
    for row in rows():
        if key not in row["key"]:
            continue
        print("\nSESSION", row["key"])
        if part == "notes":
            for n in row["notes"]:
                print(f"\nV{n['revision']} cursor={n['public_cursor']['event_count']}\n{n['text']}")
        elif part == "reports":
            for stage in ("K1", "K2"):
                print("\n", stage, json.dumps(row["stages"][stage], ensure_ascii=False))
        elif part == "q":
            print(json.dumps(row["stages"]["Q"], ensure_ascii=False))
        else:
            for b in row["batches"]:
                print(json.dumps(b, ensure_ascii=False))


def verify():
    source = {r["key"]: r for r in rows()}
    manual = read(OUT / "reading.json")
    seen = set()
    verified = 0
    for record in manual["records"]:
        key = record["key"]
        assert key not in seen, key
        seen.add(key)
        row = source[key]
        notes = {n["revision"]: n for n in row["notes"]}
        events = {e["cursor"]: e for e in row["events"]}
        for anchor in record.get("anchors", []):
            if "revision" in anchor:
                text = notes[anchor["revision"]]["text"]
            else:
                text = json.dumps(row["stages"][anchor["stage"]], ensure_ascii=False)
            assert anchor["quote"] and anchor["quote"] in text, (key, anchor)
            verified += 1
        for cursor in record.get("event_cursors", []):
            assert cursor in events, (key, cursor)
        assert sorted(record["notes_read"]) == sorted(notes), key
        assert sorted(record["stages_read"]) == sorted(row["stages"]), key
        assert record["batches_reviewed"] == len(row["batches"]), key
    result = {
        "reviewed_sessions": len(seen),
        "planned": len(source),
        "verified_quotes": verified,
        "missing": sorted(set(source) - seen),
        "reviewed_note_versions": sum(len(source[k]["notes"]) for k in seen),
        "scope": "Assistant interpretation; anchors verified, no independent human coding.",
    }
    write(OUT / "verification.json", result)
    lines = [
        "# 结晶研究机会对照过程精读",
        "",
        f"已完成 {len(seen)}/30 场精读，核对 {verified} 条原句。未读会话保留为待完成，"
        "不以自动提取代替语义阅读。",
        "",
        "本表逐场连接公开笔记、封存科学答卷和实际批次。研究组的动作由公开轨迹与批次"
        "操作顺序核对；无研究组没有实验历史。K2中的下一步实验均为未执行提议。",
        "",
    ]
    for record in sorted(manual["records"], key=lambda r: r["key"]):
        key = record["key"]
        lines += [
            f"## {key}",
            "",
            f"**{record['topic']}**",
            "",
            f"[完整公开记录](sessions/{key}.json)",
            "",
        ]
        for field, label in [
            ("initial_judgment", "起始判断"),
            ("test_and_observation", "操作与证据"),
            ("revision", "修订"),
            ("later_use", "后续使用"),
            ("boundary", "解释范围"),
            ("analysis", "分析"),
        ]:
            if record.get(field):
                lines += [f"**{label}。** {record[field]}", ""]
        for anchor in record.get("anchors", []):
            origin = f"笔记 v{anchor['revision']}" if "revision" in anchor else anchor["stage"]
            lines += [f"- {origin}：{anchor['quote']}"]
        lines.append("")
    (OUT / "READING.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps(result))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("extract", "packet", "verify", "seed-report"))
    p.add_argument("--key", default="")
    p.add_argument("--part", choices=("notes", "reports", "q", "batches"), default="notes")
    args = p.parse_args()
    if args.command == "extract":
        extract()
    elif args.command == "packet":
        packet(args.key, args.part)
    elif args.command == "seed-report":
        seed_execution_report()
    else:
        verify()


if __name__ == "__main__":
    main()
