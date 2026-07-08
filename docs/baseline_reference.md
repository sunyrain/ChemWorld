# Baseline Reference

Official baselines should be reported per task rather than merged into one
global table.

| Task Family | Reference Baselines |
| --- | --- |
| Reaction optimization | random, LHS, scripted chemistry, GP BO, RF EI, safe GP BO |
| Safety constrained | random, scripted chemistry, safe GP BO |
| Reaction to purification | random event planner, scripted chemistry |
| Reaction to crystallization | random event planner, scripted chemistry |
| Reaction to distillation | random event planner, scripted chemistry |
| Continuous-flow reaction | random event planner, scripted chemistry |
| Electrochemical conversion | random event planner, scripted chemistry |
| Partition discovery | random, scripted chemistry, LLM replay |
| Low budget characterization | random, LHS, GP BO |
| Tool-agent planning | LLM replay, tool-using LLM stub |

LLM entries are reproducibility adapters, not claims that ChemWorld already has
a validated autonomous chemical agent. Online LLM results must report model
name, date, prompt, temperature, cost, cache policy, and replay artifact.

The default BO baselines now use `n_initial=4`. The primary reaction task uses
`budget=72`, which gives recipe-based BO enough final-assay observations to
enter acquisition instead of spending the whole episode on initialization.

Reference tables should include mean, standard error, safety violations,
public/private gap when available, and the exact platform version and command.

Generate a task-based baseline report with:

```bash
chemworld baselines report \
  --tasks reaction-optimization-standard reaction-to-crystallization \
  --agents random scripted_chemistry gp_bo safe_gp_bo \
  --seeds 0 1 2 \
  --output-dir runs/baseline_report
```

The command writes:

- `baseline_results.json`: run-level metrics;
- `baseline_leaderboard.json`: task-specific leaderboard rows;
- `baseline_report.json`: metadata, platform version, commit hash, tasks,
  agents, seeds, task maturity metadata, maturity summary, and leaderboard
  rows.

Rows are grouped per task. Do not merge reaction, purification, crystallization,
distillation, flow, and electrochemistry tasks into one global table.

Every trajectory and baseline result now carries:

- `kernel_maturity`;
- `physics_maturity`;
- `proxy_allowed`.

Report generation validates that all results for the same task use the same
maturity metadata and raises an error if a task silently mixes proxy,
lite/reference-validated, or professional kernels. Multi-task reports may still
contain different maturity levels, but `maturity_summary` and leaderboard rows
make those levels explicit.

The task registry also exposes `task_maturity_manifest()` for tooling that
needs the maturity view without running baselines. Reference-validation reports
now include backend availability, optional package versions when discoverable,
local reference-repository paths and short commits when checkouts are present,
and declared tolerance profiles for common comparison families.
