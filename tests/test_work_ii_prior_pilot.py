from __future__ import annotations

import json
from pathlib import Path

from scripts.run_work_ii_prior_pilot import build_pilot_protocol

from chemworld.materials import static_material_information_dossier

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/benchmark/work_ii_prior_pilot.json"


def _plan() -> dict[str, object]:
    value = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_work_ii_prior_pilot_freezes_five_tasks_three_arms_and_five_seed_cap() -> None:
    plan = _plan()

    assert len(plan["task_ids"]) == 5
    assert len(plan["prior_arms"]) == 3
    assert plan["seed_policy"]["completion_world_seeds"] == [0, 1, 2, 3, 4]
    assert plan["participant"] == {
        "provider": "wellau",
        "wire_api": "responses",
        "model_id": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "method_config_path": (
            "configs/methods/work_ii/"
            "participant_methods_work_ii_wellau_sol_medium_prior_pilot.json"
        ),
        "method_id": "work_ii_wellau_sol_medium_direct_prior_pilot",
    }


def test_all_fifteen_mock_preflight_protocols_validate_and_hide_arm_identity() -> None:
    plan = _plan()
    built = []
    for task_id in plan["task_ids"]:
        for arm_id in plan["prior_arms"]:
            protocol = build_pilot_protocol(
                plan,
                stage_id="contract-preflight",
                task_id=task_id,
                arm_id=arm_id,
                world_seed=0,
            )
            dossier = static_material_information_dossier(
                protocol["material_information"],
                task_id=task_id,
                material_family_id=(
                    plan["tasks"][task_id].get("material_family_id")
                ),
            )
            if arm_id == "opaque":
                assert dossier is None
            else:
                assert dossier is not None
                serialized = json.dumps(dossier, sort_keys=True).lower()
                assert "misindexed" not in serialized
                assert "descriptor_permutation" not in serialized
            built.append((task_id, arm_id, protocol["material_information"]["mode"]))

    assert len(built) == 15
    assert len(set(built)) == 15


def test_real_probe_is_one_seed_one_task_three_arms_before_breadth() -> None:
    plan = _plan()
    stage = plan["stages"]["real-probe"]

    assert stage["provider"] == "wellau"
    assert stage["task_ids"] == ["electrochemical-conversion"]
    assert stage["prior_arms"] == [
        "opaque",
        "aligned_nominal",
        "misindexed_nominal",
    ]
    assert stage["world_seeds"] == [0]
    assert stage["exploration_experiments"] == 1
    assert stage["expected_cells"] == 3
