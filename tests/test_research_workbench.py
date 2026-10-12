from __future__ import annotations

import io
import json
import threading
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pytest
from apps.research_workbench.jobs import Jobs
from apps.research_workbench.server import WorkbenchServer
from apps.research_workbench.workspace_lock import WorkspaceLock

from chemworld.workbench.providers import Completion, ModelClient, ProviderError
from chemworld.workbench.service import ResearchStore
from chemworld.workbench.signals import chart_series

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def store(tmp_path):
    value = ResearchStore(tmp_path)
    yield value
    value.close()


@pytest.mark.parametrize(
    "task_id", ["reaction-to-assay", "reaction-to-crystallization", "flow-reaction-optimization"]
)
def test_reference_run_has_real_assay_signals_and_exact_replay(store, task_id):
    run = store.create({"design": {"task_id": task_id, "budget": 32, "seed": 0}})
    for action in run.data["recipe"]:
        event = run.step(action)
        assert event["transaction_status"] == "committed", event
        if run.data["status"] != "ready":
            break
    assert run.data["final_assay_count"] == 1
    assert run.data["status"] == "completed"
    assert run.env is None
    assert any(e.get("series") for e in run.data["events"])
    assert run.replay()["verified"] is True
    with zipfile.ZipFile(io.BytesIO(run.export())) as archive:
        assert "trajectory.jsonl" in archive.namelist()
        assert "run.json" in archive.namelist()
        assert any(p.startswith("measurements/") for p in archive.namelist())


def test_composed_world_runs_current_core_and_replays(store):
    composition = json.loads(
        (ROOT / "examples/world-authoring/composed-reaction-assay-v0.1.json").read_text(
            encoding="utf-8"
        )
    )
    run = store.create({"design": {"composition": composition, "budget": 24}})
    for action in run.data["recipe"]:
        event = run.step(action)
        assert event["transaction_status"] == "committed", event
        if run.data["status"] != "ready":
            break
    assert run.data["final_assay_count"] == 1
    assert run.replay()["verified"] is True


def test_invalid_submission_preserved_and_stale_write_rejected(store):
    run = store.create({})
    before = run.data["view"]["campaign_state"]["remaining_budget"]
    event = run.step({"operation": "measure", "instrument": "hplc"}, expected_step=0)
    assert event["transaction_status"] == "rejected"
    assert run.data["executed_steps"] == 0
    assert run.data["view"]["campaign_state"]["remaining_budget"] == before
    assert run.documents.verify_authoritative_integrity()["line_count"] == 1
    with pytest.raises(ValueError, match="changed"):
        run.step({"operation": "add_solvent", "volume_L": 0.02, "solvent": 0}, expected_step=0)


def test_restart_retains_events_notes_and_interrupted_status(store):
    run = store.create({})
    run.step(run.data["recipe"][0])
    run.notebook("human", "write", {"text": "Temperature hypothesis", "message": "before test"})
    run.notebook("model", "write", {"text": "Model hypothesis"})
    run.notebook("human", "write", {"text": "Revised hypothesis"})
    run.notebook("human", "restore", {"revision": 1})
    assert run.notebook("human", "read", {})["revision"] == 3
    saved = run.data["events"].copy()
    store.close()
    reopened = ResearchStore(store.root)
    archived = reopened.get(run.data["id"])
    assert archived.data["events"] == saved
    assert archived.data["status"] == "interrupted"
    assert archived.notebook("human", "read", {})["text"] == "Temperature hypothesis"
    assert archived.notebook("model", "read", {})["text"] == "Model hypothesis"
    assert archived.replay()["verified"]
    with pytest.raises(ValueError, match="not active"):
        archived.step({"operation": "wait", "duration_s": 10})
    reopened.close()


@pytest.mark.parametrize(
    "design",
    [
        {"budget": True},
        {"seed": -1},
        {"budget": 201},
        {"composition": "bad"},
        {"api_key": "secret"},
    ],
)
def test_design_rejects_invalid_fields_without_creating_run(store, design):
    with pytest.raises((ValueError, KeyError)):
        store.create({"design": design})
    assert not store.runs


