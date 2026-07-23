from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
from scripts.run_mechanism_adaptation_v0_2 import (
    _campaign_filename,
    _validate_resumable_campaign,
    _write_immutable_json,
)

from chemworld.agents.task_recipes import task_recipe_from_unit_vector
from chemworld.eval.mechanism_adaptation_execution import (
    PublicCampaignObservationSession,
    build_action_library,
    canonical_sha256,
    encode_public_experiment_trace,
    gate_a_certificate_decision,
    run_gate_a,
    selected_campaign_rows,
    validate_precomputed_design_audit,
)
from chemworld.eval.mechanism_design_audit import (
    _audit_material_alignment,
    _recipe_field_values,
)
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]


def _protocol() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_v0.2.1.json").read_text(encoding="utf-8")
    )


def _gate_a_plan() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.2.4.json").read_text(
            encoding="utf-8"
        )
    )


def _paired_gate_a_plan() -> dict[str, object]:
    return json.loads(
        (ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.2.4.json").read_text(
            encoding="utf-8"
        )
    )


def test_gate_a_fails_closed_without_online_policy_certificate() -> None:
    protocol = _protocol()
    plan = _paired_gate_a_plan()
    decision = gate_a_certificate_decision(
        protocol,
        plan,
        controlled_gate_pass=True,
    )
    assert decision["status"] == "gate_a_blocked_online_policy_certificate_pending"
    assert decision["controlled_matched_gate_pass"] is True
    assert decision["online_policy_feasible_gate_pass"] is False
    assert decision["gate_a_pass"] is False


def test_gate_a_requires_two_bound_passing_certificates() -> None:
    protocol = _protocol()
    plan = _paired_gate_a_plan()
    certificate = {
        "schema_version": "chemworld-mechanism-adaptation-online-policy-certificate-0.1",
        "certificate_scope": "online_policy_feasible_diagnosis",
        "protocol_sha256": canonical_sha256(protocol),
        "gate_a_plan_sha256": canonical_sha256(plan),
        "primary_gate_budget": 2,
        "hidden_change_time": True,
        "uses_actual_available_pre_change_history": True,
        "uses_actual_action_measurement_and_budget_contract": True,
        "status": "passed",
        "gate_pass": True,
    }
    decision = gate_a_certificate_decision(
        protocol,
        plan,
        controlled_gate_pass=True,
        online_policy_certificate=certificate,
    )
    assert decision["gate_a_pass"] is True
    stale = dict(certificate, gate_a_plan_sha256="0" * 64)
    with pytest.raises(ValueError, match="gate_a_plan_sha256"):
        gate_a_certificate_decision(
            protocol,
            plan,
            controlled_gate_pass=True,
            online_policy_certificate=stale,
        )


def test_immutable_gate_a_writer_rejects_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "formal-result.json"
    _write_immutable_json(output, {"version": 1})
    with pytest.raises(FileExistsError, match="immutable formal result"):
        _write_immutable_json(output, {"version": 2})
    assert json.loads(output.read_text(encoding="utf-8")) == {"version": 1}


def test_precomputed_design_audit_must_be_passing_and_hash_bound() -> None:
    protocol = _protocol()
    plan = _paired_gate_a_plan()
    report = json.loads(
        (
            ROOT
            / "workstreams/flagship_tasks/reports/"
            "mechanism-adaptation-design-audit-freeze-rc7.json"
        ).read_text(encoding="utf-8")
    )
    validated = validate_precomputed_design_audit(protocol, plan, report)
    assert validated["pass"] is True

    stale = dict(report, protocol_sha256="0" * 64)
    with pytest.raises(ValueError, match="protocol_sha256"):
        validate_precomputed_design_audit(protocol, plan, stale)


def test_gate_a_action_library_and_public_encoding_are_deterministic() -> None:
    first = build_action_library("reaction-to-crystallization", action_count=6, seed=41102)
    second = build_action_library("reaction-to-crystallization", action_count=6, seed=41102)
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
    action_library = build_action_library("electrochemical-conversion", action_count=3, seed=41102)
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


