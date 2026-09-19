"""English EC/PA budget-by-world matrix, with a persistent sequential result ledger."""

from __future__ import annotations

import argparse
import json
import math
import re
import tempfile
import threading
import time
from pathlib import Path

import gymnasium as gym
from scripts import run_work_ii_ec_dual_goal_trial as ec
from scripts import run_work_ii_pa_single_trial as pa
from scripts.recover_work_ii_ec_pa_network import effective_row, recover, recovery_kind
from scripts.run_work_ii_astra_single_trial import read, write

from chemworld.agents.experiment_codex_mcp import ChemWorldMCPServer
from chemworld.data.logging import load_jsonl
from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent

VERSION = "ec-pa-five-world-budget-matrix-en-v1"
ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r"[\u3400-\u9fff]")


def worlds(system):
    name = (
        "experiment_1_ec_qualification_repair_v1.0.2.json"
        if system == "EC"
        else "experiment_1_pa_qualification_v1.0.1.json"
    )
    rows = read(ROOT / "configs/benchmark" / name)["worlds"]["qualification"]
    return [
        {
            "world_id": r["world_id"],
            "world_seed": r["world_seed"],
            "world_interventions": r.get("world_interventions", []),
        }
        for r in rows
    ]


def units(*, include_ps=False):
    result = []
    # Fixed order: world, budget, task, arm. Arms rotate with world to vary wall-clock order.
    for wi in range(5):
        arms = list(pa.ARMS[wi % 3 :] + pa.ARMS[: wi % 3])
        for budget in (12, 24):
            for system, goal in (("EC", "discovery"), ("EC", "optimization"), ("PA", "discovery")):
                world = worlds(system)[wi]
                for arm in arms:
                    result.append(
                        {
                            "system": system,
                            "world": world,
                            "goal": goal,
                            "locus": "E",
                            "arm": arm,
                            "budget": budget,
                        }
                    )
    if include_ps:
        # EC has executable matched P/S priors. PA P/S need a separate public-prior design.
        for locus in ("P", "S"):
            for goal in ec.GOALS:
                for arm in pa.ARMS:
                    result.append(
                        {
                            "system": "EC",
                            "world": worlds("EC")[0],
                            "goal": goal,
                            "locus": locus,
                            "arm": arm,
                            "budget": 12,
                        }
                    )
    for row in result:
        row["unit_id"] = (
            f"{row['world']['world_id']}-B{row['budget']}-{row['goal']}-{row['locus']}-{row['arm']}"
        )
    return result


