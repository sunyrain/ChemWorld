from __future__ import annotations

import json

import pytest

from chemworld.eval.baseline_report import (
    maturity_summary_for_results,
    validate_result_maturity_consistency,
)
from chemworld.eval.runner import make_agent, run_agent


def test_baseline_runner_smoke(tmp_path) -> None:
    output = tmp_path / "random.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("random"),
        world_split="public-dev",
        budget=4,
        objective="balanced",
        seed=3,
        output_path=output,
    )
    assert len(history) == 4
    assert output.exists()
    assert output.read_text(encoding="utf-8").count("\n") == 4
    first_record = json.loads(output.read_text(encoding="utf-8").splitlines()[0])
    assert first_record["physics_maturity"] in {
        "proxy",
        "lite",
        "reference_validated",
        "professional_candidate",
        "professional",
    }
    assert "modules" in first_record["kernel_maturity"]
    assert isinstance(first_record["proxy_allowed"], bool)


def test_greedy_runner_smoke(tmp_path) -> None:
    output = tmp_path / "greedy.jsonl"
    history = run_agent(
        env_id="ChemWorld",
        agent=make_agent("greedy"),
        world_split="public-dev",
        budget=4,
        objective="balanced",
        seed=4,
        output_path=output,
    )
    assert len(history) == 4


def test_maturity_summary_rejects_silent_task_mixing() -> None:
    base = {
        "task_id": "reaction-to-assay",
        "kernel_maturity": {"lowest_level": "lite", "modules": []},
        "physics_maturity": "lite",
        "proxy_allowed": False,
    }
    summary = maturity_summary_for_results([{**base}, {**base}])
    assert summary["levels"]["lite"]["runs"] == 2
    assert summary["tasks"]["reaction-to-assay"]["runs"] == 2

    mixed = {
        **base,
        "kernel_maturity": {"lowest_level": "proxy", "modules": []},
        "physics_maturity": "proxy",
        "proxy_allowed": True,
    }
    with pytest.raises(ValueError, match="mixed maturity metadata"):
        validate_result_maturity_consistency([{**base}, mixed])

