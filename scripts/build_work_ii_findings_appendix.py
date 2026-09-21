"""Embed retained numeric results in the Chinese findings discussion catalogue.

Reads existing summaries only. No simulator, provider, judge, or new hypothesis test.
The authored catalogue remains outside the generated markers.
"""

# ruff: noqa: RUF001 -- Chinese report text uses Chinese punctuation.

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-evidence-closeout-20260921"
DOCUMENT = REPORT / "FINDINGS_AND_HYPOTHESES_ZH.md"
BEGIN = "<!-- BEGIN GENERATED FINDINGS APPENDIX -->"
END = "<!-- END GENERATED FINDINGS APPENDIX -->"
ARMS = ("Opaque", "Aligned", "MisIndexed")


def read(name):
    return json.loads((REPORT / name).read_text(encoding="utf-8"))


def number(value):
    return "—" if value is None else f"{value:.5f}"


def percent(value):
    return f"{100 * value:.1f}%"


def context(row):
    return "/".join(str(row[k]) for k in ("system", "locus", "goal", "budget") if k in row)


def table(lines, header, rows):
    lines.extend(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)])
    for row in rows:
        assert len(row) == len(header)
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    lines.append("")


def details(lines, label, note, header, rows):
    lines.extend(["<details>", f"<summary>{label}</summary>", "", note, ""])
    table(lines, header, rows)
    lines.extend(["</details>", ""])


def validate_authored(text):
    authored = text.split(BEGIN)[0] + text.split(END)[1]
    ids = re.findall(r"^\| ([A-Z]{1,3}-\d{2}) \|", authored, re.M)
    assert len(ids) == len(set(ids)), "Duplicate catalogue identifier"
    declared = re.search(r"目录规模：(\d+) 个编号条目", authored)
    assert declared and int(declared[1]) == len(ids), "Stale catalogue entry count"
    references = set(re.findall(r"\b[A-Z]{1,3}-\d{2}\b", authored))
    assert references <= set(ids), references - set(ids)
    definitions = dict(re.findall(r"^\[([^]]+)\]: (\S+)\s*$", authored, re.M))
    uses = set(re.findall(r"\[([A-Za-z][A-Za-z0-9]*)\](?![:(])", authored))
    assert uses <= definitions.keys(), uses - definitions.keys()
    for path in definitions.values():
        assert (DOCUMENT.parent / path).is_file(), path
    return Counter(identifier.split("-")[0] for identifier in ids)


