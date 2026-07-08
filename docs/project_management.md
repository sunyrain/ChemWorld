# Two-Person Workflow

ChemWorld is currently a fast two-person research prototype. We do not need a
heavy project-management system. The goal is simply to know who owns what, what
is active, and what is ready to review.

## Simple Rules

- `TODO.md` is the shared roadmap.
- Each active item has exactly one owner.
- The owner writes code, runs checks, and leaves a short handoff note.
- The other person reviews only the diff, tests, and model assumptions.
- Reference repositories in `reference_repos/` are for reading only and are not
  committed.
- Pushes should not auto-run GitHub Actions while billing is blocked; CI is
  manual-only.

## Lightweight Owner Table

Keep a tiny table in `TODO.md` or in a local note:

| Item | Owner | Status | Next Step | Files |
| --- | --- | --- | --- | --- |
| Generic reaction network | Person A | Active | build `ReactionNetworkSpec` | `src/chemworld/physchem/` |
| Property correlations | Person B | Waiting | define component schema | `src/chemworld/physchem/properties/` |

Statuses:

- `Planned`
- `Active`
- `Blocked`
- `Review`
- `Done`

That is enough.

## Branches

Use one working branch per larger topic:

```text
agent/unified-world-hardening
physchem/reaction-network
physchem/property-core
physchem/phase-equilibrium
notebooks/tutorial-polish
```

For tiny edits, working directly on the current feature branch is fine.

## Handoff Note

When one person stops working, leave a short note:

```text
Owner: Person A
Item: Generic reaction network
Changed:
- Added SpeciesSpec and ReactionSpec.
- Added parser tests for irreversible reactions.
Next:
- Add reversible reaction support.
- Connect to batch reactor backend.
Checks:
- ruff passed
- pytest tests/test_physchem_reaction_network.py passed
Risks:
- Formula parser does not handle parentheses yet.
```

## Review Rule

For two-person fast iteration, review only these questions:

1. Does it run?
2. Does it preserve physical constraints?
3. Does it keep public API simple?
4. Does it avoid copying third-party code?
5. Is the next step obvious?

## Local Checks

Run the full set before a meaningful push:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy src\chemworld
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m mkdocs build --strict
```

For quick inner-loop work, run only the targeted tests.

## GitHub Actions

The workflow is manual-only:

```text
Actions -> CI -> Run workflow
```

This avoids automatic billing-triggered startup failures on every push. If the
account billing issue is fixed later, we can re-enable push or pull-request CI.

## What Not To Do

- Do not create many labels, milestones, or formal issue templates yet.
- Do not open huge PRs that mix notebooks, core models, and docs.
- Do not commit `reference_repos/`.
- Do not copy external library source into ChemWorld.
- Do not push generated runs/results unless they are intentional examples.
