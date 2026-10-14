"""Fixed EQ research-opportunity comparison; see W2-257 experiment note."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

from scripts import run_research_formation as pool
from scripts import run_work_ii_eq_bounded_equilibrium_v2 as eq
from scripts.run_paper_case_notebooks import ROOT, case_folder, emit, read, write
from scripts.run_work_ii_study_b import _prepare_codex_home

from chemworld.agents.campaign_notebook import with_notebook
from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS

NOTE = "workstreams/flagship_tasks/WORK_II_INQUIRY_COMPLETION_20261015.md"
MODE = "eq-research-opportunity-30"
ARMS = ("Research", "NoResearch")
STAGES = eq.POSTTEST_STAGES
K1 = """Using only the information available to you, submit a complete scientific account in English
of this bounded aqueous-equilibrium world: loading, volume or dilution, pH, acid dissociation,
precipitation, possible relationships, uncertainty, supported ranges and competing explanations.
Distinguish public background information, actual observations, inference and conjecture. Cite
batch numbers and values only if you actually observed them; if you have no experimental
observations, say so explicitly and do not invent evidence. No additional laboratory access.
Return the JSON report field. Prediction questions will be revealed only after this report seals."""
Q = """Using only available information and your sealed K1 account, predict the final outcomes
of these twelve independent new batches. Each starts independently from the same world.
Return all requested point estimates, 80% prediction intervals and substantive English rationales.
Account for model and observation uncertainty. No experiments or revisions to K1 are permitted.
equilibrium_confidence is an environment diagnostic, not your uncertainty or a task score."""
K2 = """K1 and Q are sealed; no prediction truth or scores have been shown. In English discuss:
1. What relationships are supported, contradicted or untested by the information available?
2. Which actual observations changed your account, if any? Explicitly state if there were none.
3. Which competing explanations remain distinguishable or unresolved?
4. What single legal experiment would you choose next, and how would possible results differ?
5. What are the limits of the available evidence for the characterization objective?
6. Which Q forecasts are least reliable or inconsistent with your stated scope?
7. What limits generalization to new loading, dilution, paths and worlds?
Do not invent experiments, run new ones or rewrite K1/Q. Return the JSON report field."""
EQS = eq.EQS.replace(
    "using only evidence already acquired during the source campaign",
    "using only information available to you; explicitly state when there are no observations",
).replace("Cite actual batches", "Cite actual batches only if observed")
EVALUATION_INSTRUCTIONS = (
    "Evaluate the bounded aqueous-equilibrium world using only information available in this "
    "conversation. No new laboratory experiments, network, filesystem, repository or hidden-truth "
    "access. Only public_numerics.calculate is available. All free text must be English. "
    "Do not invent observations or rewrite earlier sealed outputs."
)


def schedule():
    rows = []
    for r, repeat in enumerate(pool.REPEATS):
        worlds = list(range(1, 6))
        worlds = worlds[2 * r :] + worlds[: 2 * r]
        for w in worlds:
            arms = ARMS if (r + w) % 2 else ARMS[::-1]
            rows.extend(
                {
                    "repeat": repeat,
                    "id": f"EQ-W{w:02d}-{arm}",
                    "system": "EQ",
                    "world": f"W{w:02d}",
                    "arm": "Opaque",
                    "opportunity": arm,
                    "cell": f"EQ-W{w:02d}--Opaque",
                    "model": "gpt-5.6-sol",
                    "batches": 12 if arm == "Research" else 0,
                }
                for arm in arms
            )
    return rows


def public_context(agent, current_packet):
    """The exact public contract and state; never read simulator or evaluator files."""
    return {
        "task_contract": copy.deepcopy(agent._task_contract),
        "initial_public_state": copy.deepcopy(current_packet),
        "material_information": read(
            agent.workspace.reference_directory / "material_information.json"
        ),
    }


class InitialStateCapturedError(Exception):
    """Stop before provider launch and before any laboratory action."""


class CaptureInitialState(eq.EqFreeResearchAgent):
    def _start_session(self, current_packet):
        self.captured = public_context(self, current_packet)
        raise InitialStateCapturedError


class ResearchAgent(with_notebook(eq.EqFreeResearchAgent)):
    def _start_session(self, current_packet):
        context = public_context(self, current_packet)
        write(self.output / "initial-public-context.json", context)
        original = self._process_factory

        def inline(command, prompt, cwd):
            return original(
                command, prompt + "\nCommon public background:\n" + json.dumps(context), cwd
            )

        self._process_factory = inline
        try:
            return super()._start_session(current_packet)
        finally:
            self._process_factory = original


def capture_initial(config, cell, folder):
    folder.mkdir(parents=True, exist_ok=False)
    output = folder / "source"
    output.mkdir()
    agent = CaptureInitialState(
        goal=cell["goal"],
        home_root=folder / "unused-home",
        output=output,
        workspace=folder / "laboratory",
        initial_world_model=None,
    )
    try:
        eq.physics(
            agent,
            folder / "empty-trajectory.jsonl",
            config=config,
            world=eq.world_by_id(config, cell["world_id"]),
            observation_seed=eq.deterministic_seed("eq-source-v2", cell["cell_id"]),
            observation_namespace=f"work-ii-eq-v2-source-{cell['cell_id'].lower()}",
        )
    except InitialStateCapturedError:
        pass
    finally:
        agent.close()
    trajectory = folder / "empty-trajectory.jsonl"
    if trajectory.exists() and trajectory.stat().st_size:
        raise RuntimeError("Initial public-state capture executed an action")
    if not hasattr(agent, "captured"):
        raise RuntimeError("Initial public state not captured")
    write(folder / "initial-public-context.json", agent.captured)
    return agent.captured


def posttest(agent, folder, private_folder, stage, thread_id, progress, query_rows):
    workspace = agent.home_root / "followup"
    workspace.mkdir(parents=True, exist_ok=True)
    schema = workspace / f"{stage}-schema.json"
    write(schema, eq.posttest_schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(EVALUATION_INSTRUCTIONS, encoding="utf-8")
    message = {"K1": K1, "Q": Q, "K2": K2, "EQS": EQS}[stage]
    if stage == "Q":
        message += "\n" + json.dumps(query_rows)
    if thread_id is None:
        message = (
            "You have no laboratory observations. The following is the common initial public "
            "background for the characterization task. Laboratory action budgets describe the "
            "research protocol; no actions are available in this evaluation.\n"
            + json.dumps(agent.initial_public_context)
            + "\n"
            + message
        )
    audit = private_folder / f"{stage}-numerics.jsonl"
    command = eq.provider_shared.build_command(
        eq.PROVIDER,
        schema,
        workspace,
        audit=audit,
        thread_id=thread_id,
        provider_retries=0,
    )
    command += [
        "-c",
        "mcp_servers.chemworld_lab.enabled=false",
        "-c",
        f"mcp_servers.chemworld_lab.command={json.dumps(sys.executable)}",
        "-c",
        "mcp_servers.research_notebook.enabled=false",
        "-c",
        f"model_instructions_file={json.dumps(instructions.as_posix())}",
    ]
    raw = eq.shared.launch(
        command,
        message,
        workspace,
        agent.followup_environment,
        private_folder / stage,
        1200,
        True,
        audit,
        {**progress, "phase": stage},
        numerics_budget=FOLLOWUP_NUMERICS,
    )
    write(private_folder / stage / "receipt.json", raw)
    if thread_id and raw.get("thread_id") != thread_id:
        raise RuntimeError("Evaluation thread changed")
    agent.last_thread_id = raw.get("thread_id")
    result = {
        "payload": raw.get("payload"),
        "failure": raw.get("failure") or (None if raw.get("payload") else "missing_payload"),
        "elapsed_s": raw.get("elapsed_s"),
        "method_resources": raw.get("method_resources"),
    }
    write(folder / "sealed" / f"{stage}.json", result)
    return result


def no_research(root, config, cell, progress):
    folder = root / "sources" / cell["cell_id"]
    private = eq.v1.create_cell_folders(folder)
    context = capture_initial(config, cell, private / "initial-state")
    home = private / "home"
    home.mkdir()
    agent = SimpleNamespace(
        home_root=home,
        followup_environment=_prepare_codex_home(home, eq.PROVIDER),
        initial_public_context=context,
        last_thread_id=None,
    )
    started = time.monotonic()
    result = {
        "cell_id": cell["cell_id"],
        "world_id": cell["world_id"],
        "arm": "Opaque",
        "goal": cell["goal"],
        "status": "retained_nonconforming",
        "failure": None,
        "source_status": "not_applicable",
        "operations": 0,
        "batches": [],
        "rollbacks": [],
        "posttests": {},
        "posttest_validation": {},
        "source_usage": None,
    }
    write(folder / "public-input-binding.json", context)
    for stage in STAGES:
        progress.update(phase=stage)
        turn = posttest(
            agent, folder, private, stage, agent.last_thread_id, progress, eq.queries(config)
        )
        result["posttests"][stage] = turn
        result["posttest_validation"][stage] = eq.validate_posttest(
            stage, turn["payload"], eq.queries(config)
        )
        if turn["failure"] or not result["posttest_validation"][stage]["valid"]:
            break
    result["posttest_chain_sealed"] = all(
        result["posttest_validation"].get(s, {}).get("valid") is True
        and not result["posttests"][s]["failure"]
        for s in STAGES
    )
    if result["posttest_chain_sealed"]:
        result["status"] = "completed"
    result["elapsed_s"] = time.monotonic() - started
    write(folder / "RESULT.json", result)
    return result


def prepare(root):
    config = eq.load_config()
    eq.validate_design(config)
    from scripts.run_work_ii_c_formal import runtime_surface

    surface = runtime_surface()
    surface["scripts/run_inquiry_completion.py"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    root.mkdir(parents=True, exist_ok=False)
    design = {
        "mode": MODE,
        "experiment_note": NOTE,
        "schedule": schedule(),
        "eq_config": config,
        "worker_module": "scripts.run_inquiry_completion",
        "concurrency": 4,
        "planned_sources": 30,
        "planned_source_batches": 180,
        "planned_posttests": 120,
        "planned_reference_batches": 300,
        "source_retries": 0,
        "provider": eq.PROVIDER,
        "model_rng_seed": None,
        "runtime_surface": surface,
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "evaluation_prompts": {"K1": K1, "Q": Q, "K2": K2, "EQS": EQS},
    }
    write(root / "design.json", design)
    for repeat in pool.REPEATS:
        write(root / repeat / "design.json", {"eq_config": config, "mode": MODE})


def references(root, progress):
    config = read(root / "design.json")["eq_config"]
    query_rows = eq.queries(config)
    actions = [a for q in query_rows for a in q["actions"]]
    truth = {}
    for world in config["worlds"]:
        wid = world["world_id"]
        truth[wid] = {q["query_id"]: [] for q in query_rows}
        for r in range(1, 6):
            result = eq.reference_run(
                root / "references" / wid / f"repeat-{r}",
                actions,
                config=config,
                world=world,
                batches=12,
                observation_seed=eq.deterministic_seed("eq-reference-truth-v1", wid, r),
                observation_namespace=f"work-ii-eq-truth-{wid.lower()}-r{r:02d}",
            )
            if (
                result["failure"]
                or result["rollbacks"]
                or len(result["batches"]) != 12
                or not result["exact_replay"]["verified"]
            ):
                raise RuntimeError(f"Reference/replay defect {wid}/{r}")
            for q, b in zip(query_rows, result["batches"], strict=True):
                truth[wid][q["query_id"]].append({m: b["metrics"][m] for m in eq.METRICS})
            progress["reference_batches"] += 12
            progress["unit"] = f"{wid}/{r}"
            write(root / "references/progress.json", progress)
            emit(progress)
    write(root / "references/truth.json", {"EQ": truth})
    write(
        root / "references/complete.json",
        {"completed_batches": 300, "trajectories": 25, "replay_verified": True},
    )


def execute(root, unit, progress):
    config = read(root / "design.json")["eq_config"]
    cell = next(c for c in eq.validate_design(config)["schedule"] if c["cell_id"] == unit["cell"])
    eq.configure_provider_helpers(config)
    eq.run_posttest = posttest
    eq.EqFreeResearchAgent = ResearchAgent
    source_root = root / unit["repeat"] / unit["id"]
    if case_folder(root / unit["repeat"], unit).exists():
        raise FileExistsError("Session already started; no replacement")
    if unit["opportunity"] == "Research":
        result = eq.run_cell(source_root, config, cell, progress, threading.Lock())
    else:
        result = no_research(source_root, config, cell, progress)
    truth = read(root / "references/truth.json")["EQ"][cell["world_id"]]
    result["prediction_evaluation"] = eq.evaluate_predictions(
        result["posttests"].get("Q", {}).get("payload"),
        eq.queries(config),
        truth,
    )
    result["opportunity"] = unit["opportunity"]
    write(pool.result_path(root, unit), result)
    pool.validate_result(result)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--unit")
    p.add_argument("--repeat")
    p.add_argument("--summarize", action="store_true")
    a = p.parse_args()
    root = a.root.resolve()
    if a.summarize:
        emit({k: v for k, v in pool.snapshot(root).items() if k != "cases"})
        return 0
    if not a.unit:
        prepare(root)
        return pool.coordinate_prepared(root)
    progress = {"stage": a.unit, "reference_batches": 0}
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(30):
            emit(progress)

    threading.Thread(target=heartbeat, daemon=True).start()
    try:
        if a.unit == "references":
            references(root, progress)
        else:
            unit = next(
                u
                for u in read(root / "design.json")["schedule"]
                if u["id"] == a.unit and u["repeat"] == a.repeat
            )
            execute(root, unit, progress)
    finally:
        stop.set()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
