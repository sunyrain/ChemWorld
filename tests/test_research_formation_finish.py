import pytest
from scripts import finish_research_formation as finish


def test_concurrent_target_edits_are_preserved_before_export(tmp_path, monkeypatch):
    calls = []

    def git(*args):
        calls.append(args)
        return "main" if args[0] == "branch" else finish.TODO_REL

    monkeypatch.setattr(finish, "git", git)
    with pytest.raises(RuntimeError, match="concurrent edits"):
        finish.finish(tmp_path, tmp_path / "external", tmp_path / "status.json")
    assert not any(args[0] in {"add", "commit", "push", "pull"} for args in calls)


@pytest.mark.parametrize("invalid", [True, False])
def test_push_requires_valid_exports_and_stages_only_owned_outputs(tmp_path, monkeypatch, invalid):
    repo, external = tmp_path / "repo", tmp_path / "external"
    repo.mkdir()
    monkeypatch.setattr(finish, "ROOT", repo)
    calls = []

    def git(*args):
        calls.append(args)
        return {"branch": "main", "rev-parse": "committed"}.get(args[0], "")

    def build(root, destination):
        destination.mkdir(parents=True)
        (destination / "REPORT.md").write_text("All planned slots retained.")

    def validate(*args):
        if invalid:
            raise ValueError("Changed prediction evaluation")

    monkeypatch.setattr(finish, "git", git)
    monkeypatch.setattr(finish, "build", build)
    monkeypatch.setattr(finish, "analyze", lambda *args: {"counts": {"terminal_sources": 48}})
    monkeypatch.setattr(finish, "plot", lambda *args: None)
    monkeypatch.setattr(finish, "review", lambda *args: None)
    monkeypatch.setattr(finish, "validate_exports", validate)
    monkeypatch.setattr(finish, "update_tracking", lambda *args: None)
    if invalid:
        with pytest.raises(ValueError, match="prediction evaluation"):
            finish.finish(tmp_path, external, tmp_path / "status.json")
        assert not any(args[0] in {"add", "commit", "push"} for args in calls)
    else:
        result = finish.finish(tmp_path, external, tmp_path / "status.json")
        assert result["phase"] == "completed_and_pushed"
        assert (external / "REPORT.md").read_bytes() == (
            repo / finish.REPORT_REL / "REPORT.md"
        ).read_bytes()
        assert "REVIEW.md" in (external / "REPORT.md").read_text()
        add = next(args for args in calls if args[0] == "add")
        assert set(add[2:]) == {
            finish.REPORT_REL,
            finish.NOTE_REL,
            finish.TODO_REL,
            finish.FIRST_REL,
        }
        commit = next(args for args in calls if args[0] == "commit")
        assert "--only" in commit
        assert calls.index(commit) < calls.index(("push", "origin", "main"))


def test_incomplete_denominator_cannot_be_published(tmp_path):
    finish.write(tmp_path / "design.json", {"schedule": [{"repeat": "r1", "id": "one"}]})
    with pytest.raises(ValueError, match="48 planned slots"):
        finish.validate_exports(
            tmp_path, tmp_path / "reports", {"cases": [], "counts": {"terminal_sources": 0}}
        )


def test_git_commit_only_excludes_unrelated_staged_work(tmp_path, monkeypatch):
    monkeypatch.setattr(finish, "ROOT", tmp_path)
    finish.git("init")
    finish.git("config", "user.email", "test@example.invalid")
    finish.git("config", "user.name", "Test")
    (tmp_path / "unrelated.txt").write_text("original")
    finish.git("add", "unrelated.txt")
    finish.git("commit", "-m", "initial")
    (tmp_path / "unrelated.txt").write_text("user staged work")
    (tmp_path / "report.md").write_text("new scientific report")
    finish.git("add", "unrelated.txt", "report.md")
    finish.git("commit", "--only", "-m", "results", "--", "report.md")
    assert finish.git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD") == "report.md"
    assert finish.git("diff", "--cached", "--name-only") == "unrelated.txt"
