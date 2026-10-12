"""Bounded local workers. Credentials live only on the model client in memory."""

# ruff: noqa: RUF001 -- Chinese user-facing messages use Chinese punctuation.

from __future__ import annotations

import json
import threading
from copy import deepcopy
from time import monotonic
from typing import Any

from chemworld.workbench.providers import ModelClient, ProviderError
from chemworld.workbench.service import ResearchRun, ResearchStore, integer


class Jobs:
    def __init__(self, store: ResearchStore) -> None:
        self.store = store
        self.slots = threading.BoundedSemaphore(2)
        self.threads: list[threading.Thread] = []

    def start(self, run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        run = self.store.get(run_id)
        mode = payload.get("mode", "reference")
        if mode not in {"reference", "model"}:
            raise ValueError("mode must be reference or model")
        call_limit = integer(payload.get("call_limit", 24), "call_limit", 1, 80)
        token_limit = integer(payload.get("token_limit", 100000), "token_limit", 1000, 1000000)
        wall_limit = integer(payload.get("wall_limit", 900), "wall_limit", 30, 1800)
        client = ModelClient(payload, payload.get("api_key", "")) if mode == "model" else None
        with run.lock:
            if run.env is None or run.data["status"] != "ready" or run.data["events"]:
                if client:
                    client.close()
                raise ValueError(
                    "Start an automatic worker on a fresh run; clone this design first"
                )
            if not self.slots.acquire(blocking=False):
                if client:
                    client.close()
                raise ValueError("Two workers are already running")
            run.data.update(status="running", actor="reference" if client is None else client.model)
            run.data["limits"] = {
                "call_limit": call_limit,
                "token_stop_threshold": token_limit,
                "wall_limit_s": wall_limit,
            }
            if client:
                run.data["provider"] = client.provider
                run.data["model_configuration"] = {
                    "requested_model": client.model,
                    "max_output": client.max_output,
                }
            run.persist()
            thread = threading.Thread(
                target=self._run,
                args=(run, client, call_limit, token_limit, wall_limit),
                daemon=True,
            )
            self.threads.append(thread)
            thread.start()
        return run.snapshot()

    def _run(
        self,
        run: ResearchRun,
        client: ModelClient | None,
        calls: int,
        token_limit: int,
        wall_limit: int,
    ) -> None:
        started = monotonic()
        last_result: Any = None
        stop_message = "达到模型调用上限；未终检的批次保留为未完成。"
        try:
            if client is None:
                stop_message = "参考流程已结束；未终检的批次保留为未完成。"
                for action in deepcopy(run.data["recipe"]):
                    if run.cancel.wait(0.18) or run.data["status"] != "running":
                        break
                    event = run.step(action)
                    if event["transaction_status"] != "committed":
                        run.stop("failed", "参考配方遇到拒绝，已保留失败；可复制设计后手动调整。")
                        break
            else:
                for _ in range(calls):
                    remaining = wall_limit - (monotonic() - started)
                    if remaining <= 0 or run.cancel.is_set() or run.data["status"] != "running":
                        if remaining <= 0:
                            stop_message = "达到运行时间阈值，不再发出请求。"
                        break
                    with run.lock:
                        packet = {
                            "question": run.data["question"],
                            "task": run.data["task_prompt"],
                            "state": run.data["view"],
                            "recent_events": [
                                {k: v for k, v in e.items() if k != "series"}
                                for e in run.data["events"][-6:]
                            ],
                            "total_events": len(run.data["events"]),
                            "previous_tool_result": last_result,
                            "remaining_model_calls": calls - run.data["model_calls"],
                        }
                        run.data["model_calls"] += 1
                        run.data["message"] = "等待模型响应…"
                        run.persist()
                    completion = client.complete(packet, timeout=min(45, remaining))
                    with run.lock:
                        usage = run.data["usage"]
                        complete = (
                            completion.input_tokens is not None
                            and completion.output_tokens is not None
                        )
                        usage["complete"] = usage["complete"] and complete
                        usage["input_tokens"] += completion.input_tokens or 0
                        usage["output_tokens"] += completion.output_tokens or 0
                        run.data.setdefault("model_receipts", []).append(
                            {
                                "call": run.data["model_calls"],
                                "model": completion.model,
                                "input_tokens": completion.input_tokens,
                                "output_tokens": completion.output_tokens,
                                "error": completion.error,
                                "tool": (completion.decision or {}).get("tool"),
                            }
                        )
                        run.persist()
                    if run.cancel.is_set() or monotonic() - started >= wall_limit:
                        stop_message = "达到运行时间阈值，不再执行后续操作。"
                        break  # Account for an in-flight response, but never execute after cancel.
                    if completion.error or not complete:
                        raise ProviderError(completion.error or "usage_missing")
                    decision = completion.decision
                    with run.lock:
                        if run.cancel.is_set():
                            break
                        last_result = self._tool(run, decision["tool"], decision["arguments"])
                    if usage["input_tokens"] + usage["output_tokens"] >= token_limit:
                        stop_message = "达到 token 停止阈值；不再发出请求。"
                        break
            run.stop(
                "cancelled" if run.cancel.is_set() else "stopped",
                "已取消；在途模型请求可能仍计费。"
                if run.cancel.is_set()
                else run.data.get("message")
                if run.data["status"] == "failed"
                else stop_message
                if not run.data["final_assay_count"]
                else "已完成终检，记录已保存。",
            )
        except ProviderError as exc:
            with run.lock:
                receipts = run.data.get("model_receipts", [])
                if not receipts or receipts[-1]["call"] != run.data["model_calls"]:
                    run.data["usage"]["complete"] = False
            run.stop("failed", f"模型请求停止：{exc}。没有自动重试；请检查模型、额度与接口支持。")
        except Exception as exc:
            run.data["internal_error_type"] = type(exc).__name__
            run.stop("failed", "执行异常，已保留已提交记录；未自动重试或补造结果。")
        finally:
            if client:
                client.close()
            with run.lock:
                run.data["wall_time_s"] = round(monotonic() - started, 3)
                run.persist()
            self.slots.release()

    @staticmethod
    def _tool(run: ResearchRun, tool: str, arguments: dict[str, Any]) -> Any:
        try:
            if tool == "act":
                return run.step(arguments["action"])
            if tool == "history":
                offset = integer(arguments.get("offset", 0), "offset", 0, 240)
                limit = integer(arguments.get("limit", 10), "limit", 1, 10)
                return [
                    {k: v for k, v in e.items() if k != "series"}
                    for e in run.data["events"][offset : offset + limit]
                ]
            if tool == "measurement":
                event_id = arguments["event_id"]
                event = next(e for e in run.data["events"] if e.get("measurement") == event_id)
                raw = json.loads(
                    (run.root / "measurements" / (event["measurement"] + ".json")).read_text(
                        encoding="utf-8"
                    )
                )
                # Model gets the same displayed public signal; full raw packet remains downloadable.
                return {
                    "series": event.get("series", []),
                    "processed_estimate": raw.get("processed_estimates", {}),
                    "event_id": event_id,
                }
            if tool in {"notebook_read", "notebook_write"}:
                if len(str(arguments.get("text", ""))) > 16000:
                    raise ValueError("Notebook limit is 16000 characters")
                return run.notebook("model", tool.removeprefix("notebook_"), arguments)
            if tool == "finish":
                report = arguments.get("report", "")
                if not isinstance(report, str) or len(report) > 16000:
                    raise ValueError("Report must be text of at most 16000 characters")
                with run.lock:
                    run.data["model_report"] = report
                    run.data["status"] = "stopped"
                    run.persist()
                return {"stopped": True}
            return {"error": "Unknown tool"}
        except (ValueError, KeyError, TypeError, StopIteration):
            return {"error": "Invalid tool arguments; check the public tool contract"}

    def cancel(self, run_id: str) -> dict[str, Any]:
        run = self.store.get(run_id)
        with run.lock:
            run.cancel.set()
            if run.data["status"] == "running":
                run.data["status"] = "cancelling"
                run.data["message"] = "正在取消；等待当前请求结束或网络超时，不再提交新动作。"
                run.persist()
            elif run.data["status"] == "ready":
                run.stop("cancelled", "已关闭手动实验，已有记录保留。")
            return run.snapshot()
