# Work II prior discovery — mock preflight

Status: **PASSED**

Scope: contract and execution-state qualification only; no scientific or benchmark claim.

The clean-commit mock preflight completed all **15/15 cells with 0 failures** across five tasks,
three prior arms and world seed 0. Every cell followed the frozen five-experiment trajectory:
one neutral-prefix experiment, two discriminating-prefix experiments and two autonomous-suffix
decisions. Each cell then executed four held-out queries with two replicates per query and three
blind recommendation replicates.

The runner recorded four ordered typed snapshots (pre_evidence, post_neutral,
post_discriminating, final) and validated an executable law summary at each snapshot. The
mock provider-style accounting was **90 direct calls / 90 attempts / 0 retries**, with **21,000
input tokens, 18,000 output tokens and 39,000 total tokens**. All trajectory, held-out and blind
validation denominators matched the discovery plan.

This result qualifies the state machine, schema validation, public/private query binding, blind
bookkeeping and resource denominators. It does not estimate prior benefit or harm and does not
authorize scientific interpretation. The next gate is the three-arm real WellAU discovery probe
for electrochemical conversion; only after that passes may the one-seed breadth stage run.
