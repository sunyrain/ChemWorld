# Work II Study B matched-evidence experiment note

## Question

When evidence seeking is removed, can a fresh DeepSeek participant revise an aligned, opaque, or
misindexed initial world model after reading the same evaluator-owned contradictory evidence?  The
study localizes the remaining failure to evidence acquisition versus belief updating; it is not a
new autonomous-search benchmark.

## Units and frozen coverage

- Participant: `deepseek-v4-flash`, high reasoning, native Codex `exec` session.
- Loci/tasks: A-P `electrochemical-conversion` and A-S `partition-discovery`.
- Worlds: the five already registered public C2 seeds for each selected task.
- Arms: `opaque`, `aligned_nominal`, and `misindexed_nominal` in every task-world cluster.
- Total: 10 task-world clusters and 30 fresh two-turn sessions.  There are no participant physical
  experiments and no participant access to the simulator or evaluator truth.
- The first turn receives the task, initial world model, and scoring queries, then commits a
  pre-evidence prediction.  The second turn in the same Codex thread receives the fixed evidence
  packet and commits a post-evidence prediction for the same scoring queries.
- A-P uses registered query indices 1-8 as evidence and 0,9-15 for scoring.  A-S uses the eight
  identity queries as evidence and the eight phase-process queries for scoring.  Evidence and
  scoring queries are disjoint.  Within a task-world cluster the evidence packet and scoring-query
  order are byte-identical across arms.

## Measurements

- Pre- and post-evidence mean normalized absolute error over every registered scoring
  query-metric term; all metrics have the registered unit scale of 1.
- Per-cell update gain: `pre_error - post_error`.
- Primary per-locus contrast: misindexed update gain minus aligned update gain.  Opaque is a
  descriptive reference.  Results are reported by world and as the five-world locus mean with all
  failures retained.
- Schema completeness, exact query/metric denominators, same-thread continuity, evidence identity,
  provider usage, elapsed time, and provider/infrastructure failures.

## Qualification and stopping rules

- A provider-free preflight must verify the 10 truth reports, the 8/8 disjoint query split, and the
  exact 30-cell schedule before any provider call.
- A three-arm canary checks only two-turn continuity, output schema, exact denominators, and packet
  identity.  Canary numerical outcomes do not authorize a design change and are excluded from the
  30-cell analysis.
- The scientific block is complete only when all 30 scheduled cells are terminal.  Infrastructure
  retries retain their attempt receipts; scientific/schema failures are retained and are not
  outcome-replaced.  Any execution-semantics fix after the formal block begins requires restarting
  all 30 cells from the first unit.
- No directional scientific result is a platform pass/fail gate.  A positive primary contrast
  supports an evidence-seeking bottleneck; little or no misindexed updating despite matched
  evidence supports a belief-updating bottleneck.  Mixed loci are reported as mechanism
  heterogeneity rather than pooled away.

## Expected outputs

- One input manifest with the exact schedule and per-world evidence/scoring packets.
- One sanitized cell result and provider receipt per session, plus append-only progress.
- One machine-readable summary with exact denominators, all failures, per-world scores, locus
  contrasts, and a Chinese interpretation report.  Raw provider events and credentials remain
  outside Git.
