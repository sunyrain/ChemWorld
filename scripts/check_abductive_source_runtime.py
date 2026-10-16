"""Four concurrent prescribed-action checks of the actual source/MCP boundary.

This development-only canary is not part of scientific participant evidence.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

# Import the worker before libraries that initialize native thread pools.
from scripts import run_abductive_discrimination as run
from scripts.report_paper_case_notebooks import notebook_record

RECIPE = [
    {"operation": "add_solvent", "solvent": 0, "volume_L": 0.02},
    {"operation": "add_reagent", "amount_mol": 0.001},
    {"operation": "terminate"},
    {"operation": "measure", "instrument": "final_assay"},
]
INSTRUCTIONS = """This is a technical runtime check, not a scientific investigation.
Use only the laboratory and research-notebook tools. First write one brief notebook note
stating that this is a runtime canary and no scientific inference will be made.
Execute exactly two identical batches, each in this order:
add_solvent solvent=0 volume_L=0.02; add_reagent amount_mol=0.001; terminate;
measure instrument=final_assay. Use next_state between physical actions as required by
the laboratory protocol. After both batches, commit_final_recommendation selecting completed
batch 1 with a technical rationale, then return the required brief status/summary JSON.
Do not explore, infer a mechanism, change the recipe or add physical operations.
The task-card scientific objective is suspended for this fixed runtime check.
"""
ENV_WRAPPER = """import json, os, runpy, sys
from pathlib import Path
target = Path(sys.argv[1])
keys = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS", "TOKIO_WORKER_THREADS", "RAYON_NUM_THREADS")
target.write_text(json.dumps({k: os.environ.get(k) for k in keys}), encoding="utf-8")
args = sys.argv[2:]
if args[0] == "-m":
    module = args[1]
    sys.argv = [module, *args[2:]]
    runpy.run_module(module, run_name="__main__")
else:
    script = Path(args[0]).resolve()
    sys.argv = [str(script), *args[1:]]
    sys.path[0] = str(script.parent)
    runpy.run_path(str(script), run_name="__main__")
