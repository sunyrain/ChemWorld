"""Fixed W2-87 stage B: complete trajectories, exact replay, public-only fitting."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import time
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from scripts.run_work_ii_final_diagnostic import digest, read, write

from chemworld.eval.work_ii_public_endpoint_reference import (
    FAMILIES,
    METRICS,
    candidate_domains,
    endpoints,
    fit_public,
    public_contract,
)
from chemworld.eval.work_ii_reviewer_followup import _truth_report
from chemworld.runtime.observation_services import ChemWorldObservationKernel
from chemworld.world.scenario import DefaultScenarioGenerator, get_scenario

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/development/work-ii-information-completeness-b-20260906"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-information-endpoint-20260906.json"
NOTE = "workstreams/flagship_tasks/WORK_II_INFORMATION_COMPLETENESS_EXPERIMENT_NOTE.md"


def context(seed: int) -> dict:
    instance = DefaultScenarioGenerator().generate(get_scenario("partition-discovery"), seed)
    return public_contract(instance.initial_state.temperature_K)


def coordinates(packet: dict) -> tuple[list[dict], list[dict]]:
    keep = (
        "query_id",
        "nominal_pair_id",
        "reference_partition_coefficient",
        "feature_values",
        "metric_ids",
    )
    return tuple(
        [
            [{k: q[k] for k in keep} for q in packet[field]]
            for field in ("evidence", "scoring_action_queries")
        ]
    )


def assess(fit: dict, truth: dict, target_exponent: float) -> dict:
    power = next(r for r in fit["families"] if r["family"] == FAMILIES[1])
    mae = sum(abs(power["predictions"][q][m] - truth[q][m]) for q in truth for m in METRICS) / (
        len(truth) * 4
    )
    error = abs(power["parameters"][0] - target_exponent)
    return {
        "power_exponent": power["parameters"][0],
        "exponent_abs_error": error,
        "held_out_mae": mae,
        "held_out_queries": len(truth),
        "held_out_metric_denominator": len(truth) * 4,
        "selected_family": fit["selected_family"],
        "organic_rmse_margin": fit["organic_rmse_margin"],
        "passed": fit["selected_family"] == FAMILIES[1]
        and fit["organic_rmse_margin"] >= 1e-4
        and error <= 0.1
        and mae <= 0.02
        and fit["power_optimizer_success"]
        and fit["saturation_optimizer_successes"] == 8,
    }


def main() -> None:
    global RUN, REPORT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repair-v3", action="store_true")
    args = parser.parse_args()
    previous_run, previous_report = RUN, REPORT
    if args.repair_v3:
        RUN = RUN.with_name(RUN.name + "-v3-repair")
        REPORT = REPORT.with_name(REPORT.stem + "-v3-repair.json")
    if RUN.exists() or REPORT.exists():
        raise FileExistsError("preserve the existing stage B block; do not reissue it")
    current = read(ROOT / "configs/current.json")
    old_protocol = read(ROOT / current["work_ii"]["w2_77_final_diagnostic"]["protocol"])
    source = ROOT / old_protocol["source_root"]
    manifest = read(source / "input_manifest.json")
    b3_protocol = read(ROOT / manifest["protocol_path"])
    runtime = read(ROOT / b3_protocol["runtime_config"])
    if args.repair_v3:
        runtime["scoring_contract_id"] = "partition-s0-extraction-efficiency-v3"
    unique = {}
    for cell in manifest["cells"]:
        unique.setdefault(cell["cluster_id"], cell)
    if len(unique) != 5:
        raise ValueError("historical denominator differs from five worlds")
    evidence, scoring = coordinates(next(iter(unique.values()))["public_packet"])
    excluded = {c["world_seed"] for c in unique.values()} | set(range(5))
    if args.repair_v3:
        seed = read(previous_run / "private_design.json")["world_seed"]
    else:
        seed = secrets.randbelow(2_000_000_000)
        while seed in excluded:
            seed = secrets.randbelow(2_000_000_000)
    write(RUN / "private_design.json", {"world_seed": seed, "target_exponent": 1.75})
    write(RUN / "runtime_config.json", runtime)
    contract = context(seed)
    write(RUN / "public_contract.json", contract)
    # Observer instrumentation evaluates the same state without mutation or random draws.
    observer = ChemWorldObservationKernel.observe
    captured = []

    def capture(self, state, action, rng):
        if action.get("operation") == "measure" and action.get("instrument") == "final_assay":
            truth = self._truth_values(state)
            truth["score"] = self._score(truth)
            captured.append({m: float(truth[m]) for m in METRICS})
        return observer(self, state, action, rng)

    rows, truth_maps = [], {"reference": {}, "target": {}}
    started = time.perf_counter()
    print("W2-87 B: full trajectories 0/24; provider calls 0", flush=True)
    for law, exponent, queries in (
        ("reference", 1.0, evidence),
        ("target", 1.75, evidence + scoring),
    ):
        for query in queries:
            directory = RUN / "truth" / law / query["query_id"]
            row = {
                "unit": len(rows) + 1,
                "law": law,
                "query_id": query["query_id"],
                "status": "failed",
            }
            captured.clear()
            try:
                with patch.object(ChemWorldObservationKernel, "observe", capture):
                    report = _truth_report(
                        runtime=runtime,
                        queries=[query],
                        exponent=exponent,
                        world_seed=seed,
                        cluster_id="W2-87-development-1",
                        output_root=directory,
                        liveness=lambda s: print(
                            f"W2-87 B: {len(rows)}/24 terminal; current trajectory active {s}s",
                            flush=True,
                        ),
                    )
                prediction = endpoints(
                    [query], contract, FAMILIES[1], [exponent], noisy_mean=False
                )[query["query_id"]]
                if len(captured) != 2:
                    raise ValueError(
                        f"expected execution/replay final readouts, got {len(captured)}"
                    )
                error = max(abs(prediction[m] - values[m]) for values in captured for m in METRICS)
                truth_maps[law].update(report["truth"])
                row.update(
                    status="passed" if error <= 1e-7 else "failed",
                    full_execution_completed=True,
                    exact_replay_completed=True,
                    max_noiseless_mapping_error=error,
                    predicted_noiseless=prediction,
                    actual_noiseless=captured[0],
                    receipt=report["receipts"][0],
                )
                trajectory = read_trajectory_contract(directory, report)
                row["actual_scoring_contract_id"] = trajectory
                if args.repair_v3 and trajectory != runtime["scoring_contract_id"]:
                    row.update(status="failed", failure="explicit runtime contract was not honored")
            except Exception as exc:
                row["failure"] = f"{type(exc).__name__}: {exc}"[:1000]
                if (directory / "report.json").exists():
                    row["execution_report"] = read(directory / "report.json")
            rows.append(row)
            write(RUN / "progress.json", {"rows": rows, "scheduled": 24})
            elapsed = time.perf_counter() - started
            rate = len(rows) / max(elapsed, 1e-9)
            print(
                f"W2-87 B {len(rows)}/24; {rate:.3f} executions/s; "
                f"ETA {(24 - len(rows)) / rate:.1f}s; "
                f"failures {sum(r['status'] != 'passed' for r in rows)}",
                flush=True,
            )
    packet = {
        "task_id": "partition-discovery",
        "metric_range": [0, 1],
        "candidate_mechanism_families": deepcopy(
            next(iter(unique.values()))["public_packet"]["candidate_mechanism_families"]
        ),
        "candidate_parameter_domains": candidate_domains(),
        "complete_observation_contract": contract,
        "scoring_action_queries": scoring,
        "evidence": [
            dict(
                q,
                reference_linear_observations=truth_maps["reference"].get(q["query_id"]),
                target_observations=truth_maps["target"].get(q["query_id"]),
            )
            for q in evidence
        ],
    }
    write(RUN / "public_packet.json", packet)
    fitting = None
    qualification = {"passed": False, "failure": "incomplete_physical_truth"}
    if len(truth_maps["reference"]) == 8 and len(truth_maps["target"]) == 16:
        try:
            fitting = fit_public(packet)
            write(RUN / "sealed_reference_predictions.json", fitting)
            held_out = {q["query_id"]: truth_maps["target"][q["query_id"]] for q in scoring}
            qualification = assess(fitting, held_out, 1.75)
            write(RUN / "private_scoring_truth.json", held_out)
        except Exception as exc:
            qualification = {"passed": False, "failure": f"{type(exc).__name__}: {exc}"}
    historical = []
    for index, cell in enumerate([] if args.repair_v3 else unique.values(), 1):
        packet_old = deepcopy(cell["public_packet"])
        packet_old["complete_observation_contract"] = context(cell["world_seed"])
        packet_old["candidate_parameter_domains"] = candidate_domains()
        item = {"world": f"historical-{index}", "formal_result": False}
        try:
            fitted = fit_public(packet_old)
            write(RUN / f"historical-{index}-sealed-predictions.json", fitted)
            item.update(assess(fitted, cell["scoring_truth"], 1.75), fit=fitted)
            reference_map = endpoints(
                packet_old["evidence"],
                packet_old["complete_observation_contract"],
                FAMILIES[0],
                [],
                noisy_mean=True,
            )
            item["reference_organic_rmse_under_current_contract"] = (
                sum(
                    (
                        reference_map[q["query_id"]]["product_in_organic"]
                        - q["reference_linear_observations"]["product_in_organic"]
                    )
                    ** 2
                    for q in packet_old["evidence"]
                )
                / 8
            ) ** 0.5
            item["interpretation"] = (
                "Historical compatibility diagnostic only; current semantics "
                "are not retroactively assigned to old trajectories."
            )
        except Exception as exc:
            item.update(passed=False, failure=f"{type(exc).__name__}: {exc}")
        historical.append(item)
        print(f"W2-87 B historical public-only diagnostic {index}/5", flush=True)
    if args.repair_v3:
        historical = read(previous_report)["historical_diagnostics"]
    passed = all(r["status"] == "passed" for r in rows) and qualification["passed"]
    result = {
        "schema_version": "work-ii-information-endpoint-1",
        "formal_result": False,
        "status": "development_reference_qualified" if passed else "development_reference_failed",
        "experiment_note": NOTE,
        "scheduled_physical": 24,
        "attempted_physical": len(rows),
        "completed_physical": sum(r.get("full_execution_completed", False) for r in rows),
        "exact_replays": sum(r.get("exact_replay_completed", False) for r in rows),
        "mapping_passed": sum(r["status"] == "passed" for r in rows),
        "provider_calls": 0,
        "new_development_worlds": 1,
        "additional_development_worlds_this_attempt": 0 if args.repair_v3 else 1,
        "repairs_attempt": previous_report.relative_to(ROOT).as_posix() if args.repair_v3 else None,
        "runtime_scoring_contract_id": runtime.get(
            "scoring_contract_id", "task-derived-scoring-v1"
        ),
        "new_formal_worlds": 0,
        "rows": rows,
        "failures": [r for r in rows if r["status"] != "passed"],
        "public_contract": contract,
        "public_reference_fit": fitting,
        "reference_qualification": qualification,
        "historical_diagnostics": historical,
        "gpt_development_ready": passed,
        "formal_agent_block_ready": False,
        "elapsed_seconds": time.perf_counter() - started,
        "source": {
            "binding": "work_ii.w2_77_final_diagnostic",
            "input_manifest_sha256": digest(source / "input_manifest.json"),
        },
        "development_run": RUN.relative_to(ROOT).as_posix(),
        "interpretation": "Development only. Public fitter has no simulator or scoring labels. "
        "Observer comparisons are privileged implementation validation; failures are retained. "
        "Neither this block nor current runtime equations requalify historical B3 evidence.",
    }
    write(REPORT, result)
    text = [
        "# W2-87 full endpoint reference qualification",
        "",
        f"Status: {result['status']}.",
        f"Physical executions {result['completed_physical']}/24; "
        f"exact replay {result['exact_replays']}/24; mapping passed {result['mapping_passed']}/24.",
        "New provider calls: 0. One development world; zero new formal worlds.",
        "",
        "Public-only reference recovery and held-out prediction:",
        "```json",
        json.dumps(qualification, indent=2),
        "```",
        "",
        "Full contract, candidate fits, historical diagnostics and failures: companion JSON.",
        result["interpretation"],
        "",
        "GPT can enter six-session development."
        if passed
        else "GPT and ten-world production remain unstarted under the qualification stop rule.",
    ]
    REPORT.with_suffix(".md").write_text("\n".join(text) + "\n", encoding="utf-8", newline="\n")
    binding = current["work_ii"]["w2_87_information_completeness"]
    if args.repair_v3:
        binding["retained_endpoint_failure"] = {
            "report": previous_report.relative_to(ROOT).as_posix(),
            "report_sha256": digest(previous_report),
            "complete_physical_experiments": 24,
            "exact_replays": 24,
            "mapping_passed": 0,
        }
    binding.update(
        endpoint_report=REPORT.relative_to(ROOT).as_posix(),
        endpoint_report_sha256=hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        status=result["status"],
        gpt_development_ready=passed,
        complete_physical_experiments=result["completed_physical"],
        exact_replays=result["exact_replays"],
    )
    write(ROOT / "configs/current.json", current)
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "status",
                    "completed_physical",
                    "exact_replays",
                    "mapping_passed",
                    "elapsed_seconds",
                )
            }
        ),
        flush=True,
    )


def read_trajectory_contract(directory: Path, report: dict) -> str:
    path = directory / report["receipts"][0]["trajectory"]["path"]
    with path.open(encoding="utf-8") as stream:
        return json.loads(next(stream))["scoring_contract_id"]


if __name__ == "__main__":
    main()
