from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.audit_work_i_policy_validity import main as audit_cli_main

from chemworld.campaign_resources import (
    CampaignResourceCard,
    CampaignResourceLedger,
    campaign_resource_event_id,
)
from chemworld.eval.known_policy_contract import (
    FORMAL_WORLD_SEEDS,
    INFORMATION_ARMS,
    POLICY_IDS,
    PROBE_SCHEDULE,
    known_policy_contract_sha256,
)
from chemworld.eval.policy_validity_audit import (
    CELL_SCHEMA_ID,
    CELL_SCHEMA_VERSION,
    EXECUTION_SCHEMA_ID,
    EXECUTION_SCHEMA_VERSION,
    FROZEN_THRESHOLD,
    FROZEN_THRESHOLD_BINDING_SHA256,
    MATRIX_SCHEMA_ID,
    MATRIX_SCHEMA_VERSION,
    PolicyValidityAuditError,
    audit_campaign_bundle,
    audit_policy_validity_manifest,
    audit_policy_validity_matrix,
    build_campaign_profile,
    build_execution_hashes,
    load_matrix_manifest,
)
from chemworld.eval.policy_validity_contract import profile_contract_sha256
from chemworld.eval.policy_validity_matrix import (
    MANIFEST_FILENAME as PRODUCER_MANIFEST_FILENAME,
)
from chemworld.eval.policy_validity_matrix import (
    MatrixCell,
    build_profile_record_from_execution,
    campaign_resource_card,
    run_matrix,
    semantic_sha256,
)
from chemworld.eval.provenance import canonical_json_sha256, file_sha256

CONTROLLER_HASHES = {
    policy_id: canonical_json_sha256({"synthetic_controller": policy_id})
    for policy_id in POLICY_IDS
}
SOURCE_MANIFEST_SHA256 = canonical_json_sha256({"role": "synthetic immutable V06 fixture"})
ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs/benchmark/work_i_policy_control_matrix_v0.1.json"


def _resource_card() -> CampaignResourceCard:
    return CampaignResourceCard(
        card_id="work-i-known-policy-synthetic-audit-k6-v1",
        operation_attempt_limit=60,
        vessel_start_limit=6,
        final_assay_limit=6,
        nonfinal_instrument_use_limit=6,
        stock_limits={"reagent_mol": 0.20, "solvent_L": 0.20},
        per_instrument_limits={"uvvis": 6},
        metadata={"role": "synthetic-v06-audit-fixture"},
    )


def _actions(policy_id: str, lifecycle_index: int, threshold_signal: float) -> list[dict[str, Any]]:
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
    if threshold_signal < FROZEN_THRESHOLD:
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


def _terminal_kind(action: dict[str, Any]) -> str | None:
    if action.get("operation") == "discard_batch":
        return "discard"
    if action.get("operation") == "measure" and action.get("instrument") == "final_assay":
        return "final_assay"
    return None


def _base_hashes(records: list[dict[str, Any]], snapshot: dict[str, Any]) -> dict[str, str]:
    terminals = [
        {
            "lifecycle_index": record["lifecycle_index"],
            "terminal_kind": record["terminal_kind"],
            "action": record["action"],
        }
        for record in records
        if record["terminal_kind"] is not None
    ]
    endpoints = [
        {
            "lifecycle_index": record["lifecycle_index"],
            "score": record["terminal_score"],
        }
        for record in records
        if record["terminal_kind"] == "final_assay"
    ]
    return {
        "event_sha256": canonical_json_sha256(records),
        "state_sha256": canonical_json_sha256([record["state_sha256"] for record in records]),
        "resource_sha256": snapshot["ledger_sha256"],
        "terminal_sha256": canonical_json_sha256(terminals),
        "endpoint_sha256": canonical_json_sha256(endpoints),
    }


