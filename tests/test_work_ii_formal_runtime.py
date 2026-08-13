from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

import chemworld.eval.work_ii_formal_runtime as formal_runtime
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_resource_calibration_v02 import (
    EXPECTED_PATTERN_KEYS,
    _materialize_runtime_config,
    pattern_slug,
)
from chemworld.eval.work_ii_task_resources import build_task_resource_formula_binding

ROOT = Path(__file__).resolve().parents[1]
SOURCE_BY_KEY = {
    ("A_E", "electrochemical-conversion", 8): "configs/benchmark/work_ii_campaign_pilot.json",
    ("A_E", "reaction-to-crystallization", 8): (
        "configs/benchmark/work_ii_crystallization_campaign.json"
    ),
    ("A_E", "reaction-to-distillation", 8): "configs/benchmark/work_ii_distillation_campaign.json",
    ("A_E", "partition-discovery", 8): "configs/benchmark/work_ii_partition_campaign.json",
    ("A_E", "reaction-safety-constrained", 8): "configs/benchmark/work_ii_safety_campaign.json",
    ("A_P", "reaction-safety-constrained", 10): (
        "configs/benchmark/work_ii_reaction_safety_matched_prior_d1.json"
    ),
    ("A_P", "electrochemical-conversion", 10): (
        "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json"
    ),
    ("A_S", "partition-discovery", 12): "configs/benchmark/work_ii_as_partition_d1_v0.1.json",
    ("A_S", "reaction-to-crystallization", 12): (
        "configs/benchmark/work_ii_as_crystallization_d1_v0.1.json"
    ),
}


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def _card(config: dict[str, object], key: tuple[str, str, int], path: str) -> dict[str, object]:
    locus, task_id, rounds = key
    card: dict[str, object] = {
        "card_identity": {
            "locus": locus,
            "task_id": task_id,
            "rounds": rounds,
            "world_seed": 0,
            "calibration_campaign_binding": {
                "path": path,
                "sha256": "1" * 64,
            },
            "resource_formula_binding": build_task_resource_formula_binding(config),
        },
        "protected_closeout_reserve_enforced": True,
        "proposed_hard_caps": {
            "operation_attempt_limit": 150,
            "protected_closeout_operation_reserve": 20,
            "process_time_limit_s": 50_000.0,
            "protected_closeout_reserve_s": 5_000.0,
            "input_token_limit": 9_000_000,
            "uncached_input_token_limit": 900_000,
            "output_token_limit": 90_000,
            "provider_wall_time_limit_s": 8_000.0,
            "currency_ceiling_usd": 20.0,
        },
        "currency_accounting": {"status": "observed_attributable_usd"},
    }
    card["card_sha256"] = canonical_json_sha256(card)
    return card


def _inputs(tmp_path: Path) -> tuple[Path, Path, Path, dict[str, object]]:
    root = tmp_path / "repo"
    patterns = []
    cards = []
    for key in EXPECTED_PATTERN_KEYS:
        locus, task_id, rounds = key
        source = json.loads((ROOT / SOURCE_BY_KEY[key]).read_text(encoding="utf-8"))
        config = _materialize_runtime_config(
            source,
            locus=locus,
            task_id=task_id,
            rounds=rounds,
        )
        slug = pattern_slug({"locus": locus, "task_id": task_id, "rounds": rounds})
        relative = f"normalized/{slug}.json"
        path = root / relative
        _write(path, config)
        patterns.append(
            {
                "locus": locus,
                "task_id": task_id,
                "rounds": rounds,
                "campaign_config_binding": {
                    "path": relative,
                    "sha256": file_sha256(path),
                },
            }
        )
        cards.append(_card(config, key, relative))
    manifest = {"patterns": patterns}
    summary: dict[str, object] = {
        "status": "passed",
        "calibration_passed": True,
        "method_qualification_may_be_authorized": True,
        "resource_card_proposals": cards,
    }
    design = {"schema_version": "chemworld-work-ii-formal-design-0.2"}
    manifest_path = root / "w2-26-manifest.json"
    summary_path = root / "w2-26-summary.json"
    design_path = root / "formal-design.json"
    _write(manifest_path, manifest)
    _write(summary_path, summary)
    _write(design_path, design)
    return manifest_path, summary_path, design_path, summary


