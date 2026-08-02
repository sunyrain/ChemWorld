"""Build the single derived-data source for the first ChemWorld arXiv paper.

The builder deliberately accepts only audited aggregate artifacts.  It never
reads a live trajectory directory, so pending G2 cells cannot leak into paper
tables or figures.  G2 v0.5 remains absent until its terminal replication
audit is supplied.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from chemworld.eval.autonomous_material_replication_audit import (
    AutonomousMaterialReplicationAuditError,
    validate_interpretation_binding,
)

ARXIV_V1_DERIVED_SCHEMA = "chemworld-arxiv-v1-derived-data-0.1"
_G2_V04_SCHEMA = "chemworld-autonomous-material-campaign-audit-0.3"
_G2_V05_SCHEMA = "chemworld-autonomous-material-trajectory-replication-audit-0.1"
_ARMS = ("opaque", "nominal", "misindexed")


class ArxivV1DerivedDataError(ValueError):
    """Raised when an input artifact is missing or inconsistent."""


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    """Return a deterministic SHA-256 over canonical JSON."""

    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path, *, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise ArxivV1DerivedDataError(f"{label} does not exist: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ArxivV1DerivedDataError(f"{label} must contain a JSON object")
    return value


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ArxivV1DerivedDataError(message)


def _source(path: Path, *, canonical_json: bool = False) -> dict[str, Any]:
    portable = path.as_posix()
    lower_parts = [part.lower() for part in path.parts]
    for root_name in ("workstreams", "configs", "benchmark", "paper", "runs", "src"):
        if root_name in lower_parts:
            index = lower_parts.index(root_name)
            portable = Path(*path.parts[index:]).as_posix()
            break
    result = {
        "path": portable,
        "file_sha256": file_sha256(path),
    }
    if canonical_json:
        result["canonical_json_sha256"] = canonical_sha256(_load_json(path, label=str(path)))
    return result


def _task_rows(
    g0_v10: Mapping[str, Any],
    g0_v12: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    task_rows: list[dict[str, Any]] = []
    world_rows: list[dict[str, Any]] = []
    baseline_rows: list[dict[str, Any]] = []
    v10_tasks = g0_v10["tasks"]
    v12_tasks = g0_v12["tasks"]
    for task_key in ("electrochemical", "crystallization"):
        original = v10_tasks[task_key]
        triarm = v12_tasks[task_key]
        task_id = str(triarm["task_id"])
        baselines = list(original["baselines"])
        for baseline in baselines:
            baseline_rows.append(
                {
                    "task_id": task_id,
                    "algorithm_id": baseline["algorithm_id"],
                    "role": baseline["role"],
                    "information_condition": baseline["information_condition"],
                    "mean_validated_final_score": baseline["validated_final_score"]["mean"],
                }
            )
        matched = [row for row in baselines if row["role"] == "information_matched"]
        _require(bool(matched), f"{task_id}: no information-matched baseline")
        best_matched = max(
            matched,
            key=lambda row: row["validated_final_score"]["mean"],
        )
        paired = next(
            row
            for row in original["paired_comparisons"]
            if row["algorithm_id"] == best_matched["algorithm_id"]
        )
        privileged = [row for row in baselines if row["role"] == "privileged_calibration"]
        best_privileged = (
            max(
                privileged,
                key=lambda row: row["validated_final_score"]["mean"],
            )
            if privileged
            else None
        )
        for arm in _ARMS:
            primary = triarm["primary_score_by_arm"][arm]
            predictive = triarm["predictive_secondary_diagnostic_mean_by_arm"][arm]
            declared = (
                original["participant"]["declared_world_understanding_secondary_diagnostic_mean"]
                if arm == "opaque"
                else None
            )
            task_rows.append(
                {
                    "task_id": task_id,
                    "arm": arm,
                    "world_count": primary["count"],
                    "primary_score_mean": primary["mean"],
                    "primary_score_sd": primary["sample_standard_deviation"],
                    "heldout_directional_accuracy": predictive["directional_accuracy"],
                    "heldout_brier_score": predictive["confidence_brier_score"],
                    "declared_directional_accuracy": (
                        None if declared is None else declared["directional_accuracy"]
                    ),
                    "structural_edge_f1": (
                        None if declared is None else declared["structural_edge_f1"]
                    ),
                    "mechanism_tag_f1": (
                        None if declared is None else declared["mechanism_tag_f1"]
                    ),
                    "unsupported_claim_rate": (
                        None if declared is None else declared["unsupported_claim_rate"]
                    ),
                }
            )
        for item in triarm["worlds"]:
            for arm in _ARMS:
                action = item[arm]["action"]
                world_rows.append(
                    {
                        "task_id": task_id,
                        "world_seed": item["world_seed"],
                        "arm": arm,
                        "primary_score": item[arm]["primary_score"],
                        "first_action_is_misleading": action["first_action_is_misleading"],
                        "early_misleading_share": action["early_misleading_share"],
                        "late_misleading_share": action["late_misleading_share"],
                        "final_action_is_misleading": action["final_action_is_misleading"],
                    }
                )
        contrasts = triarm["paired_contrasts"]
        recovery = triarm["recovery"]
        task_rows.append(
            {
                "task_id": task_id,
                "arm": "derived_contrasts",
                "nominal_minus_opaque_mean": contrasts["nominal_minus_opaque"]["mean"],
                "nominal_minus_opaque_familywise_97_5_interval": contrasts["nominal_minus_opaque"][
                    "world_bootstrap_97_5_interval"
                ],
                "misindexed_minus_opaque_mean": contrasts["misindexed_minus_opaque"]["mean"],
                "misindexed_minus_nominal_mean": contrasts["misindexed_minus_nominal"]["mean"],
                "first_misleading_rate_misindexed": recovery["first_action_misleading_rate_by_arm"][
                    "misindexed"
                ],
                "early_misleading_share_misindexed": recovery["early_misleading_share_by_arm"][
                    "misindexed"
                ]["mean"],
                "late_misleading_share_misindexed": recovery["late_misleading_share_by_arm"][
                    "misindexed"
                ]["mean"],
                "manipulation_check_passed": recovery["manipulation_check"]["passed"],
                "differential_action_correction_passed": recovery["differential_action_correction"][
                    "passed"
                ],
                "performance_recovery_to_opaque_passed": recovery["performance_recovery_to_opaque"][
                    "passed"
                ],
                "overall_recovery_claim_passed": recovery["overall_recovery_claim"]["passed"],
                "best_information_matched_baseline": best_matched["algorithm_id"],
                "best_information_matched_baseline_mean": best_matched["validated_final_score"][
                    "mean"
                ],
                "participant_minus_best_matched_mean": paired["participant_minus_baseline"]["mean"],
                "participant_minus_best_matched_95_interval": paired["participant_minus_baseline"][
                    "world_bootstrap_95_interval"
                ],
                "best_privileged_calibration": (
                    None if best_privileged is None else best_privileged["algorithm_id"]
                ),
                "best_privileged_calibration_mean": (
                    None
                    if best_privileged is None
                    else best_privileged["validated_final_score"]["mean"]
                ),
            }
        )
    return task_rows, world_rows, baseline_rows


def _g2_v04_rows(
    audit: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    _require(audit.get("schema_version") == _G2_V04_SCHEMA, "wrong G2 v0.4 schema")
    _require(
        audit.get("status") == "completed_audited_descriptive_matrix", "G2 v0.4 is not audited"
    )
    _require(len(audit.get("cells", [])) == 10, "G2 v0.4 must contain ten cells")
    cell_rows: list[dict[str, Any]] = []
    for cell in audit["cells"]:
        learning = cell["trajectory_learning"]["discovery_retention_recovery"]
        scores = cell["scores"]
        cell_rows.append(
            {
                "cell_id": cell["cell_id"],
                "world_seed": cell["world_seed"],
                "arm": cell["arm"],
                "completed_vessels": cell["completion"]["completed_vessels"],
                "operation_count": cell["operations"]["count"],
                "invalid_operation_count": cell["operations"]["invalid_count"],
                "nonfinal_measurement_count": cell["measurements"]["committed_count"],
                "final_score_sequence": scores["final_score_sequence"],
                "final_assay_operation_indices": [
                    row["operation_attempt_index"] for row in scores["final_assay_outcomes"]
                ],
                "best_final_score": scores["best_final_score"],
                "final_score_mean": scores["final_score_mean"],
                "batch_auc": scores["batch_final_assay_running_best_auc"],
                "realized_attempt_auc": scores["operation_attempt_running_best_auc"],
                "fixed_budget_attempt_auc": scores[
                    "budget_normalized_operation_attempt_running_best_auc"
                ],
                "global_best_discovery_fraction": learning["global_best_discovery_fraction"],
                "online_incumbent_retention_rate": learning["online_retention_rate"],
                "maximum_absolute_incumbent_drawdown": learning[
                    "maximum_absolute_drawdown_from_prior_incumbent"
                ],
                "terminal_to_global_best_ratio": learning["terminal_to_global_best_ratio"],
                "loss_episode_count": learning["loss_episode_count"],
                "recovered_loss_episode_count": learning["recovered_loss_episode_count"],
                "unresolved_loss_episode_count": learning["unresolved_loss_episode_count"],
            }
        )
    pair_rows = [
        {
            "world_seed": row["world_seed"],
            **{
                key: value
                for key, value in row["nominal_minus_opaque"].items()
                if key
                in {
                    "best_final_score",
                    "final_score_mean",
                    "batch_final_assay_running_best_auc",
                    "operation_attempt_running_best_auc",
                    "budget_normalized_operation_attempt_running_best_auc",
                    "operation_count",
                    "global_best_discovery_fraction",
                    "online_incumbent_retention_rate",
                    "maximum_absolute_incumbent_drawdown",
                    "terminal_to_global_best_ratio",
                }
            },
        }
        for row in audit["paired_worlds"]
    ]
    representative = next(
        cell for cell in audit["cells"] if cell["world_seed"] == 0 and cell["arm"] == "opaque"
    )
    first_batch = representative["batches"][0]
    demonstration = {
        "label": "development demonstration; excluded from prior-effect inference",
        "cell_id": representative["cell_id"],
        "world_seed": 0,
        "arm": "opaque",
        "operation_signature": first_batch["operation_signature"],
        "operation_count": first_batch["operation_count"],
        "diagnostic_policy": first_batch["diagnostic_policy"],
        "setpoint_policy": first_batch["setpoint_policy"],
        "final_score": first_batch["final_score"],
        "campaign_resource_endpoints": representative["resource_ledger"],
    }
    return cell_rows, pair_rows, demonstration


def _g2_v05_rows(audit: Mapping[str, Any]) -> dict[str, Any]:
    _require(audit.get("schema_version") == _G2_V05_SCHEMA, "wrong G2 v0.5 schema")
    unhashed = dict(audit)
    declared_audit_hash = unhashed.pop("audit_sha256", None)
    _require(
        declared_audit_hash == canonical_sha256(unhashed),
        "G2 v0.5 audit hash is invalid",
    )
    try:
        validate_interpretation_binding(audit)
    except AutonomousMaterialReplicationAuditError as error:
        raise ArxivV1DerivedDataError(str(error)) from error
    matrix = audit["matrix"]
    _require(
        matrix["completed_cell_count"] + matrix["right_censored_cell_count"] == 20,
        "G2 v0.5 audit is not terminal for all twenty cells",
    )
    _require(
        matrix["all_attempt_selection_policies_verified"],
        "G2 v0.5 attempt selection policy failed",
    )
    _require(matrix["all_physical_pairs_verified"], "G2 v0.5 physical pairing failed")
    _require(
        matrix["all_terminal_cells_resource_replay_verified"],
        "G2 v0.5 terminal resource or replay verification failed",
    )
    pairs = []
    for row in audit["paired_trajectories"]:
        contrast = row["nominal_minus_opaque"]
        if contrast is not None:
            contrast = dict(contrast)
            score_sequence = contrast.get("final_score_sequence")
            _require(
                isinstance(score_sequence, list) and bool(score_sequence),
                "a complete G2 v0.5 pair is missing final-score contrasts",
            )
            # The last element is the nominal-minus-opaque raw terminal score.
            # Keep it explicit so downstream analyses do not confuse it with the
            # algebraically coupled terminal-to-best retention ratio.
            contrast["terminal_final_score"] = score_sequence[-1]
        pairs.append(
            {
                "world_seed": row["world_seed"],
                "trajectory_replicate_id": row["trajectory_replicate_id"],
                "opaque_state": row["opaque_state"],
                "nominal_state": row["nominal_state"],
                "pair_complete": row["pair_complete"],
                "nominal_minus_opaque": contrast,
            }
        )
    return {
        "status": audit["status"],
        "audit_sha256": audit["audit_sha256"],
        "matrix": matrix,
        "paired_trajectories": pairs,
        "within_world_descriptive_aggregates": audit["within_world_descriptive_aggregates"],
        "interpretation": audit["interpretation"],
    }


def build_arxiv_v1_derived_data(
    *,
    g0_v10_path: Path,
    g0_v12_path: Path,
    task_design_path: Path,
    experiment_ledger_path: Path,
    g2_v04_audit_path: Path,
    g2_v05_audit_path: Path | None = None,
) -> dict[str, Any]:
    """Build a compact, auditable paper-data object from frozen inputs."""

    g0_v10 = _load_json(g0_v10_path, label="G0 v1.0 summary")
    g0_v12 = _load_json(g0_v12_path, label="G0 v1.2 summary")
    task_design = _load_json(task_design_path, label="task design audit")
    experiment_ledger = _load_json(
        experiment_ledger_path,
        label="arXiv experiment ledger",
    )
    g2_v04 = _load_json(g2_v04_audit_path, label="G2 v0.4 audit")
    _require(g0_v10.get("formal_result") is True, "G0 v1.0 is not formal")
    _require(g0_v12.get("formal_result") is True, "G0 v1.2 is not formal")
    _require(
        g0_v12.get("confirmatory_analysis_complete") is True,
        "G0 v1.2 analysis is incomplete",
    )
    task_rows, world_rows, baseline_rows = _task_rows(g0_v10, g0_v12)
    g2_cells, g2_pairs, demonstration = _g2_v04_rows(g2_v04)
    g2_v05 = None
    sources = {
        "g0_v1_0": _source(g0_v10_path, canonical_json=True),
        "g0_v1_2": _source(g0_v12_path, canonical_json=True),
        "task_design": _source(task_design_path, canonical_json=True),
        "experiment_ledger": _source(
            experiment_ledger_path,
            canonical_json=True,
        ),
        "g2_v0_4": _source(g2_v04_audit_path, canonical_json=True),
        "g2_v0_5": None,
    }
    if g2_v05_audit_path is not None:
        g2_v05_audit = _load_json(g2_v05_audit_path, label="G2 v0.5 audit")
        g2_v05 = _g2_v05_rows(g2_v05_audit)
        sources["g2_v0_5"] = _source(g2_v05_audit_path, canonical_json=True)
    qualification = dict(experiment_ledger["foundation_qualification"])
    _require(
        qualification["registered_tasks"] == task_design["task_count"],
        "task-design and experiment-ledger task counts disagree",
    )
    validation = task_design["design_validation"]
    _require(
        qualification["deterministic_complete_experiment_cases"]
        == validation["boundary_recipe_case_count"],
        "task-design and experiment-ledger execution-case counts disagree",
    )
    _require(
        qualification["bound_success_endpoints"] == validation["bound_success_metric_count"],
        "task-design and experiment-ledger endpoint counts disagree",
    )
    result: dict[str, Any] = {
        "schema_version": ARXIV_V1_DERIVED_SCHEMA,
        "status": ("frozen_complete" if g2_v05 is not None else "provisional_awaiting_g2_v0_5"),
        "paper_scope": {
            "compiled_experiment_tasks": 2,
            "autonomous_task_count": 1,
            "g0_nonduplicated_physical_experiments": 29580,
            "g2_v0_4_completed_final_assays": 60,
            "g2_v0_5_included": g2_v05 is not None,
            "general_population_prior_effect_allowed": False,
        },
        "sources": sources,
        "environment_qualification": qualification,
        "g0": {
            "task_arm_rows": task_rows,
            "world_arm_rows": world_rows,
            "baseline_rows": baseline_rows,
        },
        "g2_v0_4": {
            "audit_sha256": g2_v04["audit_sha256"],
            "cell_rows": g2_cells,
            "paired_world_rows": g2_pairs,
            "arm_descriptive_aggregates": g2_v04["arm_descriptive_aggregates"],
            "one_experiment_demonstration": demonstration,
        },
        "g2_v0_5": g2_v05,
    }
    result["derived_data_sha256"] = canonical_sha256(result)
    return result


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: (
                        json.dumps(value, ensure_ascii=False, sort_keys=True)
                        if isinstance(value, (dict, list))
                        else value
                    )
                    for key, value in row.items()
                }
            )


def write_arxiv_v1_tables(output_dir: Path, data: Mapping[str, Any]) -> list[Path]:
    """Write deterministic CSV views; every value comes from ``data``."""

    outputs = [
        output_dir / "g0-task-arm.csv",
        output_dir / "g0-world-arm.csv",
        output_dir / "g0-baselines.csv",
        output_dir / "g2-v0.4-cells.csv",
        output_dir / "g2-v0.4-paired-worlds.csv",
    ]
    rows = [
        data["g0"]["task_arm_rows"],
        data["g0"]["world_arm_rows"],
        data["g0"]["baseline_rows"],
        data["g2_v0_4"]["cell_rows"],
        data["g2_v0_4"]["paired_world_rows"],
    ]
    if data["g2_v0_5"] is not None:
        outputs.append(output_dir / "g2-v0.5-paired-trajectories.csv")
        rows.append(data["g2_v0_5"]["paired_trajectories"])
    for path, table_rows in zip(outputs, rows, strict=True):
        _write_csv(path, table_rows)
    return outputs


__all__ = [
    "ARXIV_V1_DERIVED_SCHEMA",
    "ArxivV1DerivedDataError",
    "build_arxiv_v1_derived_data",
    "canonical_sha256",
    "file_sha256",
    "write_arxiv_v1_tables",
    "write_json",
]
