"""Maintain live exports, then analyze and publish W2-251 after both fixed blocks end."""

# ruff: noqa: RUF001 -- Chinese research summaries.
from __future__ import annotations

import argparse
import re
import shutil
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.analyze_research_formation import num
from scripts.finish_research_formation import git
from scripts.plot_research_formation import plot
from scripts.report_research_extension import build
from scripts.run_paper_case_notebooks import ROOT, emit, read, write
from scripts.run_research_extension import NOTE

REPORT = "workstreams/flagship_tasks/reports/research-extension-20261014"
FIRST = "workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md"
TODO = "workstreams/flagship_tasks/WORK_II_TODOLIST.md"
MATRIX = "workstreams/flagship_tasks/WORK_II_EXPERIMENT_MATRIX.md"


def validate(root, destination, analysis):
    design = read(root / "design.json")
    if analysis["counts"]["terminal_sources"] != 90:
        raise ValueError("All 90 retained and added slots must have terminal dispositions")
    parent = Path(design["parent_root"])
    for source, units in ((parent, design["parent_schedule"]), (root, design["schedule"])):
        for unit in units:
            raw = read(source / unit["repeat"] / "results" / f"{unit['id']}.json")
            exported = read(destination / unit["repeat"] / f"{unit['id']}.json")
            original_source = raw.get("source", raw)
            if (
                exported["status"] != raw["status"]
                or exported["completed_batches"] != len(original_source.get("batches", []))
                or exported["prediction_evaluation"] != raw.get("prediction_evaluation")
            ):
                raise ValueError(f"Export changed retained outcome: {unit['repeat']}/{unit['id']}")
    q = analysis["quench"]
    if q["completed_trajectories"] != 180 or q["completed_pairs"] != 90 or q["block_stop"]:
        raise ValueError("Quench block has not completed all predeclared pairs")
    patterns = (
        r"\bsk-[A-Za-z0-9_-]{20,}",
        r"(?i)Bearer\s+[A-Za-z0-9_.-]{20,}",
        r'"(?:access_token|refresh_token|id_token|api_key)"\s*:\s*"[^"\s]+"',
    )
    for path in destination.rglob("*"):
        if path.suffix in {".md", ".json"}:
            content = path.read_text(encoding="utf-8")
            if any(re.search(pattern, content) for pattern in patterns):
                raise ValueError(f"Possible credential; export withheld: {path.name}")


