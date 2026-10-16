"""Integrate retained unified matrices into manuscript tables; no experiments."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "paper/venues/nature"
SYSTEMS = {
    "EC": "Electrochemistry",
    "RX": "Reaction processing",
    "PA": "Partitioning",
    "P": "Purification",
    "C": "Crystallization",
}
LABELS = {
    "selective_product_yield": "Product yield",
    "faradaic_efficiency": "Faradaic efficiency",
    "electrochemical_selectivity": "Selectivity",
    "energy_efficiency": "Energy efficiency",
    "transport_efficiency": "Transport efficiency",
    "score": "Score",
    "yield": "Yield",
    "conversion": "Conversion",
    "selectivity": "Selectivity",
    "byproduct_signal": "Byproduct",
    "safety_risk": "Risk",
    "product_in_organic": "Organic fraction",
    "product_in_aqueous": "Aqueous fraction",
    "purity": "Purity",
    "recovery": "Recovery",
    "crystal_yield": "Recovery",
    "crystal_purity": "Purity",
    "crystal_size": "Size index",
    "crystal_fines_fraction": "Fines",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def number(value):
    return "Unavailable" if value is None else f"{value:.6f}"


def table(headers, values):
    return "\n".join(
        [
            "| " + " | ".join(map(str, headers)) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
            *["| " + " | ".join(map(str, row)) + " |" for row in values],
        ]
    )


def equal_world(selected, field):
    groups = defaultdict(list)
    for row in selected:
        if row[field] not in ("", None):
            groups[row["world"]].append(float(row[field]))
    return fmean(fmean(values) for values in groups.values()) if groups else None


def main():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    source = ROOT / binding["report_root"]
    summary = read(source / "summary.json")
    metrics = rows(source / "session_metrics.csv")
    recommendations = rows(source / "EC_RX_RECOMMENDATIONS.csv")
    assert len(metrics) == 1380 and len(recommendations) == 180
    assert summary["counts"]["usable_forecasts"] == 298
    ec = read(source / "process/EC/coverage.json")
    rx = read(source / "process/RX/reading-summary.json")
    pa = read(source / "process/PA_P/reading-audit.json")["counts"]
    pa_extracted = read(source / "process/PA_P/index.json")["counts"]
    crystal = read(source / "process/C/verification.json")
    crystal_extracted = read(source / "process/C/extraction.json")
    process = [
        [
            "Electrochemistry",
            ec["assistant_reviewed_sessions"],
            ec["notebook_versions_loaded"],
            ec["public_events_loaded"],
            ec["mechanically_verified_quotes"],
        ],
        [
            "Reaction processing",
            rx["reviewed_sessions"],
            rx["notebook_versions_read"],
            rx["public_operations_read"],
            rx["verified_anchors"],
        ],
        [
            "Partitioning and purification",
            pa["P_sessions_close_read"] + pa["PA_sessions_close_read"],
            pa["notebook_versions_close_read"],
            pa_extracted["PA_public_events_extracted"] + pa_extracted["P_public_events_extracted"],
            pa["exact_quotes_verified"],
        ],
        [
            "Crystallization",
            crystal["reviewed_sessions"],
            crystal["reviewed_note_versions"],
            crystal_extracted["events"],
            crystal["verified_quotes"],
        ],
    ]
    assert [sum(row[i] for row in process) for i in range(1, 5)] == [300, 873, 31922, 1363]
    design = [
        ["Objectives and information", "Electrochemistry 90; reaction 90", 180, 0, 180],
        [
            "Formation of judgments",
            "Partitioning 45; purification 45; equilibrium 45; crystallization 45",
            90,
            90,
            180,
        ],
        ["Research opportunity", "Crystallization 30; equilibrium 30", 30, 30, 60],
        [
            "Matched chemical worlds",
            "Five aqueous network pairs, three sessions per world",
            0,
            30,
            30,
        ],
    ]
    lines = [
        "## Integrated six-system design and new 300-session evidence",
        "",
        "The four matrices organize complementary questions about inquiry, "
        "evidence and understanding. "
        "The new 300 and retained 150 constitute coverage, not a pooled performance denominator. "
        "Historical broad campaigns remain a further separate layer. Fixed "
        "worlds, shared observation "
        "keys and three fresh sessions per cell do not constitute independent population samples. "
        "No model sampling seed was controlled. All values below are descriptive.",
        "",
        table(["Matrix", "Coverage", "New", "Retained", "Planned"], design),
        "",
        "### New-block completion and failures",
        "",
        table(
            ["System", "Planned", "Complete chains", "Valid forecasts", "Source assays"],
            [
                [
                    SYSTEMS[r["system"]],
                    r["planned_sessions"],
                    r["completed_sessions"],
                    r["usable_forecasts"],
                    f"{r['completed_source_batches']}/{r['planned_source_batches']}",
                ]
                for r in summary["by_system"]
            ],
        ),
        "",
        "Total: 300 terminal sessions, 288 complete chains, 298 valid forecasts, "
        "3,379/3,420 source assays and 898/900 valid sealed stages. Ten purification sessions "
        "exhaust material; their 41 missing assays are scientific shortfalls. "
        "Two reaction forecasts "
        "are absent or invalid. Four service-only retries resolve interruptions without replacing "
        "scientific outcomes or adding units; interrupted attempts remain "
        "retained. Available forecasts "
        "from incomplete source histories remain in the tables, with their "
        "status in the portable data.",
        "",
    ]
    grouped = {}
    for r in rows(source / "failures.csv"):
        grouped.setdefault((r["system"], r["world"], r["repeat"], r["goal"], r["arm"]), set()).add(
            r["category"]
        )
    lines += [
        table(
            ["System", "World", "Repeat", "Goal", "Information", "Missing outcome"],
            [
                [
                    key[0],
                    key[1].split("-")[-1][1:],
                    key[2][-2:],
                    key[3],
                    key[4],
                    "Source assay shortfall" if key[0] == "P" else "Absent/invalid forecast",
                ]
                for key in sorted(grouped)
            ],
        ),
        "",
        "### Main goal and information contrasts",
        "",
        "Recommendation outcomes are independent retests. Prediction rows "
        "describe new interventions. "
        "Electrochemical means average all information conditions within each "
        "world; reaction means below "
        "use only optimization. Arrows in the preview connect group means, not a "
        "within-agent progression.",
        "",
    ]
    contrasts = []
    for label, source_rows, field, selector in [
        ("EC recommendation score", recommendations, "recommendation_score", {"system": "EC"}),
        ("EC recommendation yield", recommendations, "recommendation_yield", {"system": "EC"}),
        *[
            (f"EC {LABELS[response]} MAE", metrics, "mae", {"system": "EC", "response": response})
            for response in ("score", "selective_product_yield", "faradaic_efficiency")
        ],
        (
            "RX recommendation score",
            recommendations,
            "recommendation_score",
            {"system": "RX", "goal": "optimization"},
        ),
        (
            "RX recommendation yield",
            recommendations,
            "recommendation_yield",
            {"system": "RX", "goal": "optimization"},
        ),
        *[
            (
                f"RX {LABELS[response]} MAE",
                metrics,
                "mae",
                {"system": "RX", "goal": "optimization", "response": response},
            )
            for response in ("safety_risk", "conversion")
        ],
    ]:
        key, arms = (
            ("goal", ("discovery", "optimization"))
            if selector["system"] == "EC"
            else ("arm", ("Opaque", "Aligned"))
        )
        selected = [r for r in source_rows if all(r[k] == v for k, v in selector.items())]
        values = [equal_world([r for r in selected if r[key] == arm], field) for arm in arms]
        contrasts.append({"measure": label, "from": arms[0], "to": arms[1], "values": values})
    lines += [
        table(
            ["Measure", "From", "To", "From mean", "To mean"],
            [[r["measure"], r["from"], r["to"], *map(number, r["values"])] for r in contrasts],
        ),
        "",
    ]
    for system, title in SYSTEMS.items():
        lines += [
            f"### {title}: response-specific predictions",
            "",
            "MAE, coverage and width average available sessions within worlds, then weight "
            "the five worlds equally. N is valid/planned sessions. Missing outcomes are not zero. "
            + (
                "Intervals are nominal 90%. The two fractions are complementary."
                if system == "PA"
                else "Intervals are nominal 80%."
            ),
            "",
        ]
        selected = [r for r in summary["metrics"] if r["system"] == system]
        lines += [
            table(
                ["Condition", "Response", "N", "MAE", "Coverage", "Width"],
                [
                    [
                        (
                            (r["opportunity"] if system == "C" else r["arm"])
                            + (" / " + r["goal"] if system in ("EC", "RX") else "")
                        ),
                        LABELS[r["response"]],
                        f"{r['available_sessions']}/{r['planned_sessions']}",
                        *[
                            number(r[k + "_world_equal_available"])
                            for k in ("mae", "coverage", "interval_width")
                        ],
                    ]
                    for r in selected
                ],
            ),
            "",
            "Reference: " + selected[0]["reference_semantics"] + ".",
            "",
        ]
    lines += [
        "### Crystallization opportunity: world-specific uncertainty",
        "",
        "Both arms have three valid sessions in each world. Interval scores use alpha = 0.2; "
        "lower is better. These are prediction intervals, not confidence intervals on group means.",
        "",
    ]
    selected = [r for r in summary["metrics"] if r["system"] == "C"]
    lines += [
        table(
            ["Arm", "Response", "Mean interval score"],
            [
                [
                    r["opportunity"],
                    LABELS[r["response"]],
                    number(r["interval_score_world_equal_available"]),
                ]
                for r in selected
            ],
        ),
        "",
    ]
    lines += [
        table(
            ["World", "Arm", "Response", "MAE", "Coverage", "Width", "Interval score"],
            [
                [
                    w["world"][-2:],
                    r["opportunity"],
                    LABELS[r["response"]],
                    *[
                        number(w[k])
                        for k in ("mae", "coverage", "interval_width", "interval_score")
                    ],
                ]
                for r in selected
                if r["response"] in ("crystal_purity", "crystal_fines_fraction")
                for w in r["worlds"]
            ],
        ),
        "",
        "### Process reading coverage and evidential units",
        "",
        table(["Group", "Sessions", "Notes", "Operations", "Verified quotations"], process),
        "",
        "All 300 histories are read. The 899 nonempty sealed payloads include "
        "one invalid forecast; "
        "898 stages are valid and one forecast payload is absent. Counts refer "
        "to recording coverage, "
        "not discovery, hypothesis quality or abductive success. Cases are "
        "retrospective selections "
        "within full reading, with no independent human second-rater estimate. "
        "The older 92 action-linked "
        "windows retain their separate selection definition. Missing "
        "intermediate statements are not "
        "filled by later accounts.",
        "",
        "The main text uses four forms of positive evidence: an explicit "
        "expectation followed by its "
        "test; a relationship narrowed by a counterexample; an unsuccessful experiment producing a "
        "warranted withdrawal; and a judgment changing the next actual action. "
        "It separately traces "
        "unsupported extension and mistaken reconstruction of executed history. "
        "A session can support "
        "claims in more than one category. Neither successful recipes nor "
        "accurate numerical predictions "
        "are automatically counted as established explanations.",
        "",
        "The portable archive includes the full per-session readings and curated public scientific "
        "records for all new sessions, exact quotation/action anchors, "
        "execution-semantics checks, all "
        "planned response rows and failures. Native references differ by system, and no universal "
        "information ranking or cross-system scientific-ability score is inferred.",
        "",
    ]
    (DEST / "unified_matrices_analysis.md").write_text("\n".join(lines), encoding="utf-8")
    exported = {
        "binding": "work_ii.w2_267_unified_matrices",
        "source": binding["report_root"],
        "design": design,
        "counts": summary["counts"],
        "process_coverage": process,
        "main_contrasts": contrasts,
        "independent_human_coding": False,
        "archive_subtree": "unified_matrices/",
    }
    (DEST / "evidence/unified_matrices_summary.json").write_text(
        json.dumps(exported, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "Unified manuscript evidence: 300 sessions, 1,380 response rows, 180 "
        "EC/RX recommendations; no experiments.",
        flush=True,
    )


if __name__ == "__main__":
    main()