def _structural_design_report() -> dict[str, object]:
    protocol = _protocol()
    design = protocol["intervention_action_alignment"]
    assert isinstance(design, dict)
    report_path = design["design_audit_report"]
    assert isinstance(report_path, str)
    return json.loads((ROOT / report_path).read_text(encoding="utf-8"))


def test_current_mechanism_design_has_reachable_covered_targets() -> None:
    report = _structural_design_report()
    assert report["pass"] is True
    assert report["failure_count"] == 0


def test_design_audit_accepts_both_electrochemical_material_targets() -> None:
    report = _structural_design_report()
    assert report["pass"] is True
    checks = {
        item["check"]: item["pass"]
        for item in report["task_reports"]["electrochemical-conversion"]["checks"]
    }
    assert checks["material_law_counterfactual_solvent:public_choice_cardinality"] is True
    assert checks["material_law_counterfactual_solvent:moved_indices_publicly_reachable"] is True
    assert (
        checks["material_law_counterfactual_electrolyte_profile:public_choice_cardinality"] is True
    )
    assert (
        checks["material_law_counterfactual_electrolyte_profile:moved_indices_publicly_reachable"]
        is True
    )


def test_design_audit_accepts_reaction_solvent_as_an_alternative_target() -> None:
    protocol = _protocol()
    plan = _paired_gate_a_plan()
    intervention = protocol["task_mechanism_contracts"]["reaction-to-crystallization"][
        "interventions"
    ]["material_law_counterfactual"][0]
    intervention.update({"material_field": "solvent", "public_to_baseline": [2, 1, 0, 3]})
    action_library = _action_libraries(protocol, plan)["reaction-to-crystallization"]
    task_info = get_task("reaction-to-crystallization").to_dict()
    recipes = {
        action_id: task_recipe_from_unit_vector(task_info, vector)
        for action_id, vector in action_library.items()
    }
    findings: list[dict[str, object]] = []
    _audit_material_alignment(
        findings,
        task_id="reaction-to-crystallization",
        candidate_id="material_law_counterfactual",
        intervention=intervention,
        recipe_values=_recipe_field_values(recipes),
    )
    assert findings
    assert all(item["pass"] for item in findings)


def test_campaign_selection_never_splits_changed_no_change_pairs() -> None:
    rows = selected_campaign_rows(_protocol(), limit=3)
    assert len(rows) == 6
    assert len({row["pair_id"] for row in rows}) == 3
    for pair_id in {row["pair_id"] for row in rows}:
        pair = [row for row in rows if row["pair_id"] == pair_id]
        assert {row["arm"] for row in pair} == {"changed", "no_change_twin"}


def test_current_registry_does_not_promote_method_development_to_environment_evidence() -> None:
    current = json.loads((ROOT / "configs/current.json").read_text(encoding="utf-8"))
    assert "development_evidence" not in current
    assert current["formal_evaluation"]["status"] == "environment_ready_methods_unfrozen"
    assert current["formal_evaluation"]["formal_results_present"] is False
    assert current["formal_evaluation"]["benchmark_claim_allowed"] is False


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
                    json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
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


def test_feedback_campaign_paths_and_resume_bind_the_condition(tmp_path: Path) -> None:
    protocol = _protocol()
    row = selected_campaign_rows(protocol, limit=1)[0]
    assert _campaign_filename(row, "true_feedback") == f"{row['pair_id']}--{row['arm']}.json"
    assert _campaign_filename(row, "permuted_feedback") == (
        f"{row['pair_id']}--{row['arm']}--permuted_feedback.json"
    )

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
                    json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
                ).hexdigest(),
                "matrix_row": row,
                "feedback_condition": "permuted_feedback",
                **phases,
            }
        ),
        encoding="utf-8",
    )
    _validate_resumable_campaign(
        summary,
        row=row,
        protocol=protocol,
        feedback_condition="permuted_feedback",
    )
    with pytest.raises(RuntimeError, match="feedback-condition"):
        _validate_resumable_campaign(summary, row=row, protocol=protocol)
