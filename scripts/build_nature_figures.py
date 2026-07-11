"""Build manuscript figures and source-data tables from frozen reports.

The script deliberately reads retained audit artifacts rather than live run
directories.  It therefore cannot silently upgrade diagnostic evidence into a
confirmatory result.
"""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
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
ROLE_COLOURS = {
    "core_confirmed": "#176B87",
    "core_candidate": "#D18F00",
    "exploratory": "#8B8F97",
}


def _read_json(name: str) -> dict[str, Any]:
    return json.loads((REPORTS / name).read_text(encoding="utf-8"))


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
        "CreationDate": datetime(2026, 7, 11, tzinfo=UTC),
        "ModDate": datetime(2026, 7, 11, tzinfo=UTC),
    }
    fig.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight", metadata=metadata)
    fig.savefig(FIGURES / f"{stem}.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def build_system_figure() -> None:
    fig, ax = plt.subplots(figsize=(12.0, 4.8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")

    boxes = [
        (
            0.25,
            2.0,
            2.05,
            1.35,
            "Agent",
            "hypothesis · experiment\nmeasurement · update",
            "#E8F3F7",
        ),
        (
            2.75,
            2.0,
            2.15,
            1.35,
            "Typed interface",
            "public state · spectra\nactions · resource ledger",
            "#FFF3D6",
        ),
        (
            5.35,
            2.0,
            2.2,
            1.35,
            "World family",
            "mechanism · transport\nnoise · hidden shifts",
            "#E8F3F7",
        ),
        (8.0, 2.0, 1.75, 1.35, "Evaluator", "primary endpoint\nconstraints · cost", "#FFF3D6"),
        (10.2, 2.0, 1.55, 1.35, "Evidence", "replay · digest\npaired inference", "#E8F3F7"),
    ]
    for x, y, width, height, title, body, colour in boxes:
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            linewidth=1.2,
            edgecolor="#243447",
            facecolor=colour,
        )
        ax.add_patch(patch)
        ax.text(
            x + width / 2, y + 0.94, title, ha="center", va="center", fontsize=11, weight="bold"
        )
        ax.text(
            x + width / 2, y + 0.43, body, ha="center", va="center", fontsize=8.5, linespacing=1.35
        )
    for start, end in [(2.3, 2.75), (4.9, 5.35), (7.55, 8.0), (9.75, 10.2)]:
        ax.annotate(
            "", xy=(end, 2.68), xytext=(start, 2.68), arrowprops={"arrowstyle": "->", "lw": 1.5}
        )
    ax.annotate(
        "next decision",
        xy=(0.5, 1.8),
        xytext=(8.9, 1.8),
        arrowprops={"arrowstyle": "->", "lw": 1.2, "connectionstyle": "arc3,rad=-0.18"},
        ha="center",
        va="top",
        fontsize=9,
    )
    ax.text(
        6,
        4.3,
        "A closed-loop contract separates agent policy, hidden chemistry and evaluation",
        ha="center",
        fontsize=15,
        weight="bold",
        color="#182A3A",
    )
    ax.text(
        6,
        0.35,
        "Train worlds and Bench worlds share semantics but not hidden world-family cells",
        ha="center",
        fontsize=10,
        color="#445566",
    )
    _save(fig, "figure1_system")


def build_diagnostic_effect_figure() -> None:
    validity = _read_json("task-validity-vnext.json")
    rows: list[dict[str, Any]] = []
    for task_id, card in validity["task_cards"].items():
        test = card["minimum_adaptive_strategy_test"]
        rows.append(
            {
                "task_id": task_id,
                "task_label": TASK_LABELS[task_id],
                "release_role": card["release_role"],
                "primary_metric": card["declared_primary_metric"],
                "mean_paired_effect": test["mean_paired_effect"],
                "ci_low": test["paired_bootstrap_ci"][0],
                "ci_high": test["paired_bootstrap_ci"][1],
                "holm_adjusted_p_value": test["holm_adjusted_p_value"],
                "surface_normalized_effect": test["surface_normalized_effect"],
            }
        )
    rows.sort(key=lambda row: float(row["mean_paired_effect"]))
    _write_csv(
        SOURCE_DATA / "figure2_diagnostic_primary_effects.csv",
        list(rows[0]),
        rows,
    )

    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    for index, row in enumerate(rows):
        effect = float(row["mean_paired_effect"])
        low = float(row["ci_low"])
        high = float(row["ci_high"])
        colour = ROLE_COLOURS[str(row["release_role"])]
        ax.errorbar(
            effect,
            index,
            xerr=[[effect - low], [high - effect]],
            fmt="o",
            ms=7,
            color=colour,
            ecolor=colour,
            capsize=3,
            lw=1.5,
        )
    ax.axvline(0, color="#30363D", lw=1, ls="--")
    ax.set_yticks(range(len(rows)), [str(row["task_label"]) for row in rows])
    ax.set_xlabel("Diagnostic paired primary-metric effect (GP-BO minus random)")
    ax.set_title("Legacy diagnostic runs separate informative from unresolved tasks", weight="bold")
    ax.grid(axis="x", alpha=0.2)
    ax.text(
        0.99,
        -0.19,
        "20 paired seeds; 95% bootstrap intervals; not confirmatory vNext evidence",
        transform=ax.transAxes,
        ha="right",
        fontsize=8,
        color="#5C6670",
    )
    _save(fig, "figure2_diagnostic_effects")


def build_gate_figure() -> None:
    freeze = _read_json("confirmatory-freeze-controls.json")
    method = _read_json("method-protocol-vnext.json")
    evaluation = _read_json("evaluation-identifiability-controls.json")
    harness = _read_json("public-harness-controls.json")
    replay = _read_json("score-replay-controls.json")
    classic = _read_json("publication-classic20-full-summary.json")

    rows = [
        {
            "gate": "Confirmatory protocol frozen",
            "category": "control",
            "passed": freeze["protocol_frozen"],
        },
        {
            "gate": "Layered evaluation identifiable",
            "category": "control",
            "passed": evaluation["evaluation_identifiable"],
        },
        {"gate": "Replay-bound scoring", "category": "control", "passed": replay["controls_ready"]},
        {
            "gate": "Public message boundary",
            "category": "control",
            "passed": harness["controls_ready"],
        },
        {
            "gate": "Required method matrix",
            "category": "evidence",
            "passed": method["formal_method_matrix_ready"],
        },
        {
            "gate": "Exploit matrix complete",
            "category": "evidence",
            "passed": freeze["exploit_matrix_complete"],
        },
        {
            "gate": "Independent reproduction",
            "category": "evidence",
            "passed": classic["gates"]["independent_reproduction_complete"],
        },
        {
            "gate": "Confirmatory rerun",
            "category": "evidence",
            "passed": freeze["confirmatory_rerun_ready"],
        },
    ]
    _write_csv(SOURCE_DATA / "figure3_evidence_gates.csv", ["gate", "category", "passed"], rows)

    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    y = list(range(len(rows)))
    colours = ["#1F8A70" if row["passed"] else "#C94C4C" for row in rows]
    ax.barh(y, [1] * len(rows), color=colours, height=0.62)
    ax.set_yticks(y, [str(row["gate"]) for row in rows])
    ax.set_xlim(0, 1.22)
    ax.set_xticks([])
    ax.invert_yaxis()
    for index, row in enumerate(rows):
        ax.text(
            0.03,
            index,
            "PASS" if row["passed"] else "BLOCKED",
            va="center",
            ha="left",
            color="white",
            weight="bold",
            fontsize=9,
        )
        ax.text(1.04, index, str(row["category"]), va="center", fontsize=8, color="#5C6670")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Controls are implemented; publication evidence remains deliberately blocked", weight="bold"
    )
    _save(fig, "figure3_evidence_gates")


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
    build_diagnostic_effect_figure()
    build_gate_figure()
    evidence_names = [
        "confirmatory-freeze-controls.json",
        "evaluation-identifiability-controls.json",
        "method-protocol-vnext.json",
        "public-harness-controls.json",
        "publication-classic20-full-summary.json",
        "score-replay-controls.json",
        "task-validity-vnext.json",
    ]
    manifest = {
        "schema_version": "chemworld-manuscript-source-data-0.1",
        "evidence_class": "diagnostic_and_control_only",
        "publication_ready": False,
        "generated_by": "scripts/build_nature_figures.py",
        "evidence_sha256": {
            f"workstreams/benchmark_v1/reports/{name}": _sha256(REPORTS / name)
            for name in evidence_names
        },
        "figures": ["figure1_system", "figure2_diagnostic_effects", "figure3_evidence_gates"],
        "limitations": [
            "Figure 2 is retained legacy diagnostic evidence, not a vNext confirmatory comparison.",
            "Figure 3 reports control status and blocked gates, not method performance.",
        ],
    }
    (SOURCE_DATA / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
