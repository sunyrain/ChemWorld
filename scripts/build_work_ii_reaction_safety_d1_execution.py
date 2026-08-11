#!/usr/bin/env python3
"""Build the provider-ready reaction-safety matched-prior D1 config."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

from chemworld.eval.provenance import file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1.json"
DEFAULT_OUTPUT = (
    ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1_execution.json"
)


def build(source: dict, *, source_path: Path) -> dict:
    config = copy.deepcopy(source)
    config["pilot_id"] = "work-ii-reaction-safety-matched-prior-d1-execution"
    config["observation_noise_namespace"] = (
        "work-ii-reaction-safety-matched-prior-d1-execution"
    )
    config["execution"].update(
        {
            "failure_semantics": (
                "retain cell failures and continue every scheduled seed triplet"
            ),
            "systemic_failure_semantics": (
                "stop only when all three arms fail before the first committed operation"
            ),
            "pilot_expansion_headroom_fraction": 0.20,
        }
    )
    config["provider"].update(
        {
            "session_wall_time_limit_s": 6600.0,
            "max_recovered_mcp_tool_failures": 3,
            "max_consecutive_mcp_tool_failures": 1,
            "max_provider_error_events": 1,
            "progress_interval_s": 30.0,
        }
    )
    config["method_resources"].pop("resource_status", None)
    config["method_resources"].update(
        {
            "input_token_limit": 12_000_000,
            "uncached_input_token_limit": 1_200_000,
            "output_token_limit": 96_000,
            "wall_time_limit_s": 7200.0,
        }
    )
    config["qualification"].update(
        {
            "max_resource_rejections": 1,
            "execution_authorized": True,
            "formal_r5_authorized": False,
        }
    )
    config["development_resource_basis"] = {
        "source_config": source_path.relative_to(ROOT).as_posix(),
        "source_config_sha256": file_sha256(source_path),
        "historical_wellau_four_experiment_input_tokens_per_cell": [
            1_417_106,
            1_424_127,
            1_443_321,
        ],
        "historical_wellau_four_experiment_uncached_tokens_per_cell": [
            134_546,
            177_407,
            95_225,
        ],
        "historical_wellau_four_experiment_output_tokens_per_cell": [
            11_645,
            11_761,
            9_829,
        ],
        "historical_wellau_four_experiment_session_elapsed_s_per_cell": [
            427.142,
            435.138,
            381.578,
        ],
        "scaling_rule": (
            "development envelope allows quadratic cumulative-input growth across a 10-experiment "
            "persistent session; uncached input, output and wall time retain additional headroom"
        ),
        "formal_cap_status": "not_frozen_until_this_triplet_is_audited",
    }
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source_path = args.input.resolve()
    output_path = args.output.resolve()
    source = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(source, dict):
        raise ValueError("D1 source config must contain an object")
    generated = build(source, source_path=source_path)
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        if existing != generated:
            raise ValueError("existing D1 execution config differs from reconstruction")
    else:
        write_json_atomic(output_path, generated)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "task_id": generated["task_id"],
                "world_seed": generated["world_seed"],
                "arms": list(generated["prior_arms"]),
                "complete_experiments": generated["campaign"]["complete_experiments"],
                "snapshot_count": len(generated["snapshot_stages"]),
            },
            ensure_ascii=False,
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
