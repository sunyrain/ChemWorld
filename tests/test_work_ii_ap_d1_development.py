from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import pytest
import scripts.run_work_ii_campaign_pilot as cell_runner
import scripts.run_work_ii_five_seed_campaign as matrix_runner

from chemworld.eval.provenance import file_sha256
from chemworld.eval.work_ii_ap_d1_development import (
    AP_D1_DEVELOPMENT_AUTHORIZATION_VERSION,
    AP_D1_REQUALIFICATION_AUTHORIZATION_VERSION,
    build_ap_d1_development_cost_budget,
    validate_and_claim_ap_d1_development_attempt,
    validate_ap_d1_development_authorization,
    validate_ap_d1_development_config,
)
from chemworld.eval.work_ii_d1_execution import D1CellStore

ROOT = Path(__file__).resolve().parents[1]
READINESS = (
    ROOT / "workstreams/flagship_tasks/reports/"
    "work-ii-ap-independent-terminal-d1-readiness-v0.1.json"
)
CONFIGS = (
    ROOT / "configs/benchmark/work_ii_reaction_safety_independent_terminal_d1_execution_seed2.json",
    ROOT / "configs/benchmark/work_ii_electrochemical_independent_terminal_d1_execution_seed2.json",
)
DEEPSEEK_CONFIGS = (
    ROOT / "configs/benchmark/"
    "work_ii_reaction_safety_independent_terminal_d1_execution_seed2_deepseek_v4_flash.json",
    ROOT / "configs/benchmark/"
    "work_ii_electrochemical_independent_terminal_d1_execution_seed2_deepseek_v4_flash.json",
)


def _authorization(configs: tuple[Path, ...], outputs: tuple[Path, ...]) -> dict[str, object]:
    blocks = []
    providers = []
    for config_path, output in zip(configs, outputs, strict=True):
        config = json.loads(config_path.read_text(encoding="utf-8"))
        providers.append((config["provider"]["id"], config["provider"]["model"]))
        blocks.append(
            {
                "task_id": config["task_id"],
                "world_seed": 2,
                "campaign_config": config_path.relative_to(ROOT).as_posix(),
                "campaign_config_sha256": cell_runner.file_sha256(config_path),
                "output_root": output.relative_to(ROOT).as_posix(),
            }
        )
    if len(set(providers)) != 1:
        raise ValueError("one authorization must contain exactly one provider")
    provider_id, model = providers[0]
    authorization = {
        "schema_version": AP_D1_DEVELOPMENT_AUTHORIZATION_VERSION,
        "status": "authorized",
        "authorized_by": "user",
        "approved_at": "2026-08-13T00:00:00+08:00",
        "provider_execution_allowed": True,
        "formal_result": False,
        "formal_r5_authorized": False,
        "participant_outcomes_observed_before_authorization": 0,
        "provider": {"provider_id": provider_id, "model": model},
        "task_blocks": blocks,
        "provider_sessions_initial": len(blocks) * 3,
        "provider_process_attempts_hard_cap": len(blocks) * 6,
        "complete_experiments_total": len(blocks) * 30,
        "currency": "USD",
        "spending_limit": "finite_ceiling",
        "currency_ceiling_usd": 100.0,
        "credential_rotation_confirmed": True,
        "pricing": {
            "source": "user-confirmed-provider-price-card",
            "observed_at": "2026-08-13T00:00:00+08:00",
            "unit": "usd_per_million_tokens",
            "cache_hit_input": 0.1,
            "cache_miss_input": 1.0,
            "output": 2.0,
        },
    }
    budget = build_ap_d1_development_cost_budget(ROOT, authorization)
    authorization["initial_schedule_cost_cap_usd"] = budget["initial_schedule_cost_cap_usd"]
    authorization["all_infrastructure_resumes_cost_cap_usd"] = budget[
        "all_infrastructure_resumes_cost_cap_usd"
    ]
    authorization["currency_ceiling_usd"] = budget["all_infrastructure_resumes_cost_cap_usd"]
    return authorization


def test_real_seed2_execution_configs_compile_without_release_freeze() -> None:
    for config in (*CONFIGS, *DEEPSEEK_CONFIGS):
        assert validate_ap_d1_development_config(ROOT, config) == []


