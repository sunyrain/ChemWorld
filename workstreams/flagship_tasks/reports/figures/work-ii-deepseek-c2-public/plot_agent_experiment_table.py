#!/usr/bin/env python3
# ruff: noqa: RUF001
"""Render one ChemWorld agent experiment as an auditable table-like timeline.

The extractor uses every trajectory row belonging to the requested experiment.
The "model reasoning" column is sourced from the explicit structured decision
audit and may be replaced by a source-grounded display annotation file. It does
not expose or claim access to hidden chain-of-thought.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import textwrap
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": [
            "Microsoft YaHei",
            "Arial",
            "DejaVu Sans",
            "Liberation Sans",
        ],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
    }
)

PREVIEW_DPI = 300
SUBMISSION_DPI = 600

PALETTE = {
    "header": "#26384A",
    "header_text": "#FFFFFF",
    "grid": "#9AA6B2",
    "charge": "#DCE8F5",
    "transform": "#F4D9C8",
    "measurement": "#E7DCF1",
    "control": "#E2E5E8",
    "measurement_row": "#F8F3FB",
    "ordinary_row": "#FFFFFF",
    "final_row": "#FFF7E8",
    "accent": "#7B4FA3",
    "text": "#1E2A32",
    "muted": "#56636D",
}

METRIC_LABELS = {
    "pH_normalized": "pH_norm",
    "precipitation_signal": "沉淀信号",
    "energy_efficiency": "能量效率",
    "faradaic_efficiency": "法拉第效率",
    "ohmic_efficiency": "欧姆效率",
    "transport_efficiency": "传质效率",
    "electrochemical_conversion": "转化率",
    "electrochemical_selectivity": "选择性",
    "selective_product_yield": "选择性产率",
    "distillate_purity": "馏分纯度",
    "distillate_recovery": "馏分回收率",
    "product_in_aqueous": "水相产品",
    "product_in_organic": "有机相产品",
    "purity": "纯度",
    "recovery": "回收率",
    "score": "score",
    "safety_risk": "风险",
    "cost": "成本",
}

INSTRUMENT_METRICS = {
    "ph_meter": ("pH_normalized", "precipitation_signal"),
    "uvvis": (
        "energy_efficiency",
        "faradaic_efficiency",
        "ohmic_efficiency",
        "transport_efficiency",
    ),
    "hplc": ("purity", "recovery", "product_in_aqueous", "product_in_organic"),
    "gc": ("distillate_purity", "distillate_recovery", "purity", "recovery"),
    "final_assay": (
        "electrochemical_conversion",
        "electrochemical_selectivity",
        "selective_product_yield",
        "distillate_purity",
        "distillate_recovery",
        "purity",
        "recovery",
        "score",
    ),
}


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"Expected an object at {path}:{line_number}")
            rows.append(value)
    return rows


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def _instrument_name(value: Any) -> str:
    return {
        "ph_meter": "pH meter",
        "uvvis": "UV–Vis",
        "hplc": "HPLC",
        "gc": "GC",
        "final_assay": "final assay",
    }.get(str(value), str(value).replace("_", " "))


def _operation_label(action: Mapping[str, Any]) -> str:
    operation = str(action.get("operation", "unknown"))
    if operation == "add_reagent":
        amount = _number(action.get("amount_mol"))
        return f"加入底物\n{amount:.3f} mol" if amount is not None else "加入底物"
    if operation == "add_solvent":
        volume = _number(action.get("volume_L"))
        suffix = f"\n{1e3 * volume:.0f} mL" if volume is not None else ""
        return f"加入溶剂 S{action.get('solvent', '?')}{suffix}"
    if operation == "add_catalyst":
        amount = _number(action.get("catalyst_amount_mol"))
        suffix = f"\n{1e3 * amount:.2f} mmol" if amount is not None else ""
        return f"加入催化剂 C{action.get('catalyst', '?')}{suffix}"
    if operation == "set_potential":
        potential = _number(action.get("potential_V"))
        current = _number(action.get("current_mA"))
        first = f"{potential:.2f} V" if potential is not None else ""
        second = f"{current:.0f} mA" if current is not None else ""
        values = " / ".join(value for value in (first, second) if value)
        electrolyte = action.get("electrolyte_profile")
        extra = f"\n电解质 E{electrolyte}" if electrolyte is not None else ""
        return f"设定电位\n{values}{extra}".strip()
    if operation == "electrolyze":
        duration = _number(action.get("duration_s"))
        return f"电解\n{duration:.0f} s" if duration is not None else "电解"
    if operation == "heat":
        temperature = _number(action.get("target_temperature_K"))
        duration = _number(action.get("duration_s"))
        values = []
        if temperature is not None:
            values.append(f"{temperature:.0f} K")
        if duration is not None:
            values.append(f"{duration / 60:.0f} min")
        return "加热\n" + " / ".join(values)
    if operation == "measure":
        return f"测量\n{_instrument_name(action.get('instrument'))}"
    if operation == "terminate":
        return "终止 batch"
    return operation.replace("_", " ")


def _operation_class(action: Mapping[str, Any]) -> str:
    operation = str(action.get("operation", "unknown"))
    if operation.startswith("add_"):
        return "charge"
    if operation == "measure":
        return "measurement"
    if operation in {
        "heat",
        "cool_crystallize",
        "electrolyze",
        "set_potential",
        "quench",
        "wait",
    }:
        return "transform"
    return "control"


def _format_metric(key: str, value: float) -> str:
    if abs(value) >= 100:
        rendered = f"{value:.0f}"
    elif abs(value) >= 10:
        rendered = f"{value:.1f}"
    else:
        rendered = f"{value:.3f}"
    return f"{METRIC_LABELS.get(key, key)} {rendered}"


def _state_summary(row: Mapping[str, Any]) -> str:
    action = row.get("action", {})
    action = action if isinstance(action, Mapping) else {}
    operation = str(action.get("operation", "unknown"))
    instrument = str(action.get("instrument", ""))
    outcome = row.get("environment_outcome", {})
    outcome = outcome if isinstance(outcome, Mapping) else {}
    observation = outcome.get("observation", {})
    observation = observation if isinstance(observation, Mapping) else {}
    transaction = str(row.get("transaction_status", "unknown"))

    if operation == "measure":
        keys = INSTRUMENT_METRICS.get(instrument, ())
        metrics = [
            _format_metric(key, value)
            for key in keys
            if (value := _number(observation.get(key))) is not None
        ]
        if metrics:
            return "；".join(metrics)
        return f"{_instrument_name(instrument)} 已完成；{transaction}"
    if operation == "terminate":
        return "batch 已关闭；等待终点测量"
    cost = _number(observation.get("cost"))
    risk = _number(observation.get("safety_risk"))
    values = [f"状态 {transaction}"]
    if cost is not None:
        values.append(f"累计成本 {cost:.3f}")
    if risk is not None:
        values.append(f"风险 {risk:.3f}")
    return "；".join(values)


def _structured_reasoning(row: Mapping[str, Any]) -> tuple[str, str, str, str, str]:
    explanation = row.get("explanation", {})
    explanation = explanation if isinstance(explanation, Mapping) else {}
    audit = explanation.get("decision_audit", {})
    audit = audit if isinstance(audit, Mapping) else {}
    belief = audit.get("belief_update_rule", {})
    belief = belief if isinstance(belief, Mapping) else {}
    return (
        str(audit.get("adaptation_source", "")),
        str(audit.get("diagnostic_target", "")),
        str(audit.get("expected_effect", "")),
        str(belief.get("if_supported", "")),
        str(belief.get("if_not_supported", "")),
    )


def extract_experiment(
    trajectory_path: Path,
    *,
    experiment_index_base_1: int,
    annotations: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    all_rows = _load_jsonl(trajectory_path)
    selected = [
        row
        for row in all_rows
        if int(row.get("experiment_index", -1)) + 1 == experiment_index_base_1
    ]
    if not selected:
        raise ValueError(
            f"No trajectory rows for 1-based experiment {experiment_index_base_1}"
        )
    annotations_by_step: Mapping[str, Any] = {}
    if annotations is not None:
        candidate = annotations.get("annotations_by_trajectory_step", {})
        if isinstance(candidate, Mapping):
            annotations_by_step = candidate
    output: list[dict[str, Any]] = []
    for sequence, row in enumerate(selected, start=1):
        action = row.get("action", {})
        action = action if isinstance(action, Mapping) else {}
        adaptation, target, expected, supported, unsupported = _structured_reasoning(row)
        trajectory_step = int(row.get("step", sequence))
        display_reasoning = str(annotations_by_step.get(str(trajectory_step), "")).strip()
        if not display_reasoning:
            display_reasoning = f"Target: {target} Expected: {expected}".strip()
        output.append(
            {
                "sequence": sequence,
                "trajectory_step": trajectory_step,
                "experiment_index_base_1": experiment_index_base_1,
                "operation_type": str(action.get("operation", "unknown")),
                "operation_payload": dict(action),
                "operation_display": _operation_label(action),
                "transaction_status": str(row.get("transaction_status", "")),
                "state_display": _state_summary(row),
                "adaptation_source": adaptation,
                "diagnostic_target": target,
                "expected_effect": expected,
                "belief_if_supported": supported,
                "belief_if_not_supported": unsupported,
                "model_reasoning_display": display_reasoning,
                "leaderboard_score": row.get("leaderboard_score"),
                "operation_class": _operation_class(action),
            }
        )
    return output


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [key for key in rows[0] if key != "operation_class"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            rendered = dict(row)
            rendered["operation_payload"] = json.dumps(
                rendered["operation_payload"], ensure_ascii=False, sort_keys=True
            )
            writer.writerow(rendered)


def _wrap(value: str, width: int) -> str:
    if "\n" in value:
        return value
    return textwrap.fill(value, width=width, break_long_words=True, break_on_hyphens=False)


def render_table(
    rows: Sequence[Mapping[str, Any]],
    *,
    output_dir: Path,
    task_label: str,
    cohort_label: str,
    evidence_status: str,
    export_tiff: bool,
) -> list[str]:
    row_count = len(rows)
    figure_height = max(6.4, 0.62 * row_count + 1.8)
    # 7.2 in ~= 183 mm: a standard double-column report/paper width.
    fig = plt.figure(figsize=(7.2, figure_height), facecolor="white")
    ax = fig.add_axes((0.035, 0.075, 0.93, 0.80))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    columns = (0.0, 0.055, 0.245, 0.535, 1.0)
    headers = ("序号", "操作", "实验状态 / 仪器读数", "模型思考（结构化 decision audit）")
    header_height = 0.085
    body_height = (1.0 - header_height) / row_count

    for index, header in enumerate(headers):
        x0, x1 = columns[index], columns[index + 1]
        ax.add_patch(
            Rectangle(
                (x0, 1 - header_height),
                x1 - x0,
                header_height,
                facecolor=PALETTE["header"],
                edgecolor="white",
                linewidth=0.9,
            )
        )
        ax.text(
            (x0 + x1) / 2,
            1 - header_height / 2,
            header,
            ha="center",
            va="center",
            color=PALETTE["header_text"],
            fontsize=7.3,
            fontweight="bold",
        )

    for row_index, row in enumerate(rows):
        y1 = 1 - header_height - row_index * body_height
        y0 = y1 - body_height
        is_measurement = row["operation_type"] == "measure"
        is_final = is_measurement and "final assay" in str(row["operation_display"])
        row_color = (
            PALETTE["final_row"]
            if is_final
            else PALETTE["measurement_row"]
            if is_measurement
            else PALETTE["ordinary_row"]
        )
        ax.add_patch(
            Rectangle(
                (0, y0),
                1,
                body_height,
                facecolor=row_color,
                edgecolor=PALETTE["grid"],
                linewidth=0.55,
            )
        )
        operation_color = PALETTE[str(row["operation_class"])]
        ax.add_patch(
            Rectangle(
                (columns[1], y0),
                columns[2] - columns[1],
                body_height,
                facecolor=operation_color,
                edgecolor=PALETTE["grid"],
                linewidth=0.55,
            )
        )
        if is_measurement:
            ax.add_patch(
                Rectangle(
                    (0, y0),
                    0.008,
                    body_height,
                    facecolor=PALETTE["accent"],
                    edgecolor="none",
                )
            )
        for x in columns[1:-1]:
            ax.plot([x, x], [y0, y1], color=PALETTE["grid"], linewidth=0.55)
        y = (y0 + y1) / 2
        ax.text(
            (columns[0] + columns[1]) / 2,
            y,
            str(row["sequence"]),
            ha="center",
            va="center",
            fontsize=7.2,
            fontweight="bold",
            color=PALETTE["text"],
        )
        ax.text(
            (columns[1] + columns[2]) / 2,
            y,
            str(row["operation_display"]),
            ha="center",
            va="center",
            fontsize=6.4,
            color=PALETTE["text"],
        )
        ax.text(
            columns[2] + 0.009,
            y,
            _wrap(str(row["state_display"]), 34),
            ha="left",
            va="center",
            fontsize=6.15,
            color=PALETTE["text"],
            linespacing=1.25,
        )
        reasoning = str(row["model_reasoning_display"])
        source = str(row["adaptation_source"] or "none")
        ax.text(
            columns[3] + 0.01,
            y,
            _wrap(f"[{source}] {reasoning}", 61),
            ha="left",
            va="center",
            fontsize=6.05,
            color=PALETTE["text"],
            linespacing=1.25,
        )

    experiment_index = rows[0]["experiment_index_base_1"]
    evidence_note = (
        "该示例来自终态 corrected-semantics cohort，用于展示可审计的实验交互过程。"
        if evidence_status == "corrected_semantics_terminal"
        else "该示例来自历史 pre-fix cohort，仅用于展示交互过程。"
    )
    fig.text(
        0.035,
        0.955,
        f"DeepSeek 单次实验历程：{task_label} · Experiment {experiment_index}",
        fontsize=10.5,
        fontweight="bold",
        color=PALETTE["text"],
        ha="left",
        va="top",
    )
    fig.text(
        0.035,
        0.915,
        f"{cohort_label}｜紫色行表示仪器测量；所有 {row_count} 个轨迹步骤完整保留",
        fontsize=7.2,
        color=PALETTE["muted"],
        ha="left",
        va="top",
    )
    fig.text(
        0.035,
        0.025,
        "注：‘模型思考’来自每一步显式记录的 diagnostic target、expected effect 与 "
        "adaptation source 的结构化摘要，不是隐藏 chain-of-thought。"
        + evidence_note,
        fontsize=6.2,
        color=PALETTE["muted"],
        ha="left",
        va="bottom",
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    base = output_dir / "deepseek_c2_agent_experiment_table"
    outputs: list[str] = []
    formats: list[tuple[str, dict[str, Any]]] = [
        (".svg", {}),
        (".pdf", {}),
        (".png", {"dpi": PREVIEW_DPI}),
    ]
    if export_tiff:
        formats.append((".tiff", {"dpi": SUBMISSION_DPI}))
    for suffix, kwargs in formats:
        path = base.with_suffix(suffix)
        fig.savefig(path, bbox_inches="tight", facecolor="white", **kwargs)
        if suffix == ".svg":
            _normalize_svg_whitespace(path)
        outputs.append(path.name)
    plt.close(fig)
    return outputs


def _normalize_svg_whitespace(path: Path) -> None:
    """Remove renderer-only line-end spaces so generated SVGs stay Git-clean."""
    text = path.read_text(encoding="utf-8")
    normalized = "\n".join(line.rstrip(" \t") for line in text.splitlines())
    if text.endswith(("\n", "\r")):
        normalized += "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory", type=Path, required=True)
    parser.add_argument("--experiment-index", type=int, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--task-label", required=True)
    parser.add_argument(
        "--cohort-label",
        default="historical pre-fix public; measurement-rich representative",
    )
    parser.add_argument(
        "--evidence-status",
        choices=("historical_pre_fix", "corrected_semantics_terminal"),
        default="historical_pre_fix",
        help="Label the evidence lifecycle in the machine summary.",
    )
    parser.add_argument(
        "--export-tiff",
        action="store_true",
        help="Also render a 600-DPI TIFF; omitted by default because it is very large.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    annotations = _load_json(args.annotations) if args.annotations else None
    rows = extract_experiment(
        args.trajectory,
        experiment_index_base_1=args.experiment_index,
        annotations=annotations,
    )
    output_dir = args.output_dir.resolve()
    source_path = output_dir / "source_data" / "agent_experiment_table.csv"
    _write_csv(source_path, rows)
    outputs = render_table(
        rows,
        output_dir=output_dir,
        task_label=args.task_label,
        cohort_label=args.cohort_label,
        evidence_status=args.evidence_status,
        export_tiff=args.export_tiff,
    )
    report = {
        "schema_version": "chemworld-agent-experiment-table-summary-0.1",
        "trajectory_run": args.trajectory.parents[2].name,
        "cell_id": args.trajectory.parent.name,
        "task_label": args.task_label,
        "experiment_index_base_1": args.experiment_index,
        "trajectory_rows": len(rows),
        "nonfinal_measurement_rows": sum(
            row["operation_type"] == "measure"
            and "final assay" not in str(row["operation_display"])
            for row in rows
        ),
        "data_status": (
            "corrected_semantics_terminal_evidence"
            if args.evidence_status == "corrected_semantics_terminal"
            else "historical_descriptive_not_corrected_semantics_evidence"
        ),
        "source_data": source_path.relative_to(output_dir).as_posix(),
        "figure_outputs": outputs,
    }
    (output_dir / "agent_experiment_table_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