def review(analysis, output):
    n, new, q = analysis["counts"], analysis["cohorts"]["extension_42"], analysis["quench"]
    lines = [
        "# 覆盖扩展与匹配淬灭：完成结果",
        "",
        f"新增 {new['terminal_sources']}/42 场结束，{new['complete_chains']} 条完整链；"
        f"源批次 {new['completed_batches']}/504、封存阶段 {new['sealed_posttests']}/141。"
        f"与既有 48 场合计 {n['terminal_sources']}/90 场、{n['complete_chains']} 条完整链。",
        "原四条后测失败继续保留；新增失败不替换。没有受控模型 RNG seed，也未更换模型。",
        "",
        "## 覆盖扩展",
        "",
        "下表为五世界等权描述均值；个体值、有效分母和样本 SD 见完整分析。"
        "新加入的信息臂和原信息臂并非同时执行，因此这些差异包含时期/提供方漂移的可能影响。",
        "",
        "| 响应 | Opaque | Aligned | MisIndexed |",
        "| --- | ---: | ---: | ---: |",
    ]
    for system, metric, label in (
        ("EQ", "lowest_three_macro_mae", "平衡最低浓度三题 MAE"),
        ("EQ", "remaining_nine_macro_mae", "平衡其余九题 MAE"),
        ("EQ", "lowest_three_coverage80", "平衡最低三题区间覆盖"),
        ("C", "crystal_purity_mae", "结晶纯度 MAE"),
        ("C", "crystal_yield_mae", "结晶回收 MAE"),
        ("C", "crystal_fines_fraction_mae", "结晶细粉 MAE"),
        ("C", "recommendation_quality_and_yield_target", "结晶推荐质量与回收同时达标比例"),
    ):
        means = analysis["world_contrasts"][system][metric]["equal_world_means"]
        lines.append(
            f"| {label} | "
            + " | ".join(num(means[a]["mean"]) for a in ("Opaque", "Aligned", "MisIndexed"))
            + " |"
        )
    lines += [
        "",
        "新增覆盖回答结果是否依赖世界与信息条件，不自动建立某一统一的认识形成机制。"
        "全部笔记、动作与分阶段报告均导出；本自动汇总没有把新增文本冒充逐句人工精读。",
        "",
        "## 匹配淬灭",
        "",
        f"完成 {q['completed_trajectories']}/180 条轨迹、{q['completed_pairs']}/90 对，"
        f"有效成对测量 {q['valid_pairs']}/90。失败执行保留，缺测不填零。",
    ]
    for key, label in (("original_world", "18 条原推荐在原世界"), ("all_worlds", "五世界交叉")):
        g = q[key]
        lines += [
            "",
            f"{label}：有效 {g['valid_pairs']} 对；无淬灭达到质量与回收 "
            f"{g['quality_and_recovery']['absent']}，有淬灭 "
            f"{g['quality_and_recovery']['present']}；细粉因淬灭增加 "
            f"{g['fines_higher_with_quench']} 对、减少 {g['fines_lower_with_quench']} 对。"
            f"平均细粉变化 {num(g['mean_present_minus_absent']['crystal_fines_fraction'])}，"
            f"回收变化 {num(g['mean_present_minus_absent']['crystal_yield'])}（有−无）。",
        ]
    lines += [
        "",
        "这里固定了其余操作，可以讨论所测配方内淬灭操作的总效果。"
        "温度、反应停止、后续相态和资源后果仍是同一干预的组成部分，尚未被分别隔离。"
        "这些因果结果解释环境中的工艺差异，不能替代智能体判断形成的时间证据或因果证据。",
        f"缺测分为无淬灭臂失败 {q['endpoint_analysis']['failure_arm_counts'].get('absent', 0)} 条、"
        f"有淬灭臂失败 {q['endpoint_analysis']['failure_arm_counts'].get('present', 0)} 条。"
        "本批次分别涉及无颗粒可测、以及淬灭后原定冷却目标高于当前温度。"
        "因此后续可执行性也是操作干预的结果，以上数值只描述完整配对。",
        "",
        "[全部研究记录](REPORT.md)；[逐世界分层分析](ANALYSIS.md)；"
        "[每对淬灭数据与失败](QUENCH.md)。",
        "",
        "![EQ outcomes](figures/eq-individual-outcomes.png)",
        "",
        "![C outcomes](figures/c-individual-outcomes.png)",
        "",
        "![Matched quench outcomes](figures/quench-paired-outcomes.png)",
        "",
    ]
    (output / "REVIEW.md").write_text("\n".join(lines), encoding="utf-8")


def update_tracking(analysis):
    n, new, q = analysis["counts"], analysis["cohorts"]["extension_42"], analysis["quench"]
    today = datetime.now(timezone(timedelta(hours=8))).date().isoformat()
    replacements = {
        FIRST: (
            "Claim: Codex /root — W2-251",
            f"Claim: Codex /root — W2-251 — DONE（{today}）。"
            f"覆盖扩展 42/42 场到达终态，{new['complete_chains']} 条完整链、"
            f"{new['completed_batches']}/504 批、{new['sealed_posttests']}/141 后测；"
            f"与旧 48 场合计 90 场，失败全部保留。匹配淬灭 180/180 轨迹、"
            f"90/90 配对（有效 {q['valid_pairs']} 对），操作效果与 Agent 认识形成分开解释。"
            "模型 RNG seed 不可控。见[完成报告](../flagship_tasks/reports/"
            "research-extension-20261014/REVIEW.md)。未改稿或替换旧证据。",
        ),
        TODO: (
            "W2-251 DOING",
            f"W2-251 DONE ({today}), Claim: Codex /root. "
            f"All 42 extension sources terminal, {new['complete_chains']} full chains, "
            f"{new['completed_batches']}/504 batches and {new['sealed_posttests']}/141 stages. "
            f"Combined pool: 90 terminal / {n['complete_chains']} full chains. Quench: "
            f"180/180 trajectories, 90/90 pairs, {q['valid_pairs']} valid pairs; "
            "failures retained. "
            "[Analysis](reports/research-extension-20261014/REVIEW.md) keeps cohort differences, "
            "uncontrolled model RNG, individual outcomes and intervention limits explicit. "
            "No replacement, manuscript rewrite or claim of notebook benefit.",
        ),
    }
    for relative, (prefix, replacement) in replacements.items():
        path = ROOT / relative
        lines = path.read_text(encoding="utf-8").splitlines()
        index = next(i for i, line in enumerate(lines) if line.startswith(prefix))
        lines[index] = replacement
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path = ROOT / NOTE
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text + f"\n## Completion ({today})\n\n"
        f"42/42 new sources terminal; {new['complete_chains']} full chains, "
        f"{new['completed_batches']}/504 batches, {new['sealed_posttests']}/141 stages. "
        f"Quench: 180/180 trajectories, 90 pairs, {q['valid_pairs']} valid pairs. "
        "All failures retained. [Results](reports/research-extension-20261014/REVIEW.md).\n",
        encoding="utf-8",
    )
    path = ROOT / MATRIX
    text = path.read_text(encoding="utf-8")
    first, rest = text.split("\n", 1)
    path.write_text(
        first + f"\n\n{today} W2-251 已完成：旧 48 + 新 42 共 90 场到达终态，"
        f"完整链 {n['complete_chains']}；匹配淬灭 90 对已完成。"
        "[完成分析](reports/research-extension-20261014/REVIEW.md)区分新旧时期与全部失败。\n"
        + rest,
        encoding="utf-8",
    )


