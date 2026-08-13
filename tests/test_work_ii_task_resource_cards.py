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
    return json.loads(SOURCE.read_text(encoding="utf-8"))


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
            },
            "resource_formula_binding": build_task_resource_formula_binding(source),
        },
        "protected_closeout_reserve_enforced": True,
        "proposed_hard_caps": {
            "operation_attempt_limit": 123,
            "protected_closeout_operation_reserve": 24,
            "maximum_exact_repeats": 2,
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
        formal_source_binding={"path": "formal.json", "sha256": "2" * 64},
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
