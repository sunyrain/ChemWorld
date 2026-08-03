from __future__ import annotations

import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from chemworld.campaign_resources import (
    CampaignResourceLedger,
    campaign_resource_event_id,
)
from chemworld.eval.policy_validity_matrix import (
    BUNDLE_DIRECTORY,
    MANIFEST_FILENAME,
    PROGRESS_FILENAME,
    MatrixCell,
    PolicyMatrixError,
    build_preflight,
    build_profile_record_from_execution,
    campaign_resource_card,
    canonical_schedule,
    execute_known_policy_campaign,
    load_matrix_protocol,
    run_matrix,
    semantic_sha256,
    validate_preflight,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "configs/benchmark/work_i_policy_control_matrix_v0.1.json"


def _fake_execution(
    cell: MatrixCell,
    protocol: Mapping[str, Any],
    *,
    execution_role: str,
) -> dict[str, Any]:
    card = campaign_resource_card(protocol)
    ledger = CampaignResourceLedger(card)
    records: list[dict[str, Any]] = []
    terminals: list[dict[str, Any]] = []
    logical_campaign_id = (
        f"work-i-known-policy-world-{cell.world_seed:04d}-{cell.policy_id}"
    )
    for lifecycle_index in range(6):
        ordinal = lifecycle_index + 1
        action = {"operation": "discard_batch", "reason": "synthetic-v05-test"}
        event_id = campaign_resource_event_id(logical_campaign_id, ordinal)
        preflight = ledger.preflight(event_id, action, starts_vessel=True)
        assert preflight.allowed
        ledger.record_outcome(
            event_id,
            action,
            {"transaction_status": "committed"},
            starts_vessel=True,
        )
        terminal = {
            "lifecycle_index": lifecycle_index,
            "terminal_kind": "discard",
            "terminal_score": None,
            "terminal_event_index": ordinal,
        }
        terminals.append(terminal)
        records.append(
            {
                "event_index": ordinal,
                "lifecycle_index": lifecycle_index,
                "action": deepcopy(action),
                "observation": {},
                "reward": 0.0,
                "terminated": False,
                "truncated": False,
                "event_type": "batch_discard",
                "info": {
                    "transaction_status": "committed",
                    "experiment_ended": True,
                },
                "state": {"closed_lifecycle_count": ordinal},
                "campaign_resource_state": deepcopy(ledger.snapshot()["state"]),
                "decision_audit": {
                    "status": "provided",
                    "action": deepcopy(action),
                },
            }
        )
        records[-1]["observation_sha256"] = semantic_sha256(
            records[-1]["observation"]
        )
        records[-1]["state_sha256"] = semantic_sha256(records[-1]["state"])
        records[-1]["campaign_resource_state_sha256"] = semantic_sha256(
            records[-1]["campaign_resource_state"]
        )
    snapshot = ledger.snapshot()
    world_id = f"synthetic-world-{cell.world_seed:04d}"
    profile = build_profile_record_from_execution(
        cell=cell,
        world_id=world_id,
        resource_card_sha256=card.card_sha256,
        trajectory_records=records,
        campaign_resource_ledger=snapshot,
        lifecycle_terminals=terminals,
        threshold=0.5,
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
                "policy_id": cell.policy_id,
            },
            "material_information_sha256": semantic_sha256(
                cell.material_information
            ),
        },
        "controller_manifest": {
            "policy_id": cell.policy_id,
            "provider_call_count": 0,
            "synthetic_test_controller": True,
        },
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


def _fake_executor(
    cell: MatrixCell, protocol: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        _fake_execution(cell, protocol, execution_role="original"),
        _fake_execution(cell, protocol, execution_role="retest"),
    )


def test_preflight_is_outcome_blind_and_deterministic() -> None:
    first = build_preflight(ROOT, PROTOCOL_PATH)
    second = build_preflight(ROOT, PROTOCOL_PATH)
    assert first == second
    assert validate_preflight(first) == []
    assert first["formal_result"] is False
    assert first["formal_execution_authorized"] is False
    assert first["expected_counts"] == {
        "primary_campaigns": 30,
        "primary_closed_lifecycles": 180,
        "retest_campaigns": 30,
        "retest_closed_lifecycles": 180,
        "provider_calls": 0,
    }
    assert first["checks"]["formal_outcomes_not_read"] is True


def test_schedule_is_the_frozen_world_major_factorial() -> None:
    protocol = load_matrix_protocol(PROTOCOL_PATH)
    schedule = canonical_schedule(protocol)
    assert len(schedule) == 30
    assert len({cell.cell_id for cell in schedule}) == 30
    assert [
        (cell.world_seed, cell.information_arm, cell.policy_id)
        for cell in schedule[:6]
    ] == [
        (0, "opaque_codes", "assay_all"),
        (0, "opaque_codes", "start_then_discard"),
        (0, "opaque_codes", "measure_then_threshold"),
        (0, "anonymous_nominal_properties", "assay_all"),
        (0, "anonymous_nominal_properties", "start_then_discard"),
        (0, "anonymous_nominal_properties", "measure_then_threshold"),
    ]


