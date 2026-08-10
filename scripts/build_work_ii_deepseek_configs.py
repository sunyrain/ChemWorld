#!/usr/bin/env python3
"""Derive the frozen Work II task configs for the DeepSeek Codex provider."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def _provider() -> dict[str, Any]:
    return {
        "id": "deepseek",
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/",
        "wire_api": "responses",
        "auth_mode": "experimental_bearer_token",
        "api_key_file": "api.md",
        "model_catalog_json": "configs/providers/deepseek_v4_flash_models.json",
        "preferred_auth_method": "apikey",
        "forced_login_method": "api",
        "model": "deepseek-v4-flash",
        "reasoning_effort": "high",
        "request_timeout_s": 1200.0,
        "finalization_timeout_s": 600.0,
        "session_wall_time_limit_s": 1800.0,
        "max_recovered_mcp_tool_failures": 3,
        "max_consecutive_mcp_tool_failures": 1,
        "max_provider_error_events": 1,
        "progress_interval_s": 30.0,
    }


def _limits(task_id: str) -> dict[str, Any]:
    if task_id == "electrochemical-conversion":
        return {
            "input_token_limit": 4000000,
            "uncached_input_token_limit": 400000,
            "output_token_limit": 80000,
            "wall_time_limit_s": 7200.0,
        }
    if task_id == "reaction-to-crystallization":
        return {
            "input_token_limit": 7000000,
            "uncached_input_token_limit": 1000000,
            "output_token_limit": 100000,
            "wall_time_limit_s": 9000.0,
        }
    if task_id == "reaction-to-distillation":
        return {
            "input_token_limit": 7000000,
            "uncached_input_token_limit": 1000000,
            "output_token_limit": 100000,
            "wall_time_limit_s": 9000.0,
        }
    raise ValueError(f"unsupported Work II task: {task_id}")


def derive(source: Path, destination: Path) -> None:
    config = _load(source)
    task_id = str(config["task_id"])
    config["schema_version"] = "chemworld-work-ii-campaign-pilot-0.3"
    config["pilot_id"] = f"work-ii-{task_id}-deepseek-v4-flash-prior-campaign"
    config["execution"] = {
        **dict(config.get("execution", {})),
        "max_concurrency": 3,
        "parallelization_unit": "same_seed_prior_arm_triplet",
        "within_cell_concurrency": 1,
        "failure_semantics": (
            "retain cell failures and continue every scheduled seed triplet"
        ),
        "systemic_failure_semantics": (
            "stop only when all three arms fail before the first committed operation"
        ),
        "pilot_expansion_headroom_fraction": 0.2,
    }
    config["provider"] = _provider()
    config["qualification"] = {
        **dict(config.get("qualification", {})),
        "max_resource_rejections": 1,
    }
    config["method_resources"] = {
        **dict(config["method_resources"]),
        **_limits(task_id),
        "model_call_limit": 1,
    }
    config["provider_qualification"] = {
        "basis": "DeepSeek qualification-v2 seed-0 opaque electrochemical cell",
        "qualification_report": (
            "runs/development/work-ii-deepseek-qualification-v2-seed0-opaque/report.json"
        ),
        "catalog_requirement": "supports_search_tool=false",
        "session_contract": "one persistent Codex session per task-prior-seed cell",
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["electrochemical", "crystallization", "distillation"])
    parser.add_argument("--output-dir", type=Path, default=ROOT / "configs/benchmark")
    args = parser.parse_args()
    source_names = {
        "electrochemical": "work_ii_campaign_pilot.json",
        "crystallization": "work_ii_crystallization_campaign.json",
        "distillation": "work_ii_distillation_campaign.json",
    }
    target_names = {
        "electrochemical": "work_ii_electrochemical_deepseek_v4_flash_campaign.json",
        "crystallization": "work_ii_crystallization_deepseek_v4_flash_campaign.json",
        "distillation": "work_ii_distillation_deepseek_v4_flash_campaign.json",
    }
    selected = [args.task] if args.task else list(source_names)
    for key in selected:
        derive(
            ROOT / "configs/benchmark" / source_names[key],
            args.output_dir / target_names[key],
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
