# Work II A-S Study B4 law-guided decision assay

Status: frozen before fresh-world truth or participant execution; independent successor to the
retained B3 public-preflight rejection.

## Question

After participant-visible evidence makes the partition power law identifiable, can an agent use the
recovered law to rank and select relatively high-utility unseen actions, and can it correctly retain
the visible incumbent when no candidate clears the registered improvement margin?

## Units and frozen coverage

- Participant: `deepseek-v4-flash`, high reasoning, native Codex `exec`, no tools or files.
- Five fresh public A-S partition worlds with seeds frozen in the protocol before truth execution;
  arms `opaque`, `aligned_nominal`, and `misindexed_nominal`; 15 fresh two-turn sessions.
- The eight-row structural evidence roster is inherited unchanged from the development-only B3
  freeze: four distinct nominal pairs, paired linear-reference calibration and target-world
  observations. B3 public worlds and outcomes do not select B4 evidence or seeds.
- The action pool is the remaining 120 typed candidate recipes from the frozen 128-query grid. For
  each fresh world, evaluator truth ranks the pool by score with query ID as the tie-breaker. A
  deterministic item generator selects positions `1, 18, 35, 52, 69, 86, 103, 120`, preferring an
  unused nominal pair at the nearest rank when possible. Candidate ranks and truth are hidden.
- The participant chooses one unseen candidate query ID or `RETAIN_INCUMBENT`; it does not generate
  a free-text recipe. Evidence and action recipes are disjoint.

## Measurements

- Pre/post normalized absolute prediction error on all eight unseen action candidates.
- Anonymous mechanism family, exponent, typed-law consistency, confidence, and exact 1.75 recovery.
- Candidate Top-1 accuracy, selected rank and percentile, raw regret, normalized regret, and utility
  relative to random candidate choice.
- Policy regret when `RETAIN_INCUMBENT` is included as an admissible decision.
- Correct abstention when the best candidate does not exceed the evidence incumbent by `0.02`, false
  abstention when a qualifying opportunity exists, and false execution when it does not.
- Candidate gain over incumbent remains secondary and is never a precondition for evaluating rank or
  regret.

## Qualification and stop rules

- Development qualification remains the completed B3 result: 5/5 exponent recovery within `0.10`,
  power uniquely best against registered alternatives, and four participant-visible reference
  coefficients. The retained B3 public action failure is not reused as B4 participant evidence.
- Before participant calls, all fresh-world linear evidence and target candidate/evidence truth must
  execute and replay exactly with complete denominators. Each generated action set must contain eight
  unique unseen recipes, at least four nominal pairs, and the registered rank positions.
- No minimum gain over incumbent is required. Opportunity status is a measured world property that
  determines whether execution or abstention is the oracle policy.
- Canary uses one fresh world across three arms and checks schema, thread continuity, packet identity,
  typed law, candidate selection/abstention, and denominators only. Canary outcomes are excluded.
- After the first formal cell, any execution-semantics, candidate-generator, schema, threshold, or
  metric change requires restarting all 15 formal sessions. All failures are retained.

## Expected outputs

- Frozen protocol, fresh-world truth manifest, hidden-rank action rosters, 15 sanitized cell results,
  exact provider receipts, machine summary, Chinese report, and Paper 2 claim updates.

