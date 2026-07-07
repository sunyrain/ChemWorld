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

| Task | Split | Budget | Operation Slice | Main Metrics |
| --- | --- | --- | --- | --- |
| `reaction-optimization-standard` | `public-test` | 72 | reaction | score, yield, selectivity, sample efficiency |
| `reaction-safety-constrained` | `public-test` | 72 | reaction | score, safety risk, constraint violations |
| `reaction-mechanism-explanation` | `public-test` | 36 | reaction | score, mechanism explanation, failure analysis |
| `reaction-to-assay` | `public-dev` | 18 | reaction | final-assay score, trajectory validity |
| `reaction-to-purification` | `public-test` | 90 | reaction + separation | score, purity, recovery, mass balance |
| `partition-discovery` | `public-test` | 48 | phase/partition | phase ratio, product partition |
| `purity-yield-tradeoff` | `public-test` | 90 | reaction + separation | yield, purity, recovery, cost |
| `public-private-generalization` | `private-eval` | 72 | reaction | score, public/private gap |
| `low-budget-characterization` | `public-test` | 18 | reaction | sample efficiency, uncertainty, local model quality |
| `tool-agent-planning` | `public-dev` | 48 | reaction + separation | trajectory validity, validator use, score |

Task-based evaluation is preferred for public results because it removes
ambiguity about budget, split, objective, and seed selection.

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
