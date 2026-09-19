"""Descriptive analysis of explicitly selected, complete EC/PA world blocks.

Reads retained results only; does not dispatch experiments or write the live ledger.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean

from scripts.recover_work_ii_ec_pa_network import effective_row, recovery_records

ROOT = Path(__file__).resolve().parents[1]
ARMS = ("Opaque", "Aligned", "MisIndexed")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_record(root, original):
    row = effective_row(original)
    recoveries = recovery_records(original)
    if recoveries:
        path = Path(recoveries[-1]["result_path"])
        report = recoveries[-1]["report_path"]
    else:
        folder = root / "sources" / row["unit_id"]
        if row["system"] == "EC":
            folder /= f"{row['goal']}-{row['locus']}-{row['arm']}"
        path, report = folder / "result.json", f"{row['unit_id']}/REPORT.md"
    result = read(path)
    assert row["status"] == result["status"] == "completed", row["unit_id"]
    assert row["exact_replay"]["verified"] and row["posttests_completed"] == 3
    assert row["completed_batches"] == row["budget"]
    evaluation = result["prediction_evaluation"]
    assert evaluation == row["prediction_evaluation"] and evaluation["valid"]
    item = {
        **{key: row[key] for key in ("unit_id", "system", "goal", "arm", "budget")},
        "world": row["world"]["world_id"],
        "report": report,
        "recovered": bool(recoveries),
        "recovery_kinds": [r["kind"] for r in recoveries],
        "metrics": evaluation["metrics"],
    }
    if row["system"] == "EC":
        item["domain_metrics"] = evaluation["groups"]
        retest = result["recommendation_retest"]
        assert retest["exact_replay"]["verified"] and len(retest["batches"]) == 1
        item["retest_score"] = retest["batches"][0]["metrics"]["score"]
        item["batch_potentials"] = [
            [a["potential_V"] for a in b["actions"] if a["operation"] == "set_potential"]
            for b in result["batches"]
        ]
    else:
        item["decisions"] = evaluation["decisions"]
    return item


def aggregate(rows):
    metrics = {
        metric: {
            key: mean(r["metrics"][metric][key] for r in rows)
            for key in rows[0]["metrics"][metric]
            if key != "n"
        }
        for metric in rows[0]["metrics"]
    }
    result = {"campaigns": len(rows), "metrics": metrics}
    if rows[0]["system"] == "EC":
        result["mean_retest_score"] = mean(r["retest_score"] for r in rows)
    else:
        result["correct_decisions"] = sum(
            d["correct"] for r in rows for d in r["decisions"].values()
        )
        result["decision_readouts"] = sum(len(r["decisions"]) for r in rows)
    return result


def contrasts(rows, *, first_attempt_only=False):
    eligible = [r for r in rows if not first_attempt_only or not r["recovered"]]
    by = {(r["world"], r["goal"], r["arm"], r["budget"]): r for r in eligible}
    budgets, goals = [], []
    for (world, goal, arm, budget), low in by.items():
        metric = "score" if low["system"] == "EC" else "product_in_organic"
        high = by.get((world, goal, arm, 24))
        if budget == 12 and high:
            budgets.append(
                {
                    "world": world,
                    "system": low["system"],
                    "goal": goal,
                    "arm": arm,
                    "mae_12": low["metrics"][metric]["mae"],
                    "mae_24": high["metrics"][metric]["mae"],
                    "delta_mae_24_minus_12": high["metrics"][metric]["mae"]
                    - low["metrics"][metric]["mae"],
                }
            )
        opt = by.get((world, "optimization", arm, budget))
        if low["system"] == "EC" and goal == "discovery" and opt:
            goals.append(
                {
                    "world": world,
                    "arm": arm,
                    "budget": budget,
                    "delta_retest_opt_minus_discovery": opt["retest_score"] - low["retest_score"],
                    "delta_mae_opt_minus_discovery": opt["metrics"][metric]["mae"]
                    - low["metrics"][metric]["mae"],
                }
            )
    return {"budget": budgets, "goal": goals}


def ec_metric_comparisons(rows):
    ec_rows = [r for r in rows if r["system"] == "EC"]
    by = {(r["world"], r["goal"], r["arm"], r["budget"]): r for r in ec_rows}
    output = []
    for metric in ec_rows[0]["metrics"]:
        item = {"metric": metric}
        for goal in ("discovery", "optimization"):
            pairs = [
                (r, by[(r["world"], goal, r["arm"], 24)])
                for r in ec_rows
                if r["goal"] == goal and r["budget"] == 12
            ]
            item[goal + "_budget"] = {
                "lower_mae_at_24": sum(
                    b["metrics"][metric]["mae"] < a["metrics"][metric]["mae"] for a, b in pairs
                ),
                "pairs": len(pairs),
            }
        pairs = [
            (r, by[(r["world"], "optimization", r["arm"], r["budget"])])
            for r in ec_rows
            if r["goal"] == "discovery"
        ]
        item["goal"] = {
            "lower_mae_under_optimization": sum(
                b["metrics"][metric]["mae"] < a["metrics"][metric]["mae"] for a, b in pairs
            ),
            "pairs": len(pairs),
        }
        output.append(item)
    return output


def goal_joint_outcomes(pairs):
    return {
        "pairs": len(pairs),
        "better_retest_and_lower_mae": sum(
            p["delta_retest_opt_minus_discovery"] > 0 and p["delta_mae_opt_minus_discovery"] < 0
            for p in pairs
        ),
        "better_retest_and_higher_mae": sum(
            p["delta_retest_opt_minus_discovery"] > 0 and p["delta_mae_opt_minus_discovery"] > 0
            for p in pairs
        ),
        "equal_retest_or_mae": sum(
            p["delta_retest_opt_minus_discovery"] == 0 or p["delta_mae_opt_minus_discovery"] == 0
            for p in pairs
        ),
    }


def complete_worlds(ledger):
    """Include each system's complete scheduled prefix, without inspecting scores."""
    selected = {}
    for system in ("EC", "PA"):
        selected[system] = []
        goals = ("discovery", "optimization") if system == "EC" else ("discovery",)
        expected = {(goal, arm, budget) for goal in goals for arm in ARMS for budget in (12, 24)}
        for world in range(1, 6):
            rows = [
                effective_row(r)
                for r in ledger["results"]
                if r["system"] == system
                and r["locus"] == "E"
                and r["world"]["world_id"] == f"{system}-W{world:02d}"
            ]
            keys = [(r["goal"], r["arm"], r["budget"]) for r in rows]
            if len(keys) != len(expected) or set(keys) != expected:
                break
            if any(r["status"] != "completed" for r in rows):
                break
            selected[system].append(world)
    return selected


