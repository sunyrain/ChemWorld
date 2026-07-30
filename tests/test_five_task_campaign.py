from __future__ import annotations

import json
from pathlib import Path

import pytest
from scripts.run_static_s0_five_task_campaign import (
    _build_report,
    _full_protocol,
    _validate_plan,
)

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/benchmark/static_s0_five_task_campaign_20x5_v0.2_dev.json"


def _load(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_five_task_campaign_plan_is_exact_and_valid() -> None:
    plan = _load(PLAN_PATH)
    qualification, protocols = _validate_plan(plan)

    assert plan["world_seeds"] == [0, 1, 2, 3, 4]
    assert plan["development_world_seed"] == 0
    assert plan["held_out_world_seeds"] == [1, 2, 3, 4]
    assert plan["execution_world_seeds"] == [1, 2, 3, 4]
    assert plan["algorithm_seeds"] == [0]
    assert plan["task_ids"] == qualification["task_ids"]
    assert len(plan["task_ids"]) == 5
    assert len(protocols["baseline"]) == len(protocols["participant"]) == 5
    for kind in ("baseline", "participant"):
        for protocol in protocols[kind].values():
            validate_static_optimization_protocol(protocol)
            assert "development_seed_policy" not in protocol
            assert protocol["world_policy"]["evaluation_world_seeds"] == [0, 1, 2, 3, 4]
            assert protocol["candidate_order_seed"] == 0
            assert protocol["observation_noise_namespace"].startswith(
                plan["observation_noise_namespace_base"]
            )


def test_full_protocol_preserves_qualified_task_contracts() -> None:
    plan = _load(PLAN_PATH)
    qualification_path = ROOT / str(plan["qualification_plan_path"])
    qualification = _load(qualification_path)
    assert canonical_json_sha256(qualification) == plan["qualification_plan_sha256"]

    for task_id in plan["task_ids"]:
        baseline = _full_protocol(plan, qualification, task_id, kind="baseline")
        participant = _full_protocol(plan, qualification, task_id, kind="participant")
        assert (
            baseline["reward_contract"]["scoring_contract_id"]
            == (qualification["tasks"][task_id]["scoring_contract_id"])
        )
        assert (
            participant["reward_contract"]["scoring_contract_id"]
            == (qualification["tasks"][task_id]["scoring_contract_id"])
        )
        assert baseline["horizon"] == participant["horizon"] == 20
        assert baseline["validation_budget"] == participant["validation_budget"]
        assert baseline["final_synthesis"]["enabled"] is False
        assert participant["final_synthesis"]["enabled"] is True


def test_shared_participant_method_contains_no_task_specific_hidden_guidance() -> None:
    plan = _load(PLAN_PATH)
    method_path = ROOT / str(plan["participant"]["method_config_path"])
    methods = _load(method_path)
    architecture = methods["architecture_candidate"]

    assert architecture["task_specific_hidden_guidance"] is False
    assert architecture["hidden_world_fields_supplied"] is False
    assert architecture["matching_codes_across_coordinates_have_scientific_meaning"] is False
    assert list(methods["methods"]) == [plan["participant"]["method_id"]]


def test_campaign_report_separates_development_and_held_out_worlds() -> None:
    plan = _load(PLAN_PATH)
    participant_method = str(plan["participant"]["method_id"])
    results: list[dict[str, object]] = []
    for task_id in plan["task_ids"]:
        for method_id, kind in [
            *((
                algorithm_id,
                "baseline",
            ) for algorithm_id in plan["baseline_algorithm_ids"]),
            (participant_method, "participant"),
        ]:
            for world_seed in plan["world_seeds"]:
                score = 0.9 if world_seed == 0 else 0.6 + 0.01 * world_seed
                row: dict[str, object] = {
                    "kind": kind,
                    "task_id": task_id,
                    "world_seed": world_seed,
                    "method_id": method_id,
                    "primary_score": score,
                    "best_exploration_score": score,
                    "completed_experiment_count": 20,
                    "validation_experiment_count": 6,
                    "exact_replay": True,
                    "reused": world_seed == 0,
                }
                if kind == "participant":
                    row.update(
                        {
                            "recommendation_gain_over_incumbent": 0.0,
                            "provider_call_count": 21,
                        }
                    )
                if world_seed == 0:
                    row["provenance"] = "qualified_seed0_import"
                results.append(row)
    qualification = {
        "report_sha256": "qualification-hash",
        "_campaign_source_compatibility": {
            "mode": "ancestor_with_exact_changed_path_allowlist"
        },
    }

    report = _build_report(
        plan,
        qualification_report=qualification,
        source_commit="source-commit",
        results=results,
    )

    participant = report["tasks"][plan["task_ids"][0]]["methods"][participant_method]
    assert participant["development_seed0_blind_validated_score"]["mean"] == 0.9
    assert participant["held_out_blind_validated_score"]["count"] == 4
    assert participant["held_out_blind_validated_score"]["mean"] == pytest.approx(0.625)
    assert participant["blind_validated_score"]["mean"] == pytest.approx(0.68)
    assert report["imported_qualified_seed0_result_count"] == 30
