"""Host-owned STDIO MCP bridge for one interactive ChemWorld experiment.

The process is launched by Codex as a configured MCP server, outside the
model-generated shell-command path.  It exposes only bounded public state and
file-IPC requests; the authoritative environment remains in the parent runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from chemworld.agents.interaction import DecisionAuditRecord
from chemworld.eval.work_ii_prior_discovery import (
    WORK_II_LAW_BASES,
    WORK_II_LAW_LINKS,
    WORK_II_LAW_SUMMARY_SCHEMA_VERSION,
    WORK_II_SNAPSHOT_SCHEMA_VERSION,
    parse_work_ii_belief_snapshot,
)

MCP_SERVER_VERSION = "chemworld-experiment-codex-mcp-0.8"
IPC_VERSION = "chemworld-experiment-codex-ipc-0.2"
SERVER_NAME = "chemworld_lab"
SUPPORTED_TOOLS = (
    "material_information",
    "status",
    "history",
    "inspect_artifact",
    "commit_belief_snapshot",
    "commit_final_recommendation",
    "step",
)
ATOMIC_REPLACE_RETRY_LIMIT = 40
ATOMIC_REPLACE_RETRY_INTERVAL_S = 0.025


def _encode(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} is not a JSON object")
    return value


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(raw)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(_encode(value) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        _replace_with_retry(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _replace_with_retry(temporary: Path, path: Path) -> None:
    """Retry only transient sharing violations; preserve fail-closed semantics."""

    for retry in range(ATOMIC_REPLACE_RETRY_LIMIT + 1):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if retry >= ATOMIC_REPLACE_RETRY_LIMIT:
                raise
            time.sleep(ATOMIC_REPLACE_RETRY_INTERVAL_S)


def _append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as handle:
        handle.write(_encode(value) + b"\n")
        handle.flush()
        os.fsync(handle.fileno())


class ChemWorldMCPServer:
    """Minimal, dependency-free MCP server with a deliberately narrow surface."""

    def __init__(self, workspace: Path) -> None:
        self.root = workspace.resolve(strict=True)
        self.agent = (self.root / "agent").resolve(strict=True)
        self.public = (self.root / "public").resolve(strict=True)
        self.reference = (self.root / "reference").resolve(strict=True)
        self.ipc = (self.root / ".ipc").resolve(strict=True)
        self._terminal_outcome: dict[str, Any] | None = None
        for path in (self.agent, self.public, self.reference, self.ipc):
            path.relative_to(self.root)

    def run(self) -> int:
        for raw_line in sys.stdin.buffer:
            if not raw_line.strip():
                continue
            try:
                request = json.loads(raw_line)
                if not isinstance(request, dict):
                    raise ValueError("JSON-RPC request must be an object")
                response = self._dispatch(request)
            except Exception as error:
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": type(error).__name__,
                    },
                }
            if response is not None:
                sys.stdout.buffer.write(_encode(response) + b"\n")
                sys.stdout.buffer.flush()
        return 0

    def _dispatch(self, request: dict[str, Any]) -> dict[str, Any] | None:
        method = request.get("method")
        request_id = request.get("id")
        if method == "notifications/initialized" or str(method).startswith("notifications/"):
            return None
        if method == "initialize":
            params = request.get("params")
            protocol = (
                params.get("protocolVersion")
                if isinstance(params, dict)
                else "2025-06-18"
            )
            descriptor = self._descriptor()
            campaign = descriptor.get("session_scope") == "campaign"
            return self._result(
                request_id,
                {
                    "protocolVersion": protocol,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": SERVER_NAME, "version": MCP_SERVER_VERSION},
                    "instructions": (
                        "Use chemworld_lab.step for every physical operation. First call "
                        "material_information once. Use status, history, and inspect_artifact "
                        "only for bounded public evidence. Never fabricate an outcome. "
                        + (
                            "Commit every required belief checkpoint with "
                            "commit_belief_snapshot. An experiment_ended outcome closes only "
                            "the current batch; continue in the same session when "
                            "campaign_ended=false. After campaign_ended=true, commit the final "
                            "checkpoint if due, commit exactly one participant-owned selection "
                            "with commit_final_recommendation, then submit exactly one JSON object "
                            "matching the final response schema, with no prose or Markdown fence."
                            if campaign
                            else "After a step returns experiment_ended=true, call no more "
                            "tools and submit the final response for that experiment."
                        )
                    ),
                },
            )
        if method == "ping":
            return self._result(request_id, {})
        if method == "logging/setLevel":
            return self._result(request_id, {})
        if method == "tools/list":
            return self._result(request_id, {"tools": self._tool_definitions()})
        if method == "tools/call":
            params = request.get("params")
            if not isinstance(params, dict):
                return self._error(request_id, -32602, "invalid tools/call params")
            name = params.get("name")
            arguments = params.get("arguments", {})
            if not isinstance(name, str) or not isinstance(arguments, dict):
                return self._error(request_id, -32602, "invalid tools/call params")
            return self._result(request_id, self._call_tool(name, arguments))
        return self._error(request_id, -32601, "method not found")

    @staticmethod
    def _result(request_id: Any, result: Any) -> dict[str, Any]:
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

    @staticmethod
    def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }

    def _descriptor(self) -> dict[str, Any]:
        descriptor = _read_object(self.ipc / "active_session.json")
        if descriptor.get("schema_version") != IPC_VERSION:
            raise ValueError("unsupported active experiment session")
        return descriptor

    def _audit(
        self,
        descriptor: dict[str, Any],
        tool: str,
        arguments: Any,
        *,
        started_at: str,
        duration_ms: float,
        status: str,
        result: Any,
        error_type: str | None,
        error_code: str | None,
        error_field_path: str | None,
        error_detail: str | None,
    ) -> None:
        session_id = self._leaf(str(descriptor["session_id"]), label="session_id")
        _append_jsonl(
            self.ipc / "sessions" / session_id / "mcp_tool_calls.jsonl",
            {
                "schema_version": MCP_SERVER_VERSION,
                "tool": tool,
                "started_at": started_at,
                "duration_ms": round(duration_ms, 3),
                "status": status,
                "error_type": error_type,
                "error_code": error_code,
                "error_field_path": error_field_path,
                "error_detail": error_detail,
                "error_detail_byte_count": (
                    len(error_detail.encode("utf-8", errors="replace"))
                    if error_detail is not None
                    else 0
                ),
                "error_detail_sha256": (
                    hashlib.sha256(
                        error_detail.encode("utf-8", errors="replace")
                    ).hexdigest()
                    if error_detail is not None
                    else None
                ),
                "arguments_sha256": hashlib.sha256(_encode(arguments)).hexdigest(),
                "argument_keys": sorted(arguments) if isinstance(arguments, dict) else [],
                "result_sha256": hashlib.sha256(_encode(result)).hexdigest(),
            },
        )

    def _call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in SUPPORTED_TOOLS:
            return self._tool_error("unsupported_tool")
        descriptor = self._descriptor()
        started_at = datetime.now(UTC).isoformat()
        started = time.perf_counter()
        status = "completed"
        error_type: str | None = None
        error_code: str | None = None
        error_field_path: str | None = None
        error_detail: str | None = None
        try:
            if name == "material_information":
                payload = _read_object(self.reference / "material_information.json")
            elif name == "status":
                payload = self._status()
            elif name == "history":
                payload = self._history(arguments)
            elif name == "inspect_artifact":
                payload = self._inspect(descriptor, arguments)
            elif name == "commit_belief_snapshot":
                payload = self._commit_belief_snapshot(descriptor, arguments)
            elif name == "commit_final_recommendation":
                payload = self._commit_final_recommendation(descriptor, arguments)
            else:
                payload = self._step(descriptor, arguments)
            cap = int(descriptor["max_tool_output_bytes"])
            encoded = _encode(payload)
            if len(encoded) > cap:
                raise ValueError("tool output exceeds configured byte cap")
            result = {
                "content": [{"type": "text", "text": encoded.decode("utf-8")}],
                "isError": False,
            }
        except Exception as error:
            detail = str(error).strip()
            status = "failed"
            error_type = type(error).__name__
            error_detail = detail[:1000] if detail else error_type
            error_code = self._error_code(error_type, error_detail)
            error_field_path = self._error_field_path(error_detail)
            result = self._tool_error(
                f"{type(error).__name__}: {detail[:1000]}"
                if name in {"step", "commit_belief_snapshot", "commit_final_recommendation"}
                and detail
                else type(error).__name__
            )
        self._audit(
            descriptor,
            name,
            arguments,
            started_at=started_at,
            duration_ms=(time.perf_counter() - started) * 1000.0,
            status=status,
            result=result,
            error_type=error_type,
            error_code=error_code,
            error_field_path=error_field_path,
            error_detail=error_detail,
        )
        return result

    @staticmethod
    def _error_code(error_type: str, detail: str) -> str:
        lowered = detail.lower()
        if "decision_audit" in lowered and "required" in lowered:
            return "missing_decision_audit"
        if "expected_step" in lowered:
            return "invalid_expected_step"
        if "belief" in lowered or "snapshot" in lowered:
            return "invalid_belief_snapshot"
        if "final_recommendation" in lowered or "selected_experiment_index" in lowered:
            return "invalid_final_recommendation"
        if error_type == "PermissionError":
            return "atomic_replace_permission_error"
        if error_type == "ValueError":
            return "validation_error"
        return "tool_execution_error"

    @staticmethod
    def _error_field_path(detail: str) -> str | None:
        match = re.search(
            r"(?:snapshot\.|decision_audit\.|prior_assessment\.|law_summary\."
            r"|predictions\[|action\.|expected_step|selected_experiment_index)"
            r"[A-Za-z0-9_\.\[\]-]*",
            detail,
        )
        return match.group(0).rstrip(".") if match else None

    @staticmethod
    def _tool_error(error_type: str) -> dict[str, Any]:
        text = _encode({"ok": False, "error": error_type}).decode("utf-8")
        return {"content": [{"type": "text", "text": text}], "isError": True}

    def _history(self, arguments: dict[str, Any]) -> dict[str, Any]:
        raw_limit = arguments.get("limit", 5)
        if isinstance(raw_limit, bool) or not isinstance(raw_limit, int):
            raise ValueError("limit must be an integer")
        limit = max(1, min(raw_limit, 10))
        rows: list[dict[str, Any]] = []
        path = self.public / "history.jsonl"
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line:
                    value = json.loads(line)
                    if isinstance(value, dict):
                        rows.append(value)
        return {
            "schema_version": MCP_SERVER_VERSION,
            "authoritative": False,
            "events": rows[-limit:],
        }

    def _status(self) -> dict[str, Any]:
        if self._terminal_outcome is None:
            return _read_object(self.public / "current.json")
        campaign = self._descriptor().get("session_scope") == "campaign"
        return {
            "schema_version": MCP_SERVER_VERSION,
            "experiment_ended": True,
            "terminal_outcome": self._terminal_outcome,
            "instruction": (
                "Commit the final belief checkpoint if due, call "
                "commit_final_recommendation exactly once, then submit the final response; "
                "do not call step again."
                if campaign
                else "Submit the final response now; do not call step again."
            ),
            "final_response_contract": self._final_response_contract(campaign=campaign),
        }

    @staticmethod
    def _final_response_contract(*, campaign: bool) -> dict[str, Any]:
        return {
            "format": "json_object_only",
            "required_keys": ["status", "summary"],
            "status": "campaign_complete" if campaign else "experiment_complete",
            "summary_max_length": 3000 if campaign else 2000,
            "final_recommendation_contract": (
                {
                    "selected_experiment_index": (
                        "1-based_integer_identifying_a_completed_experiment"
                    ),
                    "selection_rationale_max_length": 2000,
                    "committed_before_blind_evaluation": True,
                }
                if campaign
                else None
            ),
            "prose_or_markdown_allowed": False,
        }

    def _commit_belief_snapshot(
        self,
        descriptor: dict[str, Any],
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if descriptor.get("session_scope") != "campaign":
            raise RuntimeError("belief checkpoints are available only in campaign sessions")
        snapshot = arguments.get("snapshot")
        if not isinstance(snapshot, dict):
            raise ValueError("snapshot must be an object")
        contract = _read_object(self.reference / "belief_checkpoint_contract.json")
        stages = contract.get("snapshot_stages")
        if not isinstance(stages, list) or not stages:
            raise ValueError("checkpoint contract has no snapshot stages")
        session_id = self._leaf(str(descriptor["session_id"]), label="session_id")
        root = self.ipc / "sessions" / session_id / "belief_snapshots"
        existing = sorted(root.glob("*.json")) if root.exists() else []
        if len(existing) >= len(stages):
            raise RuntimeError("all required belief checkpoints are already committed")
        expected_stage = str(stages[len(existing)])
        required_counts = contract.get("checkpoint_complete_experiments")
        if not isinstance(required_counts, list) or len(required_counts) != len(stages):
            raise ValueError("checkpoint experiment-count schedule is invalid")
        completed_count, observed_evidence = self._completed_experiment_state()
        if completed_count != int(required_counts[len(existing)]):
            raise RuntimeError(
                "checkpoint is not due at the current completed-experiment count: "
                f"expected {required_counts[len(existing)]}, observed {completed_count}"
            )
        parsed = parse_work_ii_belief_snapshot(
            snapshot,
            expected_stage=expected_stage,
            query_metric_contract={
                str(key): tuple(str(item) for item in value)
                for key, value in dict(contract["query_metric_contract"]).items()
            },
            allowed_feature_ids=tuple(str(item) for item in contract["allowed_feature_ids"]),
            allowed_metric_ids=tuple(str(item) for item in contract["allowed_metric_ids"]),
            allowed_prior_fields=tuple(str(item) for item in contract["allowed_prior_fields"]),
            evidence_catalog=tuple(str(item) for item in contract["evidence_catalog"]),
            nominal_information_available=bool(contract["nominal_information_available"]),
        )
        cited = set(parsed.evidence_ids) | set(parsed.law_summary.evidence_ids)
        if not cited.issubset(observed_evidence):
            raise ValueError("belief snapshot cites evidence that has not yet been observed")
        root.mkdir(parents=True, exist_ok=True)
        path = root / f"{len(existing) + 1:02d}-{expected_stage}.json"
        _atomic_json(path, parsed.to_dict())
        result = {
            "ok": True,
            "schema_version": MCP_SERVER_VERSION,
            "stage": expected_stage,
            "complete_experiment_count": completed_count,
            "committed_checkpoint_count": len(existing) + 1,
            "remaining_checkpoint_count": len(stages) - len(existing) - 1,
        }
        if result["remaining_checkpoint_count"] == 0:
            result["final_response_contract"] = self._final_response_contract(campaign=True)
        return result

    def _commit_final_recommendation(
        self,
        descriptor: dict[str, Any],
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if descriptor.get("session_scope") != "campaign":
            raise RuntimeError("final recommendations are available only in campaign sessions")
        completed_count, _ = self._completed_experiment_state()
        if completed_count < 1 or not self._campaign_terminal_observed():
            raise RuntimeError("final recommendation is allowed only after campaign terminal")
        contract = _read_object(self.reference / "belief_checkpoint_contract.json")
        stages = contract.get("snapshot_stages")
        if not isinstance(stages, list) or not stages:
            raise ValueError("checkpoint contract has no snapshot stages")
        session_id = self._leaf(str(descriptor["session_id"]), label="session_id")
        snapshot_root = self.ipc / "sessions" / session_id / "belief_snapshots"
        committed_snapshots = (
            len(list(snapshot_root.glob("*.json"))) if snapshot_root.exists() else 0
        )
        if committed_snapshots != len(stages):
            raise RuntimeError(
                "all required belief checkpoints must be committed before final recommendation"
            )
        index = arguments.get("selected_experiment_index")
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("selected_experiment_index must be an integer")
        if not 1 <= index <= completed_count:
            raise ValueError(
                "selected_experiment_index must identify a completed 1-based experiment"
            )
        rationale = arguments.get("selection_rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("selection_rationale must be a non-empty string")
        if len(rationale) > 2000:
            raise ValueError("selection_rationale exceeds 2000 characters")
        recommendation = {
            "selected_experiment_index": index,
            "selection_rationale": rationale.strip(),
        }
        path = self.ipc / "sessions" / session_id / "final_recommendation.json"
        if path.exists():
            existing = _read_object(path)
            existing_recommendation = existing.get("recommendation")
            if _encode(existing_recommendation) != _encode(recommendation):
                raise RuntimeError("a different final recommendation is already committed")
            return {
                "ok": True,
                "schema_version": MCP_SERVER_VERSION,
                "already_committed": True,
                "recommendation_sha256": hashlib.sha256(_encode(recommendation)).hexdigest(),
                "instruction": "Submit the final response now; do not call more tools.",
            }
        record = {
            "schema_version": MCP_SERVER_VERSION,
            "recommendation": recommendation,
            "recommendation_sha256": hashlib.sha256(_encode(recommendation)).hexdigest(),
            "complete_experiment_count": completed_count,
            "committed_checkpoint_count": committed_snapshots,
            "committed_after_campaign_terminal": True,
            "committed_before_blind_evaluation": True,
        }
        _atomic_json(path, record)
        return {
            "ok": True,
            "schema_version": MCP_SERVER_VERSION,
            "already_committed": False,
            "recommendation_sha256": record["recommendation_sha256"],
            "instruction": "Submit the final response now; do not call more tools.",
        }

    def _campaign_terminal_observed(self) -> bool:
        if self._terminal_outcome is not None:
            return self._terminal_outcome.get("campaign_ended") is True
        path = self.public / "history.jsonl"
        if not path.exists():
            return False
        for line in reversed(path.read_text(encoding="utf-8").splitlines()):
            if not line:
                continue
            value = json.loads(line)
            return isinstance(value, dict) and value.get("campaign_ended") is True
        return False

    def _completed_experiment_state(self) -> tuple[int, set[str]]:
        rows: list[dict[str, Any]] = []
        path = self.public / "history.jsonl"
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line:
                    value = json.loads(line)
                    if isinstance(value, dict):
                        rows.append(value)
        ended = [row for row in rows if row.get("experiment_ended") is True]
        evidence = {
            str(row["evidence_id"])
            for row in ended
            if isinstance(row.get("evidence_id"), str)
        }
        return len(ended), evidence

    def _inspect(
        self,
        descriptor: dict[str, Any],
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        artifact_id = self._leaf(str(arguments.get("artifact_id", "")), label="artifact_id")
        offset = max(self._integer(arguments.get("offset", 0), label="offset"), 0)
        cap = int(descriptor["max_tool_output_bytes"])
        requested = self._integer(arguments.get("limit", 4096), label="limit")
        limit = max(1, min(requested, max(256, cap // 2)))
        path = self.public / "artifacts" / f"{artifact_id}.json"
        text = path.read_text(encoding="utf-8")
        fragment = text[offset : offset + limit]
        session_id = self._leaf(str(descriptor["session_id"]), label="session_id")
        _append_jsonl(
            self.ipc / "sessions" / session_id / "artifact_access.jsonl",
            {
                "artifact_id": artifact_id,
                "offset": offset,
                "limit": limit,
                "returned_character_count": len(fragment),
                "total_character_count": len(text),
            },
        )
        return {
            "schema_version": MCP_SERVER_VERSION,
            "artifact_id": artifact_id,
            "offset": offset,
            "next_offset": offset + len(fragment),
            "total_character_count": len(text),
            "complete": offset + len(fragment) >= len(text),
            "encoding": "utf-8-json-text-fragment",
            "data": fragment,
        }

    def _step(
        self,
        descriptor: dict[str, Any],
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        if self._terminal_outcome is not None:
            raise RuntimeError(
                "campaign_already_ended_submit_final_response"
            )
        if descriptor.get("session_scope") == "campaign":
            contract = _read_object(self.reference / "belief_checkpoint_contract.json")
            stages = contract.get("snapshot_stages", [])
            required_counts = contract.get("checkpoint_complete_experiments", [])
            root = self.ipc / "sessions" / str(descriptor["session_id"]) / "belief_snapshots"
            committed = len(list(root.glob("*.json"))) if root.exists() else 0
            completed_count, _ = self._completed_experiment_state()
            if (
                committed < len(stages)
                and committed < len(required_counts)
                and completed_count == int(required_counts[committed])
            ):
                raise RuntimeError(
                    f"required belief checkpoint {stages[committed]} must be committed before step"
                )
        expected_step = self._integer(arguments.get("expected_step"), label="expected_step")
        if expected_step < 1:
            raise ValueError("expected_step must be positive")
        action = arguments.get("action")
        if not isinstance(action, dict) or not isinstance(action.get("operation"), str):
            raise ValueError("action.operation is required")
        decision_audit: dict[str, Any] | None = None
        if descriptor.get("session_scope") == "campaign":
            raw_audit = arguments.get("decision_audit")
            if not isinstance(raw_audit, dict):
                raise ValueError("campaign step requires decision_audit")
            decision_audit = DecisionAuditRecord.from_payload(
                raw_audit,
                action=action,
            ).to_dict()
        session_id = self._leaf(str(descriptor["session_id"]), label="session_id")
        request_id_value = arguments.get("request_id")
        if request_id_value is None:
            request_id = hashlib.sha256(
                session_id.encode("utf-8")
                + b"|"
                + str(expected_step).encode("ascii")
                + b"|"
                + _encode(action)
            ).hexdigest()[:32]
        else:
            request_id = self._leaf(str(request_id_value), label="request_id")
        envelope = {
            "schema_version": IPC_VERSION,
            "session_id": session_id,
            "request_id": request_id,
            "expected_step": expected_step,
            "action": action,
        }
        if decision_audit is not None:
            envelope["decision_audit"] = decision_audit
        session_root = self.ipc / "sessions" / session_id
        request_path = session_root / "mcp_requests" / f"{request_id}.json"
        response_path = session_root / "responses" / f"{request_id}.json"
        if request_path.exists():
            if _encode(_read_object(request_path)) != _encode(envelope):
                raise ValueError("request_id was reused with another payload")
        else:
            _atomic_json(request_path, envelope)
        deadline = time.monotonic() + float(descriptor["response_timeout_s"])
        while time.monotonic() < deadline:
            if response_path.exists():
                outcome = _read_object(response_path)
                if outcome.get("campaign_ended") is True or (
                    descriptor.get("session_scope") != "campaign"
                    and outcome.get("experiment_ended") is True
                ):
                    self._terminal_outcome = outcome
                return outcome
            current = self._descriptor()
            if current.get("session_id") != session_id:
                raise RuntimeError("session changed before the operation completed")
            time.sleep(0.05)
        raise TimeoutError("runner did not return an operation outcome")

    @staticmethod
    def _leaf(value: str, *, label: str) -> str:
        if not value or value in {".", ".."} or "/" in value or "\\" in value:
            raise ValueError(f"{label} must be a non-path string")
        return value

    @staticmethod
    def _integer(value: Any, *, label: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{label} must be an integer")
        return value

    def _belief_snapshot_schema(self) -> dict[str, Any]:
        contract = _read_object(self.reference / "belief_checkpoint_contract.json")
        stages = [str(item) for item in contract.get("snapshot_stages", [])]
        query_contract = dict(contract.get("query_metric_contract", {}))
        query_ids = [str(item) for item in query_contract]
        metric_ids = [str(item) for item in contract.get("allowed_metric_ids", [])]
        feature_ids = [str(item) for item in contract.get("allowed_feature_ids", [])]
        prior_fields = [str(item) for item in contract.get("allowed_prior_fields", [])]
        evidence_ids = [str(item) for item in contract.get("evidence_catalog", [])]
        nominal = bool(contract.get("nominal_information_available"))
        probability = {"type": "number", "minimum": 0.0, "maximum": 1.0}
        law_term_common = {
            "type": "object",
            "properties": {
                "term_id": {"type": "string", "minLength": 1, "maxLength": 200},
                "basis": {"enum": sorted(WORK_II_LAW_BASES)},
                "input_ids": {
                    "type": "array",
                    "items": {"enum": feature_ids},
                    "minItems": 1,
                    "maxItems": 2,
                    "uniqueItems": True,
                },
                "coefficient": {"type": "number"},
                "category_value": {"type": ["string", "number"]},
            },
            "required": ["term_id", "basis", "input_ids", "coefficient"],
            "additionalProperties": False,
        }
        metric_prediction = {
            "type": "object",
            "properties": {
                "metric_id": {"enum": metric_ids},
                "mean": {"type": "number"},
                "interval_lower": {"type": "number"},
                "interval_upper": {"type": "number"},
                "confidence": probability,
            },
            "required": [
                "metric_id",
                "mean",
                "interval_lower",
                "interval_upper",
                "confidence",
            ],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {
                "schema_version": {"const": WORK_II_SNAPSHOT_SCHEMA_VERSION},
                "snapshot_id": {"type": "string", "minLength": 1, "maxLength": 200},
                "stage": {"enum": stages},
                "prior_assessment": {
                    "type": "object",
                    "properties": {
                        "nominal_information_available": {"const": nominal},
                        "reliability_probability": probability if nominal else {"type": "null"},
                        "suspected_misindexed_fields": {
                            "type": "array",
                            "items": {"enum": prior_fields},
                            "uniqueItems": True,
                        },
                        "rationale": {"type": "string", "minLength": 1, "maxLength": 2000},
                    },
                    "required": [
                        "nominal_information_available",
                        "reliability_probability",
                        "suspected_misindexed_fields",
                        "rationale",
                    ],
                    "additionalProperties": False,
                },
                "predictions": {
                    "type": "array",
                    "minItems": len(query_ids),
                    "maxItems": len(query_ids),
                    "items": {
                        "type": "object",
                        "properties": {
                            "query_id": {"enum": query_ids},
                            "metrics": {
                                "type": "array",
                                "minItems": len(metric_ids),
                                "maxItems": len(metric_ids),
                                "items": metric_prediction,
                            },
                        },
                        "required": ["query_id", "metrics"],
                        "additionalProperties": False,
                    },
                },
                "law_summary": {
                    "type": "object",
                    "properties": {
                        "schema_version": {"const": WORK_II_LAW_SUMMARY_SCHEMA_VERSION},
                        "summary_id": {"type": "string", "minLength": 1, "maxLength": 200},
                        "feature_ids": {
                            "type": "array",
                            "items": {"enum": feature_ids},
                            "minItems": 1,
                            "uniqueItems": True,
                        },
                        "metric_laws": {
                            "type": "array",
                            "minItems": len(metric_ids),
                            "maxItems": len(metric_ids),
                            "items": {
                                "type": "object",
                                "properties": {
                                    "metric_id": {"enum": metric_ids},
                                    "intercept": {"type": "number"},
                                    "link": {"enum": sorted(WORK_II_LAW_LINKS)},
                                    "lower_bound": {"type": "number"},
                                    "upper_bound": {"type": "number"},
                                    "terms": {
                                        "type": "array",
                                        "maxItems": 64,
                                        "items": law_term_common,
                                    },
                                },
                                "required": [
                                    "metric_id",
                                    "intercept",
                                    "link",
                                    "lower_bound",
                                    "upper_bound",
                                    "terms",
                                ],
                                "additionalProperties": False,
                            },
                        },
                        "evidence_ids": {
                            "type": "array",
                            "items": {"enum": evidence_ids},
                            "uniqueItems": True,
                        },
                        "applicability": {"type": "string", "minLength": 1, "maxLength": 2000},
                        "limitations": {
                            "type": "array",
                            "items": {"type": "string", "minLength": 1, "maxLength": 200},
                            "maxItems": 16,
                            "uniqueItems": True,
                        },
                        "confidence": probability,
                    },
                    "required": [
                        "schema_version",
                        "summary_id",
                        "feature_ids",
                        "metric_laws",
                        "evidence_ids",
                        "applicability",
                        "limitations",
                        "confidence",
                    ],
                    "additionalProperties": False,
                },
                "evidence_ids": {
                    "type": "array",
                    "items": {"enum": evidence_ids},
                    "uniqueItems": True,
                },
                "next_experiment_intent": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 2000,
                },
                "overall_confidence": probability,
            },
            "required": [
                "schema_version",
                "snapshot_id",
                "stage",
                "prior_assessment",
                "predictions",
                "law_summary",
                "evidence_ids",
                "next_experiment_intent",
                "overall_confidence",
            ],
            "additionalProperties": False,
        }

    @staticmethod
    def _decision_audit_schema() -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expected_effect": {"type": "string", "minLength": 1, "maxLength": 1000},
                "diagnostic_target": {"type": "string", "minLength": 1, "maxLength": 1000},
                "expected_information_gain": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "belief_update_rule": {
                    "type": "object",
                    "properties": {
                        "if_supported": {"type": "string", "minLength": 1, "maxLength": 1000},
                        "if_not_supported": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 1000,
                        },
                    },
                    "required": ["if_supported", "if_not_supported"],
                    "additionalProperties": False,
                },
                "uncertainty": {
                    "type": ["number", "null"],
                    "minimum": 0.0,
                    "maximum": 1.0,
                },
                "adaptation_source": {
                    "enum": ["none", "measurement", "spectrum", "experiment_memory", "validator"]
                },
            },
            "required": [
                "expected_effect",
                "diagnostic_target",
                "expected_information_gain",
                "belief_update_rule",
                "uncertainty",
                "adaptation_source",
            ],
            "additionalProperties": False,
        }

    def _tool_definitions(self) -> list[dict[str, Any]]:
        campaign = self._descriptor().get("session_scope") == "campaign"
        snapshot_schema = self._belief_snapshot_schema() if campaign else {"type": "object"}
        contract = (
            _read_object(self.reference / "belief_checkpoint_contract.json")
            if campaign
            else {}
        )
        checkpoint_counts = contract.get("checkpoint_complete_experiments", [])
        completed_experiment_limit = (
            max(int(item) for item in checkpoint_counts) if checkpoint_counts else 1
        )
        read_annotations = {
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
        return [
            {
                "name": "material_information",
                "description": "Read the bounded material information assigned to this cell once.",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                "annotations": read_annotations,
            },
            {
                "name": "status",
                "description": "Read the latest bounded public experiment and campaign state.",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
                "annotations": read_annotations,
            },
            {
                "name": "history",
                "description": "Read a bounded non-authoritative cache of recent public outcomes.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 10}},
                    "additionalProperties": False,
                },
                "annotations": read_annotations,
            },
            {
                "name": "inspect_artifact",
                "description": (
                    "Read one bounded fragment of a referenced public "
                    "characterization artifact."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "artifact_id": {"type": "string", "minLength": 1},
                        "offset": {"type": "integer", "minimum": 0},
                        "limit": {"type": "integer", "minimum": 1},
                    },
                    "required": ["artifact_id"],
                    "additionalProperties": False,
                },
                "annotations": read_annotations,
            },
            {
                "name": "commit_belief_snapshot",
                "description": (
                    "Commit the next required typed Work II belief snapshot inside the active "
                    "campaign session. The host validates stage order, experiment-count location, "
                    "evidence references, held-out predictions, and executable law summary."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {"snapshot": snapshot_schema},
                    "required": ["snapshot"],
                    "additionalProperties": False,
                },
                "annotations": {
                    "readOnlyHint": False,
                    "destructiveHint": False,
                    "idempotentHint": False,
                    "openWorldHint": False,
                },
            },
            {
                "name": "commit_final_recommendation",
                "description": (
                    "After campaign terminal and the final belief checkpoint, commit exactly one "
                    "participant-selected completed experiment for evaluator-owned blind replay. "
                    "The index is 1-based and uses the same namespace as public campaign history. "
                    "The host stores the selection atomically; a repeated identical call is "
                    "idempotent and a differing second selection is rejected."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "selected_experiment_index": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": completed_experiment_limit,
                        },
                        "selection_rationale": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 2000,
                        },
                    },
                    "required": ["selected_experiment_index", "selection_rationale"],
                    "additionalProperties": False,
                },
                "annotations": {
                    "readOnlyHint": False,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": False,
                },
            },
            {
                "name": "step",
                "description": (
                    "Submit exactly one operation to the authoritative ChemWorld "
                    "runner and wait for its public outcome. In campaign scope, a batch "
                    "ending does not close this tool; campaign_ended=true closes it."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expected_step": {"type": "integer", "minimum": 1},
                        "action": {
                            "type": "object",
                            "properties": {"operation": {"type": "string", "minLength": 1}},
                            "required": ["operation"],
                            "additionalProperties": True,
                        },
                        "request_id": {"type": "string", "minLength": 1},
                        "decision_audit": self._decision_audit_schema(),
                    },
                    "required": (
                        ["expected_step", "action", "decision_audit"]
                        if campaign
                        else ["expected_step", "action"]
                    ),
                    "additionalProperties": False,
                },
                "annotations": {
                    "readOnlyHint": False,
                    "destructiveHint": False,
                    "idempotentHint": False,
                    "openWorldHint": False,
                },
            },
        ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args(argv)
    return ChemWorldMCPServer(args.workspace).run()


if __name__ == "__main__":
    raise SystemExit(main())
