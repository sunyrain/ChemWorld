# Roadmap

ChemWorld-Bench now prioritizes benchmark hardening and documentation
convergence before adding more physical modules.

## P0: Current Pre-Release Closure

Goal: make the current unified-world benchmark externally understandable and
locally reproducible.

- Keep the formal entry point as `gym.make("ChemWorld", task_id=...)`.
- Keep documentation structured around world law, task registry, runtime
  contracts, evaluation, and audits.
- Run environment self-consistency audit as a release gate.
- Freeze task cards for the pre-release task set.
- Remove stale docs language that implies old environment generations or
  unrelated mini-games.

## P1: Benchmark Contract Hardening

Goal: make public benchmark numbers credible.

- Generate official baseline reports for release tasks.
- Record baseline commands, seeds, platform version, commit hash, dependency
  file, and maturity metadata.
- Narrow broad task profiles so each release task exposes only relevant
  operations.
- Keep replay verification deterministic across task/scenario/mechanism hash
  boundaries.
- Sign maintainer private-eval artifacts when reporting hidden results.

## P2: Dataset And Agent Research Layer

Goal: make ChemWorld useful for agent and world-model research.

- Export JSONL and columnar datasets with dataset cards.
- Add offline world-model, imitation, and RL baseline adapters.
- Add richer explanation rubrics and example explanations.
- Compare random, BO, safe BO, scripted, LLM replay, and human-plus-LLM
  strategies across public/private splits.

## P3: Professional Physics Deepening

Goal: improve model fidelity without turning tasks into separate games.

- Replace proxy modules one slice at a time with reference-validated or
  professional-candidate kernels.
- Deepen separations, crystallization, distillation, continuous flow, and
  electrochemistry under the same world law.
- Add external backend adapters only after the local benchmark contract is
  stable.
- Preserve maturity metadata so physical fidelity changes remain auditable.

## P4: Hosted Evaluation

Goal: move from local benchmark protocol to managed evaluation when needed.

- Add hosted hidden task registry and server-side private seeds.
- Add reviewed submission ingestion.
- Add web leaderboard only after local submission bundles, verifier, and
  signed artifacts are stable.
