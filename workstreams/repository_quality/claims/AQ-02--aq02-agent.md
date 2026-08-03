# Repository quality task claim

```yaml
task_id: AQ-02
title: "Type-safe provider and cross-platform process guards"
status: REVIEW
owner: "aq02-agent"
claimed_at_utc: 2026-08-03T14:14:23Z
base_commit: "05e6324352eedea0dcf291ef0410c86cd3da983e"
branch: agent/aq02-platform-typing
worktree: "/home/chenhh/python_projects/chemworld/ChemWorld-AQ02"
declared_write_set:
  - workstreams/repository_quality/claims/AQ-02--aq02-agent.md
  - src/chemworld/providers/wellau.py
  - src/chemworld/providers/codex_subscription.py
  - src/chemworld/agents/interactive_codex_experiment.py
  - src/chemworld/rl/training.py
deliverables:
  - "Narrow WellAU request parameters to their declared Literal types"
  - "Guard Windows-only subprocess and ctypes attributes without changing cross-platform runtime semantics"
validation:
  - "Mypy on all touched source files"
  - "Ruff on all touched source files"
  - "Relevant existing provider, interactive Codex, and RL training tests"
  - "git diff --check"
completed:
  - "WellAU preserves its medium/high public and wire contract through a localized inherited-type boundary"
  - "Both Codex subprocess launchers obtain CREATE_NO_WINDOW safely at runtime"
  - "Windows RL worker accounting obtains ctypes.windll safely and fails clearly if unavailable"
files_touched:
  - src/chemworld/providers/wellau.py
  - src/chemworld/providers/codex_subscription.py
  - src/chemworld/agents/interactive_codex_experiment.py
  - src/chemworld/rl/training.py
final_commit: "d424d2fd844307eba5b1cf938a14754eb0c936b3"
reviewer: null
review_result: null
notes: >-
  PASS: uv run --cache-dir /tmp/chemworld-aq02-uv-cache --frozen --extra dev mypy
  src/chemworld/providers/wellau.py src/chemworld/providers/codex_subscription.py
  src/chemworld/agents/interactive_codex_experiment.py src/chemworld/rl/training.py (no issues in
  4 files); PASS: same uv prefix with ruff check on the four source files; PASS: same dev prefix with
  pytest -q tests/test_wellau_provider.py tests/test_codex_subscription_provider.py
  tests/test_interactive_codex_experiment.py (21 passed); PASS: uv run --no-cache --frozen --extra
  dev --extra rl pytest -q tests/test_rl_training_accounting.py (4 passed); PASS: git diff --check.
```

The worker commits this claim before implementation, edits only its own claim, and changes the status
to `REVIEW` after task-local validation. Only the coordinator marks a claim `DONE` after integration.
