from __future__ import annotations

from typing import Any

import gymnasium as gym
import pytest

import chemworld  # noqa: F401
from chemworld.agents.base import HistoryRecord
from chemworld.agents.event import ScriptedChemistryAgent
from chemworld.data.logging import observation_to_json
from chemworld.foundation import (
    WorldState,
    audit_ledger_single_source_of_truth,
)
from chemworld.foundation.state import (
    Ledger,
    PhaseLedger,
    PhaseRecord,
    ProcessLedger,
    VesselLedger,
    VesselRecord,
)
from chemworld.tasks import TaskSpec, list_tasks

PARTITION_SMOKE_ACTIONS: tuple[dict[str, Any], ...] = (
    {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.008},
    {"operation": "add_phase", "phase": "aqueous", "volume_L": 0.015},
    {"operation": "add_extractant", "extractant": "organic", "volume_L": 0.02},
    {"operation": "mix", "duration_s": 240.0, "stirring_speed_rpm": 700.0},
    {"operation": "settle", "duration_s": 420.0},
    {"operation": "separate_phase", "target_phase": "organic"},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
)


def _failure_names(state: WorldState) -> set[str]:
    return {
        finding.name
        for finding in audit_ledger_single_source_of_truth(state)
        if not finding.passed
    }


def _base_state(**updates: Any) -> WorldState:
    state = WorldState(
        species_amounts={"A": 0.01, "P": 0.0},
        volume_L=0.02,
        temperature_K=298.15,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="reactor",
    )
    return state.replace(**updates) if updates else state


def test_ledger_audit_passes_for_default_world_state() -> None:
    failures = [
        finding.to_dict()
        for finding in audit_ledger_single_source_of_truth(_base_state())
        if not finding.passed
    ]

    assert failures == []


def test_ledger_audit_rejects_material_totals_not_sourced_from_phase_ledger() -> None:
    phases = PhaseLedger(
        {
            "organic": PhaseRecord(
                phase_id="organic",
                vessel_id="reactor",
                phase_type="organic",
                volume_L=0.012,
                species_amounts_mol={"A": 0.004, "P": 0.0},
            )
        }
    )
    vessels = VesselLedger(
        {
            "reactor": VesselRecord(
                vessel_id="reactor",
                vessel_type="batch_reactor",
                max_volume_L=0.10,
                max_temperature_K=470.0,
                max_pressure_Pa=550_000.0,
                phase_ids=("organic",),
                temperature_K=298.15,
                pressure_Pa=101_325.0,
            )
        }
    )
    state = _base_state(phases=phases, vessels=vessels)

    failures = _failure_names(state)

    assert "ledger_material_single_source" in failures


def test_ledger_audit_rejects_primary_state_in_metadata() -> None:
    state = _base_state(
        metadata={
            "phase_ledger": {"organic": {"product_mol": 0.004}},
            "final_assay_done": True,
            "initial_reactant_mol": 0.01,
            "purity": 0.8,
        }
    )

    failures = _failure_names(state)

    assert "metadata_no_primary_structured_state" in failures


def test_ledger_audit_rejects_phase_metadata_material_state() -> None:
    phase = PhaseRecord(
        phase_id="organic",
        vessel_id="reactor",
        phase_type="organic",
        volume_L=0.012,
        species_amounts_mol={"A": 0.01, "P": 0.0},
        metadata={"product_mol": 0.004},
    )
    state = _base_state(
        phases=PhaseLedger({"organic": phase}),
        vessels=VesselLedger(
            {
                "reactor": VesselRecord(
                    vessel_id="reactor",
                    vessel_type="batch_reactor",
                    max_volume_L=0.10,
                    max_temperature_K=470.0,
                    max_pressure_Pa=550_000.0,
                    phase_ids=("organic",),
                    temperature_K=298.15,
                    pressure_Pa=101_325.0,
                )
            }
        ),
    )

    failures = _failure_names(state)

    assert "phase_metadata_no_primary_state:organic" in failures


def test_constitution_exposes_ledger_single_source_failures() -> None:
    state = _base_state(
        phases=PhaseLedger(
            {
                "organic": PhaseRecord(
                    phase_id="organic",
                    vessel_id="missing_vessel",
                    phase_type="organic",
                    volume_L=0.012,
                    species_amounts_mol={"A": 0.004, "P": 0.0},
                )
            }
        )
    )
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        failures = {
            check.name
            for check in env.unwrapped.constitution.check_state(state).failures()
        }
    finally:
        env.close()

    assert "ledger_material_single_source" in failures
    assert "phase_attached_vessel_exists:organic" in failures


@pytest.mark.parametrize("task", list_tasks(), ids=lambda task: task.task_id)
def test_ledger_audit_passes_during_formal_task_smoke(task: TaskSpec) -> None:
    env = gym.make("ChemWorld", task_id=task.task_id, seed=task.seeds[0])
    history: list[HistoryRecord] = []
    agent = ScriptedChemistryAgent()
    try:
        observation, task_info = env.reset(seed=task.seeds[0])
        agent.reset(task_info, task.seeds[0])
        initial_failures = [
            finding.to_dict()
            for finding in audit_ledger_single_source_of_truth(env.unwrapped._state)
            if not finding.passed
        ]
        assert initial_failures == []

        scripted_actions = (
            PARTITION_SMOKE_ACTIONS if task.task_id == "partition-discovery" else None
        )
        for step in range(min(task.budget, 18)):
            if scripted_actions is not None:
                if step >= len(scripted_actions):
                    break
                action = scripted_actions[step]
            else:
                action = agent.act(history)
            observation, reward, terminated, truncated, info = env.step(action)
            failures = [
                finding.to_dict()
                for finding in audit_ledger_single_source_of_truth(env.unwrapped._state)
                if not finding.passed
            ]
            assert failures == [], (task.task_id, step, action, failures)
            assert env.unwrapped.constitution.check_state(env.unwrapped._state).passed
            obs_json = observation_to_json(observation)
            history.append(
                HistoryRecord(
                    step=step,
                    action=action,
                    observation=obs_json,
                    reward=float(reward),
                    info=info,
                )
            )
            agent.update(action, obs_json, float(reward), info)
            if terminated or truncated:
                break
    finally:
        env.close()


def test_ledger_audit_rejects_process_compatibility_drift() -> None:
    state = _base_state(
        ledger=Ledger(time_s=10.0, cost=1.0, risk=0.2, sample_consumed_L=0.001),
    )
    object.__setattr__(
        state,
        "process",
        ProcessLedger(
            time_s=10.0,
            cost=2.0,
            risk=0.2,
            sample_consumed_L=0.001,
        ),
    )

    failures = _failure_names(state)

    assert "ledger_process_single_source" in failures
