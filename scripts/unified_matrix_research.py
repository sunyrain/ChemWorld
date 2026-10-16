"""Research adapters for the prospectively fixed six-system matrix extension.

One participant per OS process: legacy runners configure module globals. This module
does not schedule, retry, or replace participant sessions. References are evaluator-only.
"""

from __future__ import annotations

import copy
import time
from collections import Counter
from contextlib import ExitStack
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from scripts.run_paper_case_notebooks import read, write
from scripts.unified_matrix_runtime import apply_environment, bounded_builder, bounded_notebook

from chemworld.agents.diagnostic_numerics import FOLLOWUP_NUMERICS

ARMS = ("Opaque", "Aligned", "MisIndexed")
MODEL = "gpt-5.6-sol"
PROTOCOL = "six-system-four-matrix-research-v1"


def build_cases():
    """Return 90 unique conditions, without the three repeat labels."""
    rows = []
    for wi in range(1, 6):
        for system in ("EC", "RX", "PA", "P"):
            goals = (
                ("discovery", "optimization")
                if system in {"EC", "RX"}
                else ("discovery" if system == "PA" else "optimization",)
            )
            for goal in goals:
                for arm in ARMS:
                    world = f"{system}-W{wi:02d}"
                    locus = "P" if system == "RX" else "E"
                    identifier = f"{world}-B12-{goal}-{locus}-{arm}"
                    cell = identifier
                    if system == "RX":
                        native_goal = {
                            "discovery": "mechanism_discovery",
                            "optimization": "safety_constrained_optimization",
                        }[goal]
                        cell = f"{world}--P--{native_goal}--{arm}"
                    elif system == "P":
                        cell = f"{world}-B12-E-{arm}"
                    rows.append(
                        {
                            "id": identifier,
                            "cell": cell,
                            "system": system,
                            "world": world,
                            "arm": arm,
                            "goal": goal,
                            "locus": locus,
                            "model": MODEL,
                            "batches": 12,
                            "matrix": "A" if system in {"EC", "RX"} else "B",
                        }
                    )
    assert Counter(r["system"] for r in rows) == {"EC": 30, "RX": 30, "PA": 15, "P": 15}
    return rows


def _snapshot(path, payload):
    if path.exists():
        if read(path) != payload:
            raise ValueError(f"Prepared input changed: {path}")
    else:
        write(path, payload)


