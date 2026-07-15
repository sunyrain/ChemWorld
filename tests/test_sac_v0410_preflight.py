from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
import scripts.run_sac_v048_preflight as preflight

ROOT = Path(__file__).resolve().parents[1]
PARENT_PLAN_PATH = ROOT / "configs/methods/rl_v0.4/sac_v049_preflight_plan.json"
PLAN_PATH = ROOT / "configs/methods/rl_v0.4/sac_v0410_preflight_plan.json"
DIAGNOSTIC_PATH = ROOT / "workstreams/benchmark_v1/reports/rl-sac-v049-preflight-v0.4.json"


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_public_schema_reattestation_keeps_scientific_settings_and_is_namespaced() -> None:
    parent = _load(PARENT_PLAN_PATH)
    plan = _load(PLAN_PATH)
    protocol = _load(ROOT / str(plan["formal_protocol_path"]))

    checks = preflight.validate_plan(plan, protocol)
    evidence = preflight.validate_adapter_reattestation(ROOT, plan)

    assert all(checks.values())
    assert plan["schema_version"] == preflight.PUBLIC_SCHEMA_ADAPTER_PLAN_VERSION
    assert preflight.scientific_contract_sha256(parent) == preflight.scientific_contract_sha256(
        plan
    )
    assert plan["comparison"] == parent["comparison"]
    assert plan["development_evaluation"] == parent["development_evaluation"]
    assert plan["gate"] == parent["gate"]
    assert plan["comparability_boundary"]["action_adapter_schema_version"].endswith("0.2")
    assert "post-affordance-v0410" in plan["writer_gate_path"]
    assert evidence["sac_adapter_diagnostic"]["full_matrix_allowed"] is False
    assert evidence["ppo_infrastructure_failure"]["observed_work"][
        "training_environment_step_count"
    ] == 0


def test_reattestation_rejects_tampered_v049_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    plan = _load(PLAN_PATH)
    real_load = preflight._load_object

    def tampered_load(path: Path, label: str) -> dict[str, Any]:
        payload = real_load(path, label)
        if path.resolve() == DIAGNOSTIC_PATH.resolve():
            payload = copy.deepcopy(payload)
            payload["source"]["source_commit"] = "0" * 40
        return payload

    monkeypatch.setattr(preflight, "_load_object", tampered_load)
    with pytest.raises(preflight.SACPreflightError, match="sac_source"):
        preflight.validate_adapter_reattestation(ROOT, plan)
