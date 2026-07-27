"""Build the reportable static-S0 summary and presentation figures."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from chemworld.eval.provenance import file_sha256, write_json_atomic
from chemworld.eval.static_s0_reporting import (
    build_static_s0_reportable_results,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    ROOT
    / "workstreams/flagship_tasks/reports/static-s0-reportable-results-v0.1.json"
)
DEFAULT_FIGURE_DIR = ROOT / "docs/assets/images"


def _render_blind_scores(report: dict[str, Any], path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(10.2, 4.1), sharey=True)
    for axis, (task_id, task) in zip(axes, report["tasks"].items(), strict=True):
        rows = task["paired_llm_vs_best_classic"]["per_world"]
        seeds = [row["world_seed"] for row in rows]
        llm = [row["blind_final_score"] for row in rows]
        baseline = [row["best_classic_blind_score_world_mean"] for row in rows]
        axis.plot(seeds, llm, "o-", color="#c84f3d", linewidth=2, label="LLM")
        axis.plot(
            seeds,
            baseline,
            "s-",
            color="#24796c",
            linewidth=2,
            label=_algorithm_label(
                task["best_classic_calibration"]["algorithm_id"]
            ),
        )
        axis.axhline(0.0, color="#777777", linewidth=0.7)
        axis.set_title(_task_title(task_id))
        axis.set_xlabel("World seed")
        axis.set_xticks(seeds)
        axis.grid(axis="y", alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("Blind final score")
    axes[0].set_ylim(0.0, 0.7)
    figure.suptitle("Static S0: blind final recommendation by world")
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight", metadata={"Software": "ChemWorld"})
    plt.close(figure)


def _render_curves(report: dict[str, Any], path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(10.2, 4.1), sharey=True)
    for axis, (task_id, task) in zip(axes, report["tasks"].items(), strict=True):
        llm = task["llm"]["best_so_far_curve"]
        baseline = task["best_classic_calibration"][
            "best_so_far_curve_world_clustered"
        ]
        rounds = [row["round"] for row in llm]
        axis.fill_between(
            rounds,
            [row["minimum"] for row in llm],
            [row["maximum"] for row in llm],
            color="#c84f3d",
            alpha=0.12,
        )
        axis.plot(
            rounds,
            [row["mean"] for row in llm],
            color="#c84f3d",
            linewidth=2,
            label="LLM",
        )
        axis.fill_between(
            rounds,
            [row["minimum"] for row in baseline],
            [row["maximum"] for row in baseline],
            color="#24796c",
            alpha=0.12,
        )
        axis.plot(
            rounds,
            [row["mean"] for row in baseline],
            color="#24796c",
            linewidth=2,
            label=_algorithm_label(
                task["best_classic_calibration"]["algorithm_id"]
            ),
        )
        axis.axvline(8, color="#555555", linestyle="--", linewidth=0.8)
        axis.set_title(_task_title(task_id))
        axis.set_xlabel("Complete experiments")
        axis.set_xticks([1, 4, 8, 12, 16, 20])
        axis.grid(axis="y", alpha=0.22)
        axis.legend(frameon=False, fontsize=8)
    axes[0].set_ylabel("Mean best-so-far score")
    axes[0].set_ylim(0.0, 0.65)
    figure.suptitle("Static S0: fixed-world optimization progress")
    figure.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight", metadata={"Software": "ChemWorld"})
    plt.close(figure)


def _task_title(task_id: str) -> str:
    return {
        "electrochemical-conversion": "Electrochemical conversion",
        "reaction-to-crystallization": "Reaction to crystallization",
    }[task_id]


def _algorithm_label(algorithm_id: str) -> str:
    return {
        "structured_rf_ei": "RF-EI",
        "structured_gp_ei": "GP-EI",
        "structured_safe_gp_ei": "Safe GP-EI",
    }.get(algorithm_id, algorithm_id)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    args = parser.parse_args()
    report = build_static_s0_reportable_results(ROOT)
    score_figure = args.figure_dir / "static-s0-blind-scores-v0.1.png"
    curve_figure = args.figure_dir / "static-s0-optimization-curves-v0.1.png"
    score_figure_en = score_figure.with_name(
        f"{score_figure.stem}.en{score_figure.suffix}"
    )
    curve_figure_en = curve_figure.with_name(
        f"{curve_figure.stem}.en{curve_figure.suffix}"
    )
    _render_blind_scores(report, score_figure)
    _render_curves(report, curve_figure)
    shutil.copyfile(score_figure, score_figure_en)
    shutil.copyfile(curve_figure, curve_figure_en)
    report["figures"] = {
        "blind_scores": {
            "path": str(score_figure.relative_to(ROOT)).replace("\\", "/"),
            "sha256": file_sha256(score_figure),
            "english_path": str(score_figure_en.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "english_sha256": file_sha256(score_figure_en),
        },
        "optimization_curves": {
            "path": str(curve_figure.relative_to(ROOT)).replace("\\", "/"),
            "sha256": file_sha256(curve_figure),
            "english_path": str(curve_figure_en.relative_to(ROOT)).replace(
                "\\", "/"
            ),
            "english_sha256": file_sha256(curve_figure_en),
        },
    }
    write_json_atomic(args.output, report)


if __name__ == "__main__":
    main()
