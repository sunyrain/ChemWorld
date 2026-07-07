# Roadmap

ChemWorld-Bench now prioritizes benchmark hardening before adding more
physical modules under the shared `ChemWorld` law.

## P0: Benchmark Contract

- Maintain the task registry and task cards.
- Keep wrappers optional and Gymnasium-compatible.
- Validate submission bundles locally.
- Preserve deterministic replay verification.
- Keep docs buildable with `mkdocs build --strict`.

## P1: Release Infrastructure

- Publish official baseline results for built-in tasks.
- Add dataset cards and JSONL-to-columnar exports.
- Add signed private-eval result artifacts.
- Calibrate task difficulty and thresholds.
- Expand safety-cost reporting.

## P2: Research Breadth

- Add the next physical module under `ChemWorld`, not a standalone world.
- Add RL library adapters for standard baselines.
- Add offline world-model and imitation baselines.
- Add richer mechanism explanation examples and rubrics.

## P3: Scale And Interaction

- Add vectorized batch execution.
- Explore accelerated kernels only if CPU ODE becomes a bottleneck.
- Consider PettingZoo-style human/LLM/team environments.
- Add a hosted leaderboard only after the local benchmark contract is stable.

