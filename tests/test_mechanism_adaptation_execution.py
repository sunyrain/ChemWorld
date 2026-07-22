from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
from scripts.run_mechanism_adaptation_v0_2 import _validate_resumable_campaign

from chemworld.eval.mechanism_adaptation_execution import (
    PublicCampaignObservationSession,
    build_action_library,
    encode_public_experiment_trace,
    run_gate_a,
    selected_campaign_rows,
)
from chemworld.eval.mechanism_design_audit import audit_mechanism_design

ROOT = Path(__file__).resolve().parents[1]


def _protocol() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_v0.2.1.json").read_text(
            encoding="utf-8"
        )
    )


def _gate_a_plan() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.2.1.json").read_text(
            encoding="utf-8"
        )
    )


def _paired_gate_a_plan() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.2.2.json").read_text(
            encoding="utf-8"
        )
    )


def test_gate_a_action_library_and_public_encoding_are_deterministic() -> None:
    first = build_action_library(
        "reaction-to-crystallization", action_count=6, seed=41102
    )
    second = build_action_library(
        "reaction-to-crystallization", action_count=6, seed=41102
    )
    assert list(first) == [f"design-{index:02d}" for index in range(6)]
    assert all(np.array_equal(first[key], second[key]) for key in first)

    features = encode_public_experiment_trace(
        [({"b": np.asarray([np.nan]), "a": np.asarray([2.0])}, 0.5)]
    )
    assert features == [1.0, 2.0, 0.0, 0.0, 1.0, 0.5]


def test_gate_a_plan_cannot_underfill_the_fixed_decoder_budget() -> None:
    plan = _gate_a_plan()
    plan["action_library"]["action_count_per_task"] = 3
    with pytest.raises(ValueError, match="largest decoder budget"):
        run_gate_a(_protocol(), plan)


def test_paired_gate_a_must_match_the_protocol_pre_change_budget() -> None:
    plan = _paired_gate_a_plan()
    plan["paired_phase_design"]["pre_change_reference_experiments"] = 1
    with pytest.raises(ValueError, match="protocol pre-change experiment budget"):
        run_gate_a(_protocol(), plan)


def test_observation_seed_can_change_noise_without_changing_hidden_world() -> None:
    action_library = build_action_library(
        "electrochemical-conversion", action_count=3, seed=41102
    )
    selected = {"design-00": action_library["design-00"]}
    with PublicCampaignObservationSession(
        task_id="electrochemical-conversion",
        seed=23,
        interventions=(),
        action_library=selected,
        experiment_horizon=1,
        observation_seed=7001,
    ) as first:
        first_world = np.array(first.environment.world.catalyst_effects, copy=True)
        first_trace = first.observe("design-00")
    with PublicCampaignObservationSession(
        task_id="electrochemical-conversion",
        seed=23,
        interventions=(),
        action_library=selected,
        experiment_horizon=1,
        observation_seed=7002,
    ) as second:
        second_world = np.array(second.environment.world.catalyst_effects, copy=True)
        second_trace = second.observe("design-00")
    assert np.array_equal(first_world, second_world)
    assert not np.array_equal(first_trace, second_trace)


def _action_libraries(protocol: dict[str, object], plan: dict[str, object]):
    action_plan = plan["action_library"]
    return {
        task_id: build_action_library(
            task_id,
            action_count=int(action_plan["action_count_per_task"]),
            seed=int(action_plan["design_seed"]),
        )
        for task_id in protocol["design"]["tasks"]
    }


def test_current_mechanism_design_has_reachable_covered_targets() -> None:
    protocol = _protocol()
    plan = _gate_a_plan()
    report = audit_mechanism_design(
        protocol,
        plan,
        action_libraries=_action_libraries(protocol, plan),
    )
    assert report["pass"] is True
    assert report["failure_count"] == 0


def test_design_audit_rejects_electrochemical_solvent_counterfactual() -> None:
    protocol = _protocol()
    plan = _gate_a_plan()
    intervention = protocol["task_mechanism_contracts"][
        "electrochemical-conversion"
    ]["interventions"]["material_law_counterfactual"][0]
    intervention["material_field"] = "solvent"
    report = audit_mechanism_design(
        protocol,
        plan,
        action_libraries=_action_libraries(protocol, plan),
    )
    failed_checks = {item["check"] for item in report["failures"]}
    assert "material_law_counterfactual:public_choice_cardinality" in failed_checks
    assert "material_law_counterfactual:moved_indices_publicly_reachable" in failed_checks


def test_design_audit_accepts_reaction_solvent_as_an_alternative_target() -> None:
    protocol = _protocol()
    plan = _gate_a_plan()
    intervention = protocol["task_mechanism_contracts"][
        "reaction-to-crystallization"
    ]["interventions"]["material_law_counterfactual"][0]
    intervention.update(
        {"material_field": "solvent", "public_to_baseline": [2, 1, 0, 3]}
    )
    report = audit_mechanism_design(
        protocol,
        plan,
        action_libraries=_action_libraries(protocol, plan),
    )
    assert report["pass"] is True


def test_campaign_selection_never_splits_changed_no_change_pairs() -> None:
    rows = selected_campaign_rows(_protocol(), limit=3)
    assert len(rows) == 6
    assert len({row["pair_id"] for row in rows}) == 3
    for pair_id in {row["pair_id"] for row in rows}:
        pair = [row for row in rows if row["pair_id"] == pair_id]
        assert {row["arm"] for row in pair} == {"changed", "no_change_twin"}


def test_current_live_llm_target_is_v0_4_11_everywhere() -> None:
    current = json.loads((ROOT / "configs/current.json").read_text(encoding="utf-8"))
    freeze = json.loads(
        (ROOT / "configs/benchmark/method_freeze_v0.4.json").read_text(encoding="utf-8")
    )
    expected = "workstreams/benchmark_v1/reports/live-llm-dev-v0.4.11.json"
    live_llm = current["development_evidence"]["live_llm"]
    assert live_llm["report"] == expected
    assert live_llm["artifact_state"] == "pending"
    assert live_llm["artifact_roles"] == ["planned_output"]
    assert freeze["artifact_bindings"]["llm_development"]["path"] == expected


def test_campaign_resume_rejects_a_stale_matrix_row(tmp_path: Path) -> None:
    protocol = _protocol()
    row = selected_campaign_rows(protocol, limit=1)[0]
    phases = {}
    for phase in ("iid", "shifted"):
        trajectory = tmp_path / f"{phase}.jsonl"
        trajectory.write_text("{}\n", encoding="utf-8")
        phases[phase] = {
            "trajectory_path": str(trajectory),
            "trajectory_sha256": hashlib.sha256(trajectory.read_bytes()).hexdigest(),
        }
    summary = tmp_path / "campaign.json"
    summary.write_text(
        json.dumps(
            {
                "protocol_sha256": hashlib.sha256(
                    json.dumps(
                        protocol, sort_keys=True, separators=(",", ":")
                    ).encode()
                ).hexdigest(),
                "matrix_row": row,
                **phases,
            }
        ),
        encoding="utf-8",
    )
    _validate_resumable_campaign(summary, row=row, protocol=protocol)
    changed_row = dict(row)
    changed_row["world_seed"] = 999
    with pytest.raises(RuntimeError, match="matrix-row"):
        _validate_resumable_campaign(summary, row=changed_row, protocol=protocol)
