from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_ap_terminal_d1_development_execution as builder
from chemworld.eval.work_ii_ap_terminal_d1_development_execution import (
    AP_D1_PROVIDER_SPECS,
    AP_D1_TASK_SPECS,
    build_all_ap_d1_development_execution_configs,
    build_ap_d1_development_execution_configs,
    validate_ap_d1_development_execution_configs,
    validate_development_execution_config,
)
from chemworld.eval.work_ii_d1_execution import D1_EXECUTION_CONTRACT

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT
    / "workstreams/flagship_tasks/reports/"
    "work-ii-ap-independent-terminal-d1-readiness-v0.1.json"
)


@pytest.mark.parametrize("provider_id", AP_D1_PROVIDER_SPECS)
def test_real_readiness_builds_provider_blocked_seed2_execution_configs(
    provider_id: str,
) -> None:
    configs = build_ap_d1_development_execution_configs(
        ROOT, READINESS, provider_id=provider_id
    )

    assert set(configs) == set(AP_D1_TASK_SPECS)
    for task_id, config in configs.items():
        source_path = str(AP_D1_TASK_SPECS[task_id]["source"])
        assert config["task_id"] == task_id
        assert config["world_seed"] == 2
        assert config["formal_result"] is False
        assert config["campaign"]["complete_experiments"] == 10
        assert config["execution"]["d1_execution_contract"] == D1_EXECUTION_CONTRACT
        assert config["execution"]["failure_semantics"] == (
            "retain cell failures and continue every scheduled seed triplet"
        )
        assert config["execution"]["systemic_failure_semantics"] == (
            "stop only when all three arms fail before the first committed operation"
        )
        assert config["execution"]["pilot_expansion_headroom_fraction"] == 0.20
        assert config["provider"]["session_wall_time_limit_s"] == 6_600.0
        assert config["provider"]["max_recovered_mcp_tool_failures"] == 3
        assert config["provider"]["max_consecutive_mcp_tool_failures"] == 1
        assert config["provider"]["max_provider_error_events"] == 1
        assert config["provider"]["progress_interval_s"] == 30.0
        assert config["provider"]["pre_action_restart_limit"] == 0
        expected_resources = AP_D1_PROVIDER_SPECS[provider_id]["method_resources"]
        assert config["method_resources"]["input_token_limit"] == expected_resources[
            "input_token_limit"
        ]
        assert config["method_resources"]["uncached_input_token_limit"] == (
            expected_resources["uncached_input_token_limit"]
        )
        assert config["method_resources"]["output_token_limit"] == expected_resources[
            "output_token_limit"
        ]
        assert config["method_resources"]["wall_time_limit_s"] == 7_200.0
        assert "resource_status" not in config["method_resources"]
        assert config["qualification"]["max_resource_rejections"] == 1
        assert config["qualification"]["execution_authorized"] is False
        assert config["qualification"]["formal_r5_authorized"] is False
        assert config["independent_terminal_d1"]["readiness_only"] is True
        assert (
            config["independent_terminal_d1"]["source_static_config_path"]
            == source_path
        )
        assert config["independent_terminal_d1"]["readiness_status"] == (
            "ready_static_config_provider_execution_blocked"
        )
        assert validate_development_execution_config(
            config,
            task_id=task_id,
            source_path=source_path,
            provider_id=provider_id,
        ) == []


def test_deepseek_configs_only_change_provider_resources_and_namespaces() -> None:
    configs = build_all_ap_d1_development_execution_configs(ROOT, READINESS)
    assert set(configs) == {"wellau", "deepseek"}
    for task_id in AP_D1_TASK_SPECS:
        wellau = deepcopy(configs["wellau"][task_id])
        deepseek = deepcopy(configs["deepseek"][task_id])
        assert deepseek.pop("provider") == AP_D1_PROVIDER_SPECS["deepseek"]["provider"]
        wellau.pop("provider")
        assert deepseek.pop("method_resources") != wellau.pop("method_resources")
        deepseek.pop("pilot_id")
        deepseek.pop("observation_noise_namespace")
        wellau.pop("pilot_id")
        wellau.pop("observation_noise_namespace")
        assert deepseek == wellau


def test_provider_resource_caps_are_prospectively_distinct() -> None:
    configs = build_all_ap_d1_development_execution_configs(ROOT, READINESS)
    assert (
        AP_D1_PROVIDER_SPECS["deepseek"]["method_resources"]
        != AP_D1_PROVIDER_SPECS["wellau"]["method_resources"]
    )
    for task_id in AP_D1_TASK_SPECS:
        for provider_id in AP_D1_PROVIDER_SPECS:
            observed = configs[provider_id][task_id]["method_resources"]
            expected = AP_D1_PROVIDER_SPECS[provider_id]["method_resources"]
            for field, value in expected.items():
                assert observed[field] == value


def test_deepseek_provider_contract_is_exact() -> None:
    configs = build_ap_d1_development_execution_configs(
        ROOT, READINESS, provider_id="deepseek"
    )
    for config in configs.values():
        assert config["provider"] == AP_D1_PROVIDER_SPECS["deepseek"]["provider"]
        assert config["pilot_id"].endswith("-deepseek-v4-flash")
        assert config["observation_noise_namespace"] == config["pilot_id"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("selected_world_seed", 3),
        ("status", "blocked_fail_closed"),
        ("provider_execution_authorized", True),
    ],
)
def test_builder_rejects_nonexact_readiness_row(
    tmp_path: Path,
    field: str,
    value: object,
) -> None:
    readiness = json.loads(READINESS.read_text(encoding="utf-8"))
    readiness["tasks"][0][field] = value
    path = tmp_path / "readiness.json"
    path.write_text(json.dumps(readiness), encoding="utf-8")

    with pytest.raises(ValueError, match="exact ready seed2 row"):
        build_ap_d1_development_execution_configs(ROOT, path)


def test_validator_rejects_authorization_or_execution_drift() -> None:
    configs = build_ap_d1_development_execution_configs(ROOT, READINESS)
    changed = deepcopy(configs)
    changed["reaction-safety-constrained"]["qualification"][
        "execution_authorized"
    ] = True

    assert validate_ap_d1_development_execution_configs(
        ROOT,
        READINESS,
        changed,
    ) == ["A-P D1 development execution configs differ from deterministic rebuild"]


def test_validator_rejects_deepseek_provider_drift() -> None:
    configs = build_ap_d1_development_execution_configs(
        ROOT, READINESS, provider_id="deepseek"
    )
    changed = deepcopy(configs)
    changed["reaction-safety-constrained"]["provider"]["model"] = "deepseek-v4-pro"

    assert validate_ap_d1_development_execution_configs(
        ROOT,
        READINESS,
        changed,
        provider_id="deepseek",
    ) == ["A-P D1 development execution configs differ from deterministic rebuild"]


def test_builder_rejects_static_scientific_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_path = (
        ROOT
        / "configs/benchmark/"
        "work_ii_reaction_safety_independent_terminal_d1_seed2.json"
    ).resolve()
    original_load = builder._load

    def drifted_load(path: Path) -> dict[str, object]:
        value = original_load(path)
        if path.resolve() == source_path:
            value["snapshot_stages"] = ["pre_evidence", "final"]
        return value

    monkeypatch.setattr(builder, "_load", drifted_load)
    with pytest.raises(ValueError, match="scientific config differs"):
        build_ap_d1_development_execution_configs(ROOT, READINESS)
