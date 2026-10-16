"""Matched crystallization research-opportunity units for the unified matrix.

The coordinator owns scheduling and the experiment note. This module never retries
a participant or supplies evaluator references to either arm. Run each unit in its
own process: the inherited crystallization runner uses module-level adapters.
"""

from __future__ import annotations

import copy
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

from scripts import run_work_ii_c_formal as c
from scripts.run_paper_case_notebooks import ROOT, read, write
from scripts.run_work_ii_study_b import _prepare_codex_home
from scripts.unified_matrix_runtime import apply_environment, bounded_notebook, with_thread_limits

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS

REPEATS = ("repeat-01", "repeat-02", "repeat-03")
ARMS = ("Research", "NoResearch")
STAGES = ("K1", "Q", "K2")
MODE = "unified-c-research-opportunity-30"
INPUT_DIRECTORY = "matrix-c-opportunity-inputs"
CORRECTED_DESIGN = Path(
    "D:/Projects/ChemWorld-local-research/20261014-c-recovery-aligned/attempt-01"
    "/repeat-01/C/design.json"
)
K1 = """Using only the information available to you, give a self-contained scientific
account in English of this reaction-to-crystallization world: material effects,
reaction/crystallization coupling, process-history dependence, and relationships or
equations you judge useful. Distinguish public background information, actual observations,
inference and conjecture. Cite batches and values only if actually observed; if you have
no experimental observations, state that explicitly and do not invent evidence. Discuss
uncertainty, supported ranges, alternatives and unresolved quality/recovery tradeoffs.
No explanation form or equation is prescribed. No further laboratory access. Do not change
an operating recommendation if one was made. Return report. Prediction questions are
revealed only after this account seals."""
K2 = """K1 and Q are sealed; no prediction truth or scores have been supplied. Answer in
English without changing earlier outputs:
1. Which claims are supported, contradicted or untested by the available information?
Distinguish actual observations from inference; cite batches only if observed and say
explicitly if no observations were available.
2. What single legal experiment would you choose next, which competing explanations
would it distinguish, and what different outcomes would you expect?
3. Which available evidence did your account use least effectively, and which held-out
prediction is least reliable? Explain the limits of your evidence and generalization.
Do not invent experiments or run new ones. Return report."""
EVALUATION_INSTRUCTIONS = (
    "Evaluate this reaction-to-crystallization world using only the information available "
    "in this conversation. Only public_numerics.calculate is available. No laboratory, "
    "network, filesystem, repository or hidden-truth access. Answer in English; earlier "
    "outputs remain sealed. Do not invent observations. " + FOLLOWUP_NUMERICS.disclosure()
)


def build_cases():
    """Balanced fixed ordering; each world/arm has three fresh model sessions."""
    rows = []
    for index, repeat in enumerate(REPEATS):
        worlds = list(range(1, 6))
        worlds = worlds[2 * index :] + worlds[: 2 * index]
        for world in worlds:
            arms = ARMS if (index + world) % 2 else ARMS[::-1]
            rows.extend(
                {
                    "matrix": "C",
                    "repeat": repeat,
                    "id": f"C-W{world:02d}-Opportunity-{arm}",
                    "system": "C",
                    "world": f"W{world:02d}",
                    "world_seed": world - 1,
                    "arm": "Opaque",
                    "opportunity": arm,
                    "cell": f"C-W{world:02d}-B12-E-Opaque",
                    "model": "gpt-5.6-sol",
                    "batches": 12 if arm == "Research" else 0,
                }
                for arm in arms
            )
    return rows


def public_context(agent, packet):
    """Only already-public contracts, state and material cards enter this payload."""
    state = copy.deepcopy(packet)
    # A fresh episode UUID is execution bookkeeping, not scientific information.
    # The untouched packet remains in the live source prompt/trajectory context.
    state.get("campaign_state", {}).pop("campaign_id", None)
    return {
        "task_contract": copy.deepcopy(agent._task_contract),
        "initial_public_state": state,
        "material_information": read(
            agent.workspace.reference_directory / "material_information.json"
        ),
        "research_protocol": c.source_system(12),
    }


class InitialStateCapturedError(Exception):
    """Stop before provider preparation and before the first laboratory action."""


class PublicInputMismatchError(RuntimeError):
    """An adapter input defect, distinct from a participant/provider failure."""


class CaptureInitialState(c.FormalCAgent):
    def _start_session(self, current_packet):
        self.captured = public_context(self, current_packet)
        raise InitialStateCapturedError