def prior_comparisons(rows, *, first_attempt_only=False):
    eligible = [r for r in rows if not first_attempt_only or not r["recovered"]]
    by = {(r["world"], r["goal"], r["arm"], r["budget"]): r for r in eligible}
    output = []
    for system, goal in (("EC", "discovery"), ("EC", "optimization"), ("PA", "discovery")):
        metric = "score" if system == "EC" else "product_in_organic"
        for budget in (12, 24):
            for first, second in (
                ("Aligned", "Opaque"),
                ("MisIndexed", "Opaque"),
                ("Aligned", "MisIndexed"),
            ):
                pairs = [
                    (r, by[(r["world"], goal, second, budget)])
                    for r in eligible
                    if (r["system"], r["goal"], r["arm"], r["budget"])
                    == (system, goal, first, budget)
                    and (r["world"], goal, second, budget) in by
                ]
                deltas = [
                    a["metrics"][metric]["mae"] - b["metrics"][metric]["mae"] for a, b in pairs
                ]
                output.append(
                    {
                        "system": system,
                        "goal": goal,
                        "budget": budget,
                        "first_arm": first,
                        "second_arm": second,
                        "pairs": len(pairs),
                        "first_lower_mae": sum(d < 0 for d in deltas),
                        "equal_mae": sum(d == 0 for d in deltas),
                        "mean_mae_first_minus_second": mean(deltas) if deltas else None,
                    }
                )
    return output


