from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_resource_calibration import (
    build_task_resource_formula_binding,
    materialize_task_resource_caps,
    resolve_task_resource_card,
    validate_task_resource_card,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json"


def _source() -> dict[str, object]:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    source["qualification"]["maximum_exact_repeats"] = 2
    return source


def _card(source: dict[str, object]) -> dict[str, object]:
    card: dict[str, object] = {
        "card_identity": {
            "rounds": 10,
            "locus": "A_P",
            "task_id": "electrochemical-conversion",
            "world_seed": 0,
            "calibration_campaign_binding": {
                "path": "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json",
                "sha256": "1" * 64,
                "config_canonical_json_sha256": canonical_json_sha256(source),
            },
            "resource_formula_binding": build_task_resource_formula_binding(source),
        },
        "protected_closeout_reserve_enforced": True,
        "proposed_hard_caps": {
            "operation_attempt_limit": 123,
            "protected_closeout_operation_reserve": 24,
            "process_time_limit_s": 50_000.0,
            "protected_closeout_reserve_s": 5_000.0,
            "input_token_limit": 9_000_000,
            "uncached_input_token_limit": 900_000,
            "output_token_limit": 90_000,
            "provider_wall_time_limit_s": 8_000.0,
            "currency_ceiling_usd": 20.0,
        },
    }
    card["card_sha256"] = canonical_json_sha256(card)
    return card


def test_task_resource_card_materializes_every_executable_cap() -> None:
    source = _source()
    card = _card(source)
    assert validate_task_resource_card(card) == []
    config = materialize_task_resource_caps(source, card)

    assert config["campaign"]["operation_attempt_limit"] == 123
    assert config["campaign"]["process_time_limit_s"] == 50_000.0
    assert config["campaign"]["process_time_policy"]["protected_reserve_s"] == 5_000.0
    assert (
        config["campaign"]["closeout_policy"][
            "final_assay_path_total_operation_reserve"
        ]
        == 24
    )
    assert (
        config["campaign"]["closeout_policy"]["policy"]
        == "protected_closeout_reserve_enforced"
    )
    assert config["campaign"]["closeout_policy"][
        "allowed_operation_classes"
    ] == ["discard_batch", "final_assay", "quench", "terminate", "transfer"]
    assert build_task_resource_formula_binding(config) == card["card_identity"][
        "resource_formula_binding"
    ]
    assert config["method_resources"]["operation_limit"] == 123
    assert config["method_resources"]["input_token_limit"] == 9_000_000
    assert config["method_resources"]["uncached_input_token_limit"] == 900_000
    assert config["method_resources"]["output_token_limit"] == 90_000
    assert config["method_resources"]["wall_time_limit_s"] == 8_000.0
    assert config["provider"]["session_wall_time_limit_s"] == 8_000.0
    assert config["qualification"]["maximum_exact_repeats"] == 2
    assert (
        config["qualification"]["resource_calibration_status"]
        == "passed_w2_26_task_specific"
    )
    assert config["calibrated_currency_ceiling_usd"] == 20.0
    assert source["campaign"]["operation_attempt_limit"] == 110


def test_task_resource_card_rejects_cross_task_and_formula_drift() -> None:
    source = _source()
    card = _card(source)
    summary = {
        "status": "passed",
        "calibration_passed": True,
        "resource_card_proposals": [card],
    }
    resolved = resolve_task_resource_card(
        summary,
        rounds=10,
        locus="A_P",
        task_id="electrochemical-conversion",
        formal_source_config=source,
        formal_source_binding={
            "path": "formal.json",
            "sha256": "2" * 64,
            "config_canonical_json_sha256": canonical_json_sha256(source),
        },
    )
    assert resolved == card

    drifted = deepcopy(source)
    drifted["campaign"]["process_time_policy"]["repeat_allowance_s"] += 1.0
    with pytest.raises(ValueError, match="resource formula"):
        resolve_task_resource_card(
            summary,
            rounds=10,
            locus="A_P",
            task_id="electrochemical-conversion",
            formal_source_config=drifted,
        )
    with pytest.raises(ValueError, match="exactly one task resource card"):
        resolve_task_resource_card(
            summary,
            rounds=10,
            locus="A_P",
            task_id="reaction-safety-constrained",
            formal_source_config=source,
        )


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("campaign", "vessel_start_limit"),
        ("campaign", "final_assay_limit"),
        ("campaign", "nonfinal_instrument_use_limit"),
        ("campaign", "stock_limits"),
        ("campaign", "operation_repeat_limits"),
        ("method_resources", "model_call_limit"),
        ("method_resources", "training_environment_step_limit"),
        ("qualification", "maximum_exact_repeats"),
        ("provider", "model"),
    ],
)
def test_task_resource_formula_rejects_design_limit_drift(
    section: str, field: str
) -> None:
    source = _source()
    card = _card(source)
    drifted = deepcopy(source)
    value = drifted[section][field]
    if isinstance(value, int):
        drifted[section][field] = value + 1
    elif isinstance(value, dict):
        drifted[section][field] = {**value, "drift_probe": 1}
    else:
        drifted[section][field] = f"{value}-drift"
    with pytest.raises(ValueError, match="resource formula"):
        materialize_task_resource_caps(drifted, card)


def test_observed_zero_repeats_do_not_change_repeat_design() -> None:
    source = _source()
    card = _card(source)
    card["observed_maxima"] = {"exact_repeat_count": 0}
    card["card_sha256"] = canonical_json_sha256(
        {key: value for key, value in card.items() if key != "card_sha256"}
    )
    config = materialize_task_resource_caps(source, card)
    assert config["qualification"]["maximum_exact_repeats"] == 2


def test_card_rejects_repeat_design_as_a_measured_cap() -> None:
    source = _source()
    card = _card(source)
    card["proposed_hard_caps"]["maximum_exact_repeats"] = 1
    card["card_sha256"] = canonical_json_sha256(
        {key: value for key, value in card.items() if key != "card_sha256"}
    )
    assert validate_task_resource_card(card) == [
        "resource card must not redefine the exact-repeat design invariant"
    ]