class ResearchAgent(bounded_notebook(c.FormalCAgent)):
    expected_public_context = None

    def _start_session(self, current_packet):
        context = public_context(self, current_packet)
        write(self.output / "initial-public-context.json", context)
        if context != self.expected_public_context:
            raise PublicInputMismatchError("Research/NoResearch initial scientific inputs differ")
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


def capture_initial(folder, world_seed):
    folder.mkdir(parents=True, exist_ok=False)
    output = folder / "source"
    output.mkdir()
    agent = CaptureInitialState(
        batches=12,
        goal="optimization",
        home_root=folder / "unused-home",
        output=output,
        workspace=folder / "laboratory",
        role_id="free_research",
    )
    trajectory = folder / "empty-trajectory.jsonl"
    try:
        c.physics(
            agent,
            trajectory,
            world_seed=world_seed,
            arm="Opaque",
            batches=12,
            observation_seed=0,
            callback=None,
            truths=[],
        )
    except InitialStateCapturedError:
        pass
    finally:
        agent.close()
    if not hasattr(agent, "captured"):
        raise RuntimeError("Initial public-state capture failed")
    if trajectory.exists() and trajectory.stat().st_size:
        raise RuntimeError("Public-state capture executed an action")
    write(folder / "initial-public-context.json", agent.captured)
    return agent.captured


def prepared_design(source_design=None):
    """Copy the corrected protocol without editing any retained evidence."""
    source = Path(source_design or CORRECTED_DESIGN)
    design = copy.deepcopy(read(source))
    if design["protocol"] != "c-quality-initial-charge-recovery-v4-en":
        raise ValueError("Expected corrected initial-charge recovery protocol")
    if design["model"] != c.pilot.ec.PROVIDER:
        raise ValueError("Expected retained Sol medium provider configuration")
    expected = {u["cell"] for u in build_cases()}
    design["schedule"] = [s for s in design["schedule"] if s["id"] in expected]
    if {s["id"] for s in design["schedule"]} != expected:
        raise ValueError("Missing five Opaque C cells")
    public_queries = [{k: q[k] for k in ("query_id", "pair", "actions")} for q in design["queries"]]
    design.update(
        mode=MODE,
        systems={"12": c.source_system(12)},
        K1=K1,
        Q=c.pilot.prediction_question(public_queries),
        K2=K2,
        queries=public_queries,
        posttest_numerics=FOLLOWUP_NUMERICS.to_dict(),
        automatic_retries=0,
        recovery_definition=c.pilot.CRYSTAL_RECOVERY_DEFINITION,
    )
    return design


def prepare_inputs(root, *, source_design=None, progress=None):
    """Prepare five public contexts and host-only references, without model calls."""
    apply_environment()
    root = Path(root)
    destination = root / INPUT_DIRECTORY
    destination.mkdir(parents=True, exist_ok=False)
    progress = {} if progress is None else progress
    design = prepared_design(source_design)
    write(destination / "design.json", design)
    current = read(ROOT / "configs/current.json")["work_ii"]["w2_257_inquiry_completion"]
    write(
        destination / "provenance.json",
        {
            "current_binding": "work_ii.w2_257_inquiry_completion.corrected_c_semantics",
            "semantic_report": current["corrected_c_semantics"],
            "source_design": str(Path(source_design or CORRECTED_DESIGN).resolve()),
            "planned_sessions": 30,
            "planned_source_batches": 180,
            "planned_posttests": 90,
            "model_sampling_seed": None,
            "same_world_observation_mapping_across_repeats": True,
        },
    )
    for world in range(1, 6):
        progress.update(phase="c_public_context", world=f"W{world:02d}")
        capture_initial(destination / "public" / f"W{world:02d}", world - 1)
        progress.update(phase="c_references")
        result = c.fixed(
            destination / "references" / f"W{world:02d}",
            [a for q in design["queries"] for a in q["actions"]],
            world_seed=world - 1,
            batches=12,
        )
        if not result["passed"] or len(result["truth"]) != 12:
            raise RuntimeError(f"C reference/replay defect in W{world:02d}")
        progress.update(reference_batches=12 * world)
    summary = {"mode": MODE, "sessions": 30, "reference_batches": 60, "ready": True}
    write(destination / "complete.json", summary)
    return summary


