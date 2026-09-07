"""One additional attempt for the eight terminal information-block failures.

This post-hoc sensitivity block never changes the original formal evidence.
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from collections import Counter
from pathlib import Path

from scripts.run_work_ii_final_diagnostic import collect, digest, read, write

from chemworld.eval.work_ii_information_intervention import score, summarize

ROOT = Path(__file__).resolve().parents[1]


def select_failures(inputs: dict, report: dict) -> tuple[list[dict], list[dict]]:
    if report["status"] != "terminal" or len(report["rows"]) != len(inputs["cells"]):
        raise ValueError("selection requires the complete original terminal block")
    by_id = {r["cell_id"]: r for r in report["rows"]}
    if len(by_id) != len(report["rows"]):
        raise ValueError("duplicate original outcomes")
    cells, selection = [], []
    for index, cell in enumerate(inputs["cells"], 1):
        row = by_id[cell["cell_id"]]
        if row["status"] == "failed":
            cells.append(cell)
            selection.append(
                {
                    "cell_id": cell["cell_id"],
                    "original_session": index,
                    "original_failure": row["failure"],
                }
            )
        elif row["status"] != "completed":
            raise ValueError("unstarted units are outside the fixed retry selection")
    return cells, selection


def prepare(root: Path) -> None:
    if root.exists():
        raise FileExistsError("preserve existing retry attempts")
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_87_information_completeness"]
    source = ROOT / binding["deepseek_formal_run"]
    if (source / "executor.lock").exists():
        raise ValueError("original executor is active")
    report_path = ROOT / binding["deepseek_formal_report"]
    if digest(report_path) != binding["deepseek_formal_report_sha256"]:
        raise ValueError("original terminal report differs from binding")
    original, frozen = read(source / "inputs.json"), read(source / "freeze.json")
    if digest(source / "inputs.json") != frozen["inputs_sha256"]:
        raise ValueError("original inputs changed")
    cells, selection = select_failures(original, read(report_path))
    if len(cells) != 8:
        raise ValueError("this user-authorized block has exactly eight failed sessions")
    inputs = {
        **original,
        "cells": cells,
        "evidence_class": "posthoc_failure_retry",
        "original_root": str(source.relative_to(ROOT)).replace("\\", "/"),
        "original_report": binding["deepseek_formal_report"],
        "original_report_sha256": binding["deepseek_formal_report_sha256"],
        "original_inputs_sha256": frozen["inputs_sha256"],
        "selection": selection,
        "max_additional_attempts_per_cell": 1,
    }
    write(root / "inputs.json", inputs)
    write(
        root / "freeze.json",
        {
            **frozen,
            "inputs_sha256": digest(root / "inputs.json"),
            "evidence_class": "posthoc_failure_retry",
        },
    )
    write(
        root / "parallel_schedule.json",
        {
            "requested_workers": 3,
            "status": "prepared",
            "requested_epoch": time.time(),
            "reason": "user_authorized_one_retry_of_all_eight_failures",
            "block_deadline": None,
            "provider_retries": 0,
        },
    )
    print(
        "Prepared 8 additional sessions / 16 turns; original formal results retained.", flush=True
    )


def analyze(root: Path, export: Path | None = None) -> dict:
    if (root / "executor.lock").exists():
        raise ValueError("do not collect active attempts")
    inputs = read(root / "inputs.json")
    source = ROOT / inputs["original_root"]
    original_path = ROOT / inputs["original_report"]
    if (
        digest(original_path) != inputs["original_report_sha256"]
        or digest(source / "inputs.json") != inputs["original_inputs_sha256"]
    ):
        raise ValueError("original evidence changed")
    original = read(original_path)
    cells = read(source / "inputs.json")["cells"]
    results = collect(root, inputs["cells"])
    by_id = {r["cell_id"]: r for r in results}
    rows = [score(by_id.get(c["cell_id"], {"status": "unstarted"}), c) for c in inputs["cells"]]
    original_results = {r["cell_id"]: r for r in collect(source, cells)}
    # This virtual merge is a separately labelled sensitivity calculation only.
    alternative = summarize(list((original_results | by_id).values()), cells, formal=False)
    resources = summarize(results, cells, formal=False)["resources"]
    resources["scheduled_turns"] = 2 * len(inputs["cells"])
    report = {
        "schema_version": "work-ii-information-failure-retry-1",
        "formal_result": False,
        "evidence_class": "posthoc_failure_retry",
        "status": "terminal" if len(results) == len(inputs["cells"]) else "incomplete",
        "scheduled": len(inputs["cells"]),
        "counts": dict(Counter(r["status"] for r in rows)),
        "source": {"report": inputs["original_report"], "sha256": inputs["original_report_sha256"]},
        "selection": inputs["selection"],
        "rows": rows,
        "failures": [r for r in rows if r["status"] != "completed"],
        "resources": resources,
        "original_primary": original["primary"],
        "original_counts": original["counts"],
        "one_retry_sensitivity": {
            "scheduled": len(cells),
            "counts": alternative["counts"],
            "groups": alternative["groups"],
            "rows": alternative["rows"],
            "recovery_difference": alternative["primary"]["mean"],
        },
        "provider": inputs["protocol"]["providers"][inputs["model"]],
        "effective_budgets": {**inputs["protocol"][inputs["phase"]], "block_timeout_s": None},
        "execution_surface": read(root / "freeze.json"),
        "schedule": read(root / "parallel_schedule.json"),
        "interpretation": "All eight failed/interrupted original sessions were selected after "
        "their outcomes were known and received at most one fresh full-session attempt. "
        "This is a selected-failure reliability sensitivity check, not independent replication. "
        "The original 120-session primary, all failures and original resources remain unchanged. "
        "The virtual one-retry sensitivity is descriptive; it is not a replacement primary. "
        "No extra retry is triggered by another failure or an unfavorable scientific answer.",
    }
    lines = [
        "# Information intervention: one retry of eight failures",
        "",
        report["interpretation"],
        "",
        f"Status: {report['status']}; {report['counts']}; "
        f"{report['scheduled']} scheduled additional sessions.",
        "",
        "| Original session | Original failure | Retry status | Recovery / retention | Top-1 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for selected, row in zip(inputs["selection"], rows, strict=True):
        lines.append(
            f"| {selected['original_session']} | {selected['original_failure']} | "
            f"{row['status']} / {row['failure']} | {row['joint_recovery']} | {row['top1']} |"
        )
    lines += [
        "",
        "Descriptive one-retry sensitivity (original denominator retained):",
        "",
        "| Information | Population | Recovery / scheduled | Mean normalized regret |",
        "| --- | --- | --- | --- |",
    ]
    for group in alternative["groups"]:
        lines.append(
            f"| {group['information']} | {group['analysis']} | "
            f"{group['joint_recovery']}/{group['scheduled']} | "
            f"{group['mean_normalized_regret_failure_aware']:.6f} |"
        )
    lines += [
        "",
        "Additional resources (missing usage is a lower bound):",
        "```json",
        json.dumps(resources, indent=2),
        "```",
        "",
    ]
    text = "\n".join(lines)
    write(root / "summary.json", report)
    (root / "summary.md").write_text(text, encoding="utf-8", newline="\n")
    if export:
        if export.exists() or export.with_suffix(".md").exists():
            raise FileExistsError("preserve exported sensitivity report")
        write(export, report)
        export.with_suffix(".md").write_text(text, encoding="utf-8", newline="\n")
    return report


def run(root: Path, export: Path | None) -> None:
    inputs, frozen = read(root / "inputs.json"), read(root / "freeze.json")
    if (root / "executor.lock").exists() or (
        ROOT / inputs["original_root"] / "executor.lock"
    ).exists():
        raise ValueError("an executor is already active")
    if (root / "sessions").exists():
        raise FileExistsError("one launch only; preserve every attempted or unstarted retry")
    if digest(ROOT / "uv.lock") != frozen["execution_surface"]["uv.lock"]:
        raise ValueError("original locked environment required")
    archive = subprocess.check_output(
        ["git", "archive", frozen["source_commit"], "scripts", "src", "configs", "uv.lock"],
        cwd=ROOT,
    )
    with tempfile.TemporaryDirectory(prefix="chemworld-information-retry-") as directory:
        snapshot = Path(directory)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(snapshot, filter="data")
        for name, expected in frozen["execution_surface"].items():
            if digest(snapshot / name) != expected:
                raise ValueError(f"original runtime differs: {name}")
        provider = inputs["protocol"]["providers"][inputs["model"]]
        credential = Path(provider["api_key_file"])
        if not credential.is_absolute():
            destination = snapshot / credential
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / credential, destination)
        bootstrap = """import sys, runpy
from pathlib import Path
sys.path[:0] = [sys.argv[1], str(Path(sys.argv[1]) / 'src')]
from scripts import run_work_ii_information_intervention as runner
runpy.run_path(sys.argv[3])['run_parallel'](Path(sys.argv[2]), runner, 3)
"""
        result = subprocess.run(
            [
                sys.executable,
                "-u",
                "-c",
                bootstrap,
                str(snapshot),
                str(root),
                str(ROOT / "scripts/run_work_ii_information_parallel.py"),
            ],
            cwd=ROOT,
            check=False,
        )
    report = analyze(root, export)
    print(
        json.dumps({"stage": "finished", "status": report["status"], "counts": report["counts"]}),
        flush=True,
    )
    if result.returncode:
        raise RuntimeError(f"executor exited {result.returncode}; preserve all attempts")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run", "analyze"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--export", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action == "prepare":
        prepare(root)
    elif args.action == "run":
        run(root, args.export)
    else:
        report = analyze(root, args.export)
        print(json.dumps({"status": report["status"], "counts": report["counts"]}))


if __name__ == "__main__":
    main()
