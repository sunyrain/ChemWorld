from __future__ import annotations

import json
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path

import pytest
from scripts.community_release_build import (
    BUILD_HOOK,
    RUNTIME_CONFIGS,
    SOURCE_INDEX,
    public_path,
    selected_files,
    wheel_destination,
)


def source_tree(tmp_path):
    names = [BUILD_HOOK, "src/chemworld/__init__.py", *RUNTIME_CONFIGS]
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
    return sorted(names)


def test_only_tracked_approved_files_enter_distribution(tmp_path):
    names = source_tree(tmp_path)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    (tmp_path / "src/chemworld/local_notes.py").write_text("SECRET", encoding="utf-8")
    (tmp_path / "configs/private_eval.json").write_text("SECRET", encoding="utf-8")
    subprocess.run(["git", "add", "configs/private_eval.json"], cwd=tmp_path, check=True)
    assert selected_files(tmp_path) == names


def test_sdist_index_rebuild_needs_no_git_and_rejects_unsafe_paths(tmp_path):
    names = source_tree(tmp_path)
    index = tmp_path / SOURCE_INDEX
    index.write_text(json.dumps(names), encoding="utf-8")
    assert selected_files(tmp_path) == names
    index.write_text(json.dumps([*names, "../api.md"]), encoding="utf-8")
    with pytest.raises(ValueError, match="non-public"):
        selected_files(tmp_path)


def test_missing_or_symlinked_public_file_fails_closed(tmp_path):
    names = source_tree(tmp_path)
    (tmp_path / SOURCE_INDEX).write_text(json.dumps(names), encoding="utf-8")
    (tmp_path / "src/chemworld/__init__.py").unlink()
    with pytest.raises(ValueError, match="missing or unsafe"):
        selected_files(tmp_path)


@pytest.mark.parametrize(
    "name",
    [
        "api.md",
        ".env",
        "paper/draft.md",
        "output/figure.png",
        "runs/trajectory.jsonl",
        "configs/current.json",
        "configs/private_eval.placeholder.json",
        "configs/providers/models.json",
        "configs/benchmark/work_ii_campaign.json",
        "src/chemworld/__pycache__/x.py",
        "src/chemworld/../secret.py",
    ],
)
def test_research_and_private_inputs_are_outside_distribution(name):
    assert not public_path(name)


def test_config_resources_map_inside_package():
    assert wheel_destination("configs/benchmark/resource_limits.json") == (
        "chemworld/resources/configs/benchmark/resource_limits.json"
    )
    assert wheel_destination("README.md") is None
    assert wheel_destination("src/chemworld/tasks.py") == "chemworld/tasks.py"


def test_actual_archives_ignore_extra_local_files_and_rebuild_without_git(tmp_path):
    root = Path(__file__).resolve().parents[1]
    source = tmp_path / "source"
    names = selected_files(root)
    for name in names:
        target = source / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    subprocess.run(["git", "init", "-q", str(source)], check=True)
    subprocess.run(["git", "add", "."], cwd=source, check=True)

    def build(label):
        out = tmp_path / label
        # uv's default builds the wheel FROM the sdist, exercising the no-Git path.
        subprocess.run(
            ["uv", "build", "--out-dir", str(out)],
            cwd=source,
            check=True,
            capture_output=True,
            text=True,
        )
        with zipfile.ZipFile(next(out.glob("*.whl"))) as archive:
            wheel = {name: archive.read(name) for name in archive.namelist()}
        with tarfile.open(next(out.glob("*.tar.gz"))) as archive:
            sdist = {m.name: archive.extractfile(m).read() for m in archive if m.isfile()}
        return wheel, sdist

    clean = build("clean")
    for name in (
        "src/chemworld/local_private.py",
        "configs/mechanisms/local_private.yaml",
        "configs/providers/credentials.json",
        "paper/draft.md",
        "notes.txt",
    ):
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("UNTRACKED_PRIVATE_SENTINEL", encoding="utf-8")
    dirty = build("dirty")
    assert clean == dirty
    wheel, sdist = dirty
    assert not any(
        b"UNTRACKED_PRIVATE_SENTINEL" in data for data in [*wheel.values(), *sdist.values()]
    )
    resources = {
        name.removeprefix("chemworld/resources/")
        for name in wheel
        if name.startswith("chemworld/resources/configs/")
    }
    assert RUNTIME_CONFIGS.issubset(resources)
    assert "chemworld/schemas/action_schema.json" in wheel
    assert not any("/configs/providers/" in name or "/paper/" in name for name in sdist)
