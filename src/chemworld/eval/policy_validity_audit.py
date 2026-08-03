"""Fail-closed audit for Work I known-policy construct-validity controls.

The auditor consumes immutable campaign bundles produced by the matrix runner.
It does not execute chemical worlds and it does not trust producer-side profile
records or summary booleans.  Profiles and resource state are rebuilt from the
records and the complete campaign resource ledger before replay, retest, arm,
or construct-validity gates are evaluated.
"""

from __future__ import annotations

import json
import math
import statistics
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

from chemworld.campaign_resources import (
    CampaignResourceIntegrityError,
    CampaignResourceLedger,
)
from chemworld.data.logging import to_builtin
from chemworld.eval.known_policy_contract import (
    FORMAL_WORLD_SEEDS,
    INFORMATION_ARMS,
    LIFECYCLES_PER_CELL,
    POLICY_IDS,
    PROBE_SCHEDULE,
    build_known_policy_contract,
    known_policy_contract_sha256,
)
from chemworld.eval.policy_validity_contract import (
    AXES,
    ENDPOINT_CONTEXT,
    METRICS,
    PROFILE_SCHEMA_ID,
    PROFILE_SCHEMA_VERSION,
    profile_contract_sha256,
    validate_profile_record,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

AUDIT_SCHEMA_ID = "chemworld.known_policy_validity_audit"
AUDIT_SCHEMA_VERSION = "0.1.0"
MATRIX_SCHEMA_ID = "chemworld.known_policy_matrix"
MATRIX_SCHEMA_VERSION = "0.1.0"
CELL_SCHEMA_ID = "chemworld.known_policy_campaign_bundle"
CELL_SCHEMA_VERSION = "0.1.0"
EXECUTION_SCHEMA_ID = "chemworld.known_policy_campaign_execution"
EXECUTION_SCHEMA_VERSION = "0.1.0"

FROZEN_THRESHOLD = 0.007984561379998922
FROZEN_THRESHOLD_BINDING_SHA256 = "8a55b713ca900a644a301ecd8e83a0a686f9a28b3f60a18a85a4e57b66288c6a"
RETENTION_FRACTION = 0.9
FLOAT_TOLERANCE = 1e-12
COMPONENT_HASH_FIELDS = (
    "event_sha256",
    "state_sha256",
    "resource_sha256",
    "terminal_sha256",
    "profile_sha256",
    "endpoint_sha256",
)
_TERMINAL_KINDS = ("final_assay", "discard")
_PROCESS_EXCLUSIONS = {"measure", "terminate", "discard_batch"}


class PolicyValidityAuditError(ValueError):
    """Raised when immutable evidence cannot support the requested audit."""


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PolicyValidityAuditError(f"{label} must be an object")
    return value


def _sequence(value: Any, label: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise PolicyValidityAuditError(f"{label} must be an array")
    return value


def _nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PolicyValidityAuditError(f"{label} must be a non-empty string")
    return value


def _digest(value: Any, label: str) -> str:
    digest = _nonempty_string(value, label)
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise PolicyValidityAuditError(f"{label} must be a lowercase SHA-256 digest")
    return digest


def _integer(value: Any, label: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise PolicyValidityAuditError(
            f"{label} must be an integer greater than or equal to {minimum}"
        )
    return value


def _finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise PolicyValidityAuditError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise PolicyValidityAuditError(f"{label} must be finite")
    return result


def _close(left: Any, right: Any) -> bool:
    if left is None or right is None:
        return left is right
    if isinstance(left, bool) or isinstance(right, bool):
        return left == right
    if isinstance(left, int | float) and isinstance(right, int | float):
        return math.isclose(
            float(left),
            float(right),
            rel_tol=0.0,
            abs_tol=FLOAT_TOLERANCE,
        )
    return left == right


def _action(record: Mapping[str, Any], label: str) -> Mapping[str, Any]:
    return _mapping(record.get("action"), f"{label}.action")


def _operation(record: Mapping[str, Any], label: str) -> str:
    return _nonempty_string(_action(record, label).get("operation"), f"{label}.operation")


def _instrument(record: Mapping[str, Any], label: str) -> str | None:
    action = _action(record, label)
    if action.get("operation") != "measure":
        return None
    return _nonempty_string(action.get("instrument"), f"{label}.instrument")


def _metric(profile: Mapping[str, Any], metric_id: str) -> Any:
    for axis in AXES:
        axis_payload = _mapping(
            _mapping(profile.get("construct_axes"), "profile.construct_axes").get(axis["axis_id"]),
            f"profile.construct_axes.{axis['axis_id']}",
        )
        if metric_id in axis_payload:
            return axis_payload[metric_id]
    raise PolicyValidityAuditError(f"profile is missing metric {metric_id}")


def _ordered_records(records: Any, *, cell_id: str, execution_name: str) -> list[dict[str, Any]]:
    if records is None:
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} must contain complete immutable records"
        )
    raw_records = _sequence(records, f"{cell_id}.{execution_name}.records")
    if not raw_records:
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} must contain complete immutable records"
        )
    result: list[dict[str, Any]] = []
    lifecycle_rows: dict[int, list[dict[str, Any]]] = {
        index: [] for index in range(LIFECYCLES_PER_CELL)
    }
    for ordinal, raw_record in enumerate(raw_records, start=1):
        label = f"{cell_id}.{execution_name}.records[{ordinal - 1}]"
        record = dict(_mapping(raw_record, label))
        if (
            _integer(
                record.get("operation_attempt_index"), f"{label}.operation_attempt_index", minimum=1
            )
            != ordinal
        ):
            raise PolicyValidityAuditError(
                f"{label}.operation_attempt_index must equal immutable record ordinal"
            )
        lifecycle_index = _integer(record.get("lifecycle_index"), f"{label}.lifecycle_index")
        if lifecycle_index not in lifecycle_rows:
            raise PolicyValidityAuditError(f"{label}.lifecycle_index is outside 0..5")
        if record.get("transaction_status") != "committed":
            raise PolicyValidityAuditError(f"{label} is not a committed transaction")
        action = _action(record, label)
        _operation(record, label)

        state = _mapping(record.get("state"), f"{label}.state")
        if _digest(record.get("state_sha256"), f"{label}.state_sha256") != canonical_json_sha256(
            state
        ):
            raise PolicyValidityAuditError(f"{label}.state_sha256 does not bind state")
        observation = _mapping(record.get("observation"), f"{label}.observation")
        if _digest(
            record.get("observation_sha256"), f"{label}.observation_sha256"
        ) != canonical_json_sha256(observation):
            raise PolicyValidityAuditError(f"{label}.observation_sha256 does not bind observation")
        resource_state = _mapping(
            record.get("campaign_resource_state"),
            f"{label}.campaign_resource_state",
        )
        if _digest(
            record.get("campaign_resource_state_sha256"),
            f"{label}.campaign_resource_state_sha256",
        ) != canonical_json_sha256(resource_state):
            raise PolicyValidityAuditError(
                f"{label}.campaign_resource_state_sha256 does not bind resource state"
            )

        terminal_kind = record.get("terminal_kind")
        if terminal_kind not in (None, *_TERMINAL_KINDS):
            raise PolicyValidityAuditError(f"{label}.terminal_kind is invalid")
        operation = str(action["operation"])
        instrument = action.get("instrument")
        expected_terminal = (
            "final_assay"
            if operation == "measure" and instrument == "final_assay"
            else "discard"
            if operation == "discard_batch"
            else None
        )
        if terminal_kind != expected_terminal:
            raise PolicyValidityAuditError(
                f"{label}.terminal_kind disagrees with the committed action"
            )
        terminal_score = record.get("terminal_score")
        if terminal_kind == "final_assay":
            _finite(terminal_score, f"{label}.terminal_score")
        elif terminal_score is not None:
            raise PolicyValidityAuditError(
                f"{label}.terminal_score must be null outside final assay"
            )
        decision = _mapping(record.get("decision_audit"), f"{label}.decision_audit")
        if decision.get("action_sha256") != canonical_json_sha256(action):
            raise PolicyValidityAuditError(
                f"{label}.decision_audit.action_sha256 does not bind action"
            )
        if decision.get("material_information_accessed") is not False:
            raise PolicyValidityAuditError(
                f"{label}.decision_audit reports material-information access"
            )
        if decision.get("provider_call_count") != 0:
            raise PolicyValidityAuditError(
                f"{label}.decision_audit must report zero provider calls"
            )
        lifecycle_rows[lifecycle_index].append(record)
        result.append(record)

    for lifecycle_index, rows in lifecycle_rows.items():
        if not rows:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} lacks lifecycle {lifecycle_index}"
            )
        terminals = [row for row in rows if row.get("terminal_kind") is not None]
        if len(terminals) != 1 or terminals[0] is not rows[-1]:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name}.lifecycle-{lifecycle_index} "
                "must end in exactly one terminal action"
            )
    lifecycle_sequence = [int(record["lifecycle_index"]) for record in result]
    expected_sequence = [
        lifecycle_index
        for lifecycle_index in range(LIFECYCLES_PER_CELL)
        for _ in lifecycle_rows[lifecycle_index]
    ]
    if lifecycle_sequence != expected_sequence:
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} lifecycle records must be contiguous and ordered"
        )
    return result


