#!/usr/bin/env python3
"""Prepare and run the bounded 15-pair EQ readout block; never execute physics."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import shutil
import tempfile
import time
from pathlib import Path
from statistics import fmean

import jsonschema
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq
import scripts.run_work_ii_final_diagnostic as provider
from scripts.run_work_ii_study_b import _prepare_codex_home

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS

ROOT = Path(__file__).resolve().parents[1]
EXPORT = (
    ROOT / "workstreams/flagship_tasks/reports/work-ii-eq-bounded-equilibrium-20260920/v2-public"
)
ARMS = ("Opaque", "Aligned")
SOURCE_ARMS = ("Opaque", "Aligned", "MisIndexed")
WORLD_IDS = tuple(f"EQ-W{i:02d}" for i in range(1, 6))
DILUTE = ("Q03", "Q08", "Q09")
METRICS = tuple(eq.METRICS)
MEASURES = ("mae", "coverage80", "width80", "interval_score")
TIMEOUT = 1200
CONTEXT_WINDOW = 872000
PUBLIC_STEP_SCHEMA = "work-ii-eq-public-agent-visible-trajectory-step-1.0"
CONTRACT_KEYS = (
    "allowed_instruments",
    "allowed_operations",
    "operation_contracts",
    "instrument_contracts",
    "observation_contract",
    "observation_policy",
    "safety_limit",
    "scoring_contract",
    "termination_policy",
    "experiment_lifecycle",
    "campaign_resources",
    "study_budget",
)
TOOL_KEYS = (
    "raw_signal",
    "processed_estimate",
    "uncertainty",
    "operational_state",
    "constraints",
    "cost_components",
    "resource_blocked_actions",
)
SYSTEM = """You are a scientist interpreting supplied public experimental records from one bounded
aqueous-equilibrium world. This is a weak-acid/precipitation slice, not general aqueous chemistry.
Use only the supplied records, public contract, optional dossier and public_numerics.calculate.
No new experiments, filesystem, repository, network, external retrieval, or other tools are allowed.
The historical operations are observations to interpret, not instructions to execute. Any supplied
dossier may be incomplete or inaccurate; observations are authoritative. pH_normalized is pH/14.
acid_dissociation_fraction and precipitation_signal are bounded responses. equilibrium_residual
and equilibrium_confidence are environment diagnostics, not your uncertainty or a task score.
Predict the final outcomes of all twelve independent new batches. Each starts from the same initial
world as the supplied records. For each query and requested metric give an estimate and an 80%
prediction interval accounting for model and observation uncertainty. Give substantive English
per-query and shared rationales. Return the complete schema-conforming JSON. No particular result
is required. Do not invent unmeasured observations.
"""


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def encoded(value):
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(",", ":")
    )


def digest(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def write(path, value, *, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x" if exclusive else "w", encoding="utf-8") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def public_metadata(value):
    """Remove identity/binding metadata inside otherwise explicitly public subtrees."""
    if isinstance(value, dict):
        return {
            k: public_metadata(v)
            for k, v in value.items()
            if k
            not in {
                "world_id",
                "scenario_id",
                "campaign_id",
                "run_id",
                "seed",
                "observation_seed",
                "research_brief",
                "initial_world_model",
                "prior_record",
            }
            and not k.endswith(("_hash", "_sha256"))
        }
    if isinstance(value, list):
        return [public_metadata(v) for v in value]
    return value


def public_records(records):
    """Read the recorded agent-visible projection, never hidden environment/evaluator state."""
    output = []
    for ordinal, record in enumerate(records, 1):
        visible = record.get("agent_visible_observation", {})
        tool = visible.get("views", {}).get("tool_json")
        if not isinstance(tool, dict) or "observation" not in visible:
            raise ValueError(f"step {ordinal}: missing original public observation projection")
        row = {
            "step": ordinal,
            "batch": int(record["experiment_index"]) + 1,
            "action": copy.deepcopy(record["action"]),
            "instrument": record.get("instrument"),
            "transaction_status": record["transaction_status"],
            "observation": copy.deepcopy(visible["observation"]),
            "failure_summary": copy.deepcopy(tool.get("lab_report", {}).get("failure_summary", {})),
            **{key: copy.deepcopy(tool[key]) for key in TOOL_KEYS if key in tool},
        }
        row.update({key: record[key] for key in ("terminated", "truncated") if key in record})
        lab = tool.get("lab_report", {})
        if "final_assay_summary" in lab:
            row["lifecycle"] = {
                key: lab["final_assay_summary"][key]
                for key in (
                    "episode_done",
                    "experiment_ended",
                    "final_assay_count",
                    "is_final_assay",
                )
            }
        if "instrument_summary" in lab:
            row["measurement"] = copy.deepcopy(lab["instrument_summary"])
        resources = tool.get("campaign_state", {}).get("campaign_resources", {})
        if resources:
            row["resource_state"] = copy.deepcopy(resources["state"])
        # Exclude agent_trace, explanation, evaluator fields and donor reports.
        output.append(public_metadata(row))
    return output


def exported_history(path, cell_id, batches):
    """Consume the retained public-I/O export without exposing its donor explanations."""
    result_path = path.parent / "RESULT.json"
    binding = read(result_path)["source"]["agent_visible_trajectory"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != binding["public_sha256"]:
        raise ValueError(f"{cell_id}: exported trajectory does not match its result binding")
    if not binding["exact_replay_verified"] or binding["completed_batches"] != 12:
        raise ValueError(f"{cell_id}: incomplete retained source")
    exported = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if len(exported) != binding["operations"]:
        raise ValueError(f"{cell_id}: operation count mismatch")
    normalized, schemas, briefs = [], {}, {}
    for ordinal, row in enumerate(exported, 1):
        if (
            row["schema_version"] != PUBLIC_STEP_SCHEMA
            or row["cell_id"] != cell_id
            or row["step"] != ordinal
        ):
            raise ValueError(f"{cell_id}: source identity/order mismatch")
        visible = row["environment_output"]
        tool = visible["views"]["tool_json"]
        instrument = tool["lab_report"]["instrument_summary"]["instrument"]
        normalized.append(
            {
                "experiment_index": row["experiment_index"],
                "action": row["agent_output"]["action"],
                "instrument": instrument,
                "transaction_status": row["transaction"]["status"],
                "observation": visible["observation"],
                "agent_visible_observation": visible,
            }
        )
        # Public rules already shown by the original environment; no current simulator contract.
        brief = {
            key: tool["research_brief"][key]
            for key in ("measurement_contract", "sensor_contract", "score_status")
        }
        briefs[digest(brief)] = brief
        for action in tool["available_actions"]:
            schema = public_metadata(action["schema"])
            schemas[digest(schema)] = schema
    if eq.shared.summaries(normalized) != batches:
        raise ValueError(
            f"{cell_id}: exported operations/observations differ from retained batches"
        )
    if len(briefs) != 1:
        raise ValueError(f"{cell_id}: inconsistent public measurement contract")
    # Schemas can have state-dependent bounds: retain each distinct version, with per-step refs.
    schema_names = {key: f"S{i:03d}" for i, key in enumerate(schemas, 1)}
    public = public_records(normalized)
    for output, original in zip(public, exported, strict=True):
        tool = original["environment_output"]["views"]["tool_json"]
        output["public_action_schemas_after_step"] = [
            schema_names[digest(public_metadata(a["schema"]))] for a in tool["available_actions"]
        ]
        output["rollback_reason"] = original["transaction"]["rollback_reason"]
    initial = exported[0]["agent_input"]
    return {
        "public_contract": {
            **next(iter(briefs.values())),
            "operation_schema_catalog": {
                schema_names[key]: value for key, value in schemas.items()
            },
            "schema_scope": "Recorded public schemas; state-dependent bounds apply after the step.",
        },
        "initial_public_context": {
            key: copy.deepcopy(initial[key])
            for key in (
                "visible_metrics",
                "constraint_flags",
                "available_operations",
                "remaining_operations",
            )
        },
        "records": public,
    }


def locate_history(source_root, cell_id, batches):
    public_path = source_root / "sources" / cell_id / "trajectory.jsonl"
    if (source_root / "TRAJECTORY_INDEX.json").is_file() and public_path.is_file():
        return exported_history(public_path, cell_id, batches), [str(public_path.resolve())]
    candidates = []
    for base in (source_root / "sources" / cell_id, source_root / "recoveries" / cell_id):
        if base.exists():
            candidates.extend(base.rglob("trajectory.jsonl"))
    matches = []
    for path in sorted(set(candidates)):
        records = [
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line
        ]
        if eq.shared.summaries(records) != batches:
            continue
        contracts = sorted(path.parent.glob("**/reference/task_contract.json"))
        if not contracts:
            continue
        projected = [
            {key: public_metadata(read(p)[key]) for key in CONTRACT_KEYS if key in read(p)}
            for p in contracts
        ]
        if len({digest(p) for p in projected}) != 1:
            raise ValueError(f"{cell_id}: conflicting public contracts")
        contract = projected[0]
        if (
            not {"allowed_instruments", "operation_contracts", "instrument_contracts"}
            <= contract.keys()
        ):
            raise ValueError(f"{cell_id}: incomplete public contract")
        history = {"public_contract": contract, "records": public_records(records)}
        matches.append((path, history))
    if not matches:
        raise ValueError(f"{cell_id}: complete matching trajectory and public contract absent")
    if len({digest(history) for _, history in matches}) != 1:
        raise ValueError(
            f"{cell_id}: differing intermediate evidence; resolve effective source explicitly"
        )
    return matches[0][1], [str(path.resolve()) for path, _ in matches]


def validate_truth(truth, queries):
    if set(truth) != {q["query_id"] for q in queries}:
        raise ValueError("reference query mismatch")
    for repeats in truth.values():
        if len(repeats) != 5:
            raise ValueError("exactly five retained reference observations required")
        for repeat in repeats:
            if set(repeat) != set(METRICS) or any(
                not isinstance(v, (int, float)) or not math.isfinite(v) or not 0 <= v <= 1
                for v in repeat.values()
            ):
                raise ValueError("invalid reference response")


def prepare(source_root, root, export=EXPORT):
    if root.exists():
        raise ValueError("preparation is write-once; use check for an existing block")
    config = eq.load_config()
    queries = eq.queries(config)
    expected = [f"{world}--{arm}" for world in WORLD_IDS for arm in SOURCE_ARMS]
    origins = {
        c["cell_id"]: c["effective_origin"] for c in read(export / "RECOVERY_AUDIT.json")["cells"]
    }
    if set(origins) != set(expected):
        raise ValueError("the retained export must contain all fifteen fixed sources")
    index = read(export / "INDEX.json")["cells"]
    if {c["cell_id"]: c["effective_origin"] for c in index} != origins:
        raise ValueError("source index and retained-attempt map disagree")
    if any(c["status"] != "completed" or not c["posttest_chain_sealed"] for c in index):
        raise ValueError("retained source index is incomplete")
    histories, truths, errors = [], {}, []
    for number, cell_id in enumerate(expected, 1):
        result = read(export / "sources" / cell_id / "RESULT.json")
        world = cell_id.split("--")[0]
        if result["effective_origin"] != origins[cell_id] or len(result["source"]["batches"]) != 12:
            raise ValueError(f"{cell_id}: retained source identity/count mismatch")
        truth = result["reference_truth"]
        validate_truth(truth, queries)
        if world in truths and truths[world] != truth:
            raise ValueError(f"{world}: reference truth differs across source arms")
        truths[world] = truth
        try:
            history, paths = locate_history(source_root, cell_id, result["source"]["batches"])
        except ValueError as exc:
            errors.append(str(exc))
            continue
        histories.append(
            {
                "history_id": f"H{number:02d}",
                "world": world,
                "source_cell": cell_id,
                "effective_origin": origins[cell_id],
                "source_files": paths,
                "evidence": history,
                "aligned_dossier": eq.public_prior(config, world, "Aligned"),
            }
        )
    if errors:
        raise ValueError("Preparation incomplete; no inputs written:\n" + "\n".join(errors))
    cells, packets = [], {}
    for number, history in enumerate(histories):
        # No history/world/source-arm labels or primary subgroup definition reach the participant.
        common = {
            **history["evidence"],
            "queries": queries,
            "calculator_budget": FOLLOWUP_NUMERICS.disclosure(),
        }
        order = ARMS if number % 2 == 0 else tuple(reversed(ARMS))
        for arm in order:
            cell = {
                "id": f"R{len(cells) + 1:02d}",
                "history_id": history["history_id"],
                "world": history["world"],
                "readout_arm": arm,
            }
            packet = {
                **common,
                "instance_dossier": history["aligned_dossier"] if arm == "Aligned" else None,
            }
            cells.append(cell)
            packets[cell["id"]] = packet
    design = {
        "version": 1,
        "evidence_class": "development",
        "provider": eq.PROVIDER,
        "planned_sessions": 30,
        "planned_pairs": 15,
        "planned_worlds": 5,
        "dilute_queries": list(DILUTE),
        "timeout_s": TIMEOUT,
        "context_window": CONTEXT_WINDOW,
        "numerics_budget": FOLLOWUP_NUMERICS.to_dict(),
        "system": SYSTEM,
        "schema": eq.posttest_schema("Q"),
        "queries": queries,
        "cells": cells,
        "packet_sha256": {key: digest(value) for key, value in packets.items()},
        "truth_sha256": digest(truths),
        "source_input_root": str(source_root.resolve()),
    }
    # Validate pairs before creating any run directory.
    validate_pairs(design, packets)
    for key, packet in packets.items():
        write(root / "packets" / f"{key}.json", packet, exclusive=True)
    write(
        root / "private" / "source-map.json",
        [{k: v for k, v in h.items() if k != "evidence"} for h in histories],
        exclusive=True,
    )
    write(root / "private" / "truth.json", truths, exclusive=True)
    write(root / "design.json", design, exclusive=True)
    write_preparation_summary(root, design, histories, packets)
    print(
        encoded({"phase": "prepared", "sessions": 30, "pairs": 15, "provider_calls": 0}), flush=True
    )
    return design


def write_preparation_summary(root, design, histories, packets):
    """One readable input receipt in the run directory, not another release gate."""
    summary = {
        "phase": "prepared_not_started",
        "planned_sessions": 30,
        "planned_pairs": 15,
        "source_histories": len(histories),
        "source_operations": sum(len(h["evidence"]["records"]) for h in histories),
        "provider_calls": 0,
        "simulator_calls": 0,
        "histories": [],
    }
    for history in histories:
        records = history["evidence"]["records"]
        cells = [c for c in design["cells"] if c["history_id"] == history["history_id"]]
        summary["histories"].append(
            {
                "history_id": history["history_id"],
                "source_cell": history["source_cell"],
                "operations": len(records),
                "final_assays": sum(
                    r["instrument"] == "final_assay" and r["transaction_status"] == "committed"
                    for r in records
                ),
                "intermediate_measurements": sum(
                    r["instrument"] not in (None, "final_assay")
                    and r["transaction_status"] == "committed"
                    for r in records
                ),
                "rejected_or_rolled_back": sum(
                    r["transaction_status"] != "committed" for r in records
                ),
                "packet_utf8_bytes": {
                    c["readout_arm"]: len(encoded(packets[c["id"]]).encode("utf-8")) for c in cells
                },
            }
        )
    write(root / "preparation.json", summary)
    lines = [
        "# EQ fixed-evidence input preparation",
        "",
        "30 sessions / 15 pairs; not started.",
        "No provider or simulator calls.",
        "",
        "| History | Source | Operations | Intermediate measurements | Final assays | Rejections |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for h in summary["histories"]:
        lines.append(
            f"| {h['history_id']} | {h['source_cell']} | {h['operations']} | "
            f"{h['intermediate_measurements']} | {h['final_assays']} | "
            f"{h['rejected_or_rolled_back']} |"
        )
    (root / "preparation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_pairs(design, packets):
    if len(design["cells"]) != 30 or len({c["id"] for c in design["cells"]}) != 30:
        raise ValueError("readout denominator must be thirty unique cells")
    groups = {}
    for cell in design["cells"]:
        groups.setdefault(cell["history_id"], []).append(cell)
    if len(groups) != 15 or {c["world"] for c in design["cells"]} != set(WORLD_IDS):
        raise ValueError("fixed fifteen-history/five-world coverage mismatch")
    if any(sum(c["world"] == w for c in design["cells"]) != 6 for w in WORLD_IDS):
        raise ValueError("each world requires three pairs")
    for cells in groups.values():
        if len(cells) != 2 or {c["readout_arm"] for c in cells} != set(ARMS):
            raise ValueError("each history requires exactly one Opaque/Aligned pair")
        common = []
        for cell in cells:
            packet = copy.deepcopy(packets[cell["id"]])
            dossier = packet.pop("instance_dossier")
            if (dossier is None) != (cell["readout_arm"] == "Opaque"):
                raise ValueError("dossier treatment mismatch")
            common.append(packet)
        if common[0] != common[1] or cells[0]["world"] != cells[1]["world"]:
            raise ValueError("paired evidence differs")


def check(root, *, environment=True):
    design = read(root / "design.json")
    packets = {c["id"]: read(root / "packets" / f"{c['id']}.json") for c in design["cells"]}
    validate_pairs(design, packets)
    if design["packet_sha256"] != {k: digest(v) for k, v in packets.items()}:
        raise ValueError("prepared participant input changed")
    if digest(read(root / "private" / "truth.json")) != design["truth_sha256"]:
        raise ValueError("prepared reference changed")
    for cell in design["cells"]:
        started = root / "sessions" / cell["id"] / "started.json"
        if started.exists() and read(started)["design_sha256"] != digest(design):
            raise ValueError("design changed after the block started")
    if (
        design["provider"] != eq.PROVIDER
        or design["system"] != SYSTEM
        or design["timeout_s"] != TIMEOUT
        or design["context_window"] != CONTEXT_WINDOW
        or design["dilute_queries"] != list(DILUTE)
        or design["numerics_budget"] != FOLLOWUP_NUMERICS.to_dict()
        or design["schema"] != eq.posttest_schema("Q")
        or design["queries"] != eq.queries(eq.load_config())
    ):
        raise ValueError("prepared execution design changed")
    if environment:
        if not shutil.which("codex"):
            raise ValueError("Codex CLI unavailable")
        auth = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
        if not auth.is_file():
            raise ValueError("cached provider login unavailable")
    return {
        "phase": "inputs_checked",
        "sessions": 30,
        "pairs": 15,
        "provider_calls": 0,
        "network_or_auth_validity_tested": False,
    }


def prediction_validation(payload, design):
    try:
        jsonschema.validate(payload, design["schema"])
    except jsonschema.ValidationError:
        return {"valid": False, "failure": "invalid_response_schema"}
    return eq.validate_posttest("Q", payload, design["queries"])


def execute_cell(root, design, cell, progress):
    folder = root / "sessions" / cell["id"]
    packet = read(root / "packets" / f"{cell['id']}.json")
    # Auth is copied into a new isolated home; no donor sessions or repository files are copied.
    with tempfile.TemporaryDirectory(prefix="eq-readout-") as temporary:
        isolated = Path(temporary)
        workspace = isolated / "workspace"
        workspace.mkdir()
        environment = _prepare_codex_home(isolated, design["provider"])
        schema = workspace / "answer-schema.json"
        write(schema, design["schema"])
        instructions = workspace / "instructions.md"
        instructions.write_text(design["system"], encoding="utf-8")
        audit = folder / "numerics.jsonl"
        command = eq.provider_shared.build_command(
            design["provider"],
            schema,
            workspace,
            audit=audit,
            thread_id=None,
            provider_retries=0,
            numerics_budget=FOLLOWUP_NUMERICS,
        )
        command.extend(["-c", f"model_instructions_file={json.dumps(instructions.as_posix())}"])
        command.extend(["-c", f"model_context_window={design['context_window']}"])
        raw = provider.launch(
            command,
            "INPUT:\n" + encoded(packet),
            workspace,
            environment,
            folder / "provider",
            design["timeout_s"],
            True,
            audit,
            progress,
            numerics_budget=FOLLOWUP_NUMERICS,
        )
        # Preserve raw session/resource receipts outside the participant workspace and outside Git.
        sessions = isolated / "codex-home" / "sessions"
        if sessions.exists():
            shutil.copytree(sessions, folder / "private-sessions")
        return raw


def terminal_result(raw, design):
    validation = prediction_validation(raw.get("payload"), design)
    return {
        "payload": raw.get("payload"),
        "valid": validation["valid"] and not raw.get("failure"),
        "failure": raw.get("failure") or validation["failure"],
        "infrastructure_failure": bool(raw.get("failure")),
        "elapsed_s": raw.get("elapsed_s"),
        "method_resources": raw.get("method_resources"),
        "usage": raw.get("usage"),
        "numerics_attempts": raw.get("numerics_attempts"),
    }


def run(root, *, pair_only=False):
    check(root)
    design = read(root / "design.json")
    cells = design["cells"][:2] if pair_only else design["cells"]
    if (root / "stopped.json").exists():
        raise ValueError("block stopped; retain its failures and unstarted denominator")
    lock = root / "executor.lock"
    with lock.open("x", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    started = time.monotonic()
    executed, consecutive_failures = 0, 0
    try:
        for index, cell in enumerate(cells):
            folder = root / "sessions" / cell["id"]
            terminal = folder / "result.json"
            if terminal.exists():
                previous = read(terminal)
                consecutive_failures = (
                    consecutive_failures + 1 if previous["infrastructure_failure"] else 0
                )
                if consecutive_failures >= 3 or previous["failure"] == "platform_interrupted":
                    write(
                        root / "stopped.json",
                        {"reason": "infrastructure_stop", "after": cell["id"]},
                        exclusive=True,
                    )
                    break
                continue
            if (folder / "started.json").exists():
                # A fully sealed launch receipt can be recovered without another provider call.
                receipt = folder / "provider" / "receipt.json"
                if not receipt.exists():
                    raise ValueError(f"{cell['id']}: ambiguous started cell; no automatic retry")
                result = terminal_result(read(receipt), design)
            else:
                elapsed = time.monotonic() - started
                progress = {
                    "phase": "readout",
                    "completed": index,
                    "total": len(cells),
                    "session": cell["id"],
                    "new_sessions": executed,
                    "sessions_per_hour": executed * 3600 / elapsed if elapsed else 0,
                    "eta_s": elapsed / executed * (len(cells) - index) if executed else None,
                }
                print(encoded(progress), flush=True)
                write(
                    folder / "started.json",
                    {"started_epoch": time.time(), "design_sha256": digest(design)},
                    exclusive=True,
                )
                try:
                    raw = execute_cell(root, design, cell, progress)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception as exc:
                    raw = {"failure": f"launcher_exception:{type(exc).__name__}", "payload": None}
                    write(
                        folder / "exception.json",
                        {"type": type(exc).__name__, "message": str(exc)},
                        exclusive=True,
                    )
                result = terminal_result(raw, design)
                executed += 1
            write(terminal, result, exclusive=True)
            consecutive_failures = (
                consecutive_failures + 1 if result["infrastructure_failure"] else 0
            )
            if consecutive_failures >= 3 or result["failure"] == "platform_interrupted":
                write(
                    root / "stopped.json",
                    {"reason": "infrastructure_stop", "after": cell["id"]},
                    exclusive=True,
                )
                break
    finally:
        lock.unlink()
    return analyze_pair(root) if pair_only else analyze(root)


def score(payload, truth, query_ids):
    predictions = {p["query_id"]: p["metrics"] for p in payload["predictions"]}
    output = {}
    for metric in METRICS:
        errors, covered, widths, scores = [], [], [], []
        for qid in query_ids:
            p = predictions[qid][metric]
            low, high = p["lower80"], p["upper80"]
            outcomes = [row[metric] for row in truth[qid]]
            errors.append(abs(p["estimate"] - fmean(outcomes)))
            for y in outcomes:
                covered.append(low <= y <= high)
                widths.append(high - low)
                scores.append(high - low + 10 * max(low - y, y - high, 0))
        output[metric] = dict(
            zip(MEASURES, map(fmean, (errors, covered, widths, scores)), strict=True)
        )
    output["macro"] = {key: fmean(output[m][key] for m in METRICS) for key in MEASURES}
    return {
        "queries": len(query_ids),
        "references_per_metric": 5 * len(query_ids),
        "metrics": output,
    }


def mean_contrasts(rows):
    return {
        metric: {
            key: fmean(row[metric][key] for row in rows)
            for key in ("dilute_difference", "other_difference", "interaction")
        }
        for metric in (*METRICS, "macro")
    }


def analyze_pair(root):
    """Inspect the explicitly authorized first pair without launching/scoring the other cells."""
    check(root, environment=False)
    design = read(root / "design.json")
    cells = design["cells"][:2]
    if cells[0]["history_id"] != cells[1]["history_id"]:
        raise ValueError("the first two scheduled cells must form one matched pair")
    results = {}
    for cell in cells:
        path = root / "sessions" / cell["id"] / "result.json"
        if not path.exists():
            raise ValueError("pair scoring requires both sealed terminal results")
        results[cell["id"]] = read(path)
    truth = read(root / "private" / "truth.json")[cells[0]["world"]]
    other = [q["query_id"] for q in design["queries"] if q["query_id"] not in DILUTE]
    readouts = []
    for cell in cells:
        result = results[cell["id"]]
        valid = result["valid"] and prediction_validation(result["payload"], design)["valid"]
        scores = (
            {
                group: score(result["payload"], truth, ids)
                for group, ids in (("dilute", DILUTE), ("other", other), ("all", [*DILUTE, *other]))
            }
            if valid
            else None
        )
        readouts.append(
            {
                **cell,
                "valid": valid,
                "failure": result["failure"],
                "scores": scores,
                **{
                    k: result.get(k)
                    for k in ("elapsed_s", "usage", "numerics_attempts", "method_resources")
                },
            }
        )
    contrast = None
    if all(r["valid"] for r in readouts):
        arms = {r["readout_arm"]: r["scores"] for r in readouts}
        contrast = {}
        for metric in (*METRICS, "macro"):
            diffs = {
                group: arms["Aligned"][group]["metrics"][metric]["mae"]
                - arms["Opaque"][group]["metrics"][metric]["mae"]
                for group in ("dilute", "other")
            }
            contrast[metric] = {
                "dilute_difference": diffs["dilute"],
                "other_difference": diffs["other"],
                "interaction": diffs["dilute"] - diffs["other"],
            }
    report = {
        "evidence_class": "development_pair_check",
        "planned_sessions": 2,
        "terminal_sessions": 2,
        "valid_sessions": sum(r["valid"] for r in readouts),
        "history_id": cells[0]["history_id"],
        "world": cells[0]["world"],
        "full_design_sessions": 30,
        "automatic_continuation": False,
        "readouts": readouts,
        "contrast": contrast,
        "scientific_scope": "One fixed history; not the five-world primary effect.",
    }
    write(root / "pair-summary.json", report)
    lines = [
        "# First EQ fixed-evidence pair",
        "",
        "Development check: two sessions, one history.",
        f"Sealed 2/2; valid {report['valid_sessions']}/2. Other cells are not launched.",
        "",
        "| Readout | Valid | Seconds | Calculator attempts | Dilute MAE | Other MAE |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in readouts:
        values = [
            f"{row['scores'][group]['metrics']['macro']['mae']:.6f}" if row["scores"] else "NA"
            for group in ("dilute", "other")
        ]
        lines.append(
            f"| {row['readout_arm']} | {row['valid']} | {row['elapsed_s']} | "
            f"{row['numerics_attempts']} | " + " | ".join(values) + " |"
        )
    lines += [
        "",
        "Failures: " + encoded([r["failure"] for r in readouts if r["failure"]]),
        "",
        "Macro contrast: " + encoded(contrast["macro"] if contrast else None),
        "",
        "This checks the real execution path; it does not estimate a five-world effect.",
    ]
    (root / "pair-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def analyze(root):
    check(root, environment=False)
    design = read(root / "design.json")
    results = {
        c["id"]: read(root / "sessions" / c["id"] / "result.json")
        for c in design["cells"]
        if (root / "sessions" / c["id"] / "result.json").exists()
    }
    if len(results) != 30 and not (root / "stopped.json").exists():
        raise ValueError("score only after all thirty terminals or an explicit infrastructure stop")
    truths = read(root / "private" / "truth.json")
    other = [q["query_id"] for q in design["queries"] if q["query_id"] not in DILUTE]
    scored, pairs = {}, []
    for cell in design["cells"]:
        result = results.get(cell["id"])
        if result and result["valid"]:
            if not prediction_validation(result["payload"], design)["valid"]:
                raise ValueError("sealed valid response no longer validates")
            scored[cell["id"]] = {
                group: score(result["payload"], truths[cell["world"]], ids)
                for group, ids in (("dilute", DILUTE), ("other", other), ("all", [*DILUTE, *other]))
            }
    for number in range(1, 16):
        cells = [c for c in design["cells"] if c["history_id"] == f"H{number:02d}"]
        values = {c["readout_arm"]: scored.get(c["id"]) for c in cells}
        contrast = None
        if all(values.values()):
            contrast = {}
            for metric in (*METRICS, "macro"):
                diff = {
                    group: values["Aligned"][group]["metrics"][metric]["mae"]
                    - values["Opaque"][group]["metrics"][metric]["mae"]
                    for group in ("dilute", "other")
                }
                contrast[metric] = {
                    "dilute_difference": diff["dilute"],
                    "other_difference": diff["other"],
                    "interaction": diff["dilute"] - diff["other"],
                }
        pairs.append(
            {
                "history_id": f"H{number:02d}",
                "world": cells[0]["world"],
                "valid": contrast is not None,
                "contrast": contrast,
                "readouts": values,
            }
        )
    worlds = []
    for world in WORLD_IDS:
        valid = [p["contrast"] for p in pairs if p["world"] == world and p["valid"]]
        worlds.append(
            {
                "world": world,
                "valid_pairs": len(valid),
                "planned_pairs": 3,
                "contrast": mean_contrasts(valid) if len(valid) == 3 else None,
                "available_pair_description": mean_contrasts(valid) if valid else None,
            }
        )
    complete = [w["contrast"] for w in worlds if w["contrast"] is not None]
    report = {
        "evidence_class": design["evidence_class"],
        "planned_sessions": 30,
        "terminal_sessions": len(results),
        "valid_sessions": len(scored),
        "unstarted_sessions": sum(
            not (root / "sessions" / c["id"] / "started.json").exists() for c in design["cells"]
        ),
        "planned_pairs": 15,
        "valid_pairs": sum(p["valid"] for p in pairs),
        "planned_worlds": 5,
        "complete_worlds": len(complete),
        "primary": mean_contrasts(complete) if len(complete) == 5 else None,
        "complete_world_description": mean_contrasts(complete) if complete else None,
        "failures": [
            {"id": key, "failure": r["failure"]} for key, r in results.items() if not r["valid"]
        ],
        "pairs": pairs,
        "worlds": worlds,
        "resources": [
            {
                "id": key,
                **{
                    k: r.get(k)
                    for k in ("elapsed_s", "method_resources", "usage", "numerics_attempts")
                },
            }
            for key, r in results.items()
        ],
        "additional_experiments_triggered": False,
    }
    write(root / "summary.json", report)
    lines = [
        "# EQ fixed-evidence readout",
        "",
        f"Evidence: {design['evidence_class']}; fixed 30 sessions / 15 pairs / 5 worlds.",
        f"Terminal {len(results)}/30; valid {len(scored)}/30; "
        f"paired {report['valid_pairs']}/15; complete worlds {len(complete)}/5.",
        "",
        "Positive A-O means larger Aligned error. "
        "Interaction alone does not establish a sign reversal.",
        "",
        "| World | Valid pairs | Dilute A-O | Other A-O | Interaction |",
        "|---|---:|---:|---:|---:|",
    ]
    for w in worlds:
        c = w["contrast"]["macro"] if w["contrast"] else None
        fields = [
            f"{c[k]:.6f}" if c else "NA"
            for k in ("dilute_difference", "other_difference", "interaction")
        ]
        lines.append(f"| {w['world']} | {w['valid_pairs']}/3 | " + " | ".join(fields) + " |")
    lines += [
        "",
        "Primary macro: " + encoded(report["primary"]["macro"] if report["primary"] else None),
        "",
        "All response-specific MAEs, interval measures, paired values, "
        "failures and resources are in summary.json.",
        "",
        "Failures: " + encoded(report["failures"]),
        "",
        "Block closes without outcome-driven additions.",
    ]
    (root / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("prepare", "check", "run", "run-pair", "analyze", "analyze-pair")
    )
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, default=EXPORT)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_relative_to(ROOT / "runs"):
        parser.error("readout inputs and raw provider outputs must remain under ignored runs/")
    try:
        if args.command == "prepare":
            prepare(args.source_root.resolve(), root)
        elif args.command == "check":
            print(encoded(check(root)))
        elif args.command in {"run-pair", "analyze-pair"}:
            result = run(root, pair_only=True) if args.command == "run-pair" else analyze_pair(root)
            print(
                encoded(
                    {
                        key: result[key]
                        for key in ("planned_sessions", "terminal_sessions", "valid_sessions")
                    }
                )
            )
        else:
            result = run(root) if args.command == "run" else analyze(root)
            print(
                encoded(
                    {
                        key: result[key]
                        for key in (
                            "terminal_sessions",
                            "valid_sessions",
                            "valid_pairs",
                            "complete_worlds",
                        )
                    }
                )
            )
    except (ValueError, FileNotFoundError) as exc:
        parser.exit(2, str(exc) + "\n")


if __name__ == "__main__":
    main()
