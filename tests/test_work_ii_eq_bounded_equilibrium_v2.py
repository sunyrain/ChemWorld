from __future__ import annotations

import copy
from pathlib import Path

import pytest
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq


def valid_eqs() -> dict:
    return {
        "effective_pka": {
            "identifiable": True,
            "estimate": 5.0,
            "lower80": 4.8,
            "upper80": 5.2,
            "rationale": "The estimate follows from observed dilution contrasts.",
        },
        "path_dependence": {
            "assessment": "final_state_dominant",
            "rationale": "Matched final states agreed within the observed noise.",
        },
        "dissociation_precipitation": {
            "assessment": "continuous",
            "supported_range": "The tested loading and volume range only.",
            "competing_explanation": (
                "A weak threshold blurred by observation noise remains possible."
            ),
        },
    }


def test_v2_is_one_p_locus_five_worlds_three_arms_and_four_posttests() -> None:
    config = eq.load_config()
    validated = eq.validate_design(config)

    assert config["prior_locus"] == "P"
    assert config["posttest_stages"] == list(eq.POSTTEST_STAGES)
    assert config["counts"]["posttests"] == 60
    assert len(validated["schedule"]) == 15


def test_v2_prompts_require_english_and_preserve_stage_order() -> None:
    assert "所有报告文本必须使用英文" in eq.K1
    assert "所有rationale和其他自由文本字段必须使用英文" in eq.Q_PROMPT
    assert "report内容必须使用英文" in eq.K2
    assert "K1, Q, and K2 are sealed" in eq.EQS
    assert eq.POSTTEST_STAGES == ("K1", "Q", "K2", "EQS")


def test_eqs_validation_accepts_estimate_or_complete_abstention() -> None:
    payload = valid_eqs()
    assert eq.validate_posttest("EQS", payload, ())["valid"]

    abstention = copy.deepcopy(payload)
    abstention["effective_pka"].update(
        {"identifiable": False, "estimate": None, "lower80": None, "upper80": None}
    )
    assert eq.validate_posttest("EQS", abstention, ())["valid"]


def test_eqs_validation_rejects_bad_interval_enum_and_non_english_text() -> None:
    interval = valid_eqs()
    interval["effective_pka"]["lower80"] = 5.1
    assert not eq.validate_posttest("EQS", interval, ())["valid"]

    enum = valid_eqs()
    enum["path_dependence"]["assessment"] = "maybe"
    assert not eq.validate_posttest("EQS", enum, ())["valid"]

    language = valid_eqs()
    language["dissociation_precipitation"]["supported_range"] = "中文"
    assert not eq.validate_posttest("EQS", language, ())["valid"]


def test_eqs_evaluation_scores_only_registered_pka_fields() -> None:
    result = eq.evaluate_eqs(valid_eqs(), 5.1)

    assert result["valid"]
    assert result["absolute_error"] == pytest.approx(0.1)
    assert result["covered80"] is True
    assert result["structural_labels_scored"] is False


def test_v2_freeze_fails_closed_before_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    gate = tmp_path / "provider-free-gate" / "gate.json"
    eq.write(gate, {"passed": True, "config_sha256": eq.file_sha256(eq.CONFIG)})
    monkeypatch.setattr(eq, "FREEZE", tmp_path / "absent.json")

    with pytest.raises(RuntimeError, match="freeze manifest is absent"):
        eq.validate_freeze(tmp_path, eq.load_config())