def _validate_decision_boundaries(
    records: Sequence[Mapping[str, Any]], *, policy_id: str, cell_id: str
) -> None:
    by_lifecycle: dict[int, list[Mapping[str, Any]]] = {
        index: [] for index in range(LIFECYCLES_PER_CELL)
    }
    for record in records:
        by_lifecycle[int(record["lifecycle_index"])].append(record)
    for lifecycle_index, rows in by_lifecycle.items():
        seen_signal: float | None = None
        for within_index, record in enumerate(rows):
            label = f"{cell_id}.lifecycle-{lifecycle_index}.decision-{within_index}"
            decision = _mapping(record["decision_audit"], f"{label}.decision_audit")
            if decision.get("policy_id") != policy_id:
                raise PolicyValidityAuditError(f"{label} policy identity mismatch")
            operation = _operation(record, label)
            instrument = _instrument(record, label)
            if policy_id != "measure_then_threshold":
                if decision.get("adaptation_source") != "none":
                    raise PolicyValidityAuditError(
                        f"{label} unmeasured policy adaptation_source must be none"
                    )
                if decision.get("observed_signal_access") is not False:
                    raise PolicyValidityAuditError(
                        f"{label} unmeasured policy may not access a diagnostic signal"
                    )
                if decision.get("diagnostic_signal") is not None:
                    raise PolicyValidityAuditError(
                        f"{label} unmeasured policy diagnostic_signal must be null"
                    )
                continue
            if operation == "measure" and instrument == "uvvis":
                observation = _mapping(record["observation"], f"{label}.observation")
                seen_signal = _finite(
                    observation.get("conversion"), f"{label}.observation.conversion"
                )
            is_diagnostic_measurement = operation == "measure" and instrument == "uvvis"
            expected_adaptation = (
                "measurement"
                if seen_signal is not None and not is_diagnostic_measurement
                else "none"
            )
            expected_access = expected_adaptation == "measurement"
            if decision.get("adaptation_source") != expected_adaptation:
                raise PolicyValidityAuditError(
                    f"{label} adaptation_source violates the observation boundary"
                )
            if decision.get("observed_signal_access") is not expected_access:
                raise PolicyValidityAuditError(
                    f"{label} observed_signal_access violates the observation boundary"
                )
            diagnostic = decision.get("diagnostic_signal")
            if expected_access:
                if not _close(_finite(diagnostic, f"{label}.diagnostic_signal"), seen_signal):
                    raise PolicyValidityAuditError(
                        f"{label} diagnostic_signal disagrees with the public measurement"
                    )
            elif diagnostic is not None:
                raise PolicyValidityAuditError(
                    f"{label} diagnostic_signal must be null before measurement"
                )


