from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_work_ii_w2_27_selected_resource_card.py"


def _load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "build_work_ii_w2_27_selected_resource_card",
        SCRIPT,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cli_writes_receipt_and_prints_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = _load_script()
    repository = tmp_path / "repo"
    manifest = repository / "manifest.json"
    terminal = repository / "terminal.json"
    output = repository / "receipt.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text("{}", encoding="utf-8")
    terminal.write_text("{}", encoding="utf-8")
    receipt = {
        "status": "selected_card_passed",
        "selected_resource_card_sha256": "1" * 64,
        "selected_card_receipt_sha256": "2" * 64,
    }
    observed: dict[str, Path] = {}

    def _build(root: Path, manifest_path: Path, terminal_path: Path) -> dict[str, object]:
        observed.update(
            root=root,
            manifest=manifest_path,
            terminal=terminal_path,
        )
        return receipt

    monkeypatch.setattr(module, "ROOT", repository)
    monkeypatch.setattr(module, "build_w2_27_selected_resource_card_receipt", _build)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            str(SCRIPT),
            "--w2-26-manifest",
            str(manifest),
            "--ae-electrochemical-terminal-triplet",
            str(terminal),
            "--output",
            str(output),
        ],
    )

    assert module.main() == 0
    assert json.loads(output.read_text(encoding="utf-8")) == receipt
    assert observed == {
        "root": repository.resolve(),
        "manifest": manifest.resolve(),
        "terminal": terminal.resolve(),
    }
    assert json.loads(capsys.readouterr().out) == {
        "output": "receipt.json",
        "selected_card_receipt_sha256": "2" * 64,
        "selected_resource_card_sha256": "1" * 64,
        "status": "selected_card_passed",
    }


def test_build_receipt_refuses_to_overwrite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _load_script()
    repository = tmp_path / "repo"
    repository.mkdir()
    manifest = repository / "manifest.json"
    terminal = repository / "terminal.json"
    output = repository / "receipt.json"
    output.write_text("retained", encoding="utf-8")
    monkeypatch.setattr(module, "ROOT", repository)

    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        module.build_receipt(manifest, terminal, output)

    assert output.read_text(encoding="utf-8") == "retained"


@pytest.mark.parametrize("argument", ["manifest", "terminal", "output"])
def test_build_receipt_rejects_paths_outside_repository(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    argument: str,
) -> None:
    module = _load_script()
    repository = tmp_path / "repo"
    repository.mkdir()
    paths = {
        "manifest": repository / "manifest.json",
        "terminal": repository / "terminal.json",
        "output": repository / "receipt.json",
    }
    paths[argument] = tmp_path / "outside.json"
    monkeypatch.setattr(module, "ROOT", repository)

    with pytest.raises(ValueError, match="inside the repository"):
        module.build_receipt(paths["manifest"], paths["terminal"], paths["output"])
