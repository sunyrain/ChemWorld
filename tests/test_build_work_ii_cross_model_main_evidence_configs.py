from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_work_ii_cross_model_main_evidence_configs.py"
PLAN = ROOT / "configs/benchmark/work_ii_cross_model_main_evidence_completion_v0.1.json"


def _module():
    spec = importlib.util.spec_from_file_location("w2_59_builder", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_w2_59_materialized_configs_match_the_canonical_plan() -> None:
    outputs = _module().build_outputs(PLAN)

    assert len(outputs) == 14
    assert all(path.is_file() for path in outputs)
    assert all(_module()._load(path) == payload for path, payload in outputs.items())

    c2 = outputs[
        ROOT / "configs/benchmark/work_ii_c2_gpt56_sol_medium_replication_v0.1.json"
    ]
    assert c2["expected_public_totals"] == {
        "task_world_clusters": 45,
        "sessions": 135,
        "complete_experiments": 1260,
    }
    runtime_paths = [
        path
        for path in outputs
        if "work_ii_c2_gpt56_sol_medium_runtime_v0.1" in path.as_posix()
    ]
    assert len(runtime_paths) == 9
    for path in runtime_paths:
        provider = outputs[path]["provider"]
        assert provider["id"] == "chemworld_openai_https"
        assert provider["auth_mode"] == "none"
        assert provider["model"] == "gpt-5.6-sol"
        assert provider["reasoning_effort"] == "medium"