def test_deepseek_unlimited_authorization_is_exact_and_provider_bound(
    tmp_path: Path,
) -> None:
    outputs = (
        ROOT / "runs/development/ap-deepseek-reaction-seed2",
        ROOT / "runs/development/ap-deepseek-electro-seed2",
    )
    authorization = _authorization(DEEPSEEK_CONFIGS, outputs)
    authorization["spending_limit"] = "unlimited"
    authorization["currency_ceiling_usd"] = None
    authorization["credential_rotation_confirmed"] = False
    authorization["credential_use_authorized"] = True
    authorization.pop("pricing")
    authorization.pop("initial_schedule_cost_cap_usd")
    authorization.pop("all_infrastructure_resumes_cost_cap_usd")
    path = tmp_path / "deepseek-authorization.json"
    path.write_text(json.dumps(authorization), encoding="utf-8")

    for config, output in zip(DEEPSEEK_CONFIGS, outputs, strict=True):
        _, errors = validate_ap_d1_development_authorization(
            ROOT,
            path,
            config_path=config,
            output_root=output,
            readiness_path=READINESS,
        )
        assert errors == []


def test_platform_requalification_authorization_retains_historical_outcomes(
    tmp_path: Path,
) -> None:
    outputs = (
        ROOT / "runs/development/ap-deepseek-reaction-seed2-requalification",
        ROOT / "runs/development/ap-deepseek-electro-seed2-requalification",
    )
    authorization = _authorization(DEEPSEEK_CONFIGS, outputs)
    authorization.pop("participant_outcomes_observed_before_authorization")
    authorization.update(
        {
            "schema_version": AP_D1_REQUALIFICATION_AUTHORIZATION_VERSION,
            "authorization_scope": (
                "platform_requalification_after_retained_development_diagnosis"
            ),
            "current_requalification_outcomes_observed_before_authorization": 0,
            "historical_development_cells_observed_before_requalification": 12,
            "historical_development_outputs_retained": True,
            "fresh_output_roots": True,
            "platform_requalification_only": True,
            "scientific_design_changed_after_historical_outcomes": False,
            "resource_envelope_calibration_basis": (
                "provider_usage_only_without_scientific_effect_selection"
            ),
        }
    )
    path = tmp_path / "requalification-authorization.json"
    path.write_text(json.dumps(authorization), encoding="utf-8")

    for config, output in zip(DEEPSEEK_CONFIGS, outputs, strict=True):
        _, errors = validate_ap_d1_development_authorization(
            ROOT,
            path,
            config_path=config,
            output_root=output,
            readiness_path=READINESS,
        )
        assert errors == []

    authorization["scientific_design_changed_after_historical_outcomes"] = True
    path.write_text(json.dumps(authorization), encoding="utf-8")
    _, errors = validate_ap_d1_development_authorization(
        ROOT,
        path,
        config_path=DEEPSEEK_CONFIGS[0],
        output_root=outputs[0],
        readiness_path=READINESS,
    )
    assert any("retained-platform-requalification" in error for error in errors)


def test_authorization_names_exact_outputs_and_denominators(tmp_path: Path) -> None:
    outputs = (
        ROOT / "runs/development/ap-reaction-seed2",
        ROOT / "runs/development/ap-electro-seed2",
    )
    path = tmp_path / "authorization.json"
    path.write_text(json.dumps(_authorization(CONFIGS, outputs)), encoding="utf-8")

    _, errors = validate_ap_d1_development_authorization(
        ROOT,
        path,
        config_path=CONFIGS[0],
        output_root=outputs[0],
        readiness_path=READINESS,
    )
    assert errors == []

    changed = json.loads(path.read_text(encoding="utf-8"))
    changed["complete_experiments_total"] = 59
    path.write_text(json.dumps(changed), encoding="utf-8")
    _, errors = validate_ap_d1_development_authorization(
        ROOT,
        path,
        config_path=CONFIGS[0],
        output_root=outputs[0],
        readiness_path=READINESS,
    )
    assert "A-P development authorization denominator mismatch" in errors

    changed = _authorization(CONFIGS, outputs)
    changed["currency_ceiling_usd"] = 0.01
    path.write_text(json.dumps(changed), encoding="utf-8")
    _, errors = validate_ap_d1_development_authorization(
        ROOT,
        path,
        config_path=CONFIGS[0],
        output_root=outputs[0],
        readiness_path=READINESS,
    )
    assert "A-P development currency ceiling does not cover all attempts" in errors

    changed = _authorization(CONFIGS, outputs)
    changed["spending_limit"] = "unlimited"
    changed["currency_ceiling_usd"] = None
    changed.pop("pricing")
    changed.pop("initial_schedule_cost_cap_usd")
    changed.pop("all_infrastructure_resumes_cost_cap_usd")
    path.write_text(json.dumps(changed), encoding="utf-8")
    _, errors = validate_ap_d1_development_authorization(
        ROOT,
        path,
        config_path=CONFIGS[0],
        output_root=outputs[0],
        readiness_path=READINESS,
    )
    assert errors == []