def public_entry(system, world, budget, arm):
    """Check the real published research contract and material tool without a provider."""
    module = ec if system == "EC" else pa
    material = (
        ec.priors("E", arm, world_id=world["world_id"], world_seed=world["world_seed"])[0]
        if system == "EC"
        else pa.arm_material_information(arm)
    )
    kwargs = {
        "task_id": module.TASK,
        "world_split": "public-test",
        "seed": world["world_seed"],
        "material_information": material,
        "world_interventions": world["world_interventions"],
        "budget": 30 * budget,
        "budget_override": 30 * budget,
        "episode_mode_override": "campaign",
        "campaign_resource_card": module.resource_card(budget),
    }
    if system == "EC":
        kwargs.update(
            electrochemical_material_family_id="nominal-prior-latent-v2",
            electrochemical_workflow_mode="autonomous_open_v1",
            scoring_contract_id="electrochemical-s0-balanced-efficiency-v2",
        )
    else:
        kwargs["scoring_contract_id"] = "partition-s0-extraction-efficiency-v3"
    env = gym.make("ChemWorld", **kwargs)
    try:
        env.reset(seed=world["world_seed"])
        with tempfile.TemporaryDirectory(prefix="chemworld-research-") as temporary:
            home = Path(temporary)
            common = {
                "batches": budget,
                "home_root": home,
                "output": home,
                "workspace": home / "laboratory",
                "role_id": "free_research",
            }
            agent = (
                ec.FreeResearchAgent(goal="discovery", **common)
                if system == "EC"
                else pa.PAAgent(arm=arm, world=world, **common)
            )
            try:
                agent.reset(env.unwrapped.task_info(), 0)
                agent.workspace.start_session(
                    session_id="entry-check", response_timeout_s=10, session_scope="campaign"
                )
                reply = ChemWorldMCPServer(agent.workspace.root)._call_tool(
                    "material_information", {}
                )
                if reply.get("isError"):
                    raise RuntimeError("material_information tool failed")
                payload = json.loads(reply["content"][0]["text"])
                contract = agent._task_contract
                if contract["study_budget"]["complete_batches"] != budget:
                    raise RuntimeError("public batch budget mismatch")
                serialized = json.dumps(payload).lower()
                for forbidden in (
                    '"arm"',
                    "anonymous_misindexed_properties",
                    '"arm_label"',
                    "world_seed",
                    "ethanol",
                    "acetonitrile",
                    "toluene",
                    "cas_number",
                ):
                    if forbidden in serialized:
                        raise RuntimeError(f"public material exposure: {forbidden}")
                if CJK.search(
                    json.dumps(
                        [payload, contract, module.source_system(budget)], ensure_ascii=False
                    )
                ):
                    raise RuntimeError("non-English public input")
                dossier = payload["material_information"]["dossier"]
                if (dossier is None) != (arm == "Opaque"):
                    raise RuntimeError("prior dossier availability mismatch")
                return {
                    "passed": True,
                    "world": world["world_id"],
                    "budget": budget,
                    "arm": arm,
                    "material_reply": payload,
                    "study_budget": contract["study_budget"],
                }
            finally:
                agent.close()
    finally:
        env.close()


def prepare_reference(system, world, folder, progress):
    module = ec if system == "EC" else pa
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "design.json", {"world_config": world, "queries": module.queries()})
    if system == "EC":
        results = []
        for query in ec.queries():
            progress.update(stage="reference", unit=f"{world['world_id']}/{query['query_id']}")
            result = ec.reference_run(folder / query["query_id"], query["actions"], world=world)
            results.append(result)
            write(folder / "partial-results.json", results)
            if (
                result["failure"]
                or result["rollbacks"]
                or len(result["batches"]) != 1
                or not result["exact_replay"].get("verified")
            ):
                raise RuntimeError(f"reference failed: {world['world_id']}/{query['query_id']}")
        result = {
            "passed": True,
            "completed_batches": 12,
            "operations": sum(r["operation_attempts"] for r in results),
            "replay_operations": sum(r["exact_replay"]["checked_steps"] for r in results),
            "truth": {
                q["query_id"]: r["batches"][0]["metrics"]
                for q, r in zip(ec.queries(), results, strict=True)
            },
        }
    else:
        truth = []
        agent = _FrozenTruthReplayAgent([a for q in pa.queries() for a in q["actions"]])
        pa.physics(agent, folder / "reference.jsonl", truth=truth, world=world)
        records = load_jsonl(folder / "reference.jsonl")
        replay = ec.replay_with_progress(
            records, world["world_id"], world_interventions=world.get("world_interventions")
        )
        measurements = [r for r in pa.observations(records) if r["instrument"] == "hplc"]
        result = {
            "completed_batches": len(ec.summaries(records)),
            "operations": len(records),
            "exact_replay": replay,
            "replay_operations": replay["checked_steps"],
            "measurements": measurements,
            "truth": dict(zip([q["query_id"] for q in pa.queries()], truth, strict=True)),
        }
        result["passed"] = (
            result["completed_batches"] == len(measurements) == 12
            and replay.get("verified") is True
            and all(r["transaction_status"] == "committed" for r in records)
            and all(abs(sum(t[k] for k in pa.METRICS) - 1) <= 1e-8 for t in truth)
            and all(
                m["before_phase_removal"]
                and all(
                    m["observed_mask"].get(k) is True and math.isfinite(m["values"][k])
                    for k in pa.METRICS
                )
                for m in measurements
            )
        )
    write(folder / "reference-result.json", result)
    if not result["passed"]:
        raise RuntimeError(f"reference failed: {world['world_id']}")
    return result


