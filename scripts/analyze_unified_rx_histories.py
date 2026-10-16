"""Export public RX records and validate separately authored semantic readings.

Reading a JSON file here is extraction, not semantic close reading. This program
never calls a participant or simulator and never edits retained experiment data.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "workstreams/flagship_tasks/reports/unified-matrices-20261016/process/RX"
STAGES = ("K1", "Q", "K2")
EVENT_FIELDS = (
    "event_id",
    "action",
    "transaction_status",
    "ok",
    "observation",
    "state_delta_summary",
    "sample_consumed",
    "completed_ordinal",
    "lifecycle_experiment_index",
    "experiment_ended",
    "batch_discarded",
    "campaign_terminal_reason",
    "constraint_flags",
)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def export():
    binding = read(ROOT / "configs/current.json")["work_ii"]["w2_267_unified_matrices"]
    raw = Path(binding["run_root"])
    design = read(raw / "design.json")
    units = [u for u in design["schedule"] if u["system"] == "RX"]
    assert len(units) == 90
    index = []
    for unit in units:
        key = f"{unit['repeat']}/{unit['id']}"
        base = Path(design.get("retained_units", {}).get(key, raw / key))
        result = read(base / "result.json")
        source = Path(result["source_dir"])
        versions = [
            read(p)
            for p in sorted(
                (source / "notebook/experiment_documents/notebook_history").glob("*.json")
            )
        ]
        events = [
            json.loads(line)
            for line in (source / "workspace/public/operation_history.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]
        task = read(source / "workspace/reference/task_contract.json")
        prior = read(source / "public-prior-binding.json")
        payloads = {
            stage: result.get("posttests", {}).get(stage, {}).get("payload") for stage in STAGES
        }
        public = {
            "unit": unit,
            "provenance": {
                "result": str(base / "result.json"),
                "public_source": str(source),
                "resolved_via_retained_units": key in design.get("retained_units", {}),
            },
            "status": result["status"],
            "research_goal": task.get("research_goal", task.get("description")),
            "initial_information": prior,
            "source_instructions": (source / "source-instructions.txt").read_text(encoding="utf-8"),
            "posttest_prompts": {
                stage: (source / stage / "prompt.txt").read_text(encoding="utf-8")
                if (source / stage / "prompt.txt").exists()
                else None
                for stage in STAGES
            },
            "versions": [
                {
                    k: v[k]
                    for k in ("revision", "public_cursor", "text", "kind", "reviewed_through")
                    if k in v
                }
                for v in versions
            ],
            "events": [{k: e[k] for k in EVENT_FIELDS if k in e} for e in events],
            "batches": result["source"]["batches"],
            "posttests": payloads,
            "posttest_validation": result.get("posttest_validation"),
            "prediction_evaluation": result.get("prediction_evaluation"),
            "recommendation": result.get("recommendation"),
            "recommendation_retest": {
                "batches": result.get("recommendation_retest", {}).get("batches", [])
            },
        }
        path = OUT / "sources" / unit["repeat"] / (unit["id"] + ".json")
        write(path, public)
        index.append(
            {
                **unit,
                "source": path.relative_to(ROOT).as_posix(),
                "versions": len(versions),
                "events": len(events),
                "assays": len(public["batches"]),
                "posttests_present": [s for s in STAGES if payloads[s]],
                "extracted": True,
                "semantically_reviewed": False,
            }
        )
    write(
        OUT / "inventory.json",
        {
            "scope": "RX90 retained effective sessions only",
            "extraction_is_not_close_reading": True,
            "units": index,
        },
    )
    print(f"Exported {len(index)}/90 public records; semantic status is separate.")


def load(repeat: str, ident: str):
    return read(OUT / "sources" / repeat / (ident + ".json"))


def anchor(source, stage, quote, revision=None, query_id=None):
    out = {"stage": stage, "quote": quote}
    if stage == "notebook":
        note = next(v for v in source["versions"] if v["revision"] == revision)
        out.update(revision=revision, public_cursor=note["public_cursor"])
        assert quote in note["text"]
    else:
        payload = source["posttests"][stage]
        if query_id:
            payload = next(v for v in payload["predictions"] if v["query_id"] == query_id)
            out["query_id"] = query_id
        assert any(quote in s for s in strings(payload))
    return out


def save_reading(source, analysis):
    unit = source["unit"]
    value = {
        "unit": unit,
        "review_scope": {
            "status": "full_public_record_close_reading",
            "notebook_revisions": [v["revision"] for v in source["versions"]],
            "public_operations": len(source["events"]),
            "source_batches": len(source["batches"]),
            "sealed_stages": [s for s in STAGES if source["posttests"][s]],
            "kind": "internal_AI_assisted_semantic_reading_not_independent_human_validation",
        },
        **analysis,
    }
    write(OUT / "readings" / unit["repeat"] / (unit["id"] + ".json"), value)


def anchors(value):
    if isinstance(value, dict):
        if "stage" in value and "quote" in value:
            yield value
        for item in value.values():
            yield from anchors(item)
    elif isinstance(value, list):
        for item in value:
            yield from anchors(item)


def summarize():
    inventory = read(OUT / "inventory.json")["units"]
    reviewed, issues, counts = [], [], Counter()
    invalid_stages = []
    for unit in inventory:
        path = OUT / "readings" / unit["repeat"] / (unit["id"] + ".json")
        if not path.exists():
            continue
        review = read(path)
        source = load(unit["repeat"], unit["id"])
        for index, a in enumerate(anchors(review)):
            try:
                checked = anchor(
                    source, a["stage"], a["quote"], a.get("revision"), a.get("query_id")
                )
                if a.get("public_cursor") != checked.get("public_cursor"):
                    raise ValueError("cursor mismatch")
                counts["verified_anchors"] += 1
            except (AssertionError, KeyError, StopIteration, ValueError):
                issues.append({"repeat": unit["repeat"], "id": unit["id"], "anchor": index})
        reviewed.append(
            {
                "repeat": unit["repeat"],
                "id": unit["id"],
                "reading": path.relative_to(ROOT).as_posix(),
            }
        )
        counts["notebook_versions_read"] += len(source["versions"])
        counts["public_operations_read"] += len(source["events"])
        counts["source_assays_read"] += len(source["batches"])
        counts["sealed_stages_read"] += sum(bool(source["posttests"][s]) for s in STAGES)
        for stage in STAGES:
            validation = source["posttest_validation"].get(stage, {})
            if validation.get("valid"):
                counts["valid_sealed_stages"] += 1
            else:
                invalid_stages.append(
                    {
                        "repeat": unit["repeat"],
                        "id": unit["id"],
                        "stage": stage,
                        "failure": validation.get("failure"),
                        "payload_present": bool(source["posttests"][stage]),
                    }
                )
        for event in source["events"]:
            counts["operations_" + event["transaction_status"]] += 1
            if event["action"].get("instrument") == "hplc":
                counts["hplc_operations_read"] += 1
    summary = {
        "planned_sessions": 90,
        "extracted_sessions": len(inventory),
        "reviewed_sessions": len(reviewed),
        "status": "complete" if len(reviewed) == 90 and not issues else "in_progress",
        **counts,
        "issues": issues,
        "invalid_sealed_stages": invalid_stages,
        "reviewed": reviewed,
        "interpretation": (
            "Only authored per-session records count as close reading. "
            "Selected histories are not an abduction success rate. "
            "sealed_stages_read counts available payloads, including invalid ones; "
            "valid_sealed_stages retains protocol validation."
        ),
    }
    write(OUT / "reading-summary.json", summary)
    print(
        json.dumps(
            {k: v for k, v in summary.items() if k != "reviewed"}, ensure_ascii=False, indent=2
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("export", "summarize"))
    args = parser.parse_args()
    if args.command == "export":
        export()
    else:
        summarize()


if __name__ == "__main__":
    main()
