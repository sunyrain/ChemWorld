"""W2-251: fixed recipe/world quench pairs, with no model or adaptive recipe calls."""

from __future__ import annotations

import argparse
import copy
import subprocess
import time
from pathlib import Path
from statistics import fmean

import gymnasium as gym
from scripts import run_work_ii_c_formal as c
from scripts.run_paper_case_notebooks import ROOT, emit, read, write
from scripts.run_research_extension import NOTE


def paired_actions(actions):
    """The only action difference is one quench at the predeclared location."""
    indices = [i for i, a in enumerate(actions) if a["operation"] == "quench"]
    if len(indices) > 1:
        raise ValueError("The fixed block supports the observed zero/one-quench recipes only")
    absent = [copy.deepcopy(a) for a in actions if a["operation"] != "quench"]
    position = (
        indices[0]
        if indices
        else next(
            i
            for i, a in enumerate(absent)
            if a["operation"] in {"seed_crystals", "cool_crystallize"}
        )
    )
    present = copy.deepcopy(absent)
    present.insert(position, {"operation": "quench"})
    return {"absent": absent, "present": present}, position, "present" if indices else "absent"


def recipes(parent):
    rows = []
    for repeat in ("repeat-01", "repeat-02", "repeat-03"):
        for path in sorted((parent / repeat / "results").glob("C-*.json")):
            result = read(path)
            variants, position, original = paired_actions(
                result["recommendation_recipe"]["actions"]
            )
            rows.append(
                {
                    "id": f"{repeat}-{path.stem}",
                    "repeat": repeat,
                    "source_id": path.stem,
                    "source_world": path.stem.split("-")[1],
                    "selected_batch": result["recommendation"]["selected_experiment_index"],
                    "variants": variants,
                    "quench_position": position,
                    "original_variant": original,
                    "original_retest_truth": result["recommendation_retest"]["truth"][0],
                }
            )
    if len(rows) != 18:
        raise ValueError("All 18 recommendations, including failures, must be retained")
    return rows


class StateObserver(gym.Wrapper):
    """Read-only host diagnostics; nothing is exposed to a research participant."""

    def __init__(self, env, records):
        super().__init__(env)
        self.records = records

    def snapshot(self):
        state = self.unwrapped._state
        equipment = c.pilot.equipment_settings(state.equipment, "crystallizer")
        return {
            "temperature_K": state.temperature_K,
            "volume_L": state.volume_L,
            "species_amounts_mol": dict(state.species_amounts),
            "reaction_chemistry_stopped": bool(state.metadata.get("reaction_chemistry_stopped")),
            "particle_state": {
                k: copy.deepcopy(v)
                for k, v in equipment.items()
                if k.startswith("csd_") or k in {"population_cohorts", "seed_target_mol"}
            },
            "resources": {
                k: getattr(state.ledger, k)
                for k in ("time_s", "cost", "energy_jacket_J", "heat_loss_J")
            },
        }

    def step(self, action):
        before = self.snapshot()
        result = self.env.step(action)
        self.records.append(
            {
                "action": copy.deepcopy(action),
                "before": before,
                "after": self.snapshot(),
                "transaction_status": result[4].get("transaction_status"),
                "rollback_reason": result[4].get("rollback_reason"),
            }
        )
        return result


def outcome(result, states):
    truth = result["truth"][0] if len(result["truth"]) == 1 else None
    return {
        "passed": result["passed"],
        "failure": result["failure"],
        "truth": truth,
        "quality": c.pilot.quality(truth) if truth is not None else None,
        "quality_and_recovery": (
            c.pilot.quality(truth) and truth["crystal_yield"] >= 0.1 if truth is not None else None
        ),
        "operations": result["operations"],
        "elapsed_s": result["elapsed_s"],
        "exact_replay": result["exact_replay"],
        "cooling_diagnostics": result.get("host_diagnostics", []),
        "states": states,
    }


