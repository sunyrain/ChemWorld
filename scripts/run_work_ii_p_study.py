"""P 12-batch study: isolated source workers, sealed posttests and bounded recovery."""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import shutil
import subprocess
import tempfile
import threading
import time
from collections import Counter
from contextlib import nullcontext
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from statistics import mean

import psutil
from scripts import run_work_ii_c_formal as host
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_p_gate as gate
from scripts.benchmark_runtime_views import verify_resources
from scripts.recover_work_ii_ec_pa_network import EXCLUDED, provider_errors
from scripts.resume_work_ii_c_completion import atomic_write
from scripts.resume_work_ii_c_completion import retryable_transport as known_transport_failure
from scripts.run_work_ii_final_diagnostic import read, write
from scripts.run_work_ii_pa_single_trial import token_accounting
from scripts.work_ii_p_inventory import inventory_v2, inventory_v3
from scripts.work_ii_p_public import presentation

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS
from chemworld.data.logging import load_jsonl
from chemworld.eval.experiment_1_p_assets import frozen_world_truths
from chemworld.eval.runner import run_agent
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent
from chemworld.runtime.full_process_contract import FULL_PROCESS_FREE_RESEARCH_CONTRACT
from chemworld.tasks import get_task

ROOT = Path(__file__).resolve().parents[1]
METRICS = ("purity", "recovery")
NAMESPACE = "p-gate-v1"
SOURCE_LIMITS = {
    "operation_limit": 720,
    "complete_experiment_limit": 12,
    "wall_time_limit_s": 3600,
    "model_call_limit": 1,
    "input_token_limit": 16000000,
    "uncached_input_token_limit": 4000000,
    "output_token_limit": 192000,
    "training_environment_step_limit": 0,
}
WORKER_ENV = {
    "OPENBLAS_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "TOKIO_WORKER_THREADS": "2",
    "RAYON_NUM_THREADS": "2",
}
ASSET = ROOT / "configs/benchmark/experiment_1_p_asset_authoring_v1.1.0.json"
GATE = ROOT / "workstreams/flagship_tasks/reports/work-ii-p-gate-20260921-v5/summary.json"
SOURCE_SYSTEM = (
    gate.SYSTEM
    + """
Use only the supplied laboratory and numerical tools; no filesystem, repository, external
network, shell or hidden simulator access. There is no mandatory experiment grouping or
per-batch reflection. You may change your plans after observations. Complete the declared
campaign and commit_final_recommendation with a completed 1-based batch index and rationale.
Then return concise required status/summary JSON; do not produce the later reports early.
The source has 128 calculator attempts, including invalid expressions. If exhausted, continue
from available evidence. Supplied reference information can be incomplete or inaccurate;
observations are authoritative. No particular scientific outcome is required.
"""
)


class StudyAgent(gate.PAgent):
    def _command(self, *, instructions_path, schema_path):
        command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
        for server in ("chemworld_lab", "public_numerics"):
            for key, value in WORKER_ENV.items():
                command += ["-c", f"mcp_servers.{server}.env.{key}={json.dumps(value)}"]
        instructions_path.write_text(SOURCE_SYSTEM, encoding="utf-8")
        (self.output / "source-instructions.txt").write_text(SOURCE_SYSTEM, encoding="utf-8")
        return command


def prediction_question(queries):
    return (
        "Your mechanism report is sealed. Predict the final-assay observations for each of "
        "these twelve new independent batches in your world. Give purity and recovery point "
        "estimates and 80% predictive intervals (estimate, lower80, upper80) in [0,1]. "
        "Purity is the target fraction among the specified solutes in the final selected "
        "material; recovery is target product relative to original reactant charge. These "
        "are not concentration or native score. Follow each full recipe including sampling "
        "and phase disposal; consider measurement variability and model uncertainty. "
        "Each recipe starts from a fresh vessel with the original campaign inventory envelope. "
        "Return one prediction for every query_id and an English rationale. No new laboratory "
        "experiments or changes to earlier answers are allowed.\n" + json.dumps(queries)
    )


def recipe_from_records(records, selected):
    if type(selected) is not int or selected < 1:
        raise ValueError("Recommendation must identify a completed batch")
    chosen = [r for r in records if r.get("experiment_index") == selected - 1]
    committed = [r for r in chosen if r.get("transaction_status") == "committed"]
    finals = [r for r in committed if r.get("instrument") == "final_assay"]
    if len(finals) != 1 or committed[-1] is not finals[0]:
        raise ValueError("Selected recipe lacks one final committed assay")
    rejected = [r for r in chosen if r.get("transaction_status") != "committed"]
    allowed = {"validation_failed", "rolled_back", "campaign_resource_rejected"}
    if any(r.get("transaction_status") not in allowed for r in rejected):
        raise ValueError("Unknown transaction status in selected recipe")
    return {
        "lifecycle_index": selected,
        "actions": [r["action"] for r in committed],
        "rejected_attempts": [
            {k: r.get(k) for k in ("step", "action", "transaction_status")} for r in rejected
        ],
    }


