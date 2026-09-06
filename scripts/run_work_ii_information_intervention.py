"""Sequential GPT-first information intervention using the existing direct harness."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
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
    parser.add_argument("action", choices=("prepare", "freeze", "run", "analyze"))
    parser.add_argument("--phase", choices=("development", "formal"), default="development")
    parser.add_argument("--model", choices=("gpt", "deepseek"), default="gpt")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--export", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.action == "prepare":
        prepare(root, args.phase, args.model)
    elif args.action == "freeze":
        freeze(root)
    elif args.action == "run":
        run(root)
    else:
        analyze(root, args.export)


if __name__ == "__main__":
    main()
