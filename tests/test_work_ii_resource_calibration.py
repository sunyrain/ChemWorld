from __future__ import annotations

import json
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest
import scripts.run_work_ii_resource_calibration as calibration_runner

import chemworld.eval.work_ii_resource_calibration_v02 as calibration
from chemworld.eval.provenance import canonical_json_sha256, file_sha256
from chemworld.eval.resource_accounting import MethodResourceLimits

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "configs/benchmark/work_ii_resource_calibration_manifest_v0.2.json"


@pytest.fixture
def repo_tmp_path():
    path = Path(tempfile.mkdtemp(prefix=".pytest-resource-calibration-", dir=ROOT))
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _resolved_manifest(repo_tmp_path: Path) -> tuple[Path, dict[str, object]]:
    manifest = _manifest()
    source_configs = dict(calibration.AE_CONFIGS)
    for world_seed, pattern in enumerate(manifest["patterns"]):
        rounds = int(pattern["rounds"])
        task_id = str(pattern["task_id"])
        source = json.loads(
            (ROOT / source_configs[task_id]).read_text(encoding="utf-8")
        )
        source["task_id"] = task_id
        source["world_seed"] = world_seed
        source["campaign"]["complete_experiments"] = rounds
        source["campaign"]["checkpoint_complete_experiments"] = pattern[
            "checkpoint_complete_experiments"
        ]
        source["method_resources"]["complete_experiment_limit"] = rounds
        source["method_resources"]["checkpoint_complete_experiments"] = pattern[
            "checkpoint_complete_experiments"
        ][1:]
        config = calibration._materialize_runtime_config(
            source,
            locus=str(pattern["locus"]),
            task_id=task_id,
            rounds=rounds,
        )
        config_path = repo_tmp_path / f"{calibration.pattern_slug(pattern)}.json"
        config_path.write_text(json.dumps(config), encoding="utf-8")
        pattern.update(
            {
                "status": "resolved_authorization_blocked",
                "campaign_config_binding": {
                    "path": config_path.relative_to(ROOT).as_posix(),
                    "sha256": file_sha256(config_path),
                    "hash_kind": "file_sha256",
                },
                "world_seed": world_seed,
                "resource_formula_binding": (
                    calibration.build_task_resource_formula_binding(config)
                ),
                "evidence": {"source": "contract_test_fixture"},
            }
        )
    manifest.update({"status": "ready_authorization_blocked", "blocking_requirements": []})
    manifest_path = repo_tmp_path / "manifest-v0.2-contract-test.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assert calibration.validate_manifest(ROOT, manifest) == []
    return manifest_path, manifest


