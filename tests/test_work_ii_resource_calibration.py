from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest
import scripts.run_work_ii_campaign_pilot as campaign_runner
import scripts.run_work_ii_resource_calibration as calibration_runner

import chemworld.eval.work_ii_resource_calibration as calibration_module
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.work_ii_c2_admission import build_c2_selection_protocol
from chemworld.eval.work_ii_resource_calibration import (
    RESOURCE_CALIBRATION_ARMS,
    RESOURCE_CALIBRATION_Q2_GENERATION_VERSION,
    build_resource_calibration_authorization,
    build_resource_calibration_execution_manifest,
    build_resource_calibration_readiness,
    build_resource_calibration_summary,
    empty_resource_calibration_summary,
    resolve_resource_calibration_representatives,
    resource_calibration_summary_sha256,
    validate_resource_calibration_authorization,
    validate_resource_calibration_manifest,
    validate_resource_calibration_readiness,
    validate_resource_calibration_summary,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "configs/benchmark/work_ii_resource_calibration_manifest_v0.1.json"
RUNNER = ROOT / "scripts/run_work_ii_resource_calibration.py"


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


@pytest.fixture
def repo_tmp_path(monkeypatch: pytest.MonkeyPatch):
    path = Path(tempfile.mkdtemp(prefix=".pytest-resource-calibration-", dir=ROOT))
    monkeypatch.setattr(
        calibration_module,
        "DEFAULT_RESOURCE_CALIBRATION_FORMAL_DESIGN",
        (path / "formal-design-v0.2.json").relative_to(ROOT),
    )
    monkeypatch.setattr(
        calibration_module,
        "DEFAULT_RESOURCE_CALIBRATION_SELECTION_PROTOCOLS",
        {
            locus: (path / f"{locus.lower()}-selection.json").relative_to(ROOT)
            for locus in ("A_P", "A_S")
        },
    )
    monkeypatch.setattr(
        calibration_module,
        "DEFAULT_RESOURCE_CALIBRATION_Q2_GENERATION_RECORDS",
        {
            locus: (path / f"{locus.lower()}-q2-generation.json").relative_to(ROOT)
            for locus in ("A_P", "A_S")
        },
    )
    monkeypatch.setattr(
        calibration_module,
        "_validate_as_q2_record",
        lambda _root, record, *, task_id: (
            [] if record.get("task_id") == task_id else ["A_S task mismatch"],
            record.get("generated_d1_config"),
        ),
    )
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _future_manifest(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    manifest = _manifest()
    config_paths: dict[int, Path] = {}
    for pattern in manifest["patterns"]:
        rounds = pattern["rounds"]
        config = json.loads(
            (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(
                encoding="utf-8"
            )
        )
        config["pilot_id"] = f"future-calibration-{rounds}"
        config["task_id"] = f"future-{pattern['locus'].lower()}-{rounds}"
        config["world_seed"] = rounds
        config["campaign"]["complete_experiments"] = rounds
        config["campaign"]["checkpoint_complete_experiments"] = (
            pattern["checkpoint_complete_experiments"]
        )
        config["method_resources"]["complete_experiment_limit"] = rounds
        config["method_resources"]["checkpoint_complete_experiments"] = (
            pattern["checkpoint_complete_experiments"][1:]
        )
        config["qualification"] = {"q2_passed": True}
        config_path = tmp_path / f"campaign-{rounds}.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        config_paths[rounds] = config_path
        pattern["representative_task_status"] = "frozen"
        pattern["task_id"] = config["task_id"]
        pattern["world_seed"] = rounds
        pattern["task_specific_resource_formula_frozen"] = True
        pattern["campaign_config_binding"] = {
            "path": config_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(config_path),
            "hash_kind": "file_sha256",
        }
    design = {
        "schema_version": "chemworld-work-ii-formal-design-0.2",
        "tasks": [
            {
                "task_id": manifest["patterns"][0]["task_id"],
                "campaign_config": config_paths[8].relative_to(ROOT).as_posix(),
            }
        ],
    }
    design_path = tmp_path / "formal-design-v0.2.json"
    design_path.write_text(json.dumps(design), encoding="utf-8")
    protocol_paths: dict[str, Path] = {}
    q2_paths: dict[str, Path] = {}
    for rounds, locus in ((10, "A_P"), (12, "A_S")):
        task_id = str(manifest["patterns"][1 if rounds == 10 else 2]["task_id"])
        protocol = build_c2_selection_protocol(
            locus=locus,
            candidate_roster=[
                {"task_id": task_id, "frozen_rank": 1},
                {"task_id": f"future-{locus.lower()}-second", "frozen_rank": 2},
            ],
        )
        protocol_path = tmp_path / f"{locus.lower()}-selection.json"
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
        protocol_paths[locus] = protocol_path
        q2: dict[str, object] = {
            "schema_version": (
                "chemworld-work-ii-matched-prior-five-world-summary-0.3"
                if locus == "A_P"
                else "future-locus-specific-a-s-summary"
            ),
            "formal_result": False,
            "provider_call_count": 0,
            "participant_session_count": 0,
            "task_id": task_id,
            "qualification_passed": True,
            "provider_execution_authorized": False,
            "generated_d1_config": {
                "path": config_paths[rounds].relative_to(ROOT).as_posix(),
                "sha256": file_sha256(config_paths[rounds]),
            },
        }
        if locus == "A_P":
            q2.update(
                {
                    "qualification_schema_version": (
                        "chemworld-work-ii-matched-prior-qualification-0.3"
                    ),
                    "coverage": {
                        "world_count": 5,
                        "surface_queries_per_world": 121,
                        "planned_surface_query_count": 605,
                        "held_out_queries_per_world": 16,
                    },
                    "denominators": {
                        "world_count": 5,
                        "passed_world_count": 5,
                        "classified_surface_query_count": 605,
                        "physical_failure_count": 64,
                        "platform_failure_count": 0,
                        "safe_fit_count": 150,
                        "safe_held_out_count": 391,
                    },
                    "failure_count": 0,
                    "failures": [],
                    "d1_authorized": True,
                    "decision": "proceed_to_reaction_safety_d1",
                    "world_seeds": [0, 1, 2, 3, 4],
                    "worlds": [
                        {
                            "world_seed": seed,
                            "passed": True,
                            "physical_failure_count": 13 if seed < 3 else 14 if seed == 3 else 11,
                            "safe_fit_count": 30,
                            "safe_held_out_count": 78 if seed < 3 else 77 if seed == 3 else 80,
                            "leakage_audit": {
                                "passed": True,
                                "failures": [],
                                "forbidden_pattern_hits": [],
                            },
                            "prior_matching": {"passed": True, "failures": []},
                            "selected_reflection": {"passed": True},
                        }
                        for seed in range(5)
                    ],
                    "raw_bindings": [
                        {
                            "world_seed": seed,
                            "passed": True,
                            "path": f"runs/development/future-world-{seed}.json",
                            "sha256": f"{seed + 1:064x}",
                        }
                        for seed in range(5)
                    ],
                    "generated_package": {
                        "path": config_paths[rounds].relative_to(ROOT).as_posix(),
                        "sha256": file_sha256(config_paths[rounds]),
                    },
                }
            )
            q2["summary_sha256"] = canonical_json_sha256(q2)
        q2_path = tmp_path / f"{locus.lower()}-q2-generation.json"
        q2_path.write_text(json.dumps(q2), encoding="utf-8")
        q2_paths[locus] = q2_path
    design_binding = {
        "path": design_path.relative_to(ROOT).as_posix(),
        "sha256": file_sha256(design_path),
        "hash_kind": "file_sha256",
    }
    protocol_bindings = {
        locus: {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
            "hash_kind": "file_sha256",
        }
        for locus, path in protocol_paths.items()
    }
    q2_bindings = {
        locus: {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(path),
            "hash_kind": "file_sha256",
        }
        for locus, path in q2_paths.items()
    }
    selected: dict[str, object] = {}
    for pattern in manifest["patterns"]:
        rounds = int(pattern["rounds"])
        locus = str(pattern["locus"])
        if rounds == 8:
            source = "formal_design_v0.2_task"
            selection_binding = design_binding
            rule = "protocol_frozen_task_id_in_formal_design_v0.2"
        else:
            source = "protected_selection_protocol_rank_1"
            selection_binding = protocol_bindings[locus]
            pattern["q2_generation_record_binding"] = q2_bindings[locus]
            rule = "rank_1_in_protected_pre_evidence_selection_protocol"
        pattern["representative_selection_source"] = source
        pattern["representative_selection_binding"] = selection_binding
        selected[str(rounds)] = {
            "locus": locus,
            "task_id": pattern["task_id"],
            "selection_rule": rule,
        }
    manifest["representative_resolution"] = {
        "status": "resolved",
        "formal_design_binding": design_binding,
        "selection_protocol_bindings": protocol_bindings,
        "q2_generation_record_bindings": q2_bindings,
        "arbitrary_config_override_allowed": False,
        "proxy_substitution_allowed": False,
        "selected_representatives": selected,
        "blocking_requirements": [],
    }
    manifest["status"] = "ready_authorization_blocked"
    manifest["protocol_manifest_binding"] = {
        "path": MANIFEST.relative_to(ROOT).as_posix(),
        "sha256": file_sha256(MANIFEST),
        "hash_kind": "file_sha256",
    }
    manifest["development_binding_policy"] = {
        "exact_selected_campaign_configs_bound": True,
        "selection_and_q2_inputs_bound": True,
        "whole_tree_hash_required": False,
        "clean_worktree_required": False,
        "release_freeze_deferred": True,
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, manifest


def _passed_cell(pattern: dict[str, object], arm: str) -> dict[str, object]:
    rounds = int(pattern["rounds"])
    return {
        "rounds": rounds,
        "locus": pattern["locus"],
        "task_id": pattern["task_id"],
        "world_seed": pattern["world_seed"],
        "arm": arm,
        "status": "passed",
        "terminal": True,
        "calibration_passed": True,
        "complete_experiments": rounds,
        "unique_recipe_count": rounds - 2,
        "exact_repeat_count": 2,
        "operation_attempts": rounds * 7,
        "committed_operations": rounds * 6,
        "checkpoint_complete_experiments": pattern[
            "checkpoint_complete_experiments"
        ],
        "checkpoint_stages": [f"checkpoint-{index}" for index in range(5)],
        "typed_checkpoints_valid": True,
        "final_recommendation_committed": True,
        "lifecycle_closed": True,
        "exact_replay_verified": True,
        "resource_ledgers_reconciled": True,
        "process_resources": {
            "process_time_used_s": rounds * 100.0,
            "required_stage_max_s": rounds * 80.0,
            "repeat_allowance_s": rounds * 20.0,
            "protected_closeout_reserve_s": rounds * 10.0,
            "protected_closeout_reserve_consumed_s": 0.0,
            "reserve_consumption_by_operation_class": {},
        },
        "provider_resources": {
            "input_tokens": rounds * 100,
            "cache_hit_input_tokens": rounds * 50,
            "uncached_input_tokens": rounds * 50,
            "output_tokens": rounds * 10,
            "provider_elapsed_s": rounds * 2.0,
            "provider_attempts": 1,
            "mcp_recovery_count": 0,
            "mcp_error_count": 0,
            "observed_currency_usd": rounds / 1000,
        },
        "failure_counts": {
            "resource_rejection": 0,
            "unsafe_outcome": 0,
            "dynamic_physical_failure": 0,
            "provider_error": 0,
            "platform_execution_failure": 0,
        },
    }


def _passed_summary(manifest: dict[str, object], source_commit: str) -> dict[str, object]:
    cells = [
        _passed_cell(pattern, arm)
        for pattern in manifest["patterns"]
        for arm in RESOURCE_CALIBRATION_ARMS
    ]
    patterns = [
        {
            "rounds": pattern["rounds"],
            "locus": pattern["locus"],
            "task_id": pattern["task_id"],
            "world_seed": pattern["world_seed"],
            "cell_count": 3,
            "cells_terminal": 3,
            "complete_experiments": int(pattern["rounds"]) * 3,
            "belief_checkpoints": 15,
            "triplet_passed": True,
            "platform_defect_detected": False,
        }
        for pattern in manifest["patterns"]
    ]
    proposals = []
    for pattern in manifest["patterns"]:
        rounds = int(pattern["rounds"])
        proposals.append(
            {
                "rounds": rounds,
                "locus": pattern["locus"],
                "observed_maxima": {
                    "operation_attempts": rounds * 7,
                    "exact_repeat_count": 2,
                    "process_time_used_s": rounds * 100.0,
                    "input_tokens": rounds * 100,
                    "uncached_input_tokens": rounds * 50,
                    "output_tokens": rounds * 10,
                    "provider_elapsed_s": rounds * 2.0,
                    "observed_currency_usd": rounds / 1000,
                },
                "protected_closeout_reserve_enforced": True,
                "proposed_hard_caps": {
                    "operation_attempt_limit": rounds * 7,
                    "protected_closeout_operation_reserve": rounds * 2,
                    "maximum_exact_repeats": 2,
                    "process_time_limit_s": rounds * 110.0,
                    "protected_closeout_reserve_s": rounds * 10.0,
                    "input_token_limit": rounds * 100,
                    "uncached_input_token_limit": rounds * 50,
                    "output_token_limit": rounds * 10,
                    "provider_wall_time_limit_s": rounds * 2.0,
                    "currency_ceiling_usd": rounds / 1000,
                },
            }
        )
    summary = {
        "schema_version": "chemworld-work-ii-resource-calibration-summary-0.1",
        "status": "passed",
        "formal_result": False,
        "provider_calls_executed": 9,
        "manifest_sha256": canonical_json_sha256(manifest),
        "source_commit": source_commit,
        "c2_source_binding": None,
        "development_binding_policy": manifest.get("development_binding_policy"),
        "expected_denominators": manifest["expected_denominators"],
        "observed_denominators": {
            "pattern_triplets_started": 3,
            "pattern_triplets_terminal": 3,
            "cells_started": 9,
            "cells_terminal": 9,
            "complete_experiments": 90,
            "belief_checkpoints": 45,
            "provider_sessions": 9,
            "participant_model_calls": 9,
        },
        "pattern_summaries": patterns,
        "cell_summaries": cells,
        "all_failures": [],
        "resource_card_proposals": proposals,
        "calibration_passed": True,
        "method_qualification_may_be_authorized": True,
    }
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    return summary


def test_calibration_manifest_freezes_denominators_and_retains_as_gate() -> None:
    manifest = _manifest()
    assert validate_resource_calibration_manifest(ROOT, manifest) == []
    assert manifest["status"] == "not_ready_fail_closed"
    assert [row["rounds"] for row in manifest["patterns"]] == [8, 10, 12]
    assert manifest["expected_denominators"] == {
        "pattern_triplets": 3,
        "cells": 9,
        "complete_experiments": 90,
        "belief_checkpoints": 45,
        "accepted_provider_sessions": 9,
        "accepted_participant_model_calls": 9,
    }
    twelve = manifest["patterns"][2]
    assert twelve["locus"] == "A_S"
    assert twelve["task_id"] is None
    assert twelve["campaign_config_binding"] is None
    assert twelve["representative_task_status"] == "pending_two_terminal_AS_admissions"
    assert manifest["authorization_gate"]["twelve_round_proxy_substitution_forbidden"] is True


def test_calibration_readiness_is_deterministic_zero_call_and_not_ready() -> None:
    first = build_resource_calibration_readiness(ROOT, MANIFEST)
    second = build_resource_calibration_readiness(ROOT, MANIFEST)
    assert first == second
    assert validate_resource_calibration_readiness(first) == []
    assert first["status"] == "not_ready_fail_closed"
    assert first["provider_execution_allowed"] is False
    assert first["provider_calls_executed"] == 0
    assert first["method_qualification_may_be_authorized"] is False
    assert first["missing_pattern_rounds"] == [10, 12]
    assert first["representative_resolution"]["selected_representatives"]["10"] == {
        "locus": "A_P",
        "task_id": "reaction-safety-constrained",
        "selection_rule": "rank_1_in_protected_pre_evidence_selection_protocol",
    }
    assert any(
        "12-round A_S Q2 generation record is unavailable"
        in blocker
        for blocker in first["blocking_requirements"]
    )


def test_representative_resolution_fails_closed_on_missing_as_q2_generation() -> None:
    patterns, resolution = resolve_resource_calibration_representatives(
        ROOT,
        _manifest(),
        formal_design_path=ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json",
        selection_protocol_paths={
            "A_P": ROOT / "configs/benchmark/work_ii_c2_ap_selection_protocol_v0.1.json",
            "A_S": ROOT / "configs/benchmark/work_ii_c2_as_selection_protocol_v0.1.json",
        },
        q2_generation_record_paths={
            "A_P": ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-reaction-safety-matched-prior-qualification-20260811.json",
            "A_S": ROOT
            / "workstreams/flagship_tasks/reports/"
            "work-ii-as-paired-law-q1-q2-five-world-20260812.json",
        },
    )

    assert resolution["status"] == "not_ready_fail_closed"
    assert resolution["arbitrary_config_override_allowed"] is False
    assert resolution["proxy_substitution_allowed"] is False
    assert resolution["selected_representatives"]["8"]["task_id"] == "electrochemical-conversion"
    assert resolution["selected_representatives"]["10"]["task_id"] == "reaction-safety-constrained"
    assert any(
        "12-round A_S Q2 generation record is unavailable"
        in blocker
        for blocker in resolution["blocking_requirements"]
    )
    assert [row["task_id"] for row in patterns] == [
        "electrochemical-conversion",
        "reaction-safety-constrained",
        None,
    ]


def test_execution_manifest_cannot_run_before_rank_one_as_q2_generation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "chemworld.eval.work_ii_c2_admission.c2_material_dirty_paths",
        lambda _root: [],
    )
    with pytest.raises(ValueError, match="A_S Q2 generation record"):
        build_resource_calibration_execution_manifest(
            ROOT,
            MANIFEST,
            formal_design_path=ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json",
        )


def test_q2_generation_resolution_reads_the_selected_configs_exactly(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _manifest_path, frozen = _future_manifest(repo_tmp_path)
    resolution = frozen["representative_resolution"]
    design_path = ROOT / resolution["formal_design_binding"]["path"]
    protocol_paths = {
        locus: ROOT / row["path"]
        for locus, row in resolution["selection_protocol_bindings"].items()
    }
    q2_paths = {
        locus: ROOT / row["path"]
        for locus, row in resolution["q2_generation_record_bindings"].items()
    }

    patterns, rebuilt = resolve_resource_calibration_representatives(
        ROOT,
        frozen,
        formal_design_path=design_path,
        selection_protocol_paths=protocol_paths,
        q2_generation_record_paths=q2_paths,
    )

    assert rebuilt["status"] == "resolved"
    assert rebuilt["blocking_requirements"] == []
    assert rebuilt["proxy_substitution_allowed"] is False
    for pattern, expected in zip(patterns, frozen["patterns"], strict=True):
        assert pattern["task_id"] == expected["task_id"]
        assert pattern["campaign_config_binding"] == expected["campaign_config_binding"]
    assert patterns[1]["representative_selection_source"] == (
        "protected_selection_protocol_rank_1"
    )
    assert patterns[2]["representative_selection_source"] == (
        "protected_selection_protocol_rank_1"
    )


def test_q2_generation_rejects_provider_use_and_config_escape(
    repo_tmp_path: Path,
) -> None:
    _manifest_path, frozen = _future_manifest(repo_tmp_path)
    resolution = frozen["representative_resolution"]
    protocols = {
        locus: ROOT / row["path"]
        for locus, row in resolution["selection_protocol_bindings"].items()
    }
    q2_paths = {
        locus: ROOT / row["path"]
        for locus, row in resolution["q2_generation_record_bindings"].items()
    }
    ap = json.loads(q2_paths["A_P"].read_text(encoding="utf-8"))
    ap["provider_call_count"] = 1
    ap["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in ap.items() if key != "summary_sha256"}
    )
    q2_paths["A_P"].write_text(json.dumps(ap), encoding="utf-8")
    _, provider_used = resolve_resource_calibration_representatives(
        ROOT,
        frozen,
        formal_design_path=ROOT / resolution["formal_design_binding"]["path"],
        selection_protocol_paths=protocols,
        q2_generation_record_paths=q2_paths,
    )
    assert any(
        "not provider/participant-free" in item
        for item in provider_used["blocking_requirements"]
    )

    ap["provider_call_count"] = 0
    ap["generated_d1_config"]["path"] = "../../../../outside.json"
    ap["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in ap.items() if key != "summary_sha256"}
    )
    q2_paths["A_P"].write_text(json.dumps(ap), encoding="utf-8")
    _, escaped = resolve_resource_calibration_representatives(
        ROOT,
        frozen,
        formal_design_path=ROOT / resolution["formal_design_binding"]["path"],
        selection_protocol_paths=protocols,
        q2_generation_record_paths=q2_paths,
    )
    assert any("escapes repository" in item for item in escaped["blocking_requirements"])


def test_self_declared_q2_generation_record_cannot_unlock_execution(
    repo_tmp_path: Path,
) -> None:
    _manifest_path, frozen = _future_manifest(repo_tmp_path)
    resolution = frozen["representative_resolution"]
    q2_paths = {
        locus: ROOT / row["path"]
        for locus, row in resolution["q2_generation_record_bindings"].items()
    }
    ap = json.loads(q2_paths["A_P"].read_text(encoding="utf-8"))
    ap.pop("summary_sha256")
    ap["schema_version"] = RESOURCE_CALIBRATION_Q2_GENERATION_VERSION
    ap["generation_sha256"] = canonical_json_sha256(ap)
    q2_paths["A_P"].write_text(json.dumps(ap), encoding="utf-8")

    _, rebuilt = resolve_resource_calibration_representatives(
        ROOT,
        frozen,
        formal_design_path=ROOT / resolution["formal_design_binding"]["path"],
        selection_protocol_paths={
            locus: ROOT / row["path"]
            for locus, row in resolution["selection_protocol_bindings"].items()
        },
        q2_generation_record_paths=q2_paths,
    )

    assert any(
        "self-declared Q2 generation records cannot unlock execution" in error
        for error in rebuilt["blocking_requirements"]
    )


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda row: row.update({"qualification_schema_version": "stale"}), "valid frozen"),
        (lambda row: row["coverage"].update({"world_count": 4}), "valid frozen"),
        (
            lambda row: row["denominators"].update({"platform_failure_count": 1}),
            "valid frozen",
        ),
        (lambda row: row.update({"failure_count": 1}), "valid frozen"),
        (lambda row: row.update({"failures": [{"class": "platform"}]}), "valid frozen"),
        (lambda row: row.update({"d1_authorized": False}), "valid frozen"),
        (lambda row: row.update({"decision": "stop"}), "valid frozen"),
        (
            lambda row: row["worlds"][0]["leakage_audit"].update({"passed": False}),
            "world 0",
        ),
    ],
)
def test_real_ap_q2_summary_strict_contract_rejects_tampering(
    mutation,
    expected: str,
) -> None:
    path = (
        ROOT
        / "workstreams/flagship_tasks/reports/"
        "work-ii-reaction-safety-matched-prior-qualification-20260811.json"
    )
    summary = json.loads(path.read_text(encoding="utf-8"))
    assert calibration_module._validate_ap_q2_record(
        ROOT, summary, task_id="reaction-safety-constrained"
    )[0] == []
    mutation(summary)
    summary["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in summary.items() if key != "summary_sha256"}
    )
    errors, _ = calibration_module._validate_ap_q2_record(
        ROOT, summary, task_id="reaction-safety-constrained"
    )
    assert any(expected in error for error in errors)


def test_q2_config_requires_exact_integer_world_seed(repo_tmp_path: Path) -> None:
    _manifest_path, frozen = _future_manifest(repo_tmp_path)
    resolution = frozen["representative_resolution"]
    pattern = frozen["patterns"][1]
    config_path = ROOT / pattern["campaign_config_binding"]["path"]
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["world_seed"] = "10"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    ap_path = ROOT / resolution["q2_generation_record_bindings"]["A_P"]["path"]
    ap = json.loads(ap_path.read_text(encoding="utf-8"))
    ap["generated_d1_config"]["sha256"] = file_sha256(config_path)
    ap["summary_sha256"] = canonical_json_sha256(
        {key: value for key, value in ap.items() if key != "summary_sha256"}
    )
    ap_path.write_text(json.dumps(ap), encoding="utf-8")

    _, rebuilt = resolve_resource_calibration_representatives(
        ROOT,
        frozen,
        formal_design_path=ROOT / resolution["formal_design_binding"]["path"],
        selection_protocol_paths={
            locus: ROOT / row["path"]
            for locus, row in resolution["selection_protocol_bindings"].items()
        },
        q2_generation_record_paths={
            locus: ROOT / row["path"]
            for locus, row in resolution["q2_generation_record_bindings"].items()
        },
    )
    assert any(
        "lacks an exact integer world_seed" in error
        for error in rebuilt["blocking_requirements"]
    )


def test_real_child_gate_honors_file_hash_kind(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    pattern = manifest["patterns"][0]
    config_path = ROOT / pattern["campaign_config_binding"]["path"]
    authorization_path = repo_tmp_path / "authorization.json"
    reservation_path = repo_tmp_path / "reservation.json"
    authorization_path.write_text(
        json.dumps({"currency_ceiling_usd": 1.0, "authorization_sha256": "auth"}),
        encoding="utf-8",
    )
    reservation_path.write_text(
        json.dumps(
            {
                "rounds": pattern["rounds"],
                "attempt_number": 1,
                "authorization_sha256": "auth",
                "currency_ceiling_usd": 1.0,
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        campaign_runner,
        "validate_resource_calibration_authorization",
        lambda *_: [],
    )
    args = SimpleNamespace(
        resource_calibration_execution=True,
        resource_calibration_manifest=manifest_path,
        resource_calibration_authorization=authorization_path,
        resource_calibration_cost_reservation=reservation_path,
        prior_arm="opaque",
    )
    context = campaign_runner._resource_calibration_execution_context(
        args,
        config_path=config_path,
        world_seed=int(pattern["world_seed"]),
        arms=["opaque"],
    )
    assert context is not None
    assert context[2]["pattern"]["campaign_config_hash_kind"] == "file_sha256"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("campaign_config_sha256", "0" * 64),
        ("campaign_config_hash_kind", "canonical_json_sha256"),
    ],
)
def test_parent_rejects_tampered_child_config_binding(
    repo_tmp_path: Path,
    field: str,
    value: str,
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    pattern = manifest["patterns"][0]
    authorization_path = repo_tmp_path / "authorization.json"
    reservation_path = repo_tmp_path / "reservation.json"
    authorization = {"authorization_sha256": "auth"}
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    reservation_path.write_text(json.dumps({"attempt_number": 1}), encoding="utf-8")
    row = {
        "resource_calibration_execution_binding": {
            "manifest": {
                "path": manifest_path.relative_to(ROOT).as_posix(),
                "file_sha256": file_sha256(manifest_path),
            },
            "authorization": {
                "path": authorization_path.relative_to(ROOT).as_posix(),
                "file_sha256": file_sha256(authorization_path),
                "authorization_sha256": "auth",
            },
            "cost_reservation": {
                "path": reservation_path.relative_to(ROOT).as_posix(),
                "file_sha256": file_sha256(reservation_path),
            },
            "pattern": {
                "rounds": pattern["rounds"],
                "locus": pattern["locus"],
                "task_id": pattern["task_id"],
                "world_seed": pattern["world_seed"],
                "prior_arm": "opaque",
                "campaign_config_sha256": pattern["campaign_config_binding"]["sha256"],
                "campaign_config_hash_kind": pattern["campaign_config_binding"][
                    "hash_kind"
                ],
            },
        }
    }
    row["resource_calibration_execution_binding"]["pattern"][field] = value

    with pytest.raises(RuntimeError, match="detached from its execution authorization"):
        calibration_runner._validate_cell_execution_binding(
            row,
            arm="opaque",
            pattern=pattern,
            manifest_path=manifest_path,
            authorization_path=authorization_path,
            authorization=authorization,
            reservation_path=reservation_path,
        )


def test_readiness_surfaces_internal_errors_as_blockers(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    manifest["patterns"][0]["locus"] = "A_S"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    readiness = build_resource_calibration_readiness(ROOT, manifest_path)

    assert readiness["status"] == "not_ready_fail_closed"
    assert any(
        error in readiness["blocking_requirements"]
        for error in readiness["internal_errors"]
    )


def test_future_passed_summary_is_the_only_unlock_path(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    assert validate_resource_calibration_manifest(ROOT, manifest) == []
    before = build_resource_calibration_readiness(ROOT, manifest_path)
    assert before["status"] == "ready_authorization_blocked"
    assert before["method_qualification_may_be_authorized"] is False
    summary = _passed_summary(
        manifest, before["development_runtime_commit_observed"]
    )
    summary_path = manifest_path.parent / "summary.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    after = build_resource_calibration_readiness(
        ROOT, manifest_path, summary_path=summary_path
    )
    assert validate_resource_calibration_readiness(after) == []
    assert after["status"] == "calibration_passed_method_qualification_eligible"
    assert after["method_qualification_may_be_authorized"] is True


def test_readiness_accepts_unrelated_worktree_changes_but_rejects_bound_config_drift(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, manifest = _future_manifest(repo_tmp_path)
    tested_commit = "a" * 40
    current_commit = "b" * 40
    summary = _passed_summary(manifest, tested_commit)
    summary["summary_sha256"] = resource_calibration_summary_sha256(summary)
    summary_path = repo_tmp_path / "summary.json"
    summary_path.write_text(json.dumps(summary), encoding="utf-8")
    monkeypatch.setattr(calibration_module, "git_source_commit", lambda _root: current_commit)

    unrelated_changes = build_resource_calibration_readiness(
        ROOT, manifest_path, summary_path=summary_path
    )
    assert unrelated_changes["calibration_summary_errors"] == []
    assert unrelated_changes["method_qualification_may_be_authorized"] is True
    assert unrelated_changes["clean_worktree_required"] is False
    assert unrelated_changes["whole_tree_hash_required"] is False

    config_path = ROOT / manifest["patterns"][0]["campaign_config_binding"]["path"]
    original = config_path.read_text(encoding="utf-8")
    try:
        config_path.write_text(original + "\n", encoding="utf-8")
        drifted = build_resource_calibration_readiness(
            ROOT, manifest_path, summary_path=summary_path
        )
        assert any("binding is stale" in error for error in drifted["internal_errors"])
        assert drifted["method_qualification_may_be_authorized"] is False
    finally:
        config_path.write_text(original, encoding="utf-8")


def test_passed_summary_rejects_failure_and_resource_card_tampering(
    repo_tmp_path: Path,
) -> None:
    _manifest_path, manifest = _future_manifest(repo_tmp_path)
    summary = _passed_summary(manifest, "future-clean-source")
    assert validate_resource_calibration_summary(summary, manifest=manifest) == []
    tampered = deepcopy(summary)
    tampered["cell_summaries"][0]["failure_counts"]["provider_error"] = 1
    tampered["all_failures"] = [{"class": "provider_error"}]
    tampered["summary_sha256"] = resource_calibration_summary_sha256(tampered)
    errors = validate_resource_calibration_summary(tampered, manifest=manifest)
    assert any("platform failures" in error for error in errors)
    assert "passed resource calibration summary contains failures" in errors


def test_authorization_and_executor_are_usable_after_real_gate_inputs(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest_path, _manifest = _future_manifest(repo_tmp_path)
    authorization = build_resource_calibration_authorization(
        ROOT,
        manifest_path,
        currency_ceiling_usd=100.0,
        approved_at="2026-08-12T00:00:00+08:00",
        pricing_source="https://provider.example/pricing",
        pricing_observed_at="2026-08-12T00:00:00+08:00",
        cache_hit_input_usd_per_million=0.01,
        cache_miss_input_usd_per_million=0.1,
        output_usd_per_million=0.2,
    )
    assert validate_resource_calibration_authorization(
        ROOT, authorization, manifest_path
    ) == []
    assert authorization["all_infrastructure_resumes"]["provider_process_attempts"] == 18
    assert authorization["runtime_enforcement"][
        "affected_triplet_restarts_from_first_cell"
    ] is True
    source = RUNNER.read_text(encoding="utf-8")
    assert "provider executor is not implemented" not in source
    assert calibration_runner.execute_calibration is not None


def test_summary_aggregator_invalidates_platform_defect(
    repo_tmp_path: Path,
) -> None:
    _manifest_path, manifest = _future_manifest(repo_tmp_path)
    summary = build_resource_calibration_summary(
        manifest, [], source_commit="future-clean-source"
    )
    assert summary["status"] == "invalidated_platform_defect"
    assert summary["calibration_passed"] is False
    assert summary["method_qualification_may_be_authorized"] is False


def test_unexecuted_summary_template_cannot_claim_results() -> None:
    summary = empty_resource_calibration_summary(_manifest())
    assert validate_resource_calibration_summary(summary) == []
    assert summary["status"] == "not_executed"
    assert summary["observed_denominators"]["cells_started"] == 0
    tampered = deepcopy(summary)
    tampered["calibration_passed"] = True
    tampered["summary_sha256"] = resource_calibration_summary_sha256(tampered)
    assert "unexecuted resource calibration summary claims results" in (
        validate_resource_calibration_summary(tampered)
    )


def test_runner_rejects_provider_execution_before_creating_output(tmp_path: Path) -> None:
    output = tmp_path / "calibration"
    result = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--execute",
            "--manifest",
            str(MANIFEST),
            "--output",
            str(output),
            "--allow-provider-execution",
            "--authorization",
            str(tmp_path / "authorization.json"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "unresolved pattern rounds: 10,12" in result.stderr
    assert not output.exists()


def test_launch_decision_brief_is_explicitly_stale() -> None:
    brief = (
        ROOT
        / "workstreams/flagship_tasks/reports/work-ii-formal-launch-decision-brief.md"
    ).read_text(encoding="utf-8")
    assert "STALE — NOT AUTHORIZATION-ELIGIBLE" in brief
    assert "No calibration or method-qualification provider call is currently authorized" in brief
    assert "12 / 12" not in brief
    assert "Operation-attempt hard cap | 84" not in brief
