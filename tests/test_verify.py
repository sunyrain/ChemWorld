from __future__ import annotations

import pytest

from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import make_agent, run_agent
from chemworld.eval.verify import verify_records


def test_verify_records_accepts_valid_trajectory(tmp_path) -> None:
    path = tmp_path / "run.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=3,
        objective="balanced",
        seed=12,
        output_path=path,
    )
    result = verify_records(load_jsonl(path))
    assert result.verified
    assert result.checked_steps == 3


def test_verify_records_rejects_tampered_trajectory(tmp_path) -> None:
    path = tmp_path / "run.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=3,
        objective="balanced",
        seed=13,
        output_path=path,
    )
    records = load_jsonl(path)
    records[0]["reward"] = 999.0
    result = verify_records(records)
    assert not result.verified
    assert result.mismatches


def test_verify_records_rejects_mechanism_hash_mismatch(tmp_path) -> None:
    path = tmp_path / "mechanism_hash.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=path,
    )
    records = load_jsonl(path)
    records[0]["mechanism_hash"] = "tampered-mechanism-hash"

    result = verify_records(records)

    assert not result.verified
    assert any(
        mismatch["step"] == 0 and mismatch["field"] == "mechanism_hash"
        for mismatch in result.mismatches
    )


def test_verify_records_rejects_contract_hash_mismatch(tmp_path) -> None:
    path = tmp_path / "contract_hash.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=path,
    )
    records = load_jsonl(path)
    records[0]["scoring_contract_hash"] = "tampered-scoring-contract-hash"
    records[0]["observation_contract_hash"] = "tampered-observation-contract-hash"

    result = verify_records(records)

    assert not result.verified
    mismatch_fields = {mismatch["field"] for mismatch in result.mismatches}
    assert "scoring_contract_hash" in mismatch_fields
    assert "observation_contract_hash" in mismatch_fields


def test_verify_records_rejects_task_profile_hash_mismatch(tmp_path) -> None:
    path = tmp_path / "task_profile_hash.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=path,
    )
    records = load_jsonl(path)
    records[0]["task_contract_hash"] = "tampered-task-contract-hash"
    records[0]["runtime_profile_hash"] = "tampered-runtime-profile-hash"

    result = verify_records(records)

    assert not result.verified
    mismatch_fields = {mismatch["field"] for mismatch in result.mismatches}
    assert "task_contract_hash" in mismatch_fields
    assert "runtime_profile_hash" in mismatch_fields


def test_verify_records_rejects_runtime_v2_transaction_metadata_tampering(
    tmp_path,
) -> None:
    path = tmp_path / "transaction_metadata.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=path,
    )
    records = load_jsonl(path)
    records[0]["kernel_id"] = "chemworld.operation.fake"
    records[0]["transaction_status"] = "rolled_back"
    records[0]["affected_ledgers"] = ["process", "fake_ledger"]
    records[0]["world_events"][0]["event_type"] = "fake_event"

    result = verify_records(records)

    assert not result.verified
    mismatch_fields = {mismatch["field"] for mismatch in result.mismatches}
    assert "kernel_id" in mismatch_fields
    assert "transaction_status" in mismatch_fields
    assert "affected_ledgers.length" in mismatch_fields
    assert "world_events.0.event_type" in mismatch_fields


def test_verify_records_rejects_runtime_v2_state_patch_tampering(tmp_path) -> None:
    path = tmp_path / "state_patch.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=path,
    )
    records = load_jsonl(path)
    records[0]["state_patches_summary"][0]["summary"]["delta_cost"] += 0.25

    result = verify_records(records)

    assert not result.verified
    assert any(
        mismatch["field"] == "state_patches_summary.0.summary.delta_cost"
        for mismatch in result.mismatches
    )


def test_verify_records_rejects_invalid_schema() -> None:
    with pytest.raises(ValueError, match="Trajectory is empty"):
        verify_records([])


def test_verify_records_uses_task_budget_for_early_termination(tmp_path) -> None:
    path = tmp_path / "reaction_to_assay.jsonl"
    run_agent(
        env_id="ChemWorld",
        agent=make_agent("scripted_chemistry"),
        world_split="public-dev",
        budget=18,
        objective="balanced",
        seed=0,
        task_id="reaction-to-assay",
        output_path=path,
    )
    records = load_jsonl(path)
    assert len(records) < records[0]["budget"]
    assert records[-1]["terminated"]
    assert not records[-1]["truncated"]

    result = verify_records(records)
    assert result.verified
    assert result.mismatches == []
