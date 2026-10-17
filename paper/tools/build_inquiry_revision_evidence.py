"""Expose retained same-cohort references and core-history locations; no experiments."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "paper/venues/nature"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def table(headers, rows):
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(map(str, row)) + " |" for row in rows],
        ]
    )


def world_equal(rows, field):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["world"]].append(float(row[field]))
    return fmean(fmean(values) for values in grouped.values())


def world_contrasts(source):
    def rows(path):
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))

    metrics = rows(source / "session_metrics.csv")
    recommendations = rows(source / "EC_RX_RECOMMENDATIONS.csv")
    specifications = [
        ("EC operating score", recommendations, "EC", "recommendation_score", None),
        ("EC operating yield", recommendations, "EC", "recommendation_yield", None),
        ("EC score MAE", metrics, "EC", "mae", "score"),
        ("EC yield MAE", metrics, "EC", "mae", "selective_product_yield"),
        ("EC Faradaic MAE", metrics, "EC", "mae", "faradaic_efficiency"),
        ("RX operating score", recommendations, "RX", "recommendation_score", None),
        ("RX operating yield", recommendations, "RX", "recommendation_yield", None),
        ("RX risk MAE", metrics, "RX", "mae", "safety_risk"),
        ("RX conversion MAE", metrics, "RX", "mae", "conversion"),
        ("C purity MAE", metrics, "C", "mae", "crystal_purity"),
        ("C size MAE", metrics, "C", "mae", "crystal_size"),
        ("C recovery MAE", metrics, "C", "mae", "crystal_yield"),
        ("C fines MAE", metrics, "C", "mae", "crystal_fines_fraction"),
        ("C purity coverage", metrics, "C", "coverage", "crystal_purity"),
        ("C fines interval score", metrics, "C", "interval_score", "crystal_fines_fraction"),
    ]
    output = []
    for label, records, system, metric, response in specifications:
        selected = [
            r
            for r in records
            if r["system"] == system
            and (response is None or r["response"] == response)
            and (system != "RX" or r["goal"] == "optimization")
        ]
        field, arms = {
            "EC": ("goal", ["discovery", "optimization"]),
            "RX": ("arm", ["Opaque", "Aligned"]),
            "C": ("opportunity", ["NoResearch", "Research"]),
        }[system]
        for w in range(1, 6):
            pairs = [
                [r for r in selected if r["world"].endswith(f"W{w:02}") and r[field] == arm]
                for arm in arms
            ]
            output.append(
                {
                    "contrast": label,
                    "world": f"W{w:02}",
                    "first_arm": arms[0],
                    "second_arm": arms[1],
                    "first": fmean(float(r[metric]) for r in pairs[0]),
                    "second": fmean(float(r[metric]) for r in pairs[1]),
                }
            )
    retained = rows(DEST / "evidence/opportunity_world_responses.csv")
    for group in ("all", "dilute"):
        for w in range(1, 6):
            pair = [
                fmean(
                    float(r["mae"])
                    for r in retained
                    if r["world"] == f"W{w:02}"
                    and r["query_group"] == group
                    and r["opportunity"] == arm
                )
                for arm in ("NoResearch", "Research")
            ]
            output.append(
                {
                    "contrast": f"EQ {group} macro MAE",
                    "world": f"W{w:02}",
                    "first_arm": "NoResearch",
                    "second_arm": "Research",
                    "first": pair[0],
                    "second": pair[1],
                }
            )
    assert len(output) == 85
    write_csv(DEST / "evidence/world_contrasts.csv", output)
    (DEST / "evidence/world_contrasts.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    return output


def main():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    source = ROOT / binding["report_root"]
    contrast_rows = world_contrasts(source)
    responses = {
        "crystal_purity": "Purity",
        "crystal_size": "Size index",
        "crystal_yield": "Recovery",
        "crystal_fines_fraction": "Fines",
    }
    reference_rows = []
    for path in sorted((source / "process/C/sessions").glob("*/*-Research.json")):
        history = read(path)
        retained = read(Path(history["source_result"]))
        baseline = retained["public_baselines"]
        eligible = [
            b
            for b in history["batches"]
            if all(type(b["metrics"].get(m)) in (int, float) for m in responses)
        ]
        assert baseline["available"] and baseline["training_batches"] == len(eligible)
        assert len(history["batches"]) == 12 and history["prediction_evaluation"]["valid"]
        for response, label in responses.items():
            reference_rows.append(
                {
                    "session": history["key"],
                    "world": history["unit"]["world"],
                    "response": response,
                    "label": label,
                    "source_assays": 12,
                    "reference_assays": len(eligible),
                    "agent_mae": history["prediction_evaluation"]["metrics"][response]["mae"],
                    "source_mean_mae": baseline["mae"]["public_mean"][response],
                    "source_neighbor_mae": baseline["mae"]["public_nearest_neighbor"][response],
                    "source_mean": fmean(b["metrics"][response] for b in eligible),
                    "public_history": path.relative_to(source).as_posix(),
                }
            )
    assert len(reference_rows) == 60
    assert sum(r["reference_assays"] for r in reference_rows) == 179 * len(responses)
    summary = []
    for response, label in responses.items():
        selected = [r for r in reference_rows if r["response"] == response]
        assert len(selected) == 15 and len({r["world"] for r in selected}) == 5
        summary.append(
            {
                "response": response,
                "label": label,
                "sessions": 15,
                **{
                    k: world_equal(selected, k)
                    for k in ("agent_mae", "source_mean_mae", "source_neighbor_mae")
                },
                "agent_better_than_mean": sum(
                    r["agent_mae"] < r["source_mean_mae"] for r in selected
                ),
            }
        )
    write_csv(DEST / "evidence/new_c_source_references.csv", reference_rows)
    (DEST / "evidence/new_c_source_references.json").write_text(
        json.dumps(
            {
                "status": "posthoc_retained_result_summary_no_new_experiments",
                "binding": "work_ii.w2_267_unified_matrices",
                "sessions": 15,
                "source_assays": 180,
                "eligible_reference_assays": 179,
                "queries_per_response": 180,
                "summary": summary,
                "reference_definition": "Existing public_mean and public_nearest_neighbor outputs; "
                "source final assays only; truth is used only for scoring. "
                "No refitting or selection on query outcomes.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    index = read(DEST / "evidence/unified_case_index.json")
    core = [
        (
            "Purification study A",
            2,
            "Aligned; world 4; repetition 3",
            "Batches 8-10: wash and phase comparisons; note 3 after operation 158; "
            "batch 11 small wash; batch 12 no-wash repeat; final account and forecasts",
        ),
        (
            "Purification study B",
            3,
            "Aligned; world 1; repetition 2",
            "Batches 1-4 low recovery; note 2 after operation 64; operations 65-66 add both "
            "commands; batches 5-8 use remaining stock; four later assays unavailable; "
            "note 3 excludes temperature inference",
        ),
        (
            "Reaction study A",
            4,
            "Discovery; Opaque; world 1; repetition 1",
            "Batch 6 direct termination; batch 10 immediate quench; batch 11 unquenched "
            "wait; note 4 after operation 79; batch 12 quench then wait; "
            "note 5 after operation 88; subsequent forecasts",
        ),
        (
            "Electrochemical study A",
            0,
            "Optimization; Opaque; world 1; repetition 1",
            "Batches 1-2 compare signs; note 2 after operation 56; batches 9-12 refine "
            "negative-potential procedure; terminal note limits scope; forecasts extend "
            "to untested positive potentials",
        ),
        (
            "Electrochemical study B",
            1,
            "Optimization; Aligned; world 3; repetition 2",
            "Batches 1-10 screen materials and duration; note 3 after operation 70 predicts "
            "reverse-sign test; batch 11 reverses sign; batch 12 repeats positive recipe; "
            "note 4 after operation 84; forecasts retain reverse production",
        ),
    ]
    core_records = []
    for alias, position, condition, timeline in core:
        entry = index["records"][position]
        path = entry["portable_archive_path"]
        assert (source / path.removeprefix("unified_matrices/")).is_file()
        core_records.append(
            {
                "study": alias,
                "condition": condition,
                "timeline": timeline,
                "portable_archive_path": path,
            }
        )
    matched = read(DEST / "evidence/matched_world_public_histories.json")
    for alias, repeat, identifier, timeline in [
        (
            "Matched-world study A",
            "repeat-03",
            "EQ-P03-A-Opaque",
            "Notes at operation cursors 0, 36 and 72; batches 7-12 implement "
            "denser sampling, a central repeat and higher loading; final forecast",
        ),
        (
            "Matched-world study B",
            "repeat-02",
            "EQ-P01-A-Opaque",
            "Note at cursor 50 precedes dilution; operations 51-56 implement the "
            "0.75 to 0.375 M comparison; final note at 61; forecast Q09",
        ),
    ]:
        selected = [r for r in matched if r["repeat"] == repeat and r["id"] == identifier]
        assert len(selected) == 1
        core_records.append(
            {
                "study": alias,
                "condition": f"Retained matched worlds; {repeat}; {identifier}",
                "timeline": timeline,
                "portable_archive_path": "matched_world_public_histories.json",
                "record_selector": {"repeat": repeat, "id": identifier},
            }
        )
    (DEST / "evidence/core_history_index.json").write_text(
        json.dumps(
            {
                "selection": "Five core histories from the new 300-session block and two "
                "from the retained 30-session matched-world block, selected retrospectively; "
                "aliases are manuscript identifiers, not new experimental units.",
                "records": core_records,
                "supporting_execution_record": "unified_matrices/process/RX/"
                "measurement-semantics/w5-r2-discovery-misindexed-failed-heats.json",
                "independent_human_review": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    lines = [
        r"\clearpage",
        "",
        "## Core research histories and same-cohort evidence use",
        "",
        "### Main-text trajectory index",
        "",
        "Five core histories are selected from the complete reading of 300 new sessions, "
        "and two from the separately retained thirty matched-world sessions. "
        "Selection is explanatory and retrospective, not a frequency sample. These aliases "
        "remain attached to whole trajectories while individual judgments are traced within them. "
        "Exact locators are supplied in the portable evidence archive. All other cases remain "
        "in unified_case_index.json and the full per-session readings. No independent human "
        "second-rater review is claimed.",
        "",
        table(
            ["Study", "Condition", "Key times"],
            [[r["study"], r["condition"], r["timeline"]] for r in core_records],
        ),
        "",
        "Full archive paths and record selectors are retained in "
        "`core_history_index.json` in the portable evidence archive.",
        "",
        "### Source-only references in the new crystallization opportunity cohort",
        "",
        "This post hoc summary exposes reference errors already stored with the completed "
        "experiment. All fifteen Research sessions have twelve final source assays and twelve "
        "valid query forecasts. Of 180 assays, 179 have all four required numeric responses; "
        "one incomplete response record in world 1, repetition 3 is excluded from the references "
        "by the original eligibility rule, leaving eleven training assays in that session. "
        "The constant reference uses the mean of that session's response-complete public "
        "final-assay responses; the nearest-neighbour reference uses the existing public-recipe "
        "feature distance and one observed final assay. Neither fits to query truth. Both are "
        "scored against the same noiseless preassay targets as the agent. The references are "
        "diagnostics of available information, not alternative autonomous researchers or "
        "NoResearch arms. They produce point forecasts only. Means below weight worlds equally "
        "after averaging the three sessions within each world. No model or simulator was run.",
        "",
        r"\Needspace{8\baselineskip}",
        "",
        table(
            [
                "Response",
                "Agent MAE",
                "Source mean MAE",
                "Source neighbour MAE",
                "Agent beats mean",
            ],
            [
                [
                    r["label"],
                    *[
                        f"{r[k]:.6f}"
                        for k in ("agent_mae", "source_mean_mae", "source_neighbor_mae")
                    ],
                    f"{r['agent_better_than_mean']}/15",
                ]
                for r in summary
            ],
        ),
        "",
        table(
            ["Session", "Response", "Agent MAE", "Source mean MAE"],
            [
                [
                    r["session"].replace("C-W", "W").replace("-Opportunity-Research", ""),
                    r["label"],
                    f"{r['agent_mae']:.6f}",
                    f"{r['source_mean_mae']:.6f}",
                ]
                for r in reference_rows
            ],
        ),
        "",
        "### Interface ambiguity in the supporting reconstruction case",
        "",
        "The public reaction record contains two 600 s requests with outer `ok: true` and "
        "`experiment_completed: true`, alongside `transaction_status: rolled_back`, "
        "`Transaction rolled back: constitution_failed`, and zero temperature/time changes. "
        "The terminal account nevertheless interprets this as 1,200 s without reaction and "
        "later forecasts invoke the resulting history effect. Conflicting success and rollback "
        "signals therefore coexist in what the researcher could read. This case concerns "
        "interface presentation, reconstruction of experimental history and later judgment; "
        "it does not isolate a chemical-reasoning failure or show that the false account guided "
        "earlier source actions. Another retained session explicitly excludes rolled-back "
        "heating from its chemical evidence. Their public records are preserved in the archive.",
        "",
        "The supporting execution-state source is also located by "
        "`core_history_index.json` in the portable evidence archive.",
        "",
    ]
    lines += [
        "### Exact world-level contrasts for the quantitative figures",
        "",
        "Values average available sessions within the fixed world; lines connect different "
        "conditions, not successive states of one researcher. No confidence interval or "
        "population significance estimate is inferred from five worlds.",
        "",
        table(
            ["Contrast", "World", "First arm", "Second arm", "First", "Second"],
            [
                [
                    r["contrast"],
                    r["world"],
                    r["first_arm"],
                    r["second_arm"],
                    f"{r['first']:.6f}",
                    f"{r['second']:.6f}",
                ]
                for r in contrast_rows
            ],
        ),
        "",
    ]
    (DEST / "inquiry_revision_analysis.md").write_text("\n".join(lines), encoding="utf-8")
    print(
        json.dumps(
            {"same_cohort_references": summary, "core_histories": len(core_records)},
            ensure_ascii=False,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