def analyze(binding, worlds=None):
    root = ROOT / binding["run_root"]
    ledger = read(root / "summary.json")
    selected_worlds = (
        complete_worlds(ledger) if worlds is None else dict.fromkeys(("EC", "PA"), worlds)
    )
    assert all(selected_worlds.values()), "Need a complete factorial world in each system"
    expected = {
        (system, f"{system}-W{world:02d}", goal, arm, budget)
        for system in ("EC", "PA")
        for world in selected_worlds[system]
        for goal in (("discovery", "optimization") if system == "EC" else ("discovery",))
        for arm in ARMS
        for budget in (12, 24)
    }
    selected = [
        r
        for r in ledger["results"]
        if r["locus"] == "E"
        and int(r["world"]["world_id"].split("W")[-1]) in selected_worlds[r["system"]]
    ]
    keys = [
        (r["system"], r["world"]["world_id"], r["goal"], r["arm"], r["budget"]) for r in selected
    ]
    assert len(keys) == len(set(keys)) and set(keys) == expected
    rows = [source_record(root, r) for r in selected]
    groups = []
    for system, goal in (("EC", "discovery"), ("EC", "optimization"), ("PA", "discovery")):
        for budget in (12, 24):
            subset = [
                r for r in rows if (r["system"], r["goal"], r["budget"]) == (system, goal, budget)
            ]
            groups.append({"system": system, "goal": goal, "budget": budget, **aggregate(subset)})
    arm_groups = []
    world_groups = []
    for group in groups:
        subset = [r for r in rows if all(r[k] == group[k] for k in ("system", "goal", "budget"))]
        for arm in ARMS:
            arm_groups.append(
                {
                    **{k: group[k] for k in ("system", "goal", "budget")},
                    "arm": arm,
                    **aggregate([r for r in subset if r["arm"] == arm]),
                }
            )
        for world in sorted({r["world"] for r in subset}):
            world_groups.append(
                {
                    **{k: group[k] for k in ("system", "goal", "budget")},
                    "world": world,
                    **aggregate([r for r in subset if r["world"] == world]),
                }
            )
    return {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "analysis_status": (
            "complete entity-prior cohort; descriptive development evidence"
            if len(rows) == 90
            else "interim complete-world block; descriptive development evidence"
        ),
        "selection": "Complete scheduled world prefixes, separately by system; "
        "no metric threshold or best-case selection.",
        "selected_world_numbers": selected_worlds,
        "live_snapshot": {
            "status": ledger["status"],
            "planned": ledger["planned_sources"],
            "completed": ledger["completed_sources"],
            "failure": ledger.get("failure"),
            "effective_status_counts": dict(
                Counter(effective_row(r)["status"] for r in ledger["results"])
            ),
        },
        "denominators": {
            "campaigns": len(rows),
            "source_batches": sum(r["budget"] for r in rows),
            "posttests": 3 * len(rows),
            "first_attempt_completed": sum(not r["recovered"] for r in rows),
            "recovered_campaigns": sum(r["recovered"] for r in rows),
            "ec_recommendation_retests": sum(r["system"] == "EC" for r in rows),
        },
        "groups": groups,
        "arm_groups": arm_groups,
        "world_groups": world_groups,
        "prior_comparisons": prior_comparisons(rows),
        "first_attempt_only_prior_comparisons": prior_comparisons(rows, first_attempt_only=True),
        "contrasts": contrasts(rows),
        "first_attempt_only_contrasts": contrasts(rows, first_attempt_only=True),
        "goal_joint_outcomes": goal_joint_outcomes(contrasts(rows)["goal"]),
        "first_attempt_only_goal_joint_outcomes": goal_joint_outcomes(
            contrasts(rows, first_attempt_only=True)["goal"]
        ),
        "ec_metric_comparisons": ec_metric_comparisons(rows),
        "rows": rows,
        "limitations": [
            "One realization per condition; world instances within each system "
            "share a model family; "
            "no significance or population claim.",
            "12/24 sessions are independent and do not share an experimental prefix.",
            "Queries, six EC metrics and complementary PA fractions are correlated readouts, "
            "not independent agent replicates.",
            "Means weight each campaign equally; the systems and EC metrics "
            "are not pooled into a total score.",
            "Recovery sensitivity excludes complete pairs containing a recovery; "
            "it is not a randomized first-attempt comparison.",
            "Mechanism correctness and causal information loss have not been established "
            "by this numerical analysis.",
            "The unfinished fixed queue and all infrastructure failures remain "
            "in the live matrix denominator.",
        ],
    }


