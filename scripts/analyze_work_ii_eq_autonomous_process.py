# ruff: noqa: RUF001
"""Review retained EQ/P source -> K1 -> Q -> K2 evidence, without new experiments.

The limited text labels below are an explicit, retrospective author annotation of
public answers, not a keyword classifier or a measure of private reasoning.
Existing source and trajectory indexes select the cohort. Original Q scores are
recomputed by the existing retained-data scorer, including all three responses.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from statistics import fmean

from scripts.analyze_work_ii_story_candidates import eq_regime_checks

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / (
    "workstreams/flagship_tasks/reports/work-ii-eq-bounded-equilibrium-20260920/v2-public"
)
OUT = ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
STEM = "EQ_AUTONOMOUS_PROCESS"
ARMS = ("Opaque", "Aligned", "MisIndexed")
Q_LABELS = {
    "piecewise_weak_acid": "分段弱酸外推",
    "qualitative_departure": "允许脱离平台（定性）",
    "plateau_extension": "平台／弱趋势延拓",
    "competing_mixture": "弱酸与平台解释混合",
}
K2_LABELS = {
    "trace": "极稀条件",
    "scale": "等浓度放大",
    "local_dilution": "原资料附近的同容器稀释",
    "instrument_bridge": "同状态跨仪器比较",
    "replicate": "复测已有异常批次",
}
# IDs refer to the retained source sessions, not the retired fresh-reader block.
# Anchors identify exact paragraphs in the original K1; no report is rewritten.
REVIEW = {
    "EQ-W01--Opaque": (
        "piecewise_weak_acid",
        "trace",
        [
            "Applying this transformation separately",
            "C_active ≈ C_cap",
            "Behavior below 0.050 mol/L",
        ],
    ),
    "EQ-W01--Aligned": (
        "plateau_extension",
        "trace",
        ["The causal interpretation of g is not identified."],
    ),
    "EQ-W01--MisIndexed": (
        "plateau_extension",
        "trace",
        ["The empirical equations and pKa_eff estimate are supported only"],
    ),
    "EQ-W02--Opaque": (
        "piecewise_weak_acid",
        "trace",
        ["The present data favor a pH-coupled description", "**Unsupported extrapolation:**"],
    ),
    "EQ-W02--Aligned": (
        "plateau_extension",
        "trace",
        [
            "Using each final assay's pH and acid fraction",
            "Interpolation inside the tested box should favor",
        ],
    ),
    "EQ-W02--MisIndexed": (
        "plateau_extension",
        "trace",
        ["I would not extrapolate this model"],
    ),
    "EQ-W03--Opaque": (
        "piecewise_weak_acid",
        "trace",
        ["The clearest discriminating future tests"],
    ),
    "EQ-W03--Aligned": (
        "plateau_extension",
        "scale",
        ["My interpretation is therefore that the archival dilution relationship"],
    ),
    "EQ-W03--MisIndexed": (
        "competing_mixture",
        "trace",
        ["I would not extrapolate the constant-response model"],
    ),
    "EQ-W04--Opaque": (
        "qualitative_departure",
        "trace",
        ["Claims outside the tested concentration, volume"],
    ),
    "EQ-W04--Aligned": (
        "plateau_extension",
        "local_dilution",
        ["Regression forms above are descriptive interpolation summaries"],
    ),
    "EQ-W04--MisIndexed": (
        "plateau_extension",
        "instrument_bridge",
        ["The data justify the empirical plateau model for interpolation"],
    ),
    "EQ-W05--Opaque": (
        "piecewise_weak_acid",
        "trace",
        ["The conclusions apply only to water"],
    ),
    "EQ-W05--Aligned": (
        "plateau_extension",
        "trace",
        ["These are supported-range predictions"],
    ),
    "EQ-W05--MisIndexed": (
        "plateau_extension",
        "replicate",
        ["It is an empirical interpolation, not a chemical law"],
    ),
}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paragraph_at(text: str, anchor: str) -> str:
    matches = [p for p in text.split("\n\n") if anchor in p]
    if len(matches) != 1:
        raise ValueError(f"Expected one exact paragraph for {anchor!r}; found {len(matches)}")
    return matches[0]


def future_experiment(text: str) -> str:
    # Numbered action lists must not be mistaken for section 4 or section 5.
    start = re.search(r"(?mi)^(?:#+\s*)?4\. [^\n]*(?:experiment|choose)[^\n]*", text)
    end = re.search(r"(?mi)^(?:#+\s*)?5\. [^\n]*trade-?off[^\n]*", text)
    if start is None or end is None or end.start() <= start.start():
        raise ValueError("Cannot locate the original K2 future-experiment section")
    return text[start.start() : end.start()].strip()


def collect() -> dict:
    index = read(PUBLIC / "INDEX.json")
    trajectory_index = read(PUBLIC / "TRAJECTORY_INDEX.json")
    trajectory_rows = {r["cell_id"]: r for r in trajectory_index["cells"]}
    regimes = eq_regime_checks()
    scores = {r["id"]: r for r in regimes["cells"]}
    assert len(index["cells"]) == len(REVIEW) == len(scores) == 15
    assert set(REVIEW) == set(trajectory_rows) == set(scores)
    rows = []
    all_audits, all_actions = Counter(), Counter()
    missing_reasons = 0
    for cell in index["cells"]:
        cid = cell["cell_id"]
        path = PUBLIC / "sources" / cid / "RESULT.json"
        result = read(path)
        records = [
            json.loads(line)
            for line in (PUBLIC / trajectory_rows[cid]["public_path"])
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        assert len(records) == cell["operations"] == trajectory_rows[cid]["operations"]
        batches = result["source"]["batches"]
        assert len(batches) == 12
        for stage in ("K1", "Q", "K2"):
            assert result["posttests"][stage]["validation"]["valid"]
        actions = Counter()
        audits = Counter()
        for step in records:
            output = step["agent_output"]
            action = output["action"]
            actions[
                action["operation"]
                + (":" + action["instrument"] if action["operation"] == "measure" else "")
            ] += 1
            audit = output.get("decision_audit") or {}
            audits[audit.get("status", "missing")] += 1
            missing_reasons += int(
                audit.get("status") == "not_provided"
                and not audit.get("diagnostic_target")
                and not audit.get("expected_effect")
            )
        all_audits.update(audits)
        all_actions.update(actions)
        assert actions["measure:final_assay"] == len(batches)
        recipe_rows = []
        for batch in batches:
            ba = batch["actions"]
            amount = sum(a.get("amount_mol", 0) for a in ba if a["operation"] == "add_reagent")
            volume = sum(a.get("volume_L", 0) for a in ba if a["operation"] == "add_solvent")
            recipe_rows.append(
                {
                    "ordinal": batch["ordinal"],
                    "amount_mol": amount,
                    "volume_L": volume,
                    "nominal_concentration_mol_L": amount / volume,
                    "operations": ba,
                    "final_responses": {
                        k: batch["metrics"][k]
                        for k in (
                            "pH_normalized",
                            "acid_dissociation_fraction",
                            "precipitation_signal",
                        )
                    },
                }
            )
        q = result["posttests"]["Q"]["payload"]
        q08 = next(p for p in q["predictions"] if p["query_id"] == "Q08")
        q_code, k2_code, anchors = REVIEW[cid]
        scope_quotes = [
            paragraph_at(result["posttests"]["K1"]["payload"]["report"], a) for a in anchors
        ]
        scored = scores[cid]
        q08_points = [
            p for p in scored["groups"]["three_most_dilute"]["points"] if p["query"] == "Q08"
        ]
        alpha = q08["metrics"]["acid_dissociation_fraction"]
        rows.append(
            {
                "id": cid,
                "world": scored["world"],
                "arm": cell["arm"],
                "effective_origin": result["effective_origin"],
                "source_result": path.relative_to(ROOT).as_posix(),
                "trajectory": (PUBLIC / trajectory_rows[cid]["public_path"])
                .relative_to(ROOT)
                .as_posix(),
                "operation_count": len(records),
                "audit_statuses": dict(audits),
                "action_counts": dict(actions),
                "batches": recipe_rows,
                "source_concentration_range": scored["source_nominal_concentration_range"],
                "source_dissociation_range": scored["source_dissociation_range"],
                "source_dissociation_mean": fmean(
                    b["metrics"]["acid_dissociation_fraction"] for b in batches
                ),
                "scores": scored["groups"],
                "text_annotation": {
                    "kind": "retrospective_author_review_of_public_text",
                    "k1_exact_excerpts": scope_quotes,
                    "q_extrapolation_code": q_code,
                    "q_global_rationale": q["rationale"],
                    "q08_rationale": q08["rationale"],
                    "k2_future_choice_code": k2_code,
                    "k2_exact_future_section": future_experiment(
                        result["posttests"]["K2"]["payload"]["report"]
                    ),
                },
                "q08": {
                    "predictions": q08["metrics"],
                    "reference_means": {p["metric"]: p["truth_mean"] for p in q08_points},
                    "alpha_coverage": next(
                        p["coverage"]
                        for p in q08_points
                        if p["metric"] == "acid_dissociation_fraction"
                    ),
                    "alpha_interval": [alpha["lower80"], alpha["upper80"]],
                },
            }
        )
    maximum_dilute_c = max(regimes["query_concentrations"][q] for q in ("Q03", "Q08", "Q09"))
    return {
        "status": "completed_retained_data_review",
        "date": "2026-09-22",
        "new_provider_calls": 0,
        "new_simulator_calls": 0,
        "scope": "All 15 retained EQ/P autonomous campaigns; five shared-structure worlds.",
        "selection": (
            "Existing source and trajectory indexes; all three prior arms, no outcome filtering."
        ),
        "limitations": [
            "Source decision audit is not provided; K1 and K2 are retrospective public accounts.",
            "Q retains original context and can introduce new hypotheses after K1 sealing.",
            "K2 follows exposure to Q conditions; future choices are not executed "
            "or spontaneous source plans.",
            "Text labels are a bounded single-author retrospective review, "
            "not independent causal validation.",
            "Regime grouping is exploratory; trials, responses and noise replicates "
            "are not independent worlds.",
        ],
        "coverage": {
            "expected_sources": 15,
            "reviewed_sources": len(rows),
            "worlds": 5,
            "source_batches": sum(len(r["batches"]) for r in rows),
            "operations": sum(r["operation_count"] for r in rows),
            "canonical_posttests": 3 * len(rows),
            "analysis_failures": [],
            "missing_decision_reason_records": missing_reasons,
            "audit_statuses": dict(all_audits),
            "action_counts": dict(all_actions),
            "sources_wholly_above_three_dilute_queries": sum(
                r["source_concentration_range"][0] > maximum_dilute_c for r in rows
            ),
        },
        "annotation_counts": {
            arm: {
                "q_extrapolation": dict(
                    Counter(
                        r["text_annotation"]["q_extrapolation_code"]
                        for r in rows
                        if r["arm"] == arm
                    )
                ),
                "k2_future_choice": dict(
                    Counter(
                        r["text_annotation"]["k2_future_choice_code"]
                        for r in rows
                        if r["arm"] == arm
                    )
                ),
            }
            for arm in ARMS
        },
        "query_concentrations": regimes["query_concentrations"],
        "original_q_aggregate": regimes["aggregate"],
        "rows": rows,
    }


def render(data: dict) -> str:
    lines = [
        "# EQ/P：原自主研究的过程与结论核对",
        "",
        "2026-09-22。只分析保留数据，零新模型、模拟器或评审调用。"
        "覆盖全部 15 场有效来源、五世界三臂、180 批、945 步操作和 45 个 K1/Q/K2 阶段。"
        "原始恢复与历史失败沿用来源记录，不替换来源，也不将本次分析升级为正式证据。",
        "",
        "**核心发现：原自主研究的最终预测呈现不同的外推方式。五个 Opaque 会话都允许极稀条件"
        "离开已测平台，五个 Aligned 会话都主要延续平台或弱趋势；MisIndexed 有一个混合解释反例。"
        "这可把已有误差差异连接到公开表达的预测规则，但不能定位实验过程中哪个推理步骤导致差异。**",
        "",
        "本报告的单位是原 agent 完成的自主研究。固定记录的新会话读出已退出验证路径，"
        "其两次结果及资源继续保留，不混入下表，也不据此否定原研究。",
        "",
        "## 1. 范围与方法",
        "",
        "按已发布来源索引和轨迹索引纳入全部十五场；逐步计数操作与测量，按实际加料之和计算"
        "终态配方名义浓度，不将它冒充活性溶解浓度。Q03/Q08/Q09 沿用此前按公开配方浓度选择的"
        "最稀三题，其余九题不全是插值。所有 Q 分数对原五次参考观测复算，逐场加权复现原总 MAE。",
        "",
        "文本核对只编码两项有限问题：Q 公开解释采用何种低浓度外推；K2 选择什么下一实验。"
        "十五场均保留 K1 适用域摘录、Q 原解释、K2 对应原段落及原文件引用。这是单次作者探索性"
        "解释编码，不是词频自动归因，也不宣称完成全部 240 场的机理标注。"
        "类别允许定性偏离、混合解释和非稀释后续实验。",
        "",
        "完整阶段证据与数值见 [机器摘要](EQ_AUTONOMOUS_PROCESS.json)。"
        "读取现有 configs/current.json 后，当前 EQ/P 队列沿用现行矩阵指定的发布索引；"
        "不从旧注册表恢复历史实验，也不按版本名挑选有利结果。",
        "",
        "## 2. 实验实际覆盖了什么",
        "",
        "15/15 场的终态配方名义浓度均高于三道最稀题；最低为约 0.01852 mol/L，"
        "而三题分别约为 0.0001333、0.00001333、0.0001667 mol/L。"
        "这些研究没有直接测到目标极稀区间。参数跨度大不代表已经跨过响应转折。",
        "",
        "945/945 个决策 audit 状态都是 `not_provided`，诊断目标和预期效应字段为空。"
        "公开动作和观测可追溯，逐步的同期决策理由没有被提供。不能用这些占位字段重建认知更新，"
        "也不能把 K1/K2 的事后解释当作逐步决策记录；这不意味着原模型没有进行推理。",
        "",
        "## 3. 全部十五场：覆盖、预测规则和 Q08 数值",
        "",
        "Q08 是 1 μmol / 75 mL；下列解离分数、区间及参考均值均来自原自主会话。"
        "分类依据是封存 Q 的公开说明，含义仅限于可观察的外推方式。",
        "",
        "| 来源 | 已测名义浓度范围 mol/L | Q 外推方式 | Q08 解离预测 [80%区间] | 参考均值 |",
        "|---|---:|---|---:|---:|",
    ]
    for row in data["rows"]:
        alpha = row["q08"]["predictions"]["acid_dissociation_fraction"]
        lo, hi = row["source_concentration_range"]
        label = Q_LABELS[row["text_annotation"]["q_extrapolation_code"]]
        target = row["q08"]["reference_means"]["acid_dissociation_fraction"]
        lines.append(
            f"| {row['world']}/{row['arm']} | {lo:.5f}–{hi:.5f} | {label} | "
            f"{alpha['estimate']:.4f} [{alpha['lower80']:.4f}, {alpha['upper80']:.4f}] | "
            f"{target:.4f} |"
        )
    lines += [
        "",
        "Opaque 的 W01/W02/W03/W05 明确使用弱酸关系连接低浓度与高浓度平台；"
        "W04 给出脱离平台的定性外推，不强行归类为同一个定量机理。Aligned 五场虽然承认"
        "极稀条件的外推风险，数值仍接近平台。MisIndexed W03 使用弱酸与背景平台的混合解释，"
        "Q08 解离预测为 0.46，构成不能省略的反例；不能写成有资料必然维持平台。",
        "",
        "| 原自主研究分组 | Opaque MAE / 覆盖率 | Aligned MAE / 覆盖率 | MisIndexed MAE / 覆盖率 |",
        "|---|---:|---:|---:|",
    ]
    aggregates = {(r["arm"], r["group"]): r for r in data["original_q_aggregate"]}
    for group, label in (("three_most_dilute", "最稀三题"), ("other_nine", "其余九题")):
        vals = [aggregates[arm, group] for arm in ARMS]
        lines.append(
            "| "
            + label
            + " | "
            + " | ".join(f"{r['mae']:.5f} / {r['coverage']:.1%}" for r in vals)
            + " |"
        )
    lines += [
        "",
        "MAE 对原五次参考均值计算，三响应等权；覆盖率对全部参考观测计算。每臂稀释组"
        "为 5 世界 × 3 题 × 3 响应 × 5 观测 = 225 个覆盖判断，其余组为 675 个，"
        "这些判断不构成独立世界。分组是事后分析，五个世界共享底层结构，不能扩展为普遍化学规律。",
        "",
        "## 4. 哪些结论已经在 K1，哪些是在 Q 才具体化",
        "",
        "W01/Opaque 的 K1 已计算约 2.2×10⁻⁵ 的有效 Ka，以及约 0.004 mol/L 的活性池上限；"
        "同时承认缓冲、溶解限制和观测映射尚不能唯一辨别。Q 使用这个假设进一步计算低浓度解离。"
        "这一例存在可核对的 K1→Q 延续。",
        "",
        "W02/Opaque 的 K1 则主要支持 pH 调节平台和有效 pKa≈4.85，并明确限制域外外推。"
        "Q 才给出约 0.0026 mol/L 的溶解浓度上限并使用未饱和弱酸计算。"
        "因此只能说完整原会话在作答时形成了有效外推，不能把 Q 的全部成功记为 K1 已封存的发现。",
        "",
        "W02/Aligned 的 K1 同样得到局部有效 pKa≈4.84，且明确说不能把平坦响应外推到零加料。"
        "但 Q08 仍沿弱对数趋势给出解离分数 0.0804、区间 [0.053, 0.108]，参考约 0.6546。"
        "两臂在局部参数表述上的接近，没有带来相同的低浓度预测。这比“一个有知识、另一个没知识”"
        "更准确；尚不能证明先验通过锚定造成差异。",
        "",
        "所引用的 K1 均明确限制适用范围；有限文本核对显示，承认范围限制与把它落实到数值"
        "预测是不同的可观察表现。不能仅凭流畅的局限性陈述判断预测已校准。",
        "",
        "## 5. K2 提出的下一实验，保留为后测之后的判断",
        "",
        "11/15 场在 K2 选择极稀实验：Opaque 5/5、Aligned 3/5、MisIndexed 3/5。"
        "另外四场分别选择等浓度放大、原资料附近的同容器稀释、同状态跨仪器比较和复测异常批次。"
        "这些都是假设性建议，没有执行，也没有获得盲测真值反馈。K2 已经看过 Q 的条件，"
        "因此不能把这些建议写成研究过程中主动发现并验证了关键实验，更不能说追加实验已修复错误。",
        "",
        "| 来源 | K2 所选下一实验（未执行） |",
        "|---|---|",
    ]
    for row in data["rows"]:
        lines.append(
            f"| {row['world']}/{row['arm']} | "
            f"{K2_LABELS[row['text_annotation']['k2_future_choice_code']]} |"
        )
    lines += [
        "",
        "## 6. 对主故事的推进与边界",
        "",
        "可以写：在完整自主研究中，agent 形成了能描述已测平台的有效关系；跨越已测区间时，"
        "公开表达的外推规则与预测可靠性发生分化。不同先验条件影响整个研究过程，包含取证和解释；"
        "这里不要求先分离两条路径。原始操作、K1 和同上下文 Q 一起构成证据，K2 单独标为回顾。",
        "",
        "不能写：所有有先验会话都被锚定；更广探索必然更好；Opaque 已在实验中观测到稀释转折；"
        "K1 已经包含 Q 的全部推理；K2 建议就是原实验计划；从这批记录已定位出内部认知原因。",
        "",
        "本分析到此收束，不自动触发新实验或恢复剩余 28 次固定记录读出。"
        "本报告供稿件整合使用，未改写英文主文或重导出 PDF。",
        "",
        "## 附：逐场阶段证据入口",
        "",
        "以下列出原文件与 K1 原文摘录；全部 Q 原解释、K2 对应完整段落及计算分母在机器摘要中。",
    ]
    for row in data["rows"]:
        cid = row["id"]
        base = f"../work-ii-eq-bounded-equilibrium-20260920/v2-public/sources/{cid}"
        lines += [
            "",
            f"### {cid}",
            "",
            f"[原报告]({base}/EXPERIMENT_REPORT.md) · [结果]({base}/RESULT.json) · "
            f"[逐步 IO]({base}/trajectory.jsonl)",
            "",
        ]
        for quote in row["text_annotation"]["k1_exact_excerpts"]:
            lines += ["> " + quote.replace("\n", "\n> "), ""]
    lines += [
        "",
        "复算（不调用模型或模拟器）：",
        "",
        "```powershell",
        "uv run --no-sync python -m scripts.analyze_work_ii_eq_autonomous_process",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    data = collect()
    coverage = data["coverage"]
    assert coverage["operations"] == coverage["missing_decision_reason_records"] == 945
    assert coverage["source_batches"] == 180
    assert coverage["sources_wholly_above_three_dilute_queries"] == 15
    assert sum(r["text_annotation"]["k2_future_choice_code"] == "trace" for r in data["rows"]) == 11
    (OUT / f"{STEM}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / f"{STEM}_REVIEW_ZH.md").write_text(render(data), encoding="utf-8")
    print(
        json.dumps(
            {"coverage": coverage, "annotation_counts": data["annotation_counts"]},
            ensure_ascii=True,
        )
    )


if __name__ == "__main__":
    main()
