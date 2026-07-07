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

