"""Read-only discovery, scientific visibility and HTTP boundaries of the explorer."""

import json
import threading
import time
import urllib.error
import urllib.request

import pytest
from apps.experiment_explorer.catalog import Catalog, evidence_mode
from apps.experiment_explorer.server import make_server


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


@pytest.fixture
def archive(tmp_path):
    report = "workstreams/flagship_tasks/reports/bound.json"
    run = "runs/development/study"
    write(
        tmp_path / "configs/current.json",
        {
            "work_ii": {"study": {"report": report, "run_root": run, "formal_result": False}},
            "duplicate": {"path": report},
            "producer": "python tool.py --output workstreams/flagship_tasks/reports/no-path.json",
        },
    )
    write(
        tmp_path / report,
        {
            "counts": {"planned": 3, "completed": 1, "failed": 1, "not_started": 1},
            "cells": [{"cell": "failure", "quality_passed": False, "failure": "retained"}],
        },
    )
    write(tmp_path / "workstreams/flagship_tasks/reports/unbound-v99.json", {"latest": True})
    row = {
        "action": {"operation": "measure"},
        "observation": {"purity": None},
        "transaction_status": "validation_failed",
        "step": 1,
    }
    for name in ("a/trajectory.jsonl", "b/opaque.jsonl"):
        path = tmp_path / run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(row) + "\n", encoding="utf-8")
    write(tmp_path / run / "provider/trajectory.jsonl", row)
    write(tmp_path / run / "stdout.jsonl", row)
    catalog = Catalog(tmp_path)
    catalog.refresh()
    return catalog


def test_bound_reports_deduplicate_and_do_not_select_newer_names(archive):
    snapshot = archive.snapshot()
    assert snapshot["counts"] == {"reports": 1, "runs": 1, "trajectories": 2}
    assert snapshot["errors"] == []
    entry = next(e for e in snapshot["entries"] if e["kind"] == "report")
    assert len(entry["bindings"]) == 2
    assert entry["mode"] == "development"
    detail = archive.detail(entry["id"])
    assert len(detail["trajectories"]) == 2
    assert detail["report"]["cells"][0]["quality_passed"] is False
    assert detail["report"]["counts"]["not_started"] == 1


def test_no_formal_claim_from_directory_or_completed_status():
    assert evidence_mode({}, "runs/formal/x") == "unspecified"
    assert evidence_mode({"status": "completed"}, "x") == "unspecified"
    assert evidence_mode({"formal_result": True}, "x") == "formal"
    assert evidence_mode({"status": "historical_withdrawn"}, "x") == "historical"


def test_bound_run_summary_and_local_batch_summary_are_visible(archive):
    summary = "runs/development/study/summary.json"
    write(archive.root / summary, {"counts": {"failed": 1}, "formal_result": False})
    current = json.loads((archive.root / "configs/current.json").read_text())
    current["run_summary"] = {"summary": summary, "run_root": "runs/development/study"}
    write(archive.root / "configs/current.json", current)
    snapshot = archive.refresh()
    assert snapshot["counts"]["reports"] == 2
    entry = next(e for e in snapshot["entries"] if e["path"] == summary)
    assert archive.detail(entry["id"])["report"]["counts"]["failed"] == 1
    local = next(e for e in snapshot["entries"] if e["kind"] == "run")
    assert archive.detail(local["id"])["metrics"] == [{"key": "counts.failed", "value": 1}]


def test_bad_jsonl_keeps_only_contiguous_prefix_and_does_not_rewrite(archive):
    file_id = next(iter(archive.files))
    path = archive.files[file_id]
    data = path.read_bytes() + b"{broken\n" + path.read_bytes()
    path.write_bytes(data)
    payload = archive.trajectory(file_id)
    assert payload["record_count"] == 1
    assert payload["errors"][0]["line"] == 2
    assert payload["records"][0]["observation"]["purity"] is None
    assert path.read_bytes() == data


def test_deleted_report_and_empty_trajectory_are_visible_errors(archive):
    report_id = next(iter(archive.reports))
    archive.reports[report_id].unlink()
    assert archive.detail(report_id)["error"]
    file_id = next(iter(archive.files))
    archive.files[file_id].write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="No playable"):
        archive.trajectory(file_id)