def test_injected_matrix_writes_content_addressed_complete_manifest(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "matrix"
    manifest = run_matrix(
        root=ROOT,
        protocol_path=PROTOCOL_PATH,
        output_root=output_root,
        executor=_fake_executor,
        resume=False,
    )
    assert manifest["status"] == "complete"
    assert manifest["immutable"] is True
    assert manifest["materialized_counts"]["primary_campaigns"] == 30
    assert manifest["materialized_counts"]["primary_closed_lifecycles"] == 180
    assert manifest["materialized_counts"]["provider_calls"] == 0
    assert manifest["all_matched_arm_audits_passed"] is True
    assert len(manifest["cells"]) == 30
    assert len(list((output_root / BUNDLE_DIRECTORY).glob("*.json"))) == 30
    assert (output_root / MANIFEST_FILENAME).is_file()
    assert (output_root / PROGRESS_FILENAME).is_file()

    resumed = run_matrix(
        root=ROOT,
        protocol_path=PROTOCOL_PATH,
        output_root=output_root,
        executor=lambda *_: pytest.fail("completed matrix must not re-execute"),
        resume=True,
    )
    assert resumed == manifest


def test_resume_accepts_only_a_validated_canonical_prefix(tmp_path: Path) -> None:
    output_root = tmp_path / "interrupted"
    calls: list[str] = []

    def interrupted(
        cell: MatrixCell, protocol: Mapping[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        calls.append(cell.cell_id)
        if len(calls) == 4:
            raise RuntimeError("simulated interruption")
        return _fake_executor(cell, protocol)

    with pytest.raises(RuntimeError, match="simulated interruption"):
        run_matrix(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output_root=output_root,
            executor=interrupted,
            resume=False,
        )
    progress = json.loads(
        (output_root / PROGRESS_FILENAME).read_text(encoding="utf-8")
    )
    assert len(progress["cells"]) == 3
    accepted_hashes = {
        path.name: path.read_bytes()
        for path in (output_root / BUNDLE_DIRECTORY).glob("*.json")
    }
    resumed_calls: list[str] = []

    def resumed_executor(
        cell: MatrixCell, protocol: Mapping[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        resumed_calls.append(cell.cell_id)
        return _fake_executor(cell, protocol)

    manifest = run_matrix(
        root=ROOT,
        protocol_path=PROTOCOL_PATH,
        output_root=output_root,
        executor=resumed_executor,
        resume=True,
    )
    assert len(resumed_calls) == 27
    assert resumed_calls[0].startswith("cell-04-")
    assert manifest["materialized_counts"]["primary_campaigns"] == 30
    for name, content in accepted_hashes.items():
        assert (output_root / BUNDLE_DIRECTORY / name).read_bytes() == content


@pytest.mark.parametrize("failure", ["corruption", "hole", "unexpected"])
def test_resume_fails_closed_on_invalid_materialized_state(
    tmp_path: Path, failure: str
) -> None:
    output_root = tmp_path / failure
    calls = 0

    def stop_after_two(
        cell: MatrixCell, protocol: Mapping[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise RuntimeError("stop")
        return _fake_executor(cell, protocol)

    with pytest.raises(RuntimeError, match="stop"):
        run_matrix(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output_root=output_root,
            executor=stop_after_two,
            resume=False,
        )
    bundles = sorted((output_root / BUNDLE_DIRECTORY).glob("*.json"))
    if failure == "corruption":
        bundles[0].write_text("{}\n", encoding="utf-8")
    elif failure == "hole":
        bundles[0].unlink()
    else:
        (output_root / "unexpected.txt").write_text("unexpected", encoding="utf-8")
    with pytest.raises(PolicyMatrixError):
        run_matrix(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output_root=output_root,
            executor=lambda *_: pytest.fail("invalid resume must not execute"),
            resume=True,
        )


def test_resume_rejects_missing_root_and_nonresume_rejects_overwrite(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing"
    with pytest.raises(PolicyMatrixError, match="does not exist"):
        run_matrix(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output_root=missing,
            executor=_fake_executor,
            resume=True,
        )
    occupied = tmp_path / "occupied"
    occupied.mkdir()
    (occupied / "sentinel").write_text("keep", encoding="utf-8")
    with pytest.raises(PolicyMatrixError, match="refusing to overwrite"):
        run_matrix(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output_root=occupied,
            executor=_fake_executor,
            resume=False,
        )


def test_formal_execution_is_double_gated(tmp_path: Path) -> None:
    with pytest.raises(PolicyMatrixError, match="explicit authorization"):
        run_matrix(
            root=ROOT,
            protocol_path=PROTOCOL_PATH,
            output_root=tmp_path / "formal",
            executor=lambda *_: pytest.fail("formal gate must precede execution"),
            resume=False,
            execution_mode="formal",
            allow_formal_execution=False,
        )


def test_live_nonformal_retest_excludes_random_runtime_identity() -> None:
    protocol = load_matrix_protocol(PROTOCOL_PATH)
    cell = MatrixCell(
        ordinal=1,
        cell_id="nonformal-v05-retest",
        world_seed=20_000,
        information_arm="opaque_codes",
        policy_id="measure_then_threshold",
        material_information={"mode": "opaque_codes"},
    )
    original = execute_known_policy_campaign(
        cell, protocol, execution_role="original"
    )
    retest = execute_known_policy_campaign(cell, protocol, execution_role="retest")
    assert original["identity"] == retest["identity"]
    for field in (
        "trajectory_records",
        "campaign_resource_ledger",
        "lifecycle_terminals",
        "profile_record",
        "decision_audits",
        "counts",
    ):
        assert semantic_sha256(original[field]) == semantic_sha256(retest[field])
    assert all(
        "campaign_id" not in record["info"]
        and "operation_id" not in record["info"]
        for record in original["trajectory_records"]
    )

