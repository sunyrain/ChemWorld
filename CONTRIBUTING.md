# Contributing to ChemWorld

Thank you for helping improve ChemWorld. The repository combines an installable environment,
research protocols, generated evidence, documentation, and publication sources. A change can be
technically correct while still invalidating a replay or a scientific evidence binding, so please
keep the boundaries below explicit.

## Before starting

Read [DEVELOPMENT.md](DEVELOPMENT.md) and the instructions in [AGENTS.md](AGENTS.md). For work that
touches a current research programme, also read its active entry point:

- Work I: `workstreams/arxiv_v1/FIRST_PAPER_TODOLIST.md`
- Work II: `workstreams/flagship_tasks/WORK_II_TODOLIST.md`
- repository cleanup: `workstreams/repository_quality/CLEANUP_CLOSEOUT_TODOLIST.md`

Resolve active artifacts through `configs/current.json`. Do not infer the current artifact from a
version suffix, modification time, or the largest release-candidate number. Historical reports and
claim files do not authorize new work.

Before editing, inspect `git status --short --branch`. The worktree may contain another contributor's
changes. Preserve unrelated edits and agree on a non-overlapping write set when concurrent work is
unavoidable.

## Development environment

ChemWorld supports Python 3.11 and 3.12 and uses the committed `uv.lock` as its reproducible
dependency surface.

For a fresh development checkout, install the locked development environment once:

```bash
uv sync --extra dev
```

After setup, run repository commands without changing the environment:

```bash
uv run --no-sync chemworld --help
uv run --no-sync pytest -q tests/test_env.py
uv run --no-sync ruff check path/to/changed_file.py
uv run --no-sync mypy path/to/changed_module.py
```

Do not use the system Python or its installed packages as evidence about this repository. Optional
features use their declared extras, such as `rl`, `docs`, `notebooks`, `paper`, or `physchem-ref`.

## Choose the right change boundary

- `src/chemworld/` contains the installable environment, interfaces, and evaluation runtime.
- `configs/` contains active contracts and templates. Changing one may invalidate bound evidence.
- `scripts/` contains current maintenance and experiment entry points; keep wrappers thin when
  reusable behavior belongs in a tested module.
- `tests/` should cover the contract changed by the implementation, including fail-closed cases.
- `workstreams/` contains current compact evidence and coordination records, not raw runs.
- `paper/` contains manuscript sources, figures, and explicitly retained release deliverables.
- `runs/`, caches, local credentials, raw provider responses, and generated site output stay local.

Separate implementation, generated results, and manuscript integration when practical. Never edit a
generated score, receipt, hash, or report to make a gate pass.

## Scientific and evidence changes

Development mode is the default. Focused implementation and scientific-validity work does not
require rebuilding repository-wide readiness or release certificates after every edit.

Before a new data-producing experiment, add one concise experiment note stating:

- the question;
- tested units or coverage design;
- measurements and denominators;
- pass, failure, and stop rules;
- expected outputs.

Once the block starts, do not change those rules in response to its outcomes. Preserve all failures,
exact replay, and resource accounting. If a platform defect is fixed, rerun the affected
qualification block from its first unit. Development evidence remains labelled development-only.

Release freeze is a separate, explicitly authorized stage. It binds a clean committed execution
surface and rebuilds the minimum required release evidence once. Environment validation must not be
presented as Agent performance, a benchmark ranking, real-chemistry validation, or transfer evidence.

## Validation

Run the smallest meaningful checks while developing, then broaden them in proportion to risk. A
typical code change should include:

```bash
uv run --no-sync ruff check <changed Python files>
uv run --no-sync pytest -q <focused tests>
uv run --no-sync mypy <changed Python modules>
git diff --check
```

Use `uv run --no-sync mypy src/chemworld` once for a cross-package refactor or the integrated
acceptance pass. It is not a prerequisite for every isolated development edit.

Also run wheel smoke when packaging or resource lookup changes:

```bash
uv run --no-sync pytest -q tests/test_wheel_smoke.py
```

Commands expected to exceed 60 seconds must expose progress at least once per minute, including the
current stage, completed/total units, throughput, and ETA when known. Keep wrapper logs and probes
outside the repository.

## Credentials, private data, and generated output

Never commit:

- `.env`, `api.md`, `key2.md`, private seeds, access tokens, or service credentials;
- `runs/`, raw provider payloads, request/response dumps, or private evaluation data;
- caches, generated documentation sites, or local virtual environments;
- private chain-of-thought or other sensitive model internals.

Provider integrations must read credentials from the local process environment. Reports may retain
structured decisions, usage, cost, retry, and failure metadata only when the governing protocol
allows it.

For security-sensitive findings, follow [SECURITY.md](SECURITY.md) instead of opening a public issue
with exploit or credential details.

## Change checklist

Before handing off a change, confirm that:

- the change has one clear purpose and preserves unrelated work;
- active paths came from the current registry or governing TODO;
- focused positive and fail-closed tests pass;
- Ruff, relevant typing checks, and `git diff --check` pass;
- no credential, raw run, private payload, or accidental generated file is tracked;
- stale evidence remains visibly stale until an authorized rebuild;
- documentation and generated publication artifacts are synchronized when the governing workflow
  requires them;
- the handoff states what changed, what was actually tested, and what remains pending.