def _identity(*, world_seed: int, arm: str, policy_id: str, card_sha256: str) -> dict[str, Any]:
    return {
        "campaign_id": f"synthetic-world-{world_seed}-{arm}-{policy_id}",
        "world_id": f"synthetic-world-{world_seed}",
        "world_seed": world_seed,
        "information_arm": arm,
        "policy_id": policy_id,
        "resource_card_sha256": card_sha256,
        "physical_identity_sha256": canonical_json_sha256(
            {"world_seed": world_seed, "physics": "synthetic-fixed"}
        ),
        "noise_identity_sha256": canonical_json_sha256(
            {"world_seed": world_seed, "noise": "synthetic-keyed"}
        ),
        "material_information_sha256": canonical_json_sha256(
            {"world_seed": world_seed, "information_arm": arm}
        ),
    }


def _controller_manifest(policy_id: str) -> dict[str, Any]:
    return {
        "schema_id": "chemworld.known_policy_controller",
        "schema_version": "0.1.0",
        "policy_id": policy_id,
        "artifact_bindings": {
            "known_policy_contract_sha256": known_policy_contract_sha256(),
            "threshold_binding_sha256": FROZEN_THRESHOLD_BINDING_SHA256,
            "threshold": FROZEN_THRESHOLD,
            "diagnostic_signal": "observation.conversion",
            "comparator": ">=",
        },
        "reads_material_information": False,
        "provider_call_count": 0,
        "controller_sha256": CONTROLLER_HASHES[policy_id],
    }


