"""Demo: deterministic LLM-style replay harness."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from chemworld.agents.llm import LLMReplayAgent, ToolUsingLLMStubAgent
from chemworld.data.logging import load_jsonl
from chemworld.eval.runner import run_agent


def main() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        trace_path = root / "llm_trace.jsonl"
        output_path = root / "run.jsonl"
        actions = [
            {"action": {"operation": "add_solvent", "volume_L": 0.028, "solvent": 2}},
            {"action": {"operation": "add_reagent", "amount_mol": 0.010}},
            {
                "action": {
                    "operation": "add_catalyst",
                    "catalyst_amount_mol": 0.00025,
                    "catalyst": 1,
                }
            },
            {
                "action": {
                    "operation": "heat",
                    "target_temperature_K": 382.0,
                    "duration_s": 1350.0,
                    "stirring_speed_rpm": 720.0,
                }
            },
            {"action": {"operation": "quench"}},
            {"action": {"operation": "terminate"}},
            {"action": {"operation": "measure", "instrument": "final_assay"}},
        ]
        trace_path.write_text(
            "\n".join(json.dumps(action, sort_keys=True) for action in actions),
            encoding="utf-8",
        )

        history = run_agent(
            env_id="ChemWorld",
            agent=LLMReplayAgent(trace_path),
            world_split="public-dev",
            budget=18,
            objective="balanced",
            seed=0,
            task_id="reaction-to-assay",
            output_path=output_path,
        )
        print("Replay final reward:", history[-1].reward)
        records = load_jsonl(output_path)
        print("Logged agent trace entries:", len(records[-1]["agent_trace"]))
        print("Final lab report:")
        print(records[-1]["agent_view"]["lab_report"]["text"])

        stub_history = run_agent(
            env_id="ChemWorld",
            agent=ToolUsingLLMStubAgent(),
            world_split="public-dev",
            budget=18,
            objective="balanced",
            seed=0,
            task_id="reaction-to-assay",
        )
        print("ToolUsingLLMStub final reward:", stub_history[-1].reward)


if __name__ == "__main__":
    main()
