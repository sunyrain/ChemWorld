# Benchmark Tasks

ChemWorld tasks are stable benchmark contracts over one shared
physical-chemical world. A task does not define a separate game. It selects a
scenario, initial state, allowed operations, observation policy, budget, seeds,
objective, and success metrics inside the same `ChemWorld` environment and the
same `chemworld-physical-chemistry` world law.

List tasks:

```bash
chemworld tasks list
```

Inspect one task:

```bash
chemworld tasks show reaction-optimization-standard
```

Run a task:

```bash
chemworld run --task reaction-optimization-standard --agent scripted_chemistry
```

Run the task suite:

```bash
chemworld suite --task reaction-optimization-standard --agent gp_bo
```

## Built-In Tasks

| Task | Split | Mode | Budget | Operation Slice | Main Metrics |
| --- | --- | --- | --- | --- | --- |
| `reaction-optimization-standard` | `public-test` | campaign | 72 | reaction | score, yield, selectivity, sample efficiency |
| `reaction-safety-constrained` | `public-test` | campaign | 72 | reaction | score, safety risk, constraint violations |
| `reaction-mechanism-explanation` | `public-test` | campaign | 36 | reaction | score, mechanism explanation, failure analysis |
| `reaction-to-assay` | `public-dev` | single experiment | 18 | reaction | final-assay score, trajectory validity |
| `reaction-to-purification` | `public-test` | single experiment | 90 | reaction + separation | score, purity, recovery, mass balance |
| `reaction-to-crystallization` | `public-test` | single experiment | 72 | reaction + crystallization | score, crystal yield, crystal purity, crystal size |
| `reaction-to-distillation` | `public-test` | single experiment | 72 | reaction + distillation | score, distillate purity, distillate recovery, solvent loss |
| `flow-reaction-optimization` | `public-test` | campaign | 60 | reaction + continuous flow | score, flow conversion, yield, safety risk |
| `electrochemical-conversion` | `public-test` | campaign | 48 | reaction + electrochemistry | score, selectivity, energy efficiency, safety risk |
| `partition-discovery` | `public-test` | campaign | 48 | phase/partition | phase ratio, product partition |
| `purity-yield-tradeoff` | `public-test` | campaign | 90 | reaction + separation | yield, purity, recovery, cost |
| `public-private-generalization` | `private-eval` | campaign | 72 | reaction | score, public/private gap |
| `low-budget-characterization` | `public-test` | campaign | 18 | reaction | sample efficiency, uncertainty, local model quality |
| `tool-agent-planning` | `public-dev` | single experiment | 48 | reaction + separation | trajectory validity, validator use, score |

Task-based evaluation is preferred for public results because it removes
ambiguity about budget, split, objective, and seed selection.

## Physics Maturity

Each task card now exposes machine-readable physics maturity metadata:

- `kernel_maturity`: module-level maturity records such as reaction kinetics,
  reactors, separations, phase equilibrium, distillation, electrochemistry, and
  instruments.
- `physics_maturity`: the lowest maturity level among the modules used by the
  task.
- `proxy_allowed`: whether the task explicitly permits proxy kernels.

The allowed maturity levels are `proxy`, `lite`, `reference_validated`,
`professional_candidate`, and `professional`. If a task uses a proxy kernel,
it must be tagged as teaching, smoke, exploratory, or education. This prevents
professional benchmark claims from silently relying on proxy unit operations.

## Episode Modes

`single_experiment` tasks are one experimental workflow. A successful
`final_assay` terminates the episode.

`campaign` tasks are finite-budget experimental campaigns. A successful
`final_assay` scores and closes the current experiment, then the reactor state
is reset for the next independent experiment. The episode ends only when the
campaign budget is exhausted. Optimizer baselines such as LHS, greedy search,
GP-BO, RF-EI, and safe BO should be evaluated on campaign tasks.

## World, Scenario, Task

- `WorldLaw` is the shared ontology, constitution, operation registry,
  transition kernels, and observation kernels.
- `Scenario` is a hidden initial-condition and parameter family inside that
  world law, such as reaction optimization or partition discovery.
- `Task` is the public benchmark contract: scenario, split, budget, allowed
  operations, instruments, seeds, and scoring targets.

This design keeps task diversity from becoming a collection of disconnected
toy environments. Agents that learn reaction kinetics, safety constraints,
instrument noise, or phase behavior are learning reusable structure inside one
world.