def render(data):
    denominators = data["denominators"]
    selection = "; ".join(
        f"{system}: " + ", ".join(f"W{w:02d}" for w in worlds)
        for system, worlds in data["selected_world_numbers"].items()
    )
    lines = [
        "# Descriptive analysis: complete EC and PA world blocks",
        "",
        f"Generated: {data['generated_at']}. {data['analysis_status']}.",
        "",
        f"Selection: {selection}. All arms, both budgets and both EC goals are included. "
        "Any unfinished world blocks and the P/S pilot are outside this comparison, "
        "not excluded from the live study denominator. Scope is determined by completion "
        "in the fixed schedule, never by observed performance.",
        "",
        "[Live matrix](REPORT.md) · [Machine-readable analysis](completed-block-analysis.json)",
        "",
        "## Coverage",
        "",
        "```json",
        json.dumps(data["denominators"], indent=2),
        "```",
        "",
        f"{denominators['recovered_campaigns']} recovered campaigns and "
        f"{denominators['first_attempt_completed']} first-attempt completions form this "
        f"{denominators['campaigns']}-campaign block. "
        "Source batches here count effective campaigns; abandoned attempts, replay "
        "and recommendation retests are additional. "
        "All included campaigns have complete posttests and verified source replay.",
        "",
        "## Budget summaries",
        "",
        "EC reports score-prediction MAE and nominal 80% intervals; "
        "PA reports organic-product-fraction MAE and nominal 90% intervals. "
        "The metrics are not combined across systems. Each row averages all arms in the "
        "selected worlds, with equal campaign weights.",
        "",
        "| System / assignment | Budget | Mean MAE | Interval coverage "
        "| Mean interval width | Task readout |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for g in data["groups"]:
        ec = g["system"] == "EC"
        m = g["metrics"]["score" if ec else "product_in_organic"]
        level = "80" if ec else "90"
        task = (
            f"Mean retest score {g['mean_retest_score']:.5f}"
            if ec
            else f"{g['correct_decisions']}/{g['decision_readouts']} decisions"
        )
        lines.append(
            f"| {g['system']} / {g['goal']} | {g['budget']} | {m['mae']:.5f} "
            f"| {m['coverage' + level]:.1%} | {m['mean_width' + level]:.5f} | {task} |"
        )
    lines += [
        "",
        "## Matched contrasts and recovery sensitivity",
        "",
        "Counts describe paired conditions, not independent worlds or significance tests.",
        "",
        "| Comparison | All effective pairs | Pairs with both first attempts complete |",
        "|---|---:|---:|",
    ]
    for system, goal in (("EC", "discovery"), ("EC", "optimization"), ("PA", "discovery")):
        values = []
        for k in ("contrasts", "first_attempt_only_contrasts"):
            pairs = [p for p in data[k]["budget"] if (p["system"], p["goal"]) == (system, goal)]
            values.append(f"{sum(p['delta_mae_24_minus_12'] < 0 for p in pairs)}/{len(pairs)}")
        lines.append(f"| {system} {goal}: lower MAE at 24 | {' | '.join(values)} |")
    for label, key, direction in (
        ("EC optimization: higher recommendation score", "delta_retest_opt_minus_discovery", 1),
        ("EC optimization: lower prediction MAE", "delta_mae_opt_minus_discovery", -1),
    ):
        values = []
        for k in ("contrasts", "first_attempt_only_contrasts"):
            pairs = data[k]["goal"]
            values.append(f"{sum(p[key] * direction > 0 for p in pairs)}/{len(pairs)}")
        lines.append(f"| {label} | {' | '.join(values)} |")
    joint = data["goal_joint_outcomes"]
    sensitive = data["first_attempt_only_goal_joint_outcomes"]
    lines += [
        "",
        f"Optimization has both a better retest and lower prediction MAE in "
        f"{joint['better_retest_and_lower_mae']}/{joint['pairs']} pairs. "
        f"It has a better retest but higher MAE in "
        f"{joint['better_retest_and_higher_mae']}/{joint['pairs']} pairs "
        f"({sensitive['better_retest_and_higher_mae']}/{sensitive['pairs']} "
        "first-attempt-only pairs). "
        f"There are {joint['equal_retest_or_mae']} pairs tied on either outcome.",
    ]
    lines += [
        "",
        "## All six electrochemical prediction metrics",
        "",
        "Each entry counts matched conditions with lower MAE. These correlated outcomes "
        "do not constitute six independent replications of the experiment.",
        "",
        "| Metric | 24 vs 12: discovery | 24 vs 12: optimization | Optimization vs discovery |",
        "|---|---:|---:|---:|",
    ]
    for r in data["ec_metric_comparisons"]:
        d, o, g = r["discovery_budget"], r["optimization_budget"], r["goal"]
        lines.append(
            f"| {r['metric']} | {d['lower_mae_at_24']}/{d['pairs']} "
            f"| {o['lower_mae_at_24']}/{o['pairs']} "
            f"| {g['lower_mae_under_optimization']}/{g['pairs']} |"
        )
    lines += [
        "",
        "## Prior-arm results",
        "",
        "Each mean uses all selected worlds for that system. A lower MAE is better; "
        "EC retest score and PA decision accuracy are separate task outcomes.",
        "",
        "| System / assignment | Budget | Arm | Campaigns | Mean MAE | Task readout |",
        "|---|---:|---|---:|---:|---|",
    ]
    for g in data["arm_groups"]:
        ec = g["system"] == "EC"
        mae = g["metrics"]["score" if ec else "product_in_organic"]["mae"]
        task = (
            f"Retest {g['mean_retest_score']:.5f}"
            if ec
            else f"{g['correct_decisions']}/{g['decision_readouts']} decisions"
        )
        lines.append(
            f"| {g['system']} / {g['goal']} | {g['budget']} | {g['arm']} "
            f"| {g['campaigns']} | {mae:.5f} | {task} |"
        )
    lines += [
        "",
        "Paired counts below compare the same world, goal and budget. Differences "
        "include experiment-selection differences and stochastic session variation.",
        "",
        "| System / assignment | Budget | First vs second arm | First lower MAE "
        "| Mean MAE difference | First-attempt-only wins/pairs |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for p, sensitive in zip(
        data["prior_comparisons"], data["first_attempt_only_prior_comparisons"], strict=True
    ):
        lines.append(
            f"| {p['system']} / {p['goal']} | {p['budget']} "
            f"| {p['first_arm']} vs {p['second_arm']} "
            f"| {p['first_lower_mae']}/{p['pairs']} "
            f"| {p['mean_mae_first_minus_second']:.5f} "
            f"| {sensitive['first_lower_mae']}/{sensitive['pairs']} |"
        )
    lines += [
        "",
        "## World-level means",
        "",
        "Each row averages the three arms. These retain between-world heterogeneity; "
        "the worlds are instances within a shared system family.",
        "",
        "| System / assignment | World | Budget | Mean MAE |",
        "|---|---|---:|---:|",
    ]
    for g in data["world_groups"]:
        metric = "score" if g["system"] == "EC" else "product_in_organic"
        lines.append(
            f"| {g['system']} / {g['goal']} | {g['world']} | {g['budget']} "
            f"| {g['metrics'][metric]['mae']:.5f} |"
        )
    lines += [
        "",
        "## Complete per-campaign table",
        "",
        "Asterisk indicates a separately retained infrastructure recovery. "
        "EC score and PA organic fraction are different outcomes.",
        "",
        "| Campaign | Prediction MAE | Coverage | Width | Task readout |",
        "|---|---:|---:|---:|---|",
    ]
    for r in data["rows"]:
        ec = r["system"] == "EC"
        metric, level = ("score", "80") if ec else ("product_in_organic", "90")
        m = r["metrics"][metric]
        task = (
            f"Retest {r['retest_score']:.5f}"
            if ec
            else f"{sum(d['correct'] for d in r['decisions'].values())}/2 decisions"
        )
        label = r["unit_id"] + ("*" if r["recovered"] else "")
        lines.append(
            f"| [{label}]({r['report']}) | {m['mae']:.5f} "
            f"| {m['coverage' + level]:.1%} | {m['mean_width' + level]:.5f} | {task} |"
        )
    lines += ["", "## Interpretation limits", "", *[f"- {s}" for s in data["limitations"]], ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worlds",
        type=int,
        nargs="+",
        help="Explicit complete prefix for both systems; default discovers each complete prefix",
    )
    args = parser.parse_args()
    if args.worlds is not None and args.worlds != list(range(1, max(args.worlds) + 1)):
        parser.error("worlds must be a contiguous scheduled prefix starting at 1")
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_132_ec_pa_english_matrix"]
    data = analyze(binding, args.worlds)
    out = (ROOT / binding["readable_report"]).parent
    (out / "completed-block-analysis.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (out / "COMPLETED_BLOCK_ANALYSIS.md").write_text(render(data), encoding="utf-8")
    print(json.dumps({"output": str(out / "COMPLETED_BLOCK_ANALYSIS.md"), **data["denominators"]}))


if __name__ == "__main__":
    main()
