"""Bounded R51 workflow comparison; development-notebook-utility-20261012.md."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from scripts import run_hypothesis_notebook_pilot as base
from scripts import run_long_horizon_notebook_review as review
from scripts import run_notebook_access_pilot as access

from chemworld.providers.codex_subscription import CodexSubscriptionClient

ORDER = (("H", 1), ("N", 1), ("N", 2), ("H", 2), ("H", 3), ("N", 3), ("N", 4), ("H", 4))
BATCHES = 4
TOOL_BUDGET = 36
TASK = """Conduct FOUR independent physical batches as one continuing research programme
in a finite anonymous chemical simulator. Each batch starts a NEW conversation. Physical
laws and starting states stay fixed; observation noise streams differ. Each batch has
its own resource ledger. Choose recipes, controls, repeats and measurements yourself.
Investigate a controllable process-condition relationship with final yield and selectivity,
and test its scope. A higher yield alone does not establish a general relationship.

Make your research understandable to a human reviewer. In the reason for your FIRST
physical action, state the current question, why you chose this experiment, and a testable
expectation or competing expectations (uncertainty is acceptable). After consequential
evidence, give concise public scientific reasons for changed or retained decisions.
Your final report should link findings to exact public event IDs, discuss scope/confounds,
and state the next decision, or the final synthesis in batch four. Do not invent evidence,
backdate predictions or describe unperformed plans as results. No private chain-of-thought.
Records are not scored by word count; choose concise useful scientific commitments.

Your public history, original public artifacts and submitted final reports persist within
your own research programme. All bodies are ON DEMAND, never preloaded. lab_history holds
facts, not interpretations; lab_reports lists earlier report metadata or reads a selected
batch. Reports are your own fallible interpretations, not authoritative observations.
Choose what to retrieve when helpful. Do not assume a planned experiment was performed.

