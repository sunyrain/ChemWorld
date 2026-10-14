"""Read-only analysis of retained evidence; no model or simulator execution.

Validate manually selected quotations against their notebook revisions, summarize
all 90 retained sessions, and render the 42 new close readings. This does not
automatically classify scientific reasoning or estimate causal notebook effects.
"""

# Chinese report prose intentionally uses full-width punctuation.
# ruff: noqa: RUF001

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from statistics import fmean


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def key(row):
    return row["repeat"], row["id"]


def world_mean(rows, metric):
    values = []
    for world in sorted({r["world"] for r in rows}):
        observed = [
            r["measurements"][metric]
            for r in rows
            if r["world"] == world and r["measurements"].get(metric) is not None
        ]
        if observed:
            values.append(fmean(observed))
    return fmean(values) if values else None


def build(report_dir):
    analysis = read(report_dir / "analysis.json")
    rows = [read(report_dir / r["repeat"] / f"{r['id']}.json") for r in analysis["cases"]]
    lookup = {key(r): r for r in rows}
    if len(rows) != 90 or len(lookup) != 90:
        raise ValueError("Expected 90 distinct retained sessions")
    annotations = read(report_dir / "case_readings.json")["readings"]
    new_keys = {key(r) for r in rows if r["cohort"] == "extension_42"}
    if len(annotations) != 42 or {key(r) for r in annotations} != new_keys:
        raise ValueError("Close readings must cover exactly the 42 new sessions")
    notes = {}
    for a in annotations:
        prefix = f"{a['repeat']}/{a['id']}"
        text = (report_dir / f"{prefix}-notebook.md").read_text(encoding="utf-8")
        sections = re.split(r"^## Revision (\d+)\s*$", text, flags=re.M)
        revisions = dict(zip(sections[1::2], sections[2::2], strict=True))
        row = lookup[key(a)]
        if len(revisions) != row["notebook"]["version_count"]:
            raise ValueError(f"Revision count differs: {prefix}")
        if a["quote"] not in revisions[str(a["revision"])]:
            raise ValueError(f"Quotation absent from revision {a['revision']}: {prefix}")
        notes[key(a)] = len(revisions)
    if sum(notes.values()) != 139:
        raise ValueError("Expected all 139 new revisions")

    # The earlier public process summary already contains all five EQ references.
    earlier = read(report_dir.parent / "research-formation-20261013/process_analysis.json")
    eq_truth = {
        r["world"]: r["q08_reference_mean"] for r in earlier["cases"] if r["system"] == "EQ"
    }
    cases = []
    for row in rows:
        item = {
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
                "completed_batches",
                "missing_stages",
                "measurements",
                "recommendation",
            )
        }
        item["note_versions"] = row["notebook"]["version_count"]
        item["note_cursors"] = [
            {"revision": v["revision"], "public_operations": v["public_cursor"]["event_count"]}
            for v in row["notebook"]["versions"]
        ]
        item["q_valid"] = bool(
            row["prediction_evaluation"] and row["prediction_evaluation"].get("valid")
        )
        if row["system"] == "C":
            item["seed_execution"] = row["seed_execution"]
            item["purity_detail"] = row["purity_detail"]
            item["retest_truth"] = row["retest"]["truth"][0]
            selected = row["recommendation"]["selected_experiment_index"]
            item["selected_public_metrics"] = next(
                b["metrics"] for b in row["batch_outcomes"] if b["lifecycle_index"] == selected
            )
        else:
            q = row["posttests"].get("Q", {}).get("payload") or {}
            item["q08"] = next(
                (p for p in q.get("predictions", []) if p["query_id"] == "Q08"), None
            )
            item["q08_reference_mean"] = eq_truth[row["world"]]
        cases.append(item)

    grouped = {}
    for system in ("EQ", "C"):
        grouped[system] = {}
        for arm in ("Opaque", "Aligned", "MisIndexed"):
            subset = [r for r in rows if r["system"] == system and r["arm"] == arm]
            metrics = (
                ["lowest_three_macro_mae", "remaining_nine_macro_mae", "lowest_three_coverage80"]
                if system == "EQ"
                else [
                    "crystal_purity_mae",
                    "crystal_yield_mae",
                    "crystal_fines_fraction_mae",
                    "purity_signed_error",
                ]
            )
            entry = {
                "planned_sessions": len(subset),
                "valid_q": sum(
                    lookup[key(r)]["prediction_evaluation"] is not None
                    and bool(lookup[key(r)]["prediction_evaluation"].get("valid"))
                    for r in subset
                ),
                "cohorts": dict(Counter(r["cohort"] for r in subset)),
                "world_equal_means": {m: world_mean(subset, m) for m in metrics},
            }
            if system == "C":
                entry["recommendation_successes"] = sum(
                    r["measurements"]["recommendation_quality_and_yield_target"] for r in subset
                )
                entry["thermal_direction_correct"] = sum(
                    r["measurements"]["thermal_fines_direction_correct"] for r in subset
                )
            else:
                entry["sampled_below_1mM"] = sum(
                    r["measurements"]["sampled_below_1mM"] for r in subset
                )
            grouped[system][arm] = entry

    seed_rows = [r for r in rows if r["system"] == "C"]
    rejected = [
        {"repeat": r["repeat"], "id": r["id"], "cohort": r["cohort"], **b}
        for r in seed_rows
        for b in r["seed_execution"]["by_batch"]
        if b["rejected_calls"]
    ]
    counts = {
        "sessions": len(rows),
        "systems": dict(Counter(r["system"] for r in rows)),
        "cohorts": dict(Counter(r["cohort"] for r in rows)),
        "source_batches": sum(r["completed_batches"] for r in rows),
        "planned_source_batches": 1080,
        "note_versions": sum(r["notebook"]["version_count"] for r in rows),
        "new_read_sessions": len(notes),
        "new_read_versions": sum(notes.values()),
        "new_quotes_verified": len(annotations),
        "old_read_sessions_reused": 48,
        "old_read_versions_reused": 145,
        "C_sessions_with_rejected_seed": len({key(r) for r in rejected}),
        "C_batches_with_rejected_seed": len(rejected),
        "rejected_seed_calls": sum(r["rejected_calls"] for r in rejected),
    }
    result = {
        "scope": "Retrospective process analysis of 90 retained sessions; no new experiment",
        "counts": counts,
        "original_failures": analysis["failures"],
        "outcomes_by_arm": grouped,
        "rejected_seed_batches": rejected,
        "cases": cases,
        "limitations": [
            "42 new sessions were close-read now; the earlier 48-session annotations are reused.",
            "Single-analyst readings; no independent adjudication or prevalence estimates.",
            "Rejected seeds are not material additions; batch actions include attempts.",
            "No notebook-read call does not establish that notes were unavailable or unused.",
            "Public statements and chronology do not establish private reasoning or causality.",
            "C MisIndexed swaps solvent descriptors 1 and 3; solvent 2 and catalysts are intact.",
            "World-equal means retain missingness; cohorts are not concurrently randomized arms.",
            "Three sessions per cell: fixed world/observation mapping, uncontrolled model RNG.",
        ],
    }
    write(report_dir / "process_analysis.json", result)
    render(report_dir, annotations, {key(r): r for r in cases})
    return result


