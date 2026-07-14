# PPO pre-v0.4.8 diagnostic archive

This package preserves only the two previously selected PPO checkpoints and their
Dev replay/resource records. They were generated before the public per-experiment
core-progress observation and reward-contract v0.3 migration.

The files are historical diagnostics only. Current runtime loading, resuming,
formal checkpoint indexing, method-readiness claims, and Bench claims are all
forbidden. The immutable historical report remains at
`workstreams/benchmark_v1/reports/rl-ppo-dev-v0.4.json`; `archive-manifest.json`
records why its selected weights were superseded.
