"""Descriptive direct-network nuisance refit; no participant calls or design tuning."""

from __future__ import annotations

import argparse
import json
import threading
import time
from pathlib import Path

from scipy.optimize import differential_evolution
from scripts.qualify_abductive_worlds import write

from chemworld.physchem.abductive_worlds import (
    ASSAY_STD,
    METRICS,
    NOTE,
    build_queries,
    build_worlds,
    diagnostic_queries,
    solve_query,
)
from chemworld.physchem.equilibrium_mechanism import solve_coupled_weak_acid_precipitation


def direct_prediction(query, parameters):
    final = query["final_state"]
    result = solve_coupled_weak_acid_precipitation(
        acid_total_mol=final["reagent_mol"],
        volume_L=final["solvent_L"],
        pka=parameters[0],
        log10_ksp=parameters[1],
        mechanism_family="direct_free_ion_precipitation",
        cation_fraction=parameters[2],
        activity_coefficient_ratio=parameters[3],
    )
    return {
        "pH_normalized": result.pH / 14,
        "acid_dissociation_fraction": result.acid_dissociation_fraction,
        "precipitation_signal": result.precipitation_signal,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    started = time.monotonic()
    status = {
        "stage": "direct-network-nuisance-refit",
        "completed_fits": 0,
        "total_fits": 5,
        "world": None,
        "objective_evaluations": 0,
    }
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(20):
            print(json.dumps({**status, "elapsed_seconds": time.monotonic() - started}), flush=True)

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    rows = []
    try:
        for world in build_worlds():
            if world["private_authoring"]["mechanism_id"] != "B":
                continue
            status["world"] = world["world_id"]
            failures = []
            targets = [solve_query(world, query)["metrics"] for query in diagnostic_queries()]

            def objective(parameters, targets=targets, failures=failures):
                status["objective_evaluations"] += 1
                residuals = []
                for query, target in zip(diagnostic_queries(), targets, strict=True):
                    try:
                        prediction = direct_prediction(query, parameters)
                    except Exception as exc:
                        failures.append(
                            {
                                "parameters": list(parameters),
                                "query_id": query["query_id"],
                                "failure": f"{type(exc).__name__}: {exc}",
                            }
                        )
                        return 1e12
                    residuals.extend(
                        ((prediction[m] - target[m]) / ASSAY_STD[m]) ** 2 for m in METRICS
                    )
                return sum(residuals) / len(residuals)

            result = differential_evolution(
                objective,
                [(3, 7), (-8, -3), (0.01, 0.5), (0.1, 10)],
                seed=20261016,
                popsize=8,
                maxiter=40,
                polish=True,
                workers=1,
            )
            heldouts = []
            for query in build_queries():
                target = solve_query(world, query)["metrics"]
                prediction = direct_prediction(query, result.x)
                gap = {m: abs(prediction[m] - target[m]) / ASSAY_STD[m] for m in METRICS}
                heldouts.append(
                    {
                        "query_id": query["query_id"],
                        "target": target,
                        "prediction": prediction,
                        "absolute_error_sigma": gap,
                        "channels_above_three_sigma": sum(v >= 3 for v in gap.values()),
                    }
                )
            rows.append(
                {
                    "world_id": world["world_id"],
                    "optimizer_success": bool(result.success),
                    "optimizer_message": str(result.message),
                    "objective": float(result.fun),
                    "objective_evaluations": int(result.nfev),
                    "fitted_parameters": dict(
                        zip(
                            ("pka", "log10_ksp", "cation_fraction", "activity_coefficient_ratio"),
                            map(float, result.x),
                            strict=True,
                        )
                    ),
                    "heldouts": heldouts,
                    "two_channel_separated_holdouts": sum(
                        h["channels_above_three_sigma"] >= 2 for h in heldouts
                    ),
                    "failed_objective_evaluations": failures,
                }
            )
            status["completed_fits"] = len(rows)
            write(
                args.output,
                {
                    "note": NOTE,
                    "planned_fits": 5,
                    "completed_fits": len(rows),
                    "interpretation": (
                        "Best numerical refits, not a global identifiability proof; "
                        "no design retuning."
                    ),
                    "fits": rows,
                },
            )
            print(
                json.dumps(
                    {
                        **status,
                        "objective": float(result.fun),
                        "optimizer_success": bool(result.success),
                        "elapsed_seconds": time.monotonic() - started,
                    }
                ),
                flush=True,
            )
    finally:
        stop.set()
        thread.join(timeout=1)


if __name__ == "__main__":
    main()
