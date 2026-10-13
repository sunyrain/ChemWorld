"""Wait for W2-249, export/analyze all 48 results, and publish the authorized report."""

# ruff: noqa: RUF001 -- Chinese research review.
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import time
from datetime import date
from pathlib import Path

from scripts.analyze_research_formation import analyze, num
from scripts.plot_research_formation import plot
from scripts.report_research_formation import build
from scripts.run_paper_case_notebooks import ROOT, emit, read, write

REPORT_REL = "workstreams/flagship_tasks/reports/research-formation-20261013"
NOTE_REL = "workstreams/flagship_tasks/WORK_II_RESEARCH_FORMATION_20261013.md"
TODO_REL = "workstreams/flagship_tasks/WORK_II_TODOLIST.md"
FIRST_REL = "workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md"


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=True,
    )
    if result.stdout.strip():
        emit({"git": args[0], "output": result.stdout.strip()})
    return result.stdout.strip()


def validate_exports(root, destination, analysis):
    design = read(root / "design.json")
    expected = {(u["repeat"], u["id"]) for u in design["schedule"]}
    actual = {(r["repeat"], r["id"]) for r in analysis["cases"]}
    if len(expected) != 48 or actual != expected or analysis["counts"]["terminal_sources"] != 48:
        raise ValueError("The final export must retain every one of the 48 planned slots")
    for unit in design["schedule"]:
        raw = read(root / unit["repeat"] / "results" / f"{unit['id']}.json")
        exported = read(destination / unit["repeat"] / f"{unit['id']}.json")
        source = raw.get("source", raw)
        if exported["completed_batches"] != len(source.get("batches", [])):
            raise ValueError(f"Changed source denominator: {unit['id']}")
        if exported["status"] != raw["status"]:
            raise ValueError(f"Changed terminal outcome: {unit['id']}")
        if exported["prediction_evaluation"] != raw.get("prediction_evaluation"):
            raise ValueError(f"Changed prediction evaluation: {unit['id']}")
        if source.get("operations", 0) and not (source.get("exact_replay") or {}).get("verified"):
            raise ValueError(f"Retained replay defect needs explicit review: {unit['id']}")
    # Check exported text only; never print a matched credential or provider response.
    patterns = (
        r"\bsk-[A-Za-z0-9_-]{20,}",
        r"(?i)Bearer\s+[A-Za-z0-9_.-]{20,}",
        r'"(?:access_token|refresh_token|id_token|api_key)"\s*:\s*"[^"\s]+"',
    )
    for path in destination.rglob("*"):
        if path.suffix not in {".json", ".md"}:
            continue
        content = path.read_text(encoding="utf-8")
        if any(re.search(pattern, content) for pattern in patterns):
            raise ValueError(f"Possible credential in export; withheld: {path.name}")


