from __future__ import annotations

from copy import deepcopy

import pytest

from chemworld.eval.work_ii_development_confirmation import (
    build_development_confirmation_preflight,
    collect_development_cells,
    physical_campaign_contract,
)


def _result(arm: str, *, qualified: bool = True) -> dict[str, object]:
    return {
        "arm": arm,
        "completed": qualified,
        "failure": None if qualified else {"type": "retained_failure"},
        "qualification": {"passed": qualified},
        "analysis": {},
    }


def test_physical_campaign_contract_ignores_provider_and_resource_envelopes() -> None:
    left = {
        "schema_version": "a",
        "pilot_id": "left",
        "task_id": "partition-discovery",
        "world_split": "public-test",
        "objective": "balanced",
        "prior_arms": {"opaque": {"mode": "opaque_codes"}},
        "campaign": {"complete_experiments": 4},
        "provider": {"id": "wellau"},
        "method_resources": {"output_token_limit": 10},
    }
    right = deepcopy(left)
    right.update(
        {
            "schema_version": "b",
            "pilot_id": "right",
            "provider": {"id": "deepseek"},
            "method_resources": {"output_token_limit": 100},
        }
    )
    assert physical_campaign_contract(left) == physical_campaign_contract(right)


def test_collect_development_cells_retains_failures_and_rejects_duplicates() -> None:
    manifest = {"provider_group": "deepseek"}
    source = {
        "source_id": "source-a",
        "provider_group": "deepseek",
        "task_id": "task-a",
    }
    matrix = {
        "seed_reports": [
            {
                "world_seed": 0,
                "results": [
                    _result("opaque"),
                    _result("aligned_nominal"),
                    _result("misindexed_nominal", qualified=False),
                ],
            }
        ]
    }
    cells = collect_development_cells(manifest, [(source, matrix)])
    assert len(cells) == 3
    assert sum(cell["completed_and_qualified"] for cell in cells) == 2
    assert {cell["participant_state"] for cell in cells} == {"completed", "failed"}

    with pytest.raises(ValueError, match="duplicate development cell"):
        collect_development_cells(manifest, [(source, matrix), (source, matrix)])


def test_preflight_freezes_75_cells_25_clusters_and_qualified_blind_denominator() -> None:
    cells = []
    tasks = [f"task-{index}" for index in range(5)]
    for task_id in tasks:
        for world_seed in range(5):
            for arm in ("opaque", "aligned_nominal", "misindexed_nominal"):
                cells.append(
                    {
                        "task_id": task_id,
                        "world_seed": world_seed,
                        "prior_arm": arm,
                        "completed_and_qualified": not (
                            task_id == "task-4" and world_seed == 4 and arm == "opaque"
                        ),
                    }
                )
    configs = {
        task_id: {
            "task_id": task_id,
            "world_split": "public-test",
            "campaign": {"complete_experiments": 4},
        }
        for task_id in tasks
    }
    preflight = build_development_confirmation_preflight(
        source_manifest={"provider_group": "deepseek", "analysis_id": "analysis"},
        cells=cells,
        task_configs=configs,
        participant_configs=deepcopy(configs),
        source_bindings=[],
        source_commit="a" * 40,
    )
    assert preflight["status"] == "passed"
    assert preflight["retained_participant_cell_count"] == 75
    assert preflight["qualified_blind_cell_count"] == 74
    assert preflight["scheduled_truth_query_count"] == 100
    assert preflight["scheduled_blind_execution_count"] == 444
