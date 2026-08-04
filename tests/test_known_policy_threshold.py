from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from scripts.qualify_work_i_known_policy_threshold import build_markdown

from chemworld.eval.known_policy_contract import FORMAL_WORLD_SEEDS, INFORMATION_ARMS
from chemworld.eval.known_policy_threshold import (
    QUALIFICATION_WORLD_SEEDS,
    branch_counts,
    midpoint_candidates,
    qualification_report_sha256,
    select_threshold,
    source_manifest,
    stable_numeric_payload,
    threshold_binding_sha256,
    validate_qualification_report,
    validate_threshold_binding,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-known-policy-threshold-qualification-v0.1.json"
)
BINDING_PATH = ROOT / "configs/benchmark/work_i_known_policy_threshold_v0.1.json"
MARKDOWN_PATH = (
    ROOT
    / "workstreams/arxiv_v1/reports/"
    "work-i-known-policy-threshold-qualification-v0.1.md"
)


def _frozen() -> tuple[dict, dict]:
    return (
        json.loads(REPORT_PATH.read_text(encoding="utf-8")),
        json.loads(BINDING_PATH.read_text(encoding="utf-8")),
    )


def test_midpoint_candidates_are_unique_sorted_and_finite() -> None:
    assert midpoint_candidates([0.8, 0.1, 0.2, 0.2]) == pytest.approx((0.15, 0.5))
    assert midpoint_candidates([0.2, 0.2]) == ()
    with pytest.raises(ValueError, match="finite"):
        midpoint_candidates([0.1, float("nan")])


def test_report_only_numeric_canonicalization_removes_runtime_float_tails() -> None:
    assert stable_numeric_payload(0.1729546623067752) == (
        stable_numeric_payload(0.17295466230677525)
    )
    assert stable_numeric_payload(0.0756997692454747) == (
        stable_numeric_payload(0.0756997692454748)
    )
    assert stable_numeric_payload({"x": [1.0e-18, -0.0]}) == {
        "x": [0.0, 0.0]
    }


def test_selector_applies_admissibility_median_and_lower_tie_break() -> None:
    signals = {
        INFORMATION_ARMS[0]: [0.1, 0.2, 0.8],
        INFORMATION_ARMS[1]: [0.1, 0.2, 0.8],
    }
    selection = select_threshold(signals)
    assert selection["pooled_median"] == 0.2
    assert selection["selected_threshold"] == pytest.approx(0.15)
    assert selection["selected_branch_counts_by_arm"] == {
        arm: {"discard": 1, "continue_and_assay": 2}
        for arm in INFORMATION_ARMS
    }
    assert branch_counts([0.1, 0.2, 0.8], 0.15) == {
        "discard": 1,
        "continue_and_assay": 2,
    }


def test_qualification_worlds_are_disjoint_and_frozen_report_passes() -> None:
    report, binding = _frozen()
    assert set(QUALIFICATION_WORLD_SEEDS).isdisjoint(FORMAL_WORLD_SEEDS)
    assert report["qualification_world_seeds"] == list(QUALIFICATION_WORLD_SEEDS)
    assert report["formal_world_seeds_excluded"] == list(FORMAL_WORLD_SEEDS)
    assert report["status"] == "qualified_and_frozen"
    assert all(report["checks"].values())
    assert report["counts"] == {
        "original_actions": 360,
        "original_campaigns": 10,
        "original_signals": 60,
        "provider_calls": 0,
        "replay_actions": 360,
        "replay_campaigns": 10,
        "replay_signals": 60,
    }
    assert validate_qualification_report(report) == []
    assert validate_threshold_binding(binding, report) == []


def test_frozen_hashes_source_manifest_and_human_report_are_consistent() -> None:
    report, binding = _frozen()
    assert report["report_sha256"] == qualification_report_sha256(report)
    assert binding["binding_sha256"] == threshold_binding_sha256(binding)
    assert binding["qualification_report_sha256"] == report["report_sha256"]
    current_sources = source_manifest(ROOT)
    changed_paths = {
        path
        for path, digest in current_sources.items()
        if report["source_manifest"].get(path) != digest
    }
    assert changed_paths == {"src/chemworld/runtime/electrochemical_services.py"}
    assert current_sources["src/chemworld/runtime/electrochemical_services.py"] == (
        "e6c6f9a9ad6cc39ef7838d16ec50adaf107079f986d86f0fb599bb7e559ab46b"
    )
    assert MARKDOWN_PATH.read_text(encoding="utf-8") == build_markdown(
        report, binding
    )


def test_integrity_validators_reject_threshold_and_gate_tampering() -> None:
    report, binding = _frozen()
    bad_report = deepcopy(report)
    bad_report["checks"]["all_exact_replays_match"] = False
    assert "one or more qualification gates failed" in validate_qualification_report(
        bad_report
    )

    bad_binding = deepcopy(binding)
    bad_binding["threshold"] = float(binding["threshold"]) + 0.01
    errors = validate_threshold_binding(bad_binding, report)
    assert "threshold value disagrees with qualification selection" in errors
    assert "threshold binding hash mismatch" in errors