def _expected_actions(
    policy_id: str, lifecycle_index: int, terminal_kind: str
) -> list[dict[str, Any]]:
    probe = PROBE_SCHEDULE[lifecycle_index]
    prefix = [
        {"operation": "add_solvent", "volume_L": 0.025, "solvent": probe.solvent},
        {"operation": "add_reagent", "amount_mol": probe.reagent_amount_mol},
        {
            "operation": "set_potential",
            "potential_V": probe.potential_V,
            "current_mA": probe.current_mA,
            "electrolyte_profile": probe.electrolyte_profile,
        },
        {"operation": "electrolyze", "duration_s": probe.probe_duration_s},
    ]
    if policy_id == "assay_all":
        return [
            *prefix,
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
    if policy_id == "start_then_discard":
        return [
            {"operation": "add_solvent", "volume_L": 0.025, "solvent": probe.solvent},
            {
                "operation": "discard_batch",
                "reason": "known_policy_immediate_discard",
            },
        ]
    if terminal_kind == "discard":
        return [
            *prefix,
            {"operation": "measure", "instrument": "uvvis"},
            {
                "operation": "discard_batch",
                "reason": "known_policy_below_threshold",
            },
        ]
    return [
        *prefix,
        {"operation": "measure", "instrument": "uvvis"},
        {"operation": "electrolyze", "duration_s": probe.post_measure_duration_s},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]


def _validate_policy_actions(
    records: Sequence[Mapping[str, Any]], *, policy_id: str, cell_id: str
) -> None:
    by_lifecycle: dict[int, list[Mapping[str, Any]]] = {
        index: [] for index in range(LIFECYCLES_PER_CELL)
    }
    for record in records:
        by_lifecycle[int(record["lifecycle_index"])].append(record)
    for lifecycle_index, rows in by_lifecycle.items():
        terminal_kind = str(rows[-1]["terminal_kind"])
        actions = [to_builtin(_action(row, cell_id)) for row in rows]
        expected = _expected_actions(policy_id, lifecycle_index, terminal_kind)
        if actions != expected:
            raise PolicyValidityAuditError(
                f"{cell_id}.lifecycle-{lifecycle_index} actions violate the "
                f"frozen {policy_id} grammar"
            )
        if policy_id == "measure_then_threshold":
            measurement = rows[4]
            signal = _finite(
                _mapping(measurement["observation"], "threshold observation").get("conversion"),
                "threshold observation.conversion",
            )
            expected_terminal = "final_assay" if signal >= FROZEN_THRESHOLD else "discard"
            if terminal_kind != expected_terminal:
                raise PolicyValidityAuditError(
                    f"{cell_id}.lifecycle-{lifecycle_index} terminal action "
                    "disagrees with the frozen threshold"
                )


def _trajectory_metrics(scores: Sequence[float]) -> dict[str, float | None]:
    if not scores:
        return {
            "global_best_discovery_fraction": None,
            "online_incumbent_retention_rate": None,
            "maximum_absolute_incumbent_drawdown": None,
            "loss_episode_recovery_rate": None,
            "terminal_to_global_best_ratio": None,
        }
    best = max(scores)
    best_index = next(
        index for index, score in enumerate(scores) if abs(score - best) <= FLOAT_TOLERANCE
    )
    discovery = best_index / (len(scores) - 1) if len(scores) > 1 else 0.0
    if len(scores) < 2:
        return {
            "global_best_discovery_fraction": discovery,
            "online_incumbent_retention_rate": None,
            "maximum_absolute_incumbent_drawdown": None,
            "loss_episode_recovery_rate": None,
            "terminal_to_global_best_ratio": scores[-1] / best if best > 0.0 else None,
        }

    incumbent = scores[0]
    retained_count = 0
    drawdowns: list[float] = []
    loss_episodes = 0
    recovered = 0
    recovery_threshold: float | None = None
    for score in scores[1:]:
        threshold = RETENTION_FRACTION * incumbent
        retained = score + FLOAT_TOLERANCE >= threshold
        retained_count += int(retained)
        drawdowns.append(max(0.0, incumbent - score))
        if recovery_threshold is not None:
            if score + FLOAT_TOLERANCE >= recovery_threshold:
                recovered += 1
                recovery_threshold = None
        elif not retained:
            loss_episodes += 1
            recovery_threshold = threshold
        if score > incumbent + FLOAT_TOLERANCE:
            incumbent = score
    return {
        "global_best_discovery_fraction": discovery,
        "online_incumbent_retention_rate": retained_count / (len(scores) - 1),
        "maximum_absolute_incumbent_drawdown": max(drawdowns),
        "loss_episode_recovery_rate": (recovered / loss_episodes if loss_episodes else None),
        "terminal_to_global_best_ratio": scores[-1] / best if best > 0.0 else None,
    }


def _resource_rebuild(
    snapshot_payload: Any,
    records: Sequence[Mapping[str, Any]],
    *,
    cell_id: str,
    execution_name: str,
) -> dict[str, Any]:
    snapshot = dict(
        _mapping(
            snapshot_payload,
            f"{cell_id}.{execution_name}.campaign_resource_ledger_snapshot",
        )
    )
    try:
        ledger = CampaignResourceLedger.from_snapshot(snapshot)
    except (CampaignResourceIntegrityError, KeyError, TypeError, ValueError) as exc:
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} resource ledger replay failed: {exc}"
        ) from exc
    rebuilt = ledger.snapshot()
    events = _sequence(snapshot.get("events"), f"{cell_id}.{execution_name}.ledger.events")
    if len(events) != len(records):
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} resource ledger/record count mismatch"
        )
    for index, (raw_event, record) in enumerate(zip(events, records, strict=True), start=1):
        event = _mapping(raw_event, f"{cell_id}.{execution_name}.ledger.events[{index - 1}]")
        if to_builtin(event.get("action")) != to_builtin(record.get("action")):
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} resource event {index} action mismatch"
            )
        outcome = _mapping(
            event.get("outcome"),
            f"{cell_id}.{execution_name}.ledger.events[{index - 1}].outcome",
        )
        if outcome.get("committed") is not True:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} resource event {index} is not committed"
            )
        expected_start = (int(record["lifecycle_index"]) == 0 and index == 1) or (
            index > 1
            and int(records[index - 2]["lifecycle_index"]) != int(record["lifecycle_index"])
        )
        if event.get("starts_vessel") is not expected_start:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} resource event {index} vessel-start mismatch"
            )
        partial_without_hash = {
            "schema_version": snapshot["schema_version"],
            "card": snapshot["card"],
            "state": record["campaign_resource_state"],
            "events": list(events[:index]),
            "last_event_id": event.get("event_id"),
        }
        partial = {
            **partial_without_hash,
            "ledger_sha256": canonical_json_sha256(partial_without_hash),
        }
        try:
            partial_ledger = CampaignResourceLedger.from_snapshot(partial)
        except (CampaignResourceIntegrityError, KeyError, TypeError, ValueError) as exc:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} resource state at event {index} "
                f"is not replayable: {exc}"
            ) from exc
        if partial_ledger.snapshot()["state"] != record["campaign_resource_state"]:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} resource state at event {index} changed during replay"
            )
    if records[-1]["campaign_resource_state"] != rebuilt["state"]:
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} terminal resource state mismatch"
        )
    state = cast(Mapping[str, Any], rebuilt["state"])
    return {
        "verified": True,
        "ledger_sha256": rebuilt["ledger_sha256"],
        "card_sha256": ledger.card.card_sha256,
        "state": to_builtin(state),
    }


def _profile_identity(
    identity: Mapping[str, Any], trajectory_manifest_sha256: str
) -> dict[str, str]:
    fields = (
        "campaign_id",
        "world_id",
        "information_arm",
        "policy_id",
        "resource_card_sha256",
    )
    result = {field: _nonempty_string(identity.get(field), f"identity.{field}") for field in fields}
    result["trajectory_manifest_sha256"] = trajectory_manifest_sha256
    return result


def _base_component_hashes(
    records: Sequence[Mapping[str, Any]], resource_sha256: str
) -> dict[str, str]:
    terminal_rows = [
        {
            "lifecycle_index": record["lifecycle_index"],
            "terminal_kind": record["terminal_kind"],
            "action": record["action"],
        }
        for record in records
        if record.get("terminal_kind") is not None
    ]
    endpoint_rows = [
        {
            "lifecycle_index": record["lifecycle_index"],
            "score": record["terminal_score"],
        }
        for record in records
        if record.get("terminal_kind") == "final_assay"
    ]
    return {
        "event_sha256": canonical_json_sha256(list(records)),
        "state_sha256": canonical_json_sha256([record["state_sha256"] for record in records]),
        "resource_sha256": resource_sha256,
        "terminal_sha256": canonical_json_sha256(terminal_rows),
        "endpoint_sha256": canonical_json_sha256(endpoint_rows),
    }


def _trajectory_manifest_sha256(base_hashes: Mapping[str, str]) -> str:
    return canonical_json_sha256(
        {field: base_hashes[field] for field in COMPONENT_HASH_FIELDS if field != "profile_sha256"}
    )