def physics(agent, folder, cell, design, progress, *, retest=False):
    world = design["worlds"][cell["world_id"]]
    dossier = gate.public_dossier(design["asset"], world, cell["arm"])
    diagnostics, audits, parameters, failure = [], [], {}, None
    card = gate.resources()
    if retest:
        card = replace(card, vessel_start_limit=1, final_assay_limit=1)

    def callback(record, trace):
        del trace
        progress["operations"] = progress.get("operations", 0) + 1
        if (
            record.info.get("transaction_status") == "committed"
            and record.info.get("instrument") == "final_assay"
        ):
            progress["batches"] = progress.get("batches", 0) + 1

    started = time.monotonic()
    correction = (
        inventory_v3()
        if design.get("inventory_contract") == "p-inventory-v3"
        else inventory_v2()
        if design.get("inventory_contract") == "p-inventory-v2"
        else nullcontext()
    )
    with correction, presentation(dossier, gate.GOAL, 1 if retest else 12):
        try:
            run_agent(
                env_id=get_task(gate.TASK).env_id,
                agent=agent,
                task_id=gate.TASK,
                world_split="public-test",
                objective="balanced",
                seed=world["world_seed"],
                world_interventions=world["world_interventions"],
                agent_seed=0,
                observation_seed=303 if retest else 0,
                budget=720,
                budget_override=720,
                episode_mode_override="campaign",
                campaign_resource_card=card,
                material_information={"mode": "opaque_codes"},
                full_process_contract_id=FULL_PROCESS_FREE_RESEARCH_CONTRACT,
                observation_noise_mode="keyed",
                observation_noise_namespace=NAMESPACE,
                output_path=folder / "trajectory.jsonl",
                step_callback=callback,
                env_wrapper=lambda env: gate.Capture(env, diagnostics, audits, parameters),
                method_resource_limits=SOURCE_LIMITS if isinstance(agent, StudyAgent) else None,
            )
        except Exception as exc:
            failure = {"type": type(exc).__name__, "message": str(exc), "stage": progress["phase"]}
        finally:
            if isinstance(agent, StudyAgent):
                agent.close()
        records = (
            load_jsonl(folder / "trajectory.jsonl")
            if (folder / "trajectory.jsonl").exists()
            else []
        )
        replay = ec.replay_with_progress(
            records, cell["id"], world_interventions=world["world_interventions"]
        )
    resources = None
    if records:
        try:
            resources = verify_resources(records)
        except Exception as exc:
            failure = failure or {
                "stage": "resource_evaluation",
                "type": type(exc).__name__,
                "message": str(exc),
            }
    result = {
        "batches": ec.summaries(records),
        "operations": len(records),
        "failure": failure,
        "exact_replay": replay,
        "resources": resources,
        "truth": [r["truth"] for r in diagnostics if r["instrument"] == "final_assay"],
        "inventory_audits": audits,
        "elapsed_s": time.monotonic() - started,
    }
    checks = {
        "execution": failure is None,
        "exact_replay": replay.get("verified") is True,
        "resource_ledger": bool(resources and resources.get("verified")),
        "batch_count": len(result["batches"]) == (1 if retest else 12),
        "inventory": all(r["passed"] for r in audits),
    }
    result["validation_checks"] = checks
    result["passed"] = all(checks.values())
    return result, records


def retryable_transport(path):
    errors = provider_errors(path)
    return known_transport_failure(path) or (
        any("unexpected status 503 Service Unavailable" in e for e in errors)
        and not any(EXCLUDED.search(e) for e in errors)
    )


