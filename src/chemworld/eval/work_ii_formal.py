"""Outcome-blind manifest construction for the Work II formal matrix."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
from uuid import uuid4

from chemworld.eval.provenance import canonical_json_sha256, file_sha256

FORMAL_PREFLIGHT_VERSION = "chemworld-work-ii-formal-matrix-preflight-0.1"
FORMAL_CELL_VERSION = "chemworld-work-ii-formal-cell-0.1"
FORMAL_ARMS = ("opaque", "aligned_nominal", "misindexed_nominal")
FORMAL_SNAPSHOT_STAGES = (
    "pre_evidence",
    "after_experiment_1",
    "after_experiment_2",
    "final",
)
FORMAL_CHECKPOINT_EXPERIMENTS = (0, 1, 2, 4)
FORMAL_RECEIPT_VERSION = "chemworld-work-ii-formal-cell-receipt-0.1"
FORMAL_STORE_AUDIT_VERSION = "chemworld-work-ii-formal-store-audit-0.1"
FORMAL_TERMINAL_STATES = frozenset({"completed", "right_censored", "failed"})

EXPECTED_PARTICIPANT_EXECUTION_CONTRACT: dict[str, Any] = {
    "execution_unit": "task_x_prior_arm_x_world_seed_cell",
    "session_scope": "campaign",
    "accepted_scientific_codex_processes_per_cell": 1,
    "accepted_participant_provider_sessions_per_cell": 1,
    "accepted_participant_model_calls_per_cell": 1,
    "same_session_bindings": [
        "operation_tool_loop",
        "complete_experiments",
        "belief_checkpoints",
        "final_recommendation",
        "provider_receipt",
    ],
    "interaction_contract": {
        "decision_scope": "one_operation_after_each_public_outcome",
        "tool_transport": "host_owned_stdio_mcp",
        "participant_owns_operation_selection": True,
        "host_roles": [
            "schema_validation",
            "transaction_execution",
            "campaign_resource_accounting",
            "hidden_world_execution",
        ],
        "automatic_action_repair": False,
        "automatic_closeout": False,
        "checkpoint_provider_calls": 0,
    },
    "context_and_memory_contract": {
        "context_scope": (
            "one_complete_provider_process_transcript_plus_participant_visible_public_outcomes"
        ),
        "checkpoint_state_schema": "typed_work_ii_belief_snapshot",
        "checkpoint_top_level_fields": [
            "prior_assessment",
            "predictions",
            "law_summary",
            "evidence_ids",
            "next_experiment_intent",
            "overall_confidence",
        ],
        "persistent_workspace_notes_allowed": False,
        "free_text_persistent_memory_allowed": False,
        "bounded_schema_rationale_fields_allowed": True,
        "private_chain_of_thought_retained": False,
    },
    "sampling_contract": {
        "reasoning_effort": "medium",
        "temperature": None,
        "temperature_semantics": "not_exposed_or_set_by_the_codex_harness",
    },
    "timeout_contract_s": {"request": 1200.0, "finalization": 600.0},
    "lifecycle_contract": {
        "explicit_terminate_required_before_final_assay": True,
        "final_assay_closes_completed_experiment": True,
        "explicit_discard_closes_failed_or_abandoned_batch": True,
        "budget_exhaustion_right_censors_open_experiment": True,
        "all_planned_batches_share_one_campaign_resource_card": True,
    },
    "failure_and_retry_contract": {
        "missing_infrastructure_only_resume": True,
        "scientific_or_method_failure_retained": True,
        "persisted_scientific_trajectory_forbids_replacement": True,
        "result_direction_retry_forbidden": True,
    },
    "separate_reported_denominators": [
        "host_provider_process_attempt",
        "provider_session",
        "mcp_tool_call",
        "operation_attempt",
        "committed_operation",
        "complete_experiment",
        "participant_cell",
        "blind_evaluator_execution",
    ],
}

EXPECTED_REFERENCE_POLICY_CONTRACT: dict[str, Any] = {
    "role": "calibration_or_mechanism_reference_only",
    "participant_formal_denominator": False,
    "participant_information_arms": [
        "opaque_id_only",
        "aligned_property_aware",
        "misindexed_property_matched",
    ],
    "required_semantics_free_calibration_pair": {
        "policy_identity_matched": True,
        "information_conditions": ["id_only", "public_property_vector"],
        "world_and_resource_contract_matched": True,
    },
    "calibration_execution_in_75_participant_cells": False,
    "classical_policy_results_required_for_primary_h3": False,
    "classical_policy_results_required_for_resource_calibrated_interpretation": True,
    "outcome_based_method_arm_deletion_forbidden": True,
}

_SOURCE_PATHS = (
    "src/chemworld/agents/interactive_codex_experiment.py",
    "src/chemworld/agents/experiment_codex_ipc.py",
    "src/chemworld/agents/experiment_codex_mcp.py",
    "src/chemworld/campaign_resources.py",
    "src/chemworld/eval/runner.py",
    "src/chemworld/eval/verify.py",
    "src/chemworld/eval/work_ii_analysis.py",
    "src/chemworld/eval/work_ii_blind.py",
    "src/chemworld/eval/work_ii_formal.py",
    "src/chemworld/eval/work_ii_prior_discovery.py",
    "src/chemworld/eval/work_ii_process_profile.py",
    "src/chemworld/eval/work_ii_qualification.py",
    "src/chemworld/eval/work_ii_report.py",
    "src/chemworld/eval/work_ii_truth.py",
    "scripts/analyze_work_ii_formal.py",
    "scripts/run_work_ii_campaign_pilot.py",
    "scripts/run_work_ii_formal_matrix.py",
    "pyproject.toml",
    "uv.lock",
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _object(value: object, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    return value


def _string_list(value: object, label: str) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ValueError(f"{label} must be a list")
    result = [str(item) for item in value]
    if not result or len(set(result)) != len(result):
        raise ValueError(f"{label} must be a non-empty unique list")
    return result


def build_checkpoint_contract(config: Mapping[str, Any], arm: str) -> dict[str, Any]:
    """Materialize the complete public checkpoint contract used by one cell."""

    if arm not in FORMAL_ARMS:
        raise ValueError(f"unknown prior arm: {arm}")
    nominal = arm != "opaque"
    configured = config.get("belief_checkpoint")
    if isinstance(configured, Mapping):
        held_out_queries = [
            dict(_object(item, "held_out_query")) for item in configured["held_out_queries"]
        ]
        metric_ids = _string_list(configured["allowed_metric_ids"], "allowed_metric_ids")
        feature_ids = _string_list(configured["allowed_feature_ids"], "allowed_feature_ids")
        prior_fields = _string_list(configured["allowed_prior_fields"], "allowed_prior_fields")
    else:
        metric_ids = ["selective_product_yield", "energy_efficiency", "safety_risk"]
        feature_ids = [
            "electrolyte_profile",
            "solvent",
            "reagent_amount_mol",
            "potential_V",
            "current_mA",
            "duration_s",
        ]
        prior_fields = ["electrolyte_profile", "solvent"]
        held_out_queries = [
            {
                "query_id": query_id,
                "feature_values": {
                    "electrolyte_profile": electrolyte_profile,
                    "solvent": solvent,
                    "reagent_amount_mol": 0.01,
                    "potential_V": 0.8,
                    "current_mA": 100.0,
                    "duration_s": 1800.0,
                },
                "metric_ids": metric_ids,
            }
            for query_id, electrolyte_profile, solvent in (
                ("q-low", 0, 0),
                ("q-electrolyte", 3, 0),
                ("q-solvent", 0, 3),
                ("q-high", 3, 3),
            )
        ]
    query_metric_contract = {
        str(item["query_id"]): [str(metric) for metric in item.get("metric_ids", metric_ids)]
        for item in held_out_queries
    }
    complete_experiments = int(_object(config["campaign"], "campaign")["complete_experiments"])
    snapshot_stages = [
        str(item)
        for item in config.get(
            "snapshot_stages",
            ["pre_evidence", "post_neutral", "post_discriminating", "final"],
        )
    ]
    if len(snapshot_stages) != 4 or len(set(snapshot_stages)) != 4:
        raise ValueError("snapshot_stages must contain four unique stage IDs")
    checkpoint_experiments = [
        int(item)
        for item in _object(config["campaign"], "campaign")["checkpoint_complete_experiments"]
    ]
    return {
        "schema_version": "chemworld-work-ii-campaign-checkpoint-contract-0.1",
        "snapshot_stages": snapshot_stages,
        "checkpoint_complete_experiments": checkpoint_experiments,
        "query_metric_contract": query_metric_contract,
        "held_out_queries": held_out_queries,
        "allowed_feature_ids": feature_ids,
        "allowed_metric_ids": metric_ids,
        "allowed_prior_fields": prior_fields,
        "evidence_catalog": [
            f"experiment-{index}-final-assay" for index in range(1, complete_experiments + 1)
        ],
        "nominal_information_available": nominal,
        "stage_labels_are_checkpoint_ids_only": True,
        "physical_experiment_selection_authority": "participant",
    }


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"formal binding is outside the repository: {path}") from error


def _binding(root: Path, relative_path: str) -> dict[str, str]:
    path = root / relative_path
    if not path.is_file():
        raise ValueError(f"missing formal dependency: {relative_path}")
    return {
        "path": relative_path,
        "sha256": file_sha256(path),
        "hash_kind": "file_sha256",
    }


def _self_hash(payload: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in payload.items() if key != "preflight_sha256"}
    )


def _cell_key_hash(cell: Mapping[str, Any]) -> str:
    return canonical_json_sha256(
        {key: value for key, value in cell.items() if key != "cell_key_sha256"}
    )


def _write_json_once(path: Path, payload: Mapping[str, Any]) -> None:
    """Atomically publish a JSON artifact without ever replacing a prior file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_temp = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(raw_temp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise DuplicateFormalCellError(
                f"immutable formal cell artifact already exists: {path}"
            ) from error
    finally:
        temporary.unlink(missing_ok=True)


class DuplicateFormalCellError(RuntimeError):
    """A terminal formal cell would be executed or published more than once."""


class InvalidFormalCellReceiptError(RuntimeError):
    """A formal cell receipt does not satisfy its immutable binding."""


class ProviderAttemptLimitError(RuntimeError):
    """A formal cell exhausted its preregistered provider process launch cap."""


class WorkIIFormalCellStore:
    """Write-once terminal receipts plus append-only infrastructure attempts."""

    def __init__(self, root: Path, manifest: Mapping[str, Any]) -> None:
        errors = validate_formal_preflight(manifest)
        if errors:
            raise ValueError("invalid formal manifest: " + "; ".join(errors))
        self.root = Path(root)
        self.receipts = self.root / "terminal_receipts"
        self.infrastructure_attempts = self.root / "infrastructure_attempts"
        self.provider_attempts = self.root / "provider_attempt_receipts"
        cells = manifest.get("cells", [])
        self.cells = {
            str(cell["cell_key_sha256"]): dict(cell) for cell in cells if isinstance(cell, Mapping)
        }
        if len(self.cells) != len(cells):
            raise ValueError("formal manifest contains duplicate cell keys")

    def receipt_path(self, cell_key_sha256: str) -> Path:
        self._cell(cell_key_sha256)
        return self.receipts / f"{cell_key_sha256}.json"

    def has_terminal(self, cell_key_sha256: str) -> bool:
        return self.receipt_path(cell_key_sha256).is_file()

    def write_terminal(
        self,
        cell_key_sha256: str,
        *,
        state: str,
        reason_code: str,
        result: Mapping[str, Any],
    ) -> Path:
        cell = self._cell(cell_key_sha256)
        if state not in FORMAL_TERMINAL_STATES:
            raise ValueError(f"unsupported formal terminal state: {state}")
        expected_prefixes = {
            "completed": ("scientific_completed_",),
            "right_censored": (
                "scientific_right_censored_",
                "method_right_censored_",
            ),
            "failed": ("method_failed_",),
        }[state]
        if not reason_code.startswith(expected_prefixes):
            raise ValueError(f"{state} formal cell reason code has an invalid domain prefix")
        result_payload = dict(result)
        payload = {
            "schema_version": FORMAL_RECEIPT_VERSION,
            "cell_key_sha256": cell_key_sha256,
            "cell": cell,
            "state": state,
            "reason_domain": ("scientific" if reason_code.startswith("scientific_") else "method"),
            "reason_code": reason_code,
            "result": result_payload,
            "result_sha256": canonical_json_sha256(result_payload),
        }
        payload["receipt_sha256"] = canonical_json_sha256(payload)
        target = self.receipt_path(cell_key_sha256)
        _write_json_once(target, payload)
        return target

    def load_terminal(self, cell_key_sha256: str) -> dict[str, Any]:
        path = self.receipt_path(cell_key_sha256)
        payload = _load_object(path)
        self._validate_receipt(payload, expected_key=cell_key_sha256)
        return payload

    def record_infrastructure_failure(
        self,
        cell_key_sha256: str,
        error: BaseException,
        *,
        log_reference: str | None = None,
        log_sha256: str | None = None,
    ) -> Path:
        cell = self._cell(cell_key_sha256)
        if (log_reference is None) != (log_sha256 is None):
            raise ValueError("log reference and digest must be supplied together")
        payload = {
            "schema_version": FORMAL_RECEIPT_VERSION,
            "cell_key_sha256": cell_key_sha256,
            "cell_id": cell["cell_id"],
            "state": "retryable_infrastructure_failure",
            "reason_domain": "infrastructure",
            "reason_code": "infrastructure_cell_attempt_failed",
            "error_type": type(error).__name__,
            "error_message": str(error)[:2000],
            "log_reference": log_reference,
            "log_sha256": log_sha256,
        }
        payload["attempt_sha256"] = canonical_json_sha256(payload)
        target = self.infrastructure_attempts / cell_key_sha256 / f"{uuid4().hex}.json"
        _write_json_once(target, payload)
        return target

    def record_provider_attempt_launch(
        self,
        cell_key_sha256: str,
        *,
        attempt_id: str,
    ) -> Path:
        cell = self._cell(cell_key_sha256)
        existing = sorted((self.provider_attempts / cell_key_sha256).glob("*.json"))
        limit = int(cell["provider_attempt_limit"])
        if len(existing) >= limit:
            raise ProviderAttemptLimitError(
                f"formal cell exhausted provider attempt cap {limit}: {cell['cell_id']}"
            )
        payload = {
            "schema_version": FORMAL_RECEIPT_VERSION,
            "cell_key_sha256": cell_key_sha256,
            "cell_id": cell["cell_id"],
            "attempt_id": attempt_id,
            "attempt_index": len(existing) + 1,
            "attempt_limit": limit,
            "state": "provider_process_launch_authorized",
            "reason_domain": "method",
        }
        payload["attempt_sha256"] = canonical_json_sha256(payload)
        target = self.provider_attempts / cell_key_sha256 / f"{attempt_id}.json"
        _write_json_once(target, payload)
        return target

    def pending_cells(self, *, resume: bool) -> list[dict[str, Any]]:
        audit = self.audit()
        if audit["invalid_receipts"] or audit["unexpected_cell_key_sha256"]:
            raise InvalidFormalCellReceiptError(
                "formal store contains invalid or unexpected terminal receipts"
            )
        if audit["terminal_count"] and not resume:
            raise DuplicateFormalCellError(
                "formal store already contains terminal cells; use missing-only resume"
            )
        completed = set(audit["terminal_cell_key_sha256"])
        attempt_counts = audit["provider_attempt_counts_by_cell_key_sha256"]
        exhausted = [
            cell["cell_id"]
            for key, cell in self.cells.items()
            if key not in completed
            and int(attempt_counts.get(key, 0)) >= int(cell["provider_attempt_limit"])
        ]
        if exhausted:
            raise ProviderAttemptLimitError(
                "missing formal cells exhausted their provider attempt cap: " + ", ".join(exhausted)
            )
        return [dict(cell) for key, cell in self.cells.items() if key not in completed]

    def audit(self) -> dict[str, Any]:
        observed: dict[str, Mapping[str, Any]] = {}
        invalid: list[str] = []
        for path in sorted(self.receipts.glob("*.json")):
            try:
                payload = _load_object(path)
                key = str(payload["cell_key_sha256"])
                self._validate_receipt(payload)
                if path.stem != key or key in observed:
                    raise ValueError("receipt path or uniqueness invariant failed")
                observed[key] = payload
            except (
                KeyError,
                OSError,
                TypeError,
                ValueError,
                json.JSONDecodeError,
                InvalidFormalCellReceiptError,
            ):
                invalid.append(path.as_posix())
        provider_attempt_indices: dict[str, set[int]] = {}
        for path in sorted(self.provider_attempts.glob("*/*.json")):
            try:
                payload = _load_object(path)
                key = str(payload["cell_key_sha256"])
                attempt_id = str(payload["attempt_id"])
                expected_hash = canonical_json_sha256(
                    {name: value for name, value in payload.items() if name != "attempt_sha256"}
                )
                cell = self.cells[key]
                attempt_index = int(payload.get("attempt_index", -1))
                observed_indices = provider_attempt_indices.setdefault(key, set())
                if (
                    payload.get("schema_version") != FORMAL_RECEIPT_VERSION
                    or payload.get("state") != "provider_process_launch_authorized"
                    or payload.get("reason_domain") != "method"
                    or payload.get("attempt_sha256") != expected_hash
                    or path.parent.name != key
                    or path.stem != attempt_id
                    or attempt_index < 1
                    or attempt_index > int(cell["provider_attempt_limit"])
                    or attempt_index in observed_indices
                    or int(payload.get("attempt_limit", -1)) != int(cell["provider_attempt_limit"])
                ):
                    raise ValueError("provider attempt invariant failed")
                observed_indices.add(attempt_index)
            except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError):
                invalid.append(path.as_posix())
        provider_attempt_counts = {
            key: len(indices) for key, indices in provider_attempt_indices.items()
        }
        infrastructure_attempt_count = 0
        recovered: set[str] = set()
        for path in sorted(self.infrastructure_attempts.glob("*/*.json")):
            try:
                payload = _load_object(path)
                key = str(payload["cell_key_sha256"])
                expected_hash = canonical_json_sha256(
                    {name: value for name, value in payload.items() if name != "attempt_sha256"}
                )
                if (
                    payload.get("schema_version") != FORMAL_RECEIPT_VERSION
                    or payload.get("state") != "retryable_infrastructure_failure"
                    or payload.get("reason_domain") != "infrastructure"
                    or payload.get("attempt_sha256") != expected_hash
                    or key not in self.cells
                    or path.parent.name != key
                ):
                    raise ValueError("infrastructure attempt invariant failed")
                infrastructure_attempt_count += 1
                if key in observed:
                    recovered.add(key)
            except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError):
                invalid.append(path.as_posix())
        expected = set(self.cells)
        observed_keys = set(observed)
        state_counts = {
            state: sum(payload.get("state") == state for payload in observed.values())
            for state in sorted(FORMAL_TERMINAL_STATES)
        }
        report: dict[str, Any] = {
            "schema_version": FORMAL_STORE_AUDIT_VERSION,
            "expected_cell_count": len(expected),
            "terminal_count": len(observed_keys & expected),
            "state_counts": state_counts,
            "terminal_cell_key_sha256": sorted(observed_keys & expected),
            "missing_cell_key_sha256": sorted(expected - observed_keys),
            "unexpected_cell_key_sha256": sorted(observed_keys - expected),
            "invalid_receipts": invalid,
            "infrastructure_attempt_count": infrastructure_attempt_count,
            "provider_attempt_count": sum(provider_attempt_counts.values()),
            "provider_attempt_counts_by_cell_key_sha256": provider_attempt_counts,
            "recovered_infrastructure_failure_count": len(recovered),
            "complete": (
                observed_keys == expected and not invalid and not (observed_keys - expected)
            ),
        }
        report["audit_sha256"] = canonical_json_sha256(report)
        return report

    def _cell(self, cell_key_sha256: str) -> dict[str, Any]:
        try:
            return self.cells[str(cell_key_sha256)]
        except KeyError as error:
            raise ValueError(f"unknown formal cell key: {cell_key_sha256}") from error

    def _validate_receipt(
        self,
        payload: Mapping[str, Any],
        *,
        expected_key: str | None = None,
    ) -> None:
        key = str(payload.get("cell_key_sha256", ""))
        state = str(payload.get("state", ""))
        cell = payload.get("cell")
        result = payload.get("result")
        expected_receipt_hash = canonical_json_sha256(
            {name: value for name, value in payload.items() if name != "receipt_sha256"}
        )
        if (
            payload.get("schema_version") != FORMAL_RECEIPT_VERSION
            or key not in self.cells
            or cell != self.cells.get(key)
            or _cell_key_hash(cell) != key
            or state not in FORMAL_TERMINAL_STATES
            or not isinstance(result, Mapping)
            or canonical_json_sha256(result) != payload.get("result_sha256")
            or payload.get("receipt_sha256") != expected_receipt_hash
        ):
            raise InvalidFormalCellReceiptError("invalid formal terminal receipt")
        if expected_key is not None and key != expected_key:
            raise InvalidFormalCellReceiptError(
                "formal terminal receipt does not match the expected cell"
            )


