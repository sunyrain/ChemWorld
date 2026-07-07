"""Student-side JSONL runtime used by the local ChemWorld evaluator.

The runtime is intentionally small: it loads a submitted agent entrypoint and
talks to the teacher-side runner through stdin/stdout JSON lines. In a real
deployment this file can become the command executed inside a Docker container.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import traceback
from typing import Any


def _load_entrypoint(entrypoint: str) -> Any:
    module_name, _, attribute = entrypoint.partition(":")
    if not module_name or not attribute:
        raise ValueError("entrypoint must use the form 'module:function_or_object'")
    module = importlib.import_module(module_name)
    target = getattr(module, attribute)
    return target() if callable(target) else target


def _write(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, sort_keys=True) + "\n")
    sys.stdout.flush()


def _call(agent: Any, message: dict[str, Any]) -> dict[str, Any]:
    message_type = message.get("type")
    if message_type == "reset":
        result = agent.reset(message["task_info"], int(message["seed"]))
        return {"ok": True, "result": result}
    if message_type == "act":
        action = agent.act(message.get("history", []))
        if not isinstance(action, dict):
            raise TypeError("Agent.act(history) must return a dict action")
        return {"ok": True, "action": action}
    if message_type == "update":
        result = agent.update(
            message["action"],
            message["observation"],
            float(message["reward"]),
            message["info"],
        )
        return {"ok": True, "result": result}
    if message_type == "close":
        return {"ok": True, "closed": True}
    raise ValueError(f"Unknown runtime message type: {message_type!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a submitted ChemWorld agent.")
    parser.add_argument("--entrypoint", required=True)
    args = parser.parse_args(argv)

    try:
        agent = _load_entrypoint(args.entrypoint)
    except Exception:
        _write(
            {
                "ok": False,
                "phase": "startup",
                "error": traceback.format_exc(),
            }
        )
        return 2

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            response = _call(agent, json.loads(line))
        except Exception:
            response = {
                "ok": False,
                "phase": "runtime",
                "error": traceback.format_exc(),
            }
        _write(response)
        if response.get("closed"):
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