def posttest(agent, folder, stage, thread_id, progress, design, *, first_attempt=1):
    # Every worker is a separate process. The common follow-up implementation is reused
    # with P's two numeric fields; laboratory access remains disabled by that implementation.
    original = ec.METRICS
    ec.METRICS = METRICS
    try:
        attempts = []
        for number in range(first_attempt, 7):
            result = ec.posttest(agent, folder, stage, thread_id, progress, design=design)
            if result.get("payload") or result.get("failure") != "provider_failure":
                break
            path = folder / stage / "stdout.jsonl"
            revoked = any("refresh token was revoked" in e.lower() for e in provider_errors(path))
            if revoked:
                current = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
                isolated = agent.home_root / "codex-home/auth.json"
                if not current.exists() or current.read_bytes() == isolated.read_bytes():
                    break
                shutil.copyfile(current, isolated)
            elif not retryable_transport(path):
                break
            if number == 6:
                break
            archive = folder / "posttest-interruptions" / stage / f"attempt-{number}"
            archive.parent.mkdir(parents=True, exist_ok=True)
            if not archive.resolve().is_relative_to(folder.resolve()):
                raise ValueError("Archive outside source folder")
            (folder / stage).rename(archive)
            attempts.append({"receipt": result, "path": str(archive)})
            progress.update(phase=f"{stage}:transport_backoff", retry=number)
            time.sleep(min(900, 60 * 2 ** (number - 1)))
            progress["phase"] = stage
        result["transport_recovery_attempts"] = attempts
        write(folder / stage / "receipt.json", result)
        return result
    finally:
        ec.METRICS = original


def source(folder, cell, design, progress):
    folder.mkdir(parents=True, exist_ok=False)
    home = Path(tempfile.mkdtemp(prefix="chemworld-p-research-"))
    write(folder / "runtime-location.json", {"home": str(home)})
    dossier = gate.public_dossier(design["asset"], design["worlds"][cell["world_id"]], cell["arm"])
    agent = StudyAgent(
        dossier=dossier,
        home_root=home,
        output=folder,
        workspace=home / "laboratory",
        role_id="free_research",
        request_timeout_s=1200,
        finalization_timeout_s=300,
        session_wall_time_limit_s=3600,
        max_recovered_mcp_tool_failures=12,
        max_consecutive_mcp_tool_failures=6,
        max_provider_error_events=0,
        pre_action_restart_limit=0,
        accepted_turn_continuation_limit=0,
        provider_process_attempt_limit=1,
        max_initial_prompt_bytes=262144,
        max_tool_output_bytes=131072,
        history_event_limit=720,
        history_byte_limit=2097152,
    )
    result = {**cell, "status": "running", "failure": None, "posttests": {}}
    atomic_write(folder / "result.json", result)
    progress.update(phase="source", batches=0, operations=0)
    result["source"], records = physics(agent, folder, cell, design, progress)
    result["source"]["usage"] = agent.method_resource_usage()
    receipts = agent.provider_receipts()
    write(folder / "source-receipts.json", receipts)
    shutil.copytree(agent.workspace.root, folder / "workspace")
    last = receipts[-1] if receipts else {}
    result["recommendation"] = last.get("final_recommendation")
    result["failure"] = result["source"]["failure"]
    atomic_write(folder / "result.json", result)
    # A broken source transport has no sealed terminal context: preserve it for an
    # independently accounted fresh attempt, without contaminating it with posttests.
    transport = result["failure"] and retryable_transport(folder / "source-stdout.jsonl")
    if not transport and ec.posttest_context_available(last):
        for stage in ("K1", "Q", "K2"):
            progress["phase"] = stage
            turn = posttest(agent, folder, stage, last["thread_id"], progress, design)
            result["posttests"][stage] = turn
            atomic_write(folder / "result.json", result)
            if turn.get("failure"):
                result["failure"] = result["failure"] or {
                    "stage": stage,
                    "message": turn["failure"],
                }
                break
    elif not result["failure"]:
        result["failure"] = {"stage": "handoff", "message": "No intact terminal source context"}
    if not transport:
        try:
            selected = (result.get("recommendation") or {}).get("selected_experiment_index")
            result["recommendation_recipe"] = recipe_from_records(records, selected)
            retest_folder = folder / "recommendation-retest"
            retest_folder.mkdir(exist_ok=False)
            progress["phase"] = "recommendation_retest"
            retest, _ = physics(
                _FrozenTruthReplayAgent(result["recommendation_recipe"]["actions"]),
                retest_folder,
                cell,
                design,
                {"phase": "recommendation_retest"},
                retest=True,
            )
            result["recommendation_retest"] = retest
            write(retest_folder / "result.json", retest)
        except Exception as exc:
            result["failure"] = result["failure"] or {
                "stage": "recommendation_retest",
                "type": type(exc).__name__,
                "message": str(exc),
            }
    result["status"] = (
        "completed"
        if (
            not result["failure"]
            and result["source"]["passed"]
            and len(result["posttests"]) == 3
            and all(t.get("payload") and not t.get("failure") for t in result["posttests"].values())
            and result.get("recommendation_retest", {}).get("passed")
        )
        else "failed"
    )
    result["tokens"] = token_accounting(result)
    result["source_transport_retry_eligible"] = bool(
        transport
        and not result["posttests"]
        and (not records or result["source"]["exact_replay"].get("verified"))
    )
    atomic_write(folder / "result.json", result)
    return result