def review(analysis, output):
    counts = analysis["counts"]
    contrasts = analysis["world_contrasts"]
    rows = {(r["repeat"], r["id"]): r for r in analysis["cases"]}

    def means(system, metric):
        result = contrasts[system][metric]
        return tuple(result["equal_world_means"][arm]["mean"] for arm in ("Opaque", "Aligned"))

    def contrast_line(system, metric, label):
        opaque, aligned = means(system, metric)
        result = contrasts[system][metric]
        return (
            f"{label}：Opaque **{num(opaque)}**，Aligned **{num(aligned)}**；"
            f"按世界均值，Aligned 较低/相同/较高为 "
            f"{result['aligned_lower_worlds']}/{result['equal_worlds']}/"
            f"{result['aligned_higher_worlds']} 个世界。"
        )

    dilute_o, dilute_a = means("EQ", "lowest_three_macro_mae")
    ratio = (
        dilute_a / dilute_o
        if dilute_o is not None and dilute_o > 0 and dilute_a is not None
        else None
    )
    note_o = rows[("repeat-01", "EQ-W01-Opaque")]["measurements"].get("lowest_three_macro_mae")
    note_a = rows[("repeat-01", "EQ-W01-Aligned")]["measurements"].get("lowest_three_macro_mae")
    near_o, near_a = means("EQ", "remaining_nine_macro_mae")
    gap_o = (
        dilute_o / near_o if near_o is not None and near_o > 0 and dilute_o is not None else None
    )
    gap_a = (
        dilute_a / near_a if near_a is not None and near_a > 0 and dilute_a is not None else None
    )
    c = [r for r in analysis["cases"] if r["system"] == "C"]
    eq = [r for r in analysis["cases"] if r["system"] == "EQ"]
    finite_minima = [r["measurements"].get("sampled_below_1mM") for r in eq]
    sampled = sum(x == 1 for x in finite_minima)
    measured = sum(x is not None for x in finite_minima)
    feasible = [r["measurements"].get("recommendation_quality_feasible") for r in c]
    targets = [r["measurements"].get("recommendation_quality_and_yield_target") for r in c]
    negative_bias = [r["measurements"].get("purity_signed_error") for r in c]
    eq_variability = [
        analysis["condition_variability"][r["id"]]["lowest_three_macro_mae"]
        for r in eq
        if r["repeat"] == "repeat-01"
    ]
    valid_sd = [v["sample_sd"] for v in eq_variability if v["sample_sd"] is not None]
    lines = [
        "# 48 场同期笔记研究：结果与解释",
        "",
        "**中途预览，尚非最终结论。**" if analysis["provisional"] else "固定队列已全部结束。",
        "",
        f"本块 **{counts['terminal_sources']}/48 场到达终态，"
        f"{counts['complete_chains']}/48 条完整链，"
        f"{counts['completed_source_batches']}/576 个源批次，"
        f"{counts['sealed_stages']}/174 个有效封存阶段**。全部失败保留，没有按结果补跑。",
        "",
        "研究对象为同一个 Sol medium 在固定世界中自主选择实验、记录判断并完成后测。"
        "EQ 覆盖五世界 × 两信息条件 × 三次会话；结晶覆盖预先选定的 W01/W03/W05 × 两条件 × 三次。"
        "这是一块独立的当前核心证据，不混入旧稿 300 场或此前 24 场笔记案例。",
        "",
        "## 主要定量结果",
        "",
        f"**平衡的适用域差异：**最低浓度三题的平均误差为其余九题的 "
        f"**{num(gap_o)} 倍（Opaque） / {num(gap_a)} 倍（Aligned）**。"
        "这两个量同样来自封存预测，但对应不同干预范围；是否存在有依据的可迁移关系，"
        "需要结合来源证据和公开判断核对，而不能由单一总分回答。",
        "",
        contrast_line("EQ", "lowest_three_macro_mae", "平衡最低浓度三题 MAE"),
        "",
        contrast_line("EQ", "remaining_nine_macro_mae", "平衡其余九题 MAE"),
        "",
        f"本块最低浓度三题的 A/O 误差比为 **{num(ratio)}**。这是本块世界等权的描述性比值，"
        "不能直接当作原稿 8.7 倍效应的同版本复验，也不能把跨版本变化归因于笔记。"
        "当前核心、记录职责及全新服务端轨迹均须保留为比较边界。",
        "",
        contrast_line("EQ", "lowest_three_coverage80", "平衡最低浓度三题区间覆盖率"),
        "",
        "区间覆盖与区间宽度一起解释，逐响应宽度见完整表；覆盖率来自固定查询与参考观测，"
        "不当作独立样本上的总体校准率。",
        "",
        f"30 场平衡中，进入既定 1 mM 以下区域的是 **{sampled}/{measured}** 场，"
        f"另有 {30 - measured} 场无可用浓度记录。阈值是已有描述性分组，不是科学能力门槛；"
        "未直接进入某一区域不等于没有理论依据，准确外推也不自动证明本次研究形成了该知识。",
        "",
        contrast_line("C", "crystal_purity_mae", "结晶纯度 MAE"),
        "",
        contrast_line("C", "crystal_yield_mae", "结晶回收率 MAE"),
        "",
        contrast_line("C", "crystal_fines_fraction_mae", "结晶细粉比例 MAE"),
        "",
        f"结晶纯度平均有符号误差为负的会话 **{sum(v is not None and v < 0 for v in negative_bias)}/"
        f"{sum(v is not None for v in negative_bias)}**；这是低估方向的描述，误差量级和逐世界分布"
        "见详细表。不能只凭方向将轻微偏差、明显偏差与同一形成机制等同起来。",
        "",
        f"推荐独立复测满足纯度与细粉质量条件 **{sum(v == 1 for v in feasible)}/"
        f"{sum(v is not None for v in feasible)}**；同时达到回收率 ≥0.10 的 **"
        f"{sum(v == 1 for v in targets)}/{sum(v is not None for v in targets)}**，"
        f"缺失复测 {sum(v is None for v in feasible)} 场。质量与有效回收必须分别报告。",
        "",
        "## 重复性怎样理解",
        "",
        "每个世界/信息条件只有三次会话，逐次点图和均值 ± 样本 SD 同时保留。"
        "世界差异与同世界会话波动分开呈现；没有使用题目数膨胀样本量，也没有提供可靠总体成功率"
        "或预先不存在的显著性结论。模型端无可控 RNG seed，不能称作严格相同模型随机种子复现。",
        "",
        f"EQ 十个条件中可计算的最低浓度误差样本 SD 范围为 "
        f"**{num(min(valid_sd) if valid_sd else None)}–{num(max(valid_sd) if valid_sd else None)}**"
        f"（{len(valid_sd)}/10 条件）；每格三次的数值与缺失数见 [定量分析](ANALYSIS.md)。"
        "一次轨迹中出现的解释、探索深度或反例不作为模型固定倾向。",
        "",
        "![EQ individual outcomes](figures/eq-individual-outcomes.png)",
        "",
        "![C individual outcomes](figures/c-individual-outcomes.png)",
        "",
        "每个点是一条会话；圆、方、三角分别为重复 1、2、3。横轴为世界，颜色为信息条件；"
        "缺失值不补零。源研究与推荐复测、后测分别计数。",
        "",
        "## 笔记实际补充了什么",
        "",
        f"保留 **{counts['notebook_versions']} 版笔记**，初始记录早于物理操作 "
        f"{counts['initial_notes_before_actions']}/48；在完成第 1–11 批之间有版本更新的会话 "
        f"{counts['sessions_with_mid_source_revision']}/48；"
        f"主动读取 {counts['notebook_reads']} 次。"
        "这些是记录覆盖情况，不是科学质量评分。若只有开始与结束两版，只能定位公开判断的"
        "前后差异，不能声称记录了中途每一步认识变化。",
        "",
        "下面四条是本轮分析中逐段阅读并核对成功执行记录的首轮案例，选择目的是说明不同过程，"
        "不据此估计发生频率。其余 44 场保留完整模型原文和定量结果，未冒充已经逐句人工编码。",
        "",
        "**局部研究形成了有范围的描述，但这与未见条件预测仍是两项不同的结果。** "
        "首轮 EQ-W01/Opaque 在操作前提出浓度控制与弱酸趋势，完成 0.0625–2 M 的矩阵后，"
        "把强方向性主张改为限定在该区域的近平台描述，同时保留替代解释和测量噪声。"
        f"其最低浓度三题 MAE 为 {num(note_o)}。"
        "笔记明确写出了范围，不能把后测误差改写为它已经宣称平台普遍成立。"
        "这条轨迹揭示的是公开描述、证据范围与具体预测需要分别核对。"
        "[笔记](repeat-01/EQ-W01-Opaque-notebook.md) / "
        "[后测](repeat-01/EQ-W01-Opaque-reports.md)。",
        "",
        "**先验可以成为被实际检验的局部命题。** 首轮 EQ-W01/Aligned 先记录档案中 "
        "0.001 mol、0.018→0.054 L 的预期，再按该对比操作；两批最终读数的 pH_normalized "
        "变化约 +0.00444、解离率变化约 +0.01230。笔记将其称为局部相容，并未排除相关校准"
        "或其他响应面的解释。"
        f"与此同时，该场最低浓度三题 MAE 为 {num(note_a)}。"
        "这里可以连接先前表述、实际检验与后来的适用范围；尚不能据时序证明这份表述造成了"
        "全部后续决策。 [笔记](repeat-01/EQ-W01-Aligned-notebook.md)。",
        "",
        "**一次反向结果与随后收缩的公开判断。** 首轮 C-W03/Aligned 的第 11 批用 "
        "0.020 mol 得到细粉约 0.591、回收约 0.492；第 12 批进一步降至 0.010 mol 后，"
        "细粉升至约 0.846、回收降至约 0.402。最终笔记明确撤回单调改善的概括，把内点最优"
        "保留为待检验可能，并承认所有批次均未合格。该轨迹提供一种有同期依据的范围收缩；"
        "一次、部分混杂的对比并未建立普遍机理。 [笔记](repeat-01/C-W03-Aligned-notebook.md)。",
        "",
        "**失败目标也可以被如实保留。** 首轮 C-W01/Opaque 原先预计极稀条件可能同时降低"
        "细粉并保留 >0.10 回收；第 12 批公共读数的细粉约 0.002、回收仅约 0.003。"
        "最终笔记只保留质量改善，明确没有得到满意回收。其独立复测的无噪真实回收为零，"
        "与接近零的带噪公共读数分别呈现。不能将这个条件写成完整成功，也不能忽略研究者"
        "实际承认了未达目标。 [笔记](repeat-01/C-W01-Opaque-notebook.md)。",
        "",
        "## 对论文主线的含义",
        "",
        "本块将可核对的对象从最终分数推进到：一个公开判断提出时掌握哪些信息，实验实际"
        "支持了什么范围，以及它随后如何被保留、修订和用于回答。数据同时包含正确的范围限定、"
        "未定解释、局部验证和外推偏差，适合支撑对自主科研中认识形成的研究。",
        "",
        "不能把所有预测错误统一命名为研究过程中形成的误认，也不能预设自我确认循环。"
        "特别是已有明确边界声明的案例，后测出错并不直接证明模型认为自己建立了普遍规律。"
        "本块没有受控早期历史分支、无笔记对照或强制纠错条件，因此不承担这些干预的因果结论。"
        "形成机制的具体归因仍需对应证据，而不是由故事结构提前指定。",
        "",
        "## 完整性与可复核性",
        "",
        f"源轨迹回放 {counts['source_replays']}/48；参考 336 批、28 条回放；"
        f"推荐复测 {counts['retest_batches']} 批；源操作 {counts['source_operations']}，"
        f"回滚 {counts['source_rollbacks']}。有效 Q {counts['valid_Q']}/48，"
        f"不完整链 {48 - counts['complete_chains']} 条，逐条原因见定量表与 JSON。",
        "",
        "主文未在此自动重写。数据生产阶段的设计、世界、预算和停止规则保持不变；本次增加的"
        "纯度有符号误差和记录时点汇总明确属于事后描述分析。原始 provider 数据和凭证留在"
        "仓库外，Git 中只保留科学导出、分析代码、图表和说明。",
        "",
        "- [全部 48 场笔记与后测索引](REPORT.md)",
        "- [完整分层定量表](ANALYSIS.md)",
        "- [机器分析结果](analysis.json)",
        "- [固定实验说明](../../WORK_II_RESEARCH_FORMATION_20261013.md)",
        "",
    ]
    (output / "REVIEW.md").write_text("\n".join(lines), encoding="utf-8")


