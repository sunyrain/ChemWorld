import json
import os
import subprocess
import sys

from scripts import check_abductive_source_runtime as s


def test_environment_probe_preserves_script_entrypoint(tmp_path):
    wrapper, entry = tmp_path / "probe.py", tmp_path / "public_numerics.py"
    wrapper.write_text(s.ENV_WRAPPER, encoding="utf-8")
    entry.write_text("import sys; print('real script', sys.argv[1])", encoding="utf-8")
    observed = tmp_path / "environment.json"
    result = subprocess.run(
        [sys.executable, str(wrapper), str(observed), str(entry), "argument"],
        env={**os.environ, **s.run.WORKER_ENV},
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() == "real script argument"
    assert json.loads(observed.read_text()) == s.run.WORKER_ENV


def test_environment_probe_preserves_module_entrypoint(tmp_path):
    wrapper = tmp_path / "probe.py"
    wrapper.write_text(s.ENV_WRAPPER, encoding="utf-8")
    observed = tmp_path / "environment.json"
    result = subprocess.run(
        [sys.executable, str(wrapper), str(observed), "-m", "json.tool"],
        input='{"real_module":true}',
        env={**os.environ, **s.run.WORKER_ENV},
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout) == {"real_module": True}
    assert json.loads(observed.read_text()) == s.run.WORKER_ENV
