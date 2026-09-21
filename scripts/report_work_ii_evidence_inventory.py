"""Read-only evidence inventory; no model calls or simulator executions.

Remote EQ exports are read from an explicit Git commit, without checking out its runtime.
Existing cohort summaries remain authoritative; this is an analysis snapshot, not a release gate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean

from scripts.recover_work_ii_ec_pa_network import effective_row

ROOT = Path(__file__).resolve().parents[1]
REPORTS = Path("workstreams/flagship_tasks/reports")


def local(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def remote(commit, path):
    return json.loads(subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT))


def groups(rows, keys, measures):
    buckets = defaultdict(list)
    for row in rows:
        buckets[tuple(row[k] for k in keys)].append(row)
    return [
        {
            **dict(zip(keys, key, strict=True)),
            "n": len(values),
            **{m: mean(r[m] for r in values) for m in measures},
        }
        for key, values in sorted(buckets.items())
    ]


def rx_goal_pairs(rows):
    lookup = {(r["world_id"], r["locus"], r["arm"], r["goal"]): r for r in rows}
    pairs = []
    for r in rows:
        if r["goal"] != "mechanism_discovery":
            continue
        other = lookup[(r["world_id"], r["locus"], r["arm"], "safety_constrained_optimization")]
        pairs.append(
            {
                "world": r["world_id"],
                "locus": r["locus"],
                "arm": r["arm"],
                "delta_mae_opt_minus_discovery": other["prediction_macro_mae"]
                - r["prediction_macro_mae"],
                "delta_retest_opt_minus_discovery": other["recommendation_retest_score"]
                - r["recommendation_retest_score"],
            }
        )
    return {
        "pairs": pairs,
        "optimization_higher_retest": sum(r["delta_retest_opt_minus_discovery"] > 0 for r in pairs),
        "optimization_lower_mae": sum(r["delta_mae_opt_minus_discovery"] < 0 for r in pairs),
        "better_retest_worse_prediction": sum(
            r["delta_retest_opt_minus_discovery"] > 0 and r["delta_mae_opt_minus_discovery"] > 0
            for r in pairs
        ),
    }


def c_descriptive(rows):
    predictions, retests = [], []
    for r in rows:
        evaluation = r.get("prediction_evaluation") or {}
        if evaluation.get("valid"):
            for metric, values in evaluation["metrics"].items():
                predictions.append(
                    {
                        "budget": r["budget"],
                        "arm": r["arm"],
                        "metric": metric,
                        "mae": values["mae"],
                        "coverage80": values["coverage80"],
                    }
                )
        for m in r["retest_metrics"]:
            quality = (
                m.get("particles_present", True)
                and m["crystal_purity"] >= 0.80
                and m["crystal_fines_fraction"] <= 0.50
            )
            retests.append(
                {
                    "id": r["id"],
                    "budget": r["budget"],
                    "arm": r["arm"],
                    "recovery": m["crystal_yield"],
                    "quality_pass": int(quality),
                    "quality_and_recovery_ge_010": int(quality and m["crystal_yield"] >= 0.10),
                }
            )
    return {
        "prediction_groups": groups(predictions, ("budget", "metric"), ("mae", "coverage80")),
        "retests": retests,
        "retest_groups": groups(
            retests, ("budget",), ("recovery", "quality_pass", "quality_and_recovery_ge_010")
        ),
        "interpretation": "Available readouts from all scheduled cells, including the 11/12 source;"
        " observed retest quality, not noiseless truth or a pooled success score",
    }


def build(commit, p_summary=None):
    ec_path = REPORTS / "work-ii-ec-pa-five-world-en-20260919/summary.json"
    analysis_path = ec_path.with_name("completed-block-analysis.json")
    rx_path = REPORTS / "work-ii-rx-ps-five-world-dual-goal-20260919-final/SUMMARY.json"
    c_path = REPORTS / "work-ii-c-formal-20260920-v3-auto/summary.json"
    eq_path = str(REPORTS / "work-ii-eq-bounded-equilibrium-20260920/v2-public").replace("\\", "/")
    eqs_path = str(REPORTS / "work-ii-eq-s-five-world-20260920-final").replace("\\", "/")
    ec, analysis, rx, crystal = map(local, (ec_path, analysis_path, rx_path, c_path))
    effective = [effective_row(r) for r in ec["results"]]
    assert len({r["unit_id"] for r in effective}) == len(effective) == 102
    primary = {r["unit_id"]: r for r in effective if r["locus"] == "E"}
    assert len(primary) == len(analysis["rows"]) == 90
    for r in analysis["rows"]:
        current = primary[r["unit_id"]]
        assert current["status"] == "completed" and current["posttests_completed"] == 3
        assert current["prediction_evaluation"]["metrics"] == r["metrics"]
    assert sum(r["completed_batches"] for r in effective) == ec["effective_source_batches"]
    eq_index = remote(commit, eq_path + "/INDEX.json")
    eq_rows = []
    for cell in eq_index["cells"]:
        r = remote(commit, eq_path + f"/sources/{cell['cell_id']}/RESULT.json")
        metrics = list(r["prediction_evaluation"]["metrics"].values())
        assert r["cell"]["status"] == "completed" and r["prediction_evaluation"]["valid"]
        eq_rows.append(
            {
                "id": cell["cell_id"],
                "world": cell["world_id"],
                "arm": cell["arm"],
                "mae": mean(m["mae_to_five_repeat_mean"] for m in metrics),
                "coverage80": mean(m["empirical_coverage80"] for m in metrics),
                "width80": mean(m["mean_width80"] for m in metrics),
                "interval_score": mean(m["mean_interval_score_alpha_0_2"] for m in metrics),
                "eqs": r["prediction_evaluation"]["eqs"],
            }
        )
    eqs = remote(commit, eqs_path + "/AGGREGATE.json")
    canonical_path = str(REPORTS / "work-ii-eq-s-canonical-20260920-v0.3-final").replace("\\", "/")
    canonical = None
    if subprocess.check_output(
        ["git", "ls-tree", "--name-only", commit, canonical_path + "/INDEX.json"], cwd=ROOT
    ).strip():
        index = remote(commit, canonical_path + "/INDEX.json")
        cells = [
            remote(commit, canonical_path + f"/sources/{r['cell_id']}/RESULT.json")
            for r in index["cells"]
        ]
        assert len(cells) == len({r["cell"]["cell_id"] for r in cells}) == 15
        assert all(r["cell"]["status"] == "completed" for r in cells)
        assert index["completion"]["source_batches"] == 180
        assert index["completion"]["posttests"] == 45
        canonical = {
            "index": index,
            "aggregate": remote(commit, canonical_path + "/AGGREGATE.json"),
            "cells": cells,
        }
    assert len(eq_rows) == eq_index["completion"]["source_sessions"] == 15
    assert eq_index["completion"]["source_batches"] == 180
    assert eq_index["completion"]["posttests"] == 60
    assert len(rx["cells"]) == rx["complete_cells"] == 60
    assert len({r["cell_id"] for r in rx["cells"]}) == 60
    c_rows = []
    for r in crystal["results"]:
        sealed = sum(
            bool(p.get("payload")) and not p.get("failure") for p in r.get("posttests", {}).values()
        )
        retest = r.get("recommendation_retest", {})
        retest_metrics = [b["metrics"] for b in retest.get("batches", [])]
        c_rows.append(
            {
                "id": r["id"],
                "arm": r["arm"],
                "budget": r["batches_budget"],
                "status": r["status"],
                "batches": len(r.get("source", {}).get("batches", [])),
                "sealed_posttests": sealed,
                "failure": r.get("failure"),
                "source_nonconformance": r.get("retained_source_nonconformance"),
                "prediction_evaluation": r.get("prediction_evaluation"),
                "retest_execution_passed": retest.get("passed"),
                "retest_metrics": retest_metrics,
                "baseline_available": r.get("public_baselines", {}).get("available"),
                "baseline_failure": r.get("public_baselines", {}).get("failure"),
            }
        )
    c_counts = {
        k: crystal[k]
        for k in (
            "planned_sources",
            "started_sources",
            "completed_chains",
            "failed_sources",
            "planned_batches",
            "sealed_batches",
            "live_unsealed_batches",
            "completed_posttests",
            "planned_posttests",
            "qualification_completed_worlds",
        )
    }
    assert sum(r["status"] == "completed" for r in c_rows) == c_counts["completed_chains"]
    assert sum(r["sealed_posttests"] for r in c_rows) == c_counts["completed_posttests"]
    current = local(Path("configs/current.json"))
    historical = []
    for key, entry in current["work_ii"].items():
        # Keep reported denominators and dispositions, not duplicated nested runtime records.
        fields = {
            k: v for k, v in entry.items() if not isinstance(v, (dict, list)) and "sha256" not in k
        }
        fields["counts"] = entry.get("counts")
        historical.append({"registry_key": key, **fields})
    top_level_reports = sorted(
        p.relative_to(ROOT).as_posix() for p in (ROOT / REPORTS).glob("*.json")
    )
    data = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "scope": "Read-only analysis snapshot; not a new qualification"
        " or promotion of development evidence",
        "remote_commit": commit,
        "inputs": [str(p).replace("\\", "/") for p in (ec_path, analysis_path, rx_path, c_path)]
        + [eq_path + "/INDEX.json", eqs_path + "/AGGREGATE.json", "configs/current.json"],
        "complete_primary_cohorts": {
            "systems": ["EC", "PA", "RX", "EQ bounded/P v2"],
            "source_sessions": 165,
            "source_batches": 2520,
            "canonical_K1_Q_K2_stages": 495,
            "additional_EQS_stages": 15,
            "note": "EC E 60 + PA E 30 + RX P/S 60 + EQ bounded/P 15;"
            " no pilots/retries/replays included",
            "posttest_comparability": "Stage counts do not imply identical questions:"
            " RX uses seven K2 questions; EC/PA/C use three.",
        },
        "current_primary_pool_including_C": {
            "source_slots": 165 + c_counts["planned_sources"],
            "started_sources": 165 + c_counts["started_sources"],
            "complete_chains": 165 + c_counts["completed_chains"],
            "source_batches": 2520 + c_counts["sealed_batches"],
            "planned_source_batches": 2520 + c_counts["planned_batches"],
            "K1_Q_K2_stages": 495 + c_counts["completed_posttests"],
            "planned_K1_Q_K2_stages": 495 + c_counts["planned_posttests"],
            "additional_EQS_stages": 15,
            "note": "Five contemporary system blocks; C source nonconformance remains visible."
            " Historical and supplemental pilots excluded.",
        },
        "ec_pa": {
            "counts": {
                k: ec[k]
                for k in (
                    "planned_sources",
                    "completed_sources",
                    "effective_source_batches",
                    "posttests_completed",
                    "additional_source_attempts",
                    "additional_posttest_attempts",
                )
            },
            "primary_analysis_verified_against_current_effective_rows": True,
            "primary_counts": analysis["denominators"],
            "groups": analysis["groups"],
            "arm_groups": analysis["arm_groups"],
            "budget_pairs": analysis["contrasts"]["budget"],
            "goal_pairs": analysis["contrasts"]["goal"],
            "goal_joint_outcomes": analysis["goal_joint_outcomes"],
            "first_attempt_only_goal_joint_outcomes": analysis[
                "first_attempt_only_goal_joint_outcomes"
            ],
            "supplementary_cells": [
                {
                    k: r[k]
                    for k in (
                        "unit_id",
                        "status",
                        "completed_batches",
                        "posttests_completed",
                        "failure",
                    )
                }
                for r in effective
                if r["locus"] != "E"
            ],
        },
        "rx": {
            "counts": {
                k: rx[k]
                for k in (
                    "source_sessions",
                    "complete_cells",
                    "source_batches",
                    "posttests",
                    "reference_executions",
                    "recommendation_retests",
                )
            },
            "arm_groups": groups(
                rx["cells"],
                ("locus", "goal", "arm"),
                (
                    "prediction_macro_mae",
                    "prediction_macro_coverage80",
                    "recommendation_retest_score",
                ),
            ),
            "goal_contrasts": rx_goal_pairs(rx["cells"]),
        },
        "eq_bounded_p_v2": {
            "completion": eq_index["completion"],
            "rows": eq_rows,
            "arm_groups": groups(
                eq_rows, ("arm",), ("mae", "coverage80", "width80", "interval_score")
            ),
        },
        "eq_s_v02_pilot": {
            "disposition": "Immutable closed-set structural-discrimination pilot;"
            " superseded by canonical v0.3 relaunch",
            "source_sessions": 15,
            "source_batches": 180,
            "canonical_stages": 45,
            "EQS_stages": 15,
            "aggregate": eqs,
            "canonical_v03_results_visible_at_remote_commit": canonical is not None,
        },
        "eq_s_canonical_v03": canonical,
        "c_current": {
            "counts": c_counts,
            "controller": crystal.get("parallel_execution"),
            "rows": c_rows,
            "descriptive": c_descriptive(c_rows),
            "retained_prior_attempt": crystal.get("retained_prior_attempt"),
        },
        "p_current": local(p_summary)
        if p_summary
        else {
            "model_sources_completed": 0,
            "planned_sources": 15,
            "budget": 12,
            "planned_source_batches": 180,
            "planned_posttests": 45,
            "planned_retests": 15,
            "pilot_required_before_full_block": True,
        },
        "first_paper": current["publication"],
        "historical_static_programmes": {
            k: current[k]
            for k in (
                "static_scientific_optimization",
                "static_material_information_three_arm",
                "static_s0_five_task_postqualification",
            )
        },
        "historical_work_ii_registry": historical,
        "top_level_json_report_index": top_level_reports,
    }
    pool = dict(data["current_primary_pool_including_C"])
    if canonical:
        for key, increment in {
            "source_slots": 15,
            "started_sources": 15,
            "complete_chains": 15,
            "source_batches": 180,
            "planned_source_batches": 180,
            "K1_Q_K2_stages": 45,
            "planned_K1_Q_K2_stages": 45,
        }.items():
            pool[key] += increment
        data["inputs"].append(canonical_path + "/INDEX.json")
    if p_summary:
        p = data["p_current"]
        if (p.get("disposition") or {}).get("status") == "superseded_platform_diagnostic":
            raise ValueError("Superseded P diagnostics cannot enter the current primary pool")
        assert len(p["results"]) == 15
        assert sum(r["source_batches"] for r in p["results"]) == p["source_batches"]
        assert sum(r["posttests"] for r in p["results"]) == p["posttests"]
        for key, increment in {
            "source_slots": 15,
            "started_sources": sum(r["status"] != "not_started" for r in p["results"]),
            "complete_chains": p["complete_chains"],
            "source_batches": p["source_batches"],
            "planned_source_batches": 180,
            "K1_Q_K2_stages": p["posttests"],
            "planned_K1_Q_K2_stages": 45,
        }.items():
            pool[key] += increment
        pool["note"] = "Six system families; pilot, qualification, references and retries excluded."
        data["inputs"].append(str(p_summary).replace("\\", "/"))
    data["current_primary_pool"] = pool
    return data


def render(data):
    c = data["c_current"]["counts"]
    total = data["current_primary_pool"]
    p = data["p_current"]
    p_line = (
        f"| P E, 12 only | 15 | {p['complete_chains']} | {p['source_batches']}/180 | "
        f"{p['posttests']}/45 | 0 |"
        if "results" in p
        else "| P E proposed, 12 only | 0/15 | 0 | 0/180 | 0/45 | 0 |"
    )
    out = [
        "# Experiment inventory: machine-generated snapshot",
        "",
        f"Observed at {data['generated_at']}; remote evidence at `{data['remote_commit']}`.",
        "",
        "This report reads existing exports only. No provider call, physics execution,"
        " runtime checkout or evidence reclassification is performed.",
        "",
        "## Current cohorts",
        "",
        "| Block | Source sessions | Complete chains | Source batches |"
        " Sealed K1/Q/K2 | Other questions |",
        "|---|---:|---:|---:|---:|---:|",
        "| EC E, two goals, 12/24, five worlds | 60 | 60 | 1080 | 180 | 0 |",
        "| PA E, discovery, 12/24, five worlds | 30 | 30 | 540 | 90 | 0 |",
        "| EC P/S single-world supplements | 12 | 11 | 144 | 34 | 0 |",
        "| RX P/S, two goals, 12, five worlds | 60 | 60 | 720 | 180 | 0 |",
        "| EQ bounded/P v2, 12, five worlds | 15 | 15 | 180 | 45 | 15 EQS |",
        "| EQ-S v0.2.1 closed-set pilot | 15 | 15 | 180 | 45 | 15 EQS |",
        (
            "| EQ-S v0.3 canonical free-mechanism study | 15 | 15 | 180 | 45 | 0 |"
            if data["eq_s_canonical_v03"]
            else "| EQ-S v0.3 canonical study | 0 | 0 | 0 | 0 | 0 |"
        ),
        f"| C E v3, 12/24, five worlds | {c['started_sources']}/30 | {c['completed_chains']} |"
        f" {c['sealed_batches']}/540 | {c['completed_posttests']}/90 | 0 |",
        p_line,
        "",
        (
            "P source batches count final-assayed batches. Its separate lifecycle totals are "
            + str(p["batch_accounting"])
            + "; discarded batches consumed source resources and are not replacement sessions."
            if p.get("batch_accounting")
            else ""
        ),
        "",
        f"The current primary analysis pool contains {total['started_sources']}"
        f" started sources, {total['complete_chains']} complete chains,"
        f" {total['source_batches']}/{total['planned_source_batches']} source batches, and"
        f" {total['K1_Q_K2_stages']}/{total['planned_K1_Q_K2_stages']} K1/Q/K2 stages."
        " The 15 EQ supplements are additional; C completion issues remain visible.",
        "",
        "The four complete primary system cohorts contain 165 sessions, 2,520 source batches"
        " and 495 canonical posttest stages, plus 15 EQ-specific supplements. This is a scope"
        " subtotal, not a count of all historical research. Qualification recipes, reference"
        " repeats, replays, retries and reused source states are different units and are not"
        " added to it.",
        "",
        "## EC/PA complete E cohort",
        "",
        "| System / goal | Budget | n | MAE | Coverage | Task readout |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for r in data["ec_pa"]["groups"]:
        m = r["metrics"]["score" if r["system"] == "EC" else "product_in_organic"]
        coverage = m.get("coverage80", m.get("coverage90"))
        task = (
            f"retest {r['mean_retest_score']:.5f}"
            if r["system"] == "EC"
            else f"decisions {r['correct_decisions']}/{r['decision_readouts']}"
        )
        out.append(
            f"| {r['system']} / {r['goal']} | {r['budget']} | {r['campaigns']} |"
            f" {m['mae']:.5f} | {coverage:.1%} | {task} |"
        )
    out += [
        "",
        "EC coverage is nominal 80%; PA is nominal 90%."
        " MAEs have different targets and are not pooled.",
        "",
        "## RX descriptive arm means",
        "",
        "| Locus | Goal | Arm | n | Macro MAE | 80% coverage | Retest |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for r in data["rx"]["arm_groups"]:
        out.append(
            f"| {r['locus']} | {r['goal']} | {r['arm']} | {r['n']} |"
            f" {r['prediction_macro_mae']:.5f} | {r['prediction_macro_coverage80']:.1%} |"
            f" {r['recommendation_retest_score']:.5f} |"
        )
    out += [
        "",
        "## EQ bounded/P v2 descriptive means",
        "",
        "| Arm | n | Macro MAE | 80% coverage | Width |",
        "|---|---:|---:|---:|---:|",
    ]
    for r in data["eq_bounded_p_v2"]["arm_groups"]:
        out.append(
            f"| {r['arm']} | {r['n']} | {r['mae']:.5f} |"
            f" {r['coverage80']:.1%} | {r['width80']:.5f} |"
        )
    out += [
        "",
        "EQ-S v0.2.1 is a separate closed-set pilot (15/15 abstentions). The v0.3 note explicitly"
        " supersedes its participant contract. "
        + (
            "The canonical v0.3 export is now complete and included in the primary pool."
            if data["eq_s_canonical_v03"]
            else "No canonical v0.3 result export is visible."
        ),
        "",
        "## Current C incompleteness",
        "",
    ]
    for r in data["c_current"]["rows"]:
        if r["status"] != "completed":
            out.append(
                f"- {r['id']}: {r['status']}; batches {r['batches']}/{r['budget']};"
                f" posttests {r['sealed_posttests']}/3; failure `{r['failure']}`;"
                f" source nonconformance `{r['source_nonconformance']}`."
            )
    out += [
        "",
        "A missing C batch remains a source"
        " nonconformance; valid predictions remain analyzable with that label. A reporting/baseline"
        " exception after K2 is not a failed scientific answer.",
        "",
        "## Historical inventory and source navigation",
        "",
        "[summary.json](summary.json) retains the current registry entries, static programme"
        " denominators, explicit input locations and an index of the top-level historical JSON"
        " reports. It does not sum overlapping historical exports as independent experiments."
        " [ANALYSIS.md](ANALYSIS.md) gives the evidence disposition and closure plan.",
        "",
    ]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remote-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--p-summary", type=Path)
    args = parser.parse_args()
    commit = subprocess.check_output(
        ["git", "rev-parse", args.remote_commit], cwd=ROOT, text=True
    ).strip()
    data = build(commit, args.p_summary)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.output / "REPORT.md").write_text(render(data), encoding="utf-8")
    print(
        json.dumps(
            {
                "observed_at": data["generated_at"],
                "complete_primary": data["complete_primary_cohorts"],
                "C": data["c_current"]["counts"],
                "RX_goal_contrasts": {
                    k: v for k, v in data["rx"]["goal_contrasts"].items() if k != "pairs"
                },
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
