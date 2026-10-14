"""Verify complete per-session notebook readings for the corrected C cohort."""

# ruff: noqa: RUF001
from __future__ import annotations

import argparse
from pathlib import Path

from scripts.run_paper_case_notebooks import emit, read, write


def build(reports, coding, *, require_complete=False):
    analysis = read(reports / "analysis.json")
    data = read(coding)
    cases = {(r["repeat"], r["id"]): r for r in analysis["cases"]}
    expected = set(cases)
    seen, verified = set(), []
    for record in data["records"]:
        key = record["repeat"], record["id"]
        if key not in expected or key in seen or cases[key]["status"] == "pending":
            raise ValueError(f"Duplicate, pending or out-of-scope reading: {key}")
        seen.add(key)
        source = read(reports / "sessions" / key[0] / f"{key[1]}.json")
        versions = {v["revision"]: v for v in source["versions"]}
        if record["versions_read"] != len(versions):
            raise ValueError(f"Notebook version coverage differs: {key}")
        if versions and not record["quotes"]:
            raise ValueError(f"Reading lacks a version-specific quotation: {key}")
        for quote in record["quotes"]:
            if not quote["text"] or quote["text"] not in versions[quote["revision"]]["text"]:
                raise ValueError(f"Unverified quotation: {key}")
        events = {e["cursor"]: e for e in source["events"]}
        for anchor in record.get("action_checks", []):
            event = events[anchor["cursor"]]
            if (event["batch"], event["transaction_status"]) != (
                anchor["batch"],
                anchor["status"],
            ) or any(event["action"].get(k) != v for k, v in anchor["action"].items()):
                raise ValueError(f"Unverified execution anchor: {key}, {anchor}")
        verified.append(
            {
                **record,
                "status": cases[key]["status"],
                "quotations_verified": True,
                "independently_reviewed": False,
            }
        )
    result = {
        "scope": data["scope"],
        "planned_sessions": len(expected),
        "read_sessions": len(seen),
        "complete": seen == expected,
        "read_versions": sum(r["versions_read"] for r in verified),
        "verified_quotes": sum(len(r["quotes"]) for r in verified),
        "verified_action_anchors": sum(len(r.get("action_checks", [])) for r in verified),
        "pending": sorted(expected - seen),
        "records": verified,
    }
    write(reports / "case_readings_verified.json", result)
    lines = [
        "# 修正回收定义队列：逐场笔记精读",
        "",
        f"已读 {len(seen)}/{len(expected)} 场，{result['read_versions']} 版笔记；"
        f"核对 {result['verified_quotes']} 条逐版本引文及"
        f"{result['verified_action_anchors']} 个指定执行锚点。",
        "单分析者回溯精读，非盲且尚无独立复核。引文核对确认来源，不等于确认科学解释正确。"
        "后测指标见[完整定量报告](REPORT.md)；不宣称所有后测全文均做了独立人工审查。",
        "",
    ]
    for record in verified:
        key = f"{record['repeat']}/{record['id']}"
        lines += [
            f"## {key}",
            "",
            f"状态：{record['status']}；"
            f"[笔记全文]({key}-notebook.md) / [后测]({key}-reports.md) / "
            f"[执行时序](sessions/{key}.json)。",
            "",
            record["reading"],
            "",
        ]
        for quote in record["quotes"]:
            lines += [f"v{quote['revision']}：", "", f"> {quote['text']}", ""]
        if record.get("action_checks"):
            lines += [
                "执行锚点：" + ", ".join(str(a["cursor"]) for a in record["action_checks"]) + "。",
                "",
            ]
    if result["pending"]:
        lines += ["## 待精读", "", *[f"- {r}/{i}" for r, i in result["pending"]], ""]
    (reports / "CASE_READINGS.md").write_text("\n".join(lines), encoding="utf-8")
    if require_complete and not result["complete"]:
        raise ValueError("Per-session reading is incomplete")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports", required=True, type=Path)
    parser.add_argument("--coding", required=True, type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = build(args.reports, args.coding, require_complete=args.require_complete)
    emit({k: v for k, v in result.items() if k not in ("records", "pending", "scope")})


if __name__ == "__main__":
    main()
