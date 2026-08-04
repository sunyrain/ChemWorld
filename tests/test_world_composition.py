from __future__ import annotations

import gymnasium as gym
import pytest

import chemworld
from chemworld.world.composition import WorldCompositionError


def _request() -> dict[str, object]:
    return {
        "schema_version": "chemworld-world-composition-0.1",
        "composition_id": "composed-reaction-assay-test",
        "world_split": "public-dev",
        "components": [
            {"kind": "reaction", "role": "transformation", "parameters": {}},
            {"kind": "thermal", "role": "temperature-and-energy", "parameters": {}},
            {"kind": "observation", "role": "public-measurement", "parameters": {}},
        ],
        "task": {
            "budget": 8,
            "resources": {"operation_budget": 8},
            "description": "Declarative reaction-world test.",
        },
    }


def test_compile_world_composition_exposes_complete_public_surface() -> None:
    compiled = chemworld.compile_world_composition(_request())
    surface = compiled.to_public_dict()

    assert compiled.task_spec.task_id == "composed-reaction-assay-test"
    assert compiled.scenario_spec.scenario_id == "reaction-to-assay"
    assert [item["kind"] for item in surface["world"]["components"]] == [
        "reaction",
        "thermal",
        "observation",
    ]
    assert set(surface["task"]["operations"]) == set(
        compiled.task_spec.allowed_operations
    )
    assert set(surface["task"]["instruments"]) == set(
        compiled.task_spec.allowed_instruments
    )
    assert surface["task"]["resources"]["operation_budget"] == 8
    assert surface["task"]["termination"] == "final-assay-or-budget"
    assert surface["task"]["evaluation"]["metrics"] == [
        "final_assay_score",
        "trajectory_validity",
    ]


@pytest.mark.parametrize(
    ("component_kinds", "scenario_id"),
    (
        (("reaction", "thermal", "observation"), "reaction-to-assay"),
        (
            ("reaction", "thermal", "phase", "separation", "observation"),
            "reaction-to-purification",
        ),
        (("phase", "separation", "observation"), "partition-discovery"),
        (
            ("reaction", "thermal", "crystallization", "observation"),
            "reaction-to-crystallization",
        ),
        (
            ("reaction", "thermal", "distillation", "observation"),
            "reaction-to-distillation",
        ),
        (
            ("reaction", "thermal", "continuous_flow", "observation"),
            "flow-reaction-optimization",
        ),
        (
            ("reaction", "electrochemistry", "observation"),
            "electrochemical-conversion",
        ),
        (("phase", "observation"), "equilibrium-characterization"),
    ),
)
def test_registered_component_patterns_compile(
    component_kinds: tuple[str, ...],
    scenario_id: str,
) -> None:
    request = _request()
    request["composition_id"] = f"composed-{scenario_id}-test"
    request["components"] = [
        {"kind": kind, "role": kind, "parameters": {}} for kind in component_kinds
    ]

    compiled = chemworld.compile_world_composition(request)

    assert compiled.scenario_spec.scenario_id == scenario_id
    assert set(compiled.spec.component_kinds) == set(component_kinds)
    assert "terminate" in compiled.task_spec.allowed_operations
    assert "measure" in compiled.task_spec.allowed_operations
    assert "final_assay" in compiled.task_spec.allowed_instruments


def test_composed_world_runs_complete_lifecycle() -> None:
    env = gym.make("ChemWorld", composition=_request(), seed=4)
    try:
        _, info = env.reset(seed=4)
        assert info["task_id"] == "composed-reaction-assay-test"
        assert info["composition"] == env.unwrapped.compiled_composition.to_public_dict()
        actions = (
            {"operation": "add_solvent", "volume_L": 0.03, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.01},
            {
                "operation": "add_catalyst",
                "catalyst_amount_mol": 0.0002,
                "catalyst": 1,
            },
            {
                "operation": "heat",
                "target_temperature_K": 385.0,
                "duration_s": 1200.0,
                "stirring_speed_rpm": 700.0,
            },
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        )
        for action in actions:
            _, _, terminated, truncated, step_info = env.step(action)
            assert step_info["transaction_status"] == "committed"
        assert terminated
        assert not truncated
        assert step_info["leaderboard_score"] is not None
    finally:
        env.close()


def test_unregistered_component_combination_fails_before_execution() -> None:
    request = _request()
    request["components"] = [
        {"kind": "distillation", "role": "fractionation", "parameters": {}},
        {"kind": "observation", "role": "measurement", "parameters": {}},
    ]

    with pytest.raises(WorldCompositionError, match="not registered"):
        chemworld.compile_world_composition(request)


def test_fixed_task_and_composition_are_mutually_exclusive() -> None:
    with pytest.raises(ValueError, match="mutually exclusive"):
        gym.make(
            "ChemWorld",
            task_id="reaction-to-assay",
            composition=_request(),
        )


def test_composed_world_rejects_reset_scenario_override() -> None:
    env = gym.make("ChemWorld", composition=_request(), seed=0)
    try:
        with pytest.raises(ValueError, match="unavailable for composed worlds"):
            env.reset(options={"scenario_id": "reaction-to-distillation"})
    finally:
        env.close()