@pytest.mark.parametrize("provider", ["deepseek", "openai", "qwen"])
def test_provider_protocol_retains_usage_without_secret(monkeypatch, provider):
    captured = []
    decision = {"tool": "finish", "arguments": {"report": "complete"}}
    if provider == "openai":
        response = {
            "model": "actual-model",
            "status": "completed",
            "usage": {"input_tokens": 12, "output_tokens": 8},
            "output": [
                {
                    "type": "message",
                    "content": [{"type": "output_text", "text": json.dumps(decision)}],
                }
            ],
        }
    else:
        response = {
            "model": "actual-model",
            "usage": {"prompt_tokens": 12, "completion_tokens": 8},
            "choices": [{"finish_reason": "stop", "message": {"content": json.dumps(decision)}}],
        }

    class Transport:
        def open(self, request, timeout):
            captured.append(request)
            return io.BytesIO(json.dumps(response).encode())

    monkeypatch.setattr(urllib.request, "build_opener", lambda *a: Transport())
    client = ModelClient({"provider": provider, "model": "requested-model"}, "test-key-never-save")
    completion = client.complete({"state": {"observation": {"yield": None}}})
    assert completion.decision == decision
    assert completion.model == "actual-model"
    assert completion.input_tokens == 12
    assert b"test-key-never-save" not in captured[0].data
    payload = json.loads(captured[0].data)
    if provider == "openai":
        assert payload["store"] is False
        assert payload["max_output_tokens"] == 2048
    else:
        assert payload["max_tokens"] == 2048
    client.close()
    assert client._key == ""
    with pytest.raises(ProviderError, match="credential_expired"):
        client.complete({})


def test_missing_usage_stops_without_acting_and_key_is_not_persisted(store, monkeypatch):
    clients = []

    def complete(client, packet, **kwargs):
        clients.append(client)
        assert "world_id" not in packet["task"]
        return Completion(
            {
                "tool": "act",
                "arguments": {
                    "action": {"operation": "add_solvent", "volume_L": 0.03, "solvent": 0}
                },
            },
            "test",
            None,
            1,
        )

    monkeypatch.setattr(ModelClient, "complete", complete)
    run = store.create({})
    jobs = Jobs(store)
    jobs.start(
        run.data["id"],
        {
            "mode": "model",
            "provider": "deepseek",
            "model": "test",
            "api_key": "test-secret-do-not-retain",
        },
    )
    jobs.threads[-1].join(10)
    assert not jobs.threads[-1].is_alive()
    assert run.data["status"] == "failed"
    assert run.data["submitted_steps"] == 0
    assert run.data["model_calls"] == 1
    assert run.data["usage"]["complete"] is False
    assert clients[0]._key == ""
    for path in store.root.rglob("*"):
        if path.is_file():
            assert b"test-secret-do-not-retain" not in path.read_bytes()


def test_cancel_accounts_inflight_response_but_never_executes_it(store, monkeypatch):
    entered, release = threading.Event(), threading.Event()

    def complete(client, packet, **kwargs):
        entered.set()
        assert release.wait(5)
        return Completion(
            {
                "tool": "act",
                "arguments": {
                    "action": {"operation": "add_solvent", "volume_L": 0.03, "solvent": 0}
                },
            },
            "test",
            10,
            5,
        )

    monkeypatch.setattr(ModelClient, "complete", complete)
    run = store.create({})
    jobs = Jobs(store)
    jobs.start(
        run.data["id"],
        {"mode": "model", "provider": "deepseek", "model": "test", "api_key": "temporary-test-key"},
    )
    assert entered.wait(5)
    jobs.cancel(run.data["id"])
    release.set()
    jobs.threads[-1].join(5)
    assert run.data["status"] == "cancelled"
    assert run.data["executed_steps"] == 0
    assert run.data["usage"]["input_tokens"] == 10