def summarize(root, pairs, started, completed, failure=None):
    valid = [p for p in pairs if p["paired_effect"] is not None]
    original = [p for p in valid if p["world"] == p["recipe_source_world"]]

    def group(rows):
        return {
            "valid_pairs": len(rows),
            "mean_present_minus_absent": {
                m: fmean(p["paired_effect"][m] for p in rows) if rows else None for m in c.METRICS
            },
            "quality_and_recovery": {
                arm: sum(p[arm]["quality_and_recovery"] for p in rows)
                for arm in ("absent", "present")
            },
            "fines_higher_with_quench": sum(
                p["paired_effect"]["crystal_fines_fraction"] > 1e-12 for p in rows
            ),
            "fines_lower_with_quench": sum(
                p["paired_effect"]["crystal_fines_fraction"] < -1e-12 for p in rows
            ),
        }

    elapsed = max(time.monotonic() - started, 1e-6)
    result = {
        "planned_pairs": 90,
        "planned_trajectories": 180,
        "completed_trajectories": completed,
        "completed_pairs": len(pairs),
        "valid_pairs": len(valid),
        "original_world": group(original),
        "all_worlds": group(valid),
        "by_world": {
            f"W{i:02d}": group([p for p in valid if p["world"] == f"W{i:02d}"]) for i in range(1, 6)
        },
        "failures": [
            {"pair": p["id"], "arm": a, "failure": p[a]["failure"]}
            for p in pairs
            for a in ("absent", "present")
            if not p[a]["passed"]
        ],
        "block_stop": failure,
        "elapsed_s": elapsed,
        "trajectories_per_minute": 60 * completed / elapsed,
        "eta_s": elapsed / completed * (180 - completed) if completed else None,
        "pairs": pairs,
        "interpretation": "Fixed virtual-world operation effects; "
        "paired worlds/recipes are nested. "
        "No independent deterministic repeats and no agent-learning intervention.",
    }
    write(root / "summary.json", result)
    emit(
        {
            k: result[k]
            for k in (
                "completed_trajectories",
                "planned_trajectories",
                "valid_pairs",
                "elapsed_s",
                "trajectories_per_minute",
                "eta_s",
                "block_stop",
            )
        }
    )
    return result


def run(root, parent):
    fixed_recipes = recipes(parent)
    root.mkdir(parents=True, exist_ok=False)
    write(
        root / "design.json",
        {
            "experiment_note": NOTE,
            "parent_root": str(parent.resolve()),
            "recipes": fixed_recipes,
            "planned_pairs": 90,
            "planned_trajectories": 180,
            "worlds": [f"W{i:02d}" for i in range(1, 6)],
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "runtime_surface": c.runtime_surface(),
            "model_calls": 0,
        },
    )
    pairs, completed, started = [], 0, time.monotonic()
    try:
        for recipe in fixed_recipes:
            for world in range(1, 6):
                pair = {
                    "id": f"{recipe['id']}-W{world:02d}",
                    "recipe": recipe["id"],
                    "recipe_source_world": recipe["source_world"],
                    "world": f"W{world:02d}",
                }
                for arm in ("absent", "present"):
                    states = []
                    emit(
                        {
                            "stage": "quench_pair",
                            "pair": pair["id"],
                            "arm": arm,
                            "completed_trajectories": completed,
                            "planned_trajectories": 180,
                        }
                    )
                    result = c.fixed(
                        root / pair["id"] / arm,
                        recipe["variants"][arm],
                        world_seed=world - 1,
                        observation_seed=303,
                        envelope=12,
                        capture_diagnostics=True,
                        observer=lambda env, records=states: StateObserver(env, records),
                    )
                    pair[arm] = outcome(result, states)
                    write(root / pair["id"] / arm / "state_observations.json", states)
                    completed += 1
                    if result["operations"] and not result["exact_replay"].get("verified"):
                        raise RuntimeError(f"Replay defect: {pair['id']}/{arm}")
                    if result["failure"] and not (
                        result["failure"]["type"] == "ValueError"
                        and result["failure"]["message"].startswith("illegal fixed action:")
                    ):
                        raise RuntimeError(
                            f"Platform defect: {pair['id']}/{arm}: {result['failure']}"
                        )
                    if (
                        arm == recipe["original_variant"]
                        and pair["world"] == recipe["source_world"]
                    ):
                        target = recipe["original_retest_truth"]
                        if not result["passed"] or any(
                            abs(pair[arm]["truth"][m] - target[m]) > 1e-12 for m in c.METRICS
                        ):
                            raise RuntimeError(
                                f"Original recipe no longer reproduces: {pair['id']}"
                            )
                pair["paired_effect"] = (
                    {m: pair["present"]["truth"][m] - pair["absent"]["truth"][m] for m in c.METRICS}
                    if pair["absent"]["passed"] and pair["present"]["passed"]
                    else None
                )
                pairs.append(pair)
                summarize(root, pairs, started, completed)
    except Exception as exc:
        summarize(
            root, pairs, started, completed, {"type": type(exc).__name__, "message": str(exc)}
        )
        raise
    return summarize(root, pairs, started, completed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--parent", type=Path, required=True)
    args = parser.parse_args()
    run(args.root.resolve(), args.parent.resolve())


if __name__ == "__main__":
    main()
