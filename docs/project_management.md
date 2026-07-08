# Two-Person Development Rules

ChemWorld is a fast two-person research codebase. We keep coordination simple:
the shared truth is `TODO.md`, every active task has one owner, and every
completed unit is pushed immediately.

## Shared Source Of Truth

- `TODO.md` is the only active work board.
- Every active task must name exactly one `Owner`.
- A task without an owner is available.
- A task marked `Active` by the other person must not be started unless the
  owner writes a handoff note.
- Reference repositories in `reference_repos/` are read-only references and are
  not committed.

## Start Work Protocol

Before starting any task:

```powershell
git checkout main
git pull --rebase origin main
```

Then edit `TODO.md`:

- set the task `Status` to `Active`;
- write the real `Owner`;
- write the intended file area;
- write the next concrete step.

Commit and push that ownership update before coding:

```powershell
git add TODO.md
git commit -m "Claim task: <short task name>"
git push origin main
```

This prevents both people from doing the same work.

## During Work

- Pull immediately if the remote `TODO.md` changes.
- If local edits are unfinished, commit a small WIP note or stash before pulling.
- If the pull shows the other person claimed the same area first, stop and
  coordinate through `TODO.md`.
- Keep commits small enough that the other person can understand the diff.
- Do not mix notebooks, core code, generated runs, and docs in one unrelated
  commit.

## Finish Work Protocol

After finishing any task, immediately update `TODO.md`:

- set `Status` to `Done`, `Review`, or `Blocked`;
- record the commit hash if useful;
- write the next step or handoff note;
- clear or change `Owner` only when the handoff is explicit.

Then push the result:

```powershell
git add <changed files> TODO.md
git commit -m "<short completed task>"
git push origin main
```

Do not wait to batch several completed tasks into one push. The current rule is:
finish one useful unit, update `TODO.md`, push it.

## Status Values

Use only these statuses:

| Status | Meaning |
| --- | --- |
| `Planned` | Not started and available. |
| `Active` | One owner is working on it now. |
| `Blocked` | Owner cannot proceed; handoff note is required. |
| `Review` | Work is pushed and needs the other person to inspect. |
| `Done` | Work is complete and pushed. |

## Handoff Note

Use this short format in `TODO.md` when stopping or handing off:

```text
Owner: <name>
Status: Blocked / Review / Done
Changed:
- ...
Next:
- ...
Checks:
- ...
Risks:
- ...
```

## Checks

Run targeted checks for small edits. Run the full local suite before a meaningful
core change:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

GitHub Actions are currently manual-only because account billing blocks
automatic runs. Trigger CI manually only when needed:

```text
Actions -> CI -> Run workflow
```

## Do Not

- Do not commit `reference_repos/`.
- Do not copy external library source into ChemWorld.
- Do not work on another person's `Active` task without a handoff.
- Do not leave completed work unpushed.
- Do not use `git add -A` when unrelated notebook or generated files are dirty.
