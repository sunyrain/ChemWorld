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
  - src/chemworld/providers/deepseek.py
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
  - "DeepSeek and WellAU share an exact medium/high/max stored attribute type without broad casts"
  - "DeepSeek constructor acceptance remains high/max and WellAU acceptance remains medium/high"
  - "Both Codex subprocess launchers obtain CREATE_NO_WINDOW safely at runtime"
  - "Windows RL worker accounting obtains ctypes.windll safely and fails clearly if unavailable"
files_touched:
  - src/chemworld/providers/deepseek.py
  - src/chemworld/providers/wellau.py
  - src/chemworld/providers/codex_subscription.py
  - src/chemworld/agents/interactive_codex_experiment.py
  - src/chemworld/rl/training.py
final_commit: "026937359ca2c7c7a615c495f91240c1107a4a6d"
reviewer: "coordinator"
review_result: >-
  Requested shared reasoning-effort storage correction applied; pending coordinator re-review.
notes: >-
  Coordinator-authorized write-set expansion adds src/chemworld/providers/deepseek.py for the shared
  reasoning-effort storage contract. PASS: uv run --cache-dir /tmp/chemworld-aq02-uv-cache --frozen
  --extra dev mypy
  src/chemworld/providers/deepseek.py src/chemworld/providers/wellau.py
  src/chemworld/providers/codex_subscription.py src/chemworld/agents/interactive_codex_experiment.py
  src/chemworld/rl/training.py (no issues in 5 files); PASS: same uv prefix with ruff check on all 5
  source files; PASS: uv run --cache-dir /tmp/chemworld-aq02-uv-cache --frozen --extra dev --extra
  rl pytest -q tests/test_deepseek_v4_provider.py tests/test_wellau_provider.py
  tests/test_codex_subscription_provider.py tests/test_interactive_codex_experiment.py
  tests/test_rl_training_accounting.py (30 passed); PASS: git diff --check.
```

The worker commits this claim before implementation, edits only its own claim, and changes the status
to `REVIEW` after task-local validation. Only the coordinator marks a claim `DONE` after integration.
