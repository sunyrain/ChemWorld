from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_work_ii_formal_design import EXPECTED_TASKS, _public_selection

from chemworld.eval.work_ii_formal import (
    EXPECTED_METHOD_QUALIFICATION_CONTRACT,
    EXPECTED_PARTICIPANT_EXECUTION_CONTRACT,
)

ROOT = Path(__file__).resolve().parents[1]


def _design() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/work_ii_formal_design_v0.1.json").read_text(encoding="utf-8")
    )


def test_public_formal_world_selection_is_reproducible_and_unique() -> None:
    design = _design()
    cohort = design["world_cohort"]
    public = cohort["public_formal"]
    selected = _public_selection(
        task_ids=EXPECTED_TASKS,
        key=public["selection_key"],
        namespace_start=public["namespace_start"],
        namespace_size=public["namespace_size"],
        worlds_per_task=public["worlds_per_task"],
    )
    assert selected == public["task_world_seeds"]
    flattened = [seed for seeds in selected.values() for seed in seeds]
    assert len(flattened) == len(set(flattened)) == 25
    assert not set(flattened) & set(cohort["development_and_qualification"]["world_seeds"])


def test_formal_design_freezes_five_tasks_three_arms_and_seventy_five_cells() -> None:
    design = _design()
    assert tuple(item["task_id"] for item in design["tasks"]) == EXPECTED_TASKS
    assert design["prior_arms"] == [
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
    ]
    assert design["world_cohort"]["public_formal"]["participant_cell_count"] == 75
    assert design["campaign_contract"]["complete_experiments_per_cell"] == 4
    assert design["campaign_contract"]["checkpoint_complete_experiments"] == [0, 1, 2, 4]
    assert design["campaign_contract"]["matched_evidence_probe_in_primary_matrix"] is False
    assert design["participant_execution_contract"] == EXPECTED_PARTICIPANT_EXECUTION_CONTRACT
    assert design["method_qualification_contract"] == EXPECTED_METHOD_QUALIFICATION_CONTRACT
    assert design["participant_execution_contract"]["separate_reported_denominators"] == [
        "host_provider_process_attempt",
        "provider_session",
        "mcp_tool_call",
        "operation_attempt",
        "committed_operation",
        "complete_experiment",
        "participant_cell",
        "blind_evaluator_execution",
    ]
