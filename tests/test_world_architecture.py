from __future__ import annotations

import json
from pathlib import Path

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.cli import main
from chemworld.data.datasets import dataset_card, export_dataset
from chemworld.data.logging import load_jsonl
from chemworld.foundation.state import WorldState
from chemworld.schemas import (
    ACTION_SCHEMA,
    MANIFEST_SCHEMA,
    OBSERVATION_SCHEMA,
    RECIPE_SCHEMA,
    SCENARIO_SCHEMA,
    TASK_SCHEMA,
    TRAJECTORY_SCHEMA,
    load_schema_file,
    validate_action_schema,
    validate_recipe_schema,
)
from chemworld.tasks import get_task, list_tasks
from chemworld.validation import validate_action
from chemworld.world import (
    get_scenario_card,
    instrument_contracts,
    list_scenarios,
    load_chemworld_parameters,
    world_law_spec,
)
from chemworld.world.phase_kernel import partition_split
from chemworld.world.reaction_kernel import integrate_reaction_ode
from chemworld.world.state_factory import initial_chemworld_state
from chemworld.world.thermal_kernel import pressure_and_risk


def test_world_law_contains_professional_contracts() -> None:
    spec = world_law_spec().to_dict()
    assert spec["law_version"] == "chemworld-physical-chemistry"
    assert "reaction" in spec["module_versions"]
    assert "thermal_energy_balance" in spec["transition_kernel_registry"]
    assert "crystallization" in spec["transition_kernel_registry"]
    assert "distillation" in spec["transition_kernel_registry"]
    assert "continuous_flow" in spec["transition_kernel_registry"]
    assert "electrochemistry" in spec["transition_kernel_registry"]
    assert "hplc" in spec["instrument_registry"]
    assert "material_conservation" in spec["constitution_rules"]
    assert spec["backend"]["backend_id"] == "semi_mechanistic"
    module_ids = {
        module["module_id"] for module in spec["ontology_registry"]["modules"]
    }
    assert {
        "crystallization",
        "distillation",
        "continuous_flow",
        "electrochemistry",
    } <= module_ids
    assert spec["module_versions"]["reaction"] == "0.3"
    assert spec["module_versions"]["observation"] == "0.3"


