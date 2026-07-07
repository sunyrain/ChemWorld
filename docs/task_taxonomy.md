# Task Taxonomy

ChemWorld separates world law, scenario, and task.

| Layer | Meaning | Example |
| --- | --- | --- |
| World law | Shared physical-chemical rules | `chemworld-physical-chemistry` |
| Scenario | Hidden parameter and initial-condition family | reaction optimization, partition discovery |
| Task | Public benchmark contract | `reaction-to-purification` |

## Current Task Families

Reaction tasks exercise the ODE reaction module and instrument observation:

- `reaction-optimization-standard`
- `reaction-safety-constrained`
- `reaction-mechanism-explanation`
- `reaction-to-assay`
- `low-budget-characterization`
- `public-private-generalization`

Reaction + separation tasks exercise reaction planning plus downstream
processing:

- `reaction-to-purification`
- `purity-yield-tradeoff`
- `tool-agent-planning`

Year 2 process tasks extend the same world law with additional physical
modules:

- `reaction-to-crystallization`
- `reaction-to-distillation`
- `flow-reaction-optimization`
- `electrochemical-conversion`

Partition tasks isolate phase behavior so agents can learn solvent/product
distribution rules:

- `partition-discovery`

## Expansion Principle

Task diversity should come from changing budgets, allowed operations,
observation policies, objectives, and hidden parameters inside the same world.
This makes learned local world models transferable across tasks.