def test_summary_template_cli_uses_manifest_and_summary_contracts_directly(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = repo_tmp_path / "summary-template.json"
    monkeypatch.setattr(
        calibration_runner.sys,
        "argv",
        [
            "run_work_ii_resource_calibration.py",
            "--manifest",
            str(MANIFEST),
            "--summary-template",
            "--output",
            str(output),
        ],
    )

    assert calibration_runner.main() == 0
    summary = json.loads(output.read_text(encoding="utf-8"))
    assert calibration.validate_summary(summary, manifest=_manifest()) == []
    assert summary["status"] == "not_executed"
    assert summary["provider_calls_executed"] == 0
    assert summary["expected_denominators"] == calibration.EXPECTED_DENOMINATORS


def test_authorize_cli_rejects_incomplete_manifest_without_readiness_projection(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = repo_tmp_path / "authorization.json"
    monkeypatch.setattr(
        calibration_runner.sys,
        "argv",
        [
            "run_work_ii_resource_calibration.py",
            "--manifest",
            str(MANIFEST),
            "--authorize",
            "--output",
            str(output),
            "--approved-at",
            "2026-08-14T00:00:00+08:00",
            "--unlimited-spend-authorized",
            "--provider-contract-confirmed-by-user",
            "--credential-rotation-confirmed-by-user",
        ],
    )

    with pytest.raises(ValueError, match="full task matrix is incomplete"):
        calibration_runner.main()
    assert not output.exists()


def test_manifest_freezes_exact_nine_task_contracts() -> None:
    manifest = _manifest()

    assert tuple(calibration.pattern_key(row) for row in manifest["patterns"]) == (
        ("A_E", "electrochemical-conversion", 8),
        ("A_E", "reaction-to-crystallization", 8),
        ("A_E", "reaction-to-distillation", 8),
        ("A_E", "partition-discovery", 8),
        ("A_E", "reaction-safety-constrained", 8),
        ("A_P", "reaction-safety-constrained", 10),
        ("A_P", "electrochemical-conversion", 10),
        ("A_S", "partition-discovery", 12),
        ("A_S", "reaction-to-crystallization", 12),
    )
    assert manifest["expected_denominators"] == {
        "task_triplets": 9,
        "cells": 27,
        "complete_experiments": 252,
        "belief_checkpoints": 135,
        "accepted_provider_sessions": 27,
        "accepted_participant_model_calls_minimum": 27,
        "accepted_participant_model_calls_maximum": 54,
    }


def test_runtime_config_requires_current_execution_semantics() -> None:
    source = json.loads(
        (ROOT / "configs/benchmark/work_ii_campaign_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    source["campaign"]["complete_experiments"] = 8
    source["campaign"]["checkpoint_complete_experiments"] = [0, 2, 4, 6, 8]
    source["method_resources"]["complete_experiment_limit"] = 8
    source["method_resources"]["checkpoint_complete_experiments"] = [2, 4, 6, 8]
    config = calibration._materialize_runtime_config(
        source,
        locus="A_E",
        task_id="electrochemical-conversion",
        rounds=8,
    )

    assert config["w2_26_runtime_identity"]["agent_invalid_enforcement"] == "measure_only"
    assert config["w2_26_runtime_identity"]["provider_error_enforcement"] == "measure_only"
    assert config["provider"]["accepted_turn_continuation_limit"] == 1
    assert config["provider"]["provider_process_attempt_limit"] == 3
    assert config["qualification"]["required_operation_counts"] == {}
    assert calibration._config_errors(
        config,
        locus="A_E",
        task_id="electrochemical-conversion",
        rounds=8,
    ) == []

    for field_path in (
        ("w2_26_runtime_identity", "provider_error_enforcement"),
        ("qualification", "required_operation_counts"),
    ):
        incomplete = deepcopy(config)
        del incomplete[field_path[0]][field_path[1]]
        assert calibration._config_errors(
            incomplete,
            locus="A_E",
            task_id="electrochemical-conversion",
            rounds=8,
        )


@pytest.mark.parametrize(
    ("locus", "task_id", "rounds", "source_path"),
    [
        (
            "A_P",
            "reaction-safety-constrained",
            10,
            "configs/benchmark/work_ii_reaction_safety_matched_prior_d1.json",
        ),
        (
            "A_P",
            "electrochemical-conversion",
            10,
            "configs/benchmark/work_ii_electrochemical_matched_prior_d1.json",
        ),
        (
            "A_S",
            "partition-discovery",
            12,
            "configs/benchmark/work_ii_as_partition_d1_v0.1.json",
        ),
        (
            "A_S",
            "reaction-to-crystallization",
            12,
            "configs/benchmark/work_ii_as_crystallization_d1_v0.1.json",
        ),
    ],
)
def test_task_materialization_reaches_typed_resource_constructor(
    locus: str,
    task_id: str,
    rounds: int,
    source_path: str,
) -> None:
    source = json.loads((ROOT / source_path).read_text(encoding="utf-8"))
    config = calibration._materialize_runtime_config(
        source, locus=locus, task_id=task_id, rounds=rounds
    )

    assert "resource_status" not in config["method_resources"]
    assert calibration._config_errors(
        config, locus=locus, task_id=task_id, rounds=rounds
    ) == []
    limits = MethodResourceLimits.from_payload(
        config["method_resources"],
        operation_limit=int(config["method_resources"]["operation_limit"]),
    )
    assert limits.complete_experiment_limit == rounds

    stale = deepcopy(config)
    stale["method_resources"]["resource_status"] = "legacy_metadata"
    assert any(
        "unsupported MethodResourceLimits fields: resource_status" in error
        for error in calibration._config_errors(
            stale, locus=locus, task_id=task_id, rounds=rounds
        )
    )


def test_authorization_binds_every_task_and_keeps_unknown_pricing_unknown(
    repo_tmp_path: Path,
) -> None:
    manifest_path, _ = _resolved_manifest(repo_tmp_path)
    authorization = calibration.build_authorization(
        ROOT,
        manifest_path,
        currency_ceiling_usd=None,
        approved_at="2026-08-13T00:00:00Z",
        pricing_source=None,
        pricing_observed_at=None,
        cache_hit_input_usd_per_million=None,
        cache_miss_input_usd_per_million=None,
        output_usd_per_million=None,
        unlimited_spend_authorized=True,
    )

    assert calibration.validate_authorization(ROOT, authorization, manifest_path) == []
    assert len(authorization["pattern_attempt_contracts"]) == 9
    assert authorization["runtime_enforcement"]["provider_error_enforcement"] == (
        "measure_only"
    )
    assert authorization["currency_ceiling_usd"] is None
    assert authorization["pricing"]["pricing_available"] is False
    assert calibration_runner._observed_currency({}, authorization) is None


def test_task9_platform_defect_restarts_whole_triplet_once_then_exhausts_cap() -> None:
    pattern = {
        "locus": "A_S",
        "task_id": "reaction-to-crystallization",
        "rounds": 12,
    }
    authorization = {
        "runtime_enforcement": {"per_triplet_infrastructure_attempt_hard_cap": 2}
    }

    first = calibration_runner._platform_defect_disposition(
        provider_attempt_hard_cap=calibration_runner._triplet_attempt_hard_cap(
            authorization
        ),
        pattern=pattern,
        attempt_number=1,
        reserved_cost_usd=None,
    )
    assert first == {
        "status": "infrastructure_incomplete_full_triplet_restarting",
        "locus": "A_S",
        "task_id": "reaction-to-crystallization",
        "rounds": 12,
        "attempt_number": 1,
        "provider_attempt_hard_cap": 2,
        "automatic_full_triplet_resume": True,
        "next_attempt_number": 2,
        "reserved_cost_usd": None,
    }

    exhausted = calibration_runner._platform_defect_disposition(
        provider_attempt_hard_cap=calibration_runner._triplet_attempt_hard_cap(
            authorization
        ),
        pattern=pattern,
        attempt_number=2,
        reserved_cost_usd=None,
    )
    assert exhausted["status"] == (
        "infrastructure_incomplete_full_triplet_resume_cap_exhausted"
    )
    assert exhausted["automatic_full_triplet_resume"] is False
    assert exhausted["next_attempt_number"] is None


def test_platform_restart_disposition_requires_authorized_hard_cap() -> None:
    with pytest.raises(RuntimeError, match="triplet-attempt hard cap"):
        calibration_runner._triplet_attempt_hard_cap(
            {"runtime_enforcement": {}}
        )


def _one_pattern_execution(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    platform_attempts: set[int],
) -> tuple[dict[str, object], Path, list[tuple[int, str]]]:
    config_path = repo_tmp_path / "task9-config.json"
    config_path.write_text(
        json.dumps(
            {
                "campaign": {
                    "process_time_policy": {},
                    "closeout_policy": {},
                }
            }
        ),
        encoding="utf-8",
    )
    pattern = {
        "locus": "A_S",
        "task_id": "reaction-to-crystallization",
        "rounds": 12,
        "world_seed": 0,
        "campaign_config_binding": {
            "path": config_path.relative_to(ROOT).as_posix(),
            "sha256": file_sha256(config_path),
        },
    }
    manifest = {"patterns": [pattern]}
    manifest_path = repo_tmp_path / "task9-manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    authorization = {
        "authorization_sha256": "a" * 64,
        "development_runtime_commit_observed": "b" * 40,
        "unlimited_spend_authorized": True,
        "currency_ceiling_usd": None,
        "all_infrastructure_resumes": {"cost_cap_usd": None},
        "runtime_enforcement": {"per_triplet_infrastructure_attempt_hard_cap": 2},
        "pattern_attempt_contracts": [
            {
                **pattern,
                "initial_triplet_cost_cap_usd": None,
            }
        ],
    }
    authorization_path = repo_tmp_path / "task9-authorization.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    output_root = repo_tmp_path / "task9-output"
    launches: list[tuple[int, str]] = []

    class Process:
        def __init__(self, command, **_kwargs) -> None:
            cell_root = Path(command[command.index("--output") + 1])
            arm = str(command[command.index("--prior-arm") + 1])
            attempt_number = int(cell_root.parent.name.split("-")[1])
            launches.append((attempt_number, arm))
            cell_root.mkdir(parents=True)
            (cell_root / "summary.json").write_text(
                json.dumps(
                    {
                        "arm": arm,
                        "platform_defect": attempt_number in platform_attempts,
                        "qualification": {"passed": False},
                    }
                ),
                encoding="utf-8",
            )

        def poll(self) -> int:
            return 0

        def wait(self) -> int:
            return 0

    monkeypatch.setattr(
        calibration_runner,
        "validate_resource_calibration_authorization",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        calibration_runner, "_validate_cell_execution_binding", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        calibration_runner,
        "_cell_has_platform_defect",
        lambda row: bool(row["platform_defect"]),
    )
    monkeypatch.setattr(calibration_runner.subprocess, "Popen", Process)
    monkeypatch.setattr(
        calibration_runner,
        "build_resource_calibration_summary",
        lambda *_args, **_kwargs: {"status": "failed", "summary_sha256": "c" * 64},
    )
    monkeypatch.setattr(
        calibration_runner,
        "validate_resource_calibration_summary",
        lambda *_args, **_kwargs: [],
    )
    result = calibration_runner.execute_calibration(
        manifest_path=manifest_path,
        authorization_path=authorization_path,
        output_root=output_root,
        resume=False,
    )
    return result, output_root, launches


def test_task9_platform_defect_restarts_all_three_arms_without_reusing_attempt1(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    result, output_root, launches = _one_pattern_execution(
        repo_tmp_path, monkeypatch, platform_attempts={1}
    )

    assert result["status"] == "failed"
    assert launches == [
        (attempt_number, arm)
        for attempt_number in (1, 2)
        for arm in calibration.RESOURCE_CALIBRATION_ARMS
    ]
    attempts = sorted(
        (output_root / "triplet_attempts" / "a_s--reaction-to-crystallization--r12").glob(
            "attempt-*"
        )
    )
    assert len(attempts) == 2
    assert all((attempt / "triplet_report.json").is_file() for attempt in attempts)
    assert all(
        (attempts[0] / arm / "summary.json").is_file()
        for arm in calibration.RESOURCE_CALIBRATION_ARMS
    )
    progress = [
        json.loads(line)
        for line in (output_root / "progress.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert [row["event"] for row in progress[:2]] == [
        "resource_calibration_triplet_invalidated",
        "resource_calibration_triplet_restarting",
    ]
    assert progress[1]["prior_attempt_results_reused"] is False


def test_task9_platform_restart_cap_exhaustion_never_creates_attempt3(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    result, output_root, launches = _one_pattern_execution(
        repo_tmp_path, monkeypatch, platform_attempts={1, 2}
    )

    assert result["status"] == (
        "infrastructure_incomplete_full_triplet_resume_cap_exhausted"
    )
    assert result["attempt_number"] == 2
    assert len(launches) == 6
    attempts = list(
        (output_root / "triplet_attempts" / "a_s--reaction-to-crystallization--r12").glob(
            "attempt-*"
        )
    )
    assert len(attempts) == 2
    assert not (output_root / "terminal_triplets").exists()


def test_task9_method_failure_is_retained_without_restart(
    repo_tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    result, output_root, launches = _one_pattern_execution(
        repo_tmp_path, monkeypatch, platform_attempts=set()
    )

    assert result["status"] == "failed"
    assert launches == [(1, arm) for arm in calibration.RESOURCE_CALIBRATION_ARMS]
    attempts = list(
        (output_root / "triplet_attempts" / "a_s--reaction-to-crystallization--r12").glob(
            "attempt-*"
        )
    )
    assert len(attempts) == 1
    assert (
        output_root
        / "terminal_triplets"
        / "a_s--reaction-to-crystallization--r12.json"
    ).is_file()


def test_task_slug_and_terminal_report_preserve_task_identity() -> None:
    manifest = _manifest()
    slugs = [calibration.pattern_slug(row) for row in manifest["patterns"]]
    assert len(slugs) == len(set(slugs)) == 9

    pattern = deepcopy(manifest["patterns"][0])
    pattern["world_seed"] = 314
    pattern["campaign_config_binding"] = {
        "path": "configs/benchmark/work_ii_campaign_pilot.json",
        "sha256": "1" * 64,
        "hash_kind": "file_sha256",
    }
    authorization = {
        "development_runtime_commit_observed": "2" * 40,
        "authorization_sha256": "3" * 64,
    }
    report = {
        "schema_version": "chemworld-work-ii-resource-calibration-triplet-0.2",
        "locus": pattern["locus"],
        "task_id": pattern["task_id"],
        "rounds": pattern["rounds"],
        "world_seed": pattern["world_seed"],
        "config_file_sha256": pattern["campaign_config_binding"]["sha256"],
        "manifest_sha256": canonical_json_sha256(manifest),
        "development_runtime_commit_observed": authorization[
            "development_runtime_commit_observed"
        ],
        "authorization_sha256": authorization["authorization_sha256"],
        "results": [{"arm": arm} for arm in calibration.RESOURCE_CALIBRATION_ARMS],
    }
    report["triplet_report_sha256"] = canonical_json_sha256(report)
    calibration_runner._validate_triplet_report(
        report,
        pattern=pattern,
        manifest=manifest,
        authorization=authorization,
    )

    detached = deepcopy(report)
    detached["task_id"] = "reaction-safety-constrained"
    detached["triplet_report_sha256"] = canonical_json_sha256(
        {key: value for key, value in detached.items() if key != "triplet_report_sha256"}
    )
    with pytest.raises(RuntimeError, match="terminal triplet is invalid"):
        calibration_runner._validate_triplet_report(
            detached,
            pattern=pattern,
            manifest=manifest,
            authorization=authorization,
        )


def test_resume_reads_one_terminal_triplet_per_task(
    repo_tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = _manifest()
    manifest_path = repo_tmp_path / "manifest-v0.2.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    authorization = {
        "development_runtime_commit_observed": "4" * 40,
        "authorization_sha256": "5" * 64,
        "currency_ceiling_usd": None,
        "unlimited_spend_authorized": True,
        "all_infrastructure_resumes": {"cost_cap_usd": None},
        "runtime_enforcement": {"per_triplet_infrastructure_attempt_hard_cap": 2},
        "pattern_attempt_contracts": [],
    }
    authorization_path = repo_tmp_path / "authorization-v0.2.json"
    authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
    output_root = repo_tmp_path / "execution"
    terminal_root = output_root / "terminal_triplets"
    terminal_root.mkdir(parents=True)
    expected = []
    for pattern in manifest["patterns"]:
        slug = calibration.pattern_slug(pattern)
        expected.append(slug)
        (terminal_root / f"{slug}.json").write_text(
            json.dumps({"pattern_slug": slug, "results": []}), encoding="utf-8"
        )

    observed: list[tuple[str, str]] = []

    def capture_report(report, *, pattern, **_kwargs) -> None:
        observed.append((str(report["pattern_slug"]), calibration.pattern_slug(pattern)))

    monkeypatch.setattr(
        calibration_runner, "validate_resource_calibration_authorization", lambda *_: []
    )
    monkeypatch.setattr(calibration_runner, "_validate_triplet_report", capture_report)
    monkeypatch.setattr(
        calibration_runner,
        "build_resource_calibration_summary",
        lambda *_args, **_kwargs: {"status": "passed", "summary_sha256": "6" * 64},
    )
    monkeypatch.setattr(
        calibration_runner,
        "validate_resource_calibration_summary",
        lambda *_args, **_kwargs: [],
    )

    result = calibration_runner.execute_calibration(
        manifest_path=manifest_path,
        authorization_path=authorization_path,
        output_root=output_root,
        resume=True,
    )
    assert result["status"] == "passed"
    assert observed == [(slug, slug) for slug in expected]
