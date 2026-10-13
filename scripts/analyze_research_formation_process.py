"""Retrospective, provider-free process summaries of the retained 48 sessions.

No new scientific success rule or automated judgment of notebook prose is used.
Batch associations are descriptive, nested within sessions, and not causal effects.
"""

# Chinese report prose intentionally uses full-width punctuation.
# ruff: noqa: RUF001

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from statistics import fmean, median


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def qualified(metrics):
    return (
        metrics["particles_present"]
        and metrics["crystal_purity"] >= 0.8
        and metrics["crystal_fines_fraction"] <= 0.5
    )


def summarize(report_dir, raw_root):
    analysis = read(report_dir / "analysis.json")
    truth = read(raw_root / "references/truth.json")["EQ"]
    cases = []
    batches = []
    for original in analysis["cases"]:
        row = read(report_dir / original["repeat"] / f"{original['id']}.json")
        item = {
            "repeat": row["repeat"],
            "id": row["id"],
            "system": row["system"],
            "world": row["world"],
            "arm": row["arm"],
            "missing_stages": row["missing_stages"],
            "note_revisions": row["notebook"]["version_count"],
            "measurements": original["measurements"],
        }
        post = row["posttests"].get("Q", {}).get("payload") or {}
        predictions = post.get("predictions", [])
        if row["system"] == "EQ":
            item["q08_reference_mean"] = {
                m: fmean(r[m] for r in truth[f"EQ-{row['world']}"]["Q08"])
                for m in ("pH_normalized", "acid_dissociation_fraction", "precipitation_signal")
            }
            q08 = next((p for p in predictions if p["query_id"] == "Q08"), None)
            item["q08"] = q08
            item["source_mean"] = {
                m: fmean(b["metrics"][m] for b in row["batch_outcomes"])
                for m in item["q08_reference_mean"]
            }
            if q08:
                item["q08_intervals_include_source_mean"] = {
                    m: p["lower80"] <= item["source_mean"][m] <= p["upper80"]
                    for m, p in q08["metrics"].items()
                }
        else:
            item["purity_detail"] = original["purity_detail"]
            item["recommendation"] = row["recommendation"]
            item["retest_truth"] = row["retest"]["truth"][0]
            item["quench_batches"] = []
            for b, t in zip(
                row["batch_outcomes"], row["crystallization_quality"]["source_truth"], strict=True
            ):
                quench = any(a["operation"] == "quench" for a in b["actions"])
                if quench:
                    item["quench_batches"].append(b["lifecycle_index"])
                batches.append(
                    {
                        "repeat": row["repeat"],
                        "id": row["id"],
                        "batch": b["lifecycle_index"],
                        "any_quench": quench,
                        "truth": t,
                        "quality": qualified(t),
                        "quality_and_recovery": qualified(t) and t["crystal_yield"] >= 0.1,
                        "public_metrics": {
                            m: b["metrics"][m]
                            for m in ("crystal_purity", "crystal_yield", "crystal_fines_fraction")
                        },
                    }
                )
            item["quench_pattern"] = (
                "all"
                if len(item["quench_batches"]) == 12
                else "none"
                if not item["quench_batches"]
                else "mixed"
            )
        cases.append(item)

    session_groups = {}
    for pattern in ("all", "none", "mixed"):
        subset = [c for c in cases if c.get("quench_pattern") == pattern]
        session_groups[pattern] = {
            "sessions": len(subset),
            "retest_quality": sum(qualified(c["retest_truth"]) for c in subset),
            "retest_quality_and_recovery": sum(
                qualified(c["retest_truth"]) and c["retest_truth"]["crystal_yield"] >= 0.1
                for c in subset
            ),
            "cases": [f"{c['repeat']}/{c['id']}" for c in subset],
        }
    batch_groups = {}
    for flag in (True, False):
        subset = [b for b in batches if b["any_quench"] == flag]
        batch_groups[str(flag)] = {
            "batches": len(subset),
            "quality": sum(b["quality"] for b in subset),
            "quality_and_recovery": sum(b["quality_and_recovery"] for b in subset),
            "quality_recoveries": [b["truth"]["crystal_yield"] for b in subset if b["quality"]],
        }
    eq_groups = {}
    for arm in ("Opaque", "Aligned"):
        subset = [c for c in cases if c["system"] == "EQ" and c["arm"] == arm]
        valid = [c for c in subset if c["q08"]]
        eq_groups[arm] = {
            "source_sessions": len(subset),
            "valid_q": len(valid),
            "median_minimum_concentration_M": median(
                c["measurements"]["minimum_positive_concentration_M"] for c in subset
            ),
            "q08_widths_session_mean": {
                m: fmean(
                    c["q08"]["metrics"][m]["upper80"] - c["q08"]["metrics"][m]["lower80"]
                    for c in valid
                )
                for m in valid[0]["q08"]["metrics"]
            },
            "q08_covers_all_three_source_means": sum(
                all(c["q08_intervals_include_source_mean"].values()) for c in valid
            ),
        }
    return {
        "scope": "Retrospective descriptive process analysis of retained W2-249 records",
        "source_commit": analysis["source_commit"],
        "denominators": dict(Counter(c["system"] for c in cases)),
        "note_versions": sum(c["note_revisions"] for c in cases),
        "crystallization_session_quench_groups": session_groups,
        "crystallization_batch_quench_groups": batch_groups,
        "equilibrium_groups": eq_groups,
        "cases": cases,
        "crystallization_batches": batches,
        "limitations": [
            "Quench groups are post-hoc, chosen by participants and confounded with other actions.",
            "Batches and queries are nested observations, not independent researcher repeats.",
            "Interval inclusion of source means is descriptive, "
            "not a universal uncertainty criterion.",
            "Source notes, K1, Q and K2 are distinct time points; "
            "no qualitative label is assigned by code.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-dir", type=Path, required=True)
    parser.add_argument("--raw-root", type=Path, required=True)
    args = parser.parse_args()
    result = summarize(args.report_dir, args.raw_root)
    (args.report_dir / "process_analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    render_readings(args.report_dir, result)
    print(
        f"Summarized {len(result['cases'])}/48 sessions and "
        f"{len(result['crystallization_batches'])}/216 C batches; "
        "verified all close-reading quotations."
    )


def render_readings(report_dir, result):
    annotations = read(report_dir / "case_readings.json")
    rows = annotations["cases"]
    lookup = {(r["repeat"], r["id"]): r for r in result["cases"]}
    if len(rows) != 48 or len({(r["repeat"], r["id"]) for r in rows}) != 48:
        raise ValueError("Expected exactly 48 distinct reviewed sessions")
    if {(r["repeat"], r["id"]) for r in rows} != set(lookup):
        raise ValueError("Review coverage differs from retained sessions")
    lines = [
        "# 48 场同期记录逐场精读",
        "",
        annotations["scope"],
        "",
        "下文引文逐字核对到指定源笔记版本；相邻解释由分析者撰写。数字从保留导出生成。",
        "EQ 的极稀误差为 Q03/Q08/Q09 九个指标预测的 MAE；C 的复测为无噪真实结果。",
        "R1/R2/R3 是三次新会话，固定环境映射，无可控模型 RNG seed。缺测不填零。",
        "所有完整缺失原因见 [定量分析](ANALYSIS.md)；[综合解释](CLOSE_READING.md)。",
        "",
    ]
    previous = None
    for note in sorted(rows, key=lambda n: (n["id"], n["repeat"])):
        key = (note["repeat"], note["id"])
        r = lookup[key]
        prefix = f"{r['repeat']}/{r['id']}"
        text = (report_dir / f"{prefix}-notebook.md").read_text(encoding="utf-8")
        sections = re.split(r"^## Revision (\d+)\s*$", text, flags=re.M)
        revisions = dict(zip(sections[1::2], sections[2::2], strict=True))
        if note["quote"] not in revisions[str(note["revision"])]:
            raise ValueError(f"Quote absent in requested revision: {prefix}: {note['quote']}")
        if note["id"] != previous:
            lines.extend([f"## {note['id']}", ""])
            previous = note["id"]
        lines.extend([f"### {note['repeat']}", "", note["reading"], ""])
        lines.append(f"> {note['quote']}")
        lines.append("")
        lines.append(
            f"出处：[笔记 v{note['revision']}]({prefix}-notebook.md#revision-{note['revision']})；"
            f"[K1/Q/K2]({prefix}-reports.md)；"
            f"[批次与预测原始科学导出]({prefix}.json)。"
        )
        lines.append("")
        m = r["measurements"]
        if r["system"] == "EQ":
            mae = m.get("lowest_three_macro_mae")
            score = f"{mae:.5f}" if mae is not None else "缺测"
            lines.append(
                f"数值核对：最低名义浓度 {m['minimum_positive_concentration_M']:.6g} M；"
                f"极稀三题 MAE {score}。"
            )
        else:
            t = r["retest_truth"]
            verdict = (
                "质量及回收目标均达到"
                if qualified(t) and t["crystal_yield"] >= 0.1
                else "仅质量合格"
                if qualified(t)
                else "质量不合格"
            )
            lines.append(
                f"数值核对：淬灭批次 {len(r['quench_batches'])}/12；"
                f"推荐复测回收 {t['crystal_yield']:.5f}、"
                f"细粉 {t['crystal_fines_fraction']:.5f}，{verdict}；"
                f"纯度预测 MAE {m['crystal_purity_mae']:.5f}；"
                f"质量分类 {m['quality_correct_of_12']}/12 正确。"
            )
        if r["missing_stages"]:
            lines.append("缺失阶段：" + ", ".join(r["missing_stages"]) + "。")
        lines.append("")
    (report_dir / "CASE_READINGS.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