def render(report_dir, annotations, lookup):
    lines = [
        "# 新增 42 场研究笔记逐场精读",
        "",
        "覆盖全部新增 42 场、139 版源笔记。引文逐字核对到指定版本；中文解释由分析者撰写。",
        "既有 48 场、145 版的精读保留在[原分析](../research-formation-20261013/CASE_READINGS.md)。",
        "数值由保留科学导出生成，缺测不填零；R1–R3 是同世界的新会话，不是受控模型随机种子。",
        "[最终稿证据族与补实验判断](EVIDENCE_FAMILIES.md)；[全部失败和分母](ANALYSIS.md)。",
        "",
    ]
    for a in sorted(annotations, key=lambda r: (r["id"], r["repeat"])):
        row = lookup[key(a)]
        prefix = f"{a['repeat']}/{a['id']}"
        lines.extend([f"## {a['id']} {a['repeat']}", "", a["reading"], "", f"> {a['quote']}", ""])
        lines.extend(
            [
                f"出处：[笔记 v{a['revision']}]({prefix}-notebook.md#revision-{a['revision']})；"
                f"[K1 Q K2]({prefix}-reports.md)；[执行与结果]({prefix}.json)。",
                "",
            ]
        )
        if a.get("execution_check"):
            lines.extend([a["execution_check"], ""])
        m = row["measurements"]
        if row["system"] == "EQ":
            mae = m.get("lowest_three_macro_mae")
            score = f"{mae:.5f}" if mae is not None else "缺测"
            lines.append(
                f"最低名义浓度 {m['minimum_positive_concentration_M']:.6g} M；"
                f"极稀三题 MAE {score}。"
            )
        else:
            t = row["retest_truth"]
            verdict = (
                "达到质量与回收目标"
                if m["recommendation_quality_and_yield_target"]
                else "未同时达标"
            )
            lines.append(
                f"推荐复测：回收 {t['crystal_yield']:.5f}、"
                f"细粉 {t['crystal_fines_fraction']:.5f}，{verdict}；"
                f"纯度预测 MAE {m['crystal_purity_mae']:.5f}；热对比方向"
                f"{'正确' if m['thermal_fines_direction_correct'] else '错误'}。"
            )
        if row["missing_stages"]:
            lines.append("缺失阶段：" + ", ".join(row["missing_stages"]) + "。")
        lines.append("")
    (report_dir / "CASE_READINGS.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("workstreams/flagship_tasks/reports/research-extension-20261014"),
    )
    args = parser.parse_args()
    result = build(args.report_dir)
    print(json.dumps(result["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