@pytest.fixture(autouse=True)
def _accept_synthetic_w2_26(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(formal_runtime, "validate_w2_26_manifest", lambda *_: [])
    monkeypatch.setattr(formal_runtime, "validate_w2_26_summary", lambda *_args, **_kwargs: [])


def test_materializes_exact_nine_provider_free_configs(tmp_path: Path) -> None:
    manifest_path, summary_path, design_path, _ = _inputs(tmp_path)
    root = manifest_path.parent
    output = root / "formal-runtime-v0.1"

    manifest = formal_runtime.build_formal_runtime_manifest(
        root,
        w2_26_manifest_path=manifest_path,
        w2_26_summary_path=summary_path,
        formal_design_path=design_path,
        output_root=output,
    )

    assert manifest["provider_calls_executed"] == 0
    assert len(manifest["task_configs"]) == 9
    assert (
        formal_runtime.validate_formal_runtime_manifest(
            root, manifest, manifest_path=output / "manifest.json"
        )
        == []
    )
    for row in manifest["task_configs"]:
        config = json.loads(
            (root / row["formal_campaign_config_binding"]["path"]).read_text(encoding="utf-8")
        )
        assert row["formal_campaign_config_binding"].get("sha256") is None
        assert len(row["formal_campaign_config_binding"]["canonical_json_sha256"]) == 64
        assert config["method_resources"]["model_call_limit"] == 2
        assert config["provider"]["accepted_turn_continuation_limit"] == 1
        assert config["provider"]["provider_process_attempt_limit"] == 3
        assert config["qualification"]["resource_calibration_status"] == (
            "passed_w2_26_task_specific"
        )

    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        formal_runtime.build_formal_runtime_manifest(
            root,
            w2_26_manifest_path=manifest_path,
            w2_26_summary_path=summary_path,
            formal_design_path=design_path,
            output_root=output,
        )


def test_validator_rejects_config_identity_drift(tmp_path: Path) -> None:
    manifest_path, summary_path, design_path, _ = _inputs(tmp_path)
    root = manifest_path.parent
    output = root / "formal-runtime-v0.1"
    manifest = formal_runtime.build_formal_runtime_manifest(
        root,
        w2_26_manifest_path=manifest_path,
        w2_26_summary_path=summary_path,
        formal_design_path=design_path,
        output_root=output,
    )
    first = manifest["task_configs"][0]["formal_campaign_config_binding"]
    config_path = root / first["path"]
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["formal_runtime_identity"]["rounds"] = 99
    _write(config_path, config)
    first["canonical_json_sha256"] = canonical_json_sha256(config)
    manifest["manifest_sha256"] = formal_runtime.formal_runtime_manifest_sha256(manifest)

    assert any(
        "formal runtime config identity differs" in error
        for error in formal_runtime.validate_formal_runtime_manifest(root, manifest)
    )


@pytest.mark.parametrize("mutation", ["missing", "duplicate"])
def test_rejects_incomplete_or_duplicate_cards(tmp_path: Path, mutation: str) -> None:
    manifest_path, summary_path, design_path, summary = _inputs(tmp_path)
    cards = deepcopy(summary["resource_card_proposals"])
    if mutation == "missing":
        cards.pop()
    else:
        cards[-1] = deepcopy(cards[0])
    summary["resource_card_proposals"] = cards
    _write(summary_path, summary)

    with pytest.raises(ValueError, match="nine unique task cards"):
        formal_runtime.build_formal_runtime_manifest(
            manifest_path.parent,
            w2_26_manifest_path=manifest_path,
            w2_26_summary_path=summary_path,
            formal_design_path=design_path,
            output_root=manifest_path.parent / "formal-runtime-v0.1",
        )
