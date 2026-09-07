"""Sequential GPT-first information intervention using the existing direct harness."""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

from scripts.run_work_ii_final_diagnostic import collect, digest, read, run_session, write

from chemworld.eval.work_ii_information_intervention import cells_for_world, prompt, summarize

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/work_ii_information_intervention_20260906.json"
SURFACE = (
    "scripts/run_work_ii_information_intervention.py",
    "scripts/run_work_ii_final_diagnostic.py",
    "scripts/run_work_ii_study_b.py",
    "src/chemworld/eval/work_ii_information_intervention.py",
    "src/chemworld/eval/work_ii_final_diagnostic.py",
    "src/chemworld/agents/diagnostic_numerics.py",
    "uv.lock",
)


def prepare(root: Path, phase: str, model: str) -> None:
    if root.exists():
        raise FileExistsError("preserve existing block; run resumes only unattempted units")
    protocol = read(PROTOCOL)
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_87_information_completeness"]
    report = read(ROOT / binding["endpoint_report"])
    if not report["gpt_development_ready"]:
        raise ValueError("complete public reference not qualified")
    if phase == "development":
        source = ROOT / report["development_run"]
        worlds = [
            {
                "cluster_id": "W2-87-development-1",
                "target_exponent": 1.75,
                "public_packet": read(source / "public_packet.json"),
                "scoring_truth": read(source / "private_scoring_truth.json"),
            }
        ]
    else:
        stimuli = read(ROOT / protocol["formal_stimuli"])
        if stimuli["status"] != "qualified" or len(stimuli["worlds"]) != 10:
            raise ValueError("ten-world fixed stimuli are not qualified")
        worlds = stimuli["worlds"]
    cells = [c for i, w in enumerate(worlds) for c in cells_for_world(w, model, i)]
    budgets = protocol[phase][model]
    if budgets is None:
        raise ValueError("model budgets not calibrated")
    execution_protocol = {"providers": protocol["providers"], phase: budgets}
    write(
        root / "inputs.json",
        {
            "phase": phase,
            "model": model,
            "cells": cells,
            "protocol": execution_protocol,
            "reference_binding": binding,
        },
    )
    print(f"prepared {model} {phase}: {len(cells)} sessions / {len(cells) * 2} turns", flush=True)


def surface(provider: dict | None = None) -> dict:
    paths = list(SURFACE)
    if provider and provider.get("model_catalog_json"):
        paths.append(provider["model_catalog_json"])
    if provider and provider.get("transport") == "standard_http_headers":
        paths.append("src/chemworld/providers/responses_header_transport.py")
    return {p: digest(ROOT / p) for p in paths}


def freeze(root: Path) -> None:
    inputs = read(root / "inputs.json")
    if inputs["phase"] != "formal" or (root / "sessions").exists():
        raise ValueError("freeze requires unstarted formal block")
    if (root / "freeze.json").exists():
        raise FileExistsError("already frozen")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise ValueError("one clean source commit required at formal freeze")
    write(
        root / "freeze.json",
        {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "execution_surface": surface(inputs["protocol"]["providers"][inputs["model"]]),
            "inputs_sha256": digest(root / "inputs.json"),
        },
    )
    print("formal frozen once", flush=True)


def authorized_resume(root: Path) -> dict | None:
    """A later explicit resume supersedes only the stop record it names."""
    path = root / "user_resume.json"
    if not path.exists() or not (root / "user_stop.json").exists():
        return None
    record = read(path)
    if record.get("user_stop_sha256") != digest(root / "user_stop.json"):
        return None
    return record


