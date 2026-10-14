"""Link retained public notebook versions to actual experiments, without new runs.

Temporal opportunities are availability measurements, not semantic updates or
causal effects. Only public actions and measured observations are exported.
"""

# Chinese report prose intentionally uses full-width punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from pathlib import Path
from statistics import fmean

from scripts.run_paper_case_notebooks import case_folder

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams/flagship_tasks/reports/research-extension-20261014"
OUTPUT = ROOT / "workstreams/flagship_tasks/reports/inquiry-trajectories-20261014"
RAW_BASE = ROOT.parent / "ChemWorld-local-research"
RAW_ROOTS = {
    "retained_48": RAW_BASE / "20261013-research-formation/attempt-01",
    "extension_42": RAW_BASE / "20261014-research-extension/attempt-01",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_notes(path):
    parts = re.split(r"^## Revision (\d+)\s*$", path.read_text(encoding="utf-8"), flags=re.M)
    return {
        int(revision): body.strip().split("\n\n", 1)[1].strip()
        for revision, body in zip(parts[1::2], parts[2::2], strict=True)
    }


def public_events(path):
    events = []
    with path.open(encoding="utf-8") as stream:
        for cursor, line in enumerate(stream, 1):
            raw = json.loads(line)
            measured = raw["action"].get("operation") == "measure"
            observed = raw.get("agent_visible_observation", {}).get("observation")
            if observed is None:
                observed = raw.get("observation", {})
            events.append(
                {
                    "cursor": cursor,
                    "batch": raw["experiment_index"] + 1,
                    "action": raw["action"],
                    "transaction_status": raw["transaction_status"],
                    "observations": {
                        k: v
                        for k, v in observed.items()
                        if measured and v is not None and raw.get("observed_mask", {}).get(k)
                    },
                }
            )
    return events


def final_assay(event):
    return event["action"].get("instrument") == "final_assay" and committed(event)


def committed(event):
    return event["transaction_status"] == "committed"


def research_action(event):
    return committed(event) and event["action"]["operation"] not in ("measure", "terminate")


def interval_events(events, start, end):
    return [event for event in events if start < event["cursor"] <= end]


def timeline(row, events, notes):
    versions = row["notebook"]["versions"]
    result = []
    previous = 0
    for index, version in enumerate(versions):
        cursor = version["public_cursor"]["event_count"]
        if not previous <= cursor <= len(events):
            raise ValueError("Notebook cursor is out of order or beyond the trajectory")
        next_version = versions[index + 1] if index + 1 < len(versions) else None
        end = next_version["public_cursor"]["event_count"] if next_version else len(events)
        following = interval_events(events, cursor, end)
        new_assays = [event for event in following if final_assay(event)]
        after_later = next(
            (event for event in events if event["cursor"] > end and research_action(event)),
            None,
        )
        result.append(
            {
                "revision": version["revision"],
                "public_cursor": cursor,
                "text": notes[version["revision"]],
                "new_final_assays_since_previous_note": [
                    event["cursor"]
                    for event in interval_events(events, previous, cursor)
                    if final_assay(event)
                ],
                "next_revision": next_version["revision"] if next_version else None,
                "following_interval_end": end,
                "following_action_cursors": [event["cursor"] for event in following],
                "following_final_assay_cursors": [event["cursor"] for event in new_assays],
                "following_committed_research_actions": sum(map(research_action, following)),
                "following_rejected_actions": sum(not committed(event) for event in following),
                "first_research_action_after_next_revision": (
                    after_later["cursor"] if next_version and after_later else None
                ),
                "structural_feedback_opportunity": bool(
                    next_version and new_assays and after_later
                ),
                "semantic_update": "not_inferred_from_temporal_structure",
            }
        )
        previous = cursor
    return result


def path_features(events):
    batches = []
    for number in sorted({event["batch"] for event in events}):
        attempted = [event for event in events if event["batch"] == number]
        actions = [event["action"] for event in attempted if committed(event)]
        volume = sum(a.get("volume_L", 0) for a in actions if a["operation"] == "add_solvent")
        reagent = sum(a.get("amount_mol", 0) for a in actions if a["operation"] == "add_reagent")
        batches.append(
            {
                "batch": number,
                "first_cursor": attempted[0]["cursor"],
                "last_cursor": attempted[-1]["cursor"],
                "completed": any(map(final_assay, attempted)),
                "nominal_solvent_added_L": volume,
                "nominal_reagent_added_mol": reagent,
                "nominal_reagent_per_added_solvent_M": reagent / volume if volume else None,
                "solvents": sorted(
                    {a["solvent"] for a in actions if a["operation"] == "add_solvent"}
                ),
                "seed_added_g": sum(
                    a.get("seed_mass_g", 0) for a in actions if a["operation"] == "seed_crystals"
                ),
                "quench_committed": any(a["operation"] == "quench" for a in actions),
                "operation_types": sorted({a["operation"] for a in actions}),
                "rejected_attempts": sum(not committed(event) for event in attempted),
                "committed_action_sequence": actions,
            }
        )
    recipes = [
        json.dumps(b["committed_action_sequence"], sort_keys=True)
        for b in batches
        if b["completed"]
    ]
    positive = [
        b["nominal_reagent_per_added_solvent_M"]
        for b in batches
        if b["nominal_reagent_per_added_solvent_M"]
    ]
    metrics = {
        "source_operations": len(events),
        "completed_batches": sum(b["completed"] for b in batches),
        "rejected_attempts": sum(not committed(event) for event in events),
        "distinct_committed_operation_types": len(
            {e["action"]["operation"] for e in events if committed(e)}
        ),
        "distinct_solvents": len({s for b in batches for s in b["solvents"]}),
        "intermediate_measurements": sum(
            committed(e) and e["action"]["operation"] == "measure" and not final_assay(e)
            for e in events
        ),
        "exact_sequence_repeat_batches": len(recipes) - len(set(recipes)),
        "minimum_positive_nominal_concentration_M": min(positive) if positive else None,
        "maximum_positive_nominal_concentration_M": max(positive) if positive else None,
        "quench_batches": sum(b["quench_committed"] for b in batches),
    }
    return batches, metrics


def extract(row, report, raw_roots):
    folder = case_folder(raw_roots[row["cohort"]] / row["repeat"], row)
    events = public_events(folder / "trajectory.jsonl")
    prefix = report / row["repeat"] / row["id"]
    notes = parse_notes(prefix.with_name(prefix.name + "-notebook.md"))
    if len(events) != row["operations"]:
        raise ValueError("Operation count differs from retained export")
    assays = [event for event in events if final_assay(event)]
    if len(assays) != row["completed_batches"]:
        raise ValueError("Successful final-assay count differs from retained export")
    for event, batch in zip(assays, row["batch_outcomes"], strict=True):
        if event["batch"] != batch["lifecycle_index"]:
            raise ValueError("Batch index differs from retained export")
        if any(event["observations"].get(k) != v for k, v in batch["metrics"].items()):
            raise ValueError("Public final-assay metrics differ from retained export")
    versions = row["notebook"]["versions"]
    if set(notes) != {v["revision"] for v in versions}:
        raise ValueError("Notebook versions differ from retained export")
    linked = timeline(row, events, notes)
    batches, metrics = path_features(events)
    metrics.update(
        notebook_versions=len(linked),
        structural_feedback_opportunities=sum(v["structural_feedback_opportunity"] for v in linked),
        versions_with_subsequent_experiment=sum(
            v["following_committed_research_actions"] > 0 for v in linked
        ),
        versions_with_new_final_assays=sum(
            bool(v["new_final_assays_since_previous_note"]) for v in linked
        ),
    )
    return {
        **{
            k: row[k]
            for k in (
                "repeat",
                "id",
                "system",
                "world",
                "arm",
                "cohort",
                "status",
                "failure",
                "missing_stages",
            )
        },
        "source_checks": {
            "operations": True,
            "final_assays": True,
            "measurements": True,
            "notebook_cursors": True,
        },
        "metrics": metrics,
        "versions": linked,
        "batches": batches,
        "events": events,
    }


def summarize(sessions, original_failures):
    grouped = {}
    for system in ("EQ", "C"):
        for arm in ("Opaque", "Aligned", "MisIndexed"):
            rows = [s for s in sessions if s["system"] == system and s["arm"] == arm]
            metrics = {}
            for metric in rows[0]["metrics"]:
                worlds = []
                for world in sorted({s["world"] for s in rows}):
                    observed = [
                        s["metrics"][metric]
                        for s in rows
                        if s["world"] == world and s["metrics"][metric] is not None
                    ]
                    if observed:
                        worlds.append(fmean(observed))
                metrics[metric] = fmean(worlds) if worlds else None
            grouped[f"{system}/{arm}"] = {
                "sessions": len(rows),
                "sessions_with_structural_opportunity": sum(
                    s["metrics"]["structural_feedback_opportunities"] > 0 for s in rows
                ),
                "cohorts": dict(Counter(s["cohort"] for s in rows)),
                "world_equal_means": metrics,
            }
    return {
        "scope": "Retrospective public statement/action/observation alignment; no new runs",
        "counts": {
            "sessions": len(sessions),
            "operations": sum(s["metrics"]["source_operations"] for s in sessions),
            "completed_batches": sum(s["metrics"]["completed_batches"] for s in sessions),
            "notebook_versions": sum(s["metrics"]["notebook_versions"] for s in sessions),
            "structural_feedback_opportunities": sum(
                s["metrics"]["structural_feedback_opportunities"] for s in sessions
            ),
            "sessions_with_structural_opportunity": sum(
                s["metrics"]["structural_feedback_opportunities"] > 0 for s in sessions
            ),
            "source_validation_passed": sum(all(s["source_checks"].values()) for s in sessions),
        },
        "cohorts": dict(Counter(s["cohort"] for s in sessions)),
        "original_failures": original_failures,
        "grouped": grouped,
        "sessions": [
            {k: v for k, v in s.items() if k not in ("events", "batches", "versions")}
            for s in sessions
        ],
        "interpretation": [
            "Temporal windows measure available evidence, not semantic changes or cognition.",
            "Judgments may be unchanged despite a new version; "
            "absent notes are not absent beliefs.",
            "Nonmeasurement committed actions include preparation; an opportunity is not "
            "proof of a new discriminating test.",
            "Exact repeated command sequences include container identifiers and are conservative "
            "descriptions, not verified controlled replication.",
            "Nominal additions are not effective concentration, dissolved inventory "
            "or post-treatment volume.",
            "Fixed-world sessions have uncontrolled model RNG and nested, dependent batches.",
            "MisIndexed was run later; between-arm path differences are descriptive, not causal.",
            "Recovery instructions and observations differ; no clean recovery-understanding claim.",
            "Independent semantic case review remains outstanding.",
        ],
    }


def all_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from all_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_strings(child)


def verify_focal_chains(sessions, report, output):
    source = read(output / "focal_chains.json")
    lookup = {(s["repeat"], s["id"]): s for s in sessions}
    checked = []
    quotes = 0
    lines = [
        "# 研究路径与科学判断的连续主例",
        "",
        "五条既有主例的事后连续分析。逐字核对指定笔记版本与后测阶段，",
        "按真实操作位置排列；研究者所写的因果表述仍是待评价的解释。",
        "同一分析者完成，不代表独立复核或现象发生率。",
        "",
    ]
    for chain in source["chains"]:
        session = lookup[chain["repeat"], chain["id"]]
        raw_export = read(report / chain["repeat"] / f"{chain['id']}.json")
        versions = {v["revision"]: v for v in session["versions"]}
        batches = {b["batch"]: b for b in session["batches"]}
        events = {e["cursor"]: e for e in session["events"]}
        position = 0
        stages = []
        name = f"{chain['repeat']}/{chain['id']}"
        lines += [
            f"## {chain['title']}",
            "",
            f"[完整时序](sessions/{name}.json)；{name}。",
            "",
            "| 阶段 | 实际位置 | 公开判断或检验 |",
            "| --- | --- | --- |",
        ]
        for stage in chain["stages"]:
            kind = stage["kind"]
            if kind == "note":
                version = versions[stage["revision"]]
                if stage["quote"] not in version["text"]:
                    raise ValueError(f"Absent focal quotation: {name} revision {stage['revision']}")
                first = last = version["public_cursor"]
                label = f"笔记 v{stage['revision']}"
                text = stage["quote"]
                detail = {"exact_quote_verified": True}
                quotes += 1
            elif kind == "tests":
                selected = [batches[number] for number in stage["batches"]]
                first, last = selected[0]["first_cursor"], selected[-1]["last_cursor"]
                label = "批次 " + ", ".join(map(str, stage["batches"]))
                text = stage["description"]
                detail = {
                    "batches": [
                        {
                            **{
                                k: b[k]
                                for k in (
                                    "batch",
                                    "seed_added_g",
                                    "nominal_solvent_added_L",
                                    "rejected_attempts",
                                )
                            },
                            "final_assays": [
                                e["observations"]
                                for e in events.values()
                                if e["batch"] == b["batch"] and final_assay(e)
                            ],
                        }
                        for b in selected
                    ]
                }
            elif kind == "posttest":
                response = raw_export["posttests"][stage["stage"]]
                if not any(stage["quote"] in text for text in all_strings(response)):
                    raise ValueError(f"Absent focal posttest quotation: {name} {stage['stage']}")
                first = last = len(events) + 1
                label = "封存后测 " + stage["stage"]
                text = stage["quote"]
                detail = {"exact_quote_verified": True, "after_source_closed": True}
                quotes += 1
            else:
                raise ValueError(f"Unknown chain stage {kind}")
            if first < position:
                raise ValueError(f"Focal chain contradicts event chronology: {name}")
            position = last
            stages.append({**stage, "first_cursor": first, "last_cursor": last, **detail})
            escaped = text.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {label} | {first}–{last} | {escaped} |")
        lines += ["", chain["finding"], "", chain["boundary"], ""]
        checked.append({**chain, "stages": stages, "chronology_verified": True})
    result = {
        "scope": source["scope"],
        "chains_verified": len(checked),
        "exact_quotes_verified": quotes,
        "chains": checked,
    }
    write(output / "focal_chains_verified.json", result)
    (output / "FOCAL_CHAINS.md").write_text("\n".join(lines), encoding="utf-8")
    return {k: result[k] for k in ("chains_verified", "exact_quotes_verified")}


def render(summary, output):
    c = summary["counts"]
    lines = [
        "# 自主研究路径与科学判断的时序连接",
        "",
        "本分析对齐既有研究中的公开笔记、实际执行和后续行动，不新增模型或模拟器实验。",
        "",
        f"核对 {c['sessions']}/90 场、{c['operations']} 次操作、"
        f"{c['completed_batches']}/1080 次最终测定和 {c['notebook_versions']} 版笔记。",
        f"其中 {c['sessions_with_structural_opportunity']}/90 场具有至少一个结构性反馈观察窗口，"
        f"共 {c['structural_feedback_opportunities']} 个嵌套窗口。",
        "",
        "窗口要求：较早笔记之后出现新的成功最终测定，随后写出较晚笔记，其后仍有成功的非测量实验操作。",
        "它只说明完整往返过程有机会被观察，不表示判断已修订、行动由笔记造成或假说已被区分。",
        "[连续主例及解释](FOCAL_CHAINS.md)逐项核对公开判断、实际检验与后续使用。",
        "",
        "## 全部会话",
        "",
        "| 会话 | 体系/世界/信息 | 时期 | 状态 | 批次 | 笔记 | 结构窗口 | 拒绝操作 | 记录 |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for s in summary["sessions"]:
        m = s["metrics"]
        name = f"{s['repeat']}/{s['id']}"
        lines.append(
            f"| {s['repeat']} | {s['id']} | {s['cohort']} | {s['status']} | "
            f"{m['completed_batches']}/12 | {m['notebook_versions']} | "
            f"{m['structural_feedback_opportunities']} | {m['rejected_attempts']} | "
            f"[时序](sessions/{name}.json) |"
        )
    lines += [
        "",
        "## 分层描述",
        "",
        "世界等权均值；每臂15场。后一期信息臂不构成同期随机对照。",
        "",
        "| 体系/信息 | 有窗口会话 | 平均笔记版本 | 平均中间测量 | 平均完全重复序列批次 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for key, g in summary["grouped"].items():
        m = g["world_equal_means"]
        lines.append(
            f"| {key} | {g['sessions_with_structural_opportunity']}/{g['sessions']} | "
            f"{m['notebook_versions']:.3f} | {m['intermediate_measurements']:.3f} | "
            f"{m['exact_sequence_repeat_batches']:.3f} |"
        )
    lines += [
        "",
        "## 原实验不完整链",
        "",
        "缺失后测继续保留，不以新增会话替换，也不记为预测错误。",
        "",
    ]
    for f in summary["original_failures"]:
        lines.append(
            f"- {f['repeat']}/{f['id']}: {f.get('status')}; "
            f"missing={f.get('missing_stages')}; {f.get('failure')}"
        )
    lines += ["", "## 解释范围", "", *[f"- {text}" for text in summary["interpretation"]], ""]
    (output / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    analysis = read(args.report / "analysis.json")
    keys = {(r["repeat"], r["id"]) for r in analysis["cases"]}
    if len(analysis["cases"]) != 90 or len(keys) != 90:
        raise ValueError("Expected exactly 90 retained cases")
    for cohort, root in RAW_ROOTS.items():
        scheduled = {(r["repeat"], r["id"]) for r in read(root / "design.json")["schedule"]}
        exported = {(r["repeat"], r["id"]) for r in analysis["cases"] if r["cohort"] == cohort}
        if scheduled != exported:
            raise ValueError(f"Retained cohort differs from actual execution design: {cohort}")
    sessions = []
    start = time.monotonic()
    for index, original in enumerate(analysis["cases"], 1):
        row = read(args.report / original["repeat"] / f"{original['id']}.json")
        session = extract(row, args.report, RAW_ROOTS)
        sessions.append(session)
        write(args.output / "sessions" / row["repeat"] / f"{row['id']}.json", session)
        elapsed = time.monotonic() - start
        print(
            json.dumps(
                {
                    "stage": "align_retained_trajectories",
                    "completed": index,
                    "total": 90,
                    "sessions_per_minute": round(index / max(elapsed, 0.001) * 60, 2),
                    "eta_seconds": round(elapsed / index * (90 - index), 1),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    summary = summarize(sessions, analysis["failures"])
    summary["focal_checks"] = verify_focal_chains(sessions, args.report, args.output)
    write(args.output / "summary.json", summary)
    render(summary, args.output)
    print(json.dumps(summary["counts"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
