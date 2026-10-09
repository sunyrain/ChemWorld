from __future__ import annotations

import subprocess
import sys

import pytest

from chemworld.cli import main


@pytest.mark.parametrize(
    "arguments",
    [
        ["tasks", "show", "missing-task"],
        ["scenarios", "show", "missing-scenario"],
        ["run", "--env", "MissingChemWorld", "--budget", "1"],
        ["verify", "--submission", "missing-trajectory.jsonl"],
    ],
)
def test_cli_known_input_errors_have_short_diagnostics_without_tracebacks(arguments):
    result = subprocess.run(
        [sys.executable, "-m", "chemworld.cli", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "chemworld: error:" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("contents", ["{", "[]", "null"])
def test_cli_malformed_jsonl_has_path_and_line_number(contents, tmp_path, capsys):
    path = tmp_path / "bad.jsonl"
    path.write_text(contents, encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["verify", "--submission", str(path)])
    assert exc.value.code == 2
    assert f"{path}:1:" in capsys.readouterr().err


def test_cli_bad_action_shape_is_an_input_error(tmp_path, capsys):
    path = tmp_path / "action.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        main(["validate-action", "--task", "reaction-to-assay", "--action", str(path)])
    assert exc.value.code == 2
    assert "JSON object" in capsys.readouterr().err
