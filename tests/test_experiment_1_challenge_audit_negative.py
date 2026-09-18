from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from chemworld.eval.provenance import canonical_json_sha256

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_experiment_1_challenge.py"


def _module():
    spec = importlib.util.spec_from_file_location("experiment_1_challenge_audit_negative", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("key", "payload"),
    [
        ("registry_sha256", {"rows": []}),
        ("manifest_sha256", {"rows": []}),
        ("challenge_probe_sha256", {"loci": []}),
        ("audit_sha256", {"loci": []}),
    ],
)
def test_audit_rejects_forged_canonical_self_hash(key: str, payload: dict[str, object]) -> None:
    payload[key] = canonical_json_sha256(payload)
    payload["forged"] = True
    with pytest.raises(ValueError, match="canonical self-hash mismatch"):
        _module()._verify_self_hash(payload, key)


def test_audit_rejects_registry_path_escape() -> None:
    with pytest.raises(ValueError, match="escapes"):
        _module()._bound_path("../../forged-registry.json")
