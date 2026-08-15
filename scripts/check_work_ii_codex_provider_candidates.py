"""Statically check candidate providers for the Work II Codex harness.

This command never contacts a provider and never prints credential values.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Any

from chemworld.agents.interactive_codex_experiment import InteractiveCodexExperimentAgent

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIGS = (
    ROOT
    / "configs/benchmark/work_ii_campaign_pilot_qwen3_8_max_codex_harness_canary.json",
    ROOT
    / "configs/benchmark/work_ii_campaign_pilot_kimi_k2_5_openrouter_codex_harness_canary.json",
)


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def check_candidate(path: Path) -> dict[str, Any]:
    config = _read_object(path)
    provider = config.get("provider")
    if not isinstance(provider, dict):
        raise ValueError(f"provider object is missing: {path}")
    catalog_path = (ROOT / str(provider.get("model_catalog_json", ""))).resolve()
    catalog = _read_object(catalog_path)
    models = catalog.get("models")
    if not isinstance(models, list):
        raise ValueError(f"model catalog has no models list: {catalog_path}")
    model = str(provider.get("model", ""))
    model_found = any(isinstance(item, dict) and item.get("slug") == model for item in models)
    env_key = str(provider.get("env_key", ""))
    agent = InteractiveCodexExperimentAgent(
        workspace=ROOT,
        role_id="provider_static_canary",
        model=model,
        reasoning_effort=str(provider.get("reasoning_effort", "high")),
        model_provider=str(provider.get("id", "")),
        model_provider_name=str(provider.get("name", "")),
        model_provider_base_url=str(provider.get("base_url", "")),
        model_provider_env_key=env_key,
        model_provider_wire_api=str(provider.get("wire_api", "")),
        model_provider_auth_mode="env_key",
        model_provider_model_catalog_json=catalog_path,
        process_factory=lambda command, prompt, cwd: None,
    )
    command = agent._command(
        instructions_path=ROOT / "AGENTS.md",
        schema_path=ROOT / "configs/benchmark/work_ii_agent_operation_schema.json",
    )
    rendered = " ".join(command)
    expected_fragments = (
        f'model_provider="{provider["id"]}"',
        f'model_providers.{provider["id"]}.wire_api="responses"',
        f'model_providers.{provider["id"]}.env_key="{env_key}"',
        catalog_path.as_posix(),
    )
    command_contract_ready = all(fragment in rendered for fragment in expected_fragments)
    static_ready = bool(
        config.get("formal_result") is False
        and provider.get("wire_api") == "responses"
        and str(provider.get("base_url", "")).startswith("https://")
        and env_key
        and model_found
        and command_contract_ready
    )
    return {
        "config": path.relative_to(ROOT).as_posix(),
        "provider_id": provider.get("id"),
        "model": model,
        "model_catalog_entry_found": model_found,
        "codex_command_contract_ready": command_contract_ready,
        "codex_cli_available": shutil.which("codex") is not None,
        "credential_env_key": env_key,
        "credential_available": bool(os.environ.get(env_key)),
        "static_harness_ready": static_ready,
        "live_provider_call_performed": False,
        "qualification": config.get("provider_qualification"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("configs", nargs="*", type=Path)
    args = parser.parse_args()
    paths = tuple(path.resolve() for path in args.configs) or DEFAULT_CONFIGS
    checks = [check_candidate(path) for path in paths]
    payload = {
        "schema_version": "chemworld-work-ii-codex-provider-static-check-0.1",
        "paid_provider_calls": 0,
        "all_static_harness_ready": all(check["static_harness_ready"] for check in checks),
        "candidates": checks,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["all_static_harness_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
