"""Organize retained Figure 3 evidence without running agents or the simulator."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/figures/operation-prediction-story"
CASE = "EC-W01-B12-optimization-E-Opaque"
MATCH_KEYS = ("world", "locus", "budget", "arm")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def matched_pairs():
    """Retain the original matching; orient by the observed retest ordering."""
    campaigns = {
        r["id"]: r
        for r in read_csv(ROOT / "paper/figures/integrated-results/campaign_metrics.csv")
        if r["system"] in ("EC", "RX") and r["metric"] == "score"
    }
    original = read_csv(OUT / "all-60-pairs.csv")
    assert len(campaigns) == 120 and len(original) == 60
    used, rows = set(), []
    for pair in original:
        d, o = (campaigns[pair[f"{goal}_id"]] for goal in ("discovery", "optimization"))
        assert d["goal"] == "discovery" and o["goal"] == "optimization"
        assert all(d[k] == o[k] == pair[k] for k in (*MATCH_KEYS, "system"))
        for goal, campaign in (("discovery", d), ("optimization", o)):
            assert campaign["id"] not in used
            used.add(campaign["id"])
            for retained_key, source_key in (("retest", "retest"), ("score_mae", "mae")):
                assert (
                    abs(float(pair[f"{goal}_{retained_key}"]) - float(campaign[source_key])) < 1e-12
                )
        dr = float(o["retest"]) - float(d["retest"])
        de = float(o["mae"]) - float(d["mae"])
        assert abs(dr - float(pair["delta_retest"])) < 1e-12
        assert abs(de - float(pair["delta_score_mae"])) < 1e-12
        assert dr != 0 and de != 0, "The retained cohort has no exact ties."
        higher, lower = (o, d) if dr > 0 else (d, o)
        gap = float(higher["mae"]) - float(lower["mae"])
        no_recovery = d["recovered"] == o["recovered"] == "False"
        # Legacy name is broader than source restarts: any recorded recovery is excluded.
        assert no_recovery == (pair["no_source_restart"] == "True")
        rows.append(
            {
                "system": pair["system"],
                **{key: pair[key] for key in MATCH_KEYS},
                "discovery_id": d["id"],
                "optimization_id": o["id"],
                "discovery_retest": float(d["retest"]),
                "optimization_retest": float(o["retest"]),
                "discovery_score_mae": float(d["mae"]),
                "optimization_score_mae": float(o["mae"]),
                "higher_retest_goal": higher["goal"],
                "lower_mae_goal": higher["goal"] if gap < 0 else lower["goal"],
                "higher_retest_campaign": higher["id"],
                "lower_retest_campaign": lower["id"],
                "retest_gap_higher_minus_lower": abs(dr),
                "mae_higher_retest_campaign": float(higher["mae"]),
                "mae_lower_retest_campaign": float(lower["mae"]),
                "mae_gap_higher_minus_lower": gap,
                "ordering": "same" if gap < 0 else "opposite",
                "both_without_recorded_recovery": no_recovery,
                "both_conforming": d["conforming"] == o["conforming"] == "True",
                "prediction_reference": d["reference_target"],
            }
        )
    assert len(used) == len(campaigns)
    return rows


def selected_case(pairs):
    """Export only scientific fields from the bound local run and public account."""
    binding = read_json(ROOT / "configs/current.json")["work_ii"]["w2_132_ec_pa_english_matrix"]
    run_root = ROOT / binding["run_root"]
    report_root = (ROOT / binding["report"]).parent / CASE
    source = read_json(run_root / "sources" / CASE / "optimization-E-Opaque/result.json")
    truth = read_json(run_root / "references/EC-W01/reference-result.json")["truth"]
    public_trace = read_json(report_root / "public-trajectory.json")
    report = (report_root / "REPORT.md").read_text(encoding="utf-8")
    predictions = next(
        data
        for block in re.findall(r"```json\s*(.*?)```", report, re.S)
        if "predictions" in (data := json.loads(block))
    )
    q_section = report.split("## Q\n", 1)[1]
    questions = json.JSONDecoder().raw_decode(q_section[q_section.index('[{"query_id"') :])[0]
    questions = {q["query_id"]: q for q in questions}
    selected = source["recommendation"]["selected_experiment_index"]
    pair = next(r for r in pairs if r["optimization_id"] == CASE)
    retest = source["recommendation_retest"]["batches"][0]["metrics"]["score"]
    assert abs(retest - pair["optimization_retest"]) < 1e-12
    batches = []
    for number, batch in enumerate(source["batches"], 1):
        actions = [r["action"] for r in public_trace if r["experiment_index"] == number - 1]
        assert batch["actions"] == actions
        settings = recipe_fields(actions)
        batches.append(
            {
                "batch": number,
                **settings,
                "observed_score": batch["metrics"]["score"],
                "selected_recommendation": number == selected,
                "recommendation_retest_score": retest if number == selected else "",
            }
        )
    queries = []
    for prediction in predictions["predictions"]:
        qid = prediction["query_id"]
        score = prediction["score"]
        reference = truth[qid]["score"]
        queries.append(
            {
                "query": qid,
                **recipe_fields(questions[qid]["actions"]),
                "predicted_score": score["estimate"],
                "lower80": score["lower80"],
                "upper80": score["upper80"],
                "reference_score": reference,
                "absolute_error": abs(score["estimate"] - reference),
                "covered80": score["lower80"] <= reference <= score["upper80"],
            }
        )
    retained = source["prediction_evaluation"]["metrics"]["score"]
    assert len(batches) == len(queries) == 12
    assert len(public_trace) == sum(len(b["actions"]) for b in source["batches"]) == 84
    assert abs(fmean(q["absolute_error"] for q in queries) - retained["mae"]) < 1e-12
    assert abs(fmean(q["covered80"] for q in queries) - retained["coverage80"]) < 1e-12
    assert abs(retained["mae"] - pair["optimization_score_mae"]) < 1e-12
    return batches, queries, predictions["rationale"]


def recipe_fields(actions):
    # This selected case and its query bank use one uninterrupted electrolysis per batch.
    recipe = {}
    for operation in ("add_reagent", "add_solvent", "set_potential", "electrolyze"):
        selected = [a for a in actions if a["operation"] == operation]
        assert len(selected) == 1
        recipe.update({k: v for k, v in selected[0].items() if k != "operation"})
    return {
        key: recipe[key]
        for key in (
            "solvent",
            "electrolyte_profile",
            "potential_V",
            "current_mA",
            "duration_s",
            "amount_mol",
            "volume_L",
        )
    }


def table(headers, rows):
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
        + ["| " + " | ".join(str(x) for x in row) + " |" for row in rows]
    )


def count_order(rows):
    counts = Counter(r["ordering"] for r in rows)
    return [len(rows), counts["same"], counts["opposite"]]


def matrix(pairs, batches, queries, rationale):
    selected_retest = next(
        b["recommendation_retest_score"] for b in batches if b["selected_recommendation"]
    )
    lines = [
        "# Figure 3: retained-data matrix",
        "",
        "Generated by `paper/tools/analyze_operation_prediction_relationship.py`. "
        "Post hoc descriptive reorganization of retained development evidence; "
        "no new agent or simulator calls. "
        "Wording and interpretation are in [README.md](README.md).",
        "",
        "## 1. Original coverage and endpoints",
        "",
        table(
            ["System", "Worlds", "Arms", "Loci", "Budgets", "Goals", "Campaigns", "Pairs"],
            [["EC", 5, 3, "E", "12, 24", 2, 60, 30], ["RX", 5, 3, "P, S", "12", 2, 60, 30]],
        ),
        "",
        "Each original pair fixes world, arm, locus and budget. R is the independent "
        "retest score of a sealed recommendation; E is score-prediction MAE across the "
        "same 12 fixed queries within a world. EC has 1,080 source batches and RX 720; "
        "each system has 60 recommendation retests and 720 score forecasts. These are "
        "not additional independent campaign or world replicates. EC point references "
        "are single seeded observations; RX point references are five-observation means. "
        "Raw effect magnitudes are not pooled across systems.",
        "",
        "## 2. Full joint outcome matrix",
        "",
        "Rows identify the assigned goal of the campaign with the higher observed R; "
        "columns identify the assigned goal of the campaign with the lower E. "
        "Neither goal is designated as intrinsically superior.",
        "",
    ]
    for system in ("EC", "RX"):
        subset = [r for r in pairs if r["system"] == system]
        counts = Counter((r["higher_retest_goal"], r["lower_mae_goal"]) for r in subset)
        lines += [
            f"### {system}",
            "",
            table(
                [
                    "Higher retest campaign",
                    "Lower MAE: optimization",
                    "Lower MAE: discovery",
                    "Total",
                ],
                [
                    [
                        goal,
                        counts[goal, "optimization"],
                        counts[goal, "discovery"],
                        sum(counts[goal, g] for g in ("optimization", "discovery")),
                    ]
                    for goal in ("optimization", "discovery")
                ],
            ),
            "",
        ]
    lines += [
        "## 3. Performance ordering, without privileging either goal",
        "",
        table(
            ["System / subset", "Pairs", "Higher R also has lower E", "Higher R has higher E"],
            [[s, *count_order([r for r in pairs if r["system"] == s])] for s in ("EC", "RX")]
            + [
                [
                    "EC: neither campaign has recorded recovery",
                    *count_order(
                        [
                            r
                            for r in pairs
                            if r["system"] == "EC" and r["both_without_recorded_recovery"]
                        ]
                    ),
                ]
            ],
        ),
        "",
        "Let h/l be the campaign with the higher/lower observed retest within each pair. "
        "The CSV keeps g_R = R_h - R_l > 0 and g_E = E_h - E_l. "
        "g_E < 0 means the orderings agree; g_E > 0 means they disagree. Orienting by "
        "observed R is a descriptive, outcome-selected re-expression, not a randomized "
        "intervention or evidence of a positive optimization effect. There are no exact "
        "ties, significance thresholds or minimum-effect filters. Full unrounded gaps "
        "are retained; this sign classification does not establish "
        "meaningful differences near zero.",
        "",
        "The legacy CSV field `no_source_restart` is computed from both campaigns' "
        "`recovered` flags. For EC these flags include recorded assessment-only recovery, "
        "not just source restarts. The new CSV calls this `both_without_recorded_recovery`. "
        "The 17-pair sensitivity has uneven coverage and does not replace the full cohort.",
        "",
        "## 4. World and design strata",
        "",
        "These are overlapping views of the same pairs, "
        "not extra experiments or independent tests.",
        "",
    ]
    grouped = []
    for system in ("EC", "RX"):
        subset = [r for r in pairs if r["system"] == system]
        for dimension in ("world", "budget", "arm", "locus"):
            for level in sorted({r[dimension] for r in subset}):
                grouped.append(
                    [
                        system,
                        dimension,
                        level,
                        *count_order([r for r in subset if r[dimension] == level]),
                    ]
                )
    lines += [
        table(
            ["System", "Dimension", "Level", "Pairs", "Same ordering", "Opposite ordering"], grouped
        ),
        "",
        "Budget rows compare goals at a fixed budget. They are not 12-to-24 budget contrasts. "
        "World means must not be substituted for individual pair classifications.",
        "",
        "## 5. Assigned-goal means (supporting summaries)",
        "",
        table(
            ["System", "R discovery", "R optimization", "E discovery", "E optimization"],
            [
                [
                    s,
                    *[
                        f"{fmean(r[k] for r in pairs if r['system'] == s):.6f}"
                        for k in (
                            "discovery_retest",
                            "optimization_retest",
                            "discovery_score_mae",
                            "optimization_score_mae",
                        )
                    ],
                ]
                for s in ("EC", "RX")
            ],
        ),
        "",
        "This compares two complete research commissions. It neither isolates evidence "
        "selection from inference nor measures a within-session learning curve. "
        "Similar aggregate MAEs are not evidence of equivalence or zero association.",
        "",
        "## 6. Selected original research case: all source batches",
        "",
        f"Case: `{CASE}`. Retrospectively selected illustration, not an independent "
        "replication or a prevalence estimate. Batch 12 is the sealed recommendation. "
        "K1/Q accounts are later public statements, not contemporaneous internal thoughts.",
        "",
        table(
            [
                "Batch",
                "Solvent / electrolyte",
                "Potential / V",
                "Current cap / mA",
                "Time / s",
                "Score",
            ],
            [
                [
                    b["batch"],
                    f"S{b['solvent']}/E{b['electrolyte_profile']}",
                    b["potential_V"],
                    b["current_mA"],
                    b["duration_s"],
                    f"{b['observed_score']:.6f}",
                ]
                for b in batches
            ],
        ),
        "",
        f"Independent retest of the selected procedure: {selected_retest:.6f}. "
        "All source batches use 0.020 mol in 0.040 L. Individual batch scores include "
        "declines and zero scores; a running maximum would be nondecreasing by construction. "
        "There are no intermediate sealed prediction evaluations.",
        "",
        "## 7. The same agent's complete sealed score predictions",
        "",
        table(
            [
                "Query",
                "Pair",
                "V",
                "Cap / mA",
                "Time / s",
                "Prediction",
                "80% interval",
                "Reference",
                "Abs. error",
                "Covered",
            ],
            [
                [
                    q["query"],
                    f"S{q['solvent']}/E{q['electrolyte_profile']}",
                    q["potential_V"],
                    q["current_mA"],
                    q["duration_s"],
                    f"{q['predicted_score']:.6f}",
                    f"[{q['lower80']:.3f}, {q['upper80']:.3f}]",
                    f"{q['reference_score']:.6f}",
                    f"{q['absolute_error']:.6f}",
                    "yes" if q["covered80"] else "no",
                ]
                for q in queries
            ],
        ),
        "",
        f"Score MAE: {fmean(q['absolute_error'] for q in queries):.6f}; "
        f"80% interval coverage: {sum(q['covered80'] for q in queries)}/{len(queries)}. "
        "All queries use 0.012 mol in 0.025 L. Source-to-query changes include loading "
        "and electrical settings, so the failure is not attributed to a single changed variable.",
        "",
        "Original public Q rationale (verbatim):",
        "",
        f"> {rationale}",
        "",
        "Q04/Q06/Q08/Q10 form an illustrative material comparison at +0.8 V, 100 mA "
        "and 7,200 s; Q04 is accurately predicted and must remain visible alongside "
        "the three large underestimates. The full 12-query table supplies the denominator. "
        "The other matched research campaign's MAE is an auxiliary comparison, not the "
        "definition of absolute accuracy. "
        "Twelve observations do not establish population calibration.",
        "",
        "## Files and verification",
        "",
        "- [All 60 performance-oriented pairs](performance-pairs.csv)",
        "- [All 12 source batches](case-batches.csv)",
        "- [All 12 score forecasts and references](case-queries.csv)",
        "- [Original goal-oriented pairs](all-60-pairs.csv)",
        "",
        "Rebuild verifies 120 campaign endpoints against the retained paired table, all "
        "60 pairs and their matching keys, recovery flags, all 84 selected-case actions "
        "against the public trajectory, recommendation retest, and recomputed case MAE "
        "and coverage against the retained evaluation. No new model/simulator runs, "
        "result exclusions or changes to frozen evidence are involved.",
        "",
    ]
    return "\n".join(lines)


def main():
    pairs = matched_pairs()
    batches, queries, rationale = selected_case(pairs)
    write_csv("performance-pairs.csv", pairs)
    write_csv("case-batches.csv", batches)
    write_csv("case-queries.csv", queries)
    (OUT / "DATA_MATRIX.md").write_text(
        matrix(pairs, batches, queries, rationale), encoding="utf-8"
    )
    for system in ("EC", "RX"):
        n, same, opposite = count_order([r for r in pairs if r["system"] == system])
        print(f"{system}: {n} pairs; same ordering {same}; opposite ordering {opposite}")
    print("Verified 120 campaigns, 60 pairs, 12 case batches / 84 actions and 12 sealed forecasts.")
    print(f"Wrote data matrix and three CSVs to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
