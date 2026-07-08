from __future__ import annotations

import json
from pathlib import Path

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.cli import main
from chemworld.data.datasets import dataset_card, export_dataset
from chemworld.data.logging import load_jsonl
from chemworld.foundation.state import WorldState
from chemworld.runtime.domain_services import (
    ChemWorldDomainServices,
    make_chemworld_constitution,
)
from chemworld.runtime.kernels import OperationKernelRegistry, TaskRuntimeProfile
from chemworld.runtime.mechanisms import compile_mechanism_for_scenario
from chemworld.runtime.observation_services import ChemWorldObservationKernel
from chemworld.runtime.species import MechanismSpeciesView
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
from chemworld.world.observation_kernel import raw_signal
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
    assert spec["module_versions"]["observation"] == "0.4"


def test_world_layer_does_not_import_batch_core() -> None:
    world_dir = Path("src/chemworld/world")
    offenders = [
        path
        for path in world_dir.glob("*.py")
        if "chemworld.core.batch_reactor" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


def test_runtime_observation_service_is_separate_from_state_changing_services() -> None:
    domain_services = Path("src/chemworld/runtime/domain_services.py").read_text(
        encoding="utf-8"
    )
    observation_services = Path("src/chemworld/runtime/observation_services.py").read_text(
        encoding="utf-8"
    )

    assert "class ChemWorldObservationKernel" not in domain_services
    assert "class ChemWorldObservationKernel" in observation_services
    assert "score_observation" not in domain_services


def test_runtime_operation_recorder_is_separate_from_state_changing_services() -> None:
    domain_services = Path("src/chemworld/runtime/domain_services.py").read_text(
        encoding="utf-8"
    )
    record_services = Path("src/chemworld/runtime/record_services.py").read_text(
        encoding="utf-8"
    )

    assert "def _record" not in domain_services
    assert "class ChemWorldOperationRecorder" in record_services
    assert "material delta allowed or phase-ledger conserved" not in domain_services


def test_runtime_reaction_thermal_service_is_separate_from_domain_services() -> None:
    domain_services = Path("src/chemworld/runtime/domain_services.py").read_text(
        encoding="utf-8"
    )
    reaction_thermal_services = Path(
        "src/chemworld/runtime/reaction_thermal_services.py"
    ).read_text(encoding="utf-8")

    assert "def _integrate" not in domain_services
    assert "def _with_risk_and_pressure" not in domain_services
    assert "integrate_reaction_ode" not in domain_services
    assert "pressure_and_risk" not in domain_services
    assert "class ChemWorldReactionThermalServices" in reaction_thermal_services
    assert "integrate_reaction_ode" in reaction_thermal_services
    assert "pressure_and_risk" in reaction_thermal_services


def test_runtime_phase_separation_service_is_separate_from_domain_services() -> None:
    domain_services = Path("src/chemworld/runtime/domain_services.py").read_text(
        encoding="utf-8"
    )
    phase_separation_services = Path(
        "src/chemworld/runtime/phase_separation_services.py"
    ).read_text(encoding="utf-8")

    assert "def _phase_ledger" not in domain_services
    assert "def _mix_phases" not in domain_services
    assert "def _separate_phase" not in domain_services
    assert "partition_split" not in domain_services
    assert "class ChemWorldPhaseSeparationServices" in phase_separation_services
    assert "partition_split" in phase_separation_services
    assert "downstream_truth_values" in phase_separation_services


def test_runtime_electrochemical_service_is_separate_from_domain_services() -> None:
    domain_services = Path("src/chemworld/runtime/domain_services.py").read_text(
        encoding="utf-8"
    )
    electrochemical_services = Path(
        "src/chemworld/runtime/electrochemical_services.py"
    ).read_text(encoding="utf-8")

    assert "def _set_potential" not in domain_services
    assert "def _electrolyze" not in domain_services
    assert "run_electrolysis" not in domain_services
    assert "ElectrodeReactionSpec" not in domain_services
    assert "class ChemWorldElectrochemicalServices" in electrochemical_services
    assert "run_electrolysis" in electrochemical_services
    assert "ElectrodeReactionSpec" in electrochemical_services


def test_runtime_profile_requires_current_task_kernels_only() -> None:
    task = get_task("reaction-to-assay")
    profile = TaskRuntimeProfile.from_task(task)
    registry = OperationKernelRegistry.default()

    assert profile.world_law_id == "chemworld-physical-chemistry"
    assert "measure" in profile.required_kernels
    assert "add_extractant" not in profile.required_kernels
    assert all(registry.has(operation) for operation in profile.required_kernels)
    assert profile.is_operation_allowed("measure")
    assert not profile.is_operation_allowed("add_extractant")


def test_mechanism_compiler_supports_non_fixed_species_networks() -> None:
    compiled = compile_mechanism_for_scenario("electrochemical-conversion")

    assert compiled.mechanism_id == "electrochemical_conversion"
    assert "Ox" in compiled.species_index
    assert "Red" in compiled.species_index
    assert compiled.score_spec.reactant_species == "Ox"
    assert compiled.score_spec.product_species == "Red"
    assert compiled.mechanism_hash
    assert len(compiled.stoichiometric_matrix) == len(compiled.species_index)
    assert all(
        len(row) == len(compiled.network.reactions)
        for row in compiled.stoichiometric_matrix
    )


def test_runtime_species_view_uses_mechanism_roles_without_fixed_names() -> None:
    compiled = compile_mechanism_for_scenario("electrochemical-conversion")
    view = MechanismSpeciesView(compiled)
    state = WorldState(
        species_amounts={
            "Ox": 0.006,
            "Red": 0.003,
            "IsoRed": 0.001,
            "D": 0.0,
            "Coupled": 0.0,
        },
        volume_L=0.05,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="electrochemical_cell",
        metadata={"initial_Ox_mol": 0.010, "initial_reactant_mol": 0.010},
    )

    truth = view.truth_values(state)

    assert view.reactant_species(state) == "Ox"
    assert view.primary_target_species == "Red"
    assert view.primary_impurity_species == "IsoRed"
    assert view.target_amount(state) == 0.003
    assert view.impurity_amount(state) == 0.001
    assert truth["yield"] == pytest.approx(0.3)
    assert truth["conversion"] == pytest.approx(0.4)
    assert truth["selectivity"] == pytest.approx(0.75)


def test_domain_services_apply_mechanism_roles_for_reagent_and_electrolysis() -> None:
    compiled = compile_mechanism_for_scenario("electrochemical-conversion")
    services = ChemWorldDomainServices(
        load_chemworld_parameters("public-dev", seed=1),
        make_chemworld_constitution(),
        compiled,
    )
    state = WorldState(
        species_amounts={"Ox": 0.0, "Red": 0.0, "IsoRed": 0.0, "D": 0.0, "Coupled": 0.0},
        volume_L=0.05,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="electrochemical_cell",
        metadata={"solvent": 0, "catalyst": 0, "potential_V": 1.35, "current_mA": 80.0},
    )

    charged, add_record = services.apply_operation(
        state,
        {"operation": "add_reagent", "amount_mol": 0.010},
    )
    converted, electro_record = services.apply_operation(
        charged,
        {"operation": "electrolyze", "duration_s": 900.0},
    )

    assert add_record.preconditions["not_terminated"]
    assert charged.species_amounts["Ox"] == pytest.approx(0.010)
    assert "A" not in charged.species_amounts
    assert charged.metadata["initial_Ox_mol"] == pytest.approx(0.010)
    assert converted.species_amounts["Ox"] < charged.species_amounts["Ox"]
    assert converted.species_amounts["Red"] > charged.species_amounts["Red"]
    assert converted.species_amounts["IsoRed"] >= charged.species_amounts["IsoRed"]
    assert abs(electro_record.state_delta_summary["actual_current_A"]) > 0.0


def test_observation_kernel_scores_non_fixed_mechanism_species() -> None:
    compiled = compile_mechanism_for_scenario("electrochemical-conversion")
    kernel = ChemWorldObservationKernel(
        make_chemworld_constitution(),
        objective="balanced",
        compiled_mechanism=compiled,
    )
    state = WorldState(
        species_amounts={
            "Ox": 0.004,
            "Red": 0.004,
            "IsoRed": 0.001,
            "D": 0.001,
            "Coupled": 0.0,
        },
        volume_L=0.05,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="electrochemical_cell",
        metadata={"initial_Ox_mol": 0.010, "initial_reactant_mol": 0.010},
    )

    truth = kernel._truth_values(state)

    assert truth["yield"] == pytest.approx(0.4)
    assert truth["conversion"] == pytest.approx(0.6)
    assert truth["byproduct_signal"] == pytest.approx(0.2)
    assert truth["degradation_warning"] == pytest.approx(0.1)


def test_env_runtime_v2_info_contains_kernel_transaction_and_mechanism() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        _, reset_info = env.reset(seed=0)
        _, _, _, _, step_info = env.step(
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}
        )

        assert reset_info["mechanism_id"] == "simple_batch_reaction"
        assert reset_info["mechanism_hash"]
        assert step_info["kernel_id"] == "chemworld.operation.add_solvent"
        assert step_info["transaction_status"] == "committed"
        assert step_info["rollback_reason"] is None
        assert "process" in step_info["affected_ledgers"]
        assert step_info["world_events"][0]["event_type"] == "operation_applied"
    finally:
        env.close()


