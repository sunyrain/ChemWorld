#!/usr/bin/env python3
"""Observe and optionally advance the provider-free Work II A-E v0.3 phases."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from chemworld.eval.work_ii_ae_v03_supervisor import (
    PHASE_ORDER,
    AEV03SupervisorError,
    next_phase_command,
    validate_external_root,
    validate_terminal_output,
)

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts/run_work_ii_ae_prior_qualification_v03.py"
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)


def _emit(log: Path, event: dict[str, object]) -> None:
    payload = {"unix_time": time.time(), **event}
    line = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    print(line, flush=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")


def _phase_paths(base: Path, fit_output: Path) -> dict[str, Path]:
    return {
        "classifier_fit": fit_output.resolve(),
        "classifier_validation": base / "classifier-validation",
        "prospective_screen": base / "prospective-screen",
        "confirmation": base / "confirmation",
    }


def inspect_once(args: argparse.Namespace) -> tuple[str, tuple[str, ...]]:
    base = validate_external_root(ROOT, args.pipeline_root)
    log_root = validate_external_root(ROOT, args.log_root)
    fit_output = validate_external_root(ROOT, args.fit_output)
    paths = _phase_paths(base, fit_output)
    next_phase = None
    for phase in PHASE_ORDER:
        output = paths[phase]
        if (output / "platform-failure.json").exists():
            raise AEV03SupervisorError(f"{phase} stopped with platform failure")
        terminal = (output / "report.json").is_file()
        if phase == "prospective_screen":
            terminal = terminal and (output / "selection.json").is_file()
        elif phase == "confirmation":
            terminal = terminal and (output / "summary.json").is_file()
        if terminal:
            continue
        if phase == "classifier_fit" or output.exists():
            return "waiting", ()
        next_phase = phase
        break

    upstream = {}
    for phase in PHASE_ORDER:
        if phase == next_phase:
            break
        output = paths[phase]
        evidence = validate_terminal_output(
            root=ROOT,
            contract_path=args.contract.resolve(),
            output=output,
            phase=phase,
            upstream=upstream,
        )
        upstream[phase] = evidence
        status = str(evidence.report["status"])
        _emit(
            log_root / "supervisor.jsonl",
            {"event": "phase_validated", "phase": phase, "status": status},
        )
        if phase == "classifier_validation" and status != "passed":
            return "scientifically_rejected", ()
        if phase == "confirmation":
            return "completed", ()
    if next_phase is None:
        raise AEV03SupervisorError("supervisor state machine exhausted unexpectedly")
    output = paths[next_phase]
    command = next_phase_command(
        python=sys.executable,
        runner=RUNNER,
        contract_path=args.contract.resolve(),
        phase=next_phase,
        output=output,
        upstream=upstream,
    )
    _emit(
        log_root / "supervisor.jsonl",
        {
            "event": "phase_ready",
            "phase": next_phase,
            "output": str(output),
            "execute": bool(args.execute),
            "command": list(command),
        },
    )
    if not args.execute:
        return "ready", command
    output.parent.mkdir(parents=True, exist_ok=True)
    phase_log = log_root / f"{next_phase}.log"
    with phase_log.open("a", encoding="utf-8", newline="\n") as handle:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=handle,
            stderr=subprocess.STDOUT,
            text=True,
        )
    _emit(
        log_root / "supervisor.jsonl",
        {"event": "phase_started", "phase": next_phase, "pid": process.pid},
    )
    return "started", command


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fit-output", type=Path, required=True)
    parser.add_argument("--pipeline-root", type=Path, required=True)
    parser.add_argument("--log-root", type=Path, required=True)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    inspect_once(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