def evaluate(payload, observations, queries):
    try:
        rows = payload["predictions"]
        expected = [q["query_id"] for q in queries]
        if sorted(r["query_id"] for r in rows) != sorted(expected):
            raise ValueError("Missing, repeated or unknown query IDs")
        by_id = {r["query_id"]: r for r in rows}
        truth = dict(zip(expected, observations, strict=True))
        metrics = {}
        for metric in METRICS:
            errors, coverage, widths, interval_scores = [], [], [], []
            for q in expected:
                p = by_id[q][metric]
                e, lo, hi = [p[k] for k in ("estimate", "lower80", "upper80")]
                if not all(type(v) in (float, int) and math.isfinite(v) for v in (e, lo, hi)):
                    raise ValueError("Nonfinite or nonnumeric prediction")
                if not 0 <= lo <= e <= hi <= 1:
                    raise ValueError("Invalid interval")
                target = truth[q][metric]
                errors.append(abs(e - target))
                coverage.append(lo <= target <= hi)
                widths.append(hi - lo)
                interval_scores.append(hi - lo + 10 * max(lo - target, target - hi, 0))
            metrics[metric] = {
                "n": 12,
                "mae": mean(errors),
                "coverage80": mean(coverage),
                "width80": mean(widths),
                "interval_score80": mean(interval_scores),
            }
        pairs = []
        for i in range(0, 12, 2):
            a, b = expected[i : i + 2]
            for metric in METRICS:
                delta = truth[b][metric] - truth[a][metric]
                predicted = by_id[b][metric]["estimate"] - by_id[a][metric]["estimate"]

                def sign(x):
                    small = abs(x) <= 0.02 or math.isclose(abs(x), 0.02, rel_tol=0, abs_tol=1e-12)
                    return 0 if small else 1 if x > 0 else -1

                pairs.append(
                    {
                        "factor": queries[i]["factor"],
                        "metric": metric,
                        "truth_delta": delta,
                        "predicted_delta": predicted,
                        "correct": sign(delta) == sign(predicted),
                        "resolved": sign(delta) != 0,
                    }
                )
        return {"valid": True, "metrics": metrics, "pairs": pairs}
    except (TypeError, KeyError, ValueError) as exc:
        return {"valid": False, "failure": str(exc)}


def prepare(root, report):
    root.mkdir(parents=True, exist_ok=False)
    report.mkdir(parents=True, exist_ok=True)
    asset, qualified = read(ASSET), read(GATE)
    if not qualified["passed"]:
        raise ValueError("P scientific gate did not pass")
    worlds = frozen_world_truths(asset)
    world_map = {w["world_id"]: w for w in worlds}
    schedule = [
        {"id": f"{w['world_id']}-B12-E-{arm}", "world_id": w["world_id"], "arm": arm, "budget": 12}
        for w in worlds
        for arm in gate.ARMS
    ]
    query_set = gate.queries("v3")
    references = {r["world_id"]: r for r in qualified["campaigns"] if r["arm"] == "Opaque"}
    assert set(references) == set(world_map) and len(schedule) == 15
    design = {
        "protocol": "p-12-parallel-development-v1-en",
        "inventory_contract": "p-inventory-v3",
        "note": "WORK_II_P_PARALLEL_STUDY_NOTE.md",
        "model": ec.PROVIDER,
        "asset": asset,
        "worlds": world_map,
        "schedule": schedule,
        "queries": query_set,
        "source_system": SOURCE_SYSTEM,
        "goal": gate.GOAL,
        "K1": ec.K1,
        "Q": prediction_question(query_set),
        "K2": ec.K2,
        "posttest_numerics": FOLLOWUP_NUMERICS.to_dict(),
        "max_workers": 6,
        "worker_environment": WORKER_ENV,
        "admission_stagger_s": 5,
        "reference_origin": str(GATE.relative_to(ROOT)),
        "historical_reference_batches_reused": 60,
        "resources": gate.resources().to_dict(),
        "source_method_resource_limits": SOURCE_LIMITS,
        "namespace": NAMESPACE,
    }
    write(root / "design.json", design)
    write(root / "reference-results.json", references)
    for path in (
        Path(__file__),
        ROOT / "scripts/work_ii_p_public.py",
        ROOT / "scripts/work_ii_p_inventory.py",
        ROOT / "scripts/run_work_ii_p_gate.py",
    ):
        destination = root / "executor-snapshot" / path.name
        destination.parent.mkdir(exist_ok=True)
        shutil.copyfile(path, destination)
    export(root, report)