def build_formal_preflight(
    root: Path,
    design_path: Path,
    analysis_path: Path,
) -> dict[str, Any]:
    """Build the deterministic 75-cell public schedule without provider execution."""

    root = root.resolve()
    design_path = design_path.resolve()
    analysis_path = analysis_path.resolve()
    design = _load_object(design_path)
    analysis = _load_object(analysis_path)
    errors: list[str] = []

    design_digest = canonical_json_sha256(design)
    analysis_digest = canonical_json_sha256(analysis)
    analysis_binding = _object(analysis.get("design_binding"), "analysis.design_binding")
    if analysis_binding.get("sha256") != design_digest:
        errors.append("analysis plan does not bind the current formal design")
    arms = tuple(_string_list(design.get("prior_arms"), "design.prior_arms"))
    if arms != FORMAL_ARMS:
        errors.append("formal prior-arm order differs from the frozen three-arm contract")
    population = _object(analysis.get("analysis_population"), "analysis_population")
    if tuple(population.get("prior_arms", [])) != FORMAL_ARMS:
        errors.append("analysis population prior arms differ from the formal design")

    world_cohort = _object(design.get("world_cohort"), "world_cohort")
    development = _object(
        world_cohort.get("development_and_qualification"),
        "world_cohort.development_and_qualification",
    )
    public = _object(world_cohort.get("public_formal"), "world_cohort.public_formal")
    private = _object(
        world_cohort.get("private_confirmation"),
        "world_cohort.private_confirmation",
    )
    task_world_seeds = _object(public.get("task_world_seeds"), "task_world_seeds")
    development_seeds = [int(item) for item in development.get("world_seeds", [])]
    public_namespace_start = int(public.get("namespace_start", -1))
    public_namespace_size = int(public.get("namespace_size", -1))
    private_namespace_start = int(private.get("namespace_start", -1))
    private_namespace_size = int(private.get("namespace_size", -1))
    public_namespace_end = public_namespace_start + public_namespace_size
    private_namespace_end = private_namespace_start + private_namespace_size
    namespace_disjoint = (
        public_namespace_end <= private_namespace_start
        or private_namespace_end <= public_namespace_start
    )
    private_commitment = private.get("sealed_identity_commitment_sha256")
    if len(development_seeds) != len(set(development_seeds)):
        errors.append("development/qualification world identities are duplicated")
    if public_namespace_start < 0 or public_namespace_size <= 0:
        errors.append("public formal world namespace is invalid")
    if private_namespace_start < 0 or private_namespace_size <= 0:
        errors.append("private confirmation world namespace is invalid")
    if not namespace_disjoint:
        errors.append("public and private world namespaces overlap")
    if (
        not isinstance(private_commitment, str)
        or len(private_commitment) != 64
        or any(character not in "0123456789abcdef" for character in private_commitment)
    ):
        errors.append("private confirmation identity commitment is invalid")
    if private.get("identities_tracked_in_git") is not False:
        errors.append("private confirmation identities must remain outside Git")
    raw_tasks = design.get("tasks")
    if isinstance(raw_tasks, (str, bytes)) or not isinstance(raw_tasks, Sequence):
        raise ValueError("design.tasks must be a list")
    tasks = [dict(_object(item, "design task")) for item in raw_tasks]
    if len(tasks) != 5:
        errors.append("formal design must contain exactly five tasks")

    participant_execution_contract = dict(
        _object(
            design.get("participant_execution_contract"),
            "participant_execution_contract",
        )
    )
    if participant_execution_contract != EXPECTED_PARTICIPANT_EXECUTION_CONTRACT:
        errors.append("formal participant execution contract differs from the frozen method")
    reference_policy_contract = dict(
        _object(design.get("reference_policy_contract"), "reference_policy_contract")
    )
    if reference_policy_contract != EXPECTED_REFERENCE_POLICY_CONTRACT:
        errors.append("formal reference-policy contract differs from the frozen role")
    participant_execution_contract_sha256 = canonical_json_sha256(participant_execution_contract)

    cells: list[dict[str, Any]] = []
    task_bindings: list[dict[str, Any]] = []
    provider_contract: dict[str, Any] | None = None
    attempt_contract = dict(
        _object(design.get("provider_attempt_contract"), "provider_attempt_contract")
    )
    expected_attempt_contract = {
        "attempt_unit": "host_codex_process_launch",
        "initial_attempts_per_cell": 1,
        "maximum_infrastructure_resume_attempts_per_cell": 1,
        "maximum_total_provider_attempts_per_cell": 2,
        "pre_action_restart_limit_within_attempt": 0,
        "any_persisted_trajectory_forbids_replacement": True,
        "retry_after_scientific_operation_forbidden": True,
        "public_matrix_initial_attempt_count": 75,
        "public_matrix_provider_attempt_hard_cap": 150,
    }
    if attempt_contract != expected_attempt_contract:
        errors.append("formal provider-attempt contract differs from the frozen cap")
    blind_contract = dict(
        _object(design.get("blind_evaluator_contract"), "blind_evaluator_contract")
    )
    expected_blind_contract = {
        "participant_final_recommendations_per_cell": 1,
        "recommendation_unit": "one_selected_completed_experiment_index",
        "candidate_experiment_indices": [1, 2, 3, 4],
        "incumbent_definition": (
            "highest_participant_observed_leaderboard_score_tie_smallest_index"
        ),
        "blind_targets_per_cell": [
            "observed_incumbent",
            "participant_final_recommendation",
        ],
        "blind_replicates_per_target": 3,
        "paired_noise_within_replicate": True,
        "participant_feedback_from_blind_evaluator": False,
        "evaluator_provider_calls": 0,
        "evaluator_trajectory_separate_from_participant": True,
        "evaluator_resources_excluded_from_participant_ledger": True,
        "public_matrix_final_recommendation_count": 75,
        "public_matrix_blind_target_count": 150,
        "public_matrix_blind_execution_count": 450,
    }
    if blind_contract != expected_blind_contract:
        errors.append("formal blind-evaluator contract differs from the frozen denominator")
    truth_contract = dict(
        _object(
            design.get("held_out_evaluator_contract"),
            "held_out_evaluator_contract",
        )
    )
    expected_truth_contract = {
        "truth_unit": "task_x_world_cluster_x_registered_query",
        "queries_per_task_world_cluster": 4,
        "public_matrix_truth_execution_count": 100,
        "public_matrix_truth_query_metric_count": 340,
        "shared_across_prior_arms_and_checkpoints": True,
        "one_frozen_complete_experiment_per_query": True,
        "keyed_observation_coordinate_per_query": True,
        "exact_replay_required": True,
        "failed_truth_executions_retained_without_replacement": True,
        "evaluator_provider_calls": 0,
        "participant_feedback_from_truth_evaluator": False,
        "evaluator_trajectory_separate_from_participant": True,
        "evaluator_resources_excluded_from_participant_ledger": True,
        "frozen_unregistered_controls": {
            "reaction-to-crystallization": {
                "stirring_speed_rpm": 675.0,
                "catalyst_amount_mol": 0.000315,
            },
            "reaction-to-distillation": {
                "stirring_speed_rpm": 675.0,
                "catalyst_amount_mol": 0.000315,
                "evaporation_temperature_K": 332.5,
                "evaporation_duration_s": 900.0,
                "transfer_fraction": 0.77,
            },
            "partition-discovery": {"solvent_volume_L": 0.02},
            "reaction-safety-constrained": {"stirring_speed_rpm": 675.0},
        },
        "query_field_aliases": {
            "partition-discovery": {"aqueous_phase_volume_L": "aqueous_volume_L"}
        },
    }
    if truth_contract != expected_truth_contract:
        errors.append("formal held-out evaluator contract differs from the frozen denominator")
    total_query_count = 0
    total_query_metric_count = 0
    evaluator_truth_execution_count = 0
    evaluator_truth_query_metric_count = 0
    public_world_seeds: list[int] = []
    for task_index, task in enumerate(tasks, start=1):
        task_id = str(task.get("task_id"))
        relative_config = str(task.get("campaign_config"))
        config_path = root / relative_config
        config = _load_object(config_path)
        if config.get("task_id") != task_id:
            errors.append(f"{task_id}: campaign task identity mismatch")
        if tuple(config.get("prior_arms", {})) != FORMAL_ARMS:
            errors.append(f"{task_id}: campaign prior-arm order mismatch")
        opaque_contract = build_checkpoint_contract(config, "opaque")
        aligned_contract = build_checkpoint_contract(config, "aligned_nominal")
        misindexed_contract = build_checkpoint_contract(config, "misindexed_nominal")
        if aligned_contract != misindexed_contract:
            errors.append(f"{task_id}: informed checkpoint contracts are not matched")
        if tuple(opaque_contract["snapshot_stages"]) != FORMAL_SNAPSHOT_STAGES:
            errors.append(f"{task_id}: checkpoint stage IDs are not the neutral formal IDs")
        if (
            tuple(opaque_contract["checkpoint_complete_experiments"])
            != FORMAL_CHECKPOINT_EXPERIMENTS
        ):
            errors.append(f"{task_id}: checkpoint experiment schedule differs from formal design")
        if int(_object(config["campaign"], "campaign")["complete_experiments"]) != 4:
            errors.append(f"{task_id}: formal campaign must contain four experiments")
        campaign = _object(config["campaign"], f"{task_id}.campaign")
        method_resources = _object(config.get("method_resources"), f"{task_id}.method_resources")
        execution = _object(config.get("execution"), f"{task_id}.execution")
        if config.get("episode_mode") != "campaign":
            errors.append(f"{task_id}: participant session scope is not campaign")
        if int(method_resources.get("model_call_limit", -1)) != 1:
            errors.append(f"{task_id}: model-call limit is not one per cell")
        if int(method_resources.get("operation_limit", -1)) != int(
            campaign.get("operation_attempt_limit", -2)
        ):
            errors.append(f"{task_id}: method and campaign operation limits differ")
        if int(method_resources.get("complete_experiment_limit", -1)) != 4:
            errors.append(f"{task_id}: method complete-experiment limit differs")
        if method_resources.get("checkpoint_complete_experiments") != [1, 2, 4]:
            errors.append(f"{task_id}: method checkpoint resource schedule differs")
        if (
            int(execution.get("max_concurrency", -1)) != 3
            or int(execution.get("within_cell_concurrency", -1)) != 1
            or execution.get("parallelization_unit") != "same_seed_prior_arm_triplet"
        ):
            errors.append(f"{task_id}: execution concurrency contract differs")
        provider = dict(_object(config.get("provider"), f"{task_id}.provider"))
        reduced_provider = {
            key: provider.get(key)
            for key in (
                "id",
                "name",
                "base_url",
                "wire_api",
                "model",
                "reasoning_effort",
                "request_timeout_s",
                "finalization_timeout_s",
            )
        }
        timeout_contract = participant_execution_contract["timeout_contract_s"]
        sampling_contract = participant_execution_contract["sampling_contract"]
        if (
            provider.get("reasoning_effort") != sampling_contract["reasoning_effort"]
            or float(provider.get("request_timeout_s", -1.0)) != float(timeout_contract["request"])
            or float(provider.get("finalization_timeout_s", -1.0))
            != float(timeout_contract["finalization"])
        ):
            errors.append(f"{task_id}: provider sampling or timeout contract differs")
        if provider_contract is None:
            provider_contract = reduced_provider
        elif provider_contract != reduced_provider:
            errors.append(f"{task_id}: provider/model/scaffold axis drift")
        seeds = [int(item) for item in task_world_seeds.get(task_id, [])]
        if len(seeds) != 5 or len(set(seeds)) != 5:
            errors.append(f"{task_id}: public world schedule must contain five unique seeds")
        public_world_seeds.extend(seeds)
        for seed in seeds:
            if not public_namespace_start <= seed < public_namespace_end:
                errors.append(f"{task_id}: public world seed is outside its namespace")
            if seed in development_seeds:
                errors.append(f"{task_id}: public world seed overlaps qualification")
            if private_namespace_start <= seed < private_namespace_end:
                errors.append(f"{task_id}: public world seed enters the private namespace")
        config_binding = _binding(root, relative_config)
        checkpoint_digest = canonical_json_sha256(opaque_contract)
        query_count = len(opaque_contract["query_metric_contract"])
        query_metric_count = sum(
            len(metric_ids) for metric_ids in opaque_contract["query_metric_contract"].values()
        )
        evaluator_truth_execution_count += query_count * len(seeds)
        evaluator_truth_query_metric_count += query_metric_count * len(seeds)
        task_bindings.append(
            {
                "task_id": task_id,
                "campaign_config": config_binding,
                "checkpoint_contract_sha256": checkpoint_digest,
                "held_out_query_count_per_snapshot": query_count,
                "held_out_query_metric_count_per_snapshot": query_metric_count,
            }
        )
        for world_index, world_seed in enumerate(seeds, start=1):
            cluster_id = f"work-ii-public-{task_index:02d}-{world_index:02d}"
            for arm_index, arm in enumerate(FORMAL_ARMS, start=1):
                cell_id = f"{cluster_id}-arm-{arm_index:02d}"
                checkpoint = build_checkpoint_contract(config, arm)
                cell = {
                    "schema_version": FORMAL_CELL_VERSION,
                    "schedule_index": len(cells) + 1,
                    "cell_id": cell_id,
                    "world_cluster_id": cluster_id,
                    "task_id": task_id,
                    "world_index": world_index,
                    "world_seed": world_seed,
                    "world_split": "public_formal",
                    "prior_arm": arm,
                    "campaign_config_path": relative_config,
                    "campaign_config_sha256": config_binding["sha256"],
                    "checkpoint_contract_sha256": canonical_json_sha256(checkpoint),
                    "participant_execution_contract_sha256": (
                        participant_execution_contract_sha256
                    ),
                    "complete_experiment_count": 4,
                    "belief_checkpoint_count": 4,
                    "held_out_query_count_per_snapshot": query_count,
                    "held_out_query_metric_count_per_snapshot": query_metric_count,
                    "provider_session_limit": 1,
                    "provider_attempt_limit": int(
                        attempt_contract.get("maximum_total_provider_attempts_per_cell", -1)
                    ),
                    "provider_repeat": 1,
                    "participant_final_recommendation_count": 1,
                    "blind_validation_target_count": 2,
                    "blind_replicates_per_target": 3,
                    "blind_validation_execution_count": 6,
                    "terminal_states": ["completed", "right_censored", "failed"],
                }
                cell["cell_key_sha256"] = _cell_key_hash(cell)
                cells.append(cell)
                total_query_count += query_count * 4
                total_query_metric_count += query_metric_count * 4

    cell_ids = [str(cell["cell_id"]) for cell in cells]
    cell_keys = [str(cell["cell_key_sha256"]) for cell in cells]
    cluster_ids = {str(cell["world_cluster_id"]) for cell in cells}
    if len(cells) != 75 or len(set(cell_ids)) != 75 or len(set(cell_keys)) != 75:
        errors.append("formal schedule does not contain 75 unique cells")
    if len(cluster_ids) != 25:
        errors.append("formal schedule does not contain 25 independent world clusters")
    if len(public_world_seeds) != 25 or len(set(public_world_seeds)) != 25:
        errors.append("public formal world schedule does not contain 25 unique identities")
    if int(population.get("scheduled_public_cells", -1)) != len(cells):
        errors.append("analysis cell denominator differs from the generated schedule")
    if int(population.get("independent_task_world_clusters", -1)) != len(cluster_ids):
        errors.append("analysis cluster denominator differs from the generated schedule")

    source_bindings = [_binding(root, path) for path in _SOURCE_PATHS]
    blockers = [
        "formal currency ceiling is not yet approved",
        "current design and analysis plan explicitly forbid formal execution",
        "current persistent-session method lacks its final qualification receipt",
    ]
    if (
        design.get("formal_execution_allowed") is True
        or analysis.get("formal_execution_allowed") is True
    ):
        errors.append("pre-registration inputs unexpectedly allow formal execution")
    report: dict[str, Any] = {
        "schema_version": FORMAL_PREFLIGHT_VERSION,
        "status": "failed" if errors else "passed_execution_blocked",
        "formal_result": False,
        "formal_execution_allowed": False,
        "design_binding": {
            "path": _relative(root, design_path),
            "sha256": design_digest,
            "hash_kind": "canonical_json_sha256",
        },
        "analysis_binding": {
            "path": _relative(root, analysis_path),
            "sha256": analysis_digest,
            "hash_kind": "canonical_json_sha256",
        },
        "provider_contract": provider_contract,
        "participant_execution_contract": participant_execution_contract,
        "participant_execution_contract_sha256": (participant_execution_contract_sha256),
        "reference_policy_contract": reference_policy_contract,
        "provider_attempt_contract": attempt_contract,
        "blind_evaluator_contract": blind_contract,
        "held_out_evaluator_contract": truth_contract,
        "schedule_policy": {
            "order": "task_then_public_world_then_prior_arm",
            "same_world_arm_triplet_max_concurrency": 3,
            "within_cell_concurrency": 1,
            "one_persistent_session_per_cell": True,
            "missing_only_resume": True,
            "accepted_terminal_cells_are_immutable": True,
            "result_direction_early_stopping_forbidden": True,
        },
        "prompt_boundary": {
            "world_seed_exposed_to_participant": False,
            "world_cluster_id_exposed_to_participant": False,
            "prior_arm_label_exposed_to_participant": False,
            "private_identity_exposed_to_participant_or_manifest": False,
            "evaluator_truth_exposed_to_participant": False,
        },
        "world_split_contract": {
            "manifest_split": "public_formal",
            "development_and_qualification_world_seeds": development_seeds,
            "public_formal": {
                "namespace_start": public_namespace_start,
                "namespace_size": public_namespace_size,
                "world_identity_count": len(set(public_world_seeds)),
            },
            "private_confirmation": {
                "namespace_start": private_namespace_start,
                "namespace_size": private_namespace_size,
                "sealed_identity_commitment_sha256": private_commitment,
                "identities_present_in_manifest": False,
            },
            "development_public_identity_disjoint": not bool(
                set(development_seeds) & set(public_world_seeds)
            ),
            "public_private_namespace_disjoint": namespace_disjoint,
        },
        "expected_counts": {
            "tasks": len(tasks),
            "independent_task_world_clusters": len(cluster_ids),
            "participant_cells": len(cells),
            "provider_sessions": len(cells),
            "provider_attempts_initial_planned": len(cells),
            "provider_attempts_hard_cap": len(cells)
            * int(attempt_contract["maximum_total_provider_attempts_per_cell"]),
            "provider_repeats_per_cell": 1,
            "complete_experiments": len(cells) * 4,
            "belief_checkpoints": len(cells) * 4,
            "checkpoint_held_out_queries": total_query_count,
            "checkpoint_held_out_query_metrics": total_query_metric_count,
            "evaluator_truth_executions": evaluator_truth_execution_count,
            "evaluator_truth_query_metrics": evaluator_truth_query_metric_count,
            "participant_final_recommendations": len(cells),
            "blind_validation_targets": len(cells) * 2,
            "blind_validation_executions": len(cells) * 2 * 3,
        },
        "task_bindings": task_bindings,
        "source_bindings": source_bindings,
        "cells": cells,
        "blocking_requirements": blockers,
        "errors": errors,
    }
    report["preflight_sha256"] = _self_hash(report)
    return report