def prepare_inputs(root, progress=None):
    """Snapshot current contracts and compute shared references; no provider calls."""
    from scripts import run_work_ii_ec_dual_goal_trial as ec
    from scripts import run_work_ii_ec_pa_matrix as matrix
    from scripts import run_work_ii_p_study as p
    from scripts import run_work_ii_pa_single_trial as pa
    from scripts import run_work_ii_rx_ps_five_world_dual_goal as rx

    from chemworld.eval.experiment_1_p_assets import frozen_world_truths

    root = Path(root)
    progress = progress if progress is not None else {}
    folder = root / "inputs" / "research"
    ec_worlds = {w["world_id"]: w for w in matrix.worlds("EC")}
    pa_worlds = {w["world_id"]: w for w in matrix.worlds("PA")}
    rx_config = read(rx.CONFIG)
    p_asset = read(p.ASSET)
    p_worlds = {w["world_id"]: w for w in frozen_world_truths(p_asset)}
    p_queries = p.gate.queries("v3")
    common = {
        "protocol": PROTOCOL,
        "provider": ec.PROVIDER,
        "cases": build_cases(),
        "notebook": "source-stage current optional hypothesis role",
        "provider_sampling_seed": "unavailable; fresh sessions",
        "automatic_retries": 0,
        "reference_policy": "host-only shared references, never supplied to participants",
    }
    _snapshot(folder / "contract.json", common)
    _snapshot(
        folder / "EC.json",
        {
            "worlds": ec_worlds,
            "queries": ec.queries(),
            "K1": ec.K1,
            "K2": ec.K2,
            "Q": ec.prediction_question(ec.queries()),
            "posttest_numerics": FOLLOWUP_NUMERICS.to_dict(),
        },
    )
    _snapshot(folder / "PA.json", {"worlds": pa_worlds, "queries": pa.queries()})
    _snapshot(
        folder / "RX.json",
        {
            "config": rx_config,
            "p_package": read(rx.P_PACKAGE),
            "s_contract": {},
            "queries": rx.queries(rx_config, "P"),
            "K1": rx.K1,
            "K2": rx.K2,
            "Q": rx.Q_PROMPT,
        },
    )
    _snapshot(
        folder / "P.json",
        {
            "protocol": PROTOCOL,
            "inventory_contract": "p-inventory-v3",
            "asset": p_asset,
            "worlds": p_worlds,
            "queries": p_queries,
            "source_system": p.SOURCE_SYSTEM,
            "goal": p.gate.GOAL,
            "K1": ec.K1,
            "Q": p.prediction_question(p_queries),
            "K2": ec.K2,
            "posttest_numerics": FOLLOWUP_NUMERICS.to_dict(),
            "resources": p.gate.resources().to_dict(),
            "source_method_resource_limits": p.SOURCE_LIMITS,
            "namespace": p.NAMESPACE,
        },
    )
    for system, worlds in (("EC", ec_worlds), ("PA", pa_worlds)):
        for world_id, world in worlds.items():
            progress.update(stage="reference", system=system, unit=world_id)
            ref = root / "references" / "research" / world_id
            if not (ref / "reference-result.json").exists():
                matrix.prepare_reference(system, world, ref, progress)
            if not read(ref / "reference-result.json").get("passed"):
                raise RuntimeError(f"Retained reference failed: {world_id}")
    for world_id, world in p_worlds.items():
        progress.update(stage="reference", system="P", unit=world_id, operations=0, batches=0)
        ref = root / "references" / "research" / world_id
        if not (ref / "result.json").exists():
            with p.inventory_v3():
                p.gate.execute(ref, world, "Opaque", p_asset, p_queries, progress)
        if not read(ref / "result.json").get("passed"):
            raise RuntimeError(f"Retained reference failed: {world_id}")
    rx_ref = root / "references" / "research" / "RX"
    if not (rx_ref / "truth.json").exists():
        progress.update(stage="reference", system="RX", unit="five-world-five-observation-truth")
        with patch.object(rx, "LOCI", ("P",)):
            rx.generate_truth(rx_ref, rx_config)
    complete = {"provider_calls": 0, "reference_batches": 480, "conditions": 90}
    write(folder / "complete.json", complete)
    return complete


def _single_p_posttest(agent, folder, stage, thread_id, progress, design, **kwargs):
    del kwargs
    from scripts import run_work_ii_ec_dual_goal_trial as ec
    from scripts import run_work_ii_p_study as p

    with patch.object(ec, "METRICS", p.METRICS):
        return ec.posttest(agent, folder, stage, thread_id, progress, design=design)


def _pa_retest(folder, result, world):
    from scripts import run_work_ii_ec_dual_goal_trial as ec
    from scripts import run_work_ii_pa_single_trial as pa

    from chemworld.data.logging import load_jsonl
    from chemworld.eval.work_ii_truth import _FrozenTruthReplayAgent

    receipts = read(folder / "source" / "source-receipts.json")
    recommendation = (receipts[-1] if receipts else {}).get("final_recommendation") or {}
    result["recommendation"] = recommendation
    selected = next(
        (
            b
            for b in result.get("source", {}).get("batches", [])
            if b["lifecycle_index"] == recommendation.get("selected_experiment_index")
        ),
        None,
    )
    if selected is None:
        return None
    dest = folder / "recommendation-retest"
    dest.mkdir()
    failure = None
    source_card = pa.resource_card(12)
    with patch.object(
        pa,
        "resource_card",
        lambda batches=12: replace(
            source_card,
            vessel_start_limit=1,
            final_assay_limit=1,
        ),
    ):
        try:
            pa.physics(
                _FrozenTruthReplayAgent(selected["actions"]),
                dest / "trajectory.jsonl",
                batches=12,
                world=world,
            )
        except Exception as exc:
            failure = {"type": type(exc).__name__, "message": str(exc)}
    records = load_jsonl(dest / "trajectory.jsonl") if (dest / "trajectory.jsonl").exists() else []
    retest = {
        "failure": failure,
        "batches": ec.summaries(records),
        "operations": len(records),
        "exact_replay": ec.replay_with_progress(
            records, "recommendation-retest", world_interventions=world.get("world_interventions")
        ),
    }
    write(dest / "result.json", retest)
    return retest


