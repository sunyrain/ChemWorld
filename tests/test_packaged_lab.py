from __future__ import annotations

import json
import subprocess
import sys
import threading
from http.client import HTTPConnection

import pytest

from chemworld.lab.http_security import RequestRejected
from chemworld.lab.server import LabServer, build_parser
from chemworld.lab.session import LabSessionManager


@pytest.fixture(params=["packaged", "checkout"])
def lab_server(request, tmp_path):
    if request.param == "packaged":
        server = LabServer(("127.0.0.1", 0))
        prefix = "/api/sessions"
        manager = server.sessions
    else:
        from apps.task_lab.server import TaskLabServer

        server = TaskLabServer(("127.0.0.1", 0), tmp_path)
        prefix = "/api/student-sessions"
        manager = server.student_sessions
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield server, prefix, manager
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)


def request_json(server, method, path, body=None, headers=None):
    connection = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
    try:
        connection.request(method, path, body, headers or {})
        response = connection.getresponse()
        return response.status, json.loads(response.read())
    finally:
        connection.close()


@pytest.mark.parametrize(
    ("headers", "body", "status"),
    [
        ({"Content-Type": "application/json", "Origin": "https://foreign.invalid"}, "{}", 403),
        ({"Content-Type": "application/json", "Host": "foreign.invalid"}, "{}", 403),
        ({"Content-Type": "text/plain"}, "{}", 415),
        ({"Content-Type": "application/json"}, " " * 65537, 413),
        ({"Content-Type": "application/json"}, '{"seed": NaN}', 400),
        ({"Content-Type": "application/json"}, "[]", 400),
        ({"Content-Type": "application/json", "Transfer-Encoding": "chunked"}, "{}", 400),
    ],
)
def test_external_or_invalid_writes_never_create_sessions(lab_server, headers, body, status):
    server, prefix, manager = lab_server
    observed, _ = request_json(server, "POST", prefix, body, headers)
    assert observed == status
    assert manager._sessions == {}


def test_local_create_close_and_rate_limit(lab_server):
    server, prefix, manager = lab_server
    headers = {
        "Content-Type": "application/json",
        "Origin": f"http://127.0.0.1:{server.server_port}",
    }
    status, state = request_json(server, "POST", prefix, '{"task_id":"reaction-to-assay"}', headers)
    assert status == 201
    status, closed = request_json(
        server, "POST", f"{prefix}/{state['session_id']}/close", "{}", headers
    )
    assert status == 200 and closed["closed"]
    assert manager._sessions == {}
    assert (
        closed.get(
            "final_assay_count",
            closed.get("state_before_close", {}).get("campaign_state", {}).get("final_assay_count"),
        )
        == 0
    )
    server.allow_write = lambda: False
    assert request_json(server, "POST", prefix, "{}", headers)[0] == 429
    assert manager._sessions == {}


def test_capacity_close_and_exact_export_in_new_process(tmp_path):
    manager = LabSessionManager(max_sessions=1)
    session = manager.create("reaction-to-assay", 0)
    try:
        with pytest.raises(RequestRejected, match="Close"):
            manager.create("reaction-to-assay", 1)
        refused = session.step({"operation": "heat", "duration_s": 10})
        assert not refused["accepted"]
        assert session.state()["campaign_state"]["operation_count"] == 0
        assert session.export()["trajectory_jsonl"] == ""
        actions = [
            {"operation": "add_solvent", "volume_L": 0.03, "solvent": 0},
            {"operation": "add_reagent", "amount_mol": 0.01},
            {"operation": "terminate"},
            {"operation": "measure", "instrument": "final_assay"},
        ]
        for action in actions:
            assert session.step(action)["accepted"]
        assert session.replay()["verified"]
        exported = session.export()["trajectory_jsonl"]
        path = tmp_path / "browser-export.jsonl"
        path.write_text(exported, encoding="utf-8")
        child = subprocess.run(
            [
                sys.executable,
                "-c",
                "import sys; from chemworld.data.logging import load_jsonl; "
                "from chemworld.eval.verify import verify_records; "
                "r=verify_records(load_jsonl(sys.argv[1]), tolerance=0.0); "
                "assert r.verified and r.checked_steps == 4",
                str(path),
            ],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert child.returncode == 0, child.stderr
        closed = manager.close(session.session_id)
        assert closed["final_assay_count"] == 1
        assert closed["export"]["trajectory_jsonl"] == exported
        assert not session._trajectory.exists()
        with pytest.raises(ValueError, match="closed"):
            session.step(actions[0])
        replacement = manager.create("reaction-to-assay", 1)
        assert manager.close(replacement.session_id)["final_assay_count"] == 0
    finally:
        manager.close_all()


def test_packaged_cli_is_local_and_provider_free():
    args = build_parser().parse_args(["--no-browser"])
    assert args.host == "127.0.0.1"
    with pytest.raises(ValueError, match="loopback"):
        LabServer(("0.0.0.0", 0))


def test_checkout_run_cancellation_is_not_completion(monkeypatch, tmp_path):
    from apps.task_lab import server as module

    entered, resume = threading.Event(), threading.Event()

    def bounded_worker(**kwargs):
        entered.set()
        assert resume.wait(5)
        kwargs["event_callback"]({"type": "checkpoint"})
        raise AssertionError("Cancellation must stop the worker at the checkpoint")

    monkeypatch.setattr(module, "run_classic_task", bounded_worker)
    job = module.RunJob(
        job_id="test",
        tasks=["reaction-to-assay"],
        mode="adaptive",
        model="offline-test",
        agent_backend="lhs",
        thinking=False,
        reasoning_effort="high",
        budget_multiplier=1,
        campaign_override=False,
        spectrum_disclosure="unassigned",
        output_dir=tmp_path,
    )
    manager = module.RunJobManager(tmp_path)
    manager._jobs[job.job_id] = job
    worker = threading.Thread(target=manager._run, args=(job, None, 0, 8))
    worker.start()
    assert entered.wait(5)
    assert manager.cancel(job.job_id)["status"] == "cancelling"
    resume.set()
    worker.join(5)
    assert not worker.is_alive()
    assert job.status == "cancelled" and job.results == []
    assert job.events[-1]["type"] == "run_cancelled"
    assert not any(event["type"] == "run_completed" for event in job.events)
