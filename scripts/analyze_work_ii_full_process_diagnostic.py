"""Read-only trajectory replay to align diagnostics with the actual assay estimand."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import gymnasium as gym
from scripts.run_work_ii_astra_full_process_trial import LIMITS, QUALITY, ROOT, quality_checks
from scripts.run_work_ii_astra_single_trial import read, write
from scripts.run_work_ii_full_process_diagnostic import REPORT, build_report, markdown

from chemworld.data.logging import load_jsonl
from chemworld.eval.verify import _scalar_observation


def assay_truth_metrics(base, task):
    """Use the observation law, not the narrower local process-service summary."""
    truth = base.observation_kernel._truth_values(base._state)
    return {key: float(truth[key]) for key in QUALITY[task]}


def extract_truth(folder):
    output = folder / "assay-truth-replay.json"
    if output.exists():
        return read(output)
    rows = load_jsonl(folder / "trajectory.jsonl")
    first = rows[0]
    task = first["task_id"]
    env = gym.make(
        first["env_id"],
        task_id=task,
        seed=first["seed"],
        world_split=first["world_split"],
        budget_override=LIMITS[task],
        episode_mode_override="single_experiment",
        observation_seed_override=first["observation_seed"],
        observation_noise_mode=first["observation_noise_mode"],
        observation_noise_namespace=first["observation_noise_namespace"],
        campaign_resource_card=first["campaign_resource_card"],
    )
    truth, measured = {}, []
    try:
        env.reset(seed=first["seed"])
        for row in rows:
            # Instruments observe the composition immediately before sample withdrawal.
            before = assay_truth_metrics(env.unwrapped, task)
            obs, reward, terminated, truncated, info = env.step(row["action"])
            assert _scalar_observation(obs) == row["observation"]
            assert reward == row["reward"]
            assert terminated == row["terminated"] and truncated == row["truncated"]
            assert info["transaction_status"] == row["transaction_status"]
            if row["operation_type"] == "measure" and row["transaction_status"] == "committed":
                measured.append(
                    {
                        "step": row["step"],
                        "instrument": row["instrument"],
                        "assay_truth_metrics": before,
                    }
                )
                if row["instrument"] == "final_assay":
                    truth = before
    finally:
        env.close()
    result = {
        "checked_steps": len(rows),
        "exact_observation_reward_status_replay": True,
        "final_assay_truth_metrics": truth,
        "measurements": measured,
        "purpose": "Analysis of the original trajectory, not a new experimental condition.",
    }
    write(output, result)
    return result


def analyze(root):
    root = root.resolve()
    block = read(root / "block.json")
    cells = []
    started = time.monotonic()
    for index, plan in enumerate(block["plans"], 1):
        folder = root / plan["cell"]
        cell = read(folder / "analysis.json")
        extraction = extract_truth(folder)
        if "latent_process_metrics" in cell:
            cell["service_process_metrics"] = cell.pop("latent_process_metrics")
        cell.pop("latent_quality_checks", None)
        cell.pop("latent_quality_passed", None)
        cell["assay_truth_metrics"] = extraction["final_assay_truth_metrics"]
        cell["assay_truth_extraction"] = extraction
        cell["assay_truth_quality_checks"] = quality_checks(
            cell["task"], cell["assay_truth_metrics"]
        )
        cell["assay_truth_quality_passed"] = bool(cell["final_assays"]) and all(
            cell["assay_truth_quality_checks"].values()
        )
        cell["local_feasibility_witness"] = (
            cell["status"] == "completed"
            and cell["quality_passed"]
            and cell["assay_truth_quality_passed"]
            and cell["replay"]["verified"]
            and all(cell["validation"].values())
            and cell["prefix_reproduced"]
        )
        cells.append(cell)
        elapsed = time.monotonic() - started
        print(
            f"analysis-replay {index}/15 {plan['cell']} checked={extraction['checked_steps']} "
            f"cells/min={index * 60 / max(elapsed, 0.001):.2f} "
            f"ETA={(15 - index) * elapsed / index:.1f}s",
            flush=True,
        )
    report = build_report(root, block["source_binding"], cells)
    report["analysis_correction"] = {
        "original_service_metric_scope": "Process-service purity excludes other impurity families; "
        "its recovery denominator can be pre-separation product instead of initial reagent.",
        "corrected_scope": "Use the native observation-law truth before terminal sampling. "
        "Service summaries retained separately; original runs and failures unchanged.",
        "additional_conditions": 0,
    }
    report["interface_update"] = {
        "version": "chemworld-full-process-operational-state-0.1",
        "changed_after_block": True,
        "provider_tested": False,
        "added": [
            "ideal temperature/volume readings",
            "phase identities and selection",
            "explicit current-versus-carried analytical readings",
            "particle measurements terminal-only",
            "global sampling depletion limitation",
        ],
        "hidden_composition_or_parameters_exposed": False,
    }
    write(REPORT, report)
    REPORT.with_suffix(".md").write_text(markdown(report), encoding="utf-8")
    print(REPORT.relative_to(ROOT), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    analyze(args.root)


if __name__ == "__main__":
    main()