def publish(root, quench_root, reports, status):
    owned = (REPORT, FIRST, TODO, NOTE, MATRIX)
    if git("branch", "--show-current") != "main":
        raise RuntimeError("Publication needs main; results remain retained")
    for mode in ((), ("--cached",)):
        if git("diff", *mode, "--name-only", "--", *owned):
            raise RuntimeError("Concurrent edits in publication targets; preserve and report")
    git("pull", "--ff-only", "origin", "main")
    destination = ROOT / REPORT
    result = build(root, quench_root, destination)
    validate(root, destination, result)
    plot(destination / "analysis.json", destination / "figures")
    review(result, destination)
    update_tracking(result)
    git("diff", "--check")
    git("add", "--", *owned)
    git(
        "commit",
        "--only",
        "-m",
        "results: complete 90-session coverage and matched quench controls",
        "--",
        *owned,
    )
    git("push", "origin", "main")
    commit = git("rev-parse", "HEAD")
    for path in destination.rglob("*"):
        if path.is_file():
            target = reports / path.relative_to(destination)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    record = {
        "phase": "completed_and_pushed",
        "commit": commit,
        "counts": result["counts"],
        "extension": result["cohorts"]["extension_42"],
        "quench_valid_pairs": result["quench"]["valid_pairs"],
        "review": str(destination / "REVIEW.md"),
        "updated_epoch": time.time(),
    }
    write(status, record)
    emit(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--quench-root", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--status", type=Path, required=True)
    args = parser.parse_args()
    try:
        last_export = 0
        while True:
            state = read(args.root / "summary.json")
            qpath = args.quench_root / "summary.json"
            q = read(qpath) if qpath.exists() else {}
            elapsed = state.get("elapsed_s", 0)
            terminal = state["terminal_sources"]
            progress = {
                "phase": "running",
                "new_terminal_sources": state["terminal_sources"],
                "new_planned_sources": 42,
                "combined_terminal_sources": 48 + state["terminal_sources"],
                "new_batches": state["completed_batches"],
                "active": state["active_units"],
                "quench_trajectories": q.get("completed_trajectories", 0),
                "elapsed_s": elapsed,
                "terminal_sources_per_hour": terminal * 3600 / elapsed if elapsed else None,
                "rough_remaining_s": elapsed * (42 - terminal) / terminal if terminal else None,
                "eta_basis": "Elapsed/terminal-chain rate; early estimate includes pipeline fill.",
                "updated_epoch": time.time(),
            }
            write(args.status, progress)
            emit(progress)
            if (state.get("block_stop") and not state["active_units"]) or q.get("block_stop"):
                raise RuntimeError(
                    "A fixed block stopped; preserve all outputs without replacement"
                )
            if (
                state["terminal_sources"] == 42
                and not state["active_units"]
                and q.get("completed_trajectories") == 180
            ):
                break
            if time.monotonic() - last_export >= 300:
                build(args.root, args.quench_root, args.reports)
                last_export = time.monotonic()
            time.sleep(30)
        publish(args.root, args.quench_root, args.reports, args.status)
    except Exception as exc:
        write(
            args.status,
            {
                "phase": "completion_needs_attention",
                "type": type(exc).__name__,
                "reason": str(exc),
                "updated_epoch": time.time(),
                "raw_results_retained": True,
            },
        )
        emit(
            {"phase": "completion_needs_attention", "type": type(exc).__name__, "reason": str(exc)}
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
