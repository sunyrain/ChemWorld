from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "paper/tools/build_prior_discovery_supplement.py"

REQUIRED_MEMBERS = {
    "manifest.json",
    "verify_supplement.py",
    "data/publication_report.json",
    "data/b2_public_summary_rows.jsonl",
    "data/b2_identifiability_audit.json",
    "data/b2_configuration_summaries.json",
    "data/b3_cell_records.jsonl",
    "methods/b2_expression_coding.py",
}
IDENTITY_STRINGS = (
    "Jiangjie Qiu",
    "Yijun Li",
    "Yaotian Yang",
    "Honghao Chen",
    "Wentao Li",
    "Xiaonan Wang",
    "wangxiaonan@tsinghua.edu.cn",
    "Tsinghua University",
)


def _load_builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "prior_discovery_supplement_builder_for_test", BUILDER_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _contrast(rows: list[dict[str, Any]], name: str) -> dict[str, Any]:
    return next(row for row in rows if row["contrast"] == name)


@pytest.fixture
def isolated_supplement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, dict[str, Any]]:
    builder = _load_builder()
    output_zip = tmp_path / "anonymous-supplement.zip"
    original_write_zip = builder._write_zip

    monkeypatch.setattr(builder, "EXPORT_DIR", tmp_path)
    monkeypatch.setattr(builder, "OUTPUT_ZIP", output_zip)

    def isolated_write_zip(files: dict[str, bytes]) -> None:
        original_write_zip(files)
        # ROOT is only needed for source reads before this final write. Rebase it here so
        # the builder's returned display path can remain relative without touching the repo.
        monkeypatch.setattr(builder, "ROOT", tmp_path)

    monkeypatch.setattr(builder, "_write_zip", isolated_write_zip)
    result = builder.build()
    assert result["status"] == "anonymous_supplement_built"
    assert output_zip.is_file()
    return output_zip, result


def test_anonymous_supplement_projection_and_standalone_verifier(
    isolated_supplement: tuple[Path, dict[str, Any]], tmp_path: Path
) -> None:
    output_zip, result = isolated_supplement
    assert result["file_count"] >= len(REQUIRED_MEMBERS)

    with zipfile.ZipFile(output_zip) as archive:
        names = set(archive.namelist())
        assert names >= REQUIRED_MEMBERS
        assert all(not Path(name).is_absolute() for name in names)
        contents = {name: archive.read(name) for name in names}

    assert len(
        [
            line
            for line in contents["data/b3_cell_records.jsonl"].decode("utf-8").splitlines()
            if line.strip()
        ]
    ) == 60

    text = "\n".join(content.decode("utf-8") for content in contents.values())
    assert re.search(r"(?i)\bW2[-_]\d+\b", text) is None
    assert re.search(r"(?i)(?:^|[\s\"'/])runs[\\/]", text) is None
    assert re.search(r"(?i)(?:^|[\s\"'])(?:[A-Z]:[\\/])", text) is None
    assert re.search(r"(?i)/(?:home|Users|root)/", text) is None
    assert (
        re.search(
            r'(?i)"[^"]*(?:credential|api[_-]?key|access[_-]?token|bearer[_-]?token|secret)[^"]*"\s*:',
            text,
        )
        is None
    )
    for identity in IDENTITY_STRINGS:
        assert identity.casefold() not in text.casefold()

    publication = json.loads(contents["data/publication_report.json"])
    assert publication["new_formal_execution"] is False
    assert "No new formal execution" in publication["formal_result_scope"]
    assert publication["claim_boundaries"]["stochastic_participant_effect_identified"] is False
    readme = contents["README.md"].decode("utf-8")
    assert "formal_result=false" in readme
    assert "new formal execution" in readme
    b2 = publication["b2_expression_and_identifiability"]
    assert len(b2["public_summary_rows"]) == 45
    assert (
        b2["participant_visible_identifiability"]["decision"][
            "structural_family_identification_supported"
        ]
        is False
    )
    assert b2["participant_visible_identifiability"]["exact_alias"]["present"] is True
    assert (
        b2["participant_visible_identifiability"]["positive_control"][
            "readout_positive_control_passed"
        ]
        is False
    )
    models = publication["action_extension"]["models"]
    assert set(models) == {"deepseek", "gpt_5_6_sol"}
    assert "codex" not in models
    for model in models.values():
        assert model["primary_all_scheduled"]["estimand"] == (
            "all-scheduled failure-aware strategy estimand"
        )
        assert model["primary_all_scheduled"]["scheduled_stratum_count"] == 45

    effect = "mean_failure_aware_normalized_regret_difference"
    deepseek = models["deepseek"]["primary_all_scheduled"]["contrasts"]
    gpt = models["gpt_5_6_sol"]["primary_all_scheduled"]["contrasts"]
    assert _contrast(deepseek, "autonomous_exploration_minus_no_evidence")[effect] == pytest.approx(
        -0.0913, abs=5e-5
    )
    assert _contrast(gpt, "autonomous_exploration_minus_no_evidence")[effect] == pytest.approx(
        0.1102, abs=5e-5
    )

    extracted = tmp_path / "extracted"
    extracted.mkdir()
    with zipfile.ZipFile(output_zip) as archive:
        archive.extractall(extracted)
    verified = subprocess.run(
        [sys.executable, "verify_supplement.py"],
        cwd=extracted,
        capture_output=True,
        check=False,
        text=True,
    )
    assert verified.returncode == 0, verified.stderr
    assert "verified" in verified.stdout
