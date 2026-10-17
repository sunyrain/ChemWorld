"""Post hoc paired-world contrasts and seven-history internal review; no experiments."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean

from build_inquiry_revision_evidence import table, write_csv

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper/venues/nature"
DEST = PAPER / "evidence"
RESPONSES = {
    "pH_normalized": ("Normalized pH", 0.002),
    "acid_dissociation_fraction": ("Free dissociation", 0.006),
    "precipitation_signal": ("Precipitation", 0.006),
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(name, value):
    (DEST / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def paired_contrasts(binding):
    source = ROOT / binding["report_root"] / "experiment"
    run = Path(binding["run_root"])
    design = read(run / "design.json")
    queries = design["eq_config"]["queries"]
    truth = read(run / "references/truth.json")["EQ"]
    # Verify actual retained reference actions, not only matching query labels.
    checked = 0
    for pair in range(1, 6):
        for mechanism in ("A", "B"):
            world = f"EQ-P{pair:02}-{mechanism}"
            for repeat in range(1, 6):
                result = read(run / "references" / world / f"repeat-{repeat}/result.json")
                assert len(result["batches"]) == 12
                for q, b in zip(queries, result["batches"], strict=True):
                    assert q["actions"] == b["actions"]
                    checked += 1
    with (source / "predictions.csv").open(encoding="utf-8", newline="") as stream:
        predictions = list(csv.DictReader(stream))
    assert len(predictions) == 1080
    grouped = defaultdict(list)
    for row in predictions:
        grouped[row["pair"], row["query"], row["metric"], row["mechanism"]].append(row)
    contrasts = []
    for pair, query, response, mechanism in sorted(grouped):
        if mechanism != "A":
            continue
        a, b = [grouped[pair, query, response, m] for m in ("A", "B")]
        assert len(a) == len(b) == 3
        ref = []
        for m, rows in [("A", a), ("B", b)]:
            observations = truth[f"EQ-{pair}-{m}"][query]
            assert len(observations) == 5
            value = fmean(t[response] for t in observations)
            assert all(abs(float(r["reference_mean"]) - value) < 1e-12 for r in rows)
            ref.append(value)
        estimates = [fmean(float(r["estimate"]) for r in rows) for rows in (a, b)]
        reference_delta = ref[1] - ref[0]
        forecast_delta = estimates[1] - estimates[0]
        label, sd = RESPONSES[response]
        contrasts.append(
            {
                "pair": pair,
                "query": query,
                "response": response,
                "label": label,
                "reference_A": ref[0],
                "reference_B": ref[1],
                "forecast_A": estimates[0],
                "forecast_B": estimates[1],
                "reference_B_minus_A": reference_delta,
                "forecast_B_minus_A": forecast_delta,
                "absolute_contrast_error": abs(forecast_delta - reference_delta),
                "assay_sd": sd,
                "reference_gap_at_least_3_assay_sd": abs(reference_delta) >= 3 * sd,
                "direction_agrees": forecast_delta * reference_delta > 0,
                "sessions_per_world": 3,
                "reference_observations_per_query_world": 5,
            }
        )
    assert len(contrasts) == 180
    summary = []
    pair_summary = []
    for response, (label, _) in RESPONSES.items():
        rows = [r for r in contrasts if r["response"] == response]
        large = [r for r in rows if r["reference_gap_at_least_3_assay_sd"]]
        error = fmean(r["absolute_contrast_error"] for r in rows)
        zero_error = fmean(abs(r["reference_B_minus_A"]) for r in rows)
        response_pairs = []
        for pair in sorted({r["pair"] for r in rows}):
            selected = [r for r in rows if r["pair"] == pair]
            pair_error = fmean(r["absolute_contrast_error"] for r in selected)
            pair_zero = fmean(abs(r["reference_B_minus_A"]) for r in selected)
            response_pairs.append(
                {
                    "pair": pair,
                    "response": response,
                    "label": label,
                    "contrasts": len(selected),
                    "mean_absolute_contrast_error": pair_error,
                    "zero_difference_mae": pair_zero,
                    "mae_reduction_vs_zero": pair_zero - pair_error,
                    "better_than_zero": pair_error < pair_zero,
                }
            )
        pair_summary.extend(response_pairs)
        summary.append(
            {
                "response": response,
                "label": label,
                "contrasts": len(rows),
                "nonzero_reference_contrasts": sum(r["reference_B_minus_A"] != 0 for r in rows),
                "zero_reference_contrasts": sum(r["reference_B_minus_A"] == 0 for r in rows),
                "direction_agrees_all": sum(r["direction_agrees"] for r in rows),
                "large_gap_contrasts": len(large),
                "direction_agrees_large_gap": sum(r["direction_agrees"] for r in large),
                "mean_absolute_reference_contrast": zero_error,
                "mean_absolute_contrast_error": error,
                "zero_difference_mae": zero_error,
                "relative_mae_reduction_vs_zero": 1 - error / zero_error if zero_error else None,
                "pairs_better_than_zero": sum(r["better_than_zero"] for r in response_pairs),
                "pairs": len(response_pairs),
            }
        )
    write_csv(DEST / "matched_world_forecast_contrasts.csv", contrasts)
    write_csv(DEST / "matched_world_contrast_pairs.csv", pair_summary)
    dump(
        "matched_world_forecast_contrasts.json",
        {
            "analysis": "Post hoc retained forecasts; no new model or simulator execution",
            "sessions": 30,
            "predictions": 1080,
            "contrasts": 180,
            "matched_reference_action_sequences_checked": checked,
            "definition": "B minus A after averaging three fresh sessions per world; five "
            "reference observations per query-world",
            "interpretation": "Descriptive world-sensitive forecasts, not unique mechanism "
            "identification or research gain. No no-research arm; starter "
            "observations close but not identical. Queries share worlds and "
            "repeat physical target concentrations.",
            "large_gap_rule": "Post hoc descriptive display using the existing 3-assay-SD "
            "physical scale; not a significance test. All 180 contrasts "
            "retained.",
            "summary": summary,
            "amplitude_definition": "MAE of forecast B-A minus reference B-A over all 60 "
            "contrasts per response. Identical predictions in both worlds imply zero contrast; "
            "its MAE is the mean absolute reference contrast. Relative reduction uses the "
            "ratio of aggregate MAEs, never per-query division by reference gaps.",
            "pair_summary": pair_summary,
        },
    )
    dump("matched_world_query_actions.json", queries)
    return summary


def cursor(note):
    value = note["public_cursor"]
    return value["event_count"] if isinstance(value, dict) else value


def core_review(cfg):
    root = ROOT / cfg["w2_267_unified_matrices"]["report_root"] / "process"
    histories = {}
    for label, key in [
        ("Purification study A", "repeat-03__P-W04-B12-optimization-E-Aligned"),
        ("Purification study B", "repeat-02__P-W01-B12-optimization-E-Aligned"),
    ]:
        h = read(root / "PA_P/sessions" / f"{key}.json")
        histories[label] = {
            "notes": h["notes"],
            "batches": h["source_batches"],
            "events": h["events"],
            "posttests": h["posttests"],
        }
    h = read(root / "RX/sources/repeat-01/RX-W01-B12-discovery-P-Opaque.json")
    histories["Reaction study A"] = {
        "notes": h["versions"],
        "batches": h["batches"],
        "events": h["events"],
        "posttests": h["posttests"],
    }
    for label, repeat, key in [
        ("Electrochemical study A", "repeat-01", "EC-W01-B12-optimization-E-Opaque"),
        ("Electrochemical study B", "repeat-02", "EC-W03-B12-optimization-E-Aligned"),
    ]:
        case = (root / "EC/cases" / f"{repeat}--{key}.md").read_text(encoding="utf-8")
        folder = Path(
            next(
                line.removeprefix("来源\uff1a")
                for line in case.splitlines()
                if line.startswith("来源\uff1a")
            )
        )
        result = read(folder / "result.json")
        notes = [
            read(p)
            for p in sorted(
                (folder / "notebook/experiment_documents/notebook_history").glob("*.json")
            )
        ]
        histories[label] = {
            "notes": notes,
            "batches": result["batches"],
            "posttests": {k: v["payload"] for k, v in result["posttests"].items()},
        }
    matched = ROOT / cfg["w2_263_abductive_completion"]["report_root"] / "experiment/sessions"
    for label, repeat, key in [
        ("Matched-world study A", "repeat-03", "EQ-P03-A-Opaque"),
        ("Matched-world study B", "repeat-02", "EQ-P01-A-Opaque"),
    ]:
        h = read(matched / repeat / f"{key}.json")
        histories[label] = {
            "notes": h["versions"],
            "batches": h["batches"],
            "events": h["events"],
            "posttests": {k: v["payload"] for k, v in h["posttests"].items()},
        }
    specs = [
        (
            "Purification study A",
            3,
            11,
            "if it passes with recovery above 0.0479, replicate it in batch 12.",
            "Existing continuation criterion applied; purity 0.8013 passes, "
            "recovery 0.0441 fails the repeat criterion; batch 12 repeats "
            "no-wash recipe.",
            "No changed criterion or newly isolated mechanism; two outcomes "
            "govern the next choice.",
        ),
        (
            "Purification study B",
            2,
            5,
            "I will add 0.040 mol component-0 in all remaining batches and rescreen categories.",
            "Batches 5-8 add both commands; shared stock exhausted; terminal "
            "note excludes discarded temperature attempts.",
            "Actual judgment-operation-resource sequence; no randomized "
            "mediation effect or necessary self-limiting mechanism.",
        ),
        (
            "Reaction study A",
            4,
            12,
            "If quench arrests chemistry, final conversion should remain near "
            "the quenched/direct-termination region (~0.42)",
            "Quench-before-wait sequence executed; conversion 0.42724 versus "
            "unquenched-wait 0.61847; later predictions use quench-dependent "
            "history.",
            "Prospective local operational support; temperature and nonthermal"
            " effects not separated. Agent's stronger arrest interpretation is"
            " not independently established.",
        ),
        (
            "Electrochemical study A",
            2,
            9,
            None,
            "Initial matched sign comparison informs subsequent "
            "negative-potential refinement; final note scopes relation; "
            "forecasts extend near-background values to new positive "
            "potentials.",
            "Boundary statement and numerical application differ; no isolated "
            "mechanism of overextension.",
        ),
        (
            "Electrochemical study B",
            3,
            11,
            "If negative potential retains high yield, the assumed polarity "
            "specificity is rejected",
            "Matched reverse sign yields 0.384; final positive repeat about "
            "0.905; terminal account changes specificity to advantage and "
            "forecasts retain reverse production.",
            "Relation revision within optimization; one world and information "
            "condition, not a randomized testing strategy.",
        ),
        (
            "Matched-world study A",
            2,
            7,
            None,
            "After six assays, dense concentration sampling, repeat and higher"
            " loading are implemented; final forecast states smooth monotone "
            "relationship.",
            "Measured local response, not uniquely identified ion network; all"
            " twelve individual assays retained.",
        ),
        (
            "Matched-world study B",
            2,
            11,
            "Persistent high-loading behavior would suggest path dependence",
            "Dilution from 0.75 to 0.375 M executed after cursor 50; pH rises "
            "0.08045 to 0.10803; later account uses approximate reversibility.",
            "Nearest independent comparator 0.4 M; precipitation readings use "
            "different instruments; not an exact quantitative reversibility "
            "test.",
        ),
    ]
    reviews = []
    for label, revision, batch, quote, finding, boundary in specs:
        h = histories[label]
        note = next(n for n in h["notes"] if n["revision"] == revision)
        b = next(b for b in h["batches"] if b["ordinal"] == batch)
        if quote:
            assert quote in note["text"], (label, quote)
        # The final assay is later than the cited note. First-action timing is
        # retained separately and checked below where the comparison is specific.
        assert cursor(note) < b["end_step"], label
        reviews.append(
            {
                "study": label,
                "note_revision": revision,
                "note_after_operation": cursor(note),
                "selected_batch": batch,
                "final_assay_after_operation": b["end_step"],
                "exact_quote": quote,
                "supported_finding": finding,
                "scope_boundary": boundary,
            }
        )
    p = histories["Purification study A"]
    assert p["batches"][9]["end_step"] == cursor(p["notes"][2])
    assert any(a["operation"] == "wash" for a in p["batches"][10]["actions"])
    assert not any(a["operation"] == "wash" for a in p["batches"][11]["actions"])
    r = histories["Reaction study A"]
    ops = [a["operation"] for a in r["batches"][11]["actions"]]
    assert ops.index("quench") < ops.index("wait")
    assert r["batches"][10]["end_step"] == cursor(r["notes"][3])
    e = histories["Electrochemical study B"]
    assert e["batches"][9]["end_step"] == cursor(e["notes"][2])
    pos, neg = e["batches"][8]["actions"], e["batches"][10]["actions"]

    def without_sign(actions):
        return [{k: v for k, v in a.items() if k != "potential_V"} for a in actions]

    assert without_sign(pos) == without_sign(neg)
    assert "supported polarity advantage, not absolute specificity" in e["notes"][-1]["text"]
    dump(
        "core_history_review.json",
        {
            "review_type": "Single-workflow internal source and scientific review; no "
            "independent rater or blinding",
            "independent_human_review": False,
            "records": reviews,
        },
    )
    dump("core_history_review_sources.json", histories)
    return reviews


def main():
    cfg = read(ROOT / "configs/current.json")["work_ii"]
    summary = paired_contrasts(cfg["w2_263_abductive_completion"])
    reviews = core_review(cfg)
    lines = [
        "## Additional analysis of retained predictions and core histories",
        "",
        "### Do final predictions retain matched-world differences?",
        "",
        "This post hoc analysis uses all thirty matched-world sessions and"
        " 1,080 retained predictions. "
        "It compares B minus A for each parameter pair, query and response after averaging three "
        "sessions within each world. Each reference is the same "
        "five-observation mean used in original "
        "scoring. All 600 actual reference action sequences match the "
        "twelve common query definitions. "
        "All 180 pair-query-response contrasts are retained, including "
        "small gaps and wrong directions. "
        "The supplementary display of gaps at least three assay standard "
        "deviations uses the existing "
        "physical scale; this is a post hoc descriptive threshold, not a "
        "test of statistical significance. "
        "Repeated target concentrations and common worlds preclude "
        "treating these as independent trials.",
        "",
        table(
            [
                "Response",
                "Direction, nonzero",
                "Zero true gap",
                "Direction, large gap",
                "Mean absolute gap error",
            ],
            [
                [
                    s["label"],
                    f"{s['direction_agrees_all']}/{s['nonzero_reference_contrasts']}",
                    s["zero_reference_contrasts"],
                    f"{s['direction_agrees_large_gap']}/{s['large_gap_contrasts']}",
                    f"{s['mean_absolute_contrast_error']:.6f}",
                ]
                for s in summary
            ],
        ),
        "",
        "Magnitude accuracy uses the mean absolute error between forecast and reference "
        "B-minus-A differences, including all sixty contrasts for each response. Identical "
        "forecasts in the two worlds give a zero contrast, whose error is the mean absolute "
        "reference difference. The reduction below is one minus the ratio of aggregate errors; "
        "individual queries are never divided by a potentially near-zero reference gap.",
        "",
        table(
            ["Response", "Forecast MAE", "Zero-gap MAE", "Error reduction", "Pairs better"],
            [
                [
                    s["label"],
                    f"{s['mean_absolute_contrast_error']:.6f}",
                    f"{s['zero_difference_mae']:.6f}",
                    f"{100 * s['relative_mae_reduction_vs_zero']:.1f}%",
                    f"{s['pairs_better_than_zero']}/{s['pairs']}",
                ]
                for s in summary
            ],
        ),
        "",
        "The forecasts reflect both the direction and magnitude of world differences. "
        "Each response improves on the zero-gap reference in all five parameter pairs. "
        "These results describe three-session mean forecasts in the fixed worlds. "
        "The block has no NoResearch arm and supplied starter observations are close but not "
        "identical, so the comparison does not isolate research gain or unique mechanism "
        "identification. Pair-level values expose variation across the five parameter pairs:",
        "",
        table(
            ["Response", "Pair", "Contrasts", "Forecast MAE", "Zero-gap MAE"],
            [
                [
                    r["label"],
                    r["pair"],
                    r["contrasts"],
                    f"{r['mean_absolute_contrast_error']:.6f}",
                    f"{r['zero_difference_mae']:.6f}",
                ]
                for r in read(DEST / "matched_world_forecast_contrasts.json")["pair_summary"]
            ],
        ),
        "",
        "Full contrasts, pair summaries, query actions and original session forecasts "
        "are included in the portable archive.",
        "",
        "### Internal scientific review of seven core histories",
        "",
        "This is a further internal review of public records, not "
        "independent human coding or a blinded "
        "second rating. The reviewer has seen the manuscript and outcomes."
        " Notes, committed operations, "
        "measurements and later accounts are checked separately. Exact "
        "quotations and action timing "
        "checks support the identified sequence; scientific interpretation"
        " retains the boundaries below. "
        "The public source packet allows another researcher to inspect the"
        " history without relying on "
        "the manuscript paraphrase. It does not estimate prevalence.",
        "",
    ]
    for row in reviews:
        lines += [
            f"#### {row['study']}",
            "",
            f"Note {row['note_revision']}, after operation {row['note_after_operation']}; "
            f"selected batch {row['selected_batch']} ends at operation "
            f"{row['final_assay_after_operation']}.",
            "",
        ]
        if row["exact_quote"]:
            lines += ["> " + row["exact_quote"], ""]
        lines += [row["supported_finding"], "", row["scope_boundary"], ""]
    lines += [
        "### Levels of support",
        "",
        table(
            ["Evidence", "Coverage", "What it supports"],
            [
                [
                    "Integrated design",
                    "450 planned sessions in four distinct matrices",
                    "Scope of research conditions; not 450 replications of a process",
                ],
                [
                    "Controlled contrasts",
                    "Fixed worlds, condition cells and retained failures",
                    "Condition-specific operation and prediction differences",
                ],
                [
                    "Complete record reading",
                    "300 new sessions",
                    "Coverage of internal review; not prevalence of every selected phenomenon",
                ],
                [
                    "Core histories",
                    "Five new and two matched-world, selected post hoc",
                    "Actual temporally located transitions and their evidential scope",
                ],
                [
                    "Paired-world forecasts",
                    "30 sessions; 180 correlated contrasts",
                    "Whether final predictions reflect the world-specific response differences",
                ],
            ],
        ),
        "",
    ]
    (PAPER / "inquiry_followup_analysis.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "matched_forecast_summary": summary,
                "core_histories_reviewed": len(reviews),
                "new_experiments": 0,
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
