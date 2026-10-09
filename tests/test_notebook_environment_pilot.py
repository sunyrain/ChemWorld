from __future__ import annotations

import json

from scripts.run_notebook_environment_pilot import run, token_count

from chemworld.providers.deepseek import JsonCompletion


def test_token_limit_uses_adapter_usage_without_double_counting():
    assert token_count({"prompt_tokens": 299900, "completion_tokens": 100}) == 300000
    assert token_count({"prompt_tokens": 9, "completion_tokens": 1, "total_tokens": 10}) == 10
    assert token_count({"input_tokens": 7, "output_tokens": 3}) == 10


def test_pilot_executes_and_resets_context_without_loading_notebook(tmp_path):
    actions = [
        {"operation": "add_solvent", "solvent": 0, "volume_L": 0.015},
        {"operation": "add_solvent", "solvent": 1, "volume_L": 0.015},
        {"operation": "add_reagent", "amount_mol": 0.012},
        {
            "operation": "heat",
            "target_temperature_K": 350,
            "duration_s": 600,
            "stirring_speed_rpm": 600,
        },
        {
            "operation": "configure_instrument",
            "instrument": "nmr",
            "scan_count": 8,
            "resolution_factor": 1,
            "dilution_factor": 1,
        },
        {"operation": "measure", "instrument": "nmr"},
        {"operation": "terminate"},
        {"operation": "measure", "instrument": "final_assay"},
    ]
    queue = [("notebook.write", {"text": "DO_NOT_AUTOINJECT_THIS_NOTE"})]
    queue += [("lab.step", {"action": a}) for a in actions]
    queue += [("lab.next_batch", {})]
    queue += [("lab.step", {"action": a}) for a in actions]
    queue += [("finish", {"report": "Scripted harness check, not an LLM result."})]

    class ScriptedClient:
        def __init__(self, **kwargs):
            self.calls = 0

        def pricing_snapshot(self):
            return {"provider": "scripted_test_double"}

        def complete_json(self, *, user_prompt, **kwargs):
            prompt = json.loads(user_prompt)
            if prompt["batch"] == 2:
                assert "DO_NOT_AUTOINJECT_THIS_NOTE" not in user_prompt
                assert all(e.get("batch", 2) == 2 for e in prompt["interaction"])
            tool, args = queue[self.calls]
            self.calls += 1
            return JsonCompletion(
                payload={"tool": tool, "arguments": json.dumps(args), "rationale": "scripted test"},
                model="test",
                usage={"input_tokens": 1, "output_tokens": 1},
            )

    result = run(tmp_path / "pilot", client_factory=ScriptedClient)
    assert result["passed"], result
    assert result["completed_batches"] == 2
    assert result["operation_count"] == 16
    assert result["context_resets"] == 1
    assert result["tool_counts"].get("notebook.read", 0) == 0