def _execute(root, folder, unit, progress):
    """The legacy native result is retained unchanged below participant/."""
    system = unit["system"]
    inputs = read(root / "inputs" / "research" / f"{system}.json")
    participant = folder / "participant"
    refs = root / "references" / "research"
    if system == "EC":
        from scripts import run_work_ii_ec_dual_goal_trial as ec

        participant.mkdir()
        world = inputs["worlds"][unit["world"]]
        write(
            participant / "design.json",
            {
                **inputs,
                "world_config": world,
                "batches_per_source": 12,
                "system": ec.source_system(12),
                "goal": ec.GOALS[unit["goal"]],
            },
        )
        with (
            patch.object(ec, "FreeResearchAgent", bounded_notebook(ec.FreeResearchAgent)),
            patch.object(ec, "build_command", bounded_builder(ec.build_command)),
        ):
            result = ec.run_cell(
                participant,
                unit["goal"],
                "E",
                unit["arm"],
                read(refs / unit["world"] / "reference-result.json")["truth"],
                progress,
            )
        return result, participant / f"{unit['goal']}-E-{unit['arm']}"
    if system == "PA":
        from scripts import run_work_ii_pa_single_trial as pa

        world = inputs["worlds"][unit["world"]]
        with (
            patch.object(
                pa, "PAAgent", bounded_notebook(pa.PAAgent, final_recommendation_required=False)
            ),
            patch.object(pa, "build_command", bounded_builder(pa.build_command)),
        ):
            pa.execute(
                participant,
                progress,
                arm=unit["arm"],
                batches=12,
                world=world,
                reference_run=refs / unit["world"],
            )
        result = read(participant / "result.json")
        if (participant / "source" / "source-receipts.json").exists():
            result["recommendation_retest"] = _pa_retest(participant, result, world)
        return result, participant / "source"
    if system == "RX":
        from scripts import run_work_ii_ec_dual_goal_trial as ec
        from scripts import run_work_ii_rx_ps_five_world_dual_goal as rx

        goal = {
            "discovery": "mechanism_discovery",
            "optimization": "safety_constrained_optimization",
        }[unit["goal"]]
        cell = {
            "cell_id": unit["cell"],
            "world_id": unit["world"],
            "world_seed": int(unit["world"][-2:]) - 1,
            "locus": "P",
            "goal": goal,
            "arm": unit["arm"],
        }
        with ExitStack() as stack:
            # Restore globals after one unit; also safe for provider-free tests.
            for name in (
                "TASK",
                "PROVIDER",
                "METRICS",
                "GOALS",
                "SYSTEM",
                "K1",
                "K2",
                "resource_card",
                "build_command",
            ):
                stack.enter_context(patch.object(ec, name, getattr(ec, name)))
            for name in ("K1", "K2", "Q_PROMPT"):
                stack.enter_context(
                    patch.object(rx, name, inputs["Q" if name == "Q_PROMPT" else name])
                )
            rx.configure_shared_helpers()
            stack.enter_context(
                patch.object(
                    rx.rx_canary, "build_command", bounded_builder(rx.rx_canary.build_command)
                )
            )
            stack.enter_context(
                patch.object(
                    rx.rx_canary,
                    "RxFreeResearchAgent",
                    bounded_notebook(rx.rx_canary.RxFreeResearchAgent),
                )
            )
            result = rx.run_cell(
                participant,
                cell,
                p_package=inputs["p_package"],
                s_contract={},
                config=inputs["config"],
                progress=progress,
            )
            result["prediction_evaluation"] = rx.evaluate_predictions(
                result.get("posttests", {}).get("Q", {}).get("payload"),
                inputs["queries"],
                read(refs / "RX" / "truth.json")[unit["world"]]["P"],
            )
            result["recommendation_retest"] = rx.run_recommendation_retest(participant, result)
        return result, participant / "sources" / unit["cell"]
    if system == "P":
        from scripts import run_work_ii_p_study as p

        cell = {"id": unit["cell"], "world_id": unit["world"], "arm": unit["arm"], "budget": 12}
        with (
            patch.object(p, "StudyAgent", bounded_notebook(p.StudyAgent)),
            patch.object(
                p,
                "posttest",
                _single_p_posttest,
            ),
            patch.object(p.ec, "build_command", bounded_builder(p.ec.build_command)),
        ):
            result = p.source(participant, cell, inputs, progress)
        result["prediction_evaluation"] = p.evaluate(
            result.get("posttests", {}).get("Q", {}).get("payload"),
            read(refs / unit["world"] / "result.json")["observations"],
            inputs["queries"],
        )
        return result, participant
    raise ValueError(f"Unknown research system: {system}")