Only public chemworld tools may be used. Media and spectra are synthetic proxies, not real
chemical structures. Interpret numerical differences with uncertainty and confounds;
do not invent error bars or infer hidden mechanisms. Distinguish a matching recipe/target
temperature from a complete operation repeat, including sampling and instrument settings.
Each batch allows 24 physical attempts including rejections, 36 total tool requests and
300 seconds. Reserve requests for termination, final assay and reporting. Query needed
schemas together. lab_history limit is at most 10; use offsets or exact event_ids.
lab_artifact can select public fields such as observation, uncertainty or spectral_fit.
Spectral fit uncertainties concern their stated quantities, not automatically yield.
Finish ordinary measurements BEFORE terminate; then measure(instrument=final_assay).
Call finish_batch(report=...) and stop all tools. If unable to finish, explain the missing
work. Batch four is the last batch; do not rely on extra experiments. If transport closes,
report it and stop; do not repeatedly call an unavailable server.
"""
NOTE_TASK = """
You also maintain a concise versioned hypothesis notebook FOR HUMAN UNDERSTANDING AND
REVIEW. Before the first physical action record the question/expectation and choice;
after consequential evidence revise the interpretation or explain why it is retained;
at batch end leave evidence-linked findings, scope, uncertainties and the next decision.
Use ordinary Markdown; do not duplicate the entire history. Reading/log/diff/restore are
your choice, never mandatory. Avoid re-reading content already in context. A restore
creates a new revision and cannot undo experiments. Missing notes do not lock the lab.
You may pass your complete updated notebook as finish_batch(notebook_text=...) to save
the terminal interpretation with the report. Notes and reports remain distinct artifacts.
"""


class UtilityHost(access.AccessHost):
    def __init__(self, root: Path, arm: str, batch: int, deadline: float):
        self.arm = arm
        base.PilotHost.__init__(
            self,
            root,
            batch,
            tool_budget=TOOL_BUDGET,
            deadline=deadline,
            seed=0,
            observation_seed=4000 + batch,
        )

    def status(self) -> dict[str, Any]:
        return {
            **super().status(),
            "planned_batches": BATCHES,
            "later_batches_remaining": BATCHES - self.batch,
        }


def command(client, root: Path, arm: str, batch: int, deadline: float) -> list[str]:
    args = base.cli_command(client, root, batch, TOOL_BUDGET, deadline)
    for i, arg in enumerate(args):
        if arg.startswith("mcp_servers.chemworld.args="):
            args[i] = "mcp_servers.chemworld.args=" + json.dumps(
                [
                    "-m",
                    "scripts.run_notebook_utility_study",
                    "--serve",
                    "--output",
                    root.as_posix(),
                    "--arm",
                    arm,
                    "--batch",
                    str(batch),
                    "--deadline",
                    str(deadline),
                ]
            )
    folder = root / "provider" / f"session-{batch}"
    (folder / "instructions.md").write_text(
        TASK + (NOTE_TASK if arm == "N" else ""), encoding="utf-8"
    )
    (folder / "prompt.txt").write_text(
        f"Conduct batch {batch} of {BATCHES}. Start with lab_status. "
        + (
            "Your own research starts with empty records."
            if batch == 1
            else "New conversation; your earlier public facts and reports are available on demand."
        ),
        encoding="utf-8",
    )
    base.save(folder / "command.json", args)
    return args


def summarize(root: Path, batch: int, provider: dict) -> dict:
    result = review.summarize_batch(root, batch, provider)
    events = [e for e in base.records(root / "interactions.jsonl") if e["batch"] == batch]
    result["retrievals"] = [
        {
            "call": e["call"],
            "tool": e["tool"],
            "arguments": e["arguments"],
            "failed": "error" in e["result"],
        }
        for e in events
        if e["tool"]
        in {
            "lab_history",
            "lab_reports",
            "lab_artifact",
            "notebook_read",
            "notebook_log",
            "notebook_diff",
        }
    ]
    result["first_physical_call"] = next(
        (e["call"] for e in events if e["tool"] == "lab_step"), None
    )
    return result


def write_outputs(root: Path, summary: dict) -> None:
    base.save(root / "summary.json", summary)
    lines = [
        "# R51 research review",
        "",
        "Verbatim public commitments, notes and reports; no private reasoning. "
        "An existing citation does not establish scientific support.",
        "",
    ]
    public = {
        k: summary.get(k)
        for k in (
            "formal_result",
            "planned_batches",
            "completed_batches",
            "total_tokens",
            "failures",
            "elapsed_s",
        )
    }
    public["arms"] = {}
    for arm in ("H", "N"):
        series = summary["arms"][arm]
        by_batch = {b["batch"]: b for b in series["batches"]}
        public["arms"][arm] = {"total_tokens": series["total_tokens"], "batches": []}
        notes = review.notebook_timeline(root / arm)
        lines += [f"## {arm}", ""]
        for batch in range(1, BATCHES + 1):
            b = by_batch.get(batch)
            lines += [f"### Batch {batch}", ""]
            if b is None:
                lines += ["Not executed.", ""]
                public["arms"][arm]["batches"].append({"batch": batch, "executed": False})
                continue
            lines += [
                f"Engineering completed: {b['engineering_passed']}",
                "",
                "Retrievals: " + json.dumps(b["retrievals"], ensure_ascii=False),
                "",
            ]
            for note in (n for n in notes if n["batch"] == batch):
                lines += [
                    f"#### Note v{note['revision']} / call {note['call']}",
                    "",
                    note["record"]["text"],
                    "",
                ]
            lines += ["#### Actual actions and public reasons", ""]
            lines += [
                f"{i}. `{json.dumps(a['action'], ensure_ascii=False)}` — {a['reason']}"
                for i, a in enumerate(b["actual_actions_and_reasons"], 1)
            ]
            lines += [
                "",
                "#### Submitted report",
                "",
                b["host"].get("report", "Not submitted."),
                "",
                "#### Last CLI public message (not a substitute for accepted report)",
                "",
                b.get("cli_last_public_message") or "None",
                "",
            ]
            public["arms"][arm]["batches"].append(
                {
                    "batch": batch,
                    "executed": True,
                    "engineering_passed": b["engineering_passed"],
                    "steps": b["host"].get("steps", 0),
                    "actions": b["host"].get("actions", []),
                    "quality": b["host"].get("quality", []),
                    "replay": b["replay"],
                    "errors": b["host"].get("errors", []),
                    "retrievals": b["retrievals"],
                    "tool_counts": b["host"].get("tool_counts", {}),
                    "pre_first_action_revisions": b["pre_first_action_revisions"],
                    "post_last_action_revisions": b["post_last_action_revisions"],
                    "reference_issues": [
                        {
                            "revision": n["revision"],
                            "missing": n["unavailable_references_at_commit"],
                        }
                        for n in b["reference_issues"]
                    ],
                    "measurements": b["measurements"],
                    "final_observation": b["final_observation"],
                    "provider": {
                        k: b["provider"].get(k)
                        for k in (
                            "usage",
                            "usage_complete",
                            "total_tokens",
                            "exit_code",
                            "stop_reason",
                            "elapsed_s",
                        )
                    },
                    "transport_failure_count": len(b["provider"].get("transport_failures", [])),
                }
            )
    (root / "review.md").write_text("\n".join(lines), encoding="utf-8")
    base.save(root / "aggregate.json", public)


def run(root: Path) -> dict:
    root.mkdir(parents=True, exist_ok=False)
    started = time.time()
    summary = {
        "formal_result": False,
        "planned_batches": len(ORDER),
        "completed_batches": 0,
        "total_tokens": 0,
        "failures": [],
        "arms": {
            a: {"batches": [], "total_tokens": 0, "elapsed_s": 0.0, "stopped": False}
            for a in ("H", "N")
        },
    }
    write_outputs(root, summary)
    try:
        client = CodexSubscriptionClient(model="gpt-5.6-sol", max_attempts=1)
        for arm, batch in ORDER:
            series = summary["arms"][arm]
            if series["stopped"]:
                continue
            if series["elapsed_s"] >= 1200 or series["total_tokens"] >= 2000000:
                series["stopped"] = True
                summary["failures"].append(
                    {"arm": arm, "before_batch": batch, "type": "budget_stop"}
                )
                continue
            deadline = time.time() + min(300, 1200 - series["elapsed_s"])
            args = command(client, root / arm, arm, batch, deadline)
            provider = review.run_session(
                client,
                root / arm,
                arm,
                batch,
                deadline,
                summary["completed_batches"],
                started,
                command_args=args,
                planned_batches=len(ORDER),
                tool_budget=TOOL_BUDGET,
            )
            b = summarize(root / arm, batch, provider)
            series["batches"].append(b)
            series["total_tokens"] += provider["total_tokens"]
            series["elapsed_s"] += provider["elapsed_s"]
            summary["total_tokens"] += provider["total_tokens"]
            summary["completed_batches"] += int(b["engineering_passed"])
            if not b["engineering_passed"]:
                summary["failures"].append(
                    {"arm": arm, "batch": batch, "type": "incomplete_or_failed_batch"}
                )
            shared_fault = bool(
                b["host"].get("host_exception")
                or (b["replay"] and not b["replay"].get("verified"))
                or (b["host"].get("actions") and not b["quality_passed"])
            )
            series["stopped"] = bool(
                shared_fault
                or not provider["usage_complete"]
                or provider["transport_failures"]
                or (provider["exit_code"] and not provider["stop_reason"])
            )
            if series["stopped"]:
                summary["failures"].append({"arm": arm, "batch": batch, "type": "runtime_stop"})
            summary["elapsed_s"] = time.time() - started
            write_outputs(root, summary)
            print(
                json.dumps(
                    {
                        "stage": "batch_recorded",
                        "arm": arm,
                        "batch": batch,
                        "completed": summary["completed_batches"],
                        "total": len(ORDER),
                        "total_tokens": summary["total_tokens"],
                        "shared_fault": shared_fault,
                    }
                ),
                flush=True,
            )
            if shared_fault:
                break
    except Exception as error:
        summary["failures"].append({"type": type(error).__name__, "message": str(error)})
    finally:
        summary["elapsed_s"] = time.time() - started
        summary["engineering_passed"] = (
            summary["completed_batches"] == len(ORDER) and not summary["failures"]
        )
        write_outputs(root, summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--arm", choices=("H", "N"), default="N")
    parser.add_argument("--batch", type=int, choices=range(1, BATCHES + 1), default=1)
    parser.add_argument("--deadline", type=float, default=0)
    options = parser.parse_args()
    if options.serve:
        base.serve_host(
            options.output,
            options.batch,
            lambda: UtilityHost(options.output, options.arm, options.batch, options.deadline),
            dispatcher=access.dispatch,
        )
    else:
        result = run(options.output.resolve())
        print(
            json.dumps(
                {
                    k: result[k]
                    for k in (
                        "engineering_passed",
                        "completed_batches",
                        "total_tokens",
                        "elapsed_s",
                    )
                }
            ),
            flush=True,
        )
        raise SystemExit(0 if result["engineering_passed"] else 1)