def resume_frozen(
    root: Path,
    export: Path | None = None,
    *,
    without_block_deadline: bool = False,
    workers: int = 1,
) -> None:
    """Resume frozen sessions, optionally applying an explicit calendar amendment."""
    if (root / "executor.lock").exists():
        raise ValueError("executor is already active; preserve its work")
    if workers not in (1, 2, 3) or (workers > 1 and not without_block_deadline):
        raise ValueError("parallel resume requires an explicit calendar amendment and 2-3 workers")
    if workers > 1 and read(root / "parallel_schedule.json")["requested_workers"] != workers:
        raise ValueError("parallel worker count was not recorded")
    if not (root / "user_stop.json").exists() or (
        (root / "user_resume.json").exists() and not without_block_deadline
    ):
        raise ValueError("requires an explicitly stopped block without a previous resume")
    inputs, frozen, ledger = (
        read(root / name) for name in ("inputs.json", "freeze.json", "block.json")
    )
    if inputs["phase"] != "formal" or digest(root / "inputs.json") != frozen["inputs_sha256"]:
        raise ValueError("frozen formal inputs changed")
    amendment = None
    if without_block_deadline:
        amendment = read(root / "block_deadline_override.json")
        if (
            not authorized_resume(root)
            or amendment["original_deadline_epoch"] != ledger["deadline_epoch"]
            or amendment["effective_deadline_epoch"] is not None
        ):
            raise ValueError("calendar amendment must retain the original stop/resume and deadline")
        if any(
            (result.get("failure") or "").startswith(("platform_", "forbidden_"))
            for result in collect(root, inputs["cells"])
        ):
            raise ValueError("calendar amendment does not override platform/boundary stop rules")
    if not without_block_deadline and time.time() >= ledger["deadline_epoch"]:
        raise ValueError("original block deadline elapsed; do not reset the budget")
    if digest(ROOT / "uv.lock") != frozen["execution_surface"]["uv.lock"]:
        raise ValueError("resume requires the original locked environment")
    if export and (export.exists() or export.with_suffix(".md").exists()):
        raise FileExistsError("preserve existing exported report")
    archive = subprocess.check_output(
        ["git", "archive", frozen["source_commit"], "scripts", "src", "configs", "uv.lock"],
        cwd=ROOT,
    )
    with tempfile.TemporaryDirectory(prefix="chemworld-frozen-information-") as temporary:
        snapshot = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(snapshot, filter="data")
        for name, expected in frozen["execution_surface"].items():
            if digest(snapshot / name) != expected:
                raise ValueError(f"historical execution surface mismatch: {name}")
        provider = inputs["protocol"]["providers"][inputs["model"]]
        if provider.get("api_key_file"):
            credential = Path(provider["api_key_file"])
            if not credential.is_absolute():
                destination = snapshot / credential
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / credential, destination)
        # Recheck immediately before handing the unchanged block to its old executor.
        if (root / "executor.lock").exists() or (
            not without_block_deadline and time.time() >= ledger["deadline_epoch"]
        ):
            raise ValueError("executor active or original deadline elapsed")
        record = {
            "requested_epoch": time.time(),
            "reason": "user_requested_restore_original_design",
            "user_stop_sha256": digest(root / "user_stop.json"),
            "source_commit": frozen["source_commit"],
            "deadline_epoch": ledger["deadline_epoch"],
            "budget_policy": "original_calendar_deadline_unchanged",
            "resume_policy": "unattempted_only_preserve_all_failures_and_interruptions",
        }
        if amendment is None:
            with (root / "user_resume.json").open("x", encoding="utf-8") as handle:
                json.dump(record, handle, indent=2)
                handle.write("\n")
        else:
            amendment.update(
                status="running_without_calendar_deadline",
                activated_epoch=time.time(),
                continuation_source_commit=subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
                ).strip(),
            )
            write(root / "block_deadline_override.json", amendment)
            record = amendment
        bootstrap = """import sys
from pathlib import Path
sys.path[:0] = [sys.argv[1], str(Path(sys.argv[1]) / 'src')]
from scripts import run_work_ii_information_intervention as runner
root = Path(sys.argv[2])
if sys.argv[3] == 'without_block_deadline':
    original_read = runner.read
    def amended_read(path):
        value = original_read(path)
        if path == root / 'block.json':
            return {**value, 'deadline_epoch': float('inf')}
        return value
    runner.read = amended_read
if int(sys.argv[4]) > 1:
    import runpy
    run_parallel = runpy.run_path(sys.argv[5])['run_parallel']
    run_parallel(root, runner, int(sys.argv[4]))
else:
    runner.run(root)
"""
        print(json.dumps({"stage": "resume_frozen", **record}), flush=True)
        result = subprocess.run(
            [
                sys.executable,
                "-u",
                "-c",
                bootstrap,
                str(snapshot),
                str(root),
                "without_block_deadline" if without_block_deadline else "original_deadline",
                str(workers),
                str(ROOT / "scripts/run_work_ii_information_parallel.py"),
            ],
            cwd=ROOT,
            check=False,
        )
        # The original executor owns data production; the current analyzer fixes
        # cumulative usage and records the stop/resume history after it exits.
        if not (root / "executor.lock").exists():
            if amendment is not None:
                amendment.update(
                    status="finished_without_calendar_deadline", finished_epoch=time.time()
                )
                write(root / "block_deadline_override.json", amendment)
            report = analyze(root, export)
            print(
                json.dumps(
                    {"stage": "finished", "status": report["status"], "counts": report["counts"]}
                ),
                flush=True,
            )
        if result.returncode:
            raise RuntimeError(
                f"historical executor exited {result.returncode}; inspect preserved records"
            )