def validate_formal_preflight(report: Mapping[str, Any]) -> list[str]:
    """Validate self-hash, schedule uniqueness, and outcome-blind boundaries."""

    errors: list[str] = []
    if report.get("schema_version") != FORMAL_PREFLIGHT_VERSION:
        errors.append("unexpected formal preflight schema")
    if report.get("preflight_sha256") != _self_hash(report):
        errors.append("formal preflight self-hash mismatch")
    cells = report.get("cells")
    if not isinstance(cells, list):
        errors.append("formal preflight cells are missing")
        return errors
    ids = [cell.get("cell_id") for cell in cells if isinstance(cell, Mapping)]
    keys = [cell.get("cell_key_sha256") for cell in cells if isinstance(cell, Mapping)]
    if len(cells) != 75 or len(set(ids)) != 75 or len(set(keys)) != 75:
        errors.append("formal preflight must contain 75 unique cell identities")
    counts = report.get("expected_counts")
    if not isinstance(counts, Mapping) or counts.get("participant_cells") != len(cells):
        errors.append("formal preflight cell count is inconsistent")
    participant_contract = report.get("participant_execution_contract")
    participant_contract_hash = report.get("participant_execution_contract_sha256")
    if (
        participant_contract != EXPECTED_PARTICIPANT_EXECUTION_CONTRACT
        or participant_contract_hash
        != canonical_json_sha256(EXPECTED_PARTICIPANT_EXECUTION_CONTRACT)
    ):
        errors.append("formal preflight participant execution contract is invalid")
    if report.get("reference_policy_contract") != EXPECTED_REFERENCE_POLICY_CONTRACT:
        errors.append("formal preflight reference-policy contract is invalid")
    for cell in cells:
        if not isinstance(cell, Mapping):
            errors.append("formal preflight contains a malformed cell")
            continue
        if cell.get("cell_key_sha256") != _cell_key_hash(cell):
            errors.append(f"formal cell self-hash mismatch: {cell.get('cell_id')}")
        if cell.get("participant_execution_contract_sha256") != participant_contract_hash:
            errors.append(f"formal cell participant contract mismatch: {cell.get('cell_id')}")
    split = report.get("world_split_contract")
    if not isinstance(split, Mapping):
        errors.append("formal preflight world-split contract is missing")
    else:
        public = split.get("public_formal")
        private = split.get("private_confirmation")
        development_seeds = split.get("development_and_qualification_world_seeds")
        if (
            split.get("manifest_split") != "public_formal"
            or split.get("development_public_identity_disjoint") is not True
            or split.get("public_private_namespace_disjoint") is not True
            or not isinstance(public, Mapping)
            or not isinstance(private, Mapping)
            or not isinstance(development_seeds, list)
        ):
            errors.append("formal preflight world-split contract is not fail-closed")
        else:
            public_start = public.get("namespace_start")
            public_size = public.get("namespace_size")
            private_start = private.get("namespace_start")
            private_size = private.get("namespace_size")
            ranges_valid = (
                all(
                    isinstance(value, int) and not isinstance(value, bool)
                    for value in (public_start, public_size, private_start, private_size)
                )
                and public_size > 0
                and private_size > 0
            )
            if not ranges_valid:
                errors.append("formal preflight world namespaces are invalid")
            else:
                public_end = public_start + public_size
                private_end = private_start + private_size
                if not (public_end <= private_start or private_end <= public_start):
                    errors.append("formal preflight public/private namespaces overlap")
                raw_cell_seeds = [
                    cell.get("world_seed") for cell in cells if isinstance(cell, Mapping)
                ]
                cell_seeds = {
                    seed
                    for seed in raw_cell_seeds
                    if isinstance(seed, int) and not isinstance(seed, bool)
                }
                if len(cell_seeds) != 25 or public.get("world_identity_count") != 25:
                    errors.append("formal preflight public identity denominator is invalid")
                if any(
                    not isinstance(seed, int)
                    or isinstance(seed, bool)
                    or not public_start <= seed < public_end
                    or private_start <= seed < private_end
                    or seed in development_seeds
                    for seed in raw_cell_seeds
                ):
                    errors.append("formal preflight contains a cross-split world identity")
            commitment = private.get("sealed_identity_commitment_sha256")
            if (
                private.get("identities_present_in_manifest") is not False
                or not isinstance(commitment, str)
                or len(commitment) != 64
            ):
                errors.append("formal preflight private identity boundary is invalid")
        if any(
            isinstance(cell, Mapping)
            and (
                cell.get("world_split") != "public_formal"
                or any(
                    field in cell
                    for field in (
                        "private_identity",
                        "private_world_id",
                        "private_world_seed",
                    )
                )
            )
            for cell in cells
        ):
            errors.append("formal preflight cell crossed the public/private boundary")
    prompt = report.get("prompt_boundary")
    if not isinstance(prompt, Mapping) or any(
        prompt.get(key) is not False
        for key in (
            "world_seed_exposed_to_participant",
            "world_cluster_id_exposed_to_participant",
            "prior_arm_label_exposed_to_participant",
            "private_identity_exposed_to_participant_or_manifest",
            "evaluator_truth_exposed_to_participant",
        )
    ):
        errors.append("formal preflight prompt boundary is not fail-closed")
    if report.get("formal_result") is not False:
        errors.append("a preflight cannot be a formal result")
    return errors


