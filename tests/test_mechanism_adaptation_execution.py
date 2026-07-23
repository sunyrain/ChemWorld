from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
from scripts.run_mechanism_adaptation_v0_2 import (
    _campaign_filename,
    _compact_gate_a_report,
    _validate_resumable_campaign,
    _write_immutable_json,
)

from chemworld.agents.task_recipes import task_recipe_from_unit_vector
from chemworld.eval.mechanism_adaptation_execution import (
    PublicCampaignObservationSession,
    _advance_online_change_point_hypotheses,
    _balanced_hidden_change_times,
    _canonical_policy_cycle,
    _online_hypothesis_evidence_channel,
    _select_discriminative_feature_blocks,
    _update_online_change_point_posterior,
    build_action_library,
    canonical_sha256,
    encode_public_experiment_trace,
    gate_a_certificate_decision,
    gate_a_execution_contract_binding,
    run_gate_a,
    selected_campaign_rows,
    validate_precomputed_design_audit,
)
from chemworld.eval.mechanism_design_audit import (
    _audit_intervention_decision_relevance,
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


def test_online_policy_cycle_uses_canonical_order_for_information_selected_set() -> None:
    canonical = [f"design-{index:02d}" for index in range(6)]

    assert _canonical_policy_cycle(
        canonical_action_ids=canonical,
        ranked_action_ids=[
            "design-05",
            "design-00",
            "design-04",
            "design-02",
            "design-03",
            "design-01",
        ],
        action_count=4,
    ) == [
        "design-00",
        "design-02",
        "design-04",
        "design-05",
    ]


def test_online_policy_cycle_rejects_unknown_or_incomplete_rankings() -> None:
    canonical = ["design-00", "design-01", "design-02"]

    with pytest.raises(ValueError, match="outside the action library"):
        _canonical_policy_cycle(
            canonical_action_ids=canonical,
            ranked_action_ids=["design-00", "unknown", "design-01"],
            action_count=2,
        )
    with pytest.raises(ValueError, match="do not cover"):
        _canonical_policy_cycle(
            canonical_action_ids=canonical,
            ranked_action_ids=["design-00"],
            action_count=2,
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
    execution_binding = gate_a_execution_contract_binding(protocol, plan)
    certificate = {
        "schema_version": "chemworld-mechanism-adaptation-online-policy-certificate-0.4",
        "certificate_scope": "online_policy_feasible_diagnosis",
        "protocol_sha256": canonical_sha256(protocol),
        "gate_a_plan_sha256": canonical_sha256(plan),
        "controlled_matched_primary_budget": 4,
        "online_policy_gate_budget": 4,
        "hidden_change_time": True,
        "policy_received_phase_or_reset_indicator": False,
        "uses_actual_available_pre_change_history": True,
        "uses_actual_action_measurement_and_budget_contract": True,
        "execution_contract_binding_sha256": execution_binding["binding_sha256"],
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
    stale_execution = dict(
        certificate,
        execution_contract_binding_sha256="0" * 64,
    )
    with pytest.raises(ValueError, match="execution_contract_binding_sha256"):
        gate_a_certificate_decision(
            protocol,
            plan,
            controlled_gate_pass=True,
            online_policy_certificate=stale_execution,
        )


def test_immutable_gate_a_writer_rejects_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "formal-result.json"
    _write_immutable_json(output, {"version": 1})
    with pytest.raises(FileExistsError, match="immutable formal result"):
        _write_immutable_json(output, {"version": 2})
    assert json.loads(output.read_text(encoding="utf-8")) == {"version": 1}


def test_gate_a_report_references_online_certificate_without_embedding_trials(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = {
        "schema_version": "online-0.3",
        "certificate_scope": "online_policy_feasible_diagnosis",
        "status": "passed",
        "gate_pass": True,
        "certificate_sha256": "a" * 64,
        "task_reports": {"task": {"trials": [{"large": "payload"}]}},
    }
    report = {
        "certificate_decision": {
            "online_policy_feasible_certificate": certificate,
        },
        "online_policy_feasible_certificate": certificate,
    }
    certificate_path = tmp_path / "online.json"
    certificate_path.write_text(json.dumps(certificate), encoding="utf-8")
    monkeypatch.setitem(
        _compact_gate_a_report.__globals__,
        "ROOT",
        tmp_path,
    )
    compacted = _compact_gate_a_report(
        report,
        online_policy_certificate_path=certificate_path,
    )
    reference = compacted["certificate_decision"]["online_policy_feasible_certificate"]
    assert reference["certificate_sha256"] == canonical_sha256(certificate)
    assert reference["report"].endswith("online.json")
    assert "task_reports" not in reference
    assert compacted["online_policy_feasible_certificate"] == reference


def test_precomputed_design_audit_must_be_passing_and_hash_bound() -> None:
    protocol = _protocol()
    plan = _paired_gate_a_plan()
    report_path = str(
        protocol["intervention_action_alignment"]["design_audit_report"]  # type: ignore[index]
    )
    report = json.loads((ROOT / report_path).read_text(encoding="utf-8"))
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
    assert features == [
        1.0,
        2.0,
        2.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.5,
        0.5,
        0.0,
    ]


def test_public_encoding_summarizes_time_without_growing_with_step_count() -> None:
    one_step = encode_public_experiment_trace([({"signal": np.asarray([2.0])}, 0.5)])
    three_steps = encode_public_experiment_trace(
        [
            ({"signal": np.asarray([2.0])}, 0.5),
            ({"signal": np.asarray([4.0])}, 0.0),
            ({"signal": np.asarray([3.0])}, 1.0),
        ]
    )

    assert len(one_step) == len(three_steps) == 8
    assert three_steps[:4] == [1.0, 2.0, 3.0, 2.0]
    assert three_steps[4:] == [1.0, 0.5, 1.0, 1.0]


def test_online_feature_selection_uses_fit_samples_and_whole_blocks() -> None:
    samples = {
        ("no_change", "transition_contrast\u241fdesign-00"): [
            [0.0, 0.0, 0.0, 0.0, -1.0 + 0.1 * index, 0.0, 0.0, 0.0] for index in range(4)
        ],
        ("rate_law_family", "transition_contrast\u241fdesign-00"): [
            [0.0, 0.0, 0.0, 0.0, 1.0 + 0.1 * index, 0.0, 0.0, 0.0] for index in range(4)
        ],
    }
    indices, report = _select_discriminative_feature_blocks(
        samples,
        candidate_ids=["no_change", "rate_law_family"],
        evidence_action_ids=["transition_contrast\u241fdesign-00"],
        block_size=4,
        block_count=1,
        variance_floor=1.0e-4,
    )

    channel = "transition_contrast\u241fdesign-00"
    assert indices[channel] == (4, 5, 6, 7)
    assert report[channel]["selected_block_indices"] == [1]


def test_reaction_crystallization_action_library_is_relational() -> None:
    library = build_action_library(
        "reaction-to-crystallization",
        action_count=6,
        seed=41102,
    )
    vectors = list(library.values())

    for coordinate in range(vectors[0].size):
        values = {float(vector[coordinate]) for vector in vectors[:3]}
        if coordinate == 5:
            assert len(values) == 3
        else:
            assert len(values) == 1

    differing = np.flatnonzero(vectors[1] != vectors[4]).tolist()
    assert differing == [4]
    assert int(vectors[1][4] * 4) == 0
    assert int(vectors[4][4] * 4) == 2
    assert np.flatnonzero(vectors[2] != vectors[5]).tolist() == [4]


def test_electrochemical_action_library_separates_control_and_material_probes() -> None:
    library = build_action_library(
        "electrochemical-conversion",
        action_count=6,
        seed=41102,
    )
    control_sweep = list(library.values())[:4]
    assert {float(vector[0]) for vector in control_sweep} == {0.625}
    assert {float(vector[1]) for vector in control_sweep} == {0.125}
    assert len({float(vector[3]) for vector in control_sweep}) == 4
    assert len({float(vector[6]) for vector in control_sweep}) == 4

    material_probes = list(library.values())[4:]
    assert material_probes[0][0] == pytest.approx(0.125)
    assert material_probes[1][1] == pytest.approx(0.625)


def test_online_change_time_assignment_is_deterministic_and_balanced() -> None:
    first = _balanced_hidden_change_times(
        [1, 2, 4, 6],
        trial_count=30,
        seed=2_100_000_000,
        task_id="reaction-to-crystallization",
    )
    second = _balanced_hidden_change_times(
        [1, 2, 4, 6],
        trial_count=30,
        seed=2_100_000_000,
        task_id="reaction-to-crystallization",
    )
    counts = [first.count(change_time) for change_time in (1, 2, 4, 6)]
    assert first == second
    assert max(counts) - min(counts) == 1
    assert sorted(counts) == [7, 7, 8, 8]


@pytest.mark.parametrize(
    (
        "hypothesis",
        "reference_experiment_index",
        "current_experiment_index",
        "expected_encoding",
    ),
    [
        (("no_change", None), None, 1, "absolute_trace"),
        (("rate_law_family", 2), None, 3, "absolute_trace"),
        (("no_change", None), 1, 3, "stable_contrast"),
        (("rate_law_family", 2), 1, 3, "transition_contrast"),
        (("rate_law_family", 2), 3, 4, "stable_contrast"),
    ],
)
def test_online_evidence_channel_respects_reference_age(
    hypothesis: tuple[str, int | None],
    reference_experiment_index: int | None,
    current_experiment_index: int,
    expected_encoding: str,
) -> None:
    candidate_id, channel = _online_hypothesis_evidence_channel(
        hypothesis,
        "design-00",
        reference_experiment_index=reference_experiment_index,
        current_experiment_index=current_experiment_index,
    )
    assert candidate_id == hypothesis[0]
    assert channel == f"{expected_encoding}\u241fdesign-00"


def test_online_hazard_expands_only_protocol_change_points() -> None:
    posterior = {("no_change", None): 1.0}
    unchanged = _advance_online_change_point_hypotheses(
        posterior,
        change_after_experiment=3,
        allowed_change_times=[1, 2, 4, 6],
        candidate_ids=["no_change", "rate_law_family", "topology_family"],
        hazard=0.25,
    )
    assert unchanged == posterior

    expanded = _advance_online_change_point_hypotheses(
        posterior,
        change_after_experiment=2,
        allowed_change_times=[1, 2, 4, 6],
        candidate_ids=["no_change", "rate_law_family", "topology_family"],
        hazard=0.25,
    )
    assert expanded == {
        ("no_change", None): 0.75,
        ("rate_law_family", 2): 0.125,
        ("topology_family", 2): 0.125,
    }


def test_online_posterior_uses_transition_only_when_reference_predates_change() -> None:
    posterior = {
        ("no_change", None): 0.5,
        ("rate_law_family", 2): 0.5,
    }
    predictives = {
        ("no_change", "stable_contrast\u241fdesign-00"): (
            np.asarray([0.0]),
            np.asarray([0.1]),
        ),
        ("rate_law_family", "transition_contrast\u241fdesign-00"): (
            np.asarray([10.0]),
            np.asarray([0.1]),
        ),
        ("rate_law_family", "stable_contrast\u241fdesign-00"): (
            np.asarray([0.0]),
            np.asarray([0.1]),
        ),
    }
    transition = _update_online_change_point_posterior(
        posterior,
        action_id="design-00",
        observation=[10.0],
        reference_experiment_index=1,
        current_experiment_index=3,
        predictives=predictives,
    )
    assert transition[("rate_law_family", 2)] > 0.999

    stable = _update_online_change_point_posterior(
        posterior,
        action_id="design-00",
        observation=[0.0],
        reference_experiment_index=3,
        current_experiment_index=4,
        predictives=predictives,
    )
    assert stable == posterior


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
    checks = {
        item["check"]: item["pass"]
        for item in report["task_reports"]["reaction-to-crystallization"]["checks"]
    }
    assert checks["rate_law_family:explicit_rate_law_change_contract"] is True
    assert checks["rate_law_family:complete_rate_law_change_contract"] is True
    assert checks["rate_law_family:single_declared_reaction_changed"] is True
    assert checks["rate_law_family:semantic_reaction_role_bound"] is True
    assert checks["rate_law_family:declared_rate_law_transform_bound"] is True
    assert checks["rate_law_family:constitutive_domain_parameters_unchanged"] is True
    assert checks["rate_law_family:rate_law_response_certificate_declared"] is True
    assert checks["rate_law_family:bounded_frozen_rate_response"] is True
    assert checks["rate_law_family:frozen_rate_response_crosses_unity"] is True
    assert checks["rate_law_family:decision_relevance:task_primary"] is True
    assert checks["rate_law_family:decision_relevance:leaderboard_score"] is True
    assert checks["rate_law_family:decision_relevance"] is True
    assert checks["topology_family:explicit_topology_change_contract"] is True
    assert checks["topology_family:complete_topology_change_contract"] is True
    assert checks["topology_family:single_declared_topology_channel_added"] is True
    assert checks["topology_family:semantic_topology_role_bound"] is True
    assert checks["topology_family:declared_topology_transform_bound"] is True
    assert checks["topology_family:topology_rate_calibration_bound"] is True
    assert checks["topology_family:topology_domain_parameters_unchanged"] is True
    electro_checks = {
        item["check"]: item["pass"]
        for item in report["task_reports"]["electrochemical-conversion"]["checks"]
    }
    assert electro_checks["constitutive_law_family:explicit_constitutive_change_contract"] is True
    assert electro_checks["constitutive_law_family:complete_constitutive_change_contract"] is True
    assert electro_checks["constitutive_law_family:constitutive_network_unchanged"] is True
    assert electro_checks["constitutive_law_family:declared_constitutive_transform_bound"] is True
    assert electro_checks["constitutive_law_family:constitutive_calibration_bound"] is True


def test_decision_relevance_rejects_visible_but_policy_irrelevant_shift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_metrics(
        _task_id,
        vector,
        *,
        seed,
        observation_seed,
        interventions,
        primary_metric,
    ):
        del seed, observation_seed, primary_metric
        action = int(vector[0])
        baseline = (
            {"task_primary": 1.0, "leaderboard_score": 1.0}
            if action == 0
            else {"task_primary": 0.5, "leaderboard_score": 0.5}
        )
        if not interventions:
            return baseline
        return {key: value - 0.2 for key, value in baseline.items()}

    monkeypatch.setattr(
        "chemworld.eval.mechanism_design_audit._execute_recipe_metrics",
        fake_metrics,
    )
    findings: list[dict[str, object]] = []
    _audit_intervention_decision_relevance(
        findings,
        task_id="reaction-to-crystallization",
        candidate_id="rate_law_family",
        intervention={
            "kind": "mechanism_family",
            "mode": "rate_law_family",
            "severity": 0.8,
        },
        action_library={
            "action-0": np.asarray([0.0]),
            "action-1": np.asarray([1.0]),
        },
        certificate={
            "required": True,
            "required_metric_ids": ["task_primary", "leaderboard_score"],
            "world_seeds": [0, 1],
            "minimum_median_max_metric_effect": 0.01,
            "minimum_median_old_policy_regret": 0.005,
            "minimum_optimal_action_change_rate": 0.5,
        },
        baseline_cache={},
    )
    checks = {str(item["check"]): bool(item["pass"]) for item in findings}
    assert checks["rate_law_family:decision_relevance:task_primary"] is False
    assert checks["rate_law_family:decision_relevance:leaderboard_score"] is False
    assert checks["rate_law_family:decision_relevance"] is False


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


def test_design_audit_rejects_uncovered_reaction_solvent_alternative() -> None:
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
    by_check = {str(item["check"]): item for item in findings}
    assert by_check["material_law_counterfactual:supported_material_field"]["pass"] is True
    assert by_check["material_law_counterfactual:public_operation_allowed"]["pass"] is True
    assert by_check["material_law_counterfactual:moved_indices_publicly_reachable"][
        "pass"
    ] is True
    assert by_check["material_law_counterfactual:moved_indices_recipe_covered"][
        "pass"
    ] is False


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