def analyze(root: Path, export: Path | None = None) -> dict:
    inputs = read(root / "inputs.json")
    results = collect(root, inputs["cells"])
    report = summarize(results, inputs["cells"], formal=inputs["phase"] == "formal")
    report.update(
        phase=inputs["phase"],
        provider=inputs["protocol"]["providers"][inputs["model"]],
        budgets=inputs["protocol"][inputs["phase"]],
        reference_binding=inputs["reference_binding"],
    )
    if (root / "freeze.json").exists():
        report["freeze"] = read(root / "freeze.json")
    amendment_path = root / "block_deadline_override.json"
    amendment = read(amendment_path) if amendment_path.exists() else None
    if amendment and not amendment.get("activated_epoch"):
        amendment = None
    if (root / "user_stop.json").exists():
        report["user_stop"] = read(root / "user_stop.json")
        resumed = authorized_resume(root)
        if resumed:
            report["user_resume"] = resumed
            report["interpretation"] += (
                " The user authorized resuming the original configuration and calendar deadline. "
                "Only previously unattempted units resumed; all failures and interruptions remain."
            )
            if (
                report["counts"].get("unstarted")
                and amendment is None
                and time.time() >= resumed["deadline_epoch"]
            ):
                report["status"] = "deadline_reached_with_unstarted"
        else:
            report["status"] = "stopped_by_user"
            report["interpretation"] += (
                " This block was stopped by the user for a configuration change; all attempted, "
                "interrupted and unstarted units are retained. It is excluded from the new block."
            )
    if amendment is not None:
        report["schedule_amendment"] = amendment
        report["effective_budgets"] = {**report["budgets"], "block_timeout_s": None}
        report["interpretation"] += (
            " The user subsequently removed the block calendar deadline. This is a disclosed "
            "scheduling amendment, not an unchanged original block stopping rule. Turn/session "
            "timeouts, tool limits, coverage, failure rules and all earlier outcomes were retained."
        )
    parallel_path = root / "parallel_schedule.json"
    if parallel_path.exists() and (parallel := read(parallel_path)).get("activated_epoch"):
        report["parallel_schedule_amendment"] = parallel
        report["interpretation"] += (
            f" The user also authorized up to {parallel['requested_workers']} concurrent "
            "independent sessions for the remaining queue. Dispatch followed original indices; "
            "completion order could differ. Rate-limit events and concurrency changes are retained."
        )
    write(root / "summary.json", report)
    lines = [
        "# W2-87 information completeness",
        "",
        f"{inputs['model']} / {inputs['phase']}: {report['status']}; "
        f"{report['scheduled']} scheduled.",
        "",
        "| Information | Analysis | Recovery / scheduled | Status counts |",
        "| --- | --- | --- | --- |",
    ]
    for group in report["groups"]:
        lines.append(
            f"| {group['information']} | {group['analysis']} | "
            f"{group['joint_recovery']}/{group['scheduled']} | {json.dumps(group['counts'])} |"
        )
    lines.extend(
        [
            "",
            f"Primary: {json.dumps(report['primary'])}",
            "",
            report["interpretation"],
            "",
            f"Effective budgets: {json.dumps(report.get('effective_budgets', report['budgets']))}",
            "",
            "Resources:",
            "```json",
            json.dumps(report["resources"], indent=2),
            "```",
            "",
            "All failures / unstarted:",
            *[f"- {r['cell_id']}: {r['status']} / {r['failure']}" for r in report["failures"]],
        ]
    )
    content = "\n".join(lines) + "\n"
    (root / "summary.md").write_text(content, encoding="utf-8", newline="\n")
    if export:
        if export.exists() or export.with_suffix(".md").exists():
            raise FileExistsError("do not overwrite an exported terminal block")
        write(export, report)
        export.with_suffix(".md").write_text(content, encoding="utf-8", newline="\n")
    return report


