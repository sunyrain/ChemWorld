"""Observed P entry regressions: anonymity, dynamic prose and lifecycle count."""

import json
from dataclasses import replace

import gymnasium as gym
from scripts import run_work_ii_p_gate as p
from scripts.work_ii_p_public import presentation

from chemworld.foundation.state import PhaseLedger, PhaseRecord


def test_p_public_projection_covers_initial_tool_and_dynamic_task():
    env = gym.make(
        "ChemWorld",
        task_id=p.TASK,
        seed=0,
        budget_override=720,
        episode_mode_override="campaign",
        campaign_resource_card=p.resources(),
    )
    try:
        env.reset(seed=0)
        original = env.unwrapped.task_info()["material_catalog"]
        assert "ethanol" in json.dumps(original).lower()  # Retained native surface.
        with presentation(None, p.GOAL, 12):
            result = p.check_public(env.unwrapped.task_info(), None)
            assert result["anonymous"] and result["dossier_delivered"]
            assert result["contract"]["experiment_lifecycle"]["planned_complete_experiments"] == 12
            prompt = env.unwrapped.task_prompt()
            text = json.dumps(prompt).lower()
            assert "single-experiment task" not in text
            assert "ethanol" not in text
            assert prompt["task_goal"] == p.GOAL
            assert prompt["recommended_strategy"] == []
        assert env.unwrapped.task_info()["material_catalog"] == original
    finally:
        env.close()


def test_p_adapter_leaves_other_live_task_contracts_alone():
    env = gym.make("ChemWorld", task_id="reaction-to-crystallization", seed=0)
    try:
        env.reset(seed=0)
        original = env.unwrapped.task_prompt()
        with presentation(None, p.GOAL, 12):
            assert env.unwrapped.task_prompt() == original
    finally:
        env.close()


def test_scoped_dossier_excludes_private_binding_and_keeps_fixed_permutation():
    asset = p.read(p.ROOT / "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json")
    world = p.frozen_world_truths(asset)[0]
    assert p.public_dossier(asset, world, "Opaque") is None
    aligned = p.public_dossier(asset, world, "Aligned")
    wrong = p.public_dossier(asset, world, "MisIndexed")
    assert aligned["scope"] == wrong["scope"]
    for i, source in enumerate((2, 0, 3, 1)):
        assert wrong["extractants"][i]["anchors"] == aligned["extractants"][source]["anchors"]
    for payload in (aligned, wrong):
        text = json.dumps(payload)
        for field in ("private_truth_binding", "world_id", "permutation", "aligned_sha256"):
            assert field not in text


def test_selected_aqueous_product_is_measured_without_changing_other_phases():
    with presentation(None, p.GOAL, 12):
        env = gym.make(
            "ChemWorld",
            task_id=p.TASK,
            seed=0,
            full_process_contract_id=p.FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        )
        try:
            env.reset(seed=0)
            base = env.unwrapped
            state = base._state
            phases = PhaseLedger(
                {
                    "organic": PhaseRecord(
                        phase_id="organic",
                        vessel_id=state.vessel_id,
                        phase_type="organic",
                        volume_L=0.01,
                        species_amounts_mol={"P_org": 0.002},
                    ),
                    "aqueous": PhaseRecord(
                        phase_id="aqueous",
                        vessel_id=state.vessel_id,
                        phase_type="aqueous",
                        volume_L=0.01,
                        selected=True,
                        species_amounts_mol={"P_aq": 0.003, "B_aq": 0.001, "A": 0.0},
                    ),
                }
            )
            state = state.replace(
                phases=phases,
                species_amounts=phases.total_amounts_mol(),
                species=replace(state.species, initial_amounts_mol={"A": 0.02}),
                volume_L=0.02,
            )
            values = base.observation_kernel._truth_values(state)
            assert abs(values["purity"] - 0.75) < 1e-12
            assert abs(values["recovery"] - 0.15) < 1e-12
            # A scoring-role omission must not be mistaken for chemical destruction.
            assert values["process_mass_balance_error"] < 1e-12
        finally:
            env.close()


def test_prepartition_sampling_transfer_and_extractant_conserve_inventory():
    from scripts.work_ii_p_inventory import inventory_v2

    with inventory_v2(), presentation(None, p.GOAL, 12):
        env = gym.make(
            "ChemWorld",
            task_id=p.TASK,
            seed=0,
            budget_override=720,
            full_process_contract_id=p.FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        )
        try:
            env.reset(seed=0)
            audits = []
            wrapped = p.Capture(env, [], audits, {})
            actions = [
                *p.recipe()[:4],
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "quench"},
                {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.02},
                {"operation": "transfer", "transfer_fraction": 0.5},
                {"operation": "add_extractant", "extractant": 0, "volume_L": 0.05},
            ]
            for action in actions:
                info = wrapped.step(action)[4]
                assert info["transaction_status"] == "committed", (action, info)
            assert all(a["passed"] for a in audits), audits
            assert len(audits) == 4
        finally:
            env.close()


def test_prepartition_concentration_and_drying_do_not_create_product():
    from scripts.work_ii_p_inventory import inventory_v3

    with inventory_v3(), presentation(None, p.GOAL, 12):
        env = gym.make(
            "ChemWorld",
            task_id=p.TASK,
            seed=0,
            budget_override=720,
            full_process_contract_id=p.FULL_PROCESS_FREE_RESEARCH_CONTRACT,
        )
        try:
            env.reset(seed=0)
            audits = []
            wrapped = p.Capture(env, [], audits, {})
            actions = [
                *p.recipe()[:6],
                {"operation": "concentrate", "duration_s": 3600},
                {"operation": "dry"},
                {"operation": "measure", "instrument": "hplc"},
                {"operation": "add_extractant", "extractant": 0, "volume_L": 0.05},
            ]
            for action in actions:
                info = wrapped.step(action)[4]
                assert info["transaction_status"] == "committed", (action, info)
            assert all(a["passed"] for a in audits), audits
        finally:
            env.close()