"""


class CanaryAgent(run.BoundedResearchAgent):
    def _command(self, *, instructions_path, schema_path):
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        instructions_path.write_text(INSTRUCTIONS, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(INSTRUCTIONS, encoding="utf-8")
        wrapper = self.output / "mcp-environment-probe.py"
        wrapper.write_text(ENV_WRAPPER, encoding="utf-8")
        for server in ("chemworld_lab", "research_notebook", "public_numerics"):
            prefix = f"mcp_servers.{server}.args="
            matching = [i for i, value in enumerate(command) if value.startswith(prefix)]
            if len(matching) != 1:
                raise ValueError(f"Expected exactly one MCP argument list: {server}")
            index = matching[0]
            arguments = json.loads(command[index].removeprefix(prefix))
            report = self.output / f"{server}-environment.json"
            command[index] = prefix + json.dumps([str(wrapper), str(report), *arguments])
        return command


def unit(root, number):
    folder = root / f"unit-{number}"
    folder.mkdir(parents=True, exist_ok=False)
    output = folder / "private-provider/source"
    output.mkdir(parents=True)
    config = run.build_config()
    run.configure(config)
    world = config["worlds"][0]
    agent = CanaryAgent(
        goal="characterization",
        batches=2,
        home_root=folder / "private-provider/home",
        output=output,
        workspace=folder / "private-provider/laboratory",
        initial_world_model=None,
        request_timeout_s=300,
        finalization_timeout_s=180,
        session_wall_time_limit_s=600,
        max_recovered_mcp_tool_failures=0,
        max_consecutive_mcp_tool_failures=0,
        max_provider_error_events=0,
        pre_action_restart_limit=0,
        accepted_turn_continuation_limit=0,
        provider_process_attempt_limit=1,
        max_initial_prompt_bytes=262144,
        max_tool_output_bytes=131072,
        history_event_limit=360,
        history_byte_limit=524288,
    )
    started, failure = time.monotonic(), None
    progress = {"unit": number, "operations": 0, "assays": 0, "phase": "source"}
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            run.emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()

    def callback(record, trace):
        del trace
        progress["operations"] += 1
        if (
            record.info.get("instrument") == "final_assay"
            and record.info.get("transaction_status") == "committed"
        ):
            progress["assays"] += 1

    try:
        run.eq.physics(
            agent,
            folder / "trajectory.jsonl",
            config=config,
            world=world,
            batches=2,
            observation_seed=100 + number,
            observation_namespace=f"source-runtime-canary-{number}",
            callback=callback,
        )
    except Exception as exc:
        failure = {"type": type(exc).__name__, "message": str(exc)[:1600]}
    finally:
        agent.close()
    receipts = agent.provider_receipts()
    run.write(folder / "private-provider/source-receipts.json", receipts)
    records = (
        run.eq.load_jsonl(folder / "trajectory.jsonl")
        if (folder / "trajectory.jsonl").exists()
        else []
    )
    replay = (
        run.eq.verify_records(
            records, tolerance=0, world_interventions=world["world_interventions"]
        ).to_dict()
        if records
        else {"verified": False}
    )
    thread = receipts[-1].get("thread_id") if receipts else None
    followup = None
    if thread and not failure:
        progress["phase"] = "sealed_transport"
        run.inquiry.K1 = (
            'Return JSON with report exactly "source and notebook transport complete". '
            "No tools or scientific interpretation."
        )
        followup = run.posttest(
            agent, folder, folder / "private-provider", "K1", thread, progress, []
        )
    notes = notebook_record(folder)
    observed_env = {
        server: run.read(output / f"{server}-environment.json")
        if (output / f"{server}-environment.json").exists()
        else None
        for server in ("chemworld_lab", "research_notebook", "public_numerics")
    }
    actions_match = [r["action"] for r in records] == RECIPE * 2
    checks = {
        "source_no_failure": failure is None,
        "eight_prescribed_committed_operations": actions_match
        and len(records) == 8
        and all(r.get("transaction_status") == "committed" for r in records),
        "two_final_assays": len(run.eq.shared.summaries(records)) == 2,
        "source_exact_replay": replay["verified"],
        "notebook_write_retained": len(notes["versions"]) >= 1,
        "all_mcp_environment_limits_observed": all(
            v == run.WORKER_ENV for v in observed_env.values()
        ),
        "same_thread_sealed_continuation": bool(
            followup
            and not followup["failure"]
            and followup.get("payload", {}).get("report")
            == "source and notebook transport complete"
        ),
    }
    result = {
        "unit": number,
        "passed": all(checks.values()),
        "checks": checks,
        "failure": failure,
        "source_usage": agent.method_resource_usage(),
        "followup": followup,
        "observed_mcp_environment": observed_env,
        "notebook_versions": len(notes["versions"]),
        "exact_replay": replay,
        "operations": len(records),
        "elapsed_s": time.monotonic() - started,
        "scientific_participant_evidence": False,
    }
    run.write(folder / "result.json", result)
    stop.set()
    run.emit(result)
    return 0 if result["passed"] else 1


def coordinate(root):
    root.mkdir(parents=True, exist_ok=False)
    processes = []
    for number in range(1, 5):
        stream = (root / f"unit-{number}.log").open("x", encoding="utf-8")
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "scripts.check_abductive_source_runtime",
                "--root",
                str(root),
                "--unit",
                str(number),
            ],
            cwd=run.ROOT,
            stdout=stream,
            stderr=subprocess.STDOUT,
            env={**os.environ, **run.WORKER_ENV},
            **({"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}),
        )
        processes.append((number, process, stream))
    started = time.monotonic()
    while any(p.poll() is None for _, p, _ in processes):
        run.emit(
            {
                "stage": "real-source-mcp-canary",
                "terminal": sum(p.poll() is not None for _, p, _ in processes),
                "planned": 4,
                "elapsed_s": round(time.monotonic() - started),
                "log_bytes": sum((root / f"unit-{n}.log").stat().st_size for n, _, _ in processes),
            }
        )
        time.sleep(30)
    results = []
    for number, process, stream in processes:
        stream.close()
        path = root / f"unit-{number}/result.json"
        results.append(
            run.read(path)
            if path.exists()
            else {
                "unit": number,
                "passed": False,
                "worker_exit_code": process.returncode,
                "failure": "worker exited without result",
            }
        )
    summary = {
        "planned_units": 4,
        "terminal_units": 4,
        "planned_assays": 8,
        "passed_units": sum(r["passed"] for r in results),
        "passed": all(r["passed"] for r in results),
        "results": results,
        "scientific_participant_evidence": False,
    }
    run.write(root / "result.json", summary)
    run.emit({k: v for k, v in summary.items() if k != "results"})
    return 0 if summary["passed"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--unit", type=int)
    args = parser.parse_args()
    return unit(args.root, args.unit) if args.unit else coordinate(args.root)


if __name__ == "__main__":
    raise SystemExit(main())