def run(root: Path) -> None:
    if (root / "user_stop.json").exists() and not authorized_resume(root):
        raise ValueError("user-stopped block requires explicit resume-frozen authorization")
    inputs = read(root / "inputs.json")
    if inputs["phase"] == "formal":
        frozen = read(root / "freeze.json")
        provider = inputs["protocol"]["providers"][inputs["model"]]
        if frozen["execution_surface"] != surface(provider) or frozen["inputs_sha256"] != digest(
            root / "inputs.json"
        ):
            raise ValueError("frozen inputs or runtime changed")
    ledger = root / "block.json"
    if not ledger.exists():
        write(
            ledger,
            {
                "started_epoch": time.time(),
                "deadline_epoch": time.time()
                + inputs["protocol"][inputs["phase"]]["block_timeout_s"],
            },
        )
    deadline = read(ledger)["deadline_epoch"]
    existing = collect(root, inputs["cells"])
    terminal = {r["cell_id"] for r in existing}
    started, done = time.monotonic(), len(existing)
    with (root / "executor.lock").open("x", encoding="utf-8") as lock:
        lock.write(str(os.getpid()))
    try:
        for index, cell in enumerate(inputs["cells"]):
            if cell["cell_id"] in terminal:
                continue
            if time.time() >= deadline:
                print("deadline; preserve unstarted denominator", flush=True)
                break
            rate = (done - len(existing)) / max(time.monotonic() - started, 1)
            progress = {
                "phase": inputs["phase"],
                "model": cell["model"],
                "information": cell["information"],
                "terminal": done,
                "total": len(inputs["cells"]),
                "sessions_per_min": round(rate * 60, 3),
                "eta_s": round((len(inputs["cells"]) - done) / rate) if rate else None,
            }
            print(json.dumps(progress), flush=True)
            result = run_session(
                cell,
                inputs["protocol"],
                inputs["phase"],
                root / "sessions" / f"{index + 1:03d}",
                deadline,
                progress,
                prompt_factory=prompt,
            )
            done += 1
            print(
                json.dumps(
                    {
                        "terminal": done,
                        "total": len(inputs["cells"]),
                        "status": result["status"],
                        "failure": result.get("failure"),
                        "elapsed_s": round(result["elapsed_s"], 1),
                    }
                ),
                flush=True,
            )
            analyze(root)
            if result.get("failure", "").startswith(("platform_", "forbidden_")):
                print("platform/boundary stop; preserve remaining units", flush=True)
                break
    finally:
        (root / "executor.lock").unlink()
        analyze(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "freeze", "run", "analyze", "resume-frozen"))
    parser.add_argument("--phase", choices=("development", "formal"), default="development")
    parser.add_argument("--model", choices=("gpt", "deepseek"), default="gpt")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--export", type=Path)
    parser.add_argument("--without-block-deadline", action="store_true")
    parser.add_argument("--workers", type=int, choices=(1, 2, 3), default=1)
    args = parser.parse_args()
    if args.without_block_deadline and args.action != "resume-frozen":
        parser.error("--without-block-deadline applies only to an explicitly amended frozen resume")
    if args.workers > 1 and (args.action != "resume-frozen" or not args.without_block_deadline):
        parser.error("parallel workers require resume-frozen --without-block-deadline")
    root = args.root.resolve()
    if args.action == "prepare":
        prepare(root, args.phase, args.model)
    elif args.action == "freeze":
        freeze(root)
    elif args.action == "run":
        run(root)
    elif args.action == "resume-frozen":
        resume_frozen(
            root,
            args.export,
            without_block_deadline=args.without_block_deadline,
            workers=args.workers,
        )
    else:
        analyze(root, args.export)


if __name__ == "__main__":
    main()