def validate_formal_bindings(root: Path, report: Mapping[str, Any]) -> list[str]:
    """Verify every file binding carried by a committed formal preflight."""

    root = root.resolve()
    errors = validate_formal_preflight(report)
    bindings: list[Mapping[str, Any]] = []
    for name in ("design_binding", "analysis_binding"):
        candidate = report.get(name)
        if isinstance(candidate, Mapping):
            bindings.append(candidate)
        else:
            errors.append(f"formal preflight lacks {name}")
    for name in ("task_bindings", "source_bindings"):
        rows = report.get(name)
        if not isinstance(rows, list):
            errors.append(f"formal preflight lacks {name}")
            continue
        for row in rows:
            if not isinstance(row, Mapping):
                errors.append(f"formal preflight {name} contains a malformed row")
                continue
            candidate = row.get("campaign_config") if name == "task_bindings" else row
            if isinstance(candidate, Mapping):
                bindings.append(candidate)
            else:
                errors.append(f"formal preflight {name} contains a malformed binding")
    seen: dict[str, str] = {}
    for binding in bindings:
        relative = binding.get("path")
        digest = binding.get("sha256")
        hash_kind = binding.get("hash_kind")
        if (
            not isinstance(relative, str)
            or not isinstance(digest, str)
            or hash_kind not in {"file_sha256", "canonical_json_sha256"}
        ):
            errors.append("formal preflight contains an incomplete file binding")
            continue
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            errors.append(f"formal binding escapes the repository: {relative}")
            continue
        if relative in seen and seen[relative] != digest:
            errors.append(f"formal binding has conflicting digests: {relative}")
            continue
        seen[relative] = digest
        if not path.is_file():
            errors.append(f"formal binding is missing: {relative}")
        else:
            actual = (
                file_sha256(path)
                if hash_kind == "file_sha256"
                else canonical_json_sha256(_load_object(path))
            )
            if actual != digest:
                errors.append(f"formal binding digest mismatch: {relative}")
    for cell in report.get("cells", []):
        if not isinstance(cell, Mapping):
            continue
        relative = cell.get("campaign_config_path")
        digest = cell.get("campaign_config_sha256")
        if not isinstance(relative, str) or seen.get(relative) != digest:
            errors.append(f"formal cell campaign binding mismatch: {cell.get('cell_id')}")
    return errors


__all__ = [
    "FORMAL_ARMS",
    "FORMAL_CELL_VERSION",
    "FORMAL_CHECKPOINT_EXPERIMENTS",
    "FORMAL_PREFLIGHT_VERSION",
    "FORMAL_RECEIPT_VERSION",
    "FORMAL_SNAPSHOT_STAGES",
    "FORMAL_STORE_AUDIT_VERSION",
    "FORMAL_TERMINAL_STATES",
    "DuplicateFormalCellError",
    "InvalidFormalCellReceiptError",
    "ProviderAttemptLimitError",
    "WorkIIFormalCellStore",
    "build_checkpoint_contract",
    "build_formal_preflight",
    "validate_formal_bindings",
    "validate_formal_preflight",
]
