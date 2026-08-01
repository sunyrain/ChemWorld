"""Render manuscript tables and figure legends from the arXiv derived-data object."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DERIVED_SCHEMA = "chemworld-arxiv-v1-derived-data-0.1"


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != DERIVED_SCHEMA:
        raise ValueError("unsupported arXiv derived-data schema")
    declared = data.pop("derived_data_sha256")
    actual = _canonical_sha256(data)
    data["derived_data_sha256"] = declared
    if actual != declared:
        raise ValueError("derived-data content hash is invalid")
    return data


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "not measured"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(_fmt(value) for value in row) + " |" for row in rows)
    return lines


def _environment_table(data: Mapping[str, Any]) -> list[str]:
    q = data["environment_qualification"]
    scope = data["paper_scope"]
    rows = [
        ("registered task designs", q["registered_tasks"], "release surface"),
        ("typed operation types", q["registered_operations"], "release surface"),
        ("instrument types", q["registered_instruments"], "release surface"),
        (
            "deterministic complete-experiment cases",
            q["deterministic_complete_experiment_cases"],
            "design qualification",
        ),
        (
            "declared endpoints bound to evaluators",
            q["bound_success_endpoints"],
            "design qualification",
        ),
        (
            "tasks with formal compiled-agent results",
            scope["compiled_experiment_tasks"],
            "paper evidence",
        ),
        ("tasks with autonomous-agent results", scope["autonomous_task_count"], "paper evidence"),
    ]
    return _table(("Quantity", "Count", "Evidence level"), rows)


def _g0_table(data: Mapping[str, Any]) -> list[str]:
    rows = []
    for row in data["g0"]["task_arm_rows"]:
        if row["arm"] == "derived_contrasts":
            continue
        rows.append(
            (
                row["task_id"],
                row["arm"],
                row["world_count"],
                row["primary_score_mean"],
                row["heldout_directional_accuracy"],
                row["heldout_brier_score"],
                row["structural_edge_f1"],
                row["mechanism_tag_f1"],
                row["unsupported_claim_rate"],
            )
        )
    return _table(
        (
            "Task",
            "Information arm",
            "Worlds",
            "Final score",
            "Held-out accuracy",
            "Brier",
            "Structure F1",
            "Mechanism F1",
            "Unsupported claims",
        ),
        rows,
    )


def _g2_v04_table(data: Mapping[str, Any]) -> list[str]:
    aggregates = data["g2_v0_4"]["arm_descriptive_aggregates"]
    rows = []
    for arm in ("opaque", "nominal"):
        row = aggregates[arm]
        learning = row["trajectory_learning"]
        rows.append(
            (
                arm,
                row["cell_count"],
                row["mean_completion_rate"],
                row["mean_operation_count"],
                row["mean_best_final_score"],
                row["mean_batch_final_assay_running_best_auc"],
                row["mean_operation_attempt_running_best_auc"],
                row["mean_budget_normalized_operation_attempt_running_best_auc"],
                learning["mean_global_best_discovery_fraction"],
                learning["mean_online_retention_rate"],
                learning["mean_maximum_absolute_drawdown"],
                learning["mean_terminal_to_global_best_ratio"],
                learning["pooled_recovery_rate"],
            )
        )
    return _table(
        (
            "Arm",
            "Cells",
            "Completion",
            "Operations",
            "Best score",
            "Batch AUC",
            "Realized-op AUC",
            "Fixed-budget AUC",
            "Discovery fraction",
            "Retention",
            "Max drawdown",
            "Terminal / best",
            "Recovery",
        ),
        rows,
    )


def _g2_v05_table(data: Mapping[str, Any]) -> list[str]:
    replication = data["g2_v0_5"]
    if replication is None:
        return [
            "G2 v0.5 is not terminal. The preregistered 20-cell matrix remains absent from the",
            "paper data object, so no interim replication values are rendered here.",
        ]
    rows = []
    for row in replication["paired_trajectories"]:
        delta = row["nominal_minus_opaque"]
        rows.append(
            (
                row["world_seed"],
                row["trajectory_replicate_id"],
                row["opaque_state"],
                row["nominal_state"],
                None if delta is None else delta["best_final_score"],
                None if delta is None else delta["final_score_mean"],
                None if delta is None else delta["global_best_discovery_fraction"],
                None if delta is None else delta["online_incumbent_retention_rate"],
                None if delta is None else delta["maximum_absolute_incumbent_drawdown"],
                None if delta is None else delta["terminal_to_global_best_ratio"],
            )
        )
    return _table(
        (
            "World",
            "Replicate",
            "Opaque state",
            "Nominal state",
            "Δ best score",
            "Δ mean score",
            "Δ discovery",
            "Δ retention",
            "Δ drawdown",
            "Δ terminal / best",
        ),
        rows,
    )


def _g2_v05_terminal_note(data: Mapping[str, Any]) -> list[str]:
    replication = data["g2_v0_5"]
    if replication is None:
        return []
    matrix = replication["matrix"]
    interpretation = replication["interpretation"]
    branch = interpretation["selected_branch"]
    policy = interpretation["mapping_policy"]
    return [
        f"Terminal coverage: {matrix['completed_cell_count']} completed cells, "
        f"{matrix['right_censored_cell_count']} right-censored cells, and "
        f"{matrix['completed_pair_count']} complete pairs "
        f"({branch['completed_pairs_by_world']['1']} in world 1; "
        f"{branch['completed_pairs_by_world']['3']} in world 3).",
        f"The frozen interpretation mapping selected `{branch['branch_id']}`: "
        f"{branch['mixed_world_by_core_metric_count']} of "
        f"{branch['world_by_core_metric_count']} world-by-core-lifecycle classifications were "
        f"mixed. Policy SHA-256: `{policy['sha256']}`.",
        f"Frozen policy language: {branch['manuscript_language']}",
        "Provider sampling was not seed-controlled; this language is descriptive and does not "
        "identify a causal provider effect.",
    ]


def render(data: Mapping[str, Any]) -> str:
    figure_5_state = (
        "This legend becomes active only after the terminal G2 v0.5 audit is incorporated."
        if data["g2_v0_5"] is None
        else (
            "All ten pre-specified trajectory pairs are shown; an x marks a right-censored "
            "pair. Six of eight world-by-core-lifecycle classifications were mixed, selecting "
            "the frozen `frequent_within_world_reversal` interpretation branch."
        )
    )
    sections: list[str] = [
        "# Experimental Intelligence in Executable Chemical Worlds: display items",
        "",
        f"Status: `{data['status']}`.",
        f"Derived-data SHA-256: `{data['derived_data_sha256']}`.",
        "",
        "Every number in the tables below is rendered from the self-hashed arXiv derived-data",
        "object. This file is intended for direct inclusion during manuscript typesetting.",
        "",
        "## Main tables",
        "",
        "### Table 1 | Qualified environment surface and formal evidence scope",
        "",
        *_environment_table(data),
        "",
        "Counts for the environment surface are design qualifications, not claims of agent",
        "competence. Formal paper evidence covers fewer tasks than the registered surface.",
        "",
        "### Table 2 | Compiled-experiment capability profiles",
        "",
        *_g0_table(data),
        "",
        "Scores are means across ten physical worlds. Dashes indicate endpoints that were not",
        "defined for that information arm; they are not zeroes. No composite score is formed.",
        "",
        "### Table 3 | Autonomous development trajectories (G2 v0.4)",
        "",
        *_g2_v04_table(data),
        "",
        "Each arm contains five physical-world cells and six completed vessels per cell.",
        "Operations are mean submitted primitive attempts per cell. These development data select",
        "the worlds and endpoints for G2 v0.5 and are excluded from its replication estimand.",
        "",
        "### Table 4 | Fresh-trajectory replication (G2 v0.5)",
        "",
        *_g2_v05_table(data),
        "",
        "Deltas are nominal minus opaque within the same physical world and replicate block.",
        "The two deliberately selected worlds are not pooled into a population-level estimate.",
        *_g2_v05_terminal_note(data),
        "",
        "## Figure legends",
        "",
        "**Figure 1 | ChemWorld is a controlled apparatus for experimental intelligence.**",
        "**A,** Closed-loop interaction between a hidden chemical world, one typed agent action,",
        "the resulting state transition and a public measurement. **B,** Physical world, prior",
        "information, agent authority, evidence access and resources are independently controlled",
        "experimental axes. **C,** The auditable transition spine binds typed state, atomic",
        "transaction, resource receipt, immutable trace and exact replay; invalid actions and",
        "failures remain evidence. **D,** Qualified release surface. Counts establish declared",
        "reachability and evaluator binding, not agent performance across all registered tasks.",
        "",
        "**Figure 2 | One complete agent-directed experiment and its campaign ledger.**",
        "**A,** The first vessel from the opaque world-0 development campaign: the agent selected",
        "reagent and solvent addition, potential setting, electrolysis, a UV-visible measurement,",
        "termination and final assay in seven primitive operations. This example illustrates the",
        "interface and is excluded from prior-effect inference. **B,** Independently debited",
        "campaign resources reconstructed from the immutable trajectory; physical inventory and",
        "instrument use are not collapsed into a scalar token budget.",
        "",
        "**Figure 3 | Endpoint summaries conceal distinct experimental trajectories.**",
        "Final-assay sequences for opaque and anonymous nominal-information agents in development",
        "worlds 0, 2 and 4. Open circles identify the first campaign maximum. The examples expose",
        "early discovery followed by abandonment, gradual improvement, drawdown and terminal",
        "recovery that a best-score endpoint alone cannot distinguish.",
        "",
        "**Figure 4 | Prior interventions reshape behavior without guaranteeing recovery.**",
        "**A,** Paired nominal-minus-opaque effects on compiled-experiment final score with",
        "familywise 97.5% world-bootstrap intervals. **B,** Early and late shares of",
        "actions aligned with deliberately misindexed material information. **C,** Separate",
        "preregistered checks",
        "for manipulation, differential action correction, performance restoration and their joint",
        "recovery rule. **D,** Nominal-minus-opaque autonomous development effects across five",
        "physical worlds; points are worlds and horizontal bars are descriptive means. Positive",
        "drawdown differences indicate larger drawdown under nominal information.",
        "",
        "**Figure 5 | Fresh trajectories test within-world repeatability.**",
        "Nominal-minus-opaque paired differences for best score and four core lifecycle",
        "endpoints---global-best discovery fraction, online incumbent retention, maximum absolute",
        "drawdown and terminal-to-best ratio---across five fresh replicates in each",
        f"of selected physical worlds 1 and 3. {figure_5_state}",
        "Selection used the prior development matrix; those trajectories are excluded. Effects are",
        "reported within world, with no pooled population-level test.",
        "",
        "**Figure 6 | Experimental intelligence is a profile, not a scalar.**",
        "**A,** Compiled-experiment endpoint score, held-out directional accuracy, Brier score and",
        "unsupported-claim rate for the opaque participant in two chemical tasks.",
        "**B,** Autonomous",
        "completion, retention, recovery and terminal-to-best summaries by information arm. Metric",
        "directions differ and no composite score is computed; the panel demonstrates the need to",
        "retain a capability profile rather than rank systems on these bars.",
        "",
    ]
    return "\n".join(sections)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "derived_data",
        nargs="?",
        type=Path,
        default=Path("benchmark/releases/chemworld-serious-v1/arxiv-v1-derived-data.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("paper/experimental_intelligence_v1_display_items.md"),
    )
    return parser


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else REPOSITORY_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(REPOSITORY_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data = _load(_resolve(args.derived_data))
    output = _resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "derived_data_sha256": data["derived_data_sha256"],
                "g2_v0_5_included": data["g2_v0_5"] is not None,
                "output": _display_path(output),
                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            },
            sort_keys=True,
        )
    )
    return 0 if data["g2_v0_5"] is not None else 2


if __name__ == "__main__":
    raise SystemExit(main())