def test_world_layer_does_not_import_batch_core() -> None:
    world_dir = Path("src/chemworld/world")
    offenders = [
        path
        for path in world_dir.glob("*.py")
        if "chemworld.core.batch_reactor" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


def test_world_kernels_are_executable_not_metadata_only() -> None:
    world = load_chemworld_parameters("public-dev", seed=1)
    state = initial_chemworld_state().replace(
        species_amounts={
            "A": 0.01,
            "P": 0.0,
            "B": 0.0,
            "D": 0.0,
            "E": 0.0,
            "Cat_active": 0.0002,
            "Cat_dead": 0.0,
        },
        volume_L=0.025,
        metadata={
            **initial_chemworld_state().metadata,
            "initial_A_mol": 0.01,
            "solvent": 1,
            "catalyst": 1,
        },
    )
    result = integrate_reaction_ode(
        state=state,
        world=world,
        duration_s=900.0,
        target_temperature_K=380.0,
        heat=True,
        stirring_speed_rpm=700.0,
    )
    assert result is not None
    assert result.species_amounts["A"] < state.species_amounts["A"]
    assert result.species_amounts["P"] >= 0.0
    pressure, risk = pressure_and_risk(
        state=state.replace(
            species_amounts=result.species_amounts,
            temperature_K=result.temperature_K,
        ),
        solvent_risks=world.solvent_risks,
    )
    assert pressure > 0.0
    assert 0.0 <= risk <= 1.0
    split = partition_split(
        product_mol=0.005,
        impurity_mol=0.001,
        solvent=1,
        temperature_K=298.15,
        duration_s=180.0,
        stirring_speed_rpm=700.0,
        organic_volume_L=0.015,
        aqueous_volume_L=0.025,
    )
    assert split["organic_product_mol"] + split["aqueous_product_mol"] == 0.005


def test_scenarios_are_first_class_and_share_world_law() -> None:
    scenarios = list_scenarios()
    assert scenarios
    assert {scenario.world_law_id for scenario in scenarios} == {
        "chemworld-physical-chemistry"
    }
    card = get_scenario_card("reaction-to-purification")
    assert card["family"] == "reaction_separation"
    assert "separation" in card["allowed_module_tags"]
    crystallization_card = get_scenario_card("reaction-to-crystallization")
    assert crystallization_card["family"] == "reaction_crystallization"
    assert "crystallization" in crystallization_card["allowed_module_tags"]
    assert {task.world_law_id for task in list_tasks()} == {"chemworld-physical-chemistry"}


def test_instrument_contracts_expose_observation_layers() -> None:
    contracts = instrument_contracts()
    final_assay = contracts["final_assay"].to_dict()
    assert final_assay["requires_terminated"]
    assert final_assay["destructive"]
    assert "processed_estimate_schema" in final_assay
    assert "yield" in final_assay["observable_keys"]


def test_action_and_recipe_public_validation() -> None:
    action = {"operation": "measure", "instrument": "final_assay"}
    assert validate_action_schema(action).valid
    task = get_task("reaction-to-assay")
    result = validate_action(action, task.to_dict())
    assert result.valid
    blocked = validate_action(
        {"operation": "add_extractant", "volume_L": 0.01},
        get_task("reaction-optimization-standard").to_dict(),
    )
    assert not blocked.valid
    recipe = {"steps": [{"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}]}
    assert validate_recipe_schema(recipe).valid


def test_packaged_schema_files_match_runtime_constants() -> None:
    expected = {
        "action": ACTION_SCHEMA,
        "manifest": MANIFEST_SCHEMA,
        "observation": OBSERVATION_SCHEMA,
        "recipe": RECIPE_SCHEMA,
        "scenario": SCENARIO_SCHEMA,
        "task": TASK_SCHEMA,
        "trajectory": TRAJECTORY_SCHEMA,
    }
    for schema_id, schema in expected.items():
        assert load_schema_file(schema_id) == schema


def test_world_state_does_not_expose_mutable_references() -> None:
    source_metadata = {"nested": {"value": 1}}
    state = WorldState(
        species_amounts={"A": 1.0},
        volume_L=0.01,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="reactor",
        metadata=source_metadata,
    )
    source_metadata["nested"]["value"] = 99
    exported = state.to_dict()
    exported["metadata"]["nested"]["value"] = 123
    assert state.metadata["nested"]["value"] == 1


def test_env_info_logs_campaign_experiment_operation_and_render() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0, render_mode="ansi")
    try:
        _, info = env.reset(seed=0)
        assert info["scenario"]["scenario_id"] == "reaction-to-assay"
        _, _, _, _, step_info = env.step(
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}
        )
        assert step_info["campaign_id"]
        assert step_info["experiment_index"] == 0
        assert step_info["operation_id"] == 1
        assert "cost_components" in step_info
        task_info = env.unwrapped.task_info()
        assert task_info["operation_contracts"]["add_extractant"]["module"] == "separation"
        rendered = env.render()
        assert isinstance(rendered, str)
        assert "ChemWorld" in rendered
        assert "ledger:" in rendered
    finally:
        env.close()


def test_validator_rejects_invalid_payload_bounds() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        _, _ = env.reset(seed=0)
        bad = env.unwrapped.operation_validator.validate(
            {"operation": "add_solvent", "volume_L": 0.2, "solvent": 1},
            env.unwrapped._state,
        )
        assert not bad.is_valid
        assert "payload_bounds:volume_L" in bad.invalid_reasons
        assert "payload_bounds:total_volume_L" in bad.invalid_reasons
    finally:
        env.close()


def test_scenario_generator_uses_initial_state_seed_and_profile() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    try:
        _, info = env.reset(seed=0)
        assert info["scenario"]["initial_state_seed"] == 7
        assert info["scenario"]["parameter_profile"] == "downstream_processing"
        assert env.unwrapped._state.metadata["scenario_id"] == "reaction-to-purification"
        assert "initial_condition_jitter" in env.unwrapped._state.metadata
    finally:
        env.close()


def test_cli_scenarios_validation_render_and_dataset(tmp_path, capsys) -> None:
    action_path = tmp_path / "action.json"
    action_path.write_text(
        json.dumps({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}),
        encoding="utf-8",
    )
    recipe_path = tmp_path / "recipe.json"
    recipe_path.write_text(
        json.dumps({"steps": [{"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}]}),
        encoding="utf-8",
    )
    trajectory = tmp_path / "run.jsonl"
    exported = tmp_path / "dataset.jsonl"

    main(["scenarios", "list"])
    main(["scenarios", "show", "reaction-optimization"])
    main(["validate-action", "--task", "reaction-to-assay", "--action", str(action_path)])
    main(["validate-recipe", "--task", "reaction-to-assay", "--recipe", str(recipe_path)])
    main(["render", "--task", "reaction-to-assay", "--actions", str(action_path)])
    main(["run", "--task", "reaction-to-assay", "--agent", "random", "--output", str(trajectory)])
    main(
        [
            "datasets",
            "export",
            "--submission",
            str(trajectory),
            "--format",
            "jsonl",
            "--output",
            str(exported),
        ]
    )
    main(["datasets", "card", "--dataset", str(exported)])
    output = capsys.readouterr().out
    assert "reaction-optimization" in output
    assert "compiled_step_count" in output
    assert "ChemWorld" in output
    assert exported.exists()
    records = load_jsonl(exported)
    assert records[0]["campaign_id"]
    card = dataset_card(exported)
    assert card["record_count"] == len(records)
    exported_result = export_dataset(trajectory, output=tmp_path / "copy.jsonl", format="jsonl")
    assert exported_result.record_count == len(records)
