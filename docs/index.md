# ChemWorld-Bench

ChemWorld-Bench is an open benchmark for closed-loop virtual chemical
experimentation. It provides hidden semi-mechanistic worlds, standard action
and observation protocols, official baselines, trajectory logs, and leaderboard
metrics.

The official environment is `ChemWorld`, a finite-budget event-driven
physical-chemical world with reaction, phase partition, downstream separation,
cost, safety, and noisy instrument observations. It uses a reusable Chemical
World Model foundation: ontology, executable physical constitution, state
ledger, transition kernels, and instrument observation kernels.

Start with:

- [Current Progress](current_progress.md) for the implementation status.
- [Architecture](architecture.md) for the core package design.
- [Architecture Report](architecture_report.md) for the SOTA Gym benchmark
  comparison and missing-piece roadmap.
- [World Law](world_law.md) and [Task Taxonomy](task_taxonomy.md) for the
  unified-world design.
- [Benchmark Protocol](benchmark_protocol.md) for evaluation and submission
  rules.
- [Tasks](tasks.md), [Operations](operations.md), [Wrappers](wrappers.md), and
  [Submission Bundles](submission.md) for the research-release benchmark
  contract.

