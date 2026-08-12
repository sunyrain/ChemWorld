from __future__ import annotations

import importlib.util
import json
from argparse import Namespace
from pathlib import Path

import pytest

from chemworld.eval.provenance import file_sha256
from chemworld.eval.work_ii_ae_v03_supervisor import (
    AEV03SupervisorError,
    PhaseEvidence,
    _validate_trajectory_bindings,
    next_phase_command,
    validate_external_root,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/supervise_work_ii_ae_v03.py"
CONTRACT = ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"


def _script_module():
    spec = importlib.util.spec_from_file_location("ae_v03_supervisor_script", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _evidence(tmp_path: Path, phase: str, status: str) -> PhaseEvidence:
    output = tmp_path / phase
    return PhaseEvidence(
        phase=phase,
        output=output,
        plan={"phase": phase},
        receipts=[],
        report={"phase": phase, "status": status},
        selection={"selected_task_count": 0} if phase == "prospective_screen" else None,
    )


def test_next_phase_command_binds_raw_evidence_and_uses_new_output(tmp_path: Path) -> None:
    fit = _evidence(tmp_path, "classifier_fit", "completed")
    validation = _evidence(tmp_path, "classifier_validation", "passed")
    screen = _evidence(tmp_path, "prospective_screen", "completed")
    output = tmp_path / "confirmation"
    command = next_phase_command(
        python="python",
        runner=SCRIPT,
        contract_path=CONTRACT,
        phase="confirmation",
        output=output,
        upstream={
            "classifier_fit": fit,
            "classifier_validation": validation,
            "prospective_screen": screen,
        },
    )
    assert command[:2] == ("python", str(SCRIPT))
    assert command[command.index("--output") + 1] == str(output)
    for option in (
        "--fit-plan",
        "--fit-receipts",
        "--fit-report",
        "--validation-plan",
        "--validation-receipts",
        "--validation-report",
        "--screen-plan",
        "--screen-receipts",
        "--screen-report",
        "--selection",
    ):
        assert option in command
    assert "--resume" not in command
    assert "--plan-only" not in command


def test_supervisor_paths_must_be_outside_repository(tmp_path: Path) -> None:
    with pytest.raises(AEV03SupervisorError, match="outside"):
        validate_external_root(ROOT, ROOT / "runs")
    assert validate_external_root(ROOT, tmp_path) == tmp_path.resolve()


def test_terminal_trajectory_validation_accepts_one_canonical_orphan_for_resumed_receipt(
    tmp_path: Path,
) -> None:
    bound = tmp_path / "resume-executions" / "2" / "0" / "trajectory.jsonl"
    bound.parent.mkdir(parents=True)
    bound.write_text("bound\n", encoding="utf-8")
    historical = tmp_path / "executions" / "0" / "trajectory.jsonl"
    historical.parent.mkdir(parents=True)
    historical.write_text("historical\n", encoding="utf-8")
    receipt = {
        "execution_index": 0,
        "trajectory": {
            "path": "resume-executions/2/0/trajectory.jsonl",
            "sha256": file_sha256(bound),
        },
    }
    _validate_trajectory_bindings(tmp_path, [receipt])


def test_terminal_trajectory_validation_rejects_second_canonical_orphan(
    tmp_path: Path,
) -> None:
    receipts = []
    for index in range(2):
        bound = (
            tmp_path
            / "resume-executions"
            / "2"
            / str(index)
            / "trajectory.jsonl"
        )
        bound.parent.mkdir(parents=True)
        bound.write_text(f"bound-{index}\n", encoding="utf-8")
        orphan = tmp_path / "executions" / str(index) / "trajectory.jsonl"
        orphan.parent.mkdir(parents=True)
        orphan.write_text(f"orphan-{index}\n", encoding="utf-8")
        receipts.append(
            {
                "execution_index": index,
                "trajectory": {
                    "path": f"resume-executions/2/{index}/trajectory.jsonl",
                    "sha256": file_sha256(bound),
                },
            }
        )
    with pytest.raises(AEV03SupervisorError, match="more than one"):
        _validate_trajectory_bindings(tmp_path, receipts)


def test_one_step_waits_without_terminal_fit_and_does_not_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _script_module()
    fit = tmp_path / "fit"
    fit.mkdir()
    pipeline = tmp_path / "pipeline"
    logs = tmp_path / "logs"
    monkeypatch.setattr(module, "ROOT", ROOT)
    monkeypatch.setattr(
        module, "validate_external_root", lambda _root, candidate: candidate.resolve()
    )
    monkeypatch.setattr(
        module.subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail("waiting inspection must not launch"),
    )
    status, command = module.inspect_once(
        Namespace(
            pipeline_root=pipeline,
            log_root=logs,
            fit_output=fit,
            contract=CONTRACT,
            execute=False,
        )
    )
    assert status == "waiting"
    assert command == ()
    assert not logs.exists()


def test_completed_fit_plans_validation_but_default_dry_run_does_not_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _script_module()
    fit = _evidence(tmp_path, "classifier_fit", "completed")
    fit.output.mkdir(parents=True)
    (fit.output / "report.json").write_text("{}", encoding="utf-8")
    pipeline = tmp_path / "pipeline"
    logs = tmp_path / "logs"
    monkeypatch.setattr(module, "ROOT", ROOT)
    monkeypatch.setattr(
        module, "validate_external_root", lambda _root, candidate: candidate.resolve()
    )
    monkeypatch.setattr(
        module,
        "validate_terminal_output",
        lambda **kwargs: fit,
    )
    monkeypatch.setattr(
        module.subprocess,
        "Popen",
        lambda *args, **kwargs: pytest.fail("dry run must not launch"),
    )
    status, command = module.inspect_once(
        Namespace(
            pipeline_root=pipeline,
            log_root=logs,
            fit_output=fit.output,
            contract=CONTRACT,
            execute=False,
        )
    )
    assert status == "ready"
    assert command[command.index("--phase") + 1] == "classifier_validation"
    event = json.loads(
        (logs / "supervisor.jsonl").read_text(encoding="utf-8").splitlines()[-1]
    )
    assert event["event"] == "phase_ready"
    assert event["execute"] is False


def test_existing_nonterminal_validation_waits_without_revalidating_fit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _script_module()
    fit = tmp_path / "fit"
    fit.mkdir()
    (fit / "report.json").write_text("{}", encoding="utf-8")
    pipeline = tmp_path / "pipeline"
    validation = pipeline / "classifier-validation"
    validation.mkdir(parents=True)
    calls = []
    monkeypatch.setattr(
        module, "validate_external_root", lambda _root, candidate: candidate.resolve()
    )
    monkeypatch.setattr(
        module,
        "validate_terminal_output",
        lambda **kwargs: calls.append(kwargs) or pytest.fail("must not deep-validate"),
    )
    status, command = module.inspect_once(
        Namespace(
            pipeline_root=pipeline,
            log_root=tmp_path / "logs",
            fit_output=fit,
            contract=CONTRACT,
            execute=False,
        )
    )
    assert status == "waiting"
    assert command == ()
    assert calls == []


def test_validation_scientific_rejection_is_normal_terminal_stop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _script_module()
    fit = _evidence(tmp_path, "classifier_fit", "completed")
    validation = _evidence(tmp_path, "classifier_validation", "scientifically_rejected")
    fit.output.mkdir(parents=True)
    validation.output.mkdir(parents=True)
    (fit.output / "report.json").write_text("{}", encoding="utf-8")
    (validation.output / "report.json").write_text("{}", encoding="utf-8")
    pipeline = tmp_path / "pipeline"
    paths = module._phase_paths(pipeline, fit.output)
    paths["classifier_validation"] = validation.output
    monkeypatch.setattr(module, "_phase_paths", lambda *_args: paths)
    monkeypatch.setattr(
        module, "validate_external_root", lambda _root, candidate: candidate.resolve()
    )
    monkeypatch.setattr(
        module,
        "validate_terminal_output",
        lambda **kwargs: fit if kwargs["phase"] == "classifier_fit" else validation,
    )
    status, command = module.inspect_once(
        Namespace(
            pipeline_root=pipeline,
            log_root=tmp_path / "logs",
            fit_output=fit.output,
            contract=CONTRACT,
            execute=True,
        )
    )
    assert status == "scientifically_rejected"
    assert command == ()
