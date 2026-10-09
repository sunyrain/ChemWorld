from scripts.smoke_test_wheel import PROBE, clean_environment


def test_installed_smoke_does_not_inherit_editable_imports(monkeypatch):
    monkeypatch.setenv("PYTHONPATH", "/private/checkout/src")
    monkeypatch.setenv("PYTHONHOME", "/other/python")
    monkeypatch.setenv("VIRTUAL_ENV", "/editable/venv")
    env = clean_environment()
    assert "PYTHONPATH" not in env
    assert "PYTHONHOME" not in env
    assert "VIRTUAL_ENV" not in env
    assert env["PYTHONNOUSERSITE"] == "1"


def test_current_installation_probe_does_not_require_frozen_research_evidence():
    assert "mechanism_adaptation_execution" not in PROBE
    assert "is_relative_to(Path(sys.prefix)" in PROBE
    assert "for task in list_tasks()" in PROBE
    compile(PROBE, "installed-package-probe", "exec")
