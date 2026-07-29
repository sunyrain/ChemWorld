from __future__ import annotations

import json
from pathlib import Path

from scripts.run_static_s0_five_task_campaign import _full_protocol, _validate_plan

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "configs/benchmark/static_s0_five_task_campaign_20x5_v0.1_dev.json"


def _load(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_five_task_campaign_plan_is_exact_and_valid() -> None:
    plan = _load(PLAN_PATH)
    qualification, protocols = _validate_plan(plan)

    assert plan["world_seeds"] == [0, 1, 2, 3, 4]
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
