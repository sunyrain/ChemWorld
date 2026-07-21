"""Build manuscript figures and source tables from versioned evidence reports."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "workstreams" / "benchmark_v1" / "reports"
PAPER = ROOT / "paper"
FIGURES = PAPER / "figures"
SOURCE_DATA = PAPER / "source_data"

TASK_LABELS = {
    "partition-discovery": "Partition",
    "reaction-to-crystallization": "Crystallization",
    "reaction-to-distillation": "Distillation",
    "flow-reaction-optimization": "Flow reaction",
    "electrochemical-conversion": "Electrochemistry",
    "equilibrium-characterization": "Equilibrium",
}
MODE_LABELS = {
    "constitutive_law_family": "constitutive",
    "rate_law_family": "rate law",
    "topology_family": "topology",
}
EVIDENCE_FILES = (
    "architecture-readiness.json",
    "evaluation-identifiability-controls.json",
    "live-llm-controls.json",
    "mechanism-family-controls.json",
    "rl-100k-development.json",
    "safe-gp-failure-diagnostic.json",
    "safe-policy-confirmatory.json",
)


def _read_json(name: str) -> dict[str, Any]:
    payload = json.loads((REPORTS / name).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{name} must contain an object")
    return payload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _save(fig: plt.Figure, stem: str) -> None:
    metadata = {
        "Creator": "ChemWorld scripts/build_nature_figures.py",
        "CreationDate": datetime(2026, 7, 12, tzinfo=UTC),
        "ModDate": datetime(2026, 7, 12, tzinfo=UTC),
    }
    fig.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight", metadata=metadata)
    plt.close(fig)


def build_system_figure() -> None:
    fig, ax = plt.subplots(figsize=(12.0, 4.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    boxes = [
        (0.2, 2.0, 2.0, "Agent", "hypothesis · action\nmeasurement · update", "#E8F3F7"),
        (2.6, 2.0, 2.1, "Public contract", "affordances · spectra\nbudget · history", "#FFF3D6"),
        (5.1, 2.0, 2.15, "Hidden world", "mechanism · transport\nnoise · family shift", "#E8F3F7"),
        (7.65, 2.0, 1.85, "Evaluator", "endpoint · risk\ncost · validity", "#FFF3D6"),
        (9.9, 2.0, 1.85, "Evidence", "replay · digest\npaired inference", "#E8F3F7"),
    ]
    for x, y, width, title, body, colour in boxes:
        patch = FancyBboxPatch(
            (x, y),
            width,
            1.35,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            linewidth=1.2,
            edgecolor="#243447",
            facecolor=colour,
        )
        ax.add_patch(patch)
        ax.text(x + width / 2, y + 0.94, title, ha="center", va="center", weight="bold")
        ax.text(x + width / 2, y + 0.42, body, ha="center", va="center", fontsize=8.5)
    for start, end in ((2.2, 2.6), (4.7, 5.1), (7.25, 7.65), (9.5, 9.9)):
        ax.annotate("", xy=(end, 2.68), xytext=(start, 2.68), arrowprops={"arrowstyle": "->"})
    ax.annotate(
        "next operation",
        xy=(0.5, 1.75),
        xytext=(8.6, 1.75),
        arrowprops={"arrowstyle": "->", "connectionstyle": "arc3,rad=-0.18"},
        ha="center",
        fontsize=9,
    )
    ax.text(
        6,
        4.28,
        "A replay-bound contract separates policy, virtual chemistry and claims",
        ha="center",
        fontsize=15,
        weight="bold",
        color="#182A3A",
    )
    ax.text(
        6,
        0.35,
        (
            "Recipe search, open-loop operation and closed-loop operation "
            "remain separate capability strata"
        ),
        ha="center",
        fontsize=9.5,
        color="#445566",
    )
    _save(fig, "figure1_system")


def build_safe_gp_figure() -> None:
    report = _read_json("safe-policy-confirmatory.json")
    decisions = report["primary_comparison"]["task_decisions"]
    rows: list[dict[str, Any]] = []
    for task_id, card in decisions.items():
        rows.append(
            {
                "task_id": task_id,
                "task_label": TASK_LABELS[task_id],
                "mean_effect": card["mean_paired_effect"],
                "ci_low": card["paired_bootstrap_ci"][0],
                "ci_high": card["paired_bootstrap_ci"][1],
                "sesoi": card["sesoi"],
                "objective_passed": card["objective_rule_passed"],
                "risk_rate_effect": card["constraints"]["safety"]["mean_paired_effect"],
                "relative_cost_effect": card["constraints"]["cost"]["mean_paired_effect"],
                "joint_passed": card["complete_joint_rule_passed"],
            }
        )
    rows.sort(key=lambda row: str(row["task_label"]))
    _write_csv(SOURCE_DATA / "figure2_safe_gp_confirmatory.csv", list(rows[0]), rows)

    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=(11.0, 4.7), gridspec_kw={"width_ratios": [1.25, 1]}
    )
    y = np.arange(len(rows))
    for index, row in enumerate(rows):
        effect = float(row["mean_effect"])
        low = float(row["ci_low"])
        high = float(row["ci_high"])
        colour = "#1F8A70" if row["joint_passed"] else "#C94C4C"
        ax0.errorbar(
            effect,
            index,
            xerr=[[effect - low], [high - effect]],
            fmt="o",
            ms=7,
            capsize=3,
            color=colour,
        )
        ax0.scatter(float(row["sesoi"]), index, marker="|", s=180, color="#17202A", linewidths=2)
    ax0.axvline(0, color="#555", ls="--", lw=1)
    ax0.set_yticks(y, [str(row["task_label"]) for row in rows])
    ax0.set_xlabel("Primary-metric effect (Safe-GP - random)")
    ax0.set_title("a  Confirmatory objective effects", loc="left", weight="bold")
    ax0.grid(axis="x", alpha=0.2)
    ax0.text(
        0.99,
        -0.19,
        "bars: paired interval; ticks: pre-registered SESOI",
        transform=ax0.transAxes,
        ha="right",
        fontsize=8,
    )

    risk = [float(row["risk_rate_effect"]) for row in rows]
    cost = [float(row["relative_cost_effect"]) for row in rows]
    ax1.barh(y - 0.16, risk, height=0.28, label="risk-rate effect", color="#176B87")
    ax1.barh(y + 0.16, cost, height=0.28, label="relative cost effect", color="#D18F00")
    ax1.axvline(0, color="#555", lw=1)
    ax1.set_yticks(y, [str(row["task_label"]) for row in rows])
    ax1.set_xlabel("Candidate - random (lower is better)")
    ax1.set_title("b  Constraint effects", loc="left", weight="bold")
    ax1.legend(frameon=False, fontsize=8, loc="lower right")
    ax1.grid(axis="x", alpha=0.2)
    fig.suptitle(
        "Safe-GP controls risk and cost but misses the flow-task SESOI", weight="bold", y=1.02
    )
    fig.tight_layout()
    _save(fig, "figure2_safe_gp_confirmatory")


def build_development_diagnostics_figure() -> None:
    rl = _read_json("rl-100k-development.json")
    beta = _read_json("safe-gp-failure-diagnostic.json")
    rl_rows = [
        {
            "training_steps": card["training_environment_steps"],
            "mean_episode_best_score": card["summary"]["mean_episode_best_score"],
            "mean_final_score": card["summary"]["mean_final_score"],
            "invalid_action_rate": card["summary"]["invalid_action_rate"],
        }
        for card in rl["learning_curve_dev"]
    ]
    beta_rows = [
        {
            "method": method,
            "beta": (
                "random"
                if method == "random"
                else method.rsplit("_", 2)[-2] + "." + method.rsplit("_", 1)[-1]
            ),
            "mean_flow_conversion": card["mean_flow_conversion"],
            "mean_risk_exceedance_rate": card["mean_risk_exceedance_rate"],
            "mean_cost_per_experiment": card["mean_cost_per_experiment"],
            "run_count": card["run_count"],
        }
        for method, card in beta["method_summaries"].items()
    ]
    _write_csv(SOURCE_DATA / "figure3_rl_learning_curve.csv", list(rl_rows[0]), rl_rows)
    _write_csv(SOURCE_DATA / "figure3_safe_gp_beta.csv", list(beta_rows[0]), beta_rows)

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.8, 4.5))
    steps = [float(row["training_steps"]) / 1000 for row in rl_rows]
    scores = [float(row["mean_episode_best_score"]) for row in rl_rows]
    ax0.plot(steps, scores, marker="o", color="#176B87", lw=2)
    best_index = int(np.argmax(scores))
    ax0.scatter(
        steps[best_index], scores[best_index], s=100, facecolors="none", edgecolors="#C94C4C", lw=2
    )
    ax0.annotate(
        "selected by single-seed Dev",
        (steps[best_index], scores[best_index]),
        xytext=(-58, 24),
        textcoords="offset points",
        fontsize=8,
        arrowprops={"arrowstyle": "->"},
    )
    ax0.set_xlabel("SAC training steps (thousands)")
    ax0.set_ylabel("Mean episode-best Dev score")
    ax0.set_title("a  Training is non-monotonic", loc="left", weight="bold")
    ax0.grid(alpha=0.2)

    colours = {
        "random": "#8B8F97",
        "safe_beta_2_0": "#1F8A70",
        "safe_beta_1_5": "#D18F00",
        "safe_beta_1_0": "#C94C4C",
    }
    for row in beta_rows:
        method = str(row["method"])
        ax1.scatter(
            float(row["mean_risk_exceedance_rate"]),
            float(row["mean_flow_conversion"]),
            s=70 + 170 * (0.5 - float(row["mean_cost_per_experiment"])),
            color=colours[method],
            label=("random" if method == "random" else f"β={row['beta']}"),
        )
    ax1.set_xlabel("Mean risk exceedance rate (lower is better)")
    ax1.set_ylabel("Mean flow conversion (higher is better)")
    ax1.set_title("b  Lower β does not improve the frontier", loc="left", weight="bold")
    ax1.grid(alpha=0.2)
    ax1.legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Development diagnostics reject simple budget and hyperparameter heuristics",
        weight="bold",
        y=1.02,
    )
    fig.tight_layout()
    _save(fig, "figure3_development_diagnostics")


def build_mechanism_figure() -> None:
    report = _read_json("mechanism-family-controls.json")
    rows: list[dict[str, Any]] = []
    for task_id, task in report["tasks"].items():
        for mode, card in task["modes"].items():
            calibration = card["calibration"]
            rows.append(
                {
                    "task_id": task_id,
                    "task_label": TASK_LABELS[task_id],
                    "mode": mode,
                    "mode_label": MODE_LABELS[mode],
                    "median_abs_score_delta": calibration["median_abs_score_delta"],
                    "p90_abs_score_delta": calibration["p90_abs_score_delta"],
                    "detectable_fraction": calibration["detectable_fraction"],
                    "mass_balance_error_max": card["process_mass_balance_error_max"],
                    "behaviorally_distinguishable": calibration["behaviorally_distinguishable"],
                    "noncatastrophic": calibration["noncatastrophic"],
                }
            )
    rows.sort(key=lambda row: (str(row["task_label"]), str(row["mode_label"])))
    _write_csv(SOURCE_DATA / "figure4_mechanism_controls.csv", list(rows[0]), rows)
    labels = [f"{row['task_label']} · {row['mode_label']}" for row in rows]
    y = np.arange(len(rows))
    median = [float(row["median_abs_score_delta"]) for row in rows]
    p90 = [float(row["p90_abs_score_delta"]) for row in rows]
    fig, ax = plt.subplots(figsize=(8.3, 5.6))
    ax.barh(y, p90, color="#CFE8EF", label="90th percentile")
    ax.scatter(median, y, color="#176B87", s=35, label="median")
    ax.axvline(0.005, color="#1F8A70", ls="--", lw=1, label="detectability floor")
    ax.axvline(0.15, color="#C94C4C", ls="--", lw=1, label="non-catastrophic ceiling")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Absolute paired score shift")
    ax.set_title(
        "All nine executed mechanism-family controls are detectable and bounded", weight="bold"
    )
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.grid(axis="x", alpha=0.2)
    _save(fig, "figure4_mechanism_controls")


def build_evidence_gate_figure() -> None:
    architecture = _read_json("architecture-readiness.json")
    rows: list[dict[str, Any]] = []
    for name, card in architecture["control_components"].items():
        rows.append({"layer": "control", "component": name, "passed": card["passed"]})
    for name, card in architecture["formal_evidence_components"].items():
        rows.append({"layer": "formal evidence", "component": name, "passed": card["passed"]})
    _write_csv(SOURCE_DATA / "figure5_evidence_gates.csv", list(rows[0]), rows)
    control = [row for row in rows if row["layer"] == "control"]
    formal = [row for row in rows if row["layer"] == "formal evidence"]
    passed = [
        sum(bool(row["passed"]) for row in control),
        sum(bool(row["passed"]) for row in formal),
    ]
    totals = [len(control), len(formal)]
    blocked = [total - value for total, value in zip(totals, passed, strict=True)]
    fig, ax = plt.subplots(figsize=(8.8, 3.8))
    y = np.arange(2)
    ax.barh(y, passed, color="#1F8A70", label="passed")
    ax.barh(y, blocked, left=passed, color="#C94C4C", label="blocked")
    ax.set_yticks(y, ["Implemented controls", "Formal evidence"])
    ax.set_xlabel("Number of required components")
    ax.set_title("Engineering readiness does not imply benchmark validation", weight="bold")
    for index, (ok, total) in enumerate(zip(passed, totals, strict=True)):
        ax.text(total + 0.2, index, f"{ok}/{total}", va="center", weight="bold")
    ax.text(
        0.99,
        -0.24,
        f"{architecture['active_issue_count']} active scientific issues; publication_ready = false",
        transform=ax.transAxes,
        ha="right",
        fontsize=9,
        color="#5C6670",
    )
    ax.legend(frameon=False, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, "figure5_evidence_gates")


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    SOURCE_DATA.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
        }
    )
    build_system_figure()
    build_safe_gp_figure()
    build_development_diagnostics_figure()
    build_mechanism_figure()
    build_evidence_gate_figure()
    manifest = {
        "schema_version": "chemworld-manuscript-source-data-0.2",
        "evidence_class": "confirmatory_slice_development_diagnostics_and_controls",
        "publication_ready": False,
        "generated_by": "scripts/build_nature_figures.py",
        "evidence_sha256": {
            f"workstreams/benchmark_v1/reports/{name}": _sha256(REPORTS / name)
            for name in EVIDENCE_FILES
        },
        "figures": [
            "figure1_system",
            "figure2_safe_gp_confirmatory",
            "figure3_development_diagnostics",
            "figure4_mechanism_controls",
            "figure5_evidence_gates",
        ],
        "limitations": [
            (
                "Figure 2 is a bounded four-task Safe-GP confirmatory slice, "
                "not a complete method matrix."
            ),
            "Figure 3 contains single-seed RL and five-seed SafeGP development diagnostics.",
            "Figure 4 validates environment interventions, not agent mechanism adaptation.",
            "Figure 5 separates passed controls from missing formal evidence.",
        ],
    }
    (SOURCE_DATA / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
