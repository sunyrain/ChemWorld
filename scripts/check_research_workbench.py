"""Execute the fixed local workbench acceptance block, without provider calls."""

from __future__ import annotations

import argparse
import io
import json
import threading
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

from apps.research_workbench.server import WorkbenchServer

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    server = WorkbenchServer(("127.0.0.1", 0), output / "workspace")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    def request(path: str, body: Any = None, *, binary: bool = False) -> Any:
        req = urllib.request.Request(
            base + path,
            data=None if body is None else json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            return data if binary else json.loads(data)

    composition = json.loads(
        (ROOT / "examples/world-authoring/composed-reaction-assay-v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    units = [
        ("reaction", {"task_id": "reaction-to-assay"}),
        ("crystallization", {"task_id": "reaction-to-crystallization"}),
        ("continuous-flow", {"task_id": "flow-reaction-optimization"}),
        ("composition", {"composition": composition}),
    ]
    results: list[dict[str, Any]] = []
    controls: dict[str, Any] = {}
    try:
        for index, (name, design) in enumerate(units, 1):
            print(f"HTTP acceptance {index}/{len(units)}: {name}", flush=True)
            result: dict[str, Any] = {"unit": name, "failures": []}
            results.append(result)
            try:
                current = request(
                    "/api/runs",
                    {
                        "name": name,
                        "project": "Local development acceptance",
                        "question": "Fixed offline software acceptance; no scientific comparison.",
                        "design": {**design, "seed": 0, "budget": 32},
                    },
                )
                run_id = current["id"]
                result["id"] = run_id
                for action in current["recipe"]:
                    current = request(
                        f"/api/runs/{run_id}/step",
                        {
                            "action": action,
                            "expected_step": current["submitted_steps"],
                        },
                    )
                    if current["events"][-1]["transaction_status"] != "committed":
                        result["failures"].append("unexpected action rejection")
                        break
                    if current["status"] != "ready":
                        break
                result.update(
                    submitted=current["submitted_steps"],
                    rejected=current["rejected_steps"],
                    final_assays=current["final_assay_count"],
                    signal_channels=sum(len(e.get("series", [])) for e in current["events"]),
                    replay=request(f"/api/runs/{run_id}/replay", {}),
                )
                if result["final_assays"] != 1 or not result["replay"]["verified"]:
                    result["failures"].append("assay or exact replay did not pass")
                exported = request(f"/api/runs/{run_id}/export", binary=True)
                (output / f"{name}.zip").write_bytes(exported)
                with zipfile.ZipFile(io.BytesIO(exported)) as bundle:
                    result["export_entries"] = len(bundle.namelist())
                    assert "trajectory.jsonl" in bundle.namelist()
            except Exception as exc:
                result["failures"].append(f"{type(exc).__name__}: {exc}")
        control = request("/api/runs", {"name": "rejection-and-cancel"})
        run_id = control["id"]
        control = request(
            f"/api/runs/{run_id}/step",
            {
                "action": {"operation": "measure", "instrument": "hplc"},
                "expected_step": 0,
            },
        )
        controls["empty_vessel_rejected"] = control["rejected_steps"] == 1
        for text in ("Before: test hypothesis, no evidence yet.", "After: rejected measurement."):
            request(
                f"/api/runs/{run_id}/notebook",
                {
                    "author": "human",
                    "operation": "write",
                    "arguments": {"text": text},
                },
            )
        diff = request(f"/api/runs/{run_id}/notebook", {"author": "human", "operation": "diff"})
        controls["notebook_versions"] = (
            diff["after"]["revision"] == 2 and "rejected" in diff["text"]
        )
        control = request(f"/api/runs/{run_id}/cancel", {})
        controls["cancel_without_fake_assay"] = (
            control["status"] == "cancelled" and control["final_assay_count"] == 0
        )
        controls["control_id"] = run_id
    finally:
        server.shutdown()
        server.store.close()
        server.server_close()
        thread.join(3)
    reopened = WorkbenchServer(("127.0.0.1", 0), output / "workspace")
    try:
        controls["restart_retained_all_runs"] = len(reopened.store.runs) == 5
        control_run = reopened.store.get(controls["control_id"])
        controls["restart_retained_versions"] = (
            control_run.notebook("human", "read", {})["revision"] == 2
        )
    finally:
        reopened.store.close()
        reopened.server_close()
    checks = [v for v in controls.values() if isinstance(v, bool)]
    summary = {
        "development_only": True,
        "planned_units": 4,
        "completed_units": len(results),
        "passed_units": sum(not r["failures"] for r in results),
        "units": results,
        "controls": controls,
        "all_passed": all(not r["failures"] for r in results) and all(checks),
        "real_provider_requests": 0,
        "browser_visual_acceptance": "unavailable",
    }
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        json.dumps({k: v for k, v in summary.items() if k not in {"units", "controls"}}), flush=True
    )
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
