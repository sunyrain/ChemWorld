from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path
from typing import Any

from chemworld.eval.electrochemical_predictive import (
    SINGLE_STAGE_PREDICTIVE_QUERY_METRICS,
)
from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.static_optimization_protocol import (
    validate_static_optimization_protocol,
)

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK = ROOT / "configs" / "benchmark"
METHODS = ROOT / "configs" / "methods" / "llm_v1.0"

ELECTROCHEMICAL_PROTOCOL = (
    BENCHMARK
    / "scientific_optimization_s0_v1.0_electrochemical_material_opaque_20x10_formal.json"
)
CRYSTALLIZATION_PROTOCOL = (
    BENCHMARK
    / "scientific_optimization_s0_v1.0_crystallization_material_opaque_20x10_formal.json"
)
ELECTROCHEMICAL_BASELINES = (
    BENCHMARK
    / "scientific_optimization_s0_v1.0_electrochemical_classic_baselines_20x10_formal.json"
)
CRYSTALLIZATION_BASELINES = (
    BENCHMARK
    / "scientific_optimization_s0_v1.0_crystallization_classic_baselines_20x10_formal.json"
)
FREEZE_MANIFEST = (
    BENCHMARK / "scientific_optimization_s0_v1.0_freeze_manifest.json"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_campaign_subprocess_logs_do_not_overwrite_each_other(
    tmp_path: Path,
) -> None:
    campaign = runpy.run_path(
        ROOT / "scripts" / "run_static_optimization_s0_v10_campaign.py",
        run_name="static_s0_v10_campaign",
    )
    run_process = campaign["_run_process"]

    run_process(
        [sys.executable, "-c", "print('run')"],
        output=tmp_path,
        log_name="execution_run_log.json",
    )
    run_process(
        [sys.executable, "-c", "print('audit')"],
        output=tmp_path,
        log_name="execution_audit_log.json",
    )

    assert _load(tmp_path / "execution_run_log.json")["stdout"].strip() == "run"
    assert _load(tmp_path / "execution_audit_log.json")["stdout"].strip() == "audit"


def test_v10_participant_protocols_freeze_twenty_rounds_across_ten_worlds() -> None:
    electrochemical = _load(ELECTROCHEMICAL_PROTOCOL)
    crystallization = _load(CRYSTALLIZATION_PROTOCOL)

    for protocol in (electrochemical, crystallization):
        validate_static_optimization_protocol(protocol)
        assert protocol["formal_result"] is True
        assert protocol["benchmark_claim_allowed"] is False
        assert protocol["horizon"] == 20
        assert protocol["scientific_campaign_budget"]["exploration_experiments"] == 20
        assert protocol["world_policy"]["formal_world_seeds"] == list(range(10))
        assert protocol["validation_budget"] == {
            "incumbent_replicates": 3,
            "recommendation_replicates": 3,
            "independent_observation_seeds": True,
            "paired_observation_seeds_across_targets": True,
            "feedback_returned_to_agent": False,
        }
        assert (
            protocol["world_understanding"]["predictive_validation"][
                "total_physical_experiments_per_seed"
            ]
            == 12
        )

    assert (
        electrochemical["world_policy"]["electrochemical_material_family_id"]
        == "nominal-prior-latent-v2"
    )
    assert (
        electrochemical["reward_contract"]["scoring_contract_id"]
        == "electrochemical-s0-balanced-efficiency-v2"
    )
    assert (
        crystallization["world_policy"]["crystallization_material_family_id"]
        == "reaction-crystallization-latent-materials-v1"
    )
    assert (
        crystallization["reward_contract"]["scoring_contract_id"]
        == "reaction-crystallization-s0-balanced-product-v1"
    )


def test_v10_electrochemical_predictive_metrics_match_public_assay() -> None:
    protocol = _load(ELECTROCHEMICAL_PROTOCOL)
    configured = protocol["world_understanding"]["predictive_validation"][
        "metric_ids_by_intervention"
    ]

    assert configured == {
        key: list(value) for key, value in SINGLE_STAGE_PREDICTIVE_QUERY_METRICS.items()
    }
    assert "yield" not in configured["potential_V"]
    assert "conversion" not in configured["current_mA"]


def test_v10_classic_baseline_rosters_are_complete_and_labeled() -> None:
    electrochemical = _load(ELECTROCHEMICAL_BASELINES)
    crystallization = _load(CRYSTALLIZATION_BASELINES)

    for protocol in (electrochemical, crystallization):
        assert protocol["formal_result"] is True
        assert protocol["benchmark_claim_allowed"] is False
        assert protocol["horizon"] == 20
        assert protocol["world_policy"]["formal_world_seeds"] == list(range(10))
        assert protocol["algorithm_seeds"] == list(range(5))
        assert protocol["validation_budget"]["incumbent_replicates"] == 3
        assert protocol["validation_budget"]["recommendation_replicates"] == 3

    assert set(electrochemical["algorithms"]) == {
        "random",
        "lhs",
        "greedy",
        "structured_gp_ei",
        "structured_rf_ei",
        "structured_safe_gp_ei",
        "telemetry_rf_ei",
        "descriptor_gp_ei",
        "descriptor_rf_ei",
        "shuffled_descriptor_gp_ei",
        "shuffled_descriptor_rf_ei",
        "transport_prior_gp_ei",
        "transport_prior_rf_ei",
        "descriptor_telemetry_rf_ei",
    }
    assert set(crystallization["algorithms"]) == {
        "random",
        "lhs",
        "greedy",
        "structured_gp_ei",
        "structured_rf_ei",
        "structured_safe_gp_ei",
        "telemetry_rf_ei",
    }
    for algorithm_id, configuration in electrochemical["algorithms"].items():
        condition = configuration["information_condition"]
        if algorithm_id in {
            "descriptor_gp_ei",
            "descriptor_rf_ei",
            "transport_prior_gp_ei",
            "transport_prior_rf_ei",
            "descriptor_telemetry_rf_ei",
        }:
            assert condition.startswith("privileged_")


def test_v10_codex_subscription_methods_are_preflighted_and_task_bound() -> None:
    pairs = [
        (
            ELECTROCHEMICAL_PROTOCOL,
            METHODS
            / (
                "participant_methods_s0_codex_subscription_sol_"
                "electrochemical_material_opaque_20x10_v10.json"
            ),
        ),
        (
            CRYSTALLIZATION_PROTOCOL,
            METHODS
            / (
                "participant_methods_s0_codex_subscription_sol_"
                "crystallization_material_opaque_20x10_v10.json"
            ),
        ),
    ]
    for protocol_path, methods_path in pairs:
        protocol = _load(protocol_path)
        methods = _load(methods_path)
        assert protocol["method_config_path"] == methods_path.relative_to(ROOT).as_posix()
        assert protocol["method_ids"] == list(methods["methods"])
        method = methods["methods"][protocol["method_ids"][0]]
        assert method["model_id"] == "gpt-5.6-sol"
        assert method["request_configuration"]["reasoning_effort"] == "medium"
        assert (
            method["static_optimization_prompt_budget_contract"]["preflight_status"]
            == "passed_full_20_round_mock_and_exact_replay_2026_07_29"
        )


def test_v10_freeze_manifest_binds_every_protocol_method_and_reference() -> None:
    manifest = _load(FREEZE_MANIFEST)
    assert manifest["world_seeds"] == list(range(10))
    assert manifest["planned_accounting"] == {
        "participant_world_cells": 20,
        "participant_provider_calls": 420,
        "participant_exploration_experiments": 400,
        "participant_predictive_physical_experiments": 240,
        "participant_blind_validation_experiments": 120,
        "participant_total_physical_experiments": 760,
        "baseline_cells": 1050,
        "baseline_exploration_experiments": 21000,
        "baseline_blind_validation_experiments": 6300,
        "baseline_total_physical_experiments": 27300,
        "campaign_total_physical_experiments": 28060,
    }
    for track in manifest["participant_tracks"]:
        for path_field, hash_field in (
            ("protocol_path", "protocol_sha256"),
            ("method_path", "method_sha256"),
            (
                "world_understanding_reference_path",
                "world_understanding_reference_sha256",
            ),
        ):
            assert canonical_json_sha256(_load(ROOT / track[path_field])) == (
                track[hash_field]
            )
    for track in manifest["baseline_tracks"]:
        assert canonical_json_sha256(_load(ROOT / track["protocol_path"])) == (
            track["protocol_sha256"]
        )
