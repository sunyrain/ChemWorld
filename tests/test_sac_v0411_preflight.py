from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
import scripts.run_sac_v048_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
PARENT_PLAN_PATH = ROOT / "configs/methods/rl_v0.4/sac_v0410_preflight_plan.json"
PLAN_PATH = ROOT / "configs/methods/rl_v0.4/sac_v0411_preflight_plan.json"
NEGATIVE_REPORT_PATH = (
    ROOT / "workstreams/benchmark_v1/reports/rl-ppo-v0410-preflight-v0.4.json"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_public_precondition_retry_is_frozen_namespaced_and_deferred() -> None:
    parent = _load(PARENT_PLAN_PATH)
    plan = _load(PLAN_PATH)
    protocol = _load(ROOT / str(plan["formal_protocol_path"]))

    checks = preflight.validate_plan(plan, protocol)
    evidence = preflight.validate_adapter_reattestation(ROOT, plan)

    assert all(checks.values())
    assert plan["schema_version"] == preflight.PUBLIC_PRECONDITION_PLAN_VERSION
    assert preflight.scientific_contract_sha256(parent) == preflight.scientific_contract_sha256(
        plan
    )
    assert plan["comparison"] == parent["comparison"]
    assert plan["development_evaluation"] == parent["development_evaluation"]
    assert plan["gate"] == parent["gate"]
    assert plan["adapter_reattestation"]["conditional_hybrid_action_schema_version"].endswith(
        "0.3"
    )
    assert plan["adapter_reattestation"]["sac_v0410_execution_skipped"] is True
    assert "public-preconditions-v0411" in plan["writer_gate_path"]
    assert evidence["ppo_v0410_negative_report"]["full_matrix_allowed"] is False

    full_plan = _load(ROOT / str(plan["execution"]["full_training_plan"]))
    assert full_plan["current_contract_preflight"]["plan"] == PLAN_PATH.relative_to(
        ROOT
    ).as_posix()
    assert full_plan["current_contract_preflight"]["required_status"] == (
        "sac_v0411_preflight_passed_full_matrix_allowed"
    )


def test_public_precondition_retry_rejects_tampered_parent_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = _load(PLAN_PATH)
    real_load = preflight._load_object

    def tampered_load(path: Path, label: str) -> dict[str, Any]:
        payload = real_load(path, label)
        if path.resolve() == NEGATIVE_REPORT_PATH.resolve():
            payload = copy.deepcopy(payload)
            payload["source"]["source_commit"] = "0" * 40
        return payload

    monkeypatch.setattr(preflight, "_load_object", tampered_load)
    with pytest.raises(preflight.SACPreflightError, match="negative_report_source"):
        preflight.validate_adapter_reattestation(ROOT, plan)
