#!/usr/bin/env python3
"""Build the two preregistered reaction-safety D2 world-owned configs."""

from __future__ import annotations

import argparse
import copy
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from chemworld.eval.provenance import file_sha256, write_json_atomic

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = (
    ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1_execution.json"
)
DEFAULT_PACKAGE = (
    ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_package.json"
)
PREREGISTERED_WORLDS = (1, 4)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def build_world_config(
    base: Mapping[str, Any],
    world: Mapping[str, Any],
    *,
    base_path: Path,
    package_path: Path,
) -> dict[str, Any]:
    seed = int(world["world_seed"])
    if seed not in PREREGISTERED_WORLDS or world.get("qualification_passed") is not True:
        raise ValueError("D2 world is outside the preregistered qualified set")
    config = copy.deepcopy(dict(base))
    config["pilot_id"] = f"work-ii-reaction-safety-matched-prior-d2-world-{seed}"
    config["world_seed"] = seed
    config["observation_noise_namespace"] = (
        f"work-ii-reaction-safety-matched-prior-d2-world-{seed}"
    )
    config["prior_arms"] = copy.deepcopy(world["prior_arms"])
    config["belief_checkpoint"]["held_out_queries"] = copy.deepcopy(
        world["held_out_queries"]
    )
    config["intervention"]["fixed_reference_context"] = copy.deepcopy(
        world["reference_context"]
    )
    config["intervention"]["q2_binding_sha256"] = str(
        world["world_package_sha256"]
    )
    config["qualification"].update(
        {
            "d2_preregistered_worlds": list(PREREGISTERED_WORLDS),
            "d2_world_owned_config": True,
            "d2_trigger_frozen_before_d1": True,
            "d2_trigger_basis": "q2_cross_world_temperature_direction_heterogeneity",
            "formal_r5_authorized": False,
        }
    )
    config["d2_binding"] = {
        "source_base_config": base_path.relative_to(ROOT).as_posix(),
        "source_base_config_sha256": file_sha256(base_path),
        "source_matched_prior_package": package_path.relative_to(ROOT).as_posix(),
        "source_matched_prior_package_sha256": file_sha256(package_path),
        "world_package_sha256": str(world["world_package_sha256"]),
        "world_qualification_report_sha256": str(world["qualification_report_sha256"]),
        "participant_outcome_used_for_world_selection": False,
        "world_order": list(PREREGISTERED_WORLDS),
    }
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--package", type=Path, default=DEFAULT_PACKAGE)
    args = parser.parse_args()
    base_path = args.base.resolve()
    package_path = args.package.resolve()
    base = _load(base_path)
    package = _load(package_path)
    worlds = {int(world["world_seed"]): world for world in package["worlds"]}
    outputs: list[dict[str, Any]] = []
    for seed in PREREGISTERED_WORLDS:
        config = build_world_config(
            base, worlds[seed], base_path=base_path, package_path=package_path
        )
        output = (
            ROOT
            / f"configs/benchmark/work_ii_reaction_safety_matched_prior_d2_world{seed}.json"
        )
        if output.exists():
            if _load(output) != config:
                raise ValueError(f"existing D2 config differs from reconstruction: {output}")
        else:
            write_json_atomic(output, config)
        outputs.append(
            {
                "world_seed": seed,
                "output": output.relative_to(ROOT).as_posix(),
                "world_package_sha256": config["d2_binding"]["world_package_sha256"],
                "aligned_claim": config["prior_arms"]["aligned_nominal"]
                ["initial_world_model"]["model"]["claim"]["expected_relation"],
            }
        )
    print(json.dumps({"outputs": outputs}, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
