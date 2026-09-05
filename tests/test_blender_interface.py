from __future__ import annotations

from copy import deepcopy
from http.server import ThreadingHTTPServer
from threading import Thread
from typing import Any

import gymnasium as gym
import pytest
from apps.blender_lab.engine import Lab, LabError
from apps.blender_lab.projection import ProjectionStore
from apps.blender_lab.server import Handler

import chemworld  # noqa: F401
from chemworld.interfaces.blender import (
    BlenderClient,
    BlenderObserver,
    attach_blender,
    public_frame,
)


@pytest.fixture
def world():
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=7)
    env.reset(seed=7)
    yield env
    env.close()


@pytest.fixture
def service(tmp_path):
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    server.lab = Lab(tmp_path)
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    yield BlenderClient(f"http://127.0.0.1:{server.server_port}"), server.lab
    server.shutdown()
    server.server_close()
    worker.join()


def test_observer_returns_original_gym_results_and_never_retries_steps(world, monkeypatch):
    original_step = world.step
    calls = []

    def track(action):
        result = original_step(action)
        calls.append(result)
        return result

    def disconnected(frame):
        raise OSError("renderer disconnected")

    monkeypatch.setattr(world, "step", track)
    observer = BlenderObserver(world, sink=disconnected)
    result = observer.step({"operation": "add_reagent", "amount_mol": 0.01})
    assert result is calls[0]
    assert len(calls) == 1
    assert observer.projection_error == "renderer disconnected"
    assert observer.last_frame["step"] == 1
    assert observer.last_frame["campaign"]["remaining_budget"] == 17


def test_frame_uses_only_public_api_and_preserves_missing_values():
    class PublicOnly:
        @property
        def unwrapped(self):
            return self

        def observation_view(self, kind):
            if kind == "tool_json":
                return {
                    "task": {"task_id": "example"},
                    "observed_mask": {"yield": False},
                    "observation": {"yield": 0.999, "score": 0},
                    "campaign_state": {
                        "operation_count": 0,
                        "experiment_index": 0,
                        "remaining_budget": 3,
                        "budget": 3,
                        "final_assay_count": 0,
                        "best_score": None,
                        "done": False,
                    },
                }
            return {"status": "accepted", "text": "Public report", "instrument_summary": {}}

    frame = public_frame(PublicOnly(), "public-only")
    assert frame["observations"] == {"yield": None, "score": 0}
    assert frame["mapping_status"] == "report_only"
    assert frame["physical_control_enabled"] is False
    assert "world_id" not in frame and "hidden_state" not in frame


def test_http_projection_does_not_mutate_scene_inventory_or_core(world, service):
    client, lab = service
    before = lab.snapshot()
    core_before = world.unwrapped.campaign_state()["operation_count"]
    frame = public_frame(world, "owner")
    client.publish(frame)
    client.publish(frame)
    assert client.request("/api/v1/chemworld/frame")["frame"] == frame
    assert lab.snapshot() == before
    assert world.unwrapped.campaign_state()["operation_count"] == core_before
    with pytest.raises(OSError):
        client.publish({**frame, "session_id": "other"})
    client.release("owner")
    client.publish({**frame, "session_id": "other"})


def test_projection_rejects_stale_conflicting_unmeasured_and_hardware_frames(world):
    store = ProjectionStore()
    frame = public_frame(world, "one")
    store.publish({**frame, "step": 2})
    for changes in [
        {"step": 1},
        {"step": 2, "status": "different"},
        {"step": 3, "physical_control_enabled": True},
        {"step": 3, "source": "hidden_state"},
        {"step": 3, "observations": {"yield": 0.8}, "observed_mask": {}},
        {"step": 3, "hidden_state": {}},
    ]:
        with pytest.raises(LabError):
            store.publish({**frame, **changes})
    assert store.snapshot()["frame"]["step"] == 2


def test_optional_hook_is_noop_by_default(world, monkeypatch):
    monkeypatch.delenv("CHEMWORLD_BLENDER_URL", raising=False)
    assert attach_blender(world) is world
    for url in [
        "https://example.com",
        "http://user:password@127.0.0.1",
        "http://localhost/private",
    ]:
        with pytest.raises(ValueError):
            BlenderClient(url)


def test_student_session_publishes_steps_when_explicitly_enabled(service, monkeypatch):
    from apps.task_lab.student_session import StudentSession

    client, lab = service
    monkeypatch.setenv("CHEMWORLD_BLENDER_URL", client.url)
    session = StudentSession("reaction-to-assay", 7)
    try:
        assert lab.projection.snapshot()["frame"]["step"] == 0
        result = session.step({"operation": "add_reagent", "amount_mol": 0.01})
        assert result["accepted"]
        assert lab.projection.snapshot()["frame"]["step"] == 1
        assert lab.projection.snapshot()["frame"]["observations"]["yield"] is None
    finally:
        session.close()
    assert lab.projection.snapshot()["active_session_id"] is None


def test_robot_logistics_preserve_core_observation(world, service):
    client, lab = service
    before: dict[str, Any] = deepcopy(world.unwrapped.observation_view("tool_json"))
    task = client.transport()
    for _ in range(500):
        with lab.lock:
            lab.environment.tick(0.5)
        if lab.environment.data["tasks"][task["id"]]["status"] == "succeeded":
            break
    result = client.wait_task(task["id"], timeout=1)
    assert result["status"] == "succeeded"
    assert lab.environment.data["custody"]["sample_tube_01"] == "analysis"
    assert world.unwrapped.observation_view("tool_json") == before
