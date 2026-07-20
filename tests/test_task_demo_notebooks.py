from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from notebooks.task_demos.demo_utils import (
    compare_hidden_worlds,
    run_vector,
    standard_probe_vectors,
)

TASK_DEMO_DIR = Path("notebooks/task_demos")
TASK_DEMOS = {
    "01_partition_discovery.ipynb": (
        "partition-discovery",
        "constitutive_law_family",
    ),
    "02_reaction_crystallization.ipynb": (
        "reaction-to-crystallization",
        "rate_law_family",
    ),
    "03_reaction_distillation.ipynb": (
        "reaction-to-distillation",
        "topology_family",
    ),
    "04_flow_reaction.ipynb": (
        "flow-reaction-optimization",
        "rate_law_family",
    ),
    "05_electrochemical_conversion.ipynb": (
        "electrochemical-conversion",
        "constitutive_law_family",
    ),
    "06_equilibrium_characterization.ipynb": (
        "equilibrium-characterization",
        "constitutive_law_family",
    ),
}


def _notebook_text(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", ()))
        if isinstance(cell.get("source"), list)
        else str(cell.get("source", ""))
        for cell in notebook["cells"]
    )


def test_task_demo_notebooks_are_valid_and_cover_the_serious_suite() -> None:
    assert len(TASK_DEMOS) == 6
    for filename, (task_id, mechanism_mode) in TASK_DEMOS.items():
        path = TASK_DEMO_DIR / filename
        notebook = json.loads(path.read_text(encoding="utf-8"))
        text = _notebook_text(path)
        assert notebook["nbformat"] == 4
        assert len(notebook["cells"]) >= 12
        assert sum(cell["cell_type"] == "code" for cell in notebook["cells"]) >= 6
        assert task_id in text
        assert mechanism_mode in text
        for phrase in (
            "公开任务合同",
            "候选干预",
            "执行并读取反馈",
            "隐藏规律",
            "world model",
            "processed_estimate",
            "leaderboard_score",
            "不读取 hidden state",
        ):
            assert phrase in text


@pytest.mark.parametrize("task_id", [task_id for task_id, _ in TASK_DEMOS.values()])
def test_task_demo_midpoint_recipe_executes_with_public_evidence(task_id: str) -> None:
    vector = standard_probe_vectors(task_id)["mid"]
    run = run_vector(task_id, vector, seed=0)
    assert not run.trace.empty
    assert bool(run.trace["valid_before_step"].all())
    assert not bool(run.trace["precondition_failed"].any())
    assert run.metrics["leaderboard_score"] is not None
    assert np.isfinite(float(run.metrics["leaderboard_score"]))


@pytest.mark.parametrize(
    ("task_id", "mechanism_mode"),
    list(TASK_DEMOS.values()),
)
def test_task_demo_hidden_world_pair_is_executable(
    task_id: str,
    mechanism_mode: str,
) -> None:
    vector = standard_probe_vectors(task_id)["mid"]
    comparison = compare_hidden_worlds(
        task_id,
        vector,
        mechanism_mode=mechanism_mode,
        seed=0,
    )
    assert comparison["opaque_world"].tolist() == ["World A", "World B"]
    assert bool(comparison["all_actions_valid"].all())
    assert comparison["leaderboard_score"].notna().all()
