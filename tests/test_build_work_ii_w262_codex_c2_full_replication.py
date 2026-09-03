from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_work_ii_w262_codex_c2_full_replication import (  # noqa: E402
    COHORT_ID,
    SOURCE_PLAN,
    TARGET_PLAN,
    build_outputs,
)


def test_w262_builds_a_fresh_full_codex_c2_cohort() -> None:
    outputs = build_outputs()
    plan = outputs[TARGET_PLAN]

    assert len(outputs) == 10
    assert plan["cohort_id"] == COHORT_ID
    assert plan["schema_version"] == (
        "chemworld-work-ii-c2-cross-model-replication-0.1"
    )
    assert plan["expected_public_totals"] == {
        "task_world_clusters": 45,
        "sessions": 135,
        "complete_experiments": 1260,
    }
    assert plan["expected_complete_totals"] == plan["expected_public_totals"]
    assert plan["provider"]["model"] == "gpt-5.6-sol"
    assert plan["provider"]["reasoning_effort"] == "medium"
    assert plan["full_cohort_successor"]["historical_w2_59_canary_reused"] is False
    assert plan["full_cohort_successor"]["source_deepseek_plan"] == (
        SOURCE_PLAN.relative_to(ROOT).as_posix()
    )

    runtime_paths = [path for path in outputs if path != TARGET_PLAN]
    assert len(runtime_paths) == 9
    assert all(outputs[path]["provider"]["auth_mode"] == "none" for path in runtime_paths)
    assert all(
        outputs[path]["cross_model_replication"]["cohort_id"] == COHORT_ID
        for path in runtime_paths
    )
