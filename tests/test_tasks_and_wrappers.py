from __future__ import annotations

import gymnasium as gym
import numpy as np

import chemworld  # noqa: F401
from chemworld.action_codec import ActionCodec
from chemworld.agents.base import HistoryRecord
from chemworld.agents.event import ScriptedChemistryAgent
from chemworld.operation_validator import OperationValidator
from chemworld.runtime import make_chemworld_constitution
from chemworld.tasks import get_task, get_task_card, list_tasks
from chemworld.world.scoring import (
    TaskScoringContract,
    score_observation,
    task_score_observation,
)
from chemworld.world.state_factory import initial_chemworld_state
from chemworld.wrappers import (
    ActionMaskWrapper,
    NaNObservationWrapper,
    SafetyCostWrapper,
    validate_event_action,
)


def test_builtin_tasks_are_instantiable() -> None:
    task_ids = {task.task_id for task in list_tasks()}
    assert {
        "reaction-to-assay",
        "reaction-optimization-standard",
        "reaction-safety-constrained",
        "public-private-generalization",
        "reaction-mechanism-explanation",
        "reaction-to-crystallization",
        "reaction-to-distillation",
        "flow-reaction-optimization",
        "electrochemical-conversion",
    } <= task_ids
    task = get_task("reaction-optimization-standard")
    assert task.env_id == "ChemWorld"
    assert task.world_law_id == "chemworld-physical-chemistry"
    assert task.episode_mode == "campaign"
    assert task.termination_policy == "budget"
    assert task.env_kwargs(seed=7)["seed"] == 7
    assert "hplc" in task.allowed_instruments
    card = get_task_card("reaction-optimization-standard")
    assert card["task_id"] == "reaction-optimization-standard"
    assert card["world_law_id"] == "chemworld-physical-chemistry"
    assert "baseline_reference_scores" in card
    assert "failure_modes" in card
    assay_task = get_task("reaction-to-assay")
    assert assay_task.episode_mode == "single_experiment"
    assert assay_task.termination_policy == "final-assay-or-budget"


def test_all_tasks_share_one_world_law() -> None:
    tasks = list_tasks()
    assert {task.env_id for task in tasks} == {"ChemWorld"}
    assert {task.world_law_id for task in tasks} == {"chemworld-physical-chemistry"}
    assert "reaction-to-purification" in {task.task_id for task in tasks}
    assert "partition-discovery" in {task.task_id for task in tasks}
    assert "purity-yield-tradeoff" in {task.task_id for task in tasks}
    assert "reaction-to-crystallization" in {task.task_id for task in tasks}
    assert "flow-reaction-optimization" in {task.task_id for task in tasks}


def test_task_specific_scoring_contracts_are_explicit() -> None:
    values = {
        "yield": 0.40,
        "selectivity": 0.75,
        "conversion": 0.60,
        "cost": 0.10,
        "safety_risk": 0.20,
        "purity": 0.90,
        "recovery": 0.70,
        "process_mass_balance_error": 0.02,
    }
    reaction_contract = TaskScoringContract.from_success_metrics(
        objective="balanced",
        success_metrics=("score", "yield", "selectivity"),
    )
    purification_contract = TaskScoringContract.from_success_metrics(
        objective="balanced",
        success_metrics=("score", "purity", "recovery", "process_mass_balance_error"),
    )

    reaction_score = score_observation(
        objective="balanced",
        product_yield=0.40,
        selectivity=0.75,
        conversion=0.60,
        cost=0.10,
        safety_risk=0.20,
    )
    expected_purification = 0.35 * reaction_score + 0.35 * 0.90 + 0.25 * 0.70 - 0.10 * 0.02

    assert reaction_contract.score_family == "reaction"
    assert purification_contract.score_family == "purification"
    assert task_score_observation(contract=reaction_contract, values=values) == (
        reaction_score
    )
    assert task_score_observation(contract=purification_contract, values=values) == (
        expected_purification
    )


def test_env_task_info_exposes_scoring_contract() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    try:
        _, info = env.reset(seed=0)
        contract = info["scoring_contract"]
        assert contract["objective"] == "balanced"
        assert contract["score_family"] == "purification"
        assert "purity" in contract["component_weights"]
        assert "process_mass_balance_error" in contract["success_metrics"]
    finally:
        env.close()


