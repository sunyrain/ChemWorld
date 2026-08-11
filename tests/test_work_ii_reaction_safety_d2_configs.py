from __future__ import annotations

import json
from pathlib import Path

from scripts.build_work_ii_reaction_safety_d2_configs import (
    PREREGISTERED_WORLDS,
    build_world_config,
)

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_d2_configs_are_world_owned_and_preregistered() -> None:
    base_path = (
        ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_d1_execution.json"
    )
    package_path = (
        ROOT / "configs/benchmark/work_ii_reaction_safety_matched_prior_package.json"
    )
    base = _load(base_path)
    package = _load(package_path)
    worlds = {int(world["world_seed"]): world for world in package["worlds"]}

    generated = {
        seed: build_world_config(
            base, worlds[seed], base_path=base_path, package_path=package_path
        )
        for seed in PREREGISTERED_WORLDS
    }

    assert tuple(generated) == (1, 4)
    for seed, config in generated.items():
        assert config["world_seed"] == seed
        assert config["prior_arms"] == worlds[seed]["prior_arms"]
        assert config["belief_checkpoint"]["held_out_queries"] == worlds[seed][
            "held_out_queries"
        ]
        assert config["intervention"]["fixed_reference_context"] == worlds[seed][
            "reference_context"
        ]
        assert config["campaign"] == base["campaign"]
        assert config["method_resources"] == base["method_resources"]
        assert config["provider"] == base["provider"]
        assert config["d2_binding"]["participant_outcome_used_for_world_selection"] is False

    aligned_1 = generated[1]["prior_arms"]["aligned_nominal"]["initial_world_model"][
        "model"
    ]["claim"]["expected_relation"]
    aligned_4 = generated[4]["prior_arms"]["aligned_nominal"]["initial_world_model"][
        "model"
    ]["claim"]["expected_relation"]
    assert "higher-temperature side" in aligned_1
    assert "lower-temperature side" in aligned_4
