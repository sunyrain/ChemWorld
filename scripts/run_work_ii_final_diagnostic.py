#!/usr/bin/env python
"""Execute the fixed, sequential Work II minimal-submission B3 diagnostic."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from contextlib import ExitStack
from copy import deepcopy
from pathlib import Path
from typing import Any

from scripts.run_work_ii_study_b import (
    _EventState,
    _initial_command,
    _parse_payload,
    _prepare_codex_home,
    _resume_command,
)

from chemworld.eval.work_ii_final_diagnostic import (
    ARMS,
    prompt,
    schedule,
    schema,
    summarize,
    validate,
)
from chemworld.eval.work_ii_reviewer_followup import _public_query

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "configs/benchmark/work_ii_final_diagnostic_20260905.json"
SURFACE = (
    "scripts/run_work_ii_final_diagnostic.py",
    "scripts/run_work_ii_study_b.py",
    "src/chemworld/agents/diagnostic_numerics.py",
    "src/chemworld/eval/work_ii_final_diagnostic.py",
    "src/chemworld/eval/work_ii_reviewer_followup.py",
    "configs/benchmark/work_ii_final_diagnostic_20260905.json",
    "configs/providers/deepseek_v4_flash_models.json",
    "uv.lock",
)


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def science_inputs(protocol: dict, development: bool) -> tuple[list[dict], dict]:
    source = ROOT / protocol["source_root"]
    manifest = read(source / "input_manifest.json")
    current = read(ROOT / "configs/current.json")["work_ii"]
    binding = current["w2_63_b3_cross_model"]
    previous = read(ROOT / binding["report"])
    historical_report_digest = digest(ROOT / binding["report"])
    old_worlds = {r["cluster_id"] for r in previous["cell_rows_by_model"]["codex"]}
    if {c["cluster_id"] for c in manifest["cells"]} != old_worlds or len(old_worlds) != 5:
        raise ValueError("original B3 world coverage mismatch")
    source_files = [source / "input_manifest.json", source / "frozen_roster.json"]
    cells = manifest["cells"]
    if development:
        roster = read(source / "frozen_roster.json")
        truth = {}
        for family in ("linear", "power"):
            path = source / (
                "truth/development-candidate-grid/"
                + family
                + "/A_S_B3--partition-discovery--seed0/report.json"
            )
            source_files.append(path)
            truth[family] = read(path)["truth"]
        cells = []
        for arm in ARMS:
            cell = deepcopy(next(c for c in manifest["cells"] if c["arm"] == arm))
            cell.update(cluster_id="A_S_B3--partition-discovery--seed0", world_seed=0)
            packet = cell["public_packet"]
            packet["evidence"] = []
            for query in roster["evidence_queries"]:
                item = _public_query(query)
                item["reference_linear_observations"] = truth["linear"][query["query_id"]]
                item["target_observations"] = truth["power"][query["query_id"]]
                packet["evidence"].append(item)
            packet["scoring_action_queries"] = [_public_query(q) for q in roster["scoring_queries"]]
            cell["scoring_truth"] = {
                q["query_id"]: truth["power"][q["query_id"]] for q in roster["scoring_queries"]
            }
            cell["evidence_incumbent_score"] = max(
                e["target_observations"]["score"] for e in packet["evidence"]
            )
            best = max(t["score"] for t in cell["scoring_truth"].values())
            cell["action_opportunity_eligible"] = best - cell["evidence_incumbent_score"] >= 0.02
            cells.append(cell)
    # Strip stale derived fields from the historical manifest; the scorer recomputes actions.
    keep = (
        "cluster_id",
        "arm",
        "initial_world_model",
        "public_packet",
        "scoring_truth",
        "evidence_incumbent_score",
        "action_opportunity_eligible",
        "action_opportunity_threshold",
    )
    selected = [{k: c[k] for k in keep} for c in cells]
    units = schedule(selected, development=development)
    expected = 12 if development else 120
    if len(units) != expected or len({c["cell_id"] for c in units}) != expected:
        raise ValueError("fixed design coverage mismatch")
    return units, {
        "current_b3_report": binding,
        "historical_report_actual_sha256": historical_report_digest,
        "historical_registry_digest_matches": historical_report_digest == binding["report_sha256"],
        "reused_files": {p.relative_to(ROOT).as_posix(): digest(p) for p in source_files},
    }


def prepare(root: Path, phase: str) -> None:
    if root.exists():
        raise FileExistsError(
            "output already exists; use run/analyze to resume without replacement"
        )
    protocol = read(PROTOCOL)
    cells, source = science_inputs(protocol, phase == "development")
    if protocol[phase] is None:
        raise ValueError("formal budgets must be calibrated and fixed before preparation")
    write(
        root / "inputs.json",
        {"phase": phase, "protocol": protocol, "cells": cells, "source": source},
    )
    print(f"prepared {phase}: {len(cells)} sessions, {len(cells) * 2} scheduled turns", flush=True)


def surface() -> dict:
    return {name: digest(ROOT / name) for name in SURFACE}


def freeze(root: Path) -> None:
    inputs = read(root / "inputs.json")
    if inputs["phase"] != "formal" or (root / "sessions").exists():
        raise ValueError("freeze requires an unstarted formal block")
    if (root / "freeze.json").exists():
        raise FileExistsError("this block is already frozen")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).strip():
        raise ValueError("one clean source commit is required at formal freeze")
    write(
        root / "freeze.json",
        {
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "execution_surface": surface(),
            "inputs_sha256": digest(root / "inputs.json"),
            "cli_version": subprocess.check_output(
                [str(shutil.which("codex")), "--version"], text=True
            ).strip(),
        },
    )
    print("formal execution surface frozen once", flush=True)


def build_command(
    provider: dict,
    schema_path: Path,
    workspace: Path,
    *,
    audit: Path | None = None,
    thread_id: str | None = None,
    provider_retries: int | None = None,
) -> list[str]:
    command = _initial_command(provider, schema_path, workspace)
    disabled = (
        "shell_tool",
        "browser_use",
        "computer_use",
        "in_app_browser",
        "goals",
        "image_generation",
        "skill_search",
        "hooks",
        "code_mode",
        "code_mode_host",
    )
    index = command.index("--sandbox")
    command[index:index] = [arg for feature in disabled for arg in ("--disable", feature)]
    if provider_retries is not None:
        for key in ("request_max_retries", "stream_max_retries"):
            command.extend(["-c", f"model_providers.{provider['id']}.{key}={provider_retries}"])
    if audit is not None:
        server = workspace.parent / "public_numerics.py"
        shutil.copyfile(ROOT / "src/chemworld/agents/diagnostic_numerics.py", server)
        config = {
            "command": sys.executable,
            "args": [str(server), "--audit", str(audit), "--limit", "8"],
            "cwd": str(workspace),
            "required": True,
            "enabled": True,
            "supports_parallel_tool_calls": False,
            "enabled_tools": ["calculate"],
            "default_tools_approval_mode": "approve",
            "startup_timeout_sec": 30,
            "tool_timeout_sec": 15,
        }
        for key, value in config.items():
            command.extend(["-c", f"mcp_servers.public_numerics.{key}={json.dumps(value)}"])
    return (
        _resume_command(command, thread_id=thread_id, schema_path=schema_path)
        if thread_id
        else [*command, "-"]
    )


def tool_allowed(item: dict, enabled: bool) -> bool:
    kind = item.get("type", "")
    if kind in {"agent_message", "reasoning", "todo_list", "error"}:
        return True
    return (
        enabled
        and kind == "mcp_tool_call"
        and item.get("server") == "public_numerics"
        and item.get("tool") == "calculate"
    )


def stop_process(process: subprocess.Popen) -> None:
    # Terminate only the process tree created by this turn, including its MCP child.
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            check=False,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    else:
        import signal

        os.killpg(process.pid, signal.SIGKILL)  # type: ignore[attr-defined]
    process.wait(timeout=15)


def launch(
    command: list[str],
    message: str,
    workspace: Path,
    environment: dict,
    output: Path,
    timeout: float,
    enabled: bool,
    audit: Path,
    progress: dict,
) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    (output / "prompt.txt").write_text(message, encoding="utf-8")
    started = time.monotonic()
    state = _EventState()
    forbidden = threading.Event()
    provider_failure_kinds: set[str] = set()
    options = (
        {"creationflags": subprocess.CREATE_NO_WINDOW}
        if os.name == "nt"
        else {"start_new_session": True}
    )
    process = subprocess.Popen(
        command,
        cwd=workspace,
        env=environment,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        text=True,
        **options,
    )

    def consume_stdout() -> None:
        assert process.stdout is not None
        with (output / "stdout.jsonl").open("w", encoding="utf-8") as handle:
            for line in process.stdout:
                handle.write(line)
                handle.flush()
                state.consume_stdout([line])
                try:
                    event = json.loads(line)
                    if event.get("type") in {"error", "turn.failed"}:
                        error = event.get("message") or event.get("error", {}).get("message", "")
                        for term in ("max_output_tokens", "context_length", "Reconnecting"):
                            if term in str(error):
                                provider_failure_kinds.add(term)
                    if event.get("type") in {"item.started", "item.completed"} and not tool_allowed(
                        event.get("item", {}), enabled
                    ):
                        forbidden.set()
                except (ValueError, AttributeError):
                    pass

    def consume_stderr() -> None:
        assert process.stderr is not None
        with (output / "stderr.txt").open("w", encoding="utf-8") as handle:
            for line in process.stderr:
                handle.write(line)
                handle.flush()

    threads = [threading.Thread(target=f, daemon=True) for f in (consume_stdout, consume_stderr)]
    for thread in threads:
        thread.start()
    failure = None
    try:
        assert process.stdin is not None
        process.stdin.write(message)
        process.stdin.close()
        last = started
        while process.poll() is None:
            elapsed = time.monotonic() - started
            attempts = len(audit.read_text(encoding="utf-8").splitlines()) if audit.exists() else 0
            if forbidden.is_set():
                failure = "forbidden_tool"
            elif attempts > 8:
                failure = "tool_budget_exceeded"
            elif elapsed >= timeout:
                failure = "turn_timeout"
            if failure:
                stop_process(process)
                break
            if time.monotonic() - last >= 30:
                snapshot = state.snapshot()
                print(
                    json.dumps(
                        {
                            **progress,
                            "turn_elapsed_s": round(elapsed),
                            "events": sum(snapshot["event_counts"].values()),
                            "tool_attempts": attempts,
                        }
                    ),
                    flush=True,
                )
                last = time.monotonic()
            time.sleep(0.2)
    except (KeyboardInterrupt, SystemExit):
        failure = "platform_interrupted"
    finally:
        if process.poll() is None:
            stop_process(process)
        for thread in threads:
            thread.join(timeout=15)
    receipt = state.snapshot()
    receipt["provider_failure_kinds"] = sorted(provider_failure_kinds)
    receipt["payload"] = _parse_payload(receipt.pop("final_message"))
    if forbidden.is_set():
        failure = "forbidden_tool"
    receipt.update(
        exit_code=process.returncode,
        elapsed_s=time.monotonic() - started,
        failure=failure,
        stderr_byte_count=(output / "stderr.txt").stat().st_size,
        stderr_sha256=digest(output / "stderr.txt"),
    )
    if not failure and (process.returncode or receipt["provider_errors"]):
        receipt["failure"] = "provider_failure"
    write(output / "receipt.json", receipt)
    return receipt


def run_session(
    cell: dict,
    protocol: dict,
    phase: str,
    directory: Path,
    deadline: float,
    progress: dict,
    *,
    prompt_factory=prompt,
) -> dict:
    started = time.monotonic()
    result = {k: cell[k] for k in ("cell_id", "model", "tool")}
    result.update(status="failed", receipts=[])
    write(directory / "attempt.json", {**result, "started_epoch": time.time()})
    audit = directory / "tool_audit.jsonl"
    budgets = protocol[phase]
    try:
        with ExitStack() as stack:
            temporary = stack.enter_context(
                tempfile.TemporaryDirectory(prefix="chemworld-b3-minimal-")
            )
            temporary_root = Path(temporary)
            workspace = temporary_root / "workspace"
            workspace.mkdir()
            provider = deepcopy(protocol["providers"][cell["model"]])
            if provider.get("transport") == "standard_http_headers":
                from chemworld.providers.responses_header_transport import (
                    standard_headers_transport,
                )

                provider["base_url"] = stack.enter_context(
                    standard_headers_transport(
                        provider["base_url"],
                        directory / "transport.jsonl",
                        budgets["turn_timeout_s"],
                    )
                )
            environment = _prepare_codex_home(temporary_root, provider)
            thread_id = None
            for stage in ("pre", "post"):
                schema_path = temporary_root / (stage + "_schema.json")
                write(schema_path, schema(cell, stage))
                enabled = stage == "post" and cell["tool"] == "on"
                command = build_command(
                    provider,
                    schema_path,
                    workspace,
                    audit=audit if enabled else None,
                    thread_id=thread_id,
                    provider_retries=budgets.get("provider_retries"),
                )
                timeout = min(
                    budgets["turn_timeout_s"],
                    budgets["session_timeout_s"] - (time.monotonic() - started),
                    deadline - time.time(),
                )
                if timeout <= 0:
                    result["failure"] = "resource_budget_exhausted"
                    break
                receipt = launch(
                    command,
                    prompt_factory(cell, stage, cell["tool"]),
                    workspace,
                    environment,
                    directory / stage,
                    timeout,
                    enabled,
                    audit,
                    {**progress, "stage": stage},
                )
                result["receipts"].append({"stage": stage, **receipt})
                write(directory / "partial.json", result)
                if receipt["failure"]:
                    result["failure"] = receipt["failure"]
                    break
                if (
                    provider.get("reasoning_effort") == "none"
                    and receipt["usage"].get("reasoning_output_tokens") != 0
                ):
                    result["failure"] = "platform_reasoning_not_disabled"
                    break
                try:
                    validate(receipt["payload"], cell, stage)
                except ValueError:
                    result["failure"] = "participant_schema_" + stage
                    break
                result[stage] = receipt["payload"]
                if thread_id and receipt["thread_id"] != thread_id:
                    result["failure"] = "platform_thread_changed"
                    break
                thread_id = receipt["thread_id"] or thread_id
                if not thread_id:
                    result["failure"] = "platform_missing_thread"
                    break
            else:
                result["status"] = "completed"
    except Exception as error:
        result.update(failure="platform_exception", error_type=type(error).__name__)
    result["elapsed_s"] = time.monotonic() - started
    result["tool_audit"] = (
        [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
        if audit.exists()
        else []
    )
    if len(result["tool_audit"]) > 8:
        result.update(status="failed", failure="tool_budget_exceeded")
    write(directory / "result.json", result)
    return result


def collect(root: Path, cells: list[dict]) -> list[dict]:
    results = []
    for index, cell in enumerate(cells):
        directory = root / "sessions" / f"{index + 1:03d}"
        if (directory / "result.json").exists():
            results.append(read(directory / "result.json"))
        elif (directory / "attempt.json").exists():
            partial = (
                read(directory / "partial.json") if (directory / "partial.json").exists() else {}
            )
            partial.update({k: cell[k] for k in ("cell_id", "model", "tool")})
            partial.update(status="failed", failure="interrupted_attempt_not_reissued")
            receipts = []
            for stage in ("pre", "post"):
                path = directory / stage / "receipt.json"
                if path.exists():
                    receipts.append({"stage": stage, **read(path)})
                elif (directory / stage).exists():
                    state = _EventState()
                    raw = directory / stage / "stdout.jsonl"
                    if raw.exists():
                        state.consume_stdout(raw.read_text(encoding="utf-8").splitlines())
                    receipt = state.snapshot()
                    receipt.pop("final_message")
                    receipts.append(
                        {
                            "stage": stage,
                            **receipt,
                            "elapsed_s": 0,
                            "elapsed_unavailable": True,
                            "failure": "interrupted_attempt_not_reissued",
                        }
                    )
            partial["receipts"] = receipts
            audit = directory / "tool_audit.jsonl"
            partial["tool_audit"] = (
                [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
                if audit.exists()
                else []
            )
            partial["elapsed_s"] = sum(r["elapsed_s"] for r in receipts)
            results.append(partial)
    return results


def analyze(root: Path, export: Path | None = None) -> dict:
    inputs = read(root / "inputs.json")
    results = collect(root, inputs["cells"])
    report = summarize(results, inputs["cells"], formal=inputs["phase"] == "formal")
    report.update(
        phase=inputs["phase"],
        source=inputs["source"],
        providers=inputs["protocol"]["providers"],
        budgets=inputs["protocol"][inputs["phase"]],
    )
    report["execution_complete"] = len(results) == len(inputs["cells"])
    report["status"] = "terminal" if report["execution_complete"] else "incomplete"
    report["resource_accounting"] = (
        "Token totals are reported CLI usage. Missing usage or interrupted/recovered requests "
        "may leave unreported consumption; these totals are lower bounds in affected groups."
    )
    if (root / "freeze.json").exists():
        report["freeze"] = read(root / "freeze.json")
    write(root / "summary.json", report)
    lines = [
        "# Work II final B3 diagnostic",
        "",
        f"Phase: {inputs['phase']}. "
        f"Status: {report['status']}. Scheduled: {report['scheduled']}; "
        f"counts: {json.dumps(report['counts'])}.",
        "",
        "| Model | Tool | Complete / scheduled | Joint recovery | Mean regret | Top-1 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in report["by_model_tool"]:
        lines.append(
            f"| {row['model']} | {row['tool']} | {row['completed']}/{row['scheduled']} | "
            f"{row['joint_recovery']}/{row['scheduled']} | {row['mean_regret']:.5f} | "
            f"{row['top1']}/{row['scheduled']} |"
        )
    primary = report["primary"]
    lines.extend(
        [
            "",
            f"Tool-on minus off joint recovery: {primary['mean']:+.5f}; "
            "approximate world-bootstrap 95% interval: "
            f"{primary['approximate_world_bootstrap_95']}.",
            "",
            f"{report['worlds']} reused world(s); no additional independent worlds or physics. "
            "Only two selected model configurations. Aligned priors already contain the correct "
            "exponent: retention is distinct from discovery. Minimal-schema history comparisons "
            "do not identify a randomized schema effect. Public numerics is a system intervention; "
            "the old privileged simulator qualification does not prove "
            "public-only identifiability.",
            "",
            "## Resources",
            "",
            report["resource_accounting"],
            "",
            "```json",
            json.dumps(report["resources"], indent=2),
            "```",
            "",
            "## All failures / unstarted units",
            "",
            *[f"- {r['cell_id']}: {r['status']} / {r['failure']}" for r in report["failures"]],
        ]
    )
    content = "\n".join(lines) + "\n"
    (root / "summary.md").write_text(content, encoding="utf-8", newline="\n")
    if export is not None:
        write(export.with_suffix(".json"), report)
        export.with_suffix(".md").write_text(content, encoding="utf-8", newline="\n")
    return report


def run(root: Path) -> None:
    inputs = read(root / "inputs.json")
    if inputs["phase"] == "formal":
        frozen = read(root / "freeze.json")
        if frozen["execution_surface"] != surface() or frozen["inputs_sha256"] != digest(
            root / "inputs.json"
        ):
            raise ValueError("frozen execution surface or inputs drift")
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
    started = time.monotonic()
    done = len(existing)
    with (root / "executor.lock").open("x", encoding="utf-8") as lock:
        lock.write(str(os.getpid()))
    try:
        for index, cell in enumerate(inputs["cells"]):
            if cell["cell_id"] in terminal:
                continue
            if time.time() >= deadline:
                print("block deadline reached; retaining unstarted denominator", flush=True)
                break
            rate = (done - len(existing)) / max(time.monotonic() - started, 1)
            progress = {
                "phase": inputs["phase"],
                "completed_terminal": done,
                "total": len(inputs["cells"]),
                "model": cell["model"],
                "tool": cell["tool"],
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
                print("platform/boundary stop; subsequent units remain unstarted", flush=True)
                break
    finally:
        (root / "executor.lock").unlink()
        analyze(root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "freeze", "run", "analyze"))
    parser.add_argument("--phase", choices=("development", "formal"), default="development")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--export", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_relative_to(ROOT / "runs"):
        raise ValueError("raw experiment output must remain in ignored runs/")
    if args.action == "prepare":
        prepare(root, args.phase)
    elif args.action == "freeze":
        freeze(root)
    elif args.action == "run":
        run(root)
    else:
        report = analyze(root, args.export)
        print(
            json.dumps({k: report[k] for k in ("status", "scheduled", "counts", "primary")}),
            flush=True,
        )


if __name__ == "__main__":
    main()
