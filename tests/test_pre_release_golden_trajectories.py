from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from chemworld.data.logging import load_jsonl
from chemworld.eval.golden import (
    GOLDEN_SUMMARY_SCHEMA_VERSION,
    pre_release_golden_targets,
    summarize_golden_records,
)
from chemworld.eval.runner import make_agent, run_agent
from chemworld.eval.verify import verify_records
from chemworld.tasks import TASK_REGISTRY

FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "golden"
    / "pre_release_scripted_trajectories.json"
)


def _assert_summary_close(actual: Any, expected: Any, path: str = "$") -> None:
    if isinstance(expected, float):
        assert isinstance(actual, int | float), path
        assert abs(float(actual) - expected) <= 1e-9, path
        return
    if isinstance(expected, dict):
        assert isinstance(actual, dict), path
        assert set(actual) == set(expected), path
        for key in expected:
            _assert_summary_close(actual[key], expected[key], f"{path}.{key}")
        return
    if isinstance(expected, list):
        assert isinstance(actual, list), path
        assert len(actual) == len(expected), path
        for index, expected_item in enumerate(expected):
            _assert_summary_close(actual[index], expected_item, f"{path}[{index}]")
        return
    assert actual == expected, path


def test_pre_release_golden_fixture_covers_core_tasks() -> None:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    summaries = payload["summaries"]

    assert payload["fixture_schema_version"] == "chemworld-golden-fixture-0.1"
    assert {summary["task_id"] for summary in summaries} == {
        target.task_id for target in pre_release_golden_targets()
    }
    assert {
        summary["summary_schema_version"] for summary in summaries
    } == {GOLDEN_SUMMARY_SCHEMA_VERSION}


def test_pre_release_scripted_golden_trajectories_are_locked(tmp_path: Path) -> None:
    expected_payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    expected_by_task = {
        str(summary["task_id"]): summary for summary in expected_payload["summaries"]
    }

    for target in pre_release_golden_targets():
        task = TASK_REGISTRY[target.task_id]
        trajectory_path = tmp_path / f"{target.task_id}_seed{target.seed}.jsonl"
        run_agent(
            env_id="ChemWorld",
            agent=make_agent(target.agent_name),
            world_split=task.world_split,
            budget=task.budget,
            objective=task.objective,
            seed=target.seed,
            task_id=target.task_id,
            output_path=trajectory_path,
        )
        records = load_jsonl(trajectory_path)
        verify_result = verify_records(records)
        assert verify_result.verified, verify_result.mismatches

        actual = summarize_golden_records(records)
        expected = expected_by_task[target.task_id]
        _assert_summary_close(actual, expected)