def _execution(
    *,
    world_seed: int,
    arm: str,
    policy_id: str,
    threshold_signals: tuple[float, ...],
    score_offset: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    card = _resource_card()
    identity = _identity(
        world_seed=world_seed,
        arm=arm,
        policy_id=policy_id,
        card_sha256=card.card_sha256,
    )
    ledger = CampaignResourceLedger(card)
    records: list[dict[str, Any]] = []
    operation_attempt = 0
    for lifecycle_index in range(6):
        signal = threshold_signals[lifecycle_index]
        actions = _actions(policy_id, lifecycle_index, signal)
        measurement_seen = False
        for within_lifecycle_index, action in enumerate(actions):
            operation_attempt += 1
            event_id = campaign_resource_event_id(str(identity["campaign_id"]), operation_attempt)
            starts_vessel = within_lifecycle_index == 0
            preflight = ledger.preflight(event_id, action, starts_vessel=starts_vessel)
            assert preflight.allowed
            outcome = {
                "transaction_status": "committed",
                "campaign_resource_report_delta": {
                    "physical_cost": 0.1,
                    "accumulated_risk": 0.01,
                },
            }
            ledger.record_outcome(
                event_id,
                action,
                outcome,
                starts_vessel=starts_vessel,
            )
            operation = action["operation"]
            instrument = action.get("instrument")
            observation: dict[str, Any] = {}
            if operation == "measure" and instrument == "uvvis":
                observation = {"conversion": signal}
            terminal_kind = _terminal_kind(action)
            terminal_score = (
                score_offset + 0.5 + lifecycle_index * 0.01
                if terminal_kind == "final_assay"
                else None
            )
            if terminal_score is not None:
                observation = {"score": terminal_score}
            state = {
                "world_seed": world_seed,
                "policy_id": policy_id,
                "lifecycle_index": lifecycle_index,
                "within_lifecycle_index": within_lifecycle_index,
            }
            resource_state = ledger.snapshot()["state"]
            adaptation_source = "measurement" if measurement_seen else "none"
            decision = {
                "policy_id": policy_id,
                "action_sha256": canonical_json_sha256(action),
                "material_information_accessed": False,
                "provider_call_count": 0,
                "adaptation_source": adaptation_source,
                "observed_signal_access": measurement_seen,
                "diagnostic_signal": signal if measurement_seen else None,
                "controller_identity_sha256": CONTROLLER_HASHES[policy_id],
                "known_policy_contract_sha256": known_policy_contract_sha256(),
                "threshold_binding_sha256": (
                    FROZEN_THRESHOLD_BINDING_SHA256
                    if policy_id == "measure_then_threshold"
                    else None
                ),
            }
            record = {
                "operation_attempt_index": operation_attempt,
                "lifecycle_index": lifecycle_index,
                "action": action,
                "transaction_status": "committed",
                "state": state,
                "state_sha256": canonical_json_sha256(state),
                "observation": observation,
                "observation_sha256": canonical_json_sha256(observation),
                "campaign_resource_state": resource_state,
                "campaign_resource_state_sha256": canonical_json_sha256(resource_state),
                "terminal_kind": terminal_kind,
                "terminal_score": terminal_score,
                "decision_audit": decision,
            }
            records.append(record)
            if operation == "measure" and instrument == "uvvis":
                measurement_seen = True
    snapshot = ledger.snapshot()
    base_hashes = _base_hashes(records, snapshot)
    trajectory_manifest_sha256 = canonical_json_sha256(base_hashes)
    profile = build_campaign_profile(
        records,
        snapshot["state"],
        identity,
        trajectory_manifest_sha256=trajectory_manifest_sha256,
    )
    execution = {
        "schema_id": EXECUTION_SCHEMA_ID,
        "schema_version": EXECUTION_SCHEMA_VERSION,
        "provider_call_count": 0,
        "records": records,
        "campaign_resource_ledger_snapshot": snapshot,
        "profile_record": profile,
        "hashes": build_execution_hashes(records, snapshot, profile),
    }
    return execution, identity


def _bundle(
    *,
    world_seed: int,
    arm: str,
    policy_id: str,
    threshold_signals: tuple[float, ...],
    score_offset: float = 0.0,
) -> dict[str, Any]:
    execution, identity = _execution(
        world_seed=world_seed,
        arm=arm,
        policy_id=policy_id,
        threshold_signals=threshold_signals,
        score_offset=score_offset,
    )
    return {
        "schema_id": CELL_SCHEMA_ID,
        "schema_version": CELL_SCHEMA_VERSION,
        "cell_id": identity["campaign_id"],
        "identity": identity,
        "controller_manifest": _controller_manifest(policy_id),
        "original": execution,
        "retest": deepcopy(execution),
    }


def _matrix(
    *,
    threshold_signals: tuple[float, ...] = (0.0, 0.02, 0.0, 0.02, 0.0, 0.02),
    score_offsets: dict[str, float] | None = None,
) -> dict[str, Any]:
    offsets = score_offsets or {}
    return {
        "schema_id": MATRIX_SCHEMA_ID,
        "schema_version": MATRIX_SCHEMA_VERSION,
        "dependencies": {
            "profile_contract_sha256": profile_contract_sha256(),
            "known_policy_contract_sha256": known_policy_contract_sha256(),
            "threshold_binding_sha256": FROZEN_THRESHOLD_BINDING_SHA256,
        },
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "cells": [
            _bundle(
                world_seed=world_seed,
                arm=arm,
                policy_id=policy_id,
                threshold_signals=threshold_signals,
                score_offset=offsets.get(policy_id, 0.0),
            )
            for world_seed in FORMAL_WORLD_SEEDS
            for arm in INFORMATION_ARMS
            for policy_id in POLICY_IDS
        ],
    }


def _producer_execution(
    cell: MatrixCell,
    protocol: Mapping[str, Any],
    *,
    execution_role: str,
) -> dict[str, Any]:
    """Build synthetic evidence through the V05 injected-executor contract."""

    card = campaign_resource_card(protocol)
    ledger = CampaignResourceLedger(card)
    records: list[dict[str, Any]] = []
    terminals: list[dict[str, Any]] = []
    operation_attempt = 0
    threshold_signals = (0.0, 0.02, 0.0, 0.02, 0.0, 0.02)
    logical_campaign_id = (
        f"work-i-known-policy-world-{cell.world_seed:04d}-{cell.policy_id}"
    )
    for lifecycle_index, signal in enumerate(threshold_signals):
        measurement_seen = False
        for within_lifecycle_index, action in enumerate(
            _actions(cell.policy_id, lifecycle_index, signal)
        ):
            operation_attempt += 1
            event_id = campaign_resource_event_id(logical_campaign_id, operation_attempt)
            starts_vessel = within_lifecycle_index == 0
            preflight = ledger.preflight(event_id, action, starts_vessel=starts_vessel)
            assert preflight.allowed
            ledger.record_outcome(
                event_id,
                action,
                {
                    "transaction_status": "committed",
                    "campaign_resource_report_delta": {
                        "physical_cost": 0.1,
                        "accumulated_risk": 0.01,
                    },
                },
                starts_vessel=starts_vessel,
            )
            operation = action["operation"]
            instrument = action.get("instrument")
            observation: dict[str, Any] = {}
            if operation == "measure" and instrument == "uvvis":
                observation = {"conversion": signal}
            terminal_kind = _terminal_kind(action)
            terminal_score = (
                0.5 + lifecycle_index * 0.01
                if terminal_kind == "final_assay"
                else None
            )
            if terminal_score is not None:
                observation = {"score": terminal_score}
            state = {
                "world_seed": cell.world_seed,
                "policy_id": cell.policy_id,
                "lifecycle_index": lifecycle_index,
                "within_lifecycle_index": within_lifecycle_index,
            }
            resource_state = deepcopy(ledger.snapshot()["state"])
            decision_audit = {
                "action": deepcopy(action),
                "adaptation_source": "measurement" if measurement_seen else "none",
                "status": "provided",
            }
            producer_terminal_kind = (
                "assay" if terminal_kind == "final_assay" else terminal_kind
            )
            if producer_terminal_kind is not None:
                terminals.append(
                    {
                        "lifecycle_index": lifecycle_index,
                        "terminal_kind": producer_terminal_kind,
                        "terminal_score": terminal_score,
                        "terminal_event_index": operation_attempt,
                    }
                )
            record = {
                "event_index": operation_attempt,
                "lifecycle_index": lifecycle_index,
                "action": deepcopy(action),
                "observation": observation,
                "reward": 0.0,
                "terminated": False,
                "truncated": False,
                "event_type": (
                    "experiment_end"
                    if terminal_kind == "final_assay"
                    else "batch_discard"
                    if terminal_kind == "discard"
                    else "operation_result"
                ),
                "info": {
                    "transaction_status": "committed",
                    "experiment_ended": terminal_kind is not None,
                },
                "state": state,
                "campaign_resource_state": resource_state,
                "decision_audit": decision_audit,
            }
            record["observation_sha256"] = semantic_sha256(observation)
            record["state_sha256"] = semantic_sha256(state)
            record["campaign_resource_state_sha256"] = semantic_sha256(resource_state)
            records.append(record)
            if operation == "measure" and instrument == "uvvis":
                measurement_seen = True
    snapshot = ledger.snapshot()
    world_id = f"synthetic-world-{cell.world_seed:04d}"
    profile = build_profile_record_from_execution(
        cell=cell,
        world_id=world_id,
        resource_card_sha256=card.card_sha256,
        trajectory_records=records,
        campaign_resource_ledger=snapshot,
        lifecycle_terminals=terminals,
        threshold=FROZEN_THRESHOLD,
    )
    return {
        "schema_id": "chemworld.policy_control_campaign_execution",
        "schema_version": "0.1.0",
        "execution_role": execution_role,
        "identity": {
            "campaign_id": cell.cell_id,
            "cell_id": cell.cell_id,
            "world_seed": cell.world_seed,
            "world_id": world_id,
            "information_arm": cell.information_arm,
            "policy_id": cell.policy_id,
            "resource_card_sha256": card.card_sha256,
            "observation_noise_namespace": f"synthetic-world-{cell.world_seed:04d}",
            "physical_identity": {
                "world_seed": cell.world_seed,
                "world_id": world_id,
                "physics": "injected-synthetic-v06-acceptance",
            },
            "material_information_sha256": semantic_sha256(
                cell.material_information
            ),
        },
        "controller_manifest": _controller_manifest(cell.policy_id),
        "trajectory_records": records,
        "campaign_resource_ledger": snapshot,
        "lifecycle_terminals": terminals,
        "profile_record": profile,
        "decision_audits": [record["decision_audit"] for record in records],
        "counts": {
            **profile["counts"],
            "attempted_operation_count": len(records),
            "committed_operation_count": len(records),
            "provider_call_count": 0,
        },
    }


def _producer_executor(
    cell: MatrixCell, protocol: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        _producer_execution(cell, protocol, execution_role="original"),
        _producer_execution(cell, protocol, execution_role="retest"),
    )


@pytest.fixture(scope="module")
def valid_matrix() -> dict[str, Any]:
    return _matrix()


def test_complete_synthetic_matrix_passes_all_audit_gates(
    valid_matrix: dict[str, Any],
) -> None:
    report = audit_policy_validity_matrix(valid_matrix)
    assert report["passed"] is True
    assert report["status"] == "passed"
    assert all(report["gates"].values())
    assert report["counts"] == {
        "campaigns": 30,
        "closed_lifecycles": 180,
        "threshold_assays": 30,
        "threshold_discards": 30,
        "provider_calls": 0,
    }
    assert len(report["partial_ordering_checks"]) == 6
    unhashed = deepcopy(report)
    supplied_hash = unhashed.pop("audit_sha256")
    assert supplied_hash == canonical_json_sha256(unhashed)


def test_discard_profile_preserves_v01_null_and_resource_semantics() -> None:
    bundle = _bundle(
        world_seed=0,
        arm=INFORMATION_ARMS[0],
        policy_id="start_then_discard",
        threshold_signals=(0.0,) * 6,
    )
    audited = audit_campaign_bundle(bundle)
    profile = audited["profile"]
    assert profile["counts"] == {
        "planned_lifecycle_count": 6,
        "closed_lifecycle_count": 6,
        "final_assay_count": 0,
        "discard_count": 6,
        "measured_lifecycle_count": 0,
        "threshold_eligible_lifecycle_count": 0,
    }
    assert all(value is None for value in profile["endpoint_context"].values())
    assert all(value is None for value in profile["construct_axes"]["outcome_trajectory"].values())
    state = audited["resource"]["state"]
    assert state["operation_attempts"] == 12
    assert state["discarded_batches"] == 6
    assert state["stocks_used"] == {"solvent_L": pytest.approx(0.15)}


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda bundle: bundle["original"].pop("records"),
            "complete immutable records",
        ),
        (
            lambda bundle: bundle["original"]["campaign_resource_ledger_snapshot"][
                "state"
            ].__setitem__("operation_attempts", 999),
            "resource ledger replay failed",
        ),
        (
            lambda bundle: bundle["original"]["profile_record"]["construct_axes"][
                "terminal_commitment"
            ].__setitem__("assay_fraction", 0.5),
            "producer profile differs",
        ),
        (
            lambda bundle: bundle["retest"]["records"][0]["state"].__setitem__("tampered", True),
            "state_sha256 does not bind state",
        ),
        (
            lambda bundle: bundle["original"]["records"][0]["decision_audit"].__setitem__(
                "material_information_accessed", True
            ),
            "material-information access",
        ),
    ],
)
def test_campaign_audit_rejects_missing_or_tampered_evidence(mutation: Any, message: str) -> None:
    bundle = _bundle(
        world_seed=0,
        arm=INFORMATION_ARMS[0],
        policy_id="assay_all",
        threshold_signals=(0.0,) * 6,
    )
    mutation(bundle)
    with pytest.raises(PolicyValidityAuditError, match=message):
        audit_campaign_bundle(bundle)