def test_action_mask_wrapper_reports_valid_operations() -> None:
    env = ActionMaskWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        _, info = env.reset(seed=0)
        assert "action_mask" in info
        assert "add_solvent" in info["valid_operations"]
        assert "heat" not in info["valid_operations"]

        validation = validate_event_action({"operation": "heat"}, env)
        assert not validation["valid"]
        assert not validation["preconditions"]["has_volume"]

        _, _, _, _, step_info = env.step(
            {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1}
        )
        assert "heat" not in step_info["valid_operations"]
        _, _, _, _, step_info = env.step({"operation": "add_reagent", "amount_mol": 0.01})
        assert "heat" in step_info["valid_operations"]
    finally:
        env.close()


def test_action_codec_roundtrip_vector() -> None:
    codec = ActionCodec()
    action = {
        "operation": "heat",
        "target_temperature_K": 386.0,
        "duration_s": 900.0,
        "instrument": "hplc",
    }
    vector = codec.encode_vector(action)
    decoded = codec.decode_vector(vector)
    assert decoded["operation"] == "heat"
    assert decoded["instrument"] == "hplc"
    assert decoded["target_temperature_K"] == 386.0
    assert decoded["duration_s"] == 900.0
    process_vector = codec.encode_vector(
        {
            "operation": "distill",
            "target_temperature_K": 360.0,
            "duration_s": 900.0,
            "reflux_ratio": 2.5,
        }
    )
    process_decoded = codec.decode_vector(process_vector)
    assert process_decoded["operation"] == "distill"
    assert process_decoded["reflux_ratio"] == 2.5


def test_action_codec_accepts_common_recipe_aliases() -> None:
    codec = ActionCodec()
    catalyst_action = codec.canonicalize(
        {"operation": "add_catalyst", "catalyst": 2, "amount_mol": 0.0004}
    )
    assert catalyst_action["catalyst_amount_mol"] == 0.0004

    heat_action = codec.canonicalize(
        {
            "operation": "heat",
            "temperature_K": 350.0,
            "duration_s": 1200.0,
            "stirring_rpm": 800.0,
        }
    )
    assert heat_action["target_temperature_K"] == 350.0
    assert heat_action["stirring_speed_rpm"] == 800.0

    phase_action = codec.canonicalize({"operation": "separate_phase", "phase": "organic"})
    assert phase_action["target_phase"] == "organic"


def test_action_mask_is_task_aware() -> None:
    reaction_env = ActionMaskWrapper(
        gym.make("ChemWorld", task_id="reaction-optimization-standard", seed=0)
    )
    purification_env = ActionMaskWrapper(
        gym.make("ChemWorld", task_id="reaction-to-purification", seed=0)
    )
    try:
        _, reaction_info = reaction_env.reset(seed=0)
        _, purification_info = purification_env.reset(seed=0)
        assert "add_extractant" not in reaction_info["valid_operations"]
        assert "add_extractant" not in purification_info["valid_operations"]

        validation = validate_event_action({"operation": "add_extractant"}, reaction_env)
        assert not validation["valid"]
        assert not validation["preconditions"]["operation_allowed_by_task"]
        assert "operation_allowed_by_task" in validation["invalid_reasons"]

        purification_env.step({"operation": "add_solvent", "volume_L": 0.02, "solvent": 1})
        purification_env.step({"operation": "add_reagent", "amount_mol": 0.01})
        _, _, _, _, info = purification_env.step(
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.010}
        )
        assert "add_extractant" in info["valid_operations"]
    finally:
        reaction_env.close()
        purification_env.close()


def test_safety_cost_wrapper_preserves_gym_return_shape() -> None:
    env = SafetyCostWrapper(gym.make("ChemWorld", budget=2, seed=0))
    try:
        observation, info = env.reset(seed=0)
        assert isinstance(observation, dict)
        assert info["cost_signal"] == 0.0
        result = env.step({"operation": "heat", "duration_s": 100.0})
        assert len(result) == 5
        _, reward, _, _, step_info = result
        assert isinstance(reward, float)
        assert step_info["cost_signal"] > 0.0
        assert "precondition_failure" in step_info["cost_components"]
        assert step_info["constraint_budget_remaining"] <= 1.0
    finally:
        env.close()


