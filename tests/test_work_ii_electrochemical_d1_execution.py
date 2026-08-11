from __future__ import annotations

import json
from pathlib import Path

from scripts.build_work_ii_electrochemical_d1_execution import build

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json"


def test_electrochemical_d1_execution_builder_preserves_q2_pattern() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    config = build(source, source_path=SOURCE)

    assert config["task_id"] == "electrochemical-conversion"
    assert config["world_seed"] == 0
    assert config["campaign"]["complete_experiments"] == 10
    assert config["campaign"]["operation_attempt_limit"] == 110
    assert config["campaign"]["process_time_limit_s"] == 45_000.0
    assert config["provider"]["model"] == "gpt-5.6-sol"
    assert config["provider"]["reasoning_effort"] == "medium"
    assert config["provider"]["session_wall_time_limit_s"] == 6_600.0
    assert config["method_resources"]["input_token_limit"] == 12_000_000
    assert config["method_resources"]["uncached_input_token_limit"] == 1_200_000
    assert config["method_resources"]["output_token_limit"] == 96_000
    assert config["qualification"]["execution_authorized"] is True
    assert config["qualification"]["formal_r5_authorized"] is False
    assert "resource_status" not in config["method_resources"]