def source_row(unit, result):
    is_ec = unit["system"] == "EC"
    source = result if is_ec else result.get("source", {})
    batches = source.get("batches", [])
    posttests = result.get("posttests", {})
    accounting = pa.token_accounting(
        {"source": {"usage": result.get("source_usage", {})}, "posttests": posttests}
        if is_ec
        else result
    )
    retest = result.get("recommendation_retest") or {}
    return {
        **unit,
        "status": result["status"],
        "source_status": result.get("source_status") if is_ec else source.get("status"),
        "completed_batches": len(batches),
        "operations": source.get("operations", 0),
        "posttests_completed": sum(
            bool(t.get("payload")) and not t.get("failure") for t in posttests.values()
        ),
        "exact_replay": source.get("exact_replay", {}),
        "failure": result.get("failure"),
        "source_failure": result.get("source_failure") if is_ec else source.get("failure"),
        "interruption": result.get("interruption"),
        "prediction_evaluation": result.get("prediction_evaluation"),
        "token_accounting": accounting,
        "elapsed_s": result.get("elapsed_s"),
        "retest_batches": len(retest.get("batches", [])),
        "retest_operations": retest.get("operation_attempts", 0),
        "retest_replay": retest.get("exact_replay"),
        "english_output": (
            not bool(
                CJK.search(
                    json.dumps([t.get("payload") for t in posttests.values()], ensure_ascii=False)
                )
            )
        )
        if any(t.get("payload") for t in posttests.values())
        else None,
    }