def posttest(agent, folder, stage, thread_id, progress, design):
    """Exactly the same posttest instructions/schema/tools in both arms."""
    workspace = agent.home_root / "followup"
    workspace.mkdir(parents=True, exist_ok=True)
    schema_path = workspace / f"{stage}-schema.json"
    write(schema_path, c.pilot.schema(stage))
    instructions = workspace / "instructions.md"
    instructions.write_text(EVALUATION_INSTRUCTIONS, encoding="utf-8")
    prompt = design[stage]
    if thread_id is None:
        prompt = (
            "You have no laboratory observations. Below is the common initial public "
            "background. The research protocol describes the available scientific task; "
            "no laboratory actions are available in this evaluation.\n"
            + json.dumps(agent.initial_public_context)
            + "\n"
            + prompt
        )
    audit = folder / f"{stage}-numerics.jsonl"
    command = c.pilot.build_command(
        c.pilot.ec.PROVIDER,
        schema_path,
        workspace,
        audit=audit,
        thread_id=thread_id,
        provider_retries=0,
        numerics_budget=FOLLOWUP_NUMERICS,
    )
    for name in ("chemworld_lab", "research_notebook"):
        # Codex validates transport configuration even for disabled MCP servers.
        command += [
            "-c",
            f"mcp_servers.{name}.enabled=false",
            "-c",
            f"mcp_servers.{name}.command={json.dumps(sys.executable)}",
        ]
    command += ["-c", f"model_instructions_file={json.dumps(instructions.as_posix())}"]
    result = c.pilot.launch(
        with_thread_limits(command),
        prompt,
        workspace,
        agent.followup_environment,
        folder / stage,
        1200,
        True,
        audit,
        {**progress, "phase": stage},
        numerics_budget=FOLLOWUP_NUMERICS,
    )
    if not result.get("payload"):
        result["failure"] = result.get("failure") or "missing_payload"
    if not result.get("thread_id") or (thread_id is not None and result["thread_id"] != thread_id):
        result["failure"] = result.get("failure") or "posttest_thread_missing_or_changed"
    agent.last_thread_id = result.get("thread_id")
    write(folder / stage / "receipt.json", result)
    return result


def no_research(folder, design, context, truth, progress):
    folder.mkdir(parents=True, exist_ok=False)
    home = folder / "private-home"
    home.mkdir()
    agent = SimpleNamespace(
        home_root=home,
        followup_environment=_prepare_codex_home(home, c.pilot.ec.PROVIDER),
        initial_public_context=context,
        last_thread_id=None,
    )
    write(folder / "initial-public-context.json", context)
    result = {
        "status": "failed",
        "failure": None,
        "source": {"batches": [], "operations": 0, "exact_replay": None, "usage": {}},
        "source_status": "not_applicable",
        "posttests": {},
    }
    write(folder / "result.json", result)
    for stage in STAGES:
        progress.update(phase=stage)
        turn = posttest(agent, folder, stage, agent.last_thread_id, progress, design)
        result["posttests"][stage] = turn
        write(folder / "result.json", result)
        if turn.get("failure"):
            result["failure"] = {"stage": stage, "message": turn["failure"]}
            break
    result["prediction_evaluation"] = c.evaluate(
        result["posttests"].get("Q", {}).get("payload"), truth, design["queries"]
    )
    if len(result["posttests"]) == 3 and not result["failure"]:
        result["status"] = "completed"
    result["tokens"] = c.pilot.token_accounting(result)
    result["tokens"]["expected_stages"] = list(STAGES)
    result["tokens"]["complete"] = bool(
        result["tokens"].get("valid")
        and [row["stage"] for row in result["tokens"].get("stages", [])] == list(STAGES)
    )
    write(folder / "result.json", result)
    return result