def test_typed_phase_ledger_tracks_state_replacements() -> None:
    state = WorldState(
        species_amounts={"A": 1.0, "P": 0.0},
        volume_L=0.01,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="reactor",
    )
    updated = state.replace(species_amounts={"A": 0.2, "P": 0.8})

    assert updated.phases is not None
    assert updated.phases.total_amounts_mol() == {"A": 0.2, "P": 0.8}
    assert updated.process is not None
    assert updated.process.time_s == updated.ledger.time_s


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
    assert "spectra" in final_assay["raw_signal_schema"]["properties"]
    assert "yield" in final_assay["observable_keys"]


def test_virtual_instrument_signals_are_plot_ready() -> None:
    values = {
        "yield": 0.62,
        "selectivity": 0.82,
        "conversion": 0.76,
        "byproduct_signal": 0.12,
        "degradation_warning": 0.06,
        "purity": 0.88,
        "recovery": 0.70,
        "phase_ratio": 0.55,
        "impurity_signal": 0.08,
        "solvent_loss": 0.04,
        "process_mass_balance_error": 0.02,
        "distillate_purity": 0.91,
        "flow_conversion": 0.0,
        "energy_efficiency": 0.0,
    }

    hplc = raw_signal("hplc", values)
    assert hplc["kind"] == "hplc_chromatogram"
    assert len(hplc["time_min"]) == len(hplc["intensity"]) >= 100
    assert hplc["peaks"][1]["assignment"] == "P_proxy"

    uvvis = raw_signal("uvvis", values)
    assert uvvis["kind"] == "uvvis_spectrum"
    assert len(uvvis["wavelength_nm"]) == len(uvvis["absorbance"]) >= 100

    final_packet = raw_signal("final_assay", values)
    assert final_packet["kind"] == "final_assay_packet"
    assert {"hplc", "gc", "uvvis", "ir", "nmr"} <= set(final_packet["spectra"])


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
        encoding="utf-8-sig",
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