def build_campaign_profile(
    records: Sequence[Mapping[str, Any]],
    resource_state: Mapping[str, Any],
    identity: Mapping[str, Any],
    *,
    trajectory_manifest_sha256: str,
    provider_call_count: int = 0,
) -> dict[str, Any]:
    """Independently rebuild the frozen V01 profile from immutable evidence."""

    lifecycle_rows: dict[int, list[Mapping[str, Any]]] = {
        index: [] for index in range(LIFECYCLES_PER_CELL)
    }
    for record in records:
        lifecycle_rows[int(record["lifecycle_index"])].append(record)
    terminals = [record for record in records if record.get("terminal_kind") is not None]
    assays = [record for record in terminals if record["terminal_kind"] == "final_assay"]
    discards = [record for record in terminals if record["terminal_kind"] == "discard"]
    measured = 0
    nonfinal_uses = 0
    first_measurement_fractions: list[float] = []
    continued = 0
    post_measure_operations = 0
    eligible = 0
    concordant = 0
    for lifecycle_index in range(LIFECYCLES_PER_CELL):
        rows = lifecycle_rows[lifecycle_index]
        measurement_indices = [
            index
            for index, row in enumerate(rows)
            if _operation(row, "profile record") == "measure"
            and _instrument(row, "profile record") != "final_assay"
        ]
        if measurement_indices:
            measured += 1
            nonfinal_uses += len(measurement_indices)
            first_index = measurement_indices[0]
            first_measurement_fractions.append(first_index / len(rows))
            later_process = sum(
                _operation(row, "profile record") not in _PROCESS_EXCLUSIONS
                for row in rows[first_index + 1 : -1]
            )
            post_measure_operations += later_process
            continued += int(later_process > 0)
        diagnostics = [
            row
            for row in rows
            if _operation(row, "profile record") == "measure"
            and _instrument(row, "profile record") == "uvvis"
        ]
        if diagnostics:
            if len(diagnostics) != 1:
                raise PolicyValidityAuditError(
                    f"identity.campaign_id={identity.get('campaign_id')} lifecycle "
                    f"{lifecycle_index} has multiple threshold diagnostics"
                )
            signal = _finite(
                _mapping(diagnostics[0]["observation"], "diagnostic observation").get("conversion"),
                "diagnostic observation.conversion",
            )
            eligible += 1
            expected = "final_assay" if signal >= FROZEN_THRESHOLD else "discard"
            concordant += int(rows[-1]["terminal_kind"] == expected)

    closed = len(terminals)
    final_count = len(assays)
    discard_count = len(discards)
    scores = [float(record["terminal_score"]) for record in assays]
    report_only = _mapping(resource_state.get("report_only"), "resource_state.report_only")
    trajectory = _trajectory_metrics(scores)
    axes: dict[str, dict[str, Any]] = {axis["axis_id"]: {} for axis in AXES}
    axes["terminal_commitment"] = {
        "closed_lifecycle_fraction": closed / LIFECYCLES_PER_CELL,
        "assay_fraction": final_count / closed if closed else None,
        "discard_fraction": discard_count / closed if closed else None,
    }
    axes["evidence_acquisition"] = {
        "measured_lifecycle_fraction": measured / closed if closed else None,
        "nonfinal_instrument_uses_per_closed_lifecycle": (
            nonfinal_uses / closed if closed else None
        ),
        "mean_first_measurement_operation_fraction": (
            statistics.fmean(first_measurement_fractions) if first_measurement_fractions else None
        ),
    }
    axes["evidence_conditioned_action"] = {
        "continued_after_measurement_fraction": continued / closed if closed else None,
        "post_measure_process_operations_per_closed_lifecycle": (
            post_measure_operations / closed if closed else None
        ),
        "threshold_eligible_fraction": eligible / closed if closed else None,
        "threshold_decision_concordance": concordant / eligible if eligible else None,
    }
    axes["resource_deployment"] = {
        "attempted_operations_per_closed_lifecycle": (
            int(resource_state["operation_attempts"]) / closed if closed else None
        ),
        "committed_operations_per_closed_lifecycle": (len(records) / closed if closed else None),
        "total_cost_per_closed_lifecycle": (
            _finite(report_only.get("physical_cost"), "report_only.physical_cost") / closed
            if closed
            else None
        ),
        "total_risk_per_closed_lifecycle": (
            _finite(
                report_only.get("accumulated_risk"),
                "report_only.accumulated_risk",
            )
            / closed
            if closed
            else None
        ),
    }
    axes["outcome_trajectory"] = trajectory
    profile = {
        "schema_id": PROFILE_SCHEMA_ID,
        "schema_version": PROFILE_SCHEMA_VERSION,
        "contract_sha256": profile_contract_sha256(),
        "identity": _profile_identity(identity, trajectory_manifest_sha256),
        "counts": {
            "planned_lifecycle_count": LIFECYCLES_PER_CELL,
            "closed_lifecycle_count": closed,
            "final_assay_count": final_count,
            "discard_count": discard_count,
            "measured_lifecycle_count": measured,
            "threshold_eligible_lifecycle_count": eligible,
        },
        "construct_axes": axes,
        "endpoint_context": {
            "mean_assayed_score": statistics.fmean(scores) if scores else None,
            "best_assayed_score": max(scores) if scores else None,
        },
        "reliability": {
            "trajectory_exact_replay_match": True,
            "profile_exact_rebuild_match": True,
            "provider_call_count": provider_call_count,
        },
    }
    errors = validate_profile_record(profile)
    if errors:
        raise PolicyValidityAuditError(
            "rebuilt profile violates the frozen V01 contract: " + "; ".join(errors)
        )
    expected_metric_ids = {metric.metric_id for metric in METRICS}
    actual_metric_ids = {metric_id for axis in axes.values() for metric_id in axis}
    if actual_metric_ids != expected_metric_ids:
        raise PolicyValidityAuditError("rebuilt profile metric surface is incomplete")
    if set(profile["endpoint_context"]) != {metric.metric_id for metric in ENDPOINT_CONTEXT}:
        raise PolicyValidityAuditError("rebuilt endpoint-context surface is incomplete")
    return profile