def test_degenerate_threshold_is_reported_without_retuning() -> None:
    report = audit_policy_validity_matrix(_matrix(threshold_signals=(0.02,) * 6))
    assert report["passed"] is False
    assert report["status"] == "positive_control_unestablished"
    assert report["gates"]["threshold_non_degenerate"] is False
    assert report["counts"]["threshold_assays"] == 60
    assert report["counts"]["threshold_discards"] == 0
    assert report["dependencies"]["threshold_binding_sha256"] == (FROZEN_THRESHOLD_BINDING_SHA256)


def test_same_identity_retest_requires_all_six_component_hashes() -> None:
    bundle = _bundle(
        world_seed=0,
        arm=INFORMATION_ARMS[0],
        policy_id="assay_all",
        threshold_signals=(0.0,) * 6,
    )
    different_retest, _ = _execution(
        world_seed=0,
        arm=INFORMATION_ARMS[0],
        policy_id="assay_all",
        threshold_signals=(0.0,) * 6,
        score_offset=0.1,
    )
    bundle["retest"] = different_retest
    with pytest.raises(PolicyValidityAuditError, match="same-identity retest mismatch"):
        audit_campaign_bundle(bundle)


def test_matched_arm_audit_rejects_physical_identity_drift(
    valid_matrix: dict[str, Any],
) -> None:
    drifted = deepcopy(valid_matrix)
    nominal_assay = next(
        cell
        for cell in drifted["cells"]
        if cell["identity"]["world_seed"] == 0
        and cell["identity"]["information_arm"] == INFORMATION_ARMS[1]
        and cell["identity"]["policy_id"] == "assay_all"
    )
    nominal_assay["identity"]["physical_identity_sha256"] = "f" * 64
    with pytest.raises(PolicyValidityAuditError, match="matched-arm mismatch"):
        audit_policy_validity_matrix(drifted)


