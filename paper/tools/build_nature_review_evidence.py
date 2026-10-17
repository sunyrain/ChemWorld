"""Expose retained manuscript evidence at query, session and process-window levels."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from statistics import fmean
from zipfile import ZIP_DEFLATED, ZipFile

from build_abductive_evidence import main as build_explanation_evidence
from build_inquiry_revision_evidence import main as build_inquiry_revision
from build_matched_inquiry_evidence import main as build_matched_evidence
from build_unified_manuscript_evidence import main as build_unified_evidence

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.analyze_inquiry_semantics import validate_record  # noqa: E402

DEST = ROOT / "paper/venues/nature/evidence"
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
RESPONSES = ("pH_normalized", "acid_dissociation_fraction", "precipitation_signal")
GROUPS = ("all", "dilute", "other")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(name, data):
    (DEST / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def csv_file(name, rows):
    with (DEST / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_257_inquiry_completion"]
    opp = read(ROOT / binding["summary"])
    source = (ROOT / binding["summary"]).parent
    design_path = Path(binding["run_root"]) / "design.json"
    if design_path.exists():
        design = read(design_path)
        protocol = {
            "queries": design["eq_config"]["queries"],
            "evaluation_prompts": design["evaluation_prompts"],
            "source": "Public assessment subset of the retained execution design",
        }
        write("assessment_protocol.json", protocol)
    else:
        # The exported public snapshot keeps a checkout usable without private run folders.
        protocol = read(DEST / "assessment_protocol.json")
    assert [q["query_id"] for q in protocol["queries"]] == [f"Q{i:02d}" for i in range(1, 13)]
    queries, sessions, contexts, focal = [], [], [], []
    for row in opp["sessions"]:
        full = read(source / "sessions" / row["repeat"] / (row["id"] + ".json"))
        identity = {key: row[key] for key in ("repeat", "id", "world", "arm", "opportunity")}
        contexts.append({**identity, "initial_public_context": full["initial_public_context"]})
        assert row["arm"] == "Opaque"
        assert (
            full["initial_public_context"]["task_contract"]["research_brief"]["prior_record"]
            is None
        )
        scores = row.get("scores")
        for group in GROUPS:
            for response in RESPONSES:
                values = scores["groups"][group]["metrics"][response] if scores else {}
                sessions.append(
                    {
                        **identity,
                        "query_group": group,
                        "response": response,
                        "valid": bool(scores),
                        **{
                            k: values.get(k)
                            for k in ("mae", "coverage80", "width80", "interval_score80")
                        },
                    }
                )
        if scores:
            for query in scores["queries"]:
                for response, values in query["metrics"].items():
                    assert (
                        abs(values["mae"] - abs(values["estimate"] - values["reference_mean"]))
                        < 1e-12
                    )
                    queries.append(
                        {
                            **identity,
                            "query_id": query["query_id"],
                            "dilute": query["dilute"],
                            "response": response,
                            **{
                                k: values[k]
                                for k in (
                                    "estimate",
                                    "lower80",
                                    "upper80",
                                    "reference_mean",
                                    "mae",
                                    "coverage80",
                                    "width80",
                                    "interval_score80",
                                )
                            },
                            **{
                                f"reference_observation_{i}": v
                                for i, v in enumerate(values["reference_observations"], 1)
                            },
                        }
                    )
        if row["repeat"] == "repeat-01" and row["world"] == "W01":
            focal.append(
                {
                    **identity,
                    **{
                        k: full[k]
                        for k in ("notebook_versions", "public_events", "posttests", "scores")
                    },
                }
            )
    assert len(queries) == 29 * 12 * 3 and len(sessions) == 30 * 3 * 3
    for repeat in ("repeat-01", "repeat-02", "repeat-03"):
        for world in ("W01", "W02", "W03", "W04", "W05"):
            pair = [
                deepcopy(c["initial_public_context"])
                for c in contexts
                if c["repeat"] == repeat and c["world"] == world
            ]
            for c in pair:
                c["initial_public_state"]["campaign_state"].pop("campaign_id")
            assert len(pair) == 2 and pair[0] == pair[1]
    worlds = []
    for world in ("W01", "W02", "W03", "W04", "W05"):
        for arm in ("Research", "NoResearch"):
            for group in GROUPS:
                for response in RESPONSES:
                    selected = [
                        s
                        for s in sessions
                        if s["world"] == world
                        and s["opportunity"] == arm
                        and s["query_group"] == group
                        and s["response"] == response
                        and s["valid"]
                    ]
                    worlds.append(
                        {
                            "world": world,
                            "opportunity": arm,
                            "query_group": group,
                            "response": response,
                            "valid_sessions": len(selected),
                            **{
                                k: fmean(s[k] for s in selected)
                                for k in ("mae", "coverage80", "width80", "interval_score80")
                            },
                        }
                    )
    means = opp["comparison"]["equal_world_means"]
    for arm in means:
        for group in GROUPS:
            for response in RESPONSES:
                selected = [
                    w
                    for w in worlds
                    if w["opportunity"] == arm
                    and w["query_group"] == group
                    and w["response"] == response
                ]
                for metric in ("mae", "coverage80", "width80", "interval_score80"):
                    assert (
                        abs(
                            fmean(w[metric] for w in selected)
                            - means[arm][group]["metrics"][response][metric]
                        )
                        < 1e-12
                    )
    csv_file("opportunity_query_predictions.csv", queries)
    csv_file("opportunity_session_responses.csv", sessions)
    csv_file("opportunity_world_responses.csv", worlds)
    write(
        "public_inputs.json",
        {
            "condition": "Opaque",
            "records": contexts,
            "parity": "15/15 pairs equal after removing only the non-scientific campaign ID",
        },
    )
    write(
        "focal_equilibrium_study.json",
        {
            "label": "Equilibrium study A",
            "sessions": focal,
            "identity_note": (
                "New opportunity W01 repeat 1; not the historical 0.092/0.51730 example."
            ),
        },
    )
    records, eligibility, windows = [], [], []
    for directory, system in [
        ("inquiry-trajectories-20261014", "EQ"),
        ("c-recovery-aligned-20261014", "C"),
    ]:
        base = REPORTS / directory
        codes = {
            (r["repeat"], r["id"], r["from_revision"]): r
            for r in read(base / "semantic_analysis.json")["records"]
            if r["id"].startswith(system + "-")
        }
        for path in sorted((base / "sessions").glob("repeat-*/" + system + "-*.json")):
            s = read(path)
            records.append(s)
            for earlier, later in zip(s["versions"][:-1], s["versions"][1:], strict=True):
                assays = [
                    e
                    for e in s["events"]
                    if earlier["public_cursor"] < e["cursor"] <= later["public_cursor"]
                    and e["transaction_status"] == "committed"
                    and e["action"].get("instrument") == "final_assay"
                ]
                subsequent = [
                    e
                    for e in s["events"]
                    if e["cursor"] > later["public_cursor"]
                    and e["transaction_status"] == "committed"
                    and e["action"]["operation"] not in ("measure", "terminate")
                ]
                eligible = bool(assays and subsequent)
                assert eligible == earlier["structural_feedback_opportunity"]
                key = (s["repeat"], s["id"], earlier["revision"])
                assert eligible == (key in codes)
                eligibility.append(
                    {
                        "system": system,
                        "repeat": s["repeat"],
                        "id": s["id"],
                        "from_revision": earlier["revision"],
                        "to_revision": later["revision"],
                        "earlier_cursor": earlier["public_cursor"],
                        "later_cursor": later["public_cursor"],
                        "new_final_assays": len(assays),
                        "subsequent_committed_research_actions": len(subsequent),
                        "eligible": eligible,
                        "exclusion": "" if eligible else "no_subsequent_committed_research_action",
                        "action_link": codes[key]["action_link"] if eligible else "not_coded",
                    }
                )
                if eligible:
                    verified = validate_record(codes[key], s)
                    windows.append(
                        {
                            **verified,
                            "earlier_text": earlier["text"],
                            "later_text": later["text"],
                            "source_file": path.relative_to(ROOT).as_posix(),
                        }
                    )
    assert len(records) == 90 and len(eligibility) == 178 and len(windows) == 92
    assert sum(w["quotes_verified"] for w in windows) == 182
    assert all(e["new_final_assays"] > 0 for e in eligibility)
    csv_file("process_window_eligibility.csv", eligibility)
    write(
        "process_windows.json",
        {
            "review_status": "single-analyst source verification; no independent second rater",
            "records": windows,
        },
    )
    write("process_public_records.json", {"sessions": records})
    counts = {
        system: {
            "adjacent_pairs": sum(e["system"] == system for e in eligibility),
            "included": sum(e["system"] == system and e["eligible"] for e in eligibility),
            "no_continuation": sum(
                e["system"] == system and not e["eligible"] for e in eligibility
            ),
        }
        for system in ("EQ", "C")
    }
    differences = {
        r: means["Research"]["dilute"]["metrics"][r]["mae"]
        - means["NoResearch"]["dilute"]["metrics"][r]["mae"]
        for r in RESPONSES
    }
    summary = {
        "scope": "Retrospective decomposition of retained evidence; no new experiments",
        "information_condition": "Opaque",
        "planned_sessions": 30,
        "valid_forecasts": 29,
        "query_response_rows": len(queries),
        "session_group_response_rows": len(sessions),
        "world_group_response_rows": len(worlds),
        "public_input_pairs_verified": 15,
        "equal_world_means": means,
        "dilute_mae_differences": differences,
        "dissociation_share_of_dilute_macro_difference": differences[RESPONSES[1]]
        / sum(differences.values()),
        "process_sessions": len(records),
        "notebook_versions": sum(len(s["versions"]) for s in records),
        "adjacent_note_pairs": len(eligibility),
        "eligible_windows": len(windows),
        "excluded_no_continuation": len(eligibility) - len(windows),
        "by_system": counts,
        "selected_plan_links": dict(Counter(w["action_link"] for w in windows)),
        "verified_quotes": 182,
        "independent_second_rater": False,
    }
    write("summary.json", summary)
    (DEST / "README.md").write_text(
        "# Retained evidence for manuscript review\n\n"
        "This package exposes existing evidence, not additional experiments or new "
        "independent coding. "
        "The comparison is Opaque: no instance archival relationship was supplied. "
        "All 15 scientific-input "
        "pairs match after excluding only the campaign identifier. The exact public "
        "contracts, initial "
        "states and material information are in public_inputs.json.\n\n"
        "- assessment_protocol.json: exact public query actions and retained evaluation "
        "prompts, excluding private world parameters and provider configuration.\n"
        "- opportunity_query_predictions.csv: 1,044 query-response rows, including "
        "estimates, 80% intervals, "
        "held-out means and all five reference observations for 29 valid forecasts. Truth was "
        "not given to agents.\n"
        "- opportunity_session_responses.csv: all 270 planned session/group/response "
        "cells; missing values "
        "remain empty, not zero.\n"
        "- opportunity_world_responses.csv: 90 world/group/response means, with "
        "valid-session counts.\n"
        "- focal_equilibrium_study.json: both matched sessions for Equilibrium study "
        "A, including source "
        "operations, full public notebook versions and sealed accounts. This is the "
        "new 0.085/0.716032 "
        "case, not the historical 0.092/0.51730 case.\n"
        "- process_window_eligibility.csv: all 178 adjacent version pairs across 90 "
        "sessions. All have "
        "new final assays; 92 also have a committed non-measurement/non-termination "
        "operation after the "
        "later note. The remaining 86 lack that continuation.\n"
        "- process_windows.json: all 92 retained codes, full adjacent notes, exact "
        "quotation locations, "
        "operation cursors, selected execution anchors and source paths.\n"
        "- process_public_records.json: all 90 public session histories, including "
        "rejected operations "
        "and the 86 pairs excluded from the action-linked window definition.\n"
        "- summary.json: exact counts, means and decomposition.\n\n"
        "Window eligibility is determined from timing, new assays and later "
        "committed actions before "
        "semantic plan matching. It does not test whether a particular plan "
        "succeeds. Nevertheless, "
        "requiring subsequent committed research conditions the sample on continued activity. The "
        "selected immediate-plan labels do not enumerate every proposal; partly "
        "matched, rejected or "
        "unexecuted proposals remain in full notes and operation records. Terminal "
        "revisions are not "
        "classified as no learning. A second independent coder has not been added.\n\n"
        "Reproduce from repository: uv run --no-sync python "
        "paper/tools/build_nature_review_evidence.py. "
        "The producer recomputes world means and window eligibility, checks all 182 quotations and "
        "their temporal anchors, and preserves the missing forecast. "
        "This producer also invokes build_abductive_evidence.py for the seven selected "
        "judgment histories (explanation_histories.json), focal_equilibrium_assays.csv and "
        "corrected_c_source_assays.csv, corrected_c_query_responses.csv, "
        "corrected_c_session_responses.csv and corrected_c_distribution_summary.json. "
        "These are retrospective, single-analyst derived analyses, not new experiments "
        "or full-cohort explanatory coding. Run plot_abductive_evidence.py for the six "
        "retained data-derived figures. All current main and Extended Data artwork is "
        "explicitly labelled ImageGen preview; new matrices are governed by their exact tables.\n",
        encoding="utf-8",
    )
    build_explanation_evidence()
    build_matched_evidence()
    build_unified_evidence()
    build_inquiry_revision()
    unified = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    unified_root = ROOT / unified["report_root"]
    with (DEST / "README.md").open("a", encoding="utf-8") as stream:
        stream.write(
            "\n## Integrated matrices and new 300-session evidence\n\n"
            "The new primary block is separate from the older evidence described above. "
            "Four matrices cover 450 planned sessions: 300 new and 150 retained. "
            "The new block retains 288 complete chains, 298 valid forecasts, "
            "3,379/3,420 source assays and 898/900 valid stages. Ten material-exhausted "
            "purification histories and two absent/invalid reaction forecasts remain included. "
            "Four service-only retries preserve their interrupted attempts.\n\n"
            "unified_matrices_summary.json supplies machine-recomputed main contrasts and "
            "coverage. In the ZIP, unified_matrices/ contains the entire curated report "
            "tree: 1,380 planned session-response rows, recommendations, all failures, "
            "all 300 public-history readings and their scientific source extracts. "
            "No raw provider envelopes or credentials are included. Reading spans 873 "
            "notes, 31,922 operations and 1,363 verified quotations; it is not an "
            "abduction rate or independent human coding.\n\n"
            "Repository source: ../../../../" + unified["report_root"] + "/PROCESS_REVIEW.md. "
            "Compilation does not rerun experiments or change evidence status.\n"
            "The new_c_source_references CSV/JSON expose existing source-only references "
            "for the same fifteen crystallization Research sessions (179 eligible response "
            "records among 180 assays). core_history_index.json maps the main study labels "
            "to trajectories and critical times. These are retrospective evidence summaries, "
            "not additional sessions or independent human validation.\n"
        )
    archive = ROOT / "output/paper/chemworld-review-evidence.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for path in sorted(DEST.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(DEST).as_posix())
        for path in sorted(unified_root.rglob("*")):
            if path.is_file() and path.suffix in {".md", ".json", ".csv"}:
                bundle.write(path, "unified_matrices/" + path.relative_to(unified_root).as_posix())
    print(
        f"Retained evidence: {len(queries)} query rows; {len(sessions)} session-response cells; "
        f"{len(eligibility)} adjacent pairs / {len(windows)} windows; 182 checked quotes; "
        "15 matched scientific-input pairs. No new experiments.",
        flush=True,
    )


if __name__ == "__main__":
    main()
