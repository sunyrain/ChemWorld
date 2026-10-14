"""Validate analyst codes for every retained structural feedback window.

No code infers semantic labels. Exact quotations and temporal execution anchors
are checked; qualitative classifications remain a single analyst's interpretation.
"""

# Chinese report prose intentionally uses full-width punctuation.
# ruff: noqa: RUF001

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "workstreams/flagship_tasks/reports/inquiry-trajectories-20261014"
UPDATES = {"established", "revised", "narrowed", "unresolved", "restated", "unassessable"}
LINKS = {"matched", "partly_matched", "rejected", "not_executed", "unclear", "no_explicit_plan"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def record_key(record):
    return record["repeat"], record["id"], record["from_revision"]


def validate_record(record, session):
    versions = {v["revision"]: v for v in session["versions"]}
    earlier = versions[record["from_revision"]]
    later = versions[record["to_revision"]]
    if not earlier["structural_feedback_opportunity"]:
        raise ValueError("Not a prespecified structural window")
    if earlier["next_revision"] != later["revision"]:
        raise ValueError("Window must use adjacent versions")
    if not record["update_types"] or not set(record["update_types"]) <= UPDATES:
        raise ValueError("Unknown public-update label")
    if not record["update_quote"] or record["update_quote"] not in later["text"]:
        raise ValueError("Update quotation absent from the later version")
    plan = record["next_plan_quote"]
    if plan is not None and (not plan or plan not in later["text"]):
        raise ValueError("Plan quotation absent from the later version")
    link = record["action_link"]
    if link not in LINKS:
        raise ValueError("Unknown action-link label")
    if link == "no_explicit_plan" and (plan is not None or record["action_cursors"]):
        raise ValueError("No-plan code cannot assert a matched plan or action")
    if link not in ("no_explicit_plan", "unclear") and plan is None:
        raise ValueError("An assessed plan needs its prospective quotation")
    events = {e["cursor"]: e for e in session["events"]}
    evidence = []
    for number in record["new_evidence_batches"]:
        assays = [
            e
            for e in events.values()
            if e["batch"] == number
            and e["action"].get("instrument") == "final_assay"
            and e["transaction_status"] == "committed"
        ]
        if len(assays) != 1:
            raise ValueError("Evidence requires one successful final assay per cited batch")
        event = assays[0]
        if not earlier["public_cursor"] < event["cursor"] <= later["public_cursor"]:
            raise ValueError("Evidence citation was not newly available in this window")
        evidence.append(event["cursor"])
    if not evidence:
        raise ValueError("A coded feedback window needs a new-evidence anchor")
    selected = [events[cursor] for cursor in record["action_cursors"]]
    if not all(
        later["public_cursor"] < e["cursor"] <= later["following_interval_end"] for e in selected
    ):
        raise ValueError("Action citation is outside the immediate prospective interval")
    if link in ("matched", "partly_matched") and (
        not selected or not any(e["transaction_status"] == "committed" for e in selected)
    ):
        raise ValueError("A matched execution requires an actual committed action")
    if link == "rejected" and (
        not selected or all(e["transaction_status"] == "committed" for e in selected)
    ):
        raise ValueError("Rejected execution needs a rejected attempt")
    if link == "not_executed" and selected:
        raise ValueError("An unexecuted plan cannot carry executed action anchors")
    if not record["interpretation"].strip():
        raise ValueError("Analyst interpretation is required")
    return {
        **record,
        "earlier_cursor": earlier["public_cursor"],
        "later_cursor": later["public_cursor"],
        "immediate_interval_end": later["following_interval_end"],
        "verified_evidence_cursors": evidence,
        "verified_actions": selected,
        "quotes_verified": 1 + (plan is not None),
        "interpretation_independently_reviewed": False,
    }


def build(output):
    summary = (
        read(output / "summary.json")
        if (output / "summary.json").exists()
        else {"sessions": read(output / "analysis.json")["cases"]}
    )
    coding = read(output / "semantic_coding.json")
    sessions = {
        (r["repeat"], r["id"]): read(output / "sessions" / r["repeat"] / f"{r['id']}.json")
        for r in summary["sessions"]
    }
    expected = {
        (s["repeat"], s["id"], v["revision"])
        for s in sessions.values()
        for v in s["versions"]
        if v["structural_feedback_opportunity"]
    }
    if len(expected) != coding["planned_windows"]:
        raise ValueError("Planned semantic coverage differs from retained structural windows")
    records = coding["records"]
    keys = {record_key(r) for r in records}
    if len(keys) != len(records) or not keys <= expected:
        raise ValueError("Duplicate or out-of-scope codes")
    verified = []
    for record in records:
        try:
            verified.append(validate_record(record, sessions[record["repeat"], record["id"]]))
        except ValueError as error:
            raise ValueError(f"{record_key(record)}: {error}") from error
    pending = sorted(expected - keys)
    complete_sessions = []
    no_window_sessions = []
    for key in sessions:
        required = {k for k in expected if k[:2] == key}
        if not required:
            no_window_sessions.append(key)
        elif required <= keys:
            complete_sessions.append(key)
    coverage = {}
    for system in sorted({s["system"] for s in sessions.values()}):
        system_keys = {key for key, session in sessions.items() if session["system"] == system}
        system_windows = {key for key in expected if key[:2] in system_keys}
        coverage[system] = {
            "sessions": len(system_keys),
            "planned_windows": len(system_windows),
            "coded_windows": len(system_windows & keys),
            "sessions_all_available_windows_coded": sum(
                k in system_keys for k in complete_sessions
            ),
            "sessions_without_observable_complete_window": sum(
                k in system_keys for k in no_window_sessions
            ),
        }
    result = {
        "scope": coding["scope"],
        "complete": not pending,
        "planned_windows": len(expected),
        "coded_windows": len(verified),
        "verified_quotes": sum(r["quotes_verified"] for r in verified),
        "coverage_by_system": coverage,
        "sessions_all_available_windows_coded": complete_sessions,
        "sessions_without_observable_complete_window": no_window_sessions,
        "pending_windows": pending,
        "records": verified,
        "limitations": [
            "Codes describe public statements and selected immediate plans, not private cognition.",
            "Matching execution is not evidence that the statement caused the action.",
            "A plan may have been fixed initially; sequence alone does not establish adaptation.",
            "Public claims can be wrong; validation checks provenance, not scientific truth.",
            "No-window sessions remain unassessed for this cycle, not classified as nonlearning.",
            "Independent coding/adjudication remains unfinished.",
        ],
    }
    if not pending:
        column_counts = [("all", len(expected), len(complete_sessions))] + [
            (system, values["planned_windows"], values["sessions_all_available_windows_coded"])
            for system, values in sorted(coverage.items())
        ]
        result["descriptive_code_counts"] = {
            "action_links": dict(Counter(r["action_link"] for r in verified)),
            "public_update_types_overlapping": dict(
                Counter(label for r in verified for label in r["update_types"])
            ),
        }
        result["descriptive_by_system"] = {}
        for system in ("all", *sorted(coverage)):
            group = [
                r
                for r in verified
                if system == "all" or sessions[r["repeat"], r["id"]]["system"] == system
            ]
            session_keys = {(r["repeat"], r["id"]) for r in group}
            counts = {"windows": len(group), "sessions_with_windows": len(session_keys)}
            for field, labels in (("action_link", LINKS), ("update_types", UPDATES)):
                counts[field] = {}
                for label in sorted(labels):
                    selected = [
                        r
                        for r in group
                        if (r[field] == label if field == "action_link" else label in r[field])
                    ]
                    counts[field][label] = {
                        "windows": len(selected),
                        "sessions_at_least_once": len({(r["repeat"], r["id"]) for r in selected}),
                    }
            result["descriptive_by_system"][system] = counts
    (output / "semantic_analysis.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# 全队列研究反馈窗口的语义分析",
        "",
        f"已编码 {len(verified)}/{len(expected)} 个预先列出的结构窗口，"
        f"逐字核对 {result['verified_quotes']} 条指定版本引文。",
        "标注来自单一分析者，尚未独立复核。"
        if not pending
        else "全部窗口完成前不报告各语义标签的总体分布。标注来自单一分析者，尚未独立复核。",
        "",
        "匹配表示选定的公开计划与实际动作相符；初始既定设计与反馈调整在解释中分别说明。",
        "更新类型表示研究者公开作出了怎样的判断，不等于关系已被科学证实。",
        "",
        "## 覆盖进度",
        "",
        "| 体系 | 全部会话 | 已编码/计划窗口 | 有窗口且全部编码的会话 | 无完整观察窗口的会话 |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for system, counts in coverage.items():
        lines.append(
            f"| {system} | {counts['sessions']} | "
            f"{counts['coded_windows']}/{counts['planned_windows']} | "
            f"{counts['sessions_all_available_windows_coded']} | "
            f"{counts['sessions_without_observable_complete_window']} |"
        )
    if not pending:
        lines += [
            "",
            "## 完整覆盖后的描述性计数",
            "",
            "会话列表示至少有一个该标签窗口的会话数，分母仅为具有窗口的会话；",
            f"{len(no_window_sessions)}场无窗口会话单独保留。"
            f"窗口嵌套于会话，不能作为{len(expected)}个独立样本。",
            "公开更新标签允许重叠；同一会话也可有不同执行标签，因此会话列不可相加。",
            "matched仅评估所选即时计划；不表示新发现、反馈导致行动或计划的全部内容均执行。",
            "",
            "| 标签 | "
            + " | ".join(
                f"{system}窗口 /{windows} | {system}会话 /{sessions}"
                for system, windows, sessions in column_counts
            )
            + " |",
            "| --- | " + " | ".join(["---:"] * (2 * (1 + len(coverage)))) + " |",
        ]
        for field, labels in (("action_link", LINKS), ("update_types", UPDATES)):
            for label in sorted(labels):
                values = []
                for system in ("all", *sorted(coverage)):
                    count = (
                        result["descriptive_by_system"]
                        .get(system, {})
                        .get(field, {})
                        .get(label, {})
                    )
                    values += [
                        str(count.get("windows", 0)),
                        str(count.get("sessions_at_least_once", 0)),
                    ]
                lines.append(f"| {field}: {label} | " + " | ".join(values) + " |")
        synthesis = "SYNTHESIS.md" if (output / "SYNTHESIS.md").exists() else "REVIEW.md"
        lines += ["", f"完整解释见[研究过程综合分析]({synthesis})。"]
    lines += [
        "",
        "## 已完成窗口",
        "",
        "| 会话与版本 | 公开更新 | 计划执行 | 解释 |",
        "| --- | --- | --- | --- |",
    ]
    for r in verified:
        name = f"{r['repeat']}/{r['id']}"
        labels = ", ".join(r["update_types"])
        explanation = r["interpretation"].replace("|", "\\|")
        lines.append(
            f"| [{name}](sessions/{name}.json) v{r['from_revision']}→v{r['to_revision']} | "
            f"{labels} | {r['action_link']} | {explanation} |"
        )
    lines += ["", "## 未完成窗口", ""]
    if not pending:
        lines += ["无；105个窗口均有逐版本引文、证据与执行时序检查。"]
    for repeat, name, revision in pending:
        lines.append(f"- {repeat}/{name}: v{revision}→v{revision + 1}")
    lines += ["", "## 无完整观察窗口的会话", ""]
    for repeat, name in no_window_sessions:
        lines.append(f"- {repeat}/{name}：不满足连续时序覆盖，不据此判断是否学习。")
    lines += ["", *[f"- {text}" for text in result["limitations"]], ""]
    (output / "SEMANTIC_ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = build(args.output)
    fields = ("complete", "planned_windows", "coded_windows", "verified_quotes")
    print(json.dumps({key: result[key] for key in fields}))
    if args.require_complete and not result["complete"]:
        raise SystemExit("Semantic coverage is incomplete")


if __name__ == "__main__":
    main()
