from __future__ import annotations

import json
from pathlib import Path

import gymnasium as gym

import chemworld  # noqa: F401
from chemworld.agent_interface import agent_view_bundle
from chemworld.data.logging import TrajectoryLogger, load_jsonl
from chemworld.foundation import audit_public_payload
from chemworld.tasks import list_tasks


def test_public_task_info_hides_mechanism_truth_for_all_tasks() -> None:
    for task in list_tasks():
        env = gym.make("ChemWorld", task_id=task.task_id, seed=task.seeds[0])
        try:
            _observation, info = env.reset(seed=task.seeds[0])
            hidden_species = set(
                env.unwrapped.scenario_instance.compiled_mechanism.species_index
            )
            assert audit_public_payload(info, hidden_species_ids=hidden_species) == []
            assert "mechanism_manifest" not in info
            assert "reactions" not in info
            assert "debug_mechanism" not in info
            assert "runtime" not in info
            assert "mechanism_observable_mapping" not in info["observation_contract"]
            assert "hidden_parameter_seed" not in info["scenario"]
            assert "initial_state_seed" not in info["scenario"]
            assert "parameter_profile" not in info["scenario"]
            constitution_checks = info["constitution"]["checks"]
            assert all(check["value"] is None for check in constitution_checks)
            assert all(check["message"] == "" for check in constitution_checks)
            assert all(
                not any(
                    check["name"].endswith(f":{species_id}")
                    for species_id in hidden_species
                )
                for check in constitution_checks
            )
        finally:
            env.close()


def test_debug_truth_task_info_keeps_truth_under_debug_keys() -> None:
    env = gym.make(
        "ChemWorld",
        task_id="reaction-to-assay",
        seed=0,
        debug_truth=True,
    )
    try:
        _observation, info = env.reset(seed=0)
        hidden_species = set(env.unwrapped.scenario_instance.compiled_mechanism.species_index)
        assert "debug_mechanism" in info
        assert "mechanism_manifest" in info["debug_mechanism"]
        assert "reactions" in info["debug_mechanism"]
        assert audit_public_payload(
            info,
            hidden_species_ids=hidden_species,
            allow_debug_truth=True,
        ) == []
    finally:
        env.close()


def test_agent_views_and_trajectory_do_not_leak_hidden_species_or_rates(
    tmp_path: Path,
) -> None:
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        observation, task_info = env.reset(seed=0)
        evaluator_logging_task_info = {
            **task_info,
            **env.unwrapped.evaluator_provenance(),
        }
        hidden_species = set(env.unwrapped.scenario_instance.compiled_mechanism.species_index)
        actions = [
            {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2},
            {"operation": "add_reagent", "amount_mol": 0.010},
            {"operation": "add_catalyst", "catalyst_amount_mol": 0.00025, "catalyst": 1},
            {
                "operation": "heat",
                "target_temperature_K": 382.0,
                "duration_s": 1350.0,
                "stirring_speed_rpm": 720.0,
            },
            {"operation": "measure", "instrument": "hplc"},
        ]
        info = {}
        trajectory_path = tmp_path / "public_views.jsonl"
        with TrajectoryLogger(trajectory_path) as logger:
            for step, action in enumerate(actions, start=1):
                observation, reward, terminated, truncated, info = env.step(action)
                view = agent_view_bundle(env.unwrapped, observation, info)
                for payload in (observation, info, view):
                    assert audit_public_payload(
                        payload,
                        hidden_species_ids=hidden_species,
                    ) == []
                assert all(
                    check["value"] is None and check["message"] == ""
                    for check in info["constitution_checks"]
                )
                logger.log(
                    task_info=evaluator_logging_task_info,
                    step=step,
                    action=action,
                    observation=observation,
                    reward=float(reward),
                    terminated=bool(terminated),
                    truncated=bool(truncated),
                    info=info,
                    agent_metadata={"agent_name": "public-leakage-test"},
                    agent_view=view,
                )
        records = load_jsonl(trajectory_path)
        assert records
        json.dumps(records[-1], sort_keys=True)
        for record in records:
            assert audit_public_payload(record, hidden_species_ids=hidden_species) == []
    finally:
        env.close()


def test_public_leakage_auditor_negative_and_public_label_cases() -> None:
    hidden_species = {"A", "P", "Cat_active"}
    assert audit_public_payload(
        {"raw_signal": {"peaks": [{"species_id": "target_public"}]}},
        hidden_species_ids=hidden_species,
    ) == []
    findings = audit_public_payload(
        {"raw_signal": {"peaks": [{"species_id": "A"}]}},
        hidden_species_ids=hidden_species,
    )
    assert findings
    assert findings[0].reason in {"hidden_species_id", "non_public_species_label"}

    manifest_findings = audit_public_payload(
        {"mechanism_manifest": {"species_roles": {"A": ["reactant"]}}},
        hidden_species_ids=hidden_species,
    )
    assert manifest_findings
    assert manifest_findings[0].reason == "sensitive_key"

    rate_findings = audit_public_payload(
        {"rate_law": {"equation_id": "arrhenius_mass_action", "A": 1.0e5}},
        hidden_species_ids=hidden_species,
    )
    assert rate_findings
    assert rate_findings[0].reason == "sensitive_key"