def export_source(unit, result, folder, out, design):
    """Scientific outputs and public measurements only; raw provider files remain in runs/."""
    out.mkdir(parents=True, exist_ok=True)
    source_folder = folder if unit["system"] == "EC" else folder / "source"
    path = source_folder / "trajectory.jsonl"
    records = load_jsonl(path) if path.exists() else []
    public_records = [
        {
            k: r[k]
            for k in (
                "step",
                "experiment_index",
                "action",
                "transaction_status",
                "rollback_reason",
                "instrument",
                "processed_estimate",
                "observed_mask",
            )
            if k in r
        }
        for r in records
    ]
    row = source_row(unit, result)
    write(out / "summary.json", row)
    write(out / "public-trajectory.json", public_records)
    lines = [
        f"# {unit['unit_id']}",
        "",
        "Development experiment; one independent source session.",
        "",
        f"Status: {row['status']}; completed batches: {row['completed_batches']}/{unit['budget']}; "
        f"posttests: {row['posttests_completed']}/3.",
        "",
        "## Research assignment",
        "",
        design["system"],
        "",
        design["goal"],
        "",
        "## Batch outcomes",
        "",
        "| Batch | Final measured outcomes |",
        "| --- | --- |",
    ]
    source = result if unit["system"] == "EC" else result.get("source", {})
    for batch in source.get("batches", []):
        lines.append(f"| {batch['lifecycle_index']} | {json.dumps(batch['metrics'])} |")
    lines += [
        "",
        "Public operations and purchased measurements: [trajectory](public-trajectory.json).",
    ]
    for stage in ("K1", "Q", "K2"):
        turn = result.get("posttests", {}).get(stage, {})
        lines += ["", f"## {stage}", "", "### Question", "", design[stage], "", "### Response", ""]
        payload = turn.get("payload")
        if payload and isinstance(payload, dict) and "report" in payload:
            lines.append(payload["report"])
        else:
            lines += ["```json", json.dumps(payload, ensure_ascii=False, indent=2), "```"]
        if turn.get("failure"):
            lines += ["", f"Failure: {turn['failure']}"]
    lines += [
        "",
        "## Evaluation and resource use",
        "",
        "```json",
        json.dumps(row, ensure_ascii=False, indent=2),
        "```",
        "",
    ]
    (out / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return row


def run(
    root,
    report,
    *,
    include_ps=False,
    prepare_only=False,
    recover_network=False,
    recover_host_unit=None,
    interrupted_home=None,
    host_reboot_time=None,
):
    planned = units(include_ps=include_ps)
    prompts = {
        s: {
            "K1": m.K1,
            "Q": ec.prediction_question(ec.queries()) if s == "EC" else pa.question("Q"),
            "K2": m.K2,
        }
        for s, m in (("EC", ec), ("PA", pa))
    }
    if CJK.search(json.dumps(prompts, ensure_ascii=False)):
        raise ValueError("new participant questions must be English")
    design = {
        "version": VERSION,
        "provider": ec.PROVIDER,
        "units": planned,
        "questions": prompts,
        "development_only": True,
        "ec_system": {str(n): ec.source_system(n) for n in (12, 24)},
        "pa_system": {str(n): pa.source_system(n) for n in (12, 24)},
        "queries": {"EC": ec.queries(), "PA": pa.queries()},
        "stop_rule": "No retries; stop on reference/replay defects or pre-action source failure.",
        "pa_ps": "Not queued: public P/S priors require a separate applicability design.",
    }
    root.mkdir(parents=True, exist_ok=True)
    report.mkdir(parents=True, exist_ok=True)
    if (root / "design.json").exists():
        if read(root / "design.json") != design:
            raise RuntimeError("saved matrix differs; never alter a started block")
    else:
        write(root / "design.json", design)
    started = time.monotonic()
    progress = {"stage": "entry", "completed_sources": 0, "planned_sources": len(planned)}
    state = {
        "status": "running",
        "results": [{**u, "status": "not_started"} for u in planned],
        "references": {},
        "entries": [],
        "failure": None,
    }
    if (root / "summary.json").exists():
        state = read(root / "summary.json")
        if state["status"] == "stopped" and recover_network:
            if (
                not (state.get("failure") or {})
                .get("message", "")
                .startswith("source startup/replay failure:")
            ):
                raise RuntimeError("this stop is not an eligible source network failure")
            state.setdefault("runtime_incidents", []).append(state["failure"])
            state["failure"] = None
        elif state["status"] not in ("prepared", "running"):
            raise RuntimeError("completed or stopped matrix cannot be automatically restarted")
        state["status"] = "running"
    if recover_network:
        amendment = {
            "authorization": "2026-09-19 user requested network-failure retries",
            "max_recovery_attempts_per_source": 1,
            "boundary": "posttests after intact source, or fresh source after zero actions",
            "original_design_unchanged": True,
        }
        if not (root / "network-recovery-amendment.json").exists():
            write(root / "network-recovery-amendment.json", amendment)
        state["network_recovery_policy"] = amendment

    def save():
        rows = state["results"]
        effective = [effective_row(r) for r in rows]
        attempted = [r for r in rows if r["status"] in ("completed", "failed")]
        recoveries = [
            r.get("infrastructure_recovery") or r.get("network_recovery")
            for r in rows
            if r.get("infrastructure_recovery") or r.get("network_recovery")
        ]
        successful = [r for r in effective if r["status"] == "completed"]
        total_elapsed = sum(r.get("elapsed_s") or 0 for r in successful)
        progress.update(
            completed_sources=len(attempted),
            elapsed_s=time.monotonic() - started,
            sources_per_hour=len(successful) / total_elapsed * 3600 if total_elapsed else None,
            eta_s=total_elapsed / len(successful) * (len(rows) - len(attempted))
            if successful
            else None,
        )
        state.update(
            version=VERSION,
            development_only=True,
            formal_result=False,
            progress=dict(progress),
            planned_sources=len(rows),
            planned_source_batches=sum(r["budget"] for r in rows),
            attempted_sources=len(attempted),
            completed_sources=len(successful),
            first_attempt_completed_sources=sum(r["status"] == "completed" for r in rows),
            source_batches=sum(r.get("completed_batches", 0) for r in rows)
            + sum(r["new_source_batches"] for r in recoveries),
            effective_source_batches=sum(r.get("completed_batches", 0) for r in effective),
            posttests_completed=sum(r.get("posttests_completed", 0) for r in effective),
            reference_batches=sum(r["completed_batches"] for r in state["references"].values()),
            reference_operations=sum(r["operations"] for r in state["references"].values()),
            extra_verification_operations=sum(
                i.get("additional_replay_operations", 0)
                for i in state.get("preparation_incidents", [])
            )
            + sum(
                r.get("interruption", {}).get("additional_replay_operations", 0)
                for r in rows
                if r.get("interruption")
            ),
            retries=len(recoveries),
            host_recoveries=sum(
                r["kind"] == "fresh_source_after_host_interruption" for r in recoveries
            ),
            additional_source_attempts=sum(r["new_source_attempts"] for r in recoveries),
            additional_posttest_attempts=sum(r["new_posttest_attempts"] for r in recoveries),
        )
        write(root / "summary.json", state)
        # Public ledger omits reference answers and material packets until source completion.
        public = {k: v for k, v in state.items() if k not in ("references", "entries")}
        write(report / "summary.json", public)
        lines = [
            "# EC and PA: five worlds, two budgets, three prior arms",
            "",
            "[Fixed design and preparation incident](../../WORK_II_EC_PA_FIVE_WORLD_NOTE.md).",
            "",
            f"Status: **{state['status']}**. Model: GPT-5.6 Sol / medium. English protocol.",
            "",
            f"Sources attempted: {len(attempted)}/{len(rows)}; "
            f"completed: {state['completed_sources']}. "
            f"Current logical-source batches: {state['effective_source_batches']}/"
            f"{state['planned_source_batches']}; "
            f"posttests: {state['posttests_completed']}/{3 * len(rows)}.",
            f"Physical source final assays across all attempts: {state['source_batches']}. "
            "Interrupted and replacement attempts are both charged.",
            "",
            f"Reference batches: {state['reference_batches']}/120; operations: "
            f"{state['reference_operations']}/900. "
            "Exact replay and EC recommendation retests are additional.",
            "Additional verification operations after preparation corrections: "
            f"{state['extra_verification_operations']}.",
            "",
            "E: 90 sources / 1,620 planned batches / 270 posttests. "
            "The EC P/S pilot, if enabled, follows all E sources: "
            "12 sources / 144 batches / 36 posttests.",
            "",
            f"First-attempt completions: {state['first_attempt_completed_sources']}; "
            f"infrastructure recovery attempts: {state['retries']} "
            f"(host-reboot replacements: {state['host_recoveries']}). "
            f"Additional source attempts: {state['additional_source_attempts']}; "
            f"additional posttest attempts: {state['additional_posttest_attempts']}. "
            "Completion totals above include separately recorded recoveries. "
            "The table retains first-attempt outcomes.",
            "",
            "| Unit | Status | Batches | Posttests | English output |",
            "| --- | --- | ---: | ---: | --- |",
        ]
        for row in rows:
            label = (
                f"[{row['unit_id']}]({row['unit_id']}/REPORT.md)"
                if row.get("exported")
                else row["unit_id"]
            )
            lines.append(
                f"| {label} | {row['status']} | "
                f"{row.get('completed_batches', 0)}/{row['budget']} | "
                f"{row.get('posttests_completed', 0)}/3 | {row.get('english_output', '')} |"
            )
            recovery = row.get("infrastructure_recovery") or row.get("network_recovery")
            if recovery:
                restored = recovery["row"]
                lines.append(
                    f"| ↳ [Infrastructure recovery]({recovery['report_path']}) | "
                    f"{restored['status']} ({recovery['kind']}) | "
                    f"{restored['completed_batches']}/{row['budget']} | "
                    f"{restored['posttests_completed']}/3 | {restored['english_output']} |"
                )
        lines += [
            "",
            "## Live progress",
            "",
            "```json",
            json.dumps(progress, indent=2),
            "```",
            "",
            "All failures remain in the planned denominator. "
            "No result-based retries or substitutions. "
            "Single observations per cell do not establish general budget effects.",
            "",
        ]
        if state.get("failure"):
            lines += ["## Failure", "", str(state["failure"]), ""]
        (report / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    stopped = threading.Event()

    def heartbeat():
        while not stopped.wait(30):
            live = {"heartbeat": dict(progress), "elapsed_s": time.monotonic() - started}
            write(root / "progress.json", live)
            print(json.dumps(live, default=str), flush=True)

    worker = threading.Thread(target=heartbeat, daemon=True)
    worker.start()

    def repair_network(index, unit, result, folder, source_design):
        row = state["results"][index]
        host_restart = unit["unit_id"] == recover_host_unit
        if (recover_network or host_restart) and not (
            row.get("network_recovery") or row.get("infrastructure_recovery")
        ):
            recovery = recover(
                root,
                report,
                unit,
                result,
                folder,
                source_design,
                state["references"][unit["world"]["world_id"]]["truth"],
                progress,
                host_restart=host_restart,
            )
            if recovery:
                row["infrastructure_recovery" if host_restart else "network_recovery"] = recovery
                save()
                # Stop only if transport recovery itself failed; scientific invalidity is retained.
                recovered_result = read(Path(recovery["result_path"]))
                if recovered_result.get("failure"):
                    raise RuntimeError(f"infrastructure recovery failed: {unit['unit_id']}")
        return effective_row(row)

    try:
        if recover_host_unit:
            from scripts.seal_work_ii_ec_host_interruption import seal

            if not interrupted_home or not host_reboot_time:
                raise ValueError(
                    "host recovery requires the retained home and diagnosed reboot time"
                )
            index = next(i for i, u in enumerate(planned) if u["unit_id"] == recover_host_unit)
            unit = planned[index]
            parent = root / "sources" / unit["unit_id"]
            folder = parent / f"{unit['goal']}-{unit['locus']}-{unit['arm']}"
            progress.update(stage="verify_host_interruption", unit=unit["unit_id"])
            if not state["results"][index].get("infrastructure_recovery"):
                if state["results"][index]["status"] not in ("running", "failed"):
                    raise ValueError("cannot replace a completed or unstarted source")
                result = seal(unit, folder, interrupted_home, reboot_time=host_reboot_time)
                state["results"][index] = source_row(unit, result)
                export_source(
                    unit, result, folder, report / unit["unit_id"], read(parent / "design.json")
                )
                state["results"][index]["exported"] = True
                state.setdefault("runtime_incidents", []).append(result["interruption"])
                save()
                repair_network(index, unit, result, folder, read(parent / "design.json"))
        save()
        if not state["entries"]:
            for system in ("EC", "PA"):
                for world in worlds(system):
                    for budget in (12, 24):
                        for arm in pa.ARMS:
                            progress.update(
                                stage="entry",
                                unit=f"{world['world_id']}/{budget}/{arm}",
                                entries_completed=len(state["entries"]),
                                entries_total=60,
                            )
                            state["entries"].append(public_entry(system, world, budget, arm))
                            print(
                                json.dumps({"entry_completed": len(state["entries"]), "total": 60}),
                                flush=True,
                            )
                            save()
        if len(state["entries"]) != 60:
            raise RuntimeError("incomplete entry block; preserve and diagnose before execution")
        for system in ("EC", "PA"):
            for world in worlds(system):
                wid = world["world_id"]
                if wid not in state["references"]:
                    progress.update(stage="reference", unit=wid)
                    state["references"][wid] = prepare_reference(
                        system, world, root / "references" / wid, progress
                    )
                    save()
        if prepare_only:
            state["status"] = "prepared"
            save()
            return state
        if recover_network:
            for index, unit in enumerate(planned):
                row = state["results"][index]
                if row["status"] != "failed":
                    continue
                parent = root / "sources" / unit["unit_id"]
                folder = (
                    parent / f"{unit['goal']}-{unit['locus']}-{unit['arm']}"
                    if unit["system"] == "EC"
                    else parent
                )
                result = read(folder / "result.json")
                repaired = repair_network(index, unit, result, folder, read(parent / "design.json"))
                if not repaired["operations"] or not repaired["exact_replay"].get("verified"):
                    raise RuntimeError(f"source startup/replay failure: {unit['unit_id']}")
        for index, unit in enumerate(planned):
            if state["results"][index]["status"] in ("completed", "failed"):
                continue
            folder = root / "sources" / unit["unit_id"]
            if folder.exists():
                raise RuntimeError(
                    f"partial source retained; no automatic retry: {unit['unit_id']}"
                )
            state["results"][index]["status"] = "running"
            progress.pop("provider_liveness", None)
            progress.update(
                stage="source",
                unit=unit["unit_id"],
                operations=0,
                batches=0,
                planned_batches=unit["budget"],
            )
            save()
            wid = unit["world"]["world_id"]
            if unit["system"] == "EC":
                folder.mkdir(parents=True)
                source_design = {
                    **prompts["EC"],
                    "queries": ec.queries(),
                    "query_version": ec.QUERY_VERSION,
                    "world_config": unit["world"],
                    "batches_per_source": unit["budget"],
                    "system": ec.source_system(unit["budget"]),
                    "goal": ec.GOALS[unit["goal"]],
                }
                write(folder / "design.json", source_design)
                result = ec.run_cell(
                    folder,
                    unit["goal"],
                    unit["locus"],
                    unit["arm"],
                    state["references"][wid]["truth"],
                    progress,
                )
                actual_folder = folder / f"{unit['goal']}-{unit['locus']}-{unit['arm']}"
            else:
                pa.execute(
                    folder,
                    progress,
                    arm=unit["arm"],
                    batches=unit["budget"],
                    world=unit["world"],
                    reference_run=root / "references" / wid,
                )
                result = read(folder / "result.json")
                source_design = read(folder / "design.json")
                actual_folder = folder
            state["results"][index] = source_row(unit, result)
            save()
            export_source(unit, result, actual_folder, report / unit["unit_id"], source_design)
            state["results"][index]["exported"] = True
            save()
            row = repair_network(index, unit, result, actual_folder, source_design)
            if not row["operations"] or not row["exact_replay"].get("verified"):
                raise RuntimeError(f"source startup/replay failure: {unit['unit_id']}")
            if recover_network and recovery_kind(unit, result, actual_folder) is None:
                # A network interruption in a partial physical campaign needs explicit diagnosis.
                from scripts.recover_work_ii_ec_pa_network import network_failure, source_folder

                if (
                    result.get("failure")
                    and network_failure(source_folder(unit, actual_folder) / "source-stdout.jsonl")
                    and not state["results"][index].get("network_recovery")
                ):
                    raise RuntimeError(f"partial source network failure: {unit['unit_id']}")
        state["status"] = "completed"
        progress.update(stage="completed")
        save()
    except BaseException as exc:
        state["status"] = "stopped"
        state["failure"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "progress": dict(progress),
        }
        save()
        raise
    finally:
        stopped.set()
        worker.join(timeout=1)
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--include-ec-ps", action="store_true")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--recover-network", action="store_true")
    parser.add_argument("--recover-host-interruption", dest="recover_host_unit")
    parser.add_argument("--interrupted-home", type=Path)
    parser.add_argument("--host-reboot-time")
    args = parser.parse_args()
    run(
        args.output.resolve(),
        args.report.resolve(),
        include_ps=args.include_ec_ps,
        prepare_only=args.prepare_only,
        recover_network=args.recover_network,
        recover_host_unit=args.recover_host_unit,
        interrupted_home=args.interrupted_home,
        host_reboot_time=args.host_reboot_time,
    )


if __name__ == "__main__":
    main()
