"""Retrospective explanation histories and corrected-C distributions; no experiments."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "paper/venues/nature/evidence"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(name, value):
    (DEST / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def csv_write(name, rows):
    with (DEST / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def assays(events):
    return [
        e
        for e in events
        if e["transaction_status"] == "committed" and e["action"].get("instrument") == "final_assay"
    ]


def describe(values):
    ordered = sorted(values)

    def quantile(q):
        i = (len(ordered) - 1) * q
        lo = int(i)
        hi = min(lo + 1, len(ordered) - 1)
        return ordered[lo] + (ordered[hi] - ordered[lo]) * (i - lo)

    return {
        "n": len(values),
        "mean": fmean(values),
        "min": min(values),
        "q25": quantile(0.25),
        "median": quantile(0.5),
        "q75": quantile(0.75),
        "max": max(values),
    }


def main():
    current = read(ROOT / "configs/current.json")["work_ii"]["w2_257_inquiry_completion"]
    focal = read(DEST / "focal_equilibrium_study.json")["sessions"][0]
    process = read(DEST / "process_public_records.json")["sessions"]
    lookup = {(s["repeat"], s["id"]): s for s in process}
    # Fixed, retrospective panel: focal EQ and the four C cases already in the manuscript.
    selections = [
        ("repeat-01", "C-W05-Aligned"),
        ("repeat-02", "C-W05-Aligned"),
        ("repeat-02", "C-W02-Aligned"),
        ("repeat-03", "C-W03-Aligned"),
    ]
    selected = [lookup[k] for k in selections]
    eqnotes = [
        {
            "revision": n["revision"],
            "public_cursor": n["public_cursor"]["event_count"],
            "text": n["text"],
        }
        for n in focal["notebook_versions"]
    ]

    def anchor(notes, revision, snippet):
        note = next(n for n in notes if n["revision"] == revision)
        assert snippet in note["text"], snippet
        return {"revision": revision, "public_cursor": note["public_cursor"], "quote": snippet}

    histories = [
        {
            "history": "EQ-loading",
            "case": "Equilibrium study A",
            "kind": "initial expectation",
            "phenomenon": "Weak-acid/precipitation task before source observations",
            "first": anchor(
                eqnotes,
                1,
                (
                    "increasing total reagent concentration (moles divided by liquid "
                    "volume) should lower pH and reduce the acid dissociation fraction"
                ),
            ),
            "conditional_prediction": (
                "Increasing loading lowers pH and dissociation; possible precipitation onset."
            ),
            "tests": list(range(1, 8)),
            "observed": "Near-flat final assays at nominal reagent loading 0.05-0.8 M.",
            "revision": anchor(
                eqnotes,
                2,
                (
                    "a reagent-concentration effect is unresolved/unsupported rather "
                    "than proven absent"
                ),
            ),
            "terminal": anchor(eqnotes, 3, "H1 [not supported in tested scope]"),
            "standing": (
                "Expected observable trend unsupported in tested range; no global absence claim."
            ),
            "later_use": "Motivates proposed alternative feed explanation in revision 2.",
        },
        {
            "history": "EQ-component",
            "case": "Equilibrium study A",
            "kind": "candidate explanatory hypothesis",
            "phenomenon": "Six loading assays fail to show the initially expected trend",
            "first": anchor(
                eqnotes,
                2,
                (
                    "The selectable component 0, rather than anonymous limiting "
                    "reagent, may be the chemically relevant total acid loading"
                ),
            ),
            "conditional_prediction": (
                "Systematic pH/dissociation curve or threshold supports candidate;"
                " flat response favours fixed-background/weak coupling."
            ),
            "tests": list(range(8, 13)),
            "observed": "Component-labelled final loading 0.1-0.8 M remains near-flat.",
            "terminal": anchor(eqnotes, 3, "neither anonymous reagent concentration"),
            "standing": (
                "Agent abandons expected trend; implemented feed switch does not "
                "distinguish chemical identity."
            ),
            "later_use": (
                "Bounded plateau retained; fixed background, saturation/clamping "
                "and unresolved loading dependence remain alternatives."
            ),
            "semantic_limit": (
                "Both operation names add the same single feed in the retained "
                "execution version; not a distinct-acid intervention."
            ),
        },
        {
            "history": "EQ-background",
            "case": "Equilibrium study A",
            "kind": "explanatory alternative and empirical approximation",
            "phenomenon": "Near-flat responses across nominal loading and both feed commands",
            "first": anchor(
                eqnotes,
                2,
                "flat responses would favor a fixed-background or weakly coupled interpretation",
            ),
            "conditional_prediction": (
                "Within 0.4-0.8 M near-constant response; much lower loading or "
                "orthogonal solubility test could overturn approximation."
            ),
            "tests": list(range(8, 13)),
            "observed": (
                "Local plateau persists; suggested broader discrimination remains unexecuted."
            ),
            "terminal": anchor(
                eqnotes,
                3,
                (
                    "A reproducible shift under much lower loading, a broader dilution"
                    " range, or orthogonal solubility measurement would overturn the "
                    "near-constant approximation."
                ),
            ),
            "standing": "Empirical bounded support; mechanism unresolved in terminal source note.",
            "later_use": (
                "Q08 rationale favours 'experimentally supported fixed acidic "
                "background'; estimate 0.085, 80% interval [0.035,0.350], "
                "reference mean 0.716032."
            ),
            "untested_proposal": (
                "Broader dilution/orthogonal solubility; no subsequent source "
                "operation after terminal revision."
            ),
        },
    ]
    specifications = [
        (
            "C-charge",
            "Lower-charge study",
            "prospective empirical expectation",
            5,
            "A further reduction to 0.02 mol",
            "Lower loading crosses fines 0.50 while retaining recovery above 0.368.",
            "H5 [supported by final test]",
            (
                "Local recipe improvement supported; concentration and "
                "catalyst/reagent ratio not separated."
            ),
            "Recommend completed batch 12.",
            [11, 12],
        ),
        (
            "C-interpolation",
            "Interpolation study",
            "prospective empirical expectation",
            3,
            "an intermediate 0.065 L loading",
            "Intermediate volume retains recovery and restores fines below 0.50.",
            "H3 [disconfirmed as a simple interpolation]",
            "Expectation retracted after fines rise; monotonicity and repeatability unresolved.",
            "Recommend lifecycle batch 4.",
            [4, 11, 12],
        ),
    ]
    for session, spec in zip(selected[:2], specifications, strict=True):
        key, label, kind, rev, first, prediction, terminal, standing, use, batches = spec
        notes = session["versions"]
        histories.append(
            {
                "history": key,
                "case": label,
                "kind": kind,
                "phenomenon": "Prior batch outcomes leave a recovery/fines tradeoff",
                "first": anchor(notes, rev, first),
                "conditional_prediction": prediction,
                "tests": batches,
                "observed": [e for e in assays(session["events"]) if e["batch"] in batches],
                "terminal": anchor(notes, notes[-1]["revision"], terminal),
                "standing": standing,
                "later_use": anchor(notes, notes[-1]["revision"], use),
                "identity": {k: session[k] for k in ("repeat", "id", "cohort")},
            }
        )
    # Rejected-operation cases retain every version, including terminal use; no count of abduction.
    for session, label in zip(selected[2:], ("Seed case B", "Seed case C"), strict=True):
        histories.append(
            {
                "history": label,
                "case": label,
                "kind": "execution-evidence boundary",
                "identity": {k: session[k] for k in ("repeat", "id", "cohort")},
                "phenomenon": "Large-seed intervention proposed but requests rejected",
                "conditional_prediction": None,
                "conditional_prediction_status": (
                    "Not assigned a new explanatory conditional by this analysis; full"
                    " public versions retained."
                ),
                "versions": session["versions"],
                "seed_events": [
                    e for e in session["events"] if e["action"].get("operation") == "seed_crystals"
                ],
                "standing": "Recognizes high-dose test unexecuted"
                if label.endswith("B")
                else "Treats rejected high-dose request as executed negative evidence",
            }
        )
    semantics_paths = [
        "src/chemworld/runtime/primitive_services.py",
        "src/chemworld/runtime/species.py",
        "src/chemworld/runtime/observation_services.py",
        "configs/scenarios/mechanism_scenarios.yaml",
    ]
    sources = {
        p: subprocess.check_output(
            ["git", "show", f"{current['source_commit']}:{p}"], cwd=ROOT
        ).decode("utf-8")
        for p in semantics_paths
    }
    assert (
        'return self._add_feed(state, {feeds[component]: float(action["amount_mol"])})'
        in sources[semantics_paths[0]]
    )
    card = sources[semantics_paths[3]].split("  - card_id:")[1]
    assert "A: 1.0" in card and "Cat_active: 0.01" in card and "P: 0.0" in card
    assert (
        "acid_total = max(self.species_view.initial_reactant_amount(state), 0.0)"
        in sources[semantics_paths[2]]
    )
    semantic_record = {
        "source_commit": current["source_commit"],
        "files": semantics_paths,
        "mechanism": "simple_batch_reaction",
        "feed": "A",
        "component_selector": 0,
        "derivation": (
            "Single positive non-catalytic initial feed A; "
            "reagent_charge_amounts excludes catalyst. add_component(0) "
            "selects A; both update the initial-amount ledger. Equilibrium "
            "acid_total reads initial_reactant_amount. The two names do not "
            "change acid identity at equal amount."
        ),
        "scope": (
            "Read-only inspection of retained execution source and focal "
            "trajectory mechanism_id; no simulator rerun or changed runtime."
        ),
        "scientific_implication": (
            "Candidate generation and test intention observed; chemical "
            "identity discrimination not implemented. Plateau observations "
            "constrain local response but do not identify fixed-background "
            "mechanism."
        ),
    }
    trajectory = (
        Path(current["run_root"])
        / "repeat-01/EQ-W01-Research/sources/EQ-W01--Opaque/trajectory.jsonl"
    )
    if trajectory.exists():
        with trajectory.open(encoding="utf-8") as stream:
            first_event = json.loads(next(stream))
        assert first_event["mechanism_id"] == semantic_record["mechanism"]
        assert first_event["agent_metadata"]["git_commit"] == current["source_commit"]
    qtext = json.dumps(focal["posttests"]["Q"], ensure_ascii=False)
    assert (
        "The point estimate still favors the experimentally supported fixed acidic background"
        in qtext
    )
    write(
        "explanation_histories.json",
        {
            "design": (
                "Retrospective fixed panel of the existing focal EQ case and four "
                "previously illustrated corrected-C cases. Seven related judgment "
                "histories across five sessions; not a prevalence sample. "
                "Selection is not independent of earlier interpretation."
            ),
            "cohorts": (
                "EQ study A belongs to the separate 30-session opportunity block, "
                "not the 90-session process-window cohort."
            ),
            "review": "Single analyst; quotes and temporal anchors checked, no independent coder.",
            "histories": histories,
            "equilibrium_all_versions": eqnotes,
            "crystallization_all_versions": [
                {"repeat": s["repeat"], "id": s["id"], "versions": s["versions"]} for s in selected
            ],
            "operation_semantics": semantic_record,
        },
    )
    eqrows = []
    for e in assays(focal["public_events"]):
        actions = [
            x["action"]
            for x in focal["public_events"]
            if x["batch"] == e["batch"] and x["transaction_status"] == "committed"
        ]
        volume = sum(a.get("volume_L", 0) for a in actions if a["operation"] == "add_solvent")
        loading = sum(
            a.get("amount_mol", 0)
            for a in actions
            if a["operation"] in ("add_reagent", "add_component")
        )
        eqrows.append(
            {
                "batch": e["batch"],
                "cursor": e["cursor"],
                "feed_command": "component"
                if any(a["operation"] == "add_component" for a in actions)
                else "reagent",
                "nominal_added_mol": loading,
                "total_added_solvent_L": volume,
                "nominal_concentration_M": loading / volume,
                **{
                    k: e["observations"][k]
                    for k in ("pH_normalized", "acid_dissociation_fraction", "precipitation_signal")
                },
            }
        )
    assert len(eqrows) == 12
    csv_write("focal_equilibrium_assays.csv", eqrows)
    refs = read(ROOT / current["source_references"])
    valid = [s for s in refs["sessions"] if s["valid_Q"]]
    source_rows, query_rows, session_rows = [], [], []
    metrics = ("crystal_yield", "crystal_purity", "crystal_size", "crystal_fines_fraction")
    for session in valid:
        identity = {k: session[k] for k in ("repeat", "id", "world", "arm")}
        events = assays(lookup[(session["repeat"], session["id"])]["events"])
        for metric in metrics:
            assert (
                abs(
                    fmean(e["observations"][metric] for e in events)
                    - session["queries"][0]["source_mean"][metric]
                )
                < 1e-12
            )
        source_rows += [
            {**identity, "batch": e["batch"], **{k: e["observations"][k] for k in metrics}}
            for e in events
        ]
        for q in session["queries"]:
            for metric in metrics:
                query_rows.append(
                    {
                        **identity,
                        "query": q["query_id"],
                        "response": metric,
                        "source_mean": q["source_mean"][metric],
                        "same_solvent_mean": q["same_solvent_mean"][metric],
                        "prediction": q["agent"][metric],
                        "truth": q["reference_truth"][metric],
                        "signed_error": q["agent"][metric] - q["reference_truth"][metric],
                        "fallback": q["fallback"],
                    }
                )
        for metric in metrics:
            qrows = [
                r
                for r in query_rows
                if r["repeat"] == session["repeat"]
                and r["id"] == session["id"]
                and r["response"] == metric
            ]
            session_rows.append(
                {
                    **identity,
                    "response": metric,
                    "source_mean": fmean(e["observations"][metric] for e in events),
                    "target_mean": fmean(q["truth"] for q in qrows),
                    "prediction_mean": fmean(q["prediction"] for q in qrows),
                    "signed_error": fmean(q["signed_error"] for q in qrows),
                    **{
                        method + "_mae": session["mae"][method][metric]
                        for method in ("agent", "source_mean", "same_solvent_mean")
                    },
                }
            )
    assert len(valid) == 42 and len(query_rows) == 504 * 4
    csv_write("corrected_c_source_assays.csv", source_rows)
    csv_write("corrected_c_query_responses.csv", query_rows)
    csv_write("corrected_c_session_responses.csv", session_rows)
    summary = {
        "scope": (
            "42/45 corrected-C sessions with valid Q; all available source "
            "assays in those sessions. Three missing Q excluded from numerical"
            " comparisons, not counted as zero. Not historical C."
        ),
        "source_assays": len(source_rows),
        "queries": 504,
        "metrics": {},
    }
    for metric in metrics:
        rows = [r for r in query_rows if r["response"] == metric]
        ss = [r for r in session_rows if r["response"] == metric]
        summary["metrics"][metric] = {
            "source_observations": describe([r[metric] for r in source_rows]),
            "target_values_with_repeated_queries": describe([r["truth"] for r in rows]),
            "predictions": describe([r["prediction"] for r in rows]),
            "signed_error": describe([r["signed_error"] for r in rows]),
            "predictions_below_truth": sum(r["signed_error"] < 0 for r in rows),
            "equal_world": {
                k: fmean(
                    fmean(r[k] for r in ss if r["world"] == w)
                    for w in sorted({r["world"] for r in ss})
                )
                for k in (
                    "source_mean",
                    "target_mean",
                    "prediction_mean",
                    "signed_error",
                    "agent_mae",
                    "source_mean_mae",
                    "same_solvent_mean_mae",
                )
            },
        }
    write("corrected_c_distribution_summary.json", summary)
    for metric in metrics:
        reference = next(g for g in refs["groups"] if g["arm"] == "all")["equal_world_mae"]
        for method in ("agent", "source_mean", "same_solvent_mean"):
            assert (
                abs(
                    summary["metrics"][metric]["equal_world"][method + "_mae"]
                    - reference[method][metric]
                )
                < 1e-12
            )
    print(
        (
            "Retained analysis: 7 histories / 5 sessions; 12 focal assays; 42 "
            "valid C sessions / 504 queries."
        ),
        flush=True,
    )
    print(json.dumps(summary["metrics"]["crystal_purity"], ensure_ascii=True), flush=True)


if __name__ == "__main__":
    main()