def test_cell_runner_rejects_missing_explicit_authorization_before_cell(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cell_runner,
        "_run_cell",
        lambda **_kwargs: pytest.fail("provider cell must not start"),
    )
    with pytest.raises(RuntimeError, match="requires authorization"):
        cell_runner.run(
            argparse.Namespace(
                config=CONFIGS[0],
                output=ROOT / "runs/development/ap-reaction-seed2/attempt",
                progress_file=tmp_path / "progress.jsonl",
                world_seed=2,
                prior_arm="opaque",
                ap_development_execution=True,
                ap_development_authorization=None,
                ap_development_readiness=READINESS,
                ap_development_authorized_output_root=(ROOT / "runs/development/ap-reaction-seed2"),
                formal_manifest=None,
                release_manifest=None,
                qualification_execution=False,
                qualification_authorization=None,
                qualification_attempt_authorization=None,
                qualification_cost_ledger=None,
                resource_calibration_execution=False,
                resource_calibration_manifest=None,
                resource_calibration_authorization=None,
                resource_calibration_cost_reservation=None,
            )
        )


def test_matrix_runner_rejects_missing_authorization_before_output_or_provider(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        matrix_runner.subprocess,
        "Popen",
        lambda *_args, **_kwargs: pytest.fail("provider process must not start"),
    )
    output = ROOT / "runs/development/ap-reaction-seed2-test-never-created"
    with pytest.raises(RuntimeError, match="requires explicit authorization"):
        matrix_runner.run(
            argparse.Namespace(
                config=CONFIGS[0],
                output=output,
                progress_file=tmp_path / "progress.jsonl",
                world_seed=[2],
                heartbeat_interval_s=30.0,
                max_concurrency=3,
                readiness_receipt=None,
                release_manifest=None,
                ap_development_execution=True,
                ap_development_authorization=None,
                ap_development_readiness=READINESS,
                resume=False,
            )
        )
    assert not output.exists()


def test_matrix_runner_rejects_seed_drift_before_output_or_provider(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        matrix_runner.subprocess,
        "Popen",
        lambda *_args, **_kwargs: pytest.fail("provider process must not start"),
    )
    outputs = (
        ROOT / "runs/development/ap-reaction-seed2-test-seed-drift",
        ROOT / "runs/development/ap-electro-seed2-test-seed-drift",
    )
    authorization_path = tmp_path / "authorization.json"
    authorization_path.write_text(json.dumps(_authorization(CONFIGS, outputs)), encoding="utf-8")
    with pytest.raises(RuntimeError, match="seed differs"):
        matrix_runner.run(
            argparse.Namespace(
                config=CONFIGS[0],
                output=outputs[0],
                progress_file=tmp_path / "progress.jsonl",
                world_seed=[3],
                heartbeat_interval_s=30.0,
                max_concurrency=3,
                readiness_receipt=None,
                release_manifest=None,
                ap_development_execution=True,
                ap_development_authorization=authorization_path,
                ap_development_readiness=READINESS,
                resume=False,
            )
        )
    assert not outputs[0].exists()