def build_execution_hashes(
    records: Sequence[Mapping[str, Any]],
    resource_snapshot: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> dict[str, str]:
    """Return the six component hashes used by replay and retest gates."""

    base = _base_component_hashes(
        records, _digest(resource_snapshot.get("ledger_sha256"), "resource ledger hash")
    )
    return {
        **base,
        "profile_sha256": canonical_json_sha256(profile),
    }


def _validate_controller_manifest(payload: Any, *, policy_id: str, cell_id: str) -> dict[str, Any]:
    manifest = dict(_mapping(payload, f"{cell_id}.controller_manifest"))
    _nonempty_string(manifest.get("schema_id"), f"{cell_id}.controller.schema_id")
    _nonempty_string(manifest.get("schema_version"), f"{cell_id}.controller.schema_version")
    if manifest.get("policy_id") != policy_id:
        raise PolicyValidityAuditError(f"{cell_id} controller policy_id mismatch")
    bindings = _mapping(
        manifest.get("artifact_bindings"), f"{cell_id}.controller.artifact_bindings"
    )
    if bindings.get("known_policy_contract_sha256") != known_policy_contract_sha256():
        raise PolicyValidityAuditError(
            f"{cell_id} controller known-policy contract binding is stale"
        )
    if manifest.get("reads_material_information") is not False:
        raise PolicyValidityAuditError(f"{cell_id} controller must not read material information")
    if manifest.get("provider_call_count") != 0:
        raise PolicyValidityAuditError(f"{cell_id} controller must make zero provider calls")
    _digest(manifest.get("controller_sha256"), f"{cell_id}.controller_sha256")
    threshold_binding = bindings.get("threshold_binding_sha256")
    if policy_id == "measure_then_threshold":
        if threshold_binding != FROZEN_THRESHOLD_BINDING_SHA256:
            raise PolicyValidityAuditError(f"{cell_id} threshold controller binding is stale")
        if not _close(bindings.get("threshold"), FROZEN_THRESHOLD):
            raise PolicyValidityAuditError(f"{cell_id} threshold value is not frozen V03")
        if bindings.get("diagnostic_signal") != "observation.conversion":
            raise PolicyValidityAuditError(
                f"{cell_id} threshold diagnostic signal is not frozen V03"
            )
        if bindings.get("comparator") != ">=":
            raise PolicyValidityAuditError(f"{cell_id} threshold comparator is not frozen V03")
    elif threshold_binding not in (None, FROZEN_THRESHOLD_BINDING_SHA256):
        raise PolicyValidityAuditError(
            f"{cell_id} unmeasured controller has an unknown threshold binding"
        )
    return manifest


def _validate_cell_identity(payload: Any, *, cell_id: str) -> dict[str, Any]:
    identity = dict(_mapping(payload, f"{cell_id}.identity"))
    for field in (
        "campaign_id",
        "world_id",
        "information_arm",
        "policy_id",
        "resource_card_sha256",
        "physical_identity_sha256",
        "noise_identity_sha256",
        "material_information_sha256",
    ):
        _nonempty_string(identity.get(field), f"{cell_id}.identity.{field}")
    _integer(identity.get("world_seed"), f"{cell_id}.identity.world_seed")
    if identity["information_arm"] not in INFORMATION_ARMS:
        raise PolicyValidityAuditError(f"{cell_id} has an unknown information arm")
    if identity["policy_id"] not in POLICY_IDS:
        raise PolicyValidityAuditError(f"{cell_id} has an unknown policy")
    for field in (
        "resource_card_sha256",
        "physical_identity_sha256",
        "noise_identity_sha256",
        "material_information_sha256",
    ):
        _digest(identity[field], f"{cell_id}.identity.{field}")
    return identity


def _audit_execution(
    payload: Any,
    *,
    identity: Mapping[str, Any],
    controller_manifest: Mapping[str, Any],
    cell_id: str,
    execution_name: str,
) -> dict[str, Any]:
    execution = _mapping(payload, f"{cell_id}.{execution_name}")
    if execution.get("schema_id") != EXECUTION_SCHEMA_ID:
        raise PolicyValidityAuditError(f"{cell_id}.{execution_name} schema_id mismatch")
    if execution.get("schema_version") != EXECUTION_SCHEMA_VERSION:
        raise PolicyValidityAuditError(f"{cell_id}.{execution_name} schema_version mismatch")
    provider_calls = _integer(
        execution.get("provider_call_count"),
        f"{cell_id}.{execution_name}.provider_call_count",
    )
    if provider_calls != 0:
        raise PolicyValidityAuditError(f"{cell_id}.{execution_name} must make zero provider calls")
    records = _ordered_records(
        execution.get("records"), cell_id=cell_id, execution_name=execution_name
    )
    policy_id = str(identity["policy_id"])
    _validate_decision_boundaries(records, policy_id=policy_id, cell_id=cell_id)
    _validate_policy_actions(records, policy_id=policy_id, cell_id=cell_id)
    for record in records:
        decision = cast(Mapping[str, Any], record["decision_audit"])
        if decision.get("controller_identity_sha256") != controller_manifest.get(
            "controller_sha256"
        ):
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} decision/controller identity mismatch"
            )
        if decision.get("known_policy_contract_sha256") != known_policy_contract_sha256():
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} decision contract binding is stale"
            )
        if (
            policy_id == "measure_then_threshold"
            and decision.get("threshold_binding_sha256") != FROZEN_THRESHOLD_BINDING_SHA256
        ):
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} decision threshold binding is stale"
            )

    resource = _resource_rebuild(
        execution.get("campaign_resource_ledger_snapshot"),
        records,
        cell_id=cell_id,
        execution_name=execution_name,
    )
    if resource["card_sha256"] != identity["resource_card_sha256"]:
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} resource card identity mismatch"
        )
    resource_state = cast(Mapping[str, Any], resource["state"])
    terminal_counts = {
        "final_assay": sum(record.get("terminal_kind") == "final_assay" for record in records),
        "discard": sum(record.get("terminal_kind") == "discard" for record in records),
    }
    expected_state = {
        "operation_attempts": len(records),
        "vessel_starts": LIFECYCLES_PER_CELL,
        "final_assays": terminal_counts["final_assay"],
        "discarded_batches": terminal_counts["discard"],
        "nonfinal_instrument_uses": sum(
            _operation(record, "resource count") == "measure"
            and _instrument(record, "resource count") != "final_assay"
            for record in records
        ),
    }
    for field, expected in expected_state.items():
        if resource_state.get(field) != expected:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name} resource state {field} does not reconcile"
            )

    base_hashes = _base_component_hashes(records, str(resource["ledger_sha256"]))
    trajectory_hash = _trajectory_manifest_sha256(base_hashes)
    profile = build_campaign_profile(
        records,
        resource_state,
        identity,
        trajectory_manifest_sha256=trajectory_hash,
        provider_call_count=provider_calls,
    )
    producer_profile = _mapping(
        execution.get("profile_record"), f"{cell_id}.{execution_name}.profile_record"
    )
    if to_builtin(producer_profile) != to_builtin(profile):
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} producer profile differs from independent rebuild"
        )
    computed_hashes = build_execution_hashes(
        records, cast(Mapping[str, Any], execution["campaign_resource_ledger_snapshot"]), profile
    )
    supplied_hashes = _mapping(execution.get("hashes"), f"{cell_id}.{execution_name}.hashes")
    if set(supplied_hashes) != set(COMPONENT_HASH_FIELDS):
        raise PolicyValidityAuditError(
            f"{cell_id}.{execution_name} component hash surface is incomplete"
        )
    for field in COMPONENT_HASH_FIELDS:
        supplied = _digest(supplied_hashes.get(field), f"{cell_id}.{execution_name}.hashes.{field}")
        if supplied != computed_hashes[field]:
            raise PolicyValidityAuditError(
                f"{cell_id}.{execution_name}.{field} does not match the immutable evidence"
            )
    return {
        "hashes": computed_hashes,
        "trajectory_manifest_sha256": trajectory_hash,
        "profile": profile,
        "resource": resource,
        "action_trace_sha256": canonical_json_sha256([record["action"] for record in records]),
        "diagnostic_vector": [
            _mapping(record["observation"], "diagnostic observation")["conversion"]
            for record in records
            if _operation(record, "diagnostic vector") == "measure"
            and _instrument(record, "diagnostic vector") == "uvvis"
        ],
        "terminal_vector": [
            record["terminal_kind"] for record in records if record.get("terminal_kind") is not None
        ],
    }


