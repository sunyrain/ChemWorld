from __future__ import annotations

import subprocess

import pytest
from scripts.diagnose_work_ii_catalyst_effect_chain import (
    _actions,
    _sampling_audit,
    _scoped_dirty_paths,
)

from chemworld.foundation import WorldState
from chemworld.foundation.state_ledgers import SpeciesLedger


def _state(*, factor: float) -> WorldState:
    initial_a = 0.015 * factor
    species = {
        "A": 0.004 * factor,
        "P": 0.009 * factor,
        "B": 0.001 * factor,
        "D": 0.0005 * factor,
        "Cat_active": 0.0002 * factor,
        "Cat_dead": 0.0001 * factor,
    }
    return WorldState(
        species_amounts=species,
        volume_L=0.025 * factor,
        temperature_K=410.0,
        pressure_Pa=101_325.0,
        phase="liquid",
        vessel_id="reactor",
        species=SpeciesLedger(initial_amounts_mol={"A": initial_a}),
    )


def test_zero_dose_control_omits_catalyst_charge() -> None:
    actions = _actions(
        temperature_K=410.0,
        duration_s=1_800.0,
        catalyst_amount_mol=0.0,
    )

    assert all(action["operation"] != "add_catalyst" for action in actions)
    assert [action for action in actions if action["operation"] == "heat"] == [
        {
            "operation": "heat",
            "target_temperature_K": 410.0,
            "duration_s": 1_800.0,
            "stirring_speed_rpm": 675.0,
        }
    ]


def test_positive_dose_control_adds_exact_catalyst_charge() -> None:
    actions = _actions(
        temperature_K=350.0,
        duration_s=7_200.0,
        catalyst_amount_mol=0.000315,
    )

    catalyst_actions = [
        action for action in actions if action["operation"] == "add_catalyst"
    ]
    assert catalyst_actions == [
        {
            "operation": "add_catalyst",
            "catalyst_amount_mol": 0.000315,
            "catalyst": 1,
        }
    ]


def test_sampling_audit_accepts_proportional_withdrawal_with_scaled_basis() -> None:
    audit = _sampling_audit(_state(factor=1.0), _state(factor=0.8))

    assert audit["volume_factor"] == pytest.approx(0.8)
    assert audit["maximum_amount_scaling_residual_mol"] <= 1.0e-15
    assert audit["post_withdrawal_truth"] == pytest.approx(
        audit["pre_withdrawal_truth"]
    )


def test_scoped_dirty_paths_include_untracked_runtime_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=["git"],
            returncode=0,
            stdout=(
                " M src/chemworld/world/reaction_kernel.py\n"
                "?? scripts/new_diagnostic.py\n"
                "?? unrelated-notes.txt\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert _scoped_dirty_paths() == [
        "scripts/new_diagnostic.py",
        "src/chemworld/world/reaction_kernel.py",
    ]