def test_extra_archive_and_direct_source_directory_are_supported(archive, tmp_path):
    extra = tmp_path / "external"
    write(extra / "cohort/trajectory.jsonl", {"action": {"operation": "heat"}})
    report_id = next(iter(archive.reports))
    write(archive.reports[report_id], {"cells": [{"source_directory": str(extra / "cohort")}]})
    extended = Catalog(tmp_path, [tmp_path / "runs", extra, extra])
    assert extended.refresh()["counts"]["trajectories"] == 3
    assert len(extended.detail(report_id)["trajectories"]) == 3


@pytest.fixture
def server(archive):
    server = make_server(archive, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    server.server_close()
    thread.join()


def request(base, route, data=None, headers=None):
    req = urllib.request.Request(
        base + route,
        headers=headers or {},
        data=None if data is None else json.dumps(data).encode(),
    )
    return urllib.request.urlopen(req, timeout=10)


def test_http_catalog_detail_and_trajectory_routes(server):
    with request(server, "/api/catalog") as response:
        catalog = json.load(response)
    report_id = next(e["id"] for e in catalog["entries"] if e["kind"] == "report")
    with request(server, f"/api/experiment?id={report_id}") as response:
        detail = json.load(response)
    with request(server, f"/api/trajectory?id={detail['trajectories'][0]['id']}") as response:
        assert json.load(response)["records"][0]["transaction_status"] == "validation_failed"
    with request(server, "/") as response:
        assert "实验观测台" in response.read().decode()
        assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    with request(server, "/app.mjs") as response:
        assert response.headers["Content-Type"].startswith("text/javascript")


@pytest.mark.parametrize(
    "route", ["/../api.md", "/api/trajectory?id=../../api.md", "/server.py", "/api/experiment"]
)
def test_no_arbitrary_file_reads(server, route):
    with pytest.raises(urllib.error.HTTPError) as exc:
        request(server, route)
    assert exc.value.code == 404


@pytest.mark.parametrize(
    "headers", [{"Origin": "https://external.example"}, {"Host": "external.example"}]
)
def test_loopback_host_and_origin_required(server, headers):
    with pytest.raises(urllib.error.HTTPError) as exc:
        request(server, "/api/catalog", headers=headers)
    assert exc.value.code == 403


def test_verification_exception_is_not_reported_as_a_pass(server, archive, monkeypatch):
    import chemworld.eval.verify

    def fail(*args, **kwargs):
        raise ValueError("Missing original world intervention")

    monkeypatch.setattr(chemworld.eval.verify, "verify_records", fail)
    with request(server, "/api/verify", {"id": next(iter(archive.files))}) as response:
        job_id = json.load(response)["id"]
    for _ in range(50):
        with request(server, f"/api/verification?id={job_id}") as response:
            result = json.load(response)
        if result["status"] != "running":
            break
        time.sleep(0.02)
    assert result["status"] == "error"
    assert "Missing original world intervention" in result["error"]


def test_long_windows_paths_can_be_indexed_and_read(tmp_path):
    from apps.experiment_explorer.catalog import disk_path

    write(tmp_path / "configs/current.json", {})
    root = tmp_path / "runs" / ("a" * 95) / ("b" * 95) / ("c" * 40)
    disk_path(root).mkdir(parents=True)
    disk_path(root / "trajectory.jsonl").write_text(
        '{"action":{"operation":"measure"}}\n', encoding="utf-8"
    )
    catalog = Catalog(tmp_path)
    catalog.refresh()
    # os.walk itself must also support a directory beyond MAX_PATH.
    assert len(catalog.files) == 1
    assert catalog.trajectory(next(iter(catalog.files)))["record_count"] == 1


def test_recording_summary_exposes_real_groups_and_preserves_unfinished_batch(archive):
    file_id = next(iter(archive.files))
    rows = [
        {
            "step": 1,
            "campaign_id": "c",
            "experiment_index": 0,
            "action": {"operation": "terminate"},
            "transaction_status": "committed",
        },
        {
            "step": 2,
            "campaign_id": "c",
            "experiment_index": 0,
            "action": {"operation": "measure", "instrument": "final_assay"},
            "transaction_status": "committed",
        },
        {
            "step": 3,
            "campaign_id": "c",
            "experiment_index": 1,
            "action": {"operation": "heat"},
            "transaction_status": "validation_failed",
        },
    ]
    archive.files[file_id].write_text("\n".join(map(json.dumps, rows)), encoding="utf-8")
    summary = archive.recording_summaries([file_id])[file_id]
    assert (summary["experiments"], summary["steps"], summary["final_assays"]) == (2, 3, 1)
    assert summary["failed_transactions"] == 1
    archive.files[file_id].write_text(json.dumps(rows[0]), encoding="utf-8")
    assert archive.recording_summaries([file_id])[file_id]["steps"] == 1


def test_receipts_include_final_output_but_not_evaluator_state_or_credentials(archive):
    file_id = next(iter(archive.files))
    directory = archive.files[file_id].parent
    write(
        directory / "summary.json",
        {
            "provider_receipts": [{"final_payload": {"conclusion": "saved"}}],
            "private_seed": 999,
            "api_key": "not-for-display",
        },
    )
    write(directory / "evaluator_states.json", {"hidden_truth": "excluded"})
    context = archive.trajectory(file_id)["context"]
    assert context["summary.json"]["provider_receipts"][0]["final_payload"]["conclusion"] == "saved"
    assert "private_seed" not in str(context)
    assert "not-for-display" not in str(context)
    assert "hidden_truth" not in str(context)


def test_http_recording_summary_and_viewer_assets(server, archive):
    file_id = next(iter(archive.files))
    with request(server, f"/api/recordings?id={file_id}") as response:
        assert json.load(response)[file_id]["experiments"] == 1
    for asset in ("/viewer.mjs", "/viewer.css"):
        with request(server, asset) as response:
            assert response.status == 200


def test_categories_come_from_task_records_and_bound_roots(archive):
    from apps.experiment_explorer.categories import categories_in, recorded_categories

    ids = list(archive.files)
    write(
        archive.files[ids[0]],
        {"task_id": "reaction-to-crystallization", "action": {"operation": "heat"}},
    )
    write(
        archive.files[ids[1]],
        {"benchmark_task_id": "electrochemical-conversion", "action": {"operation": "heat"}},
    )
    result = archive.refresh()
    for entry in result["entries"]:
        assert entry["categories"] == ["electrochemistry", "crystallization"]
    assert categories_in({"results": {"reaction-to-distillation": {"failed": 1}}}) == {
        "distillation"
    }
    assert categories_in("version99-crystal-summary") == set()
    assert recorded_categories(
        {
            "task_id": "reaction-to-crystallization",
            "prompt": "Other task examples include reaction-to-distillation",
        }
    ) == {"crystallization"}


def test_one_shot_plans_label_members_without_combining_matrix_files(tmp_path):
    write(tmp_path / "configs/current.json", {})
    run = tmp_path / "runs/development/study"
    recipes = {"R1C1_0": {"temperature_K": 310}, "R2C2_0": {"temperature_K": 320}, "missing": {}}
    write(
        run / "model/acquire_standard_0/result.json",
        {
            "name": "acquire_standard_0",
            "model": "saved-planner",
            "payload": recipes,
        },
    )
    for name in ("R1C1_0", "R2C2_0", "unplanned"):
        write(
            run / f"physical/source/standard/0/{name}/trajectory.jsonl",
            {
                "task_id": "reaction-to-crystallization",
                "action": {"operation": "heat"},
            },
        )
    catalog = Catalog(tmp_path)
    catalog.refresh()
    detail = catalog.detail(next(iter(catalog.entries)))
    assert "groups" not in detail
    assert len(detail["trajectories"]) == 3
    meta = catalog.recording_summaries(list(catalog.files))
    for file_id, path in catalog.files.items():
        member = path.parent.name
        payload = catalog.trajectory(file_id)
        assert payload["record_count"] == 1
        if member == "unplanned":
            assert "planning" not in payload["context"]
            assert "planning" not in meta[file_id]
        else:
            planning = payload["context"]["planning"]
            assert planning["member"] == member
            assert planning["plan"] == recipes[member]
            assert planning["planned"] == 3
            assert meta[file_id]["planning"]["kind"] == "one_shot_plan"
            assert "plan" not in meta[file_id]["planning"]
