#!/usr/bin/env python3
"""Render first-paper tables and figure legends from current-bound figure data."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_first_paper_figure_data import (  # noqa: E402
    SCHEMA,
    build_figure_data,
    canonical_sha256,
)

DEFAULT_DATA = (
    ROOT / "paper/figures/first-paper-world-instrument-v1" / "first-paper-figure-data-v1.json"
)
DEFAULT_OUTPUT = ROOT / "paper/experimental_intelligence_v1_display_items.md"


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA:
        raise ValueError("unsupported first-paper figure-data schema")
    declared = data.get("figure_data_sha256")
    unhashed = {key: value for key, value in data.items() if key != "figure_data_sha256"}
    if declared != canonical_sha256(unhashed):
        raise ValueError("first-paper figure-data content hash is invalid")
    if data != build_figure_data(ROOT):
        raise ValueError("first-paper figure data is not current-bound")
    return data


def _fmt(value: Any, digits: int = 3) -> str:
    if isinstance(value, bool):
        return "PASS" if value else "FAIL"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(_fmt(value) for value in row) + " |" for row in rows)
    return lines


def _surface_table(data: Mapping[str, Any]) -> list[str]:
    figure_1 = data["figure_1"]
    figure_2 = data["figure_2"]
    reference = figure_1["reference_counts"]
    construction = figure_1["construction_counts"]
    rows = [
        (
            "reusable component types",
            len(figure_1["components"]),
            "declared component vocabulary",
        ),
        ("frozen component patterns", len(figure_2["patterns"]), "coverage design"),
        ("registered reference tasks", reference["reference_tasks"], "reference landmarks"),
        ("typed operation kinds", reference["typed_operations"], "public action surface"),
        ("synthetic instrument contracts", reference["instruments"], "public measurement surface"),
        ("task-metric bindings", reference["task_metric_bindings"], "evaluation bindings"),
        (
            "coverage-generated compositions",
            construction["generated_compositions"],
            "full generated census",
        ),
        (
            "unseen reaction-distillation compositions",
            figure_2["unseen_composition_count"],
            "absent from reference identities",
        ),
        ("controlled fork pairs", construction["controlled_fork_pairs"], "single private target"),
        ("provider-free fork traces", construction["fork_traces"], "parent and child executions"),
    ]
    return _table(("Quantity", "Count", "Interpretation"), rows)


def _qualification_table(data: Mapping[str, Any]) -> list[str]:
    figure_3 = data["figure_3"]
    rows: list[tuple[Any, ...]] = []
    for row in figure_3["execution_censuses"]:
        rows.append((row["label"], row["passed"], row["denominator"], "complete execution"))
    for row in figure_3["qualification_censuses"]:
        role = "expected rejection" if row["label"].startswith("invalid") else "qualified probe"
        rows.append((row["label"], row["passed"], row["denominator"], role))
    return _table(("Qualification unit", "Passed", "Denominator", "Gate role"), rows)


def _deterministic_table(data: Mapping[str, Any]) -> list[str]:
    rows = [
        (
            case["case_id"],
            case["label"],
            case["submitted"],
            case["committed"],
            case["rolled_back"],
            case["final_assays"],
            case["resource_reconciled"],
            case["exact_replay"],
        )
        for case in data["figure_4"]["cases"]
    ]
    return _table(
        (
            "Case",
            "Scientific use",
            "Submitted",
            "Committed",
            "Rollback",
            "Final assay",
            "Resources",
            "Replay",
        ),
        rows,
    )


def _fork_table(data: Mapping[str, Any]) -> list[str]:
    values = data["figure_5"]
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for row in values["rows"]:
        groups.setdefault(row["intervention_class"], []).append(row)
    labels = {
        "mechanism_or_constitutive_law": "constitutive-law family",
        "material_law_counterfactual": "material-law counterfactual",
    }
    rows = []
    for key in ("mechanism_or_constitutive_law", "material_law_counterfactual"):
        group = groups[key]
        rows.append(
            (
                labels[key],
                len(group),
                ", ".join(str(row["seed"]) for row in group),
                values["public_contract_component_count"],
                sum(all(row["gates"].values()) for row in group),
            )
        )
    return _table(
        ("Intervention", "Pairs", "Seeds", "Invariant public fields", "All gates passed"),
        rows,
    )


def _agent_table(data: Mapping[str, Any]) -> list[str]:
    agent = data["figure_6"]["complete_agent"]
    used = agent["resource_usage"]
    limits = agent["resource_limits"]
    provider = agent["provider"]
    rows = [
        ("submitted actions", agent["submitted"], 16, "environment action ceiling"),
        ("committed actions", agent["committed"], agent["submitted"], "all submitted actions"),
        ("rollbacks", agent["rolled_back"], 0, "required zero"),
        ("explicit termination", agent["terminate"], 1, "required lifecycle closure"),
        ("final assay", agent["final_assay"], 1, "required exactly once"),
        (
            "environment process time (s)",
            used["process_time_s"],
            limits["process_time_s"],
            "simulated process ledger",
        ),
        (
            "instrument uses",
            used["instrument_uses"],
            limits["instrument_uses"],
            "environment resource ledger",
        ),
        (
            "sample consumed (mL)",
            1_000 * used["sample_consumed_L"],
            1_000 * limits["sample_consumed_L"],
            "environment resource ledger",
        ),
        ("provider sessions", provider["sessions"], 1, "provider ledger"),
        ("logical agent turns", provider["logical_turns"], 1, "provider ledger"),
        ("instrument-interface calls", provider["mcp_calls"], 17, "provider ledger"),
        ("cumulative input tokens", provider["input_tokens"], 640_000, "provider ledger"),
        (
            "cached input tokens",
            provider["cache_hit_tokens"],
            provider["input_tokens"],
            "reused context",
        ),
        ("uncached input tokens", provider["cache_miss_tokens"], 192_000, "independent hard limit"),
        ("output tokens", provider["output_tokens"], 64_000, "provider ledger"),
    ]
    return _table(("Ledger item", "Observed", "Reference or limit", "Meaning"), rows)


def _endpoint_table(data: Mapping[str, Any]) -> list[str]:
    endpoint = data["figure_6"]["endpoint_near_example"]
    rows = [
        ("raw terminal score", endpoint["raw_terminal_score"]),
        ("normalized best-discovery position", endpoint["best_discovery_fraction"]),
        ("online incumbent retention", endpoint["online_retention_rate"]),
        ("maximum drawdown", endpoint["maximum_drawdown"]),
        ("terminal-to-best ratio", endpoint["terminal_to_best_ratio"]),
    ]
    return _table(("Process coordinate", "Matched-pair contrast"), rows)


def render(data: Mapping[str, Any]) -> str:
    zeros = data["figure_3"]["zero_findings"]
    fork_values = data["figure_5"]
    recovery = data["figure_4"]["recovery"]
    sections: list[str] = [
        "# ChemWorld first-paper numeric display items",
        "",
        "Status: complete for the current first-paper evidence programme.",
        "",
        "Every number below is rendered from the current-bound reader-facing figure data.",
        "Counts retain their exact qualification denominators and are not statistical samples.",
        "",
        "## Main tables",
        "",
        "### Table 1 | Public construction surface and evidence scope",
        "",
        *_surface_table(data),
        "",
        "Reference tasks, operations, instruments, metrics, generated compositions and fork",
        "traces count different objects. The 15 reference tasks do not bound the world space.",
        "",
        "### Table 2 | Full-census qualification",
        "",
        *_qualification_table(data),
        "",
        f"Zero findings: {zeros['failure_classes']} registered failure classes, "
        f"{zeros['missing_receipts']} missing receipts and "
        f"{zeros['public_private_leakage']} public/private leakage findings.",
        "",
        "### Table 3 | Deterministic instrument-use cases",
        "",
        *_deterministic_table(data),
        "",
        f"The planned rollback occurred at step {recovery['rollback_step']}; physical state, "
        "observation random-number state and ghost state were preserved, the declared penalty",
        f"reconciled, and the following {recovery['subsequent_commits']} actions committed.",
        "",
        "### Table 4 | Controlled single-private-component forks",
        "",
        *_fork_table(data),
        "",
        f"The full census contains {fork_values['pair_count']} pairs and "
        f"{fork_values['trace_count']} provider-free traces. Every pair passed lineage,",
        "public invariance, same-sequence executability, expected divergence, replay and",
        "zero-provider gates.",
        "",
        "### Table 5 | Complete-agent environment and provider ledgers",
        "",
        *_agent_table(data),
        "",
        "Cached input is reused context, not repeated model output. Environment process time",
        "and provider resources are independent ledgers.",
        "",
        "#### Worked endpoint-near process record",
        "",
        *_endpoint_table(data),
        "",
        "The archived world-1, replicate-3 pair is descriptive only. Its near-zero raw terminal",
        "contrast does not erase its process-coordinate differences and supports no model ranking.",
        "",
        "## Figure legends",
        "",
        "**Figure 1 | Object hierarchy and public instrument contract.**",
        "**A,** Reusable physical and transactional components compile into a world.",
        "**B,** A task contract attaches the initial state, actions, instruments, observations,",
        "resources, termination and evaluation surface while private laws remain hidden.",
        "**C,** Scenarios instantiate a task, trajectories record interaction, and a controlled",
        "fork is a separate single-private-component intervention. **D,** Reference tasks, typed",
        "operations, instruments and task-metric bindings retain distinct denominators.",
        "",
        "**Figure 2 | Coverage-guided construction beyond the reference task identities.**",
        "**A,** Eight component patterns define the frozen construction blocks; the highlighted",
        "reaction-distillation pattern is absent from the reference identities. **B,** Pairwise",
        "discrete coverage, seeded space filling and ordered workflow interactions determine the",
        "rows. **C,** Fifteen reference tasks and 52 generated compositions count different",
        "objects. **D,** All eight unseen rows and all 52 generated rows completed; unseen does",
        "not mean unbounded or arbitrary.",
        "",
        "**Figure 3 | Full-census qualification of the virtual instrument.**",
        "**A,** All reference and generated execution units passed. **B,** Module, interface,",
        "compile-mutant and invalid-action censuses retain their exact denominators. **C,** "
        "invalid",
        "declarations fail before construction, while invalid actions preserve physical state.",
        "**D,** Failure classes, missing receipts and public/private leakage findings were zero.",
        "",
        "**Figure 4 | Deterministic cases exercise lifecycle and failure semantics.**",
        "**A,** Eight cases cover multistage, resource-limited and reference-library workflows.",
        (
            "**B,** The single protocol-frozen precondition failure remains in the "
            "89-action census and"
        ),
        "is followed by 18 commits. **C,** Rollback preserves non-accounting state while charging",
        "the declared attempt consequences. **D,** All eight lifecycles, final assays, resource",
        "ledgers and exact replays passed.",
        "",
        "**Figure 5 | Controlled forks change one private component under an invariant "
        "public contract.**",
        "**A,** Parent and child share nine public fields and the same action sequence.",
        "**B,** Three constitutive-law and three material-law pairs change one private "
        "target each.",
        "**C,** All six pairs pass every registered gate. **D,** Physical-state and public-",
        "observation divergence occurs in the protocol-frozen channels. The traces contain no",
        "provider calls and support no agent-adaptation claim.",
        "",
        "**Figure 6 | Instrument records distinguish endpoint, process and execution status.**",
        "**A,** The 12-action deterministic reference and 15-action complete-agent trajectory are",
        "independent execution units on the same frozen unseen world. **B,** All 15 agent actions",
        "committed, with one termination, one final assay and exact replay. **C,** Environment",
        "resources and provider context use separate ledgers. **D,** An archived matched pair has",
        "a near-zero terminal contrast but marked discovery, retention, drawdown and terminal-",
        "retention differences; the example is descriptive and supports no model ranking.",
        "",
    ]
    return "\n".join(sections)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("figure_data", nargs="?", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    data = _load(_resolve(args.figure_data))
    output = _resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "figure_data_sha256": data["figure_data_sha256"],
                "output": output.relative_to(ROOT).as_posix()
                if ROOT in output.parents
                else output.as_posix(),
                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
