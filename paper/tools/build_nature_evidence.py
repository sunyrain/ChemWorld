"""Build manuscript tables from retained evidence; no experiments or image generation."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "paper/venues/nature"
REPORTS = ROOT / "workstreams/flagship_tasks/reports"
METRICS = {
    "crystal_yield": "Recovery",
    "crystal_purity": "Purity",
    "crystal_size": "Size index",
    "crystal_fines_fraction": "Fines",
}
EQ_RESPONSES = {
    "pH_normalized": "Normalized pH",
    "acid_dissociation_fraction": "Dissociation",
    "precipitation_signal": "Precipitation",
}


def response_tables(means):
    """Expose response contributions and repeat variation, retaining missing cells."""
    with (DEST / "evidence/opportunity_session_responses.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        sessions = list(csv.DictReader(stream))
    with (DEST / "evidence/opportunity_world_responses.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        worlds = list(csv.DictReader(stream))
    assert len(sessions) == 270 and len(worlds) == 90
    lines = [
        "### Response-specific point errors",
        "",
        "Within each world, valid sessions receive equal weight; worlds then receive equal "
        "weight. The macro error averages the three response errors. Differences are "
        "Research minus NoResearch, so positive values favour NoResearch. All/dilute/other "
        "contain twelve/three/nine queries. These are descriptive repeated-session results, "
        "not estimates from independent world samples.",
        "",
        table(
            ["Group", "Response", "Research", "NoResearch", "Difference"],
            [
                [
                    group,
                    label,
                    fmt(means["Research"][group]["metrics"][response]["mae"]),
                    fmt(means["NoResearch"][group]["metrics"][response]["mae"]),
                    fmt(
                        means["Research"][group]["metrics"][response]["mae"]
                        - means["NoResearch"][group]["metrics"][response]["mae"]
                    ),
                ]
                for group in ("all", "dilute", "other")
                for response, label in EQ_RESPONSES.items()
            ],
        ),
        "",
        "Dissociation accounts for 85.2% of the dilute macro-MAE increase, calculated "
        "as its response difference divided by the sum of the three response differences. "
        "This decomposition is not a claim that every session or query deteriorates. "
        "Interval outcomes below also distinguish point prediction from uncertainty quality.",
        "",
    ]
    for group in ("all", "dilute", "other"):
        lookup = {
            (r["world"], r["opportunity"], r["response"]): r
            for r in worlds
            if r["query_group"] == group
        }
        lines += [
            f"### Within-world response means: {group} queries",
            "",
            table(
                ["World", "Arm", "Valid n/3", *EQ_RESPONSES.values()],
                [
                    [
                        world[1:],
                        arm,
                        lookup[world, arm, "pH_normalized"]["valid_sessions"],
                        *[
                            fmt(float(lookup[world, arm, response]["mae"]))
                            for response in EQ_RESPONSES
                        ],
                    ]
                    for world in ("W01", "W02", "W03", "W04", "W05")
                    for arm in ("Research", "NoResearch")
                ],
            ),
            "",
        ]
    for group in ("all", "dilute"):
        lookup = {
            (r["world"], r["opportunity"], r["repeat"], r["response"]): r
            for r in sessions
            if r["query_group"] == group
        }
        lines += [
            f"### Every planned session: {group} response errors",
            "",
            table(
                ["World", "Arm", "Repeat", *EQ_RESPONSES.values()],
                [
                    [
                        world[1:],
                        arm,
                        repeat[-1],
                        *[
                            fmt(float(r["mae"]) if r["mae"] else None)
                            for response in EQ_RESPONSES
                            for r in [lookup[world, arm, repeat, response]]
                        ],
                    ]
                    for world in ("W01", "W02", "W03", "W04", "W05")
                    for arm in ("Research", "NoResearch")
                    for repeat in ("repeat-01", "repeat-02", "repeat-03")
                ],
            ),
            "",
        ]
    lines += [
        "The review archive also supplies every session's other-query results, coverage, "
        "interval width and interval score. Its 1,044 query-response rows retain the point "
        "estimate, stated 80% interval and withheld reference mean for all 29 valid forecasts. "
        "Nine empty session/group/response cells belong to the single missing forecast; "
        "they are neither zero errors nor additional failed sessions.",
        "",
    ]
    return lines


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", r"\|").replace("\n", " ")

    return "\n".join(
        [
            "| " + " | ".join(map(cell, headers)) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        + ["| " + " | ".join(map(cell, row)) + " |" for row in rows]
    )


def fmt(value):
    return "-" if value is None else f"{value:.6f}"


def identity(row):
    return row["world"][1:] + "/" + row["arm"][0] + "/" + row["repeat"][-1]


def failure_label(row):
    failure = row.get("failure") or {}
    message = failure.get("message", "")
    if "max_provider_error_events" in message:
        return "Source stopped at the configured provider-error limit"
    if "resource accounting" in message:
        return "Source stopped when resource accounting could not be validated"
    if message == "provider_failure":
        return "Provider failure during " + failure.get("stage", "assessment")
    return message or "Assessment payload missing"


def retained_tables():
    lines = [
        "## Historical broad-study tables",
        "",
        "These 34 tables preserve the original numerical cells and denominators. "
        "They do not describe the corrected crystallization or opportunity cohorts. "
        "Historical crystallization recovery diagnostics retain their original protocol "
        "limitations. The original broad study comprises 300 campaigns; the five-model "
        "equilibrium subset overlaps that count. Earlier figure labels in table captions "
        "refer to the historical report, not current preview figures.",
        "",
    ]
    legacy = (ROOT / "paper/venues/ncs/supplementary_en.md").read_text(encoding="utf-8")
    legacy_lines = legacy.splitlines()
    heading = ""
    counter = 0
    i = 0
    while i < len(legacy_lines):
        line = legacy_lines[i]
        if line.startswith("#"):
            heading = line.lstrip("# ")
        if (
            line.startswith("|")
            and i + 1 < len(legacy_lines)
            and re.match(r"\|[ :|\-]+$", legacy_lines[i + 1])
        ):
            previous = i - 1
            while previous >= 0 and not legacy_lines[previous].strip():
                previous -= 1
            caption = legacy_lines[previous] if previous >= 0 else ""
            table = []
            while i < len(legacy_lines) and legacy_lines[i].startswith("|"):
                table.append(legacy_lines[i])
                i += 1
            counter += 1
            if counter == 3:
                lines += [
                    "Tables 3-18 report MAE / empirical interval coverage (%), averaged "
                    "over five world sessions. All scheduled sessions remain included. "
                    "PA intervals are nominally 90%; all others are 80%. Response scales "
                    "and reference targets differ across systems.",
                    "",
                ]
            lines += [f"### Retained table {counter}: {heading}", ""]
            if caption.startswith(("**Table", "**Supplementary Table")):
                lines += [caption, ""]
            if counter == 33:
                lines += [
                    "For each campaign, prediction error decomposes as "
                    r"$\operatorname{MSE}=\overline{p-y}^{\,2}+"
                    r"\frac{1}{12}\sum_i[(p_i-\bar p)-(y_i-\bar y)]^2$. "
                    "Centred RMSE is the square root of the second term. Demeaning "
                    "uses withheld references for diagnosis, not as an available predictor.",
                    "",
                ]
            lines += ["\n".join(table), ""]
            note_start = i
            while note_start < len(legacy_lines) and not legacy_lines[note_start].strip():
                note_start += 1
            note = []
            while note_start < len(legacy_lines):
                value = legacy_lines[note_start]
                if not value.strip() or value.startswith(
                    ("#", "|", "![", "**Table", "**Supplementary")
                ):
                    break
                note.append(value)
                note_start += 1
            if note:
                note_text = " ".join(note)
                note_text = re.sub(
                    r"The source-observation band in Supplementary Figure S8"
                    r".*?specific to each campaign\.",
                    "The displayed source ranges are specific to each campaign.",
                    note_text,
                )
                note_text = re.sub(r"Figure 4b shows.*?separately\.", "", note_text).strip()
                note_text = note_text.replace(
                    "Public explanation categories and K1/Q chronology are in section C.4.",
                    "Public explanation categories appear in retained table 21 above.",
                )
                lines += [note_text, ""]
            continue
        i += 1
    lines += [
        "## Executed process relationships",
        "",
        "The following equations describe the retained virtual-world laws, not mechanisms "
        "inferred by the participants. The initial-charge final-assay recovery formula below "
        "also describes the checked full-process observation route in the repeated cohort. "
        "The internal stage-recovery metric and mismatched participant description are "
        "distinguished above; they must not be substituted for the observed/scored response.",
        "",
    ]
    for start, end in (("## H.1 ", "## H.2 "), ("## H.3 ", "## H.4 ")):
        section = legacy.split(start, 1)[1].split(end, 1)[0]
        section = "### " + section
        section = section.replace(
            "The concentration in Figure 4a and Supplementary Figure S8a",
            "Nominal concentration in the retained source comparisons",
        )
        section = section.replace("Appendix G separately tests", "The retained diagnostics test")
        lines += [section.strip(), ""]
    return lines, counter


def main():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_257_inquiry_completion"]
    opportunity = read(ROOT / binding["summary"])
    references = read(ROOT / binding["source_references"])
    paths = read(ROOT / binding["research_paths"])
    cs = read(ROOT / binding["corrected_c_semantics"])
    c_root = (ROOT / binding["corrected_c_semantics"]).parent
    c_summary = read(c_root / "analysis.json")
    c_rows = [read(c_root / x["repeat"] / (x["id"] + ".json")) for x in c_summary["cases"]]
    old_root = REPORTS / "research-extension-20261014"
    old_summary = read(old_root / "analysis.json")
    eq_rows = [
        read(old_root / x["repeat"] / (x["id"] + ".json"))
        for x in old_summary["cases"]
        if x["system"] == "EQ"
    ]
    old_semantics = read(REPORTS / "inquiry-trajectories-20261014/semantic_analysis.json")
    windows = [r for r in old_semantics["records"] if r["id"].startswith("EQ-")]
    windows += cs["records"]
    current = eq_rows + c_rows
    assert len(current) == 90 and len(windows) == 92
    assert len(opportunity["sessions"]) == 30 and opportunity["valid_Q"] == 29
    assert len(references["sessions"]) == 45 and references["valid_sessions"] == 42
    assert sum(not r["missing_stages"] for r in current) == 80
    assert sum("Q" in r["sealed_stages"] for r in current) == 83
    review = read(DEST / "evidence/summary.json")
    lines = [
        "# Supplementary Information",
        "",
        "## Evidence organization and units",
        "",
        "The main manuscript connects the organization of inquiry to the formation, testing, "
        "revision and application of scientific explanations. Abduction is an interpretive "
        "framework; the retained process counts are not rates of abductive success. "
        "Tables below use retained machine "
        "summaries. Current process evidence combines original equilibrium (45) and "
        "corrected-recovery crystallization (45), not old plus new crystallization. "
        "A separate thirty-session opportunity comparison uses a common assessment protocol. "
        "The 300 historical campaigns, 24 earlier selected notebook sessions, current process "
        "sessions and opportunity sessions are not pooled into one performance estimate. "
        "Reference batches, recipe retests, windows and repeated observations do not add "
        "researcher sessions. All failures remain in planned denominators.",
        "",
        "A portable review archive accompanies these tables. It contains the full public "
        "initial contexts, exact query/session/world response tables, the continuous "
        "equilibrium study, every adjacent notebook pair, quotation/action anchors and all "
        "ninety current public process histories. The package supports source inspection; "
        "it is not an independent recoding or a persistent public deposit.",
        "",
        table(
            ["Evidence layer", "Planned sessions", "Complete chains", "Valid forecasts"],
            [
                ["Current equilibrium", 45, 39, 41],
                ["Corrected crystallization", 45, 41, 42],
                ["Current process total", 90, 80, 83],
                ["Opportunity: Research", 15, 14, 14],
                ["Opportunity: NoResearch", 15, 15, 15],
            ],
        ),
        "",
        "O/A/M denote Opaque/Aligned/MisIndexed. A session label is world/information/repeat. "
        "Dashes indicate missing values, never zero error. All point errors are descriptive. "
        "Worlds are fixed and repeated; model sampling seeds are unavailable.",
        "",
        "## All current process sessions",
        "",
        "### Equilibrium",
        "",
        table(
            ["Session", "Batches /12", "Missing stages", "All MAE", "Dilute MAE", "Other MAE"],
            [
                [
                    identity(r),
                    r["completed_batches"],
                    ", ".join(r["missing_stages"]) or "-",
                    fmt(r["measurements"].get("all_twelve_macro_mae")),
                    fmt(r["measurements"].get("lowest_three_macro_mae")),
                    fmt(r["measurements"].get("remaining_nine_macro_mae")),
                ]
                for r in sorted(eq_rows, key=identity)
            ],
        ),
        "",
        "### Crystallization with consistent recovery definition",
        "",
        "Recovery means seed-excluded solid target divided by tracked initial reagent charge, "
        "clipped to [0,1]. It is not recovery relative to product before separation. "
        "Old predictions made under a different description are not substituted here. "
        "Size is the normalized public index, not micrometres.",
        "",
        table(
            ["Session", "Batches /12", "Missing stages", "Recovery MAE", "Purity MAE", "Fines MAE"],
            [
                [
                    identity(r),
                    r["completed_batches"],
                    ", ".join(r["missing_stages"]) or "-",
                    *[
                        fmt(r["measurements"].get(k + "_mae"))
                        for k in ("crystal_yield", "crystal_purity", "crystal_fines_fraction")
                    ],
                ]
                for r in sorted(c_rows, key=identity)
            ],
        ),
        "",
        "### All incomplete current process chains",
        "",
        table(
            ["System", "Session", "Missing stages", "Retained failure"],
            [
                [
                    r["system"],
                    identity(r),
                    ", ".join(r["missing_stages"]),
                    failure_label(r),
                ]
                for r in current
                if r["missing_stages"]
            ],
        ),
        "",
        "## Research paths",
        "",
        "All 150 path records and fifty within-world contrasts are retained separately from "
        "the forecast cohorts. Counts use committed operations, including resuspension. "
        "Group means are descriptive and do not identify exploration as a cause.",
        "",
        table(
            ["System", "Goal", "Budget", "Arm", "Sessions", "Solvents", "Measurements"],
            [
                [
                    g["system"],
                    g["goal"],
                    g["budget"],
                    g["arm"],
                    g["n"],
                    fmt(g["means"]["distinct_solvents"]),
                    fmt(g["means"]["intermediate_measurements"]),
                ]
                for g in paths["groups"]
            ],
        ),
        "",
        "### Initial choices in corrected crystallization",
        "",
        table(
            ["Information", "Planned sessions", "First solvent counts", "First catalyst counts"],
            [
                [
                    g["arm"],
                    g["n"],
                    *[
                        "; ".join(
                            ("None" if k == "None" else prefix + k) + f": {v}"
                            for k, v in sorted(g["first_choices"][field].items())
                        )
                        for field, prefix in (("first_solvent", "S"), ("first_catalyst", "C"))
                    ],
                ]
                for g in paths["groups"]
                if g["system"] == "C"
            ],
        ),
        "",
        "## Current process windows",
        "",
        "All 34 equilibrium and 58 corrected crystallization windows are included below. "
        "They occur in 30 and 35 sessions, respectively; fifteen and ten other sessions have "
        "no complete observable window. This is a recording denominator, not learning prevalence. "
        "Public statements, new observations and committed actions are checked separately. "
        "Matched plans do not prove causal effects of notebook text. Review is single-analyst; "
        "there is no independent second-rater estimate.",
        "",
        "### Eligibility before semantic plan matching",
        "",
        "All 268 notebook versions yield 178 adjacent pairs, each with at least one new "
        "committed final assay between notes. A pair enters the action-linked analysis "
        "only when a committed research operation follows the later note; measurement "
        "and termination alone do not count. This timing rule is evaluated before "
        "matching the meaning of a selected plan to an action. It does not require that "
        "plan to succeed, but it does condition the sample on continued committed research.",
        "",
        table(
            ["System", "Adjacent pairs", "Included", "No later research action"],
            [
                [system, v["adjacent_pairs"], v["included"], v["no_continuation"]]
                for system, v in review["by_system"].items()
            ]
            + [["Total", 178, 92, 86]],
        ),
        "",
        "All 92 eligible windows are coded: 83 selected plans match, seven partly match "
        "and two have no explicit next plan. A label concerns one selected immediate "
        "plan, not every proposal in that note. Full records retain rejected, abandoned "
        "and changed proposals, including those in otherwise matched windows. Terminal "
        "revisions in the 86 excluded pairs remain inspectable and are not designated "
        "as failures to learn. All 182 quotations and their temporal anchors are checked "
        "against the recorded versions.",
        "",
        "### All eligible windows",
        "",
        table(
            ["System", "Session", "Versions", "New batches", "Action link"],
            [
                [
                    r["id"].split("-")[0],
                    r["id"].split("-")[1][1:]
                    + "/"
                    + r["id"].split("-")[2][0]
                    + "/"
                    + r["repeat"][-1],
                    str(r["from_revision"]) + " to " + str(r["to_revision"]),
                    ", ".join(map(str, r["new_evidence_batches"])),
                    r["action_link"],
                ]
                for r in windows
            ],
        ),
        "",
        "### Quotations from the current coded windows",
        "",
        "The following are checked public quotations, not analyst reconstructions of private "
        "reasoning. Each numbered pair follows the order of the window inventory above. "
        "The update and next plan must be interpreted with the executed-action anchors, "
        "including rejected actions, in the retained coding records.",
        "",
    ]
    for number, r in enumerate(windows, 1):
        plan = (
            f"Next plan: “{r['next_plan_quote']}”"
            if r["next_plan_quote"] is not None
            else "No explicit next-plan quotation is available."
        )
        lines += [
            f"**Window {number}.** Update: “{r['update_quote']}” {plan}",
            "",
        ]
    lines += [
        "### Focal cases in the current narrative",
        "",
        table(
            ["Case", "Observable sequence", "Scope"],
            [
                [
                    "Corrected C, 05/A/1",
                    "Lower charge proposed, then executed",
                    "Local improvement; catalyst ratio also changes",
                ],
                [
                    "Corrected C, 05/A/2",
                    "0.065 L interpolation fails; expectation retracted",
                    "Revision without operational improvement",
                ],
                [
                    "Seed case B: corrected C, 02/A/2",
                    "Only 0.05 g seed commits; high-dose test withdrawn",
                    "Correctly recognizes unexecuted intervention",
                ],
                [
                    "Seed case C: corrected C, 03/A/3",
                    "Rejected seed additions described as a 1 g test",
                    "Negative evidence lacks the claimed intervention",
                ],
                [
                    "Corrected C, 04/A/2",
                    "430 K test follows claimed 440 K boundary",
                    "Earlier cold-target requests were rejected",
                ],
                [
                    "Corrected C, 01/M/3",
                    "Noise acknowledged; 310 K recipe repeated",
                    "Uncertainty awareness and recommendation failure coexist",
                ],
                [
                    "Equilibrium study A: opportunity world 1, Research repeat 1",
                    "Initial trend revised; component tests; dilute forecast",
                    "Bounded local relation weighted in unresolved extrapolation",
                ],
                [
                    "Opportunity, world 2, Research repeats 1 and 2",
                    "Plateau research followed by different dilute forecasts",
                    "Accurate extrapolation need not directly sample the target region",
                ],
            ],
        ),
        "",
        "The exact opportunity quote is: “The point estimate still favors the experimentally "
        "supported fixed acidic background”. The world-1 Research repeat-1 dilute estimate "
        "is 0.085 [0.035, 0.350], versus reference mean 0.716032; the corresponding NoResearch "
        "estimate is 0.569 [0.040, 0.980]. The researcher acknowledges the untested boundary. "
        "This is the new opportunity-comparison case, not the historical case with "
        "prediction 0.092 and reference 0.51730. The archive preserves both matched "
        "study-A sessions with full notes, operations and assessments. Neither the "
        "single trajectory nor its matched outcome establishes a self-confirmation cycle.",
        "",
        "## Source-only forecast references",
        "",
        "Each reference fits only the session's source final assays. Same-solvent matching "
        "uses exact sets of committed solvent IDs and falls back to the overall mean. "
        "It does not match quantities or thermal history. Five-world-equal errors and "
        "session wins are distinct summaries.",
        "",
    ]
    for group in references["groups"]:
        lines += [
            f"### {group['arm']}: {group['valid_sessions']}/"
            f"{45 if group['arm'] == 'all' else 15} valid sessions",
            "",
            table(
                ["Response", "Agent", "Source mean", "Same solvent", "Wins vs mean"],
                [
                    [
                        label,
                        *[
                            fmt(group["equal_world_mae"][m][k])
                            for m in ("agent", "source_mean", "same_solvent_mean")
                        ],
                        str(group["agent_strict_wins"]["source_mean"][k])
                        + "/"
                        + str(group["valid_sessions"]),
                    ]
                    for k, label in METRICS.items()
                ],
            ),
            "",
            f"Fallback queries: {group['fallback_queries']}/{group['query_count']}.",
            "",
        ]
    lines += [
        "### Session-level source-reference comparisons",
        "",
        table(
            [
                "Session",
                "Recovery: agent / mean",
                "Purity: agent / mean",
                "Size: agent / mean",
                "Fines: agent / mean",
            ],
            [
                [
                    identity(r),
                    *[
                        fmt(r.get("mae", {}).get("agent", {}).get(k))
                        + " / "
                        + fmt(r.get("mae", {}).get("source_mean", {}).get(k))
                        for k in METRICS
                    ],
                ]
                for r in references["sessions"]
            ],
        ),
        "",
        "## Separate research-opportunity comparison",
        "",
        "Thirty sessions, 180/180 source batches, 117/120 assessment stages and 29 valid "
        "forecasts. The world-3 third Research session lost Q and later stages after a "
        "network stream failure. All source records and K1 are retained. No replacement "
        "was made. This is a total research-package effect, not a notebook ablation.",
        "",
        "### Initial scientific information",
        "",
        "All thirty sessions use Opaque information. The exact public inputs contain "
        "the task and goals, response definitions, material catalogue, legal operations "
        "and instruments, resource limits and initial public state. The instance archival "
        "prior is null: no additional fitted local law or world-specific dossier is supplied. "
        "This does not remove public chemical framing or the model's pretrained knowledge. "
        "The archive includes all thirty full initial contexts. Fifteen within-world/repeat "
        "comparisons verify equality after removing only the campaign identifier. Research "
        "then receives twelve source batches and the notebook opportunity; NoResearch "
        "receives no source observations. Assessment prompts, order and restrictions match.",
        "",
        "### Session-level macro errors",
        "",
        table(
            ["World", "Repeat", "Opportunity", "Batches", "All MAE", "Dilute MAE", "Other MAE"],
            [
                [
                    r["world"][1:],
                    r["repeat"][-1],
                    r["opportunity"],
                    r["source_batches"],
                    *[
                        fmt((r.get("scores") or {}).get("groups", {}).get(g, {}).get("macro_mae"))
                        for g in ("all", "dilute", "other")
                    ],
                ]
                for r in opportunity["sessions"]
            ],
        ),
        "",
    ]
    means = opportunity["comparison"]["equal_world_means"]
    lines += [
        table(
            ["Query group", "Research", "NoResearch", "Difference"],
            [
                [
                    g,
                    fmt(means["Research"][g]["macro_mae"]),
                    fmt(means["NoResearch"][g]["macro_mae"]),
                    fmt(means["Research"][g]["macro_mae"] - means["NoResearch"][g]["macro_mae"]),
                ]
                for g in ("all", "dilute", "other")
            ],
        ),
        "",
        *response_tables(means),
        "### Interval outcomes",
        "",
        "Nominal 80% intervals; equal-world means. Lower interval score is better. "
        "Coverage alone rewards broad intervals.",
        "",
        table(
            ["Group", "Response", "Arm", "Coverage", "Width", "Interval score"],
            [
                [
                    g,
                    {
                        "pH_normalized": "Normalized pH",
                        "acid_dissociation_fraction": "Dissociation",
                        "precipitation_signal": "Precipitation",
                    }[response],
                    arm,
                    fmt(v["coverage80"]),
                    fmt(v["width80"]),
                    fmt(v["interval_score80"]),
                ]
                for arm, groups in means.items()
                for g, outcomes in groups.items()
                for response, v in outcomes["metrics"].items()
            ],
        ),
        "",
        "### Missing-forecast sensitivity",
        "",
        opportunity["posthoc_missing_forecast_sensitivity"]["basis"],
        "",
        table(
            ["Group", "Difference lower", "Difference upper"],
            [
                [
                    g,
                    fmt(v["research_minus_no_research"]["lower"]),
                    fmt(v["research_minus_no_research"]["upper"]),
                ]
                for g, v in opportunity["posthoc_missing_forecast_sensitivity"]["groups"].items()
            ],
        ),
        "",
        "The failed initial execution attempt is retained separately: four launched "
        "sessions, two completed source histories totalling 24 batches and no K1. "
        "An assessment-transport defect was fixed before the entire block restarted. "
        "Final-block recorded usage is 13,428,656 input-plus-output tokens, with "
        "29/30 complete ledgers and one partial record; unavailable cost is not zero.",
        "",
        "## Retained matched-quench dispositions",
        "",
        "Ninety planned pairs, 75 complete, all 180 trajectories replayed. Eighteen donor "
        "recipes are historical and not corrected-block participants. Effects are present "
        "minus absent, conditional on both final assays. Failed arms are not repaired. "
        "No agent receives the control outcomes.",
        "",
    ]
    pairs = read(old_root / "quench_pairs.json")
    donors = sorted({p["recipe"] for p in pairs})
    lines += [
        table(
            ["Donor", "Source world", "Information", "Repeat"],
            [
                [i + 1, d.split("-")[-2][1:], d.split("-")[-1], d.split("-")[1]]
                for i, d in enumerate(donors)
            ],
        ),
        "",
    ]
    qrows = []
    for i, donor in enumerate(donors, 1):
        vals = []
        for p in sorted((p for p in pairs if p["recipe"] == donor), key=lambda x: x["world"]):
            vals.append(
                fmt(p["paired_effect"]["crystal_fines_fraction"])
                if p["paired_effect"]
                else ("Absent fails" if not p["absent"]["passed"] else "Present fails")
            )
        qrows.append([i, *vals])
    lines += [table(["Donor", "World 1", "World 2", "World 3", "World 4", "World 5"], qrows), ""]
    legacy, count = retained_tables()
    assert count == 34
    lines += legacy
    (DEST / "supplementary.md").write_text("\n".join(lines), encoding="utf-8")
    coverage = Counter(r["id"].split("-")[0] for r in windows)
    print(
        f"Complete: {len(current)} current sessions; {dict(coverage)} windows; "
        f"{opportunity['terminal']} opportunity sessions; {len(pairs)} quench pairs; "
        f"{count} unchanged historical tables. No new experiments or plots.",
        flush=True,
    )


if __name__ == "__main__":
    main()