def test_child_attempt_receipt_is_exact_and_single_use(tmp_path: Path) -> None:
    output = ROOT / "runs/development/ap-reaction-attempt-claim-test"
    config = json.loads(CONFIGS[0].read_text(encoding="utf-8"))
    store = D1CellStore(
        output / "store",
        config_path=CONFIGS[0],
        task_id=config["task_id"],
        world_seeds=[2],
        arms=list(config["prior_arms"]),
    )
    key = store.key(2, "opaque")
    attempt_id = "test-attempt"
    receipt = store.record_provider_attempt_launch(key, attempt_id=attempt_id)
    authorization_path = tmp_path / "child-authorization.json"
    authorization_path.write_text(
        json.dumps(
            {
                "status": "authorized",
                "provider_execution_allowed": True,
                "formal_result": False,
                "formal_r5_authorized": False,
                "provider": {
                    "provider_id": config["provider"]["id"],
                    "model": config["provider"]["model"],
                },
            }
        ),
        encoding="utf-8",
    )
    cost_ledger = output / "cost_ledgers" / key / f"{attempt_id}.json"
    cost_ledger.parent.mkdir(parents=True)
    cost_ledger.write_text(
        json.dumps(
            {
                "state": "full_token_cap_reserved_before_provider_launch",
                "task_id": config["task_id"],
                "cell_key_sha256": key,
                "attempt_id": attempt_id,
                "authorization_sha256": file_sha256(authorization_path),
                "readiness_sha256": file_sha256(READINESS),
                "within_authorized_ceiling": True,
            }
        ),
        encoding="utf-8",
    )
    attempt_output = output / "attempts" / key / attempt_id
    try:
        claim = validate_and_claim_ap_d1_development_attempt(
            ROOT,
            config_path=CONFIGS[0],
            output_root=output,
            attempt_output=attempt_output,
            attempt_receipt_path=receipt,
            cost_ledger_path=cost_ledger,
            world_seed=2,
            arm="opaque",
            authorization_path=authorization_path,
            readiness_path=READINESS,
        )
        assert claim["attempt_id"] == attempt_id
        with pytest.raises(ValueError, match="already claimed"):
            validate_and_claim_ap_d1_development_attempt(
                ROOT,
                config_path=CONFIGS[0],
                output_root=output,
                attempt_output=attempt_output,
                attempt_receipt_path=receipt,
                cost_ledger_path=cost_ledger,
                world_seed=2,
                arm="opaque",
                authorization_path=authorization_path,
                readiness_path=READINESS,
            )
    finally:
        if output.exists():
            shutil.rmtree(output)


def test_matrix_runner_passes_exact_development_authorization_to_children(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output = ROOT / "runs/development/ap-reaction-seed2-test-authorized"
    authorization_path = tmp_path / "authorization.json"
    authorization_path.write_text(
        json.dumps(
            _authorization(
                CONFIGS,
                (
                    output,
                    ROOT / "runs/development/ap-electro-seed2-test-authorized",
                ),
            )
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        matrix_runner,
        "validate_ap_d1_development_authorization",
        lambda *_args, **_kwargs: (
            json.loads(authorization_path.read_text(encoding="utf-8")),
            [],
        ),
    )
    monkeypatch.setattr(matrix_runner, "git_source_commit", lambda _root: "development")
    monkeypatch.setenv("WELLAU_API_KEY", "test-only-no-network")

    commands: list[list[str]] = []

    class FakeStream:
        def __iter__(self):
            return iter(())

    class FakeProcess:
        stdout = FakeStream()

        def poll(self):
            return 1

        def wait(self, timeout=None):
            return 1

    def fake_popen(command, **_kwargs):
        commands.append(command)
        return FakeProcess()

    monkeypatch.setattr(matrix_runner.subprocess, "Popen", fake_popen)
    try:
        report = matrix_runner.run(
            argparse.Namespace(
                config=CONFIGS[0],
                output=output,
                progress_file=tmp_path / "progress.jsonl",
                world_seed=[2],
                heartbeat_interval_s=0.01,
                max_concurrency=3,
                readiness_receipt=None,
                release_manifest=None,
                ap_development_execution=True,
                ap_development_authorization=authorization_path,
                ap_development_readiness=READINESS,
                resume=False,
            )
        )
        assert report["development_only"] is True
        assert report["formal_r5_authorized"] is False
        assert len(commands) == 3
        assert all("--ap-development-execution" in command for command in commands)
        assert all("--ap-development-attempt-receipt" in command for command in commands)
        assert all("--ap-development-cost-ledger" in command for command in commands)
        assert all("--release-manifest" not in command for command in commands)
    finally:
        if output.exists():
            shutil.rmtree(output)