def startup_failure(folder, result):
    """No accepted provider context and zero physical work: local startup only."""
    stdout = folder / "source-stdout.jsonl"
    stderr = folder / "source-stderr.txt"
    if (
        result.get("source", {}).get("operations", 0)
        or result.get("posttests")
        or not stdout.exists()
        or stdout.stat().st_size
        or not stderr.exists()
    ):
        return False
    text = stderr.read_text(encoding="utf-8", errors="replace")
    return "required MCP servers failed to initialize: chemworld_lab" in text or (
        "memory allocation of" in text and "bytes failed" in text
    )


def worker(root, cell_id):
    design = read(root / "design.json")
    pilot = cell_id == "pilot"
    cell = copy.deepcopy(
        design["schedule"][0]
        if pilot
        else next(c for c in design["schedule"] if c["id"] == cell_id)
    )
    if pilot:
        cell["id"] += "-pilot"
    parent = root / ("pilot" if pilot else "sources/" + cell_id)
    parent.mkdir(parents=True, exist_ok=True)
    status = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "cell": cell["id"],
        "phase": "starting",
        "started_epoch": time.time(),
    }
    stop = threading.Event()

    def emit():
        status["epoch"] = time.time()
        atomic_write(parent / "status.json", dict(status))
        print(json.dumps(status), flush=True)

    def heartbeat():
        while not stop.wait(30):
            emit()

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    emit()
    try:
        for attempt in range(1, 7):
            folder = parent / f"attempt-{attempt}"
            if folder.exists():
                previous = read(folder / "result.json")
                if previous["status"] == "completed" or not (
                    previous.get("source_transport_retry_eligible")
                    or startup_failure(folder, previous)
                ):
                    atomic_write(parent / "effective.json", {"path": str(folder / "result.json")})
                    return
                continue
            status["attempt"] = attempt
            result = source(folder, cell, design, status)
            atomic_write(parent / "effective.json", {"path": str(folder / "result.json")})
            if (
                not (
                    result.get("source_transport_retry_eligible") or startup_failure(folder, result)
                )
                or attempt == 6
            ):
                break
            status.update(phase="source:transport_backoff", retry=attempt)
            emit()
            time.sleep(min(900, 60 * 2 ** (attempt - 1)))
        status["phase"] = "terminal"
    except BaseException as exc:
        status.update(
            phase="worker_error", failure={"type": type(exc).__name__, "message": str(exc)}
        )
        raise
    finally:
        stop.set()
        thread.join(timeout=2)
        emit()


def effective(parent):
    path = parent / "effective.json"
    if path.exists():
        return read(Path(read(path)["path"]))
    candidates = sorted(parent.glob("attempt-*/result.json"))
    return read(candidates[-1]) if candidates else None


def batch_accounting(parent):
    pointer = Path(read(parent / "effective.json")["path"])
    result = read(pointer)
    original = (result.get("posttest_repair") or {}).get("original_result")
    source_folder = Path(original).parent if original else pointer.parent
    started, assayed, discarded = set(), set(), []
    for record in load_jsonl(source_folder / "trajectory.jsonl"):
        if record.get("transaction_status") != "committed":
            continue
        index = record["experiment_index"] + 1
        started.add(index)
        action = record["action"]
        if action.get("instrument") == "final_assay":
            assayed.add(index)
        if action.get("operation") == "discard_batch":
            discarded.append({"lifecycle_index": index, "reason": action.get("reason")})
    return {
        "started": len(started),
        "final_assayed": len(assayed),
        "discarded": len(discarded),
        "discarded_batches": discarded,
    }


