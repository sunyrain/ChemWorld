"""Read-only resource accounting for scientific and technical W2-263 blocks.

CLI receipt usage is cumulative within a resumed thread. Never sum source,
K1, Q and K2 token counters. No provider payload or credential is exported.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.run_paper_case_notebooks import case_folder, read, write

TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens")
OPTIONAL_KEYS = ("cache_write_input_tokens", "reasoning_output_tokens")
SOURCE_KEYS = {
    "input_tokens": "prompt_tokens",
    "cached_input_tokens": "prompt_cache_hit_tokens",
    "output_tokens": "completion_tokens",
    "cache_write_input_tokens": "prompt_cache_write_tokens",
    "reasoning_output_tokens": "reasoning_output_tokens",
}


def normalized_usage(receipt):
    if receipt.get("usage_observed") is False or receipt.get("usage_complete") is False:
        return None
    usage = receipt.get("usage") or {}
    source_format = "prompt_tokens" in usage
    values = {
        key: usage.get(SOURCE_KEYS[key] if source_format else key)
        for key in (*TOKEN_KEYS, *OPTIONAL_KEYS)
    }
    valid = all(
        isinstance(values[k], int) and not isinstance(values[k], bool) and values[k] >= 0
        for k in TOKEN_KEYS
    )
    return values if valid else None


def chain_summary(identifier, stages, *, terminal, failure=None, source_usage=None):
    """Retain last observed cumulative receipt; missing/failed chains stay incomplete."""
    previous, previous_stage, last, thread = None, None, None, None
    missing, violations, rows = [], [], []
    elapsed = []
    for name, receipt in stages:
        usage = normalized_usage(receipt)
        current_thread = receipt.get("thread_id")
        if thread is not None and current_thread != thread:
            violations.append({"stage": name, "issue": "thread_identity_changed_or_missing"})
        if thread is None:
            thread = current_thread
        if not current_thread:
            missing.append({"stage": name, "field": "thread_id"})
        delta = None
        if usage is None:
            missing.append({"stage": name, "field": "usage"})
        else:
            if previous is not None:
                delta = {
                    key: usage[key] - previous[key]
                    if usage[key] is not None and previous[key] is not None
                    else None
                    for key in usage
                }
                for key, value in delta.items():
                    if value is not None and value < 0:
                        violations.append(
                            {"stage": name, "field": key, "issue": "cumulative_counter_decreased"}
                        )
            elif not rows:
                delta = usage.copy()
            last = {"stage": name, "tokens": usage}
        elapsed_s = receipt.get("elapsed_s", receipt.get("session_elapsed_s"))
        if isinstance(elapsed_s, (int, float)):
            elapsed.append(elapsed_s)
        rows.append(
            {
                "stage": name,
                "raw_cumulative_usage": receipt.get("usage"),
                "normalized_cumulative_tokens": usage,
                "increment_since_previous_receipt": delta,
                "previous_stage": previous_stage,
                "failure": receipt.get("failure"),
                "elapsed_s": elapsed_s,
            }
        )
        previous, previous_stage = usage, name
    stage_failures = any(row["failure"] for row in rows)
    complete = bool(terminal and rows and not failure and not missing and not violations)
    complete = complete and not stage_failures
    observed = last["tokens"] if last and not violations else None
    return {
        "unit": identifier,
        "terminal": terminal,
        "failure": failure,
        "logical_cli_receipts_observed": len(rows),
        "source_process_attempts_observed": (source_usage or {}).get(
            "provider_process_attempt_count"
        ),
        "source_logical_cli_turns_observed": (source_usage or {}).get("logical_codex_turn_count"),
        "backend_api_requests": None,
        "backend_api_requests_accounting_complete": False,
        "latest_observed_cumulative_receipt": last,
        "observed_cumulative_tokens": observed,
        "total_tokens": observed if complete else None,
        "token_accounting_complete": complete,
        "missing_fields": missing,
        "monotonicity_or_thread_issues": violations,
        "observed_receipt_elapsed_sum_s": sum(elapsed) if elapsed else None,
        "elapsed_sum_is_parallel_wall_time": False,
        "monetary_cost_usd": None,
        "monetary_accounting_complete": False,
        "monetary_unavailable_reason": "Subscription access has no attributable per-unit USD price",
        "stages": rows,
    }


def read_stages(private, followups):
    stages = []
    source = private / "source-receipts.json"
    if source.exists():
        for index, receipt in enumerate(read(source), 1):
            stages.append((f"source-{index}", receipt))
    for name in followups:
        path = private / name / "receipt.json"
        if path.exists():
            stages.append((name, read(path)))
    return stages


def aggregate(name, purpose, planned, chains, *, not_started=0):
    known = [r["observed_cumulative_tokens"] for r in chains if r["observed_cumulative_tokens"]]
    observed = {
        key: sum(r[key] for r in known if r[key] is not None)
        if known and all(r[key] is not None for r in known)
        else None
        for key in (*TOKEN_KEYS, *OPTIONAL_KEYS)
    }
    complete = bool(chains) and all(r["token_accounting_complete"] for r in chains)
    return {
        "block": name,
        "purpose": purpose,
        "planned_units": planned,
        "started_units": len(chains),
        "not_started_units": not_started,
        "terminal_units": sum(r["terminal"] for r in chains),
        "units_with_observed_cumulative_tokens": len(known),
        "units_with_incomplete_token_accounting": sum(
            not r["token_accounting_complete"] for r in chains
        ),
        "logical_cli_receipts_observed": sum(r["logical_cli_receipts_observed"] for r in chains),
        "observed_tokens_from_latest_receipts": observed if known else None,
        "total_tokens_for_started_units": observed if complete else None,
        "token_accounting_complete_for_started_units": complete,
        "planned_block_complete": complete and len(chains) == planned,
        "backend_api_requests": None,
        "monetary_cost_usd": None,
        "monetary_accounting_complete": False,
        "chains": chains,
    }


def participant_group(root, purpose):
    design = read(root / "design.json")
    stop_path = root / "block-stop.json"
    stopped = read(stop_path) if stop_path.exists() else {}
    chains, not_started = [], 0
    for unit in design["schedule"]:
        result_path = root / unit["repeat"] / "results" / f"{unit['id']}.json"
        folder = case_folder(root / unit["repeat"], unit)
        worker_failed = stopped.get("unit") == [unit["repeat"], unit["id"]]
        if not folder.exists() and not result_path.exists() and not worker_failed:
            not_started += 1
            continue
        result = read(result_path) if result_path.exists() else {}
        stages = read_stages(folder / "private-provider", ("K1", "Q", "K2"))
        failure = result.get("failure") or (stopped.get("reason") if worker_failed else None)
        chains.append(
            chain_summary(
                f"{unit['repeat']}/{unit['id']}",
                stages,
                terminal=result_path.exists() or worker_failed,
                failure=failure,
                source_usage=result.get("source_usage"),
            )
        )
    return aggregate(root.name, purpose, len(design["schedule"]), chains, not_started=not_started)


def canary_group(root):
    result = read(root / "result.json")
    chains = []
    for unit in result["results"]:
        folder = root / f"unit-{unit['unit']}"
        chains.append(
            chain_summary(
                folder.name,
                read_stages(folder / "private-provider", ("K1",)),
                terminal=True,
                failure=unit.get("failure"),
                source_usage=unit.get("source_usage"),
            )
        )
    return aggregate(
        root.name, "technical runtime canary; excluded from scientific evidence", 4, chains
    )


def transport_group(root):
    stages = [(name, read(root / name / "receipt.json")) for name in ("initial", "continued")]
    chain = chain_summary("two-turn-transport", stages, terminal=True)
    return aggregate(
        root.name, "technical transport probe; excluded from scientific evidence", 1, [chain]
    )


def summarize(args):
    groups = [participant_group(args.participant, "current scientific participant cohort")]
    groups += [
        participant_group(p, "retained technical startup attempt") for p in args.retained_attempt
    ]
    groups += [canary_group(p) for p in args.canary]
    groups += [transport_group(p) for p in args.transport]
    summary = {
        "method": (
            "Within a verified single thread, use the last observed cumulative receipt, "
            "never the sum of stage counters"
        ),
        "incomplete_accounting": (
            "Observed partial counters are retained separately; "
            "unknown totals and costs are null, never zero"
        ),
        "count_units": (
            "CLI receipts and source process attempts are host-side observations, "
            "not backend API request counts"
        ),
        "elapsed_semantics": (
            "Sum of observed receipt durations is cumulative session time, "
            "not measured compute time or wall time under parallel execution"
        ),
        "groups": groups,
    }
    write(args.report, summary)
    for group in groups:
        print(
            f"{group['block']}: {group['terminal_units']}/{group['started_units']} terminal; "
            f"{group['units_with_observed_cumulative_tokens']} token observations; "
            f"{group['units_with_incomplete_token_accounting']} incomplete accounts",
            flush=True,
        )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--participant", type=Path, required=True)
    parser.add_argument("--retained-attempt", type=Path, action="append", default=[])
    parser.add_argument("--canary", type=Path, action="append", default=[])
    parser.add_argument("--transport", type=Path, action="append", default=[])
    parser.add_argument("--report", type=Path, required=True)
    summarize(parser.parse_args())


if __name__ == "__main__":
    main()