def audit_campaign_bundle(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Audit one original/retest campaign bundle and return rebuilt evidence."""

    if payload.get("schema_id") != CELL_SCHEMA_ID:
        raise PolicyValidityAuditError("campaign bundle schema_id mismatch")
    if payload.get("schema_version") != CELL_SCHEMA_VERSION:
        raise PolicyValidityAuditError("campaign bundle schema_version mismatch")
    cell_id = _nonempty_string(payload.get("cell_id"), "campaign bundle cell_id")
    identity = _validate_cell_identity(payload.get("identity"), cell_id=cell_id)
    if cell_id != identity["campaign_id"]:
        raise PolicyValidityAuditError("campaign bundle cell_id/campaign_id mismatch")
    controller = _validate_controller_manifest(
        payload.get("controller_manifest"),
        policy_id=str(identity["policy_id"]),
        cell_id=cell_id,
    )
    original = _audit_execution(
        payload.get("original"),
        identity=identity,
        controller_manifest=controller,
        cell_id=cell_id,
        execution_name="original",
    )
    retest = _audit_execution(
        payload.get("retest"),
        identity=identity,
        controller_manifest=controller,
        cell_id=cell_id,
        execution_name="retest",
    )
    exact = {
        field: original["hashes"][field] == retest["hashes"][field]
        for field in COMPONENT_HASH_FIELDS
    }
    exact["trajectory_manifest_sha256"] = (
        original["trajectory_manifest_sha256"] == retest["trajectory_manifest_sha256"]
    )
    if not all(exact.values()):
        failed = [field for field, passed in exact.items() if not passed]
        raise PolicyValidityAuditError(
            f"{cell_id} same-identity retest mismatch: {', '.join(failed)}"
        )
    test_retest = {
        "same_controller": original["action_trace_sha256"] == retest["action_trace_sha256"],
        "same_trajectory_identity": original["trajectory_manifest_sha256"]
        == retest["trajectory_manifest_sha256"],
        "same_profile": original["profile"] == retest["profile"],
        "all_component_hashes": all(exact.values()),
    }
    return {
        "cell_id": cell_id,
        "identity": identity,
        "controller_sha256": controller["controller_sha256"],
        "profile": original["profile"],
        "resource": original["resource"],
        "hashes": original["hashes"],
        "trajectory_manifest_sha256": original["trajectory_manifest_sha256"],
        "action_trace_sha256": original["action_trace_sha256"],
        "diagnostic_vector": original["diagnostic_vector"],
        "terminal_vector": original["terminal_vector"],
        "exact_replay": exact,
        "test_retest": test_retest,
    }


def _arm_invariance(cells: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_key: dict[tuple[int, str], dict[str, Mapping[str, Any]]] = {}
    for cell in cells:
        identity = cast(Mapping[str, Any], cell["identity"])
        key = (int(identity["world_seed"]), str(identity["policy_id"]))
        by_key.setdefault(key, {})[str(identity["information_arm"])] = cell
    expected_keys = {(seed, policy_id) for seed in FORMAL_WORLD_SEEDS for policy_id in POLICY_IDS}
    if set(by_key) != expected_keys:
        raise PolicyValidityAuditError("arm-invariance groups do not cover the frozen matrix")
    groups: dict[str, Any] = {}
    for (seed, policy_id), arms in sorted(by_key.items()):
        if set(arms) != set(INFORMATION_ARMS):
            raise PolicyValidityAuditError(
                f"world {seed} policy {policy_id} lacks a matched information arm"
            )
        left = arms[INFORMATION_ARMS[0]]
        right = arms[INFORMATION_ARMS[1]]
        left_identity = cast(Mapping[str, Any], left["identity"])
        right_identity = cast(Mapping[str, Any], right["identity"])
        identity_fields = (
            "world_seed",
            "world_id",
            "policy_id",
            "resource_card_sha256",
            "physical_identity_sha256",
            "noise_identity_sha256",
        )
        checks = {
            "paired_identity": all(
                left_identity[field] == right_identity[field] for field in identity_fields
            ),
            "distinct_material_dossier": (
                left_identity["material_information_sha256"]
                != right_identity["material_information_sha256"]
            ),
            "action_trace": left["action_trace_sha256"] == right["action_trace_sha256"],
            "diagnostic_vector": left["diagnostic_vector"] == right["diagnostic_vector"],
            "terminal_vector": left["terminal_vector"] == right["terminal_vector"],
            "counts": left["profile"]["counts"] == right["profile"]["counts"],
            "construct_axes": left["profile"]["construct_axes"]
            == right["profile"]["construct_axes"],
            "endpoint_context": left["profile"]["endpoint_context"]
            == right["profile"]["endpoint_context"],
            "state_hash": left["hashes"]["state_sha256"] == right["hashes"]["state_sha256"],
            "resource_state": left["resource"]["state"] == right["resource"]["state"],
            "terminal_hash": left["hashes"]["terminal_sha256"]
            == right["hashes"]["terminal_sha256"],
            "endpoint_hash": left["hashes"]["endpoint_sha256"]
            == right["hashes"]["endpoint_sha256"],
        }
        if not all(checks.values()):
            failed = [name for name, passed in checks.items() if not passed]
            raise PolicyValidityAuditError(
                f"world {seed} policy {policy_id} matched-arm mismatch: {', '.join(failed)}"
            )
        groups[f"world-{seed}:{policy_id}"] = checks
    return {"passed": True, "groups": groups}


def _policy_cells(cells: Sequence[Mapping[str, Any]], policy_id: str) -> list[Mapping[str, Any]]:
    return [
        cell
        for cell in cells
        if cast(Mapping[str, Any], cell["identity"])["policy_id"] == policy_id
    ]


def _exact_signature_checks(cells: Sequence[Mapping[str, Any]]) -> dict[str, bool]:
    exact = build_known_policy_contract()["expected_profile_signatures"]["exact_by_policy"]
    checks: dict[str, bool] = {}
    for policy_id in POLICY_IDS:
        policy_cells = _policy_cells(cells, policy_id)
        for metric_id, expected in exact[policy_id].items():
            checks[f"{policy_id}:{metric_id}"] = all(
                _close(_metric(cast(Mapping[str, Any], cell["profile"]), metric_id), expected)
                for cell in policy_cells
            )
    threshold_cells = _policy_cells(cells, "measure_then_threshold")
    for cell in threshold_cells:
        profile = cast(Mapping[str, Any], cell["profile"])
        p = float(_metric(profile, "assay_fraction"))
        cell_id = str(cell["cell_id"])
        algebra = {
            "assay_fraction": p,
            "discard_fraction": 1.0 - p,
            "continued_after_measurement_fraction": p,
            "post_measure_process_operations_per_closed_lifecycle": p,
            "mean_first_measurement_operation_fraction": 2.0 / 3.0 - p / 6.0,
            "attempted_operations_per_closed_lifecycle": 6.0 + 2.0 * p,
            "committed_operations_per_closed_lifecycle": 6.0 + 2.0 * p,
        }
        for metric_id, expected in algebra.items():
            checks[f"{cell_id}:algebra:{metric_id}"] = _close(_metric(profile, metric_id), expected)
    return checks


def _conditional_null_checks(cells: Sequence[Mapping[str, Any]]) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    trajectory_ids = [
        metric.metric_id for metric in METRICS if metric.axis_id == "outcome_trajectory"
    ]
    for cell in cells:
        profile = cast(Mapping[str, Any], cell["profile"])
        policy_id = str(cast(Mapping[str, Any], cell["identity"])["policy_id"])
        cell_id = str(cell["cell_id"])
        measured = int(cast(Mapping[str, Any], profile["counts"])["measured_lifecycle_count"])
        checks[f"{cell_id}:first-measurement-null"] = (
            _metric(profile, "mean_first_measurement_operation_fraction") is None
        ) == (measured == 0)
        if policy_id == "start_then_discard":
            checks[f"{cell_id}:discard-endpoint-null"] = all(
                value is None
                for value in cast(Mapping[str, Any], profile["endpoint_context"]).values()
            )
            checks[f"{cell_id}:discard-trajectory-null"] = all(
                _metric(profile, metric_id) is None for metric_id in trajectory_ids
            )
        if policy_id == "assay_all":
            checks[f"{cell_id}:assay-endpoint-finite"] = all(
                isinstance(value, int | float)
                and not isinstance(value, bool)
                and math.isfinite(float(value))
                for value in cast(Mapping[str, Any], profile["endpoint_context"]).values()
            )
    return checks


def _policy_summary(cells: Sequence[Mapping[str, Any]], policy_id: str) -> dict[str, float]:
    policy_cells = _policy_cells(cells, policy_id)
    metric_ids = (
        "assay_fraction",
        "discard_fraction",
        "measured_lifecycle_fraction",
        "nonfinal_instrument_uses_per_closed_lifecycle",
        "continued_after_measurement_fraction",
        "attempted_operations_per_closed_lifecycle",
        "committed_operations_per_closed_lifecycle",
    )
    return {
        metric_id: statistics.fmean(
            float(_metric(cast(Mapping[str, Any], cell["profile"]), metric_id))
            for cell in policy_cells
        )
        for metric_id in metric_ids
    }


def _ordering_checks(summaries: Mapping[str, Mapping[str, float]]) -> dict[str, bool]:
    assay = summaries["assay_all"]
    discard = summaries["start_then_discard"]
    threshold = summaries["measure_then_threshold"]
    return {
        "assay_fraction": assay["assay_fraction"]
        > threshold["assay_fraction"]
        > discard["assay_fraction"],
        "discard_fraction": discard["discard_fraction"]
        > threshold["discard_fraction"]
        > assay["discard_fraction"],
        "measured_lifecycle_fraction": threshold["measured_lifecycle_fraction"]
        > assay["measured_lifecycle_fraction"]
        == discard["measured_lifecycle_fraction"],
        "nonfinal_instrument_uses_per_closed_lifecycle": threshold[
            "nonfinal_instrument_uses_per_closed_lifecycle"
        ]
        > assay["nonfinal_instrument_uses_per_closed_lifecycle"]
        == discard["nonfinal_instrument_uses_per_closed_lifecycle"],
        "continued_after_measurement_fraction": threshold["continued_after_measurement_fraction"]
        > assay["continued_after_measurement_fraction"]
        == discard["continued_after_measurement_fraction"],
        "attempted_operations_per_closed_lifecycle": threshold[
            "attempted_operations_per_closed_lifecycle"
        ]
        > assay["attempted_operations_per_closed_lifecycle"]
        > discard["attempted_operations_per_closed_lifecycle"],
    }


def _resource_expectation_checks(cells: Sequence[Mapping[str, Any]]) -> dict[str, bool]:
    grouped: dict[tuple[int, str], dict[str, Mapping[str, Any]]] = {}
    for cell in cells:
        identity = cast(Mapping[str, Any], cell["identity"])
        key = (int(identity["world_seed"]), str(identity["information_arm"]))
        grouped.setdefault(key, {})[str(identity["policy_id"])] = cell
    checks: dict[str, bool] = {}
    for (seed, arm), policies in sorted(grouped.items()):
        states = {
            policy_id: cast(Mapping[str, Any], policies[policy_id]["resource"])["state"]
            for policy_id in POLICY_IDS
        }
        assay = cast(Mapping[str, Any], states["assay_all"])
        discard = cast(Mapping[str, Any], states["start_then_discard"])
        threshold = cast(Mapping[str, Any], states["measure_then_threshold"])
        label = f"world-{seed}:{arm}"
        checks[f"{label}:discard-no-reagent"] = (
            float(cast(Mapping[str, Any], discard["stocks_used"]).get("reagent_mol", 0.0)) == 0.0
        )
        checks[f"{label}:shared-prefix-stocks"] = assay["stocks_used"] == threshold["stocks_used"]
        checks[f"{label}:discard-fewer-operations"] = int(discard["operation_attempts"]) < int(
            assay["operation_attempts"]
        ) and int(discard["operation_attempts"]) < int(threshold["operation_attempts"])
    return checks


def audit_policy_validity_matrix(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Audit the complete 5 x 2 x 3 matrix without executing formal worlds."""

    if payload.get("schema_id") != MATRIX_SCHEMA_ID:
        raise PolicyValidityAuditError("matrix manifest schema_id mismatch")
    if payload.get("schema_version") != MATRIX_SCHEMA_VERSION:
        raise PolicyValidityAuditError("matrix manifest schema_version mismatch")
    dependencies = _mapping(payload.get("dependencies"), "matrix.dependencies")
    expected_dependencies = {
        "profile_contract_sha256": profile_contract_sha256(),
        "known_policy_contract_sha256": known_policy_contract_sha256(),
        "threshold_binding_sha256": FROZEN_THRESHOLD_BINDING_SHA256,
    }
    for field, expected in expected_dependencies.items():
        if dependencies.get(field) != expected:
            raise PolicyValidityAuditError(f"matrix dependency {field} is stale")
    source_manifest_sha256 = _digest(
        payload.get("source_manifest_sha256"), "matrix.source_manifest_sha256"
    )
    raw_cells = _sequence(payload.get("cells"), "matrix.cells")
    if len(raw_cells) != 30:
        raise PolicyValidityAuditError("matrix must contain exactly 30 campaign bundles")
    audited_cells = [
        audit_campaign_bundle(_mapping(cell, f"matrix.cells[{index}]"))
        for index, cell in enumerate(raw_cells)
    ]
    factorial_keys = {
        (
            int(cast(Mapping[str, Any], cell["identity"])["world_seed"]),
            str(cast(Mapping[str, Any], cell["identity"])["information_arm"]),
            str(cast(Mapping[str, Any], cell["identity"])["policy_id"]),
        )
        for cell in audited_cells
    }
    expected_keys = {
        (seed, arm, policy_id)
        for seed in FORMAL_WORLD_SEEDS
        for arm in INFORMATION_ARMS
        for policy_id in POLICY_IDS
    }
    if factorial_keys != expected_keys:
        raise PolicyValidityAuditError("matrix cells do not match the frozen factorial")
    if len({cell["cell_id"] for cell in audited_cells}) != len(audited_cells):
        raise PolicyValidityAuditError("matrix cell identifiers must be unique")

    arm_audit = _arm_invariance(audited_cells)
    exact_checks = _exact_signature_checks(audited_cells)
    null_checks = _conditional_null_checks(audited_cells)
    summaries = {policy_id: _policy_summary(audited_cells, policy_id) for policy_id in POLICY_IDS}
    ordering_checks = _ordering_checks(summaries)
    resource_checks = _resource_expectation_checks(audited_cells)
    threshold_profiles = _policy_cells(audited_cells, "measure_then_threshold")
    threshold_assays = sum(
        int(cast(Mapping[str, Any], cell["profile"])["counts"]["final_assay_count"])
        for cell in threshold_profiles
    )
    threshold_closed = sum(
        int(cast(Mapping[str, Any], cell["profile"])["counts"]["closed_lifecycle_count"])
        for cell in threshold_profiles
    )
    non_degenerate = 0 < threshold_assays < threshold_closed
    gates = {
        "matrix_complete": len(audited_cells) == 30,
        "all_180_lifecycles_closed": sum(
            int(cast(Mapping[str, Any], cell["profile"])["counts"]["closed_lifecycle_count"])
            for cell in audited_cells
        )
        == 180,
        "all_profiles_rebuilt": True,
        "all_resource_ledgers_replayed": all(
            cast(Mapping[str, Any], cell["resource"])["verified"] is True for cell in audited_cells
        ),
        "all_exact_replays_and_retests_match": all(
            all(cast(Mapping[str, Any], cell["exact_replay"]).values())
            and all(cast(Mapping[str, Any], cell["test_retest"]).values())
            for cell in audited_cells
        ),
        "matched_arm_invariance": arm_audit["passed"] is True,
        "zero_provider_calls": all(
            cast(Mapping[str, Any], cell["profile"])["reliability"]["provider_call_count"] == 0
            for cell in audited_cells
        ),
        "threshold_non_degenerate": non_degenerate,
        "exact_policy_signatures": all(exact_checks.values()),
        "conditional_null_rules": all(null_checks.values()),
        "six_partial_orderings": len(ordering_checks) == 6 and all(ordering_checks.values()),
        "resource_expectations": all(resource_checks.values()),
    }
    report: dict[str, Any] = {
        "schema_id": AUDIT_SCHEMA_ID,
        "schema_version": AUDIT_SCHEMA_VERSION,
        "status": "passed" if all(gates.values()) else "positive_control_unestablished",
        "passed": all(gates.values()),
        "formal_execution_performed_by_auditor": False,
        "manifest_sha256": canonical_json_sha256(payload),
        "source_manifest_sha256": source_manifest_sha256,
        "dependencies": expected_dependencies,
        "counts": {
            "campaigns": len(audited_cells),
            "closed_lifecycles": sum(
                int(cast(Mapping[str, Any], cell["profile"])["counts"]["closed_lifecycle_count"])
                for cell in audited_cells
            ),
            "threshold_assays": threshold_assays,
            "threshold_discards": threshold_closed - threshold_assays,
            "provider_calls": 0,
        },
        "gates": gates,
        "exact_signature_checks": exact_checks,
        "conditional_null_checks": null_checks,
        "partial_ordering_checks": ordering_checks,
        "resource_expectation_checks": resource_checks,
        "arm_invariance": arm_audit,
        "policy_summaries": summaries,
        "cells": audited_cells,
        "explicit_non_orderings": build_known_policy_contract()["expected_profile_signatures"][
            "explicit_non_orderings"
        ],
        "claim_boundary": {
            "construct_validity_positive_control": True,
            "endpoint_performance_ranking": False,
            "material_information_null_effect": False,
            "provider_or_model_capability": False,
            "real_laboratory_claim": False,
            "formal_retuning_allowed": False,
        },
    }
    report["audit_sha256"] = canonical_json_sha256(report)
    return report


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyValidityAuditError(f"cannot read {label} {path}: {exc}") from exc
    return dict(_mapping(payload, label))


def load_matrix_manifest(path: Path) -> dict[str, Any]:
    """Load a manifest and verify every referenced immutable campaign bundle."""

    manifest_path = path.resolve()
    manifest = _load_json_object(manifest_path, "matrix manifest")
    raw_cells = _sequence(manifest.get("cells"), "matrix manifest cells")
    if not raw_cells:
        raise PolicyValidityAuditError("matrix manifest has no campaign bundles")
    if all(isinstance(cell, Mapping) and "bundle_path" not in cell for cell in raw_cells):
        return manifest
    root = manifest_path.parent
    cells: list[dict[str, Any]] = []
    for index, raw_reference in enumerate(raw_cells):
        reference = _mapping(raw_reference, f"matrix manifest cells[{index}]")
        relative = Path(
            _nonempty_string(
                reference.get("bundle_path"),
                f"matrix manifest cells[{index}].bundle_path",
            )
        )
        if relative.is_absolute():
            raise PolicyValidityAuditError("campaign bundle paths must be relative")
        bundle_path = (root / relative).resolve()
        try:
            bundle_path.relative_to(root)
        except ValueError as exc:
            raise PolicyValidityAuditError(
                "campaign bundle path escapes the manifest directory"
            ) from exc
        supplied_hash = _digest(
            reference.get("bundle_sha256"),
            f"matrix manifest cells[{index}].bundle_sha256",
        )
        if file_sha256(bundle_path) != supplied_hash:
            raise PolicyValidityAuditError(f"campaign bundle hash mismatch: {relative}")
        supplied_bytes = _integer(
            reference.get("bundle_bytes"),
            f"matrix manifest cells[{index}].bundle_bytes",
        )
        if bundle_path.stat().st_size != supplied_bytes:
            raise PolicyValidityAuditError(f"campaign bundle byte count mismatch: {relative}")
        cells.append(_load_json_object(bundle_path, "campaign bundle"))
    return {**manifest, "cells": cells}


def audit_policy_validity_manifest(path: Path) -> dict[str, Any]:
    """Read and audit an immutable V05 matrix manifest."""

    return audit_policy_validity_matrix(load_matrix_manifest(path))


__all__ = [
    "AUDIT_SCHEMA_ID",
    "AUDIT_SCHEMA_VERSION",
    "CELL_SCHEMA_ID",
    "CELL_SCHEMA_VERSION",
    "COMPONENT_HASH_FIELDS",
    "EXECUTION_SCHEMA_ID",
    "EXECUTION_SCHEMA_VERSION",
    "FROZEN_THRESHOLD",
    "FROZEN_THRESHOLD_BINDING_SHA256",
    "MATRIX_SCHEMA_ID",
    "MATRIX_SCHEMA_VERSION",
    "PolicyValidityAuditError",
    "audit_campaign_bundle",
    "audit_policy_validity_manifest",
    "audit_policy_validity_matrix",
    "build_campaign_profile",
    "build_execution_hashes",
    "load_matrix_manifest",
]