def export(root, report):
    design = read(root / "design.json")
    references = read(root / "reference-results.json")
    results = []
    for cell in design["schedule"]:
        r = effective(root / "sources" / cell["id"])
        results.append(r or {**cell, "status": "not_started", "posttests": {}})
    summary = {
        "observed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "development_only": True,
        "planned_sources": 15,
        "planned_batches": 180,
        "planned_posttests": 45,
        "planned_retests": 15,
        "max_workers": design.get("max_workers", 15),
        "complete_chains": sum(r["status"] == "completed" for r in results),
        "source_batches": sum(len(r.get("source", {}).get("batches", [])) for r in results),
        "posttests": sum(
            bool(t.get("payload")) and not t.get("failure")
            for r in results
            for t in r["posttests"].values()
        ),
        "retests": sum(bool(r.get("recommendation_retest", {}).get("passed")) for r in results),
        "status_counts": dict(Counter(r["status"] for r in results)),
        "historical_reference_batches_reused": 60,
        "new_reference_batches": 0,
        "results": [],
    }
    pilot = effective(root / "pilot")
    summary["pilot"] = (
        None
        if not pilot
        else {
            "status": pilot["status"],
            "source_batches": len(pilot.get("source", {}).get("batches", [])),
            "posttests": sum(
                bool(t.get("payload")) and not t.get("failure") for t in pilot["posttests"].values()
            ),
            "failure": pilot.get("failure"),
            "operations": pilot.get("source", {}).get("operations"),
            "retest_passed": pilot.get("recommendation_retest", {}).get("passed"),
            "tokens": pilot.get("tokens"),
            "posttest_repair": pilot.get("posttest_repair"),
        }
    )
    prior = root / "prior-integration-attempts.json"
    summary["prior_integration_costs"] = read(prior) if prior.exists() else None
    disposition = root / "disposition.json"
    summary["disposition"] = read(disposition) if disposition.exists() else None
    lines = [
        "# Purification: five worlds, three E arms, twelve batches",
        "",
        f"Observed: {summary['observed_at']}. Development evidence. Sol medium; English.",
        f"Disposition: {summary['disposition'] or 'current development block'}.",
        "",
        f"Complete chains: {summary['complete_chains']}/15;"
        f" final-assayed source batches: {summary['source_batches']}/180;"
        f" sealed K1/Q/K2: {summary['posttests']}/45;"
        f" recommendation retests: {summary['retests']}/15.",
        "",
        f"Separate integration pilot: {None if not pilot else pilot['status']}."
        " Historical reference batches reused: 60; new reference batches: 0.",
        (
            "Pilot interruption retained: "
            + str(pilot["posttest_repair"]["original_failure"])
            + "; resumed on the original thread without repeating source experiments."
            if pilot and pilot.get("posttest_repair")
            else ""
        ),
        "",
        "| Cell | Status | Final-assayed batches | Posttests | Retest |",
        "|---|---|---:|---:|---|",
    ]
    terminal = all(r["status"] in ("completed", "failed") for r in results)
    extra = {"attempts": 0, "source_batches": 0, "operations": 0, "local_startup_attempts": 0}
    for r in results:
        n = sum(bool(t.get("payload")) and not t.get("failure") for t in r["posttests"].values())
        row = {k: r[k] for k in ("id", "world_id", "arm", "budget", "status")}
        row.update(
            source_batches=len(r.get("source", {}).get("batches", [])),
            posttests=n,
            failure=r.get("failure"),
            tokens=r.get("tokens"),
            replay=r.get("source", {}).get("exact_replay"),
            source_validation=r.get("source", {}).get("validation_checks"),
            timing_s={
                "source": r.get("source", {}).get("elapsed_s"),
                **{
                    stage: r["posttests"].get(stage, {}).get("elapsed_s")
                    for stage in ("K1", "Q", "K2")
                },
                "retest": r.get("recommendation_retest", {}).get("elapsed_s"),
            },
            recommendation=r.get("recommendation"),
            retest_metrics=[
                b["metrics"] for b in r.get("recommendation_retest", {}).get("batches", [])
            ],
        )
        if terminal and r["posttests"].get("Q", {}).get("payload"):
            row["prediction_evaluation"] = evaluate(
                r["posttests"]["Q"]["payload"],
                references[r["world_id"]]["observations"],
                design["queries"],
            )
        if terminal:
            row["batch_accounting"] = batch_accounting(root / "sources" / r["id"])
        summary["results"].append(row)
        lines.append(
            f"| [{r['id']}]({r['id']}.md) | {r['status']} |"
            f" {row['source_batches']}/12 | {n}/3 |"
            f" {bool(r.get('recommendation_retest', {}).get('passed'))} |"
        )
        if r["status"] in ("completed", "failed"):
            text = [
                f"# {r['id']}",
                "",
                f"Status: {r['status']}; failure: {r.get('failure')}",
                "",
                "## Source instructions",
                "",
                SOURCE_SYSTEM,
                "",
                "## Batch observations",
                "",
                "```json",
                json.dumps(r.get("source", {}).get("batches", []), indent=2),
                "```",
                "",
                "## Recommendation and retest",
                "",
                "```json",
                json.dumps(
                    {
                        "recommendation": r.get("recommendation"),
                        "retest_metrics": row["retest_metrics"],
                    },
                    indent=2,
                ),
                "```",
            ]
            for stage in ("K1", "Q", "K2"):
                text.extend(
                    [
                        "",
                        f"## {stage} prompt",
                        "",
                        design[stage],
                        "",
                        f"## {stage} answer",
                        "",
                        json.dumps(
                            r["posttests"].get(stage, {}).get("payload"),
                            ensure_ascii=False,
                            indent=2,
                        ),
                    ]
                )
            text += [
                "",
                "## Prediction evaluation",
                "",
                "```json",
                json.dumps(row.get("prediction_evaluation"), indent=2),
                "```",
                "",
            ]
            (report / f"{r['id']}.md").write_text("\n".join(text), encoding="utf-8")
        parent = root / "sources" / r["id"]
        pointer = (
            read(parent / "effective.json")["path"]
            if (parent / "effective.json").exists()
            else None
        )
        for path in parent.glob("attempt-*/result.json"):
            if str(path) == pointer:
                continue
            attempt = read(path)
            startup = startup_failure(path.parent, attempt)
            if attempt.get("source_transport_retry_eligible") or startup:
                extra["attempts"] += 1
                extra["source_batches"] += len(attempt["source"]["batches"])
                extra["operations"] += attempt["source"]["operations"]
                extra["local_startup_attempts"] += int(startup)
    summary["extra_source_attempts"] = extra
    summary["terminal"] = terminal
    if terminal:
        summary["batch_accounting"] = {
            key: sum(row["batch_accounting"][key] for row in summary["results"])
            for key in ("started", "final_assayed", "discarded")
        }
        lines += [
            "",
            "Batch lifecycle totals: " + str(summary["batch_accounting"]) + ". "
            "Discarded batches consume the campaign budget and are retained; they do not "
            "count as final-assayed batches or trigger a replacement source.",
        ]
    lines += [
        "",
        f"Additional transport/startup attempts (not independent effective cells): {extra}.",
        "",
        "Prediction evaluation appears only after the source matrix is terminal."
        " Pilot and historical reference costs are separate. Scientific negative outcomes"
        " and nonconforming sources are retained.",
        "",
    ]
    atomic_write(report / "summary.json", summary)
    (report / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def spawn_worker(root, cell_id):
    parent = root / ("pilot" if cell_id == "pilot" else "sources/" + cell_id)
    parent.mkdir(parents=True, exist_ok=True)
    command = [
        "uv",
        "run",
        "--no-sync",
        "python",
        "-m",
        "scripts.run_work_ii_p_study",
        "--phase",
        "worker",
        "--root",
        str(root),
        "--cell",
        cell_id,
    ]
    with (parent / "worker.log").open("ab", buffering=0) as log:
        return subprocess.Popen(
            command,
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            env={**os.environ, **WORKER_ENV},
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )


def recover_startup(root, report):
    """Backfill only zero-operation local startup failures; live workers keep running."""
    launch = read(ROOT / "runs/formal/work-ii-c-five-world-20260920-v3-auto/parallel-launch.json")
    command = launch["command"]
    proxy = command[command.index("--proxy") + 1]
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        os.environ[key] = proxy
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "stage": "startup_recovery",
        "max_workers": 15,
        "worker_env": WORKER_ENV,
        "started_epoch": time.time(),
        "recovered_cells": [],
    }

    def emit():
        state["epoch"] = time.time()
        atomic_write(root / "startup-recovery-status.json", state)
        print(json.dumps(state), flush=True)

    active = {}
    for cell in read(root / "design.json")["schedule"]:
        parent = root / "sources" / cell["id"]
        status = read(parent / "status.json")
        if host.controller_alive(status):
            continue
        pointer = read(parent / "effective.json")
        path = Path(pointer["path"])
        result = read(path)
        if result["status"] != "failed" or not startup_failure(path.parent, result):
            continue
        active[cell["id"]] = spawn_worker(root, cell["id"])
        state["recovered_cells"].append(cell["id"])
        emit()
        time.sleep(5)
    while active:
        state["active_recovery_workers"] = len(active)
        emit()
        time.sleep(30)
        for cell_id, process in list(active.items()):
            if process.poll() is not None:
                state.setdefault("exit_codes", {})[cell_id] = process.returncode
                del active[cell_id]
    # The original controller still owns any originally successful startup.
    # Avoid racing its summary writer; it has no authority over these disjoint cells.
    while host.controller_alive(read(root / "controller-status.json")):
        state["stage"] = "waiting_for_original_workers"
        emit()
        time.sleep(30)
    export(root, report)
    state.update(stage="terminal", active_recovery_workers=0)
    emit()


