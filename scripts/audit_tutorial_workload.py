# ruff: noqa: RUF001
"""Audit tutorial notebooks for nontrivial student workload guidance."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

TUTORIAL_NOTEBOOKS = (
    "day_01_enter_virtual_lab.ipynb",
    "day_02_ontology_and_constitution.ipynb",
    "day_03_observation_and_instruments.ipynb",
    "day_04_mechanism_scans.ipynb",
    "day_05_surrogate_modeling.ipynb",
    "day_06_baselines_and_leaderboard.ipynb",
    "day_07_capstone_artifact.ipynb",
    "day_08_gpt_planner_and_validation.ipynb",
    "day_09_bayesian_optimization.ipynb",
    "day_10_public_leaderboard_challenge.ipynb",
    "day_11_private_generalization.ipynb",
    "day_12_demo_day_artifact.ipynb",
)

REQUIRED_SECTIONS = (
    "学习路径定位",
    "课堂时间盒：每 30 分钟都有产出",
    "本日任务梯度",
    "三小时实验工单",
    "学生工作区",
    "验收口径",
)

REQUIRED_TIMEBOXES = (
    "0:00-0:30",
    "0:30-1:00",
    "1:00-1:30",
    "1:30-2:00",
    "2:00-2:30",
    "2:30-3:00",
)

MINIMUM_WORKLOAD_MARKERS = {
    "day_01_enter_virtual_lab.ipynb": ("至少新增 6 条不同 recipe", "至少画 2 张图"),
    "day_02_ontology_and_constitution.ipynb": ("至少构造 4 个非法动作", "修复为合法 recipe"),
    "day_03_observation_and_instruments.ipynb": ("至少比较 HPLC", "每类至少做 3 次重复测量"),
    "day_04_mechanism_scans.ipynb": ("至少完成 20 个扫描实验", "写出 3 条机制假设"),
    "day_05_surrogate_modeling.ipynb": ("至少使用 30 条实验样本", "训练至少 2 个模型"),
    "day_06_baselines_and_leaderboard.ipynb": ("至少运行 5 类策略", "每类至少 3 个 seed"),
    "day_07_capstone_artifact.ipynb": (
        "至少 1 个完整 submission bundle",
        "至少 replay/verify 2 条轨迹",
    ),
    "day_08_gpt_planner_and_validation.ipynb": (
        "至少写 3 个 GPT-style plan",
        "全部经过 validate/repair",
    ),
    "day_09_bayesian_optimization.ipynb": ("至少进入 3 次 acquisition 决策", "至少各跑 3 个 seed"),
    "day_10_public_leaderboard_challenge.ipynb": (
        "至少提交 2 个 agent",
        "每个 agent 至少 3 个 seed",
    ),
    "day_11_private_generalization.ipynb": ("至少比较 2 个策略", "每个策略至少 3 个 seed"),
    "day_12_demo_day_artifact.ipynb": ("整理最终 6 类证据", "8-10 页展示稿"),
}

EVIDENCE_MARKERS = (
    "表",
    "图",
    "验证",
    "轨迹",
    "解释",
    "下一轮",
)

QUESTION_RUN = "?" * 2
GARBLED_MARKERS = (
    "## " + ("?" * 6),
    f"| {QUESTION_RUN} | {QUESTION_RUN} |",
    ("?" * 3) + " ChemWorld",
    ("?" * 4) + " recipe",
    "\u951b",
    "\u9359",
    "\u93c4",
    "\ufffd",
)


def _notebook_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    chunks: list[str] = []
    for cell in notebook.get("cells", []):
        source = cell.get("source", "")
        chunks.append("".join(source) if isinstance(source, list) else str(source))
    return "\n".join(chunks)


def audit_notebook(path: Path) -> dict[str, Any]:
    text = _notebook_text(path)
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]
    missing_timeboxes = [slot for slot in REQUIRED_TIMEBOXES if slot not in text]
    missing_workload = [
        marker
        for marker in MINIMUM_WORKLOAD_MARKERS[path.name]
        if marker not in text
    ]
    garbled = [marker for marker in GARBLED_MARKERS if marker in text]
    evidence_count = sum(1 for marker in EVIDENCE_MARKERS if marker in text)
    has_student_template = "experiments_added" in text and "next_experiment" in text
    passed = (
        not missing_sections
        and not missing_timeboxes
        and not missing_workload
        and not garbled
        and evidence_count >= 4
        and has_student_template
    )
    return {
        "notebook": path.name,
        "passed": passed,
        "missing_sections": missing_sections,
        "missing_timeboxes": missing_timeboxes,
        "missing_workload_markers": missing_workload,
        "garbled_markers": garbled,
        "evidence_marker_count": evidence_count,
        "has_student_template": has_student_template,
    }


def audit_tutorials(root: Path) -> list[dict[str, Any]]:
    tutorial_dir = root / "notebooks" / "tutorials"
    return [audit_notebook(tutorial_dir / name) for name in TUTORIAL_NOTEBOOKS]


def _write_outputs(rows: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "tutorial_workload_audit.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (output_dir / "tutorial_workload_audit.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        fieldnames = [
            "notebook",
            "passed",
            "missing_sections",
            "missing_timeboxes",
            "missing_workload_markers",
            "garbled_markers",
            "evidence_marker_count",
            "has_student_template",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "missing_sections": ";".join(row["missing_sections"]),
                    "missing_timeboxes": ";".join(row["missing_timeboxes"]),
                    "missing_workload_markers": ";".join(row["missing_workload_markers"]),
                    "garbled_markers": ";".join(row["garbled_markers"]),
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs") / "tutorial_audit",
    )
    args = parser.parse_args()

    rows = audit_tutorials(args.root)
    _write_outputs(rows, args.output_dir)
    passed = all(row["passed"] for row in rows)
    print(
        json.dumps(
            {
                "notebooks": len(rows),
                "passed": sum(1 for row in rows if row["passed"]),
                "failed": sum(1 for row in rows if not row["passed"]),
                "output_dir": str(args.output_dir),
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