def update_tracking(analysis):
    n = analysis["counts"]
    completed_date = date.today().isoformat()
    path = ROOT / TODO_REL
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("W2-249 DOING"))
    lines[index] = (
        f"W2-249 DONE ({completed_date}), Claim: Codex /root. "
        "Completed the authorized 48-session current-core EQ/C notebook block: "
        f"48 terminal sources, {n['complete_chains']} complete chains, "
        f"{n['completed_source_batches']}/576 source batches, "
        f"{n['sealed_stages']}/174 sealed stages, "
        f"{n['notebook_versions']} notebook versions; all failures retained without replacements. "
        "Shared references: 336 batches / 28 replayed trajectories. "
        "World-stratified O/A contrasts, "
        "three-repeat variability, individual plots and four explicitly selected retrospective "
        "process readings are in the [review](reports/research-formation-20261013/REVIEW.md). "
        "No notebook-benefit causal claim, model expansion or manuscript rewrite. "
        "Raw provider data and credentials remain outside Git; execution source stays 68dce156."
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path = ROOT / FIRST_REL
    lines = path.read_text(encoding="utf-8").splitlines()
    index = next(
        i for i, line in enumerate(lines) if line.startswith("Claim: Codex /root — W2-249")
    )
    lines[index] = (
        f"Claim: Codex /root — W2-249 — DONE（{completed_date}）。48 场均到达终态，"
        f"{n['complete_chains']} 条完整链，{n['completed_source_batches']}/576 源批次、"
        f"{n['sealed_stages']}/174 后测、{n['notebook_versions']} 版笔记；"
        "四并发、失败保留且未补跑。"
        "按世界统计 Opaque/Aligned 差异与三次重复波动，导出全部笔记/后测及明确选例的过程解释。"
        "见 [完整结果分析](../flagship_tasks/reports/research-formation-20261013/REVIEW.md)。"
        "原始数据在仓库外，不替换历史结果、不改稿。"
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path = ROOT / NOTE_REL
    text = path.read_text(encoding="utf-8")
    text += (
        "\n## Completed analysis and publication\n\n"
        f"All 48 sources reached terminal dispositions: {n['complete_chains']} complete chains, "
        f"{n['completed_source_batches']}/576 source batches, "
        f"{n['sealed_stages']}/174 valid sealed "
        f"stages and {n['notebook_versions']} notebook versions. Failures are retained, with no "
        "replacement source. The user explicitly authorized analysis and main publication after "
        "completion. The final exporter checks all planned slots against the raw terminal statuses "
        "and prediction evaluations; runtime and source budgets were not modified.\n\n"
        "[Review and all records](reports/research-formation-20261013/REVIEW.md) include "
        "world-level comparisons and all individual repeats, resource/failure accounting, "
        "notebook timing, and four explicitly selected first-round process examples. Signed "
        "purity error and structural note timing are retrospective descriptive additions; "
        "no uncalibrated LLM judge or new scientific pass threshold was introduced. "
        "No manuscript or historical evidence was replaced.\n"
    )
    path.write_text(text, encoding="utf-8")


def finish(root, external_reports, status_path):
    owned = (REPORT_REL, NOTE_REL, TODO_REL, FIRST_REL)
    if git("branch", "--show-current") != "main":
        raise RuntimeError("Publication must use main; leave the active branch untouched")
    # Protect edits in the files we actually change; unrelated work is allowed.
    for mode in ((), ("--cached",)):
        if git("diff", *mode, "--name-only", "--", *owned):
            raise RuntimeError("Target documentation has concurrent edits; preserve them")
    git("pull", "--ff-only")
    destination = ROOT / REPORT_REL
    if destination.exists():
        raise RuntimeError(
            "Report destination already exists; do not overwrite another publication"
        )
    write(status_path, {"phase": "analyzing", "terminal_sources": 48})
    build(root, destination)
    result = analyze(root, destination, destination)
    plot(destination / "analysis.json", destination / "figures")
    review(result, destination)
    index = destination / "REPORT.md"
    index.write_text(
        index.read_text(encoding="utf-8")
        + "\nFinal interpretation: [REVIEW.md](REVIEW.md); "
        + "world-stratified statistics: [ANALYSIS.md](ANALYSIS.md).\n",
        encoding="utf-8",
    )
    validate_exports(root, destination, result)
    update_tracking(result)
    git("diff", "--check")
    git("add", "--", *owned)
    git(
        "commit",
        "--only",
        "-m",
        "results: analyze 48-session research formation notebook study",
        "--",
        *owned,
    )
    git("push", "origin", "main")
    commit = git("rev-parse", "HEAD")
    # The live observer only writes this external tree; terminal scientific data are immutable.
    for path in destination.rglob("*"):
        if path.is_file():
            target = external_reports / path.relative_to(destination)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    status = {
        "phase": "completed_and_pushed",
        "commit": commit,
        "counts": result["counts"],
        "review": str(destination / "REVIEW.md"),
        "completed_epoch": time.time(),
    }
    write(status_path, status)
    emit(status)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--status", type=Path, required=True)
    args = parser.parse_args()
    try:
        while True:
            state = read(args.root / "summary.json")
            progress = {
                "phase": "waiting_for_all_sources",
                "terminal_sources": state["terminal_sources"],
                "planned_sources": 48,
                "batches": state["completed_batches"],
                "active": len(state["active_units"]),
                "updated_epoch": time.time(),
            }
            write(args.status, progress)
            emit(progress)
            if state.get("block_stop") and not state["active_units"]:
                raise RuntimeError("Experiment stopped before completion; retain all outputs")
            if state["terminal_sources"] == 48 and not state["active_units"]:
                break
            time.sleep(30)
        finish(args.root, args.reports, args.status)
    except Exception as exc:
        status = {
            "phase": "failed_without_retry",
            "type": type(exc).__name__,
            "reason": str(exc),
            "updated_epoch": time.time(),
            "raw_results_retained": True,
        }
        write(args.status, status)
        emit(status)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