def coordinate(root, report):
    previous = root / "controller-status.json"
    if previous.exists() and host.controller_alive(read(previous)):
        raise ValueError("P coordinator is already alive")
    design = read(root / "design.json")
    state = {
        "pid": os.getpid(),
        "process_created": psutil.Process().create_time(),
        "started_epoch": time.time(),
        "stage": "pilot",
        "max_workers": design.get("max_workers", 6),
    }
    # Reuse the known working process-local transport without printing credentials.
    launch = ROOT / "runs/formal/work-ii-c-five-world-20260920-v3-auto/parallel-launch.json"
    if launch.exists():
        command = read(launch)["command"]
        proxy = command[command.index("--proxy") + 1]
        for key in (
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "ALL_PROXY",
            "http_proxy",
            "https_proxy",
            "all_proxy",
        ):
            os.environ[key] = proxy

    def emit(active):
        summary = export(root, report)
        elapsed = time.time() - state["started_epoch"]
        completed = summary["complete_chains"]
        sealed = [effective(root / "sources" / c["id"]) for c in design["schedule"]]
        terminal = sum(bool(r and r["status"] in ("completed", "failed")) for r in sealed)
        base = effective(root / "pilot")
        durations = {"source": 0.0, "K1": 0.0, "Q": 0.0, "K2": 0.0}
        if base and base.get("source"):
            durations["source"] = base["source"].get("elapsed_s", 0)
            for stage in ("K1", "Q", "K2"):
                durations[stage] = base["posttests"].get(stage, {}).get("elapsed_s", 0)
        full = sum(durations.values()) + 5
        remaining = []
        for cell, result in zip(design["schedule"], sealed, strict=True):
            if result and result["status"] in ("completed", "failed"):
                continue
            path = root / "sources" / cell["id"] / "status.json"
            status = read(path) if path.exists() else {}
            phase = status.get("phase", "starting")
            if phase == "source":
                estimate = durations["source"] * max(0, 1 - status.get("batches", 0) / 12)
                estimate += sum(durations[s] for s in ("K1", "Q", "K2")) + 5
            elif phase in ("K1", "Q", "K2"):
                stages = ["K1", "Q", "K2"]
                estimate = sum(durations[s] for s in stages[stages.index(phase) :]) + 5
            elif phase == "recommendation_retest":
                estimate = 5
            else:
                estimate = full
            remaining.append(estimate)
        eta = (
            max(max(remaining, default=0), sum(remaining) / state["max_workers"])
            if full > 5
            else None
        )
        state.update(
            epoch=time.time(),
            active_workers=len(active),
            completed_sources=completed,
            source_batches=summary["source_batches"],
            posttests=summary["posttests"],
            sources_per_hour=3600 * completed / elapsed if completed else None,
            terminal_sources=terminal,
            eta_s=eta if base and base.get("status") == "completed" else None,
            eta_basis=(
                "Pilot phase durations and remaining work across actual worker slots; conditional"
            ),
        )
        atomic_write(previous, state)
        print(json.dumps(state), flush=True)

    pilot = effective(root / "pilot")
    if not pilot or pilot["status"] not in ("completed", "failed"):
        process = spawn_worker(root, "pilot")
        while process.poll() is None:
            emit([process])
            time.sleep(30)
        pilot = effective(root / "pilot")
    if not pilot or pilot["status"] != "completed":
        state.update(
            stage="pilot_requires_inspection",
            failure=pilot.get("failure") if pilot else "worker_error",
        )
        emit([])
        return
    state["stage"] = "parallel_sources"
    active = {}
    pending = []
    for cell in design["schedule"]:
        r = effective(root / "sources" / cell["id"])
        if not r or r["status"] not in ("completed", "failed"):
            pending.append(cell)
    while active or pending:
        while pending and len(active) < state["max_workers"]:
            cell = pending.pop(0)
            active[cell["id"]] = spawn_worker(root, cell["id"])
            emit(active)
            time.sleep(5)
        emit(active)
        time.sleep(30)
        for cell_id, process in list(active.items()):
            if process.poll() is not None:
                state.setdefault("worker_exit_codes", {})[cell_id] = process.returncode
                del active[cell_id]
    state["stage"] = "terminal"
    emit([])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase",
        choices=("prepare", "launch", "coordinate", "worker", "export", "recover-startup"),
        required=True,
    )
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--cell")
    args = parser.parse_args()
    root = args.root.resolve()
    report = args.report.resolve() if args.report else None
    if args.phase == "prepare":
        prepare(root, report)
    elif args.phase == "worker":
        worker(root, args.cell)
    elif args.phase == "coordinate":
        coordinate(root, report)
    elif args.phase == "export":
        export(root, report)
    elif args.phase == "recover-startup":
        recover_startup(root, report)
    else:
        path = root / "controller-status.json"
        if path.exists() and host.controller_alive(read(path)):
            raise ValueError("P coordinator already running")
        command = [
            "uv",
            "run",
            "--no-sync",
            "python",
            "-m",
            "scripts.run_work_ii_p_study",
            "--phase",
            "coordinate",
            "--root",
            str(root),
            "--report",
            str(report),
        ]
        process = host.detached_process(command, root / "controller.log")
        print(
            json.dumps(
                {
                    "launcher_pid": process.pid,
                    "concurrency_after_pilot": read(root / "design.json")["max_workers"],
                }
            )
        )


if __name__ == "__main__":
    main()
