from __future__ import annotations

import copy
import json
from pathlib import Path

from chemworld.eval.mechanism_adaptation import (
    load_mechanism_adaptation_protocol,
)
from chemworld.eval.mechanism_preregistration import (
    validate_mechanism_preregistration,
)

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = (
    ROOT / "configs/benchmark/mechanism_adaptation_v0.3.0.json"
)
PLAN_PATH = (
    ROOT / "configs/benchmark/mechanism_adaptation_gate_a_v0.3.0.json"
)


def _bound_inputs() -> tuple[dict, dict, dict, dict, dict]:
    protocol = load_mechanism_adaptation_protocol(PROTOCOL_PATH)
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    relation_graph = json.loads(
        (ROOT / plan["diagnostic_relation_graph"]["report"]).read_text(
            encoding="utf-8"
        )
    )
    sample_size = json.loads(
        (ROOT / plan["sample_size_audit"]["report"]).read_text(
            encoding="utf-8"
        )
    )
    manifest = json.loads(
        (ROOT / plan["preregistration"]["manifest"]).read_text(
            encoding="utf-8"
        )
    )
    return protocol, plan, relation_graph, sample_size, manifest


def test_rc24_sample_size_audit_uses_independent_world_clusters() -> None:
    _protocol, plan, _graph, sample_size, _manifest = _bound_inputs()

    assert sample_size["pass"] is True
    assert sample_size["selected_independent_world_clusters_per_family"] == 180
    assert sample_size["clusters_per_changed_family_per_change_time"] == 60
    assert sample_size["provider_repeat_role"] == "nested_technical_replicate"
    assert (
        sample_size["selected_design"][
            "reference_wilson_pass_probability"
        ]["0.9"]
        >= plan["sample_size_audit"][
            "minimum_power_at_true_reference_success_0.90"
        ]
    )


def test_rc24_preregistration_is_current_and_hash_bound() -> None:
    protocol, plan, relation_graph, sample_size, manifest = _bound_inputs()

    assert (
        validate_mechanism_preregistration(
            manifest,
            repository_root=ROOT,
            protocol=protocol,
            plan=plan,
            relation_graph=relation_graph,
            sample_size_audit=sample_size,
        )
        == []
    )
    assert (
        manifest["certification_subjects"]["a3"]
        == "frozen_reference_diagnostic_policy"
    )
    assert manifest["certification_subjects"]["gates_b_to_e"] == "participant_agent"
    assert manifest["statistics"]["pooled_micro_average_controls_gate"] is False


def test_rc24_preregistration_rejects_threshold_drift() -> None:
    protocol, plan, relation_graph, sample_size, manifest = _bound_inputs()
    changed_plan = copy.deepcopy(plan)
    changed_plan["online_attainability_certificate"][
        "frozen_pass_criteria"
    ]["change_decision_probability_threshold"] = 0.6

    errors = validate_mechanism_preregistration(
        manifest,
        repository_root=ROOT,
        protocol=protocol,
        plan=changed_plan,
        relation_graph=relation_graph,
        sample_size_audit=sample_size,
    )

    assert errors == [
        "preregistration manifest is stale or differs from its bound inputs"
    ]