def normalize_result(result, unit, source_dir, elapsed_s):
    source = result.get("source") or {
        "batches": result.get("batches", []),
        "operations": result.get("operations", 0),
        "exact_replay": result.get("exact_replay", {}),
        "usage": result.get("source_usage"),
        "failure": result.get("source_failure"),
        "rollbacks": result.get("rollbacks", []),
    }
    posttests = result.get("posttests", {})
    retest = result.get("recommendation_retest")
    checks = {
        "source_batches": len(source.get("batches", [])) == 12,
        "source_replay": source.get("exact_replay", {}).get("verified") is True,
        "sealed_stages": all(
            posttests.get(s, {}).get("payload")
            and not posttests[s].get("failure")
            and result.get("posttest_validation", {}).get(s, {}).get("valid", True)
            for s in ("K1", "Q", "K2")
        ),
        "prediction": result.get("prediction_evaluation", {}).get("valid") is True,
        "recommendation_retest": unit["system"] == "PA"
        or bool(
            retest
            and not retest.get("failure")
            and len(retest.get("batches", [])) == 1
            and retest.get("exact_replay", {}).get("verified") is True
        ),
        "no_failure": not result.get("failure") and not source.get("failure"),
    }
    return {
        **unit,
        "protocol": PROTOCOL,
        "status": "completed" if all(checks.values()) else "failed",
        "failure": result.get("failure")
        or source.get("failure")
        or (
            None
            if all(checks.values())
            else {"type": "nonconforming", "failed_checks": [k for k, v in checks.items() if not v]}
        ),
        "checks": checks,
        "source": source,
        "posttests": posttests,
        "posttest_validation": result.get("posttest_validation", {}),
        "prediction_evaluation": result.get("prediction_evaluation"),
        "recommendation": result.get("recommendation"),
        "recommendation_retest": retest,
        "participant": str(source_dir),
        "source_dir": str(source_dir),
        "elapsed_s": elapsed_s,
        "provider_sampling_seed": "unavailable; fresh session",
    }


def _native_locations(folder, unit):
    participant = folder / "participant"
    if unit["system"] == "EC":
        source = participant / f"{unit['goal']}-E-{unit['arm']}"
        return source / "result.json", source
    if unit["system"] == "RX":
        source = participant / "sources" / unit["cell"]
        return source / "result.json", source
    return participant / "result.json", (
        participant / "source" if unit["system"] == "PA" else participant
    )


def execute_unit(root, unit, progress=None):
    """Run one fixed session; an existing result is returned, never replaced."""
    root = Path(root)
    apply_environment()
    unit = copy.deepcopy(unit)
    if unit["model"] != MODEL or unit["batches"] != 12:
        raise ValueError("Model or batch budget differs from the fixed design")
    expected = next((r for r in build_cases() if r["id"] == unit["id"]), None)
    if expected is None or any(unit.get(k) != v for k, v in expected.items()):
        raise ValueError("Unit differs from the fixed condition matrix")
    repeat = unit["repeat"]
    if repeat not in {"repeat-01", "repeat-02", "repeat-03"}:
        raise ValueError("Unexpected independent-session repeat")
    folder = root / repeat / unit["id"]
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / "result.json").exists():
        return read(folder / "result.json")
    if (folder / "status.json").exists() and read(folder / "status.json").get("status") in {
        "completed",
        "failed",
    }:
        raise RuntimeError("Terminal status retained; automatic replacement is disabled")
    if (folder / "participant").exists():
        raise RuntimeError("Partial participant retained; automatic retry is disabled")
    progress = progress if progress is not None else {}
    started = time.monotonic()
    progress.update(stage="research", phase="source", unit=unit["id"], batches=0, operations=0)
    write(folder / "attempt.json", {"unit": unit, "started_epoch": time.time()})
    try:
        native, source_dir = _execute(root, folder, unit, progress)
        result = normalize_result(native, unit, source_dir, time.monotonic() - started)
    except Exception as exc:
        native_path, source_dir = _native_locations(folder, unit)
        native = read(native_path) if native_path.exists() else {}
        native["failure"] = native.get("failure") or {
            "type": type(exc).__name__,
            "message": str(exc),
            "stage": progress.get("phase"),
        }
        result = normalize_result(native, unit, source_dir, time.monotonic() - started)
        result["fatal_execution_error"] = True
    write(folder / "result.json", result)
    write(folder / "status.json", result)
    return result
