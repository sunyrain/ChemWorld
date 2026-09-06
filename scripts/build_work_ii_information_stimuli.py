"""Qualify the fixed ten-world W2-87 stimuli before any formal agent response."""

from __future__ import annotations

import secrets
import time
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from scripts.qualify_work_ii_information_endpoint import assess, context, read_trajectory_contract
from scripts.run_work_ii_final_diagnostic import digest, read, write

from chemworld.eval.work_ii_public_endpoint_reference import (
    FAMILIES,
    METRICS,
    endpoints,
    fit_public,
)
from chemworld.eval.work_ii_reviewer_followup import _truth_report
from chemworld.runtime.observation_services import ChemWorldObservationKernel

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/development/work-ii-information-ten-world-stimuli-20260906"
REPORT = ROOT / "workstreams/flagship_tasks/reports/work-ii-information-stimuli-20260906.json"
EXPONENTS = (1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95, 2.05, 2.15, 2.25)


def main() -> None:
    if RUN.exists() or REPORT.exists():
        raise FileExistsError("fixed block already exists; never overwrite or replace worlds")
    current = read(ROOT / "configs/current.json")
    binding = current["work_ii"]["w2_87_information_completeness"]
    qualification = read(ROOT / binding["endpoint_report"])
    if not qualification["gpt_development_ready"]:
        raise ValueError("v3 development reference is not qualified")
    development = ROOT / qualification["development_run"]
    template = read(development / "public_packet.json")
    runtime = read(development / "runtime_config.json")
    if runtime.get("scoring_contract_id") != "partition-s0-extraction-efficiency-v3":
        raise ValueError("stimuli must use the explicit v3 contract")
    excluded = {read(development / "private_design.json")["world_seed"]} | set(range(5))
    old_protocol = read(ROOT / current["work_ii"]["w2_77_final_diagnostic"]["protocol"])
    old = read(ROOT / old_protocol["source_root"] / "input_manifest.json")
    excluded.update(c["world_seed"] for c in old["cells"])
    seeds = []
    while len(seeds) < 10:
        seed = secrets.randbelow(2_000_000_000)
        if seed not in excluded and seed not in seeds:
            seeds.append(seed)
    write(RUN / "private_design.json", {"seeds": seeds, "target_exponents": EXPONENTS})
    write(RUN / "runtime_config.json", runtime)
    evidence = [
        {k: v for k, v in q.items() if "observations" not in k} for q in template["evidence"]
    ]
    scoring = template["scoring_action_queries"]
    observer = ChemWorldObservationKernel.observe
    captures = []

    def capture(self, state, action, rng):
        if action.get("operation") == "measure" and action.get("instrument") == "final_assay":
            values = self._truth_values(state)
            values["score"] = self._score(values)
            captures.append({m: float(values[m]) for m in METRICS})
        return observer(self, state, action, rng)

    worlds, checks, rows = [], [], []
    started = time.perf_counter()
    print("W2-87 stimuli: 0/240 full executions + replay; provider calls 0", flush=True)
    for wi, (seed, exponent) in enumerate(zip(seeds, EXPONENTS, strict=True), 1):
        cluster = f"W2-87-world-{wi:02d}"
        contract = context(seed)
        truth_maps = {"reference": {}, "target": {}}
        world_rows = []
        for law, alpha, queries in (
            ("reference", 1.0, evidence),
            ("target", exponent, evidence + scoring),
        ):
            for query in queries:
                directory = RUN / "truth" / cluster / law / query["query_id"]
                row = {
                    "unit": len(rows) + 1,
                    "world": cluster,
                    "law": law,
                    "query_id": query["query_id"],
                    "status": "failed",
                }
                captures.clear()
                try:
                    with patch.object(ChemWorldObservationKernel, "observe", capture):
                        report = _truth_report(
                            runtime=runtime,
                            queries=[query],
                            exponent=alpha,
                            world_seed=seed,
                            cluster_id=cluster,
                            output_root=directory,
                            liveness=lambda s: print(
                                f"stimuli {len(rows)}/240; active unit {s}s", flush=True
                            ),
                        )
                    truth_maps[law].update(report["truth"])
                    prediction = endpoints(
                        [query], contract, FAMILIES[1], [alpha], noisy_mean=False
                    )[query["query_id"]]
                    if len(captures) != 2:
                        raise ValueError("missing final execution/replay observation")
                    error = max(
                        abs(prediction[m] - values[m]) for values in captures for m in METRICS
                    )
                    actual_contract = read_trajectory_contract(directory, report)
                    row.update(
                        full_execution_completed=True,
                        exact_replay_completed=True,
                        mapping_error=error,
                        actual_scoring_contract_id=actual_contract,
                        status="passed"
                        if error <= 1e-7 and actual_contract == runtime["scoring_contract_id"]
                        else "failed",
                    )
                except Exception as exc:
                    row["failure"] = f"{type(exc).__name__}: {exc}"[:1000]
                rows.append(row)
                world_rows.append(row)
                elapsed = time.perf_counter() - started
                rate = len(rows) / max(elapsed, 1e-9)
                print(
                    f"stimuli {len(rows)}/240; {rate:.3f} executions/s; "
                    f"ETA {(240 - len(rows)) / rate:.0f}s; "
                    f"failures {sum(r['status'] != 'passed' for r in rows)}",
                    flush=True,
                )
                write(RUN / "progress.json", {"rows": rows, "scheduled": 240})
        packet = deepcopy(template)
        packet["complete_observation_contract"] = contract
        packet["evidence"] = [
            dict(
                q,
                reference_linear_observations=truth_maps["reference"].get(q["query_id"]),
                target_observations=truth_maps["target"].get(q["query_id"]),
            )
            for q in evidence
        ]
        write(RUN / cluster / "public_packet.json", packet)
        check = {"world": cluster, "passed": False}
        try:
            fit = fit_public(packet)
            write(RUN / cluster / "sealed_predictions.json", fit)
            hidden = {q["query_id"]: truth_maps["target"][q["query_id"]] for q in scoring}
            check.update(assess(fit, hidden, exponent), candidate_fit=fit)
            check["passed"] = check["passed"] and all(r["status"] == "passed" for r in world_rows)
            worlds.append(
                {
                    "cluster_id": cluster,
                    "target_exponent": exponent,
                    "public_packet": packet,
                    "scoring_truth": hidden,
                }
            )
        except Exception as exc:
            check["failure"] = f"{type(exc).__name__}: {exc}"
        checks.append(check)
        print(
            f"stimuli reference fit {wi}/10: {'passed' if check['passed'] else 'failed'}",
            flush=True,
        )
    passed = len(worlds) == 10 and all(c["passed"] for c in checks)
    write(
        RUN / "stimuli.json",
        {
            "status": "qualified" if passed else "failed",
            "worlds": worlds,
            "formal_result": False,
            "purpose": "fixed qualified stimuli for later formal agent block",
        },
    )
    result = {
        "schema_version": "work-ii-information-stimuli-1",
        "status": "qualified" if passed else "failed",
        "formal_result": False,
        "scheduled_worlds": 10,
        "qualified_worlds": sum(c["passed"] for c in checks),
        "scheduled_physical": 240,
        "attempted_physical": len(rows),
        "completed_physical": sum(r.get("full_execution_completed", False) for r in rows),
        "exact_replays": sum(r.get("exact_replay_completed", False) for r in rows),
        "provider_calls": 0,
        "rows": rows,
        "checks": checks,
        "failures": [r for r in rows if r["status"] != "passed"],
        "elapsed_seconds": time.perf_counter() - started,
        "stimuli": (RUN / "stimuli.json").relative_to(ROOT).as_posix(),
        "stimuli_sha256": digest(RUN / "stimuli.json"),
        "interpretation": "Fixed stimulus qualification, not formal agent outcomes. "
        "Ten independent generated instances span one power family; no world replacement.",
    }
    write(REPORT, result)
    content = (
        "# W2-87 ten-world stimulus qualification\n\n"
        f"{result['status']}: {result['qualified_worlds']}/10 worlds; "
        f"{result['completed_physical']}/240 executions; {result['exact_replays']}/240 replays.\n\n"
        + result["interpretation"]
        + "\nAll rows and candidate fits are in the companion JSON.\n"
    )
    REPORT.with_suffix(".md").write_text(content, encoding="utf-8", newline="\n")
    print(content, flush=True)


if __name__ == "__main__":
    main()
