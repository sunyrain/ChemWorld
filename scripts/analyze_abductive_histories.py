"""Index retained public notes and verify analyst-coded proposition histories.

No simulator/provider calls. Text extraction and analyst interpretation are
separate; source paragraphs are never automatically counted as abductions.
"""

# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
OUTPUT = REPORTS / "abductive-completion-20261016/histories"
COHORTS = {
    "EQ_process": ("inquiry-trajectories-20261014", "EQ-*.json", 45),
    "C_corrected": ("c-recovery-aligned-20261014", "C-*.json", 45),
    "EQ_opportunity": ("inquiry-completion-20261015", "EQ-*-Research.json", 15),
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sessions():
    current = read(ROOT / "configs/current.json")["work_ii"]
    assert current["w2_258_manuscript"]["evidence_binding"] == "work_ii.w2_257_inquiry_completion"
    binding = current["w2_257_inquiry_completion"]
    assert binding["corrected_c_semantics"].startswith(
        "workstreams/flagship_tasks/reports/c-recovery-aligned-20261014/"
    )
    results = []
    for cohort, (folder, pattern, expected) in COHORTS.items():
        paths = sorted((REPORTS / folder / "sessions").glob(f"repeat-*/{pattern}"))
        if len(paths) != expected:
            raise ValueError(f"Coverage mismatch: {cohort}: {len(paths)}/{expected}")
        for path in paths:
            source = read(path)
            notes = []
            for version in source.get("versions", source.get("notebook_versions", [])):
                cursor = version["public_cursor"]
                notes.append(
                    {
                        "revision": version["revision"],
                        "cursor": cursor["event_count"] if isinstance(cursor, dict) else cursor,
                        "text": version["text"],
                    }
                )
            events = source.get("events", source.get("public_events", []))
            paragraphs = []
            for note in notes:
                heading = ""
                for i, paragraph in enumerate(re.split(r"\n\s*\n", note["text"]), 1):
                    if paragraph.strip().startswith("#"):
                        heading = paragraph.splitlines()[0].strip()
                    paragraphs.append(
                        {
                            "paragraph_id": f"v{note['revision']}:p{i}",
                            "revision": note["revision"],
                            "cursor": note["cursor"],
                            "heading": heading,
                            "quote": paragraph.strip(),
                            "candidate_only": True,
                        }
                    )
            results.append(
                {
                    "key": f"{cohort}/{source['repeat']}/{source['id']}",
                    "cohort": cohort,
                    "repeat": source["repeat"],
                    "id": source["id"],
                    "status": source["status"],
                    "failure": source.get("failure"),
                    "source": path.relative_to(ROOT).as_posix(),
                    "notes": notes,
                    "events": events,
                    "paragraphs": paragraphs,
                }
            )
    return results


def packet(rows, cohort, repeat, case=None):
    sys.stdout.reconfigure(encoding="utf-8")
    for row in rows:
        if row["cohort"] != cohort or row["repeat"] != repeat:
            continue
        if case and case not in row["id"]:
            continue
        print(f"\n=== {row['key']} [{row['status']}] ===")
        for note in row["notes"]:
            print(f"\nVERSION {note['revision']} cursor={note['cursor']}\n{note['text']}")


def is_research(event):
    return event["transaction_status"] == "committed" and event["action"]["operation"] not in (
        "measure",
        "terminate",
    )


def assay(event):
    return (
        event["transaction_status"] == "committed"
        and event["action"].get("instrument") == "final_assay"
    )


def batch_summary(row):
    grouped = defaultdict(list)
    for event in row["events"]:
        grouped[event["batch"]].append(event)
    batches = []
    for batch, events in sorted(grouped.items()):
        executed = [e for e in events if e["transaction_status"] == "committed"]
        seeds = [e for e in events if e["action"]["operation"] == "seed_crystals"]
        batches.append(
            {
                "batch": batch,
                "cursor_range": [events[0]["cursor"], events[-1]["cursor"]],
                "final_assays": [
                    {"cursor": e["cursor"], "observations": e["observations"]}
                    for e in executed
                    if assay(e)
                ],
                "committed_seed_g": sum(
                    e["action"].get("seed_mass_g", 0)
                    for e in seeds
                    if e["transaction_status"] == "committed"
                ),
                "rejected_seed_attempts": sum(
                    e["transaction_status"] != "committed" for e in seeds
                ),
                "treatments": [
                    {"cursor": e["cursor"], **e["action"]}
                    for e in executed
                    if e["action"]["operation"] not in ("terminate", "create_container")
                ],
                "rejected_actions": [
                    {
                        "cursor": e["cursor"],
                        "transaction_status": e["transaction_status"],
                        **e["action"],
                    }
                    for e in events
                    if e["transaction_status"] != "committed"
                ],
            }
        )
    return batches


def seed_execution_checks(rows):
    """Quantify actual doses in four manually identified public-note comparisons."""
    selected = {
        "C_corrected/repeat-02/C-W02-Aligned": (7, 9, 10, 11),
        "C_corrected/repeat-02/C-W03-Aligned": (10,),
        "C_corrected/repeat-03/C-W02-Aligned": (7, 12),
        "C_corrected/repeat-03/C-W03-Aligned": (2, 8),
    }
    results = []
    for row in rows:
        if row["key"] not in selected:
            continue
        for batch in batch_summary(row):
            if batch["batch"] not in selected[row["key"]]:
                continue
            results.append(
                {
                    "key": row["key"],
                    "source": row["source"],
                    "batch": batch["batch"],
                    "committed_seed_g": batch["committed_seed_g"],
                    "rejected_seed_attempts": batch["rejected_seed_attempts"],
                    "seed_actions": [
                        {
                            "cursor": e["cursor"],
                            "status": e["transaction_status"],
                            "seed_mass_g": e["action"].get("seed_mass_g"),
                        }
                        for e in row["events"]
                        if e["batch"] == batch["batch"]
                        and e["action"]["operation"] == "seed_crystals"
                    ],
                }
            )
    return {
        "scope": "Selected comparisons, not an estimate of misdescription prevalence.",
        "cases": results,
    }


def verify_coding(rows):
    source = {row["key"]: row for row in rows}
    results = []
    seen = set()
    for path in sorted(OUTPUT.glob("*_manual.json")):
        coding = read(path)
        for record in coding["records"]:
            key = record["key"]
            if key not in source or key in seen:
                raise ValueError(f"Unknown or duplicate session: {key}")
            seen.add(key)
            row = source[key]
            versions = {note["revision"]: note for note in row["notes"]}
            histories = []
            for number, history in enumerate(record["histories"], 1):
                if history["kind"] not in (
                    "explanatory_candidate",
                    "empirical_relation",
                    "operational_expectation",
                ):
                    raise ValueError(f"Invalid kind: {key}: {history['kind']}")
                anchors = []
                for anchor in history["anchors"]:
                    version = versions[anchor["revision"]]
                    if not anchor["contains"] or anchor["contains"] not in version["text"]:
                        raise ValueError(f"Unverified quotation: {key}: {anchor}")
                    paragraph = next(
                        (
                            p
                            for p in row["paragraphs"]
                            if p["revision"] == anchor["revision"]
                            and anchor["contains"] in p["quote"]
                        ),
                        None,
                    )
                    if paragraph is None:
                        raise ValueError(f"Anchor spans paragraphs: {key}: {anchor}")
                    following = [e for e in row["events"] if e["cursor"] > version["cursor"]]
                    anchors.append(
                        {
                            **anchor,
                            "paragraph_id": paragraph["paragraph_id"],
                            "public_cursor": version["cursor"],
                            "context_quote": paragraph["quote"],
                            "subsequent_committed_research_actions": sum(
                                map(is_research, following)
                            ),
                            "subsequent_final_assays": sum(map(assay, following)),
                            "source_evidence_precedes_note": any(
                                assay(e) and e["cursor"] <= version["cursor"] for e in row["events"]
                            ),
                            "is_last_available_note": anchor["revision"]
                            == row["notes"][-1]["revision"],
                        }
                    )
                if [a["public_cursor"] for a in anchors] != sorted(
                    a["public_cursor"] for a in anchors
                ):
                    raise ValueError(f"Out-of-order history: {key}: {history['topic']}")
                histories.append(
                    {
                        **{k: v for k, v in history.items() if k != "standing"},
                        "analyst_scoped_assessment": history["standing"],
                        "history_id": f"{key}/H{number:02}",
                        "anchors": anchors,
                        "semantic_review": "assistant_analyst_full_notebook_reading",
                        "independent_human_review": False,
                    }
                )
            results.append(
                {
                    **record,
                    "histories": histories,
                    "cohort": row["cohort"],
                    "source": row["source"],
                    "manual_file": path.relative_to(ROOT).as_posix(),
                    "status": row["status"],
                    "failure": row["failure"],
                    "versions_read": len(row["notes"]),
                    "all_available_versions_read": True,
                    "operations": len(row["events"]),
                    "completed_source_batches": sum(map(assay, row["events"])),
                }
            )
    if seen != set(source):
        raise ValueError(f"Uncoded sessions: {sorted(set(source) - seen)}")
    return sorted(results, key=lambda r: r["key"])


def verify_sealed_followups():
    reviewed = read(OUTPUT / "sealed_followups.json")
    for record in reviewed["records"]:
        text = (ROOT / record["source"]).read_text(encoding="utf-8")
        parts = re.split(r"^## (K1|Q|K2|EQS)\s*$", text, flags=re.MULTILINE)
        stages = dict(zip(parts[1::2], parts[2::2], strict=True))
        for anchor in record["anchors"]:
            if anchor["contains"] not in stages.get(anchor["stage"], ""):
                raise ValueError(f"Unverified sealed quotation: {record['key']}: {anchor}")
    return {
        "scope": reviewed["scope"],
        "reviewed_reports": len(reviewed["records"]),
        "verified_stage_specific_quotes": sum(len(r["anchors"]) for r in reviewed["records"]),
    }


def render_report(records, summary):
    lines = [
        "# 全会话笔记精读与焦点命题历史",
        "",
        f"全部 {summary['reviewed_sessions']}/105 场、{summary['read_versions']} 版公开笔记已读。"
        f"逐场整理 {summary['focal_histories']} 条焦点命题历史，"
        f"{summary['verified_quote_anchors']} 个指定版本引文均逐字核对。",
        "",
        "这是覆盖所有会话的回溯语义精读，每场选取能呈现认识变化的焦点命题；"
        "不是对所有命题的穷举，也不是反绎成功率。解释、经验关系和工艺预期分别标记。"
        "两位协作助手分割会话完成阅读，不是独立重复编码或人类评审。"
        "后续用途主要指源研究动作、后续笔记和终点推荐；封存预测没有全队列逐篇精读。",
        "",
        "| 队列 | 会话 | 笔记版本 | 焦点历史 | 非 completed 状态 |",
        "|---|---:|---:|---:|---:|",
    ]
    for cohort, counts in summary["cohorts"].items():
        lines.append(
            f"| {cohort} | {counts['sessions']} | {counts['versions']} | "
            f"{counts['histories']} | {counts['noncompleted_status']} |"
        )
    lines += ["", "## 逐场结果", ""]
    for record in records:
        lines += [
            f"### {record['key']}",
            "",
            f"状态：`{record['status']}`；{record['versions_read']} 版；"
            f"{record['completed_source_batches']} 个最终测定。",
            "",
            record["reading"],
            "",
        ]
        for history in record["histories"]:
            lines += [
                f"**{history['topic']}** — `{history['kind']}` / "
                f"分析者限定判断 `{history['analyst_scoped_assessment']}`",
                "",
                history["test_interpretation"],
                "",
                "后续用途：" + history["later_use"],
                "",
            ]
            for anchor in history["anchors"]:
                lines += [
                    f"> v{anchor['revision']}，公开动作游标 {anchor['public_cursor']}："
                    + anchor["contains"],
                    "",
                ]
            lines += [
                "首次引文之后的结构性可用性："
                f"{history['anchors'][0]['subsequent_committed_research_actions']} 个提交研究动作、"
                f"{history['anchors'][0]['subsequent_final_assays']} 次最终测定。"
                "这些计数只描述时间顺序，不自动确认该命题驱动了动作。",
                "",
            ]
    (OUTPUT / "SESSION_READINGS.md").write_text("\n".join(lines), encoding="utf-8")


def build(rows):
    records = verify_coding(rows)
    histories = [h for r in records for h in r["histories"]]
    cohorts = {}
    for cohort in COHORTS:
        selected = [r for r in records if r["cohort"] == cohort]
        cohorts[cohort] = {
            "sessions": len(selected),
            "versions": sum(r["versions_read"] for r in selected),
            "histories": sum(len(r["histories"]) for r in selected),
            "source_final_assays": sum(r["completed_source_batches"] for r in selected),
            "noncompleted_status": sum(r["status"] != "completed" for r in selected),
            "statuses": dict(Counter(r["status"] for r in selected)),
        }
    summary = {
        "status": "complete_retained_notebook_reading_and_focal_history_coding",
        "planned_sessions": 105,
        "reviewed_sessions": len(records),
        "read_versions": sum(r["versions_read"] for r in records),
        "focal_histories": len(histories),
        "verified_quote_anchors": sum(len(h["anchors"]) for h in histories),
        "unverified_quote_anchors": 0,
        "histories_by_kind": dict(Counter(h["kind"] for h in histories)),
        "histories_by_analyst_scoped_assessment": dict(
            Counter(h["analyst_scoped_assessment"] for h in histories)
        ),
        "histories_first_anchored_after_last_source_research_action": sum(
            h["anchors"][0]["subsequent_committed_research_actions"] == 0 for h in histories
        ),
        "sessions_with_only_initial_note": [r["key"] for r in records if r["versions_read"] == 1],
        "sessions_without_explanatory_candidate_in_focal_selection": [
            r["key"]
            for r in records
            if not any(h["kind"] == "explanatory_candidate" for h in r["histories"])
        ],
        "cohorts": cohorts,
        "sealed_followup_review": verify_sealed_followups(),
        "failures": [
            {
                k: r[k]
                for k in ("key", "status", "failure", "versions_read", "completed_source_batches")
            }
            for r in records
            if r["status"] != "completed"
        ],
        "scope": [
            "All public notebook versions read; focal propositions traced across versions.",
            "Focal counts are not an exhaustive proposition denominator or an abduction rate.",
            "Assessment labels are analyst-scoped judgments, not verified explanatory mechanisms.",
            "Two assistants split sessions; no independent double-coding or human-review claim.",
            "All source operations indexed; substantive checks separate from temporal counts.",
            "Later use: source actions/notes/recommendations; sealed forecasts not all close-read.",
            "No simulator or provider calls; no old outcome replaced; cohorts remain distinct.",
        ],
    }
    write(OUTPUT / "histories_verified.json", {"scope": summary["scope"], "records": records})
    write(OUTPUT / "summary.json", summary)
    write(OUTPUT / "seed_execution_checks.json", seed_execution_checks(rows))
    write(
        OUTPUT / "execution_summaries.json",
        {
            "scope": "Public committed/rejected actions; no inferred cognition.",
            "sessions": [
                {"key": r["key"], "source": r["source"], "batches": batch_summary(r)} for r in rows
            ],
        },
    )
    with (OUTPUT / "session_summary.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        fields = [
            "key",
            "cohort",
            "status",
            "versions_read",
            "operations",
            "completed_source_batches",
        ]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: r[k] for k in fields} for r in records)
    render_report(records, summary)
    print(
        json.dumps(
            {
                k: summary[k]
                for k in (
                    "reviewed_sessions",
                    "read_versions",
                    "focal_histories",
                    "verified_quote_anchors",
                )
            }
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", choices=COHORTS)
    parser.add_argument("--repeat", default="repeat-01")
    parser.add_argument("--case")
    args = parser.parse_args()
    rows = sessions()
    if args.packet:
        packet(rows, args.packet, args.repeat, args.case)
        return
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write(
        OUTPUT / "source_index.json",
        {
            "scope": "105 retained research sessions; 309 complete public note versions",
            "source": "Current W2-257 binding; 45 EQ + 45 corrected C + 15 opportunity Research",
            "coding": "Paragraphs are extraction candidates, not semantic or abduction labels.",
            "sessions": [
                {k: v for k, v in row.items() if k not in ("events", "notes", "paragraphs")}
                | {
                    "versions": len(row["notes"]),
                    "paragraphs": len(row["paragraphs"]),
                    "operations": len(row["events"]),
                    "terminal_cursor": row["notes"][-1]["cursor"] if row["notes"] else None,
                }
                for row in rows
            ],
        },
    )
    build(rows)


if __name__ == "__main__":
    main()
