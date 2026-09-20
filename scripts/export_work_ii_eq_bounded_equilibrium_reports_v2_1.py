#!/usr/bin/env python3
"""Export sanitized EQ v2 reports without mutating the frozen v2 exporter."""
# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import scripts.export_work_ii_eq_bounded_equilibrium_reports as legacy
import scripts.export_work_ii_eq_bounded_equilibrium_reports_v2 as frozen_v2

# Keep stable references before legacy.export is configured with the v2 wrappers.
# The frozen v2 exporter looked these functions up dynamically, which caused its
# wrappers to call themselves recursively after monkeypatching the legacy module.
_LEGACY_RENDER_CELL = legacy.render_cell
_LEGACY_RENDER_AGGREGATE = legacy.render_aggregate


def render_cell(payload: Mapping[str, Any]) -> str:
    rendered = _LEGACY_RENDER_CELL(payload)
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
            f"Dissociation-precipitation assessment: `{coupling.get('assessment', 'unavailable')}`.",
            "",
            f"Supported range: {coupling.get('supported_range', 'Unavailable.')}",
            "",
            f"Competing explanation: {coupling.get('competing_explanation', 'Unavailable.')}",
            "",
        ]
    )
    rendered = rendered.replace(marker, section + marker)
    return rendered.replace(
        "Reference truth was released only after every K2 response was sealed.",
        "Reference truth was released only after every EQS response was sealed.",
    )


def render_aggregate(
    rows: Sequence[Mapping[str, Any]], completion: Mapping[str, Any]
) -> str:
    rendered = _LEGACY_RENDER_AGGREGATE(rows, completion)
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
    legacy.validate_completion = frozen_v2.validate_completion
    legacy.render_cell = render_cell
    legacy.render_aggregate = render_aggregate
    index = legacy.export(root, destination)
    (destination / "REPRODUCE.md").write_text(
        "# Reproduction\n\n"
        "The source campaign, posttests, truth generation, and evaluations remain bound to the frozen EQ v2 design. "
        "Public Markdown was generated with the rendering-only v2.1 exporter, which preserves the frozen v2 content contract while fixing recursive wrapper dispatch. "
        "No source result, sealed response, prediction, truth value, or score is modified by export. "
        "Private authentication material, raw model event streams, session identifiers, and usage accounting remain outside this package.\n",
        encoding="utf-8",
    )
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    index = export(args.input.resolve(), args.output.resolve())
    print(
        json.dumps(
            {
                "stage": "export_complete",
                "cells": len(index["cells"]),
                "output": str(args.output.resolve()),
                "exporter": "v2.1-rendering-fix",
            }
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
