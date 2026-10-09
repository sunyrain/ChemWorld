"""Fixed R36 development block against attributed NIST Shomate data.

No model fitting. Exit 1 means a recorded prediction/domain failure; exit 2 means
an execution error. Existing output is never overwritten. No network is needed.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from math import sqrt
from pathlib import Path
from time import perf_counter
from typing import Any

from chemworld.foundation.gas import GAS_CV, GAS_IDS, GAS_R, GasBoundary
from chemworld.physchem.gas_control import GAS_CONTROL_MODEL, advance_gas
from chemworld.runtime.semantics import RUNTIME_SEMANTICS_ID

REFERENCE_PATH = (
    Path(__file__).resolve().parents[1] / "configs/reference_data/nist_gas_shomate.json"
)
TEMPERATURES_K = (298.15, 350.0, 400.0, 470.0)
INITIAL_TEMPERATURE_K = 298.15
VOLUME_L = 0.02
INITIAL_PRESSURE_PA = 100000.0
DURATION_S = 60.0
RELATIVE_ERROR_LIMIT = 0.05


def shomate(reference: dict[str, Any], gas: str, temperature_K: float) -> tuple[float, float]:
    """Return NIST Cp [J/(mol K)] and H [kJ/mol], without extrapolation."""
    for segment in reference["gases"][gas]["segments"]:
        low, high = segment["temperature_range_K"]
        if low <= temperature_K <= high:
            a, b, c, d, e, f, _, h = segment["coefficients"]
            t = temperature_K / 1000.0
            cp = a + b * t + c * t**2 + d * t**3 + e / t**2
            enthalpy = a * t + b * t**2 / 2 + c * t**3 / 3 + d * t**4 / 4 - e / t + f - h
            return float(cp), float(enthalpy)
    raise ValueError(f"{gas}: {temperature_K} K outside the transcribed NIST reference domain")


def reference_heat_j(reference: dict[str, Any], gas: str, temperature_K: float) -> float:
    """Closed ideal gas: Q = n*(delta H - R*delta T), using known initial n."""
    initial_h = shomate(reference, gas, INITIAL_TEMPERATURE_K)[1]
    final_h = shomate(reference, gas, temperature_K)[1]
    delta_u = 1000.0 * (final_h - initial_h) - GAS_R * (temperature_K - INITIAL_TEMPERATURE_K)
    return initial_moles() * delta_u


def initial_moles() -> float:
    return INITIAL_PRESSURE_PA * VOLUME_L * 0.001 / (GAS_R * INITIAL_TEMPERATURE_K)


def pure_gas(gas: str) -> GasBoundary:
    amounts = tuple(initial_moles() if name == gas else 0.0 for name in GAS_IDS)
    energy = sum(n * cv * INITIAL_TEMPERATURE_K for n, cv in zip(amounts, GAS_CV, strict=True))
    return GasBoundary(VOLUME_L, INITIAL_TEMPERATURE_K, amounts, amounts, initial_energy_J=energy)


def sealed_heating(gas: str, temperature_K: float) -> GasBoundary:
    # Both flow limits are zero: atmosphere and pressure target cannot add/vent gas.
    return advance_gas(
        pure_gas(gas),
        duration_s=DURATION_S,
        final_temperature_K=temperature_K,
        pressure_setpoint_Pa=INITIAL_PRESSURE_PA,
        atmosphere=0,
        purge_flow_mol_s=0.0,
        maximum_flow_mol_s=0.0,
    )


def compare(predicted: float, reference: float, unit: str) -> dict[str, Any]:
    error = predicted - reference
    relative_error = abs(error) / abs(reference)
    return {
        "unit": unit,
        "predicted": predicted,
        "reference": reference,
        "signed_error": error,
        "absolute_error": abs(error),
        "relative_error": relative_error,
        "within_5_percent": relative_error <= RELATIVE_ERROR_LIMIT,
    }


def evaluate_unit(reference: dict[str, Any], kind: str, gas: str, temp: float) -> dict[str, Any]:
    cp = GAS_CV[GAS_IDS.index(gas)] + GAS_R
    if kind == "cp":
        return compare(cp, shomate(reference, gas, temp)[0], "J/(mol K)")
    if kind == "sealed_heat":
        final = sealed_heating(gas, temp)
        sealed = (
            final.amounts_mol == pure_gas(gas).amounts_mol
            and sum(final.added_mol) == 0
            and sum(final.removed_mol) == 0
            and final.enthalpy_in_J == final.enthalpy_out_J == final.pump_work_J == 0
        )
        if not sealed:
            raise ValueError("Sealed zero-flow calculation changed its inventory or flow ledger")
        return compare(final.bath_heat_J, reference_heat_j(reference, gas, temp), "J") | {
            "moles": initial_moles(),
            "final_pressure_Pa": final.pressure_pa,
            "material_residual_mol": final.material_residual_mol,
            "energy_residual_J": final.energy_residual_j,
            "zero_flow_verified": sealed,
        }
    if kind != "out_of_domain":
        raise ValueError(f"Unknown comparison kind: {kind}")
    rejection: str | None
    try:
        sealed_heating(gas, temp)
    except ValueError as exc:
        # An unrelated ValueError must not masquerade as the expected domain rejection.
        rejection = str(exc)
        rejected = rejection == "Gas advancement outside time/temperature domain"
        if not rejected:
            raise
    else:
        rejected, rejection = False, None
    return {
        "runtime_rejected": rejected,
        "rejection": rejection,
        "analytical_cp_extrapolation_not_runtime": compare(
            cp, shomate(reference, gas, temp)[0], "J/(mol K)"
        ),
    }


def metrics(rows: list[dict[str, Any]], expected: int) -> dict[str, Any]:
    available = [row for row in rows if row["execution_status"] == "complete"]
    errors = [row["absolute_error"] for row in available]
    relative = [row["relative_error"] for row in available]
    passed = sum(row["within_5_percent"] for row in available)
    return {
        "expected": expected,
        "evaluated": len(available),
        "passed": passed,
        "prediction_failed": len(available) - passed,
        "execution_failed": len(rows) - len(available),
        "missing": expected - len(rows),
        "unit": available[0]["unit"] if available else None,
        "metric_denominator": len(available),
        "mae": sum(errors) / len(errors) if errors else None,
        "rmse": sqrt(sum(e * e for e in errors) / len(errors)) if errors else None,
        "max_absolute_error": max(errors) if errors else None,
        "mean_relative_error": sum(relative) / len(relative) if relative else None,
        "max_relative_error": max(relative) if relative else None,
    }


def run_block(
    reference: dict[str, Any], progress: Callable[[int, str], None] | None = None
) -> dict[str, Any]:
    design = [
        (kind, gas, temperature)
        for kind, temperatures in (
            ("cp", TEMPERATURES_K),
            ("sealed_heat", TEMPERATURES_K[1:]),
            ("out_of_domain", (1000.0,)),
        )
        for gas in GAS_IDS
        for temperature in temperatures
    ]
    rows: list[dict[str, Any]] = []
    for kind, gas, temp in design:
        row: dict[str, Any] = {
            "id": f"{kind}-{gas}-{temp:g}K",
            "kind": kind,
            "gas": gas,
            "temperature_K": temp,
        }
        try:
            row.update(evaluate_unit(reference, kind, gas, temp))
            row["execution_status"] = "complete"
        except Exception as exc:
            row.update(execution_status="error", error=f"{type(exc).__name__}: {exc}")
        rows.append(row)
        if progress:
            progress(len(rows), row["id"])
    domain_rows = [row for row in rows if row["kind"] == "out_of_domain"]
    prediction_failures = [row["id"] for row in rows if row.get("within_5_percent") is False]
    domain_failures = [row["id"] for row in domain_rows if row.get("runtime_rejected") is False]
    execution_errors = [row["id"] for row in rows if row["execution_status"] == "error"]
    extrapolations = [
        row["analytical_cp_extrapolation_not_runtime"] | {"execution_status": "complete"}
        for row in domain_rows
        if row["execution_status"] == "complete"
    ]
    return {
        "schema": "chemworld-r36-gas-reference-1",
        "evidence_status": "development; not formal qualification or laboratory validation",
        "runtime_semantics_id": RUNTIME_SEMANTICS_ID,
        "gas_model": GAS_CONTROL_MODEL,
        "reference_id": reference["reference_id"],
        "source": reference["source"],
        "citation": reference["citation"],
        "accessed_date": reference["accessed_date"],
        "source_urls": {gas: reference["gases"][gas]["url"] for gas in GAS_IDS},
        "pointwise_reference_uncertainty": reference["pointwise_uncertainty"],
        "design": {
            "relative_error_limit": RELATIVE_ERROR_LIMIT,
            "initial_temperature_K": INITIAL_TEMPERATURE_K,
            "initial_pressure_Pa": INITIAL_PRESSURE_PA,
            "volume_L": VOLUME_L,
            "heating_duration_s": DURATION_S,
            "maximum_and_purge_flow_mol_s": 0.0,
            "fitted_parameters": [],
            "gas_constant_J_mol_K": GAS_R,
            "runtime_cv_J_mol_K": dict(zip(GAS_IDS, GAS_CV, strict=True)),
        },
        "summary": {
            "expected_units": 24,
            "evaluated_units": len(rows) - len(execution_errors),
            "cp": metrics([row for row in rows if row["kind"] == "cp"], 12),
            "sealed_heat": metrics([row for row in rows if row["kind"] == "sealed_heat"], 9),
            "out_of_domain": {
                "expected": 3,
                "evaluated": sum(row["execution_status"] == "complete" for row in domain_rows),
                "correctly_rejected": sum(
                    row.get("runtime_rejected", False) for row in domain_rows
                ),
                "analytical_cp_extrapolation_not_runtime": metrics(extrapolations, 3),
            },
            "prediction_failures": prediction_failures,
            "domain_failures": domain_failures,
            "execution_errors": execution_errors,
            "all_in_domain_predictions_within_threshold": (
                not prediction_failures and not execution_errors
            ),
        },
        "units": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=REFERENCE_PATH)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    started = perf_counter()

    def progress(completed: int, unit: str) -> None:
        elapsed = max(perf_counter() - started, 1e-9)
        rate = completed / elapsed
        print(
            f"R36 {completed}/24 {unit}; {rate:.1f} units/s; ETA {(24 - completed) / rate:.1f}s",
            flush=True,
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        report = run_block(reference, progress)
        output.write(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    summary = report["summary"]
    print(json.dumps(summary, indent=2))
    if summary["execution_errors"]:
        return 2
    return int(bool(summary["prediction_failures"] or summary["domain_failures"]))


if __name__ == "__main__":
    raise SystemExit(main())
