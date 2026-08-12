#!/usr/bin/env python3
"""Plan or execute one provider-free Work II A-E v0.3 development phase."""

from __future__ import annotations

import argparse
import errno
import json
import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO

from chemworld.eval.provenance import write_json_atomic
from chemworld.eval.work_ii_ae_prior_qualification_v03 import (
    AEPriorQualificationV03Error,
    build_development_summary,
    build_phase_plan,
    build_phase_report,
    execute_one,
    load_resume_prefix,
    select_screen_loci,
    validate_next_receipt,
    validate_plan,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = (
    ROOT / "configs/benchmark/work_ii_ae_prior_distinguishability_v0.3_candidate.json"
)


@contextmanager
def _output_lock(path: Path) -> Iterator[None]:
    """Hold a process-scoped advisory lock without adding a runtime dependency."""

    path.parent.mkdir(parents=True, exist_ok=True)
    handle: BinaryIO = path.open("a+b")
    acquired = False
    try:
        handle.seek(0)
        if handle.read(1) == b"":
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except OSError as error:
            raise AEPriorQualificationV03Error(
                "another A-E v0.3 runner already owns this output"
            ) from error
        yield
    finally:
        try:
            if acquired:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        finally:
            handle.close()


def _pid_is_running(pid: int) -> bool:
    """Conservatively check whether a prior local runner PID is still alive."""

    if pid <= 0:
        return True
    if os.name == "nt":
        import ctypes

        process_query_limited_information = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(
            process_query_limited_information, False, pid
        )
        if not handle:
            # Access denied is treated as active; invalid PID is inactive.
            return ctypes.get_last_error() != 87
        try:
            exit_code = ctypes.c_ulong()
            if not ctypes.windll.kernel32.GetExitCodeProcess(
                handle, ctypes.byref(exit_code)
            ):
                return True
            return exit_code.value == 259
        finally:
            ctypes.windll.kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError as error:
        return error.errno != errno.ESRCH
    return True


def _load(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    value = json.loads(path.resolve().read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AEPriorQualificationV03Error(f"{path} must contain one object")
    return value


def _load_receipts(path: Path | None) -> list[dict[str, object]] | None:
    if path is None:
        return None
    resolved = path.resolve()
    if resolved.is_dir():
        try:
            files = sorted(resolved.glob("*.json"), key=lambda item: int(item.stem))
        except ValueError as error:
            raise AEPriorQualificationV03Error(
                f"{path} receipt filenames must be numeric execution indexes"
            ) from error
        if [int(item.stem) for item in files] != list(range(len(files))):
            raise AEPriorQualificationV03Error(
                f"{path} receipt indexes must be complete from zero"
            )
        values = [_load(item) for item in files]
    else:
        payload = json.loads(resolved.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise AEPriorQualificationV03Error(f"{path} must contain one receipt list")
        values = payload
    if any(not isinstance(value, dict) for value in values):
        raise AEPriorQualificationV03Error(f"{path} contains a non-object receipt")
    return values  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument(
        "--phase",
        choices=(
            "classifier_fit",
            "classifier_validation",
            "prospective_screen",
            "confirmation",
        ),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fit-report", type=Path)
    parser.add_argument("--fit-plan", type=Path)
    parser.add_argument("--fit-receipts", type=Path)
    parser.add_argument("--validation-report", type=Path)
    parser.add_argument("--validation-plan", type=Path)
    parser.add_argument("--validation-receipts", type=Path)
    parser.add_argument("--screen-report", type=Path)
    parser.add_argument("--screen-plan", type=Path)
    parser.add_argument("--screen-receipts", type=Path)
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Continue only a fully validated missing suffix in an existing output",
    )
    parser.add_argument(
        "--interrupted-pid",
        action="append",
        type=int,
        default=[],
        help="PID from the interrupted runner; repeat for wrapper/child PIDs",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and not args.resume:
        raise AEPriorQualificationV03Error("v0.3 output must not already exist")
    if args.resume and args.plan_only:
        raise AEPriorQualificationV03Error("--resume and --plan-only are incompatible")
    if args.resume and not args.interrupted_pid:
        raise AEPriorQualificationV03Error(
            "--resume requires at least one --interrupted-pid ownership check"
        )
    active_pids = [pid for pid in args.interrupted_pid if _pid_is_running(pid)]
    if active_pids:
        raise AEPriorQualificationV03Error(
            "refusing resume while prior runner PIDs remain active: "
            + ", ".join(map(str, active_pids))
        )
    lock_path = output / ".runner.lock"
    lock = _output_lock(lock_path) if args.resume else None
    if lock is not None:
        lock.__enter__()
    try:
        return _run(args, output)
    finally:
        if lock is not None:
            lock.__exit__(None, None, None)


def _run(args: argparse.Namespace, output: Path) -> int:
    fit_report = _load(args.fit_report)
    fit_plan = _load(args.fit_plan)
    fit_receipts = _load_receipts(args.fit_receipts)
    validation_report = _load(args.validation_report)
    validation_plan = _load(args.validation_plan)
    validation_receipts = _load_receipts(args.validation_receipts)
    screen_report = _load(args.screen_report)
    screen_plan = _load(args.screen_plan)
    screen_receipts = _load_receipts(args.screen_receipts)
    selection = _load(args.selection)
    plan = build_phase_plan(
        ROOT,
        args.contract.resolve(),
        args.phase,
        fit_report=fit_report,
        fit_plan=fit_plan,
        fit_receipts=fit_receipts,
        validation_report=validation_report,
        validation_plan=validation_plan,
        validation_receipts=validation_receipts,
        screen_report=screen_report,
        screen_plan=screen_plan,
        screen_receipts=screen_receipts,
        selection=selection,
    )
    errors = validate_plan(plan)
    if errors:
        raise AEPriorQualificationV03Error("invalid plan: " + "; ".join(errors))
    if not args.resume:
        output.mkdir(parents=True)
        write_json_atomic(output / "plan.json", plan)
    if args.plan_only:
        print(
            json.dumps(
                {
                    "phase": plan["phase"],
                    "primary": plan["denominators"]["primary_executions"],
                    "exact_replay": plan["denominators"]["exact_replays"],
                }
            )
        )
        return 0
    receipts: list[dict[str, object]] = load_resume_prefix(output, plan) if args.resume else []
    lock_path = output / ".runner.lock"
    lock = None if args.resume else _output_lock(lock_path)
    if lock is not None:
        lock.__enter__()
    try:
        total = len(plan["executions"])
        resume_root = output / "resume-executions"
        attempts = [
            int(path.name)
            for path in resume_root.glob("*")
            if path.is_dir() and path.name.isdigit()
        ]
        attempt = max(attempts, default=0) + 1
        for row in plan["executions"][len(receipts) :]:
            execution_root = None
            if args.resume:
                execution_root = (
                    output
                    / "resume-executions"
                    / str(attempt)
                    / str(row["execution_index"])
                )
            receipt = execute_one(ROOT, plan, row, output, execution_root=execution_root)
            next_errors = validate_next_receipt(plan, len(receipts), receipt)
            if next_errors:
                raise AEPriorQualificationV03Error(
                    "invalid write-once continuation: " + "; ".join(next_errors)
                )
            receipts.append(receipt)
            receipt_path = output / "receipts" / f"{receipt['execution_index']}.json"
            receipt_path.parent.mkdir(parents=True, exist_ok=True)
            write_json_atomic(receipt_path, receipt)
            completed = len(receipts)
            print(
                json.dumps(
                    {
                        "stage": plan["phase"],
                        "completed": completed,
                        "total": total,
                        "throughput_denominator": total,
                        "platform_failures": sum(
                            row["status"] == "platform_failure" for row in receipts
                        ),
                        "runner_pid": os.getpid(),
                    }
                ),
                flush=True,
            )
            # The failing receipt is durable before stopping; no next unit starts.
            if receipt["status"] == "platform_failure":
                write_json_atomic(
                    output / "platform-failure.json",
                    {
                        "restart_required_from_execution_zero": True,
                        "failed_execution_id": receipt["execution_id"],
                        "failure": receipt["failure"],
                    },
                )
                return 2
        contract = _load(args.contract)
        assert contract is not None
        report = build_phase_report(contract, plan, receipts, fit_report=fit_report)
        write_json_atomic(output / "report.json", report)
        if args.phase == "prospective_screen":
            selection = select_screen_loci(contract, report["locus_results"])
            write_json_atomic(output / "selection.json", selection)
        if args.phase == "confirmation":
            assert fit_report and validation_report and screen_report and selection
            summary = build_development_summary(
                contract,
                fit_report,
                validation_report,
                screen_report,
                selection,
                report,
            )
            write_json_atomic(output / "summary.json", summary)
        print(
            json.dumps({"status": report["status"], "output": str(output)}),
            flush=True,
        )
        return (
            0
            if report["status"] in {"completed", "passed", "no_eligible_tasks"}
            else 1
        )
    finally:
        if lock is not None:
            lock.__exit__(None, None, None)


if __name__ == "__main__":
    raise SystemExit(main())
