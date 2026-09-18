"""Ask the sealed posttests once for a terminated, resource-incomplete EC source."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_ec_dual_goal_trial import PROVIDER, evaluate_predictions, posttest
from scripts.run_work_ii_study_b import _prepare_codex_home


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--cell", required=True)
    args = parser.parse_args()
    root = args.sources.resolve()
    design = read(root / "design.json")
    summary = read(root / "summary.json")
    if len(summary["results"]) != 18:
        raise RuntimeError("finish the single-executor source queue before posttest completion")
    original = next(c for c in summary["results"] if c["cell_id"] == args.cell)
    if original["posttests"] or not original.get("recommendation"):
        raise RuntimeError("requires sealed recommendation and no previously delivered posttests")
    source = root / args.cell
    output = source / "posttest-completion"
    output.mkdir(exist_ok=False)
    receipts = read(source / "source-receipts.json")
    thread_id = receipts[-1]["thread_id"]
    write(output / "attempt.json", {"started_epoch": time.time(), "source_thread": thread_id})
    result = {
        "cell_id": args.cell,
        "original_source_status": original["source_status"],
        "original_chain_status": original["status"],
        "procedure_amendment": "posttests after resource-incomplete source; no source rerun",
        "new_physical_experiments": 0,
        "posttests": {},
        "failure": None,
    }
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="chemworld-ec-followup-") as temporary:
        home_root = Path(temporary)
        environment = _prepare_codex_home(home_root, PROVIDER)
        shutil.copytree(source / "provider-rollouts", home_root / "codex-home" / "sessions")
        agent = SimpleNamespace(home_root=home_root, followup_environment=environment)
        for index, stage in enumerate(("K1", "Q", "K2")):
            print(f"posttest completion {index}/3; {args.cell} {stage}", flush=True)
            turn = posttest(
                agent, output, stage, thread_id,
                {"stage": args.cell, "completed": index, "total": 3},
                design=design,
            )
            result["posttests"][stage] = turn
            if turn.get("failure") or turn.get("thread_id") != thread_id:
                result["failure"] = turn.get("failure") or "source thread changed"
                break
        shutil.copytree(home_root / "codex-home" / "sessions", output / "provider-rollouts")
    result["prediction_evaluation"] = evaluate_predictions(
        result["posttests"].get("Q", {}).get("payload"), read(root / "truth.json"),
        query_set=design["queries"],
    )
    result["elapsed_s"] = time.monotonic() - started
    result["status"] = (
        "completed"
        if not result["failure"] and len(result["posttests"]) == 3
        and result["prediction_evaluation"]["valid"]
        else "failed"
    )
    write(output / "result.json", result)
    print(f"posttest completion finished: {result['status']}", flush=True)


if __name__ == "__main__":
    main()
