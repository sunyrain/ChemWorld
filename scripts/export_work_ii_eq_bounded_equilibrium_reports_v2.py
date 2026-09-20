#!/usr/bin/env python3
"""Export sanitized English reports for the complete EQ v2 block."""
# ruff: noqa: E501, RUF001

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import scripts.export_work_ii_eq_bounded_equilibrium_reports as legacy
import scripts.recover_work_ii_eq_bounded_equilibrium_v2 as recovery
import scripts.run_work_ii_eq_bounded_equilibrium_v2 as eq

legacy.eq = eq
legacy.recovery = recovery
legacy.STAGES = eq.POSTTEST_STAGES


def validate_completion(root: Path) -> Mapping[str, Any]:
    completion = eq.read(root / "completion.json")
    expected = {
        "source_sessions": 15,
        "source_batches": 180,
        "posttests": 60,
        "reference_executions": 300,
    }
    if any(completion.get(key) != value for key, value in expected.items()):
        raise RuntimeError(f"EQ v2 completion denominators do not match: {completion}")
    if completion.get("equilibrium_confidence_used_as_agent_uncertainty_or_score") is not False:
        raise RuntimeError("EQ v2 completion has an invalid confidence-scoring declaration")
    return completion


def render_cell(payload: Mapping[str, Any]) -> str:
    rendered = legacy.render_cell(payload)
    marker = "## Blind-prediction evaluation"
    eqs = (payload["posttests"].get("EQS", {}).get("payload") or {})
    pka = eqs.get("effective_pka", {})
    path = eqs.get("path_dependence", {})
    coupling = eqs.get("dissociation_precipitation", {})
    section = "\n".join(
        [
            "### EQ-specific supplement",
            "",
            f"Effective pKa identifiable: `{pka.get('identifiable')}`; estimate `{legacy.number(pka.get('estimate'))}`; 80% interval `[{legacy.number(pka.get('lower80'))}, {legacy.number(pka.get('upper80'))}]`.",
            "",
            str(pka.get("rationale", "Unavailable.")),
            "",
            f"Path-dependence assessment: `{path.get('assessment', 'unavailable')}`.",
            "",
            str(path.get("rationale", "Unavailable.")),
            "",
            f"Dissociation–precipitation assessment: `{coupling.get('assessment', 'unavailable')}`.",
            "",
            f"Supported range: {coupling.get('supported_range', 'Unavailable.')}",
            "",
            f"Competing explanation: {coupling.get('competing_explanation', 'Unavailable.')}",
            "",
        ]
    )
    rendered = rendered.replace(marker, section + marker)
    rendered = rendered.replace(
        "Reference truth was released only after every K2 response was sealed.",
        "Reference truth was released only after every EQS response was sealed.",
    )
    return rendered


def render_aggregate(rows: Sequence[Mapping[str, Any]], completion: Mapping[str, Any]) -> str:
    rendered = legacy.render_aggregate(rows, completion)
    rendered = rendered.replace(
        "45 sealed K1/Q/K2 posttests",
        "60 sealed K1/Q/K2/EQS posttests",
    )
    rendered = rendered.replace(
        "K1 preceded fixed blind Q; K2 preceded truth generation.",
        "K1 preceded fixed blind Q; K2 preceded EQS; all EQS responses preceded truth generation.",
    )
    eqs_rows = [row["prediction_evaluation"].get("eqs", {}) for row in rows]
    identifiable = sum(item.get("identifiable") is True for item in eqs_rows)
    covered = [item["covered80"] for item in eqs_rows if item.get("covered80") is not None]
    supplement = "\n".join(
        [
            "",
            "## EQ-specific supplement diagnostics",
            "",
            f"Effective pKa was declared identifiable in {identifiable}/15 cells. Among identifiable cells, 80% interval coverage was {sum(covered)}/{len(covered)}. Structural supplement labels remain descriptive because no independent categorical truth evaluator was registered.",
            "",
        ]
    )
    return rendered + supplement


def export(root: Path, destination: Path) -> dict[str, Any]:
    legacy.validate_completion = validate_completion
    legacy.render_cell = render_cell
    legacy.render_aggregate = render_aggregate
    return legacy.export(root, destination)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = export(args.input.resolve(), args.output.resolve())
    print(json.dumps({"stage": "export_complete", "cells": len(index["cells"]), "output": str(args.output.resolve())}), flush=True)


if __name__ == "__main__":
    main()