def test_endpoint_rank_is_explicitly_outside_construct_recovery() -> None:
    report = audit_policy_validity_matrix(
        _matrix(
            score_offsets={
                "assay_all": -0.25,
                "measure_then_threshold": 0.25,
            }
        )
    )
    assert report["passed"] is True
    assert "mean_assayed_score" in report["explicit_non_orderings"]
    assert "best_assayed_score" in report["explicit_non_orderings"]


def test_manifest_loader_verifies_relative_path_hash_and_byte_count(
    tmp_path: Path,
) -> None:
    matrix = _matrix()
    references = []
    for index, cell in enumerate(matrix["cells"]):
        relative = Path("cells") / f"cell-{index:02d}.json"
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(cell, sort_keys=True) + "\n"
        path.write_text(text, encoding="utf-8", newline="\n")
        references.append(
            {
                "bundle_path": relative.as_posix(),
                "bundle_sha256": file_sha256(path),
                "bundle_bytes": path.stat().st_size,
            }
        )
    manifest = {**matrix, "cells": references}
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    loaded = load_matrix_manifest(manifest_path)
    assert len(loaded["cells"]) == 30
    assert loaded["cells"][0]["schema_id"] == CELL_SCHEMA_ID

    bad = deepcopy(manifest)
    bad["cells"][0]["bundle_sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(PolicyValidityAuditError, match="bundle hash mismatch"):
        load_matrix_manifest(manifest_path)


def test_v05_run_matrix_manifest_passes_all_v06_audit_gates(tmp_path: Path) -> None:
    output_root = tmp_path / "producer-matrix"
    manifest = run_matrix(
        root=ROOT,
        protocol_path=PROTOCOL_PATH,
        output_root=output_root,
        executor=_producer_executor,
        resume=False,
    )
    assert manifest["execution_mode"] == "injected_test"
    assert manifest["formal_result"] is False
    assert manifest["materialized_counts"] == {
        "primary_campaigns": 30,
        "primary_closed_lifecycles": 180,
        "retest_campaigns": 30,
        "retest_closed_lifecycles": 180,
        "provider_calls": 0,
    }

    report = audit_policy_validity_manifest(
        output_root / PRODUCER_MANIFEST_FILENAME
    )
    assert report["passed"] is True
    assert all(report["gates"].values())
    assert report["manifest_sha256"] == manifest["manifest_sha256"]
    assert report["counts"] == {
        "campaigns": 30,
        "closed_lifecycles": 180,
        "threshold_assays": 30,
        "threshold_discards": 30,
        "provider_calls": 0,
    }


def test_cli_stdout_is_one_read_only_json_receipt(
    tmp_path: Path,
    valid_matrix: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    manifest_path = tmp_path / "inline-manifest.json"
    manifest_path.write_text(json.dumps(valid_matrix), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["audit_work_i_policy_validity.py", "--manifest", str(manifest_path)],
    )
    assert audit_cli_main() == 0
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["passed"] is True
    assert receipt["formal_execution_performed_by_auditor"] is False
    assert list(tmp_path.iterdir()) == [manifest_path]