def render(data, story):
    groups = story["world_rows"]
    rows = [row for group in groups for row in group["arms"].values()]
    assert len(groups) == 80 and all(set(g["arms"]) == set(ARMS) for g in groups)
    assert len(rows) == len({r["id"] for r in rows}) == 240
    assert sum(r["conforming"] for r in rows) == 238
    assert sum(len(r["metrics"]) for r in rows) == 1065
    for key, count in (
        ("budget_contrasts", 18),
        ("prior_contrasts", 234),
        ("c_baseline_contrasts", 16),
        ("calibration", 78),
        ("c_response_diagnostics", 8),
        ("p_factor_directions", 36),
    ):
        assert len(data[key]) == count, key
    lines = [
        "自动展开既有汇总：240 来源、80 组三臂世界条件、1,065 个来源—响应记录；"
        "18 个预算对比、234 个先验对比、16 个 C 基线对比、78 组校准摘要。"
        "另列 90 行目标配对（RX 同一批配对用两个端点，非 90 个独立配对）、"
        "30 行 EQ/P 浓度组结果、20 行 C 响应联合对比、36 行 P 干预读出。",
        "",
        "每个折叠表都嵌在本文件中。数值以五位小数显示，精确值保留在原 JSON；"
        "极小差异四舍五入后可能显示相同。这里不按输赢删行、不做新的显著性检验。",
        "",
    ]
    details(
        lines,
        "A. 全部 18 项预算对比",
        "差值=24次−12次MAE，负值有利24次。双方合规同时排除不合规来源及其配对；"
        "去一世界范围是影响度，不是置信区间。",
        ["编号", "条件", "响应", "12→24 MAE", "改善", "均差", "去一世界范围", "合规均差(n)"],
        [
            [
                f"B{i:03d}",
                context(r),
                r["metric"],
                f"{number(r['all_scheduled']['second_mean'])}→{number(r['all_scheduled']['first_mean'])}",
                f"{r['all_scheduled']['first_lower']}/{r['all_scheduled']['n']}",
                number(r["all_scheduled"]["mean_difference"]),
                ", ".join(map(number, r["all_scheduled"]["leave_one_world_out_difference_range"])),
                f"{number(r['both_conforming']['mean_difference'])} ({r['both_conforming']['n']})",
            ]
            for i, r in enumerate(data["budget_contrasts"], 1)
        ],
    )
    details(
        lines,
        "B. 全部 234 项先验对比",
        "每行五个世界配对；差值=前臂−后臂MAE。macro仅在同体系内等权汇总；"
        "负差不证明模型正确理解资料。去一世界范围不作推断区间。",
        [
            "编号",
            "条件",
            "响应",
            "前/后臂",
            "两臂均值",
            "前臂胜",
            "均差",
            "去一世界范围",
            "合规均差(n)",
        ],
        [
            [
                f"T{i:03d}",
                context(r),
                r["metric"],
                f"{r['first_arm']}/{r['second_arm']}",
                f"{number(r['all_scheduled']['first_mean'])}/{number(r['all_scheduled']['second_mean'])}",
                f"{r['all_scheduled']['first_lower']}/{r['all_scheduled']['n']}",
                number(r["all_scheduled"]["mean_difference"]),
                ", ".join(map(number, r["all_scheduled"]["leave_one_world_out_difference_range"])),
                f"{number(r['both_conforming']['mean_difference'])} ({r['both_conforming']['n']})",
            ]
            for i, r in enumerate(data["prior_contrasts"], 1)
        ],
    )
    details(
        lines,
        "C. 全部 16 项 C 同源基线对比",
        "均值和最近邻均使用同一 agent 的公开终测；不获得额外来源实验。"
        "差值=agent−基线。低变化响应可能使简单基线有优势。",
        ["编号", "预算", "响应", "参考", "Agent/参考 MAE", "Agent胜", "合规均差(n)"],
        [
            [
                f"N{i:03d}",
                r["budget"],
                r["metric"],
                r["reference"],
                f"{number(r['all_scheduled']['first_mean'])}/{number(r['all_scheduled']['second_mean'])}",
                f"{r['all_scheduled']['first_lower']}/{r['all_scheduled']['n']}",
                f"{number(r['both_conforming']['mean_difference'])} ({r['both_conforming']['n']})",
            ]
            for i, r in enumerate(data["c_baseline_contrasts"], 1)
        ],
    )
    details(
        lines,
        "D. 全部 78 组误差、覆盖率和区间宽度摘要",
        "每组汇总三臂共15来源；below统计单来源覆盖率低于名义的数量。"
        "不同体系参考目标不同，不能直接用覆盖率排科学能力。",
        ["编号", "条件", "响应", "MAE", "名义", "覆盖", "宽度", "低于名义的来源"],
        [
            [
                f"U{i:03d}",
                context(r),
                r["metric"],
                number(r["mae"]),
                percent(r["nominal"]),
                percent(r["coverage"]),
                number(r["width"]),
                f"{r['below_nominal_sources']}/{r['n']}",
            ]
            for i, r in enumerate(data["calibration"], 1)
        ],
    )
    details(
        lines,
        "E. 全部目标配对：EC得分、RX得分及RX宏平均",
        "差值=优化−探索；复测正值有利优化，MAE负值有利优化。"
        "RX两个端点共享30配对；首次标志表示双方均首次有效运行。",
        ["端点", "世界", "先验层", "预算", "臂", "复测差", "预测MAE差", "双方首次"],
        [
            [
                endpoint,
                r["world"],
                r["locus"],
                r["budget"],
                r["arm"],
                number(r["delta_retest"]),
                number(r["delta_mae"]),
                r["first_attempt"],
            ]
            for endpoint, pairs in data["goal_pairs"].items()
            for r in pairs
        ],
    )
    details(
        lines,
        "F. EQ/P全部15来源的浓度组结果",
        "三道最稀题为Q03/Q08/Q09，其余九题含其他边界条件。"
        "源均值是事后参考，题组不是预注册新主端点。",
        ["世界", "臂", "源浓度范围(M)", "题组", "MAE", "源均值MAE", "覆盖", "宽度"],
        [
            [
                r["world"],
                r["arm"],
                "–".join(number(v) for v in r["source_nominal_concentration_range"]),
                name,
                number(v["mae"]),
                number(v["source_mean_mae"]),
                percent(v["coverage"]),
                number(v["width"]),
            ]
            for r in story["eq_p_query_regimes"]["cells"]
            for name, v in r["groups"].items()
        ],
    )
    details(
        lines,
        "G. C全部20项回收—纯度联合先验对比",
        "差值为资料臂−Opaque MAE。负回收差且正纯度差为本文的响应反向组合。",
        ["世界", "预算", "臂", "回收差", "纯度差", "双方合规"],
        [
            [
                r["world"],
                r["budget"],
                r["arm"],
                number(r["recovery_delta"]),
                number(r["purity_delta"]),
                r["both_conforming"],
            ]
            for r in story["c_paired_response_tradeoffs"]
        ],
    )
    details(
        lines,
        "H. C全部8组响应均值、跨度与有符号偏差",
        "跨度为每世界12题极差的平均。低估数量是相关查询条目数，非独立世界。",
        ["预算", "响应", "源均值", "真值均值", "预测均值", "真值跨度", "偏差", "低估条目"],
        [
            [
                r["budget"],
                r["metric"],
                number(r["source_observed_mean"]),
                number(r["reference_mean"]),
                number(r["prediction_mean"]),
                number(r["mean_reference_span"]),
                number(r["signed_bias"]),
                f"{r['underestimated_queries']}/{r['queries']}",
            ]
            for r in data["c_response_diagnostics"]
        ],
    )
    details(
        lines,
        "I. P全部36项三臂干预方向结果",
        "固定0.02小效应分辨率；可分辨效应和小效应分别列出。0/0表示不适用，非失败。",
        ["臂", "干预", "响应", "总正确", "可分辨效应正确", "小效应正确"],
        [
            [
                r["arm"],
                r["factor"],
                r["metric"],
                f"{r['correct']}/{r['total']}",
                f"{r['resolved_correct']}/{r['resolved_total']}",
                f"{r['small_effect_correct']}/{r['small_effect_total']}",
            ]
            for r in data["p_factor_directions"]
        ],
    )
    lines.extend(
        [
            "<details>",
            "<summary>J. 全部80组三臂世界：所有1,065个来源—响应的MAE、覆盖率、宽度</summary>",
            "",
            "每格依次为MAE / 覆盖率 / 区间宽度。星号为来源少终检，仍保留全部评估。"
            "C/P的复测数值为各自分母的回收，EC/RX为各自得分，不能跨体系混算。"
            "EQ/PA未安排推荐复测，以—表示。质量合格仅在有该字段时列出。",
            "",
        ]
    )
    metric_triplets = 0
    for i, group in enumerate(groups, 1):
        lines.extend([f"#### W{i:03d} · {context(group)} · {group['world']}", ""])
        source_notes = []
        for arm in ARMS:
            r = group["arms"][arm]
            quality = "" if "quality_pass" not in r else f"，质量合格={r['quality_pass']}"
            source_notes.append(
                f"{arm}: `{r['id']}`{'*' if not r['conforming'] else ''}，"
                f"复测={number(r.get('retest'))}{quality}"
            )
        lines.extend(["；".join(source_notes) + "。", ""])
        metrics = sorted(group["arms"]["Opaque"]["metrics"])
        assert all(sorted(group["arms"][arm]["metrics"]) == metrics for arm in ARMS)
        values = []
        for metric in metrics:
            cells = [metric]
            for arm in ARMS:
                r = group["arms"][arm]
                v = r["metrics"][metric]
                cells.append(
                    f"{number(v['mae'])} / {percent(v['coverage'])} / {number(v['width'])}"
                    + ("*" if not r["conforming"] else "")
                )
            values.append(cells)
            metric_triplets += 1
        table(lines, ["响应", *ARMS], values)
    assert metric_triplets == 355
    lines.extend(["</details>", ""])
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check without writing")
    args = parser.parse_args()
    original = DOCUMENT.read_text(encoding="utf-8")
    assert original.count(BEGIN) == original.count(END) == 1
    counts = validate_authored(original)
    rendered = render(read("DETAILED_ANALYSIS.json"), read("STORY_WORLD_ANALYSIS.json"))
    before, remainder = original.split(BEGIN)
    _, after = remainder.split(END)
    updated = before + BEGIN + "\n\n" + rendered + "\n" + END + after
    if args.check:
        assert updated == original, "Numeric appendix is stale; regenerate it"
    else:
        DOCUMENT.write_text(updated, encoding="utf-8")
    print(f"Catalogue validated: {sum(counts.values())} entries; {dict(counts)}")
    print("Retained appendix: 240 campaigns / 80 groups / 1065 metrics; all links resolve.")


if __name__ == "__main__":
    main()