def test_signal_supports_metadata_and_new_spectral_arrays():
    legacy = {
        "time_min": [0, 1, 2],
        "intensity": [0, 4, 0],
        "axis": {"key": "time_min", "unit": "min"},
        "raw_signal": {"key": "intensity", "unit": "a.u."},
    }
    modern = {
        "axis": {"unit": "ppm", "values": [0, 1, 2]},
        "raw_signal": {"unit": "relative_signal", "values": [0, 3, 0]},
    }
    assert len(chart_series(legacy)[0]["points"]) == 3
    assert chart_series(modern)[0]["reverse_x"] is True
    assert chart_series({"kind": "missing"}) == []


def test_workspace_has_single_writer_and_lock_is_released(tmp_path):
    first = WorkspaceLock(tmp_path)
    try:
        with pytest.raises(ValueError, match="already open"):
            WorkspaceLock(tmp_path)
    finally:
        first.close()
    WorkspaceLock(tmp_path).close()


def test_token_threshold_stops_before_second_model_call(store, monkeypatch):
    def complete(client, packet, **kwargs):
        return Completion(
            {"tool": "notebook_write", "arguments": {"text": "A hypothesis"}}, "test", 950, 100
        )

    monkeypatch.setattr(ModelClient, "complete", complete)
    run = store.create({})
    jobs = Jobs(store)
    jobs.start(
        run.data["id"],
        {
            "mode": "model",
            "provider": "deepseek",
            "model": "test",
            "api_key": "temporary-test-key",
            "token_limit": 1000,
        },
    )
    jobs.threads[-1].join(5)
    assert run.data["model_calls"] == 1
    assert run.data["status"] == "stopped"
    assert "token" in run.data["message"]
    assert run.notebook("model", "read", {})["text"] == "A hypothesis"


def test_provider_error_is_redacted_and_never_retried(monkeypatch):
    calls = []

    class Transport:
        def open(self, request, timeout):
            calls.append(1)
            raise urllib.error.HTTPError(
                request.full_url,
                401,
                "secret-returned-by-provider",
                {},
                io.BytesIO(b"test-key-never-save"),
            )

    monkeypatch.setattr(urllib.request, "build_opener", lambda *a: Transport())
    client = ModelClient({"provider": "deepseek", "model": "test"}, "test-key-never-save")
    with pytest.raises(ProviderError) as error:
        client.complete({})
    assert str(error.value) == "provider_http_401"
    assert len(calls) == 1
    client.close()


@pytest.fixture
def http_server(tmp_path):
    server = WorkbenchServer(("127.0.0.1", 0), tmp_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server, f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    server.store.close()
    server.server_close()
    thread.join(3)


def test_http_complete_manual_path_and_security(http_server):
    server, base = http_server

    def request(path, body=None, headers=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(
            base + path, data=data, headers=headers or {"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.load(response)

    assert request("/api/health")["ok"]
    assert len(request("/api/catalog")["tasks"]) == 15
    created = request("/api/runs", {"name": "HTTP test", "design": {"budget": 24}})
    run_id = created["id"]
    current = created
    for action in created["recipe"]:
        current = request(
            f"/api/runs/{run_id}/step",
            {"action": action, "expected_step": current["submitted_steps"]},
        )
        if current["status"] == "completed":
            break
    assert current["final_assay_count"] == 1
    assert request(f"/api/runs/{run_id}/replay", {})["verified"]
    for headers in (
        {"Content-Type": "application/json", "Origin": "https://evil.example"},
        {"Content-Type": "text/plain"},
        {"Content-Type": "application/json", "Host": "evil.example"},
    ):
        with pytest.raises(urllib.error.HTTPError) as error:
            request("/api/runs", {}, headers)
        assert error.value.code in {403, 415}
    assert len(server.store.runs) == 1
    with pytest.raises(urllib.error.HTTPError) as error:
        request(
            f"/api/runs/{run_id}/notebook",
            {
                "author": "model",
                "operation": "write",
                "arguments": {"text": "human pretending to be model"},
            },
        )
    assert error.value.code == 400