def normalize_result(native, unit, source_folder):
    """Keep original resources/results and add common completion accounting."""
    result = copy.deepcopy(native)
    result["native_status"] = result.get("status")
    source = result.setdefault("source", {})
    source.setdefault("batches", [])
    source.setdefault("operations", 0)
    source.setdefault("exact_replay", None)
    source.setdefault("usage", {})
    stages = result.setdefault("posttests", {})
    validation = result.setdefault("posttest_validation", {})
    for stage, turn in stages.items():
        if stage in validation:
            continue
        payload = turn.get("payload")
        if stage == "Q":
            evaluation = result.get("prediction_evaluation") or {}
            validation[stage] = {
                "valid": evaluation.get("valid") is True,
                "failures": evaluation.get("failures", evaluation.get("failure")),
            }
        else:
            valid = isinstance(payload, dict) and isinstance(payload.get("report"), str)
            valid = bool(valid and payload["report"].strip())
            validation[stage] = {"valid": valid, "failure": None if valid else "missing_report"}
    sealed = all(
        stages.get(stage, {}).get("payload")
        and not stages[stage].get("failure")
        and validation.get(stage, {}).get("valid")
        for stage in STAGES
    )
    retest = result.get("recommendation_retest") or {}
    checks = {
        "source_batches": len(source["batches"]) == unit["batches"],
        "source_replay": not source["operations"]
        or (source["exact_replay"] or {}).get("verified") is True,
        "sealed_stages": bool(sealed),
        "prediction": (result.get("prediction_evaluation") or {}).get("valid") is True,
        "recommendation_retest": unit["opportunity"] == "NoResearch"
        or bool(retest.get("passed") and (retest.get("exact_replay") or {}).get("verified")),
        "no_failure": not result.get("failure") and not source.get("failure"),
    }
    result["checks"] = checks
    result["status"] = "completed" if all(checks.values()) else "failed"
    if not all(checks.values()) and not result.get("failure"):
        result["failure"] = {
            "type": "nonconforming",
            "failed_checks": [k for k, value in checks.items() if not value],
        }
    if (
        isinstance(result.get("failure"), dict)
        and result["failure"].get("type") == "PublicInputMismatchError"
    ):
        result["fatal_execution_error"] = True
    result["posttest_chain_sealed"] = bool(sealed)
    result["source_dir"] = str(source_folder)
    result["paths"] = {
        "source": str(source_folder),
        "trajectory": str(source_folder / "trajectory.jsonl"),
        "notebook": str(source_folder / "notebook"),
    }
    return result


def execute_unit(root, unit, progress=None):
    """Execute once, retaining every source/posttest failure and numerical outcome."""
    apply_environment()
    root = Path(root)
    progress = {} if progress is None else progress
    folder = root / unit["repeat"] / unit["id"]
    status_path = folder / "status.json"
    if status_path.exists() and read(status_path).get("status") not in {"running", "queued"}:
        raise FileExistsError("Terminal unit cannot be overwritten")
    if folder.exists() and any(
        p.name not in {"status.json", "live.json"} for p in folder.iterdir()
    ):
        raise FileExistsError("Unit already started; no participant retry")
    expected = next(
        (u for u in build_cases() if (u["repeat"], u["id"]) == (unit["repeat"], unit["id"])),
        None,
    )
    if expected is None or any(unit.get(k) != v for k, v in expected.items()):
        raise ValueError("Unit is outside the fixed crystallization opportunity matrix")
    prepared = root / INPUT_DIRECTORY
    if not read(prepared / "complete.json")["ready"]:
        raise RuntimeError("C input preparation is incomplete")
    design = read(prepared / "design.json")
    context = read(prepared / "public" / unit["world"] / "initial-public-context.json")
    reference = read(prepared / "references" / unit["world"] / "result.json")
    truth = dict(zip([q["query_id"] for q in design["queries"]], reference["truth"], strict=True))
    started = time.monotonic()
    folder.mkdir(parents=True, exist_ok=True)
    write(status_path, {**unit, "status": "running", "started_epoch": time.time()})
    write(folder / "design.json", design)
    write(folder / "public-input-binding.json", context)
    result = {"status": "failed", "failure": None, "source": {}, "posttests": {}}
    source = (
        folder / "sources" / unit["cell"]
        if unit["opportunity"] == "Research"
        else folder / "source"
    )
    original_agent, original_posttest = c.FormalCAgent, c.pilot.posttest
    try:
        if unit["opportunity"] == "Research":
            cell = next(row for row in design["schedule"] if row["id"] == unit["cell"])
            write(folder / "qualification" / unit["world"] / "queries/result.json", reference)
            ResearchAgent.expected_public_context = context
            c.FormalCAgent, c.pilot.posttest = ResearchAgent, posttest
            result = c.source(folder, cell, progress)
        else:
            result = no_research(source, design, context, truth, progress)
    except Exception as exc:
        native_path = source / "result.json"
        if native_path.exists():
            result = read(native_path)
        result["adapter_failure"] = {
            "stage": progress.get("phase"),
            "type": type(exc).__name__,
            "message": str(exc),
        }
        result["failure"] = result.get("failure") or result["adapter_failure"]
        result["fatal_execution_error"] = True
        result["status"] = "failed"
    finally:
        c.FormalCAgent, c.pilot.posttest = original_agent, original_posttest
        ResearchAgent.expected_public_context = None
    result = normalize_result(result, unit, source)
    for stage, turn in result["posttests"].items():
        write(folder / "sealed" / f"{stage}.json", turn)
    result.update(unit=unit, elapsed_s=time.monotonic() - started)
    write(folder / "result.json", result)
    write(
        status_path,
        {
            **unit,
            "status": result["status"],
            "failure": result["failure"],
            "elapsed_s": result["elapsed_s"],
        },
    )
    return result