def test_task_safety_limit_reaches_constraint_flags() -> None:
    env = gym.make("ChemWorld", task_id="reaction-safety-constrained", seed=0)
    try:
        _, info = env.reset(seed=0)
        assert info["safety_limit"] == 0.35
        actions = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 0},
            {"operation": "add_reagent", "amount_mol": 0.030},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.0003, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 500.0,
                "duration_s": 2400.0,
                "stirring_speed_rpm": 1100.0,
            },
        ]
        step_info = {}
        for action in actions:
            _, _, _, _, step_info = env.step(action)
        assert step_info["safety_limit"] == 0.35
        assert (
            step_info["constraint_flags"]["unsafe"]
            == step_info["constraint_flags"]["unsafe_by_task_limit"]
        )
    finally:
        env.close()


def test_operation_validator_enforces_instrument_policy() -> None:
    validator = OperationValidator(
        constitution=make_chemworld_constitution(),
        allowed_operations={"measure"},
        allowed_instruments={"uvvis"},
    )
    state = initial_chemworld_state().replace(volume_L=0.02)
    allowed = validator.validate({"operation": "measure", "instrument": "uvvis"}, state)
    blocked = validator.validate({"operation": "measure", "instrument": "hplc"}, state)
    assert allowed.preconditions["instrument_allowed_by_task"]
    assert not blocked.preconditions["instrument_allowed_by_task"]
    assert "instrument_allowed_by_task" in blocked.invalid_reasons


def test_process_preconditions_are_stateful() -> None:
    env = ActionMaskWrapper(gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0))
    try:
        _, info = env.reset(seed=0)
        assert "filter_crystals" not in info["valid_operations"]
        for action in (
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 385.0,
                "duration_s": 1500.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "seed_crystals", "seed_mass_g": 0.006},
            {
                "operation": "cool_crystallize",
                "target_temperature_K": 278.15,
                "duration_s": 1200.0,
            },
        ):
            _, _, _, _, info = env.step(action)
        assert "filter_crystals" in info["valid_operations"]
    finally:
        env.close()


def test_nan_observation_wrapper_returns_vector_with_mask() -> None:
    env = NaNObservationWrapper(gym.make("ChemWorld", task_id="reaction-to-assay", seed=0))
    try:
        observation, _ = env.reset(seed=0)
        width = len(env.observation_keys)
        assert observation.shape == (width * 2,)
        assert np.any(observation[:width] == -1.0)
        assert set(np.unique(observation[width:])).issubset({0.0, 1.0})
    finally:
        env.close()


def test_purification_task_reaches_downstream_assay() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=2)
    try:
        obs, info = env.reset(seed=2)
        del obs
        assert "separate_phase" in info["allowed_operations"]
        actions = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 385.0,
                "duration_s": 1500.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "quench"},
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
            {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.018},
            {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 850.0},
            {"operation": "settle", "duration_s": 420.0},
            {"operation": "separate_phase", "target_phase": "organic"},
            {"operation": "wash", "wash_volume_L": 0.008},
            {"operation": "dry"},
            {"operation": "concentrate", "duration_s": 600.0},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        final_info = {}
        observation = {}
        for action in actions:
            observation, _, terminated, _, final_info = env.step(action)
        assert terminated
        assert final_info["leaderboard_score"] is not None
        assert float(observation["purity"][0]) >= 0.0
        assert float(observation["recovery"][0]) >= 0.0
        assert final_info["processed_estimate"]["process_mass_balance_error"] >= 0.0
    finally:
        env.close()


