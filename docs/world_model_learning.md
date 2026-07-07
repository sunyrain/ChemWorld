# World-Model Learning

ChemWorld is meant to evaluate local world-model learning under finite
experimental budget.

Agents never need to recover the full hidden simulator. A good local model
should instead support decisions such as:

- which reaction conditions are promising;
- where measurement uncertainty is still high;
- when high temperature or concentration becomes unsafe;
- which solvent/catalyst interaction appears beneficial;
- how product partitions between aqueous and organic phases;
- whether purification improves final score after recovery and cost penalties.

## Data Available To Learners

Trajectory records provide:

- action and operation type;
- public observation values;
- observed mask;
- raw instrument signal summaries;
- processed estimates;
- uncertainty metadata;
- cost, risk, and sample ledgers;
- constitution and precondition results.

They do not expose hidden rate parameters, true species amounts, or unmeasured
phase amounts in normal runs.

## Surrogate Interface

Surrogate models can implement:

```python
fit(trajectory)
predict(action_or_recipe)
uncertainty(action_or_recipe)
recommend(history, constraints)
```

This interface is intentionally broad enough for student models, Bayesian
optimization, random-forest surrogates, and LLM/tool agents.

The public interfaces live in `chemworld.models`, not in
`chemworld.foundation`. Foundation describes the hidden world and its laws;
models describe a learner's local approximation of that world.
