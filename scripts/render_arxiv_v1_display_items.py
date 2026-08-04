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
        ("registered task designs", q["registered_tasks"], "instrument surface"),
        ("typed operation types", q["registered_operations"], "instrument surface"),
        ("instrument types", q["registered_instruments"], "instrument surface"),
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
                row["task_id"].replace("-", " ").capitalize(),
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
            "The fresh-session study is not complete. Its prespecified 20-cell matrix "
            "remains absent from the",
            "paper data object, so no interim replication values are rendered here.",
        ]
    rows = []
    for row in replication["paired_trajectories"]:
        delta = row["nominal_minus_opaque"]
        rows.append(
            (
                row["world_seed"],
                int(str(row["trajectory_replicate_id"]).removeprefix("r")),
                row["opaque_state"].replace("_", "-"),
                row["nominal_state"].replace("_", "-"),
                None if delta is None else delta["best_final_score"],
                None if delta is None else delta["terminal_final_score"],
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
            "Δ raw terminal",
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
    return [
        f"Terminal coverage: {matrix['completed_cell_count']} completed cells, "
        f"{matrix['right_censored_cell_count']} right-censored cells, and "
        f"{matrix['completed_pair_count']} complete pairs "
        f"({branch['completed_pairs_by_world']['1']} in world 1; "
        f"{branch['completed_pairs_by_world']['3']} in world 3).",
        "The prespecified interpretation classified "
        f"{branch['mixed_world_by_core_metric_count']} of "
        f"{branch['world_by_core_metric_count']} world-by-core-lifecycle classifications as mixed.",
        "The frozen categorical lifecycle summary is supporting; the main continuous endpoint "
        "diagnostic compares best score with algebraically independent raw terminal score.",
        "Provider sampling was not seed-controlled; the summary does not identify a causal "
        "provider effect or a variance-dominance relation.",
    ]


def render(data: Mapping[str, Any]) -> str:
    sections: list[str] = [
        (
            "# ChemWorld: A Programmable Virtual Instrument for Measuring Experimental "
            "Process Profiles: "
            "numeric display items"
        ),
        "",
        "Status: complete for the evidence reported below.",
        "",
        "Every number in the tables below is rendered from the frozen analysis data.",
        "The tables and legends are formatted for direct manuscript typesetting.",
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
        "### Table 2 | Compiled-control capability profiles",
        "",
        *_g0_table(data),
        "",
        "Scores are means across ten simulator worlds. Dashes indicate endpoints that were not",
        "defined for that information arm; they are not zeroes. No composite score is formed.",
        "",
        "### Table 3 | Primitive-control development trajectories",
        "",
        *_g2_v04_table(data),
        "",
        "Each arm contains five simulator-world cells and six completed vessels per cell.",
        "Operations are mean submitted primitive attempts per cell. These development data select",
        "the worlds and endpoints for the fresh-session study and are excluded from its "
        "replication estimand.",
        "",
        "### Table 4 | Fresh primitive-control trajectories",
        "",
        *_g2_v05_table(data),
        "",
        "Deltas are nominal minus opaque within the same physical world and replicate block.",
        "The two deliberately selected worlds are not pooled into a population-level estimate.",
        *_g2_v05_terminal_note(data),
        "",
        "## Figure legends",
        "",
        "**Figure 1 | ChemWorld apparatus and controlled world forks.**",
        "**A,** An agent selects a typed action; the executable world returns only the public",
        "observation while recording the identity-bound transition. **B,** Hidden simulator-world",
        "and material identity, action authority, evidence access, resource accounting and replay",
        "are separate protocol controls. **C,** The frozen qualification changes one named private",
        "component while preserving nine public-contract components. **D,** Six parent-child pairs",
        "and 24 provider-free traces passed the registered programmability gates. These probes",
        "establish the tested executable-world interventions, not agent performance, arbitrary",
        "world recombination, rule adaptation or physical transfer.",
        "",
        "**Figure 2 | Known policies qualify the experimental-process profile.**",
        "**A,** Three frozen policies specify distinct evidence and terminal-decision structures.",
        "**B,** Campaign-equal terminal profiles recover assay-all, threshold-gated and",
        "immediate-discard signatures. **C,** Evidence acquisition, continued investment and",
        "resource use remain separate readouts; registered undefined quantities remain null.",
        "**D,** All 30 same-identity deterministic retests match their primary campaigns. The",
        "primary evidence comprises 30 campaigns and 180 closed lifecycles; the additional 30",
        "campaigns and 180 lifecycles are excluded reliability retests. This is a bounded positive",
        "control in the simulated apparatus, not an endpoint, agent or model ranking.",
        "",
        "**Figure 3 | Lifecycle completion does not specify terminal policy.**",
        "**A,** The 120 closed lifecycles partition into 84 final assays and 36 explicit discards:",
        "60 assays for the Codex-based complete system and 24 assays plus 36 discards for the",
        "DeepSeek-based complete system. **B,** Terminal commitments by matched simulator world",
        "and information arm; system identities include model, scaffold, transport and run",
        "configuration. **C,** All 36 registered discard identities remain in the latent-terminal",
        "audit, with 6 resolved and 30 unresolved after the frozen entry gate failed.",
        "**D,** Registered censoring and finite-population bounds replace latent-dependent point",
        "estimates; the no-discard-opportunity cell remains structurally null. Shadow assays were",
        "evaluator-only counterfactual evaluations, were not agent choices or observations, and",
        "did not add original agent experiments.",
        "",
        "**Figure 4 | Compiled controls separate outcome, prediction, calibration and claims.**",
        "**A,** All paired nominal-minus-opaque endpoint differences across ten designed worlds",
        "per task; the ranges summarize finite-set resampling sensitivity rather than population",
        "confidence intervals. **B,** Held-out",
        "prediction and calibration are displayed as separate raw metrics. **C,** Opaque-arm",
        "epistemic readouts retain registered missingness without imputation. "
        "**D,** Protocol-frozen",
        "manipulation, correction, performance-restoration and joint gates remain separate.",
        "Classical optimizers are calibration controls, not the target competition; the figure",
        "supports no scalar ranking or general population information effect.",
        "",
        "**Figure 5 | Primitive-control agents expose complete experimental lifecycles.**",
        "**A,** One descriptive seven-operation lifecycle makes a UV-visible observation available",
        "before the next system decision and explicit final assay. **B,** The campaign resource",
        "receipt reports units and denominators outside the prompt. **C,** Identity, resource",
        "events and exact executable replay align the public process record with evaluator state.",
        "**D,** Failed, rejected and terminal actions retain their distinct transaction and",
        "closure",
        "semantics. Operations are repeated events within campaigns, not independent samples;",
        "replay concerns simulator state and records, not a physical batch or stochastic provider",
        "decision.",
        "",
        "**Figure 6 | Fresh trajectories reveal process structure omitted by endpoints.**",
        "All ten pre-specified trajectory pairs are shown. **A,** The frozen selected-world design",
        "contains eight complete matched pairs and two explicitly right-censored pairs. **B,**",
        "Best-of-campaign and raw terminal contrasts",
        "disagree in sign for 2/8 complete pairs; this is the primary endpoint diagnostic.",
        "**C,** Continuous contrasts separately display discovery, retention, drawdown, recovery",
        "and relative terminal retention. **D,** The 6/8 mixed classification is supporting and",
        "threshold-sensitive, ranging from two to eight across the frozen sensitivity grid. These",
        "deliberately selected worlds describe within-world process variation and are not pooled",
        "into a population-level model or information-effect claim.",
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