def test_purification_recipe_accepts_user_facing_aliases() -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-purification", seed=1)
    try:
        env.reset(seed=1)
        actions = [
            {"operation": "add_solvent", "volume_L": 0.03, "solvent": 1},
            {"operation": "add_reagent", "amount_mol": 0.012},
            {"operation": "add_catalyst", "catalyst": 2, "amount_mol": 0.0004},
            {
                "operation": "heat",
                "temperature_K": 350.0,
                "duration_s": 1200.0,
                "stirring_rpm": 800.0,
            },
            {"operation": "quench"},
            {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.012},
            {"operation": "add_extractant", "volume_L": 0.02, "solvent": 2},
            {"operation": "mix", "duration_s": 120.0, "stirring_rpm": 600.0},
            {"operation": "settle", "duration_s": 300.0},
            {"operation": "separate_phase", "phase": "organic"},
            {"operation": "wash", "phase": "organic", "volume_L": 0.01},
            {"operation": "dry", "phase": "organic", "duration_s": 300.0},
            {
                "operation": "concentrate",
                "phase": "organic",
                "target_volume_L": 0.008,
                "duration_s": 300.0,
            },
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        final_info = {}
        for action in actions:
            _, _, terminated, _, final_info = env.step(action)
            assert not final_info["constraint_flags"]["precondition_failed"]
        assert terminated
        assert final_info["leaderboard_score"] is not None
    finally:
        env.close()


def _run_scripted_task(task_id: str) -> tuple[dict[str, np.ndarray], dict[str, object]]:
    task = get_task(task_id)
    env = gym.make("ChemWorld", task_id=task_id, seed=0)
    try:
        observation, info = env.reset(seed=0)
        agent = ScriptedChemistryAgent()
        agent.reset(info, seed=0)
        history: list[HistoryRecord] = []
        step_info: dict[str, object] = {}
        assay_observation: dict[str, np.ndarray] | None = None
        assay_info: dict[str, object] | None = None
        for _ in range(task.budget):
            action = agent.act(history)
            observation, reward, terminated, truncated, step_info = env.step(action)
            if action.get("operation") == "measure" and action.get("instrument") == "final_assay":
                assay_observation = observation
                assay_info = step_info
            history.append(
                HistoryRecord(
                    step=len(history) + 1,
                    action=action,
                    observation=observation,
                    reward=reward,
                    info=step_info,
                )
            )
            if terminated or truncated:
                break
        assert not any(
            record.info.get("constraint_flags", {}).get("precondition_failed", False)
            for record in history
        )
        return assay_observation or observation, assay_info or step_info
    finally:
        env.close()


def test_year2_process_tasks_reach_assay_with_scripted_agent() -> None:
    crystallization_obs, crystallization_info = _run_scripted_task(
        "reaction-to-crystallization"
    )
    assert crystallization_info["leaderboard_score"] is not None
    assert float(crystallization_obs["crystal_yield"][0]) >= 0.0
    assert float(crystallization_obs["crystal_purity"][0]) >= 0.0

    distillation_obs, distillation_info = _run_scripted_task("reaction-to-distillation")
    assert distillation_info["leaderboard_score"] is not None
    assert float(distillation_obs["distillate_purity"][0]) >= 0.0
    assert float(distillation_obs["distillate_recovery"][0]) >= 0.0


def test_flow_and_electrochemistry_campaigns_produce_process_assays() -> None:
    flow_obs, _ = _run_scripted_task("flow-reaction-optimization")
    electro_obs, _ = _run_scripted_task("electrochemical-conversion")
    assert float(flow_obs["flow_conversion"][0]) >= 0.0
    assert float(electro_obs["electrochemical_selectivity"][0]) >= 0.0
    assert float(electro_obs["energy_efficiency"][0]) >= 0.0


def test_electrolysis_info_reports_charge_and_overpotential() -> None:
    env = gym.make("ChemWorld", task_id="electrochemical-conversion", seed=0)
    try:
        env.reset()
        sequence = [
            {"operation": "add_solvent", "volume_L": 0.026, "solvent": 1},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "set_potential", "potential_V": 1.15, "current_mA": 75.0},
            {"operation": "electrolyze", "duration_s": 1800.0},
        ]
        info = {}
        for action in sequence:
            _, _, _, _, info = env.step(action)
        summary = info["state_delta_summary"]
        assert summary["charge_C"] > 0.0
        assert summary["faradaic_charge_C"] > 0.0
        assert "overpotential_V" in summary
        assert "equilibrium_potential_V" in summary
        assert 0.0 <= summary["faradaic_efficiency"] <= 1.0
    finally:
        env.close()
