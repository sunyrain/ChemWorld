"""Small executable checks for the current public onboarding path, not an audit framework."""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import gymnasium as gym

import chemworld  # noqa: F401 -- registers the environment

ROOT = Path(__file__).resolve().parents[1]


def test_onboarding_action_literals_have_required_fields():
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        for name in ("action_schema.md", "operations.md", "operations.en.md"):
            text = (ROOT / "docs" / name).read_text(encoding="utf-8")
            for block in re.findall(r"```python\n(.*?)```", text, re.S):
                for node in ast.walk(ast.parse(block)):
                    if not isinstance(node, ast.Dict):
                        continue
                    try:
                        action = ast.literal_eval(node)
                    except (ValueError, TypeError):
                        continue
                    if "operation" in action:
                        schema = env.unwrapped.action_schema(action["operation"])
                        assert schema["valid_operation_type"], (name, action)
                        assert set(schema["required_fields"]) <= set(action), (name, action)
    finally:
        env.close()


def test_documented_recipe_is_a_real_completed_experiment():
    text = (ROOT / "docs/action_schema.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```python\n(.*?)```", text, re.S)
    recipe = None
    for block in blocks:
        tree = ast.parse(block)
        for statement in tree.body:
            if isinstance(statement, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "recipe"
                for target in statement.targets
            ):
                recipe = ast.literal_eval(statement.value)
    assert recipe is not None
    env = gym.make("ChemWorld", task_id="reaction-to-assay", seed=0)
    try:
        env.reset(seed=0)
        for action in recipe:
            _, _, terminated, truncated, info = env.step(action)
            assert info["transaction_status"] == "committed", (action, info["constraint_flags"])
        assert terminated and not truncated
        assert info["instrument"] == "final_assay"
        # Single-experiment mode terminates directly; campaign summaries are not populated.
        assert info["observed_mask"]["score"] is True
    finally:
        env.close()


def test_minimal_custom_agent_runs_outside_checkout(tmp_path):
    output = tmp_path / "minimal.jsonl"
    result = subprocess.run(
        [sys.executable, str(ROOT / "examples/demo_minimal_agent.py"), "--output", str(output)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert payload["formal_result"] is False
    assert payload["final_assay_completed"]
    assert payload["replay"]["verified"]


def test_bilingual_entrypoints_include_current_complete_example():
    for suffix in (".md", ".en.md"):
        text = (ROOT / ("docs/getting_started" + suffix)).read_text(encoding="utf-8")
        assert "uv sync --locked --extra dev" in text
        assert "demo_minimal_agent.py" in text
        assert "demo_offline_research.py" in text
        assert "03e8026301c185fd6ba5bdbda7460765d9b3e724" in text
        assert (ROOT / ("docs/offline_research" + suffix)).is_file()
